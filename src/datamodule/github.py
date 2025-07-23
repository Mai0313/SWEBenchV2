import time
import base64
from typing import Any
import asyncio
from datetime import datetime
from functools import cached_property
from urllib.parse import urlparse

import httpx
import dotenv
import logfire
from pydantic import Field, ConfigDict, computed_field
from pydantic_settings import BaseSettings

from src.types.prs import PullRequest
from src.types.limit import RateLimit
from src.types.models import FileData, TrainingData, ExtractionResult

dotenv.load_dotenv()


class GitHubPRExtractorBase(BaseSettings):
    """GitHub PR data extractor for creating LLM training datasets.

    This class extracts merged pull requests from a GitHub repository
    and formats them into training data with before/after file contents.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    token: str | None = Field(
        default=None,
        validation_alias="GITHUB_TOKEN",
        description="GitHub API token for authentication",
        frozen=False,
        deprecated=False,
    )
    base_url: str = Field(
        default="https://api.github.com",
        validation_alias="GITHUB_API_BASE_URL",
        description="Base URL for GitHub API",
        frozen=False,
        deprecated=False,
    )
    repo_url: str = Field(
        ...,
        title="Github Repository URL",
        description="This should be a full url to the repository, e.g. `https://github.com/Mai0313/SWEBenchV2`",
        frozen=False,
        deprecated=False,
    )
    max_page: int | None = Field(
        default=None,
        title="Max Page",
        description="Maximum number of pages to fetch for PRs",
        frozen=False,
        deprecated=False,
    )
    per_page: int | None = Field(
        default=None,
        title="Per Page",
        description="Number of PRs to fetch per page",
        frozen=False,
        deprecated=False,
    )

    @computed_field
    @cached_property
    def repo_owner(self) -> str:
        """Return the number of PRs to fetch per page."""
        parsed_url = urlparse(url=self.repo_url)
        return parsed_url.path.strip("/").split("/")[0]

    @computed_field
    @cached_property
    def repo_name(self) -> str:
        """Return the number of PRs to fetch per page."""
        parsed_url = urlparse(url=self.repo_url)
        return parsed_url.path.strip("/").split("/")[1]

    @computed_field
    @cached_property
    def _max_page(self) -> int:
        """Return the maximum number of pages to fetch."""
        return self.max_page if self.max_page is not None else int(1e6)

    @computed_field
    @cached_property
    def _per_page(self) -> int:
        """Return the number of PRs to fetch per page."""
        return self.per_page if self.per_page is not None else 100

    @computed_field
    @cached_property
    def headers(self) -> dict[str, Any]:
        headers: dict[str, str] = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers.update({"Authorization": f"Bearer {self.token}"})
        return headers


class GitHubPRExtractor(GitHubPRExtractorBase):
    def get_rate_limit(self) -> RateLimit:
        with httpx.Client(base_url=self.base_url, headers=self.headers, timeout=10) as client:
            response = client.get("/rate_limit")
            rate_limit = RateLimit(**response.json())
            logfire.info("Rate limit info", **rate_limit.rate.model_dump())
            return rate_limit

    def get_merged_prs(self) -> list[PullRequest]:
        all_prs: list[PullRequest] = []
        page = 1

        with httpx.Client(base_url=self.base_url, headers=self.headers, timeout=10) as client:
            while True:
                if page > self._max_page:
                    break

                response = client.get(
                    url=f"/repos/{self.repo_owner}/{self.repo_name}/pulls",
                    params={
                        "state": "closed",
                        "sort": "updated",
                        "direction": "desc",
                        "per_page": self._per_page + 1,
                        "page": page,
                    },
                )

                if response.status_code == 403:
                    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                    if reset_time:
                        wait_time = reset_time - int(time.time()) + 1
                        logfire.info(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue

                if response.status_code != 200:
                    logfire.error(f"Error fetching PRs: {response.status_code}")
                    break

                response_list: list[dict[str, Any]] = response.json()

                # Check if we've reached the end of available data
                if not response_list:
                    logfire.info(f"No more PRs found at page {page}. Stopping pagination.")
                    break

                # Only keep merged PRs
                merged_prs = [
                    PullRequest(**pr) for pr in response_list if pr.get("merged_at") is not None
                ]
                all_prs.extend(merged_prs)
                # Check Link header for pagination info
                link_header = response.headers.get("Link")
                if link_header and 'rel="next"' not in link_header:
                    logfire.info("Reached last page based on Link header.")
                    break
                page += 1
        logfire.info(
            f"Extracted {len(all_prs)} merged PRs from {self.repo_owner}/{self.repo_name}"
        )
        return all_prs

    def get_pr_files(self, pr_number: int) -> list[FileData]:
        with httpx.Client(base_url=self.base_url, headers=self.headers, timeout=10) as client:
            logfire.info(f"Fetching files for PR #{pr_number}")
            response = client.get(
                url=f"/repos/{self.repo_owner}/{self.repo_name}/pulls/{pr_number}/files"
            )
            if response.status_code != 200:
                logfire.error(f"Error fetching PR files: {response.status_code}")
                return []
            return [FileData(**file) for file in response.json()]

    def get_file_content(self, file_path: str, sha: str) -> str:
        with httpx.Client(base_url=self.base_url, headers=self.headers, timeout=10) as client:
            response = client.get(
                url=f"/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}",
                params={"ref": sha},
            )

            if response.status_code != 200:
                return ""

            file_info: dict[str, Any] = response.json()
            if file_info.get("encoding") == "base64":
                content = base64.b64decode(file_info["content"]).decode("utf-8")
                return content
            return file_info.get("content", "")

    def extract_pr_data(self, pr_info: PullRequest) -> TrainingData:
        # Get PR modified files
        files_data: list[FileData] = self.get_pr_files(pr_number=pr_info.number)

        for file_info in files_data:
            if file_info.status == "removed":
                # File was deleted
                file_info.before_edit = self.get_file_content(
                    file_path=file_info.filename, sha=pr_info.base.sha
                )
            elif file_info.status == "added":
                # File was added
                file_info.after_edit = self.get_file_content(
                    file_path=file_info.filename, sha=pr_info.head.sha
                )
            else:
                # File was modified
                file_info.before_edit = self.get_file_content(
                    file_path=file_info.filename, sha=pr_info.base.sha
                )
                file_info.after_edit = self.get_file_content(
                    file_path=file_info.filename, sha=pr_info.head.sha
                )

        # Build training data
        question = f"PR#{pr_info.number}\nTitle:\n{pr_info.title}\nDescription:\n{pr_info.body}"
        training_data = TrainingData(pr_info=pr_info, question=question, files=files_data)
        return training_data

    def extract_all_pr_data(self, save_json: bool) -> ExtractionResult:
        logfire.info(f"Extracting data from {self.repo_owner}/{self.repo_name}")
        # Get all merged PRs
        merged_prs = self.get_merged_prs()
        logfire.info(f"Found {len(merged_prs)} merged PRs")

        # Extract detailed data for each PR
        all_training_data: list[TrainingData] = []

        for pr_info in merged_prs:
            pr_data = self.extract_pr_data(pr_info=pr_info)
            all_training_data.append(pr_data)

        data = ExtractionResult(
            repository=f"{self.repo_owner}/{self.repo_name}",
            extracted_at=datetime.now().isoformat(),
            total_prs=len(all_training_data),
            prs=all_training_data,
        )
        if save_json:
            data.save_log()
        return data


class AsyncGitHubPRExtractor(GitHubPRExtractorBase):
    async def get_rate_limit(self) -> RateLimit:
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.headers, timeout=10
        ) as client:
            response = await client.get("/rate_limit")
            rate_limit = RateLimit(**response.json())
            logfire.info("Rate limit info", **rate_limit.rate.model_dump())
            return rate_limit

    async def get_merged_prs(self) -> list[PullRequest]:
        all_prs: list[PullRequest] = []
        page = 1

        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.headers, timeout=10
        ) as client:
            while True:
                if page > self._max_page:
                    break

                response = await client.get(
                    url=f"/repos/{self.repo_owner}/{self.repo_name}/pulls",
                    params={
                        "state": "closed",
                        "sort": "updated",
                        "direction": "desc",
                        "per_page": self._per_page + 1,
                        "page": page,
                    },
                )

                if response.status_code == 403:
                    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                    if reset_time:
                        wait_time = reset_time - int(time.time()) + 1
                        logfire.info(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                        continue

                if response.status_code != 200:
                    logfire.error(f"Error fetching PRs: {response.status_code}")
                    break

                response_list: list[dict[str, Any]] = response.json()

                # Check if we've reached the end of available data
                if not response_list:
                    logfire.info(f"No more PRs found at page {page}. Stopping pagination.")
                    break

                # Only keep merged PRs
                merged_prs = [
                    PullRequest(**pr) for pr in response_list if pr.get("merged_at") is not None
                ]
                all_prs.extend(merged_prs)
                # Check Link header for pagination info
                link_header = response.headers.get("Link")
                if link_header and 'rel="next"' not in link_header:
                    logfire.info("Reached last page based on Link header.")
                    break
                page += 1
        logfire.info(
            f"Extracted {len(all_prs)} merged PRs from {self.repo_owner}/{self.repo_name}"
        )
        return all_prs

    async def get_pr_files(self, pr_number: int) -> list[FileData]:
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.headers, timeout=10
        ) as client:
            logfire.info(f"Fetching files for PR #{pr_number}")
            response = await client.get(
                url=f"/repos/{self.repo_owner}/{self.repo_name}/pulls/{pr_number}/files"
            )
            if response.status_code != 200:
                logfire.error(f"Error fetching PR files: {response.status_code}")
                return []
            return [FileData(**file) for file in response.json()]

    async def get_file_content(self, file_path: str, sha: str) -> str:
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.headers, timeout=10
        ) as client:
            response = await client.get(
                url=f"/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}",
                params={"ref": sha},
            )

            if response.status_code != 200:
                return ""

            file_info: dict[str, Any] = response.json()
            if file_info.get("encoding") == "base64":
                content = base64.b64decode(file_info["content"]).decode("utf-8")
                return content
            return file_info.get("content", "")

    async def extract_pr_data(self, pr_info: PullRequest) -> TrainingData:
        # Get PR modified files
        files_data: list[FileData] = await self.get_pr_files(pr_number=pr_info.number)

        for file_info in files_data:
            if file_info.status == "removed":
                # File was deleted
                file_info.before_edit = await self.get_file_content(
                    file_path=file_info.filename, sha=pr_info.base.sha
                )
            elif file_info.status == "added":
                # File was added
                file_info.after_edit = await self.get_file_content(
                    file_path=file_info.filename, sha=pr_info.head.sha
                )
            else:
                # File was modified
                file_info.before_edit = await self.get_file_content(
                    file_path=file_info.filename, sha=pr_info.base.sha
                )
                file_info.after_edit = await self.get_file_content(
                    file_path=file_info.filename, sha=pr_info.head.sha
                )

        # Build training data
        question = f"PR#{pr_info.number}\nTitle:\n{pr_info.title}\nDescription:\n{pr_info.body}"
        training_data = TrainingData(pr_info=pr_info, question=question, files=files_data)
        return training_data

    async def extract_all_pr_data(self, save_json: bool) -> ExtractionResult:
        logfire.info(f"Extracting data from {self.repo_owner}/{self.repo_name}")
        # Get all merged PRs
        merged_prs = await self.get_merged_prs()
        logfire.info(f"Found {len(merged_prs)} merged PRs")

        # Extract detailed data for each PR
        all_training_data: list[TrainingData] = []

        for pr_info in merged_prs:
            pr_data = await self.extract_pr_data(pr_info=pr_info)
            all_training_data.append(pr_data)

        data = ExtractionResult(
            repository=f"{self.repo_owner}/{self.repo_name}",
            extracted_at=datetime.now().isoformat(),
            total_prs=len(all_training_data),
            prs=all_training_data,
        )
        if save_json:
            data.save_log()
        return data
