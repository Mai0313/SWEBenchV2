import os
import json
import time
import base64
from typing import Any
from pathlib import Path
from datetime import datetime

import logfire
from pydantic import Field, ConfigDict, computed_field
import requests
from pydantic_settings import BaseSettings

from src.types.models import PRInfo, FileData, TrainingData, ExtractionResult


class GitHubPRExtractor(BaseSettings):
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

    @computed_field
    @property
    def session(self) -> requests.Session:
        """Create a requests session with GitHub API headers.

        Returns:
            requests.Session: Configured session with GitHub API headers
        """
        headers: dict[str, str] = {"Accept": "application/vnd.github.v3+json"}

        if self.token:
            headers.update({"Authorization": f"Bearer {self.token}"})

        session = requests.Session()
        session.headers.update(headers)
        return session

    def get_merged_prs(
        self, repo_owner: str, repo_name: str, per_page: int = 100
    ) -> list[dict[str, Any]]:
        """Fetch all merged pull requests from a repository.

        Args:
            repo_owner (str): Repository owner username
            repo_name (str): Repository name
            per_page (int): Number of PRs per page (default: 100)

        Returns:
            List[Dict[str, Any]]: List of merged pull request data
        """
        all_prs: list[dict[str, Any]] = []
        page = 1

        while True:
            response = self.session.get(
                url=f"{self.base_url}/repos/{repo_owner}/{repo_name}/pulls",
                params={
                    "state": "closed",
                    "sort": "updated",
                    "direction": "desc",
                    "per_page": per_page,
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

            prs: list[dict[str, Any]] = response.json()
            if not prs:
                break

            # Only keep merged PRs
            merged_prs = [pr for pr in prs if pr["merged_at"] is not None]
            all_prs.extend(merged_prs)

            logfire.info(f"Page {page}: Found {len(merged_prs)} merged PRs")
            page += 1

            # Avoid making requests too quickly
            time.sleep(0.1)

        return all_prs

    def get_pr_files(
        self, repo_owner: str, repo_name: str, pr_number: int
    ) -> list[dict[str, Any]]:
        """Fetch the list of files modified in a pull request.

        Args:
            repo_owner (str): Repository owner username
            repo_name (str): Repository name
            pr_number (int): Pull request number

        Returns:
            List[Dict[str, Any]]: List of modified files information
        """
        response = self.session.get(
            url=f"{self.base_url}/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files"
        )

        if response.status_code != 200:
            logfire.error(f"Error fetching PR files: {response.status_code}")
            return []

        return response.json()

    def get_file_content(
        self, repo_owner: str, repo_name: str, file_path: str, sha: str
    ) -> str | None:
        """Fetch file content at a specific commit SHA.

        Args:
            repo_owner (str): Repository owner username
            repo_name (str): Repository name
            file_path (str): Path to the file
            sha (str): Commit SHA

        Returns:
            Optional[str]: File content or None if failed to fetch
        """
        response = self.session.get(
            url=f"{self.base_url}/repos/{repo_owner}/{repo_name}/contents/{file_path}",
            params={"ref": sha},
        )

        if response.status_code != 200:
            return None

        file_info: dict[str, Any] = response.json()
        if file_info.get("encoding") == "base64":
            content = base64.b64decode(file_info["content"]).decode("utf-8")
            return content

        return file_info.get("content", "")

    def extract_pr_data(
        self, repo_owner: str, repo_name: str, pr: dict[str, Any]
    ) -> TrainingData | None:
        """Extract detailed data for a single pull request.

        Args:
            repo_owner (str): Repository owner username
            repo_name (str): Repository name
            pr (Dict[str, Any]): Pull request data from GitHub API

        Returns:
            Optional[TrainingData]: Training data for the PR or None if failed
        """
        pr_number = pr["number"]
        logfire.info(f"Processing PR #{pr_number}: {pr['title']}")

        # Get PR modified files
        files_data: list[dict[str, Any]] = self.get_pr_files(repo_owner, repo_name, pr_number)

        if not files_data:
            return None

        # Get PR detailed information
        pr_url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
        pr_response = self.session.get(pr_url)

        if pr_response.status_code != 200:
            return None

        pr_detail: dict[str, Any] = pr_response.json()

        # Build PR info
        pr_info = PRInfo(
            number=pr_number,
            title=pr["title"],
            body=pr["body"] or "",
            url=pr["html_url"],
            created_at=pr["created_at"],
            merged_at=pr["merged_at"],
            author=pr["user"]["login"],
            base_branch=pr["base"]["ref"],
            head_branch=pr["head"]["ref"],
            base_sha=pr["base"]["sha"],
            head_sha=pr["head"]["sha"],
        )

        # Build training data
        training_data = TrainingData(pr_info=pr_info, question=self.format_question(pr), files=[])

        # Process each modified file
        for file_info in files_data:
            if file_info["status"] == "removed":
                # File was deleted
                before_content = self.get_file_content(
                    repo_owner, repo_name, file_info["filename"], pr["base"]["sha"]
                )

                file_data = FileData(
                    filename=file_info["filename"],
                    status=file_info["status"],
                    additions=file_info["additions"],
                    deletions=file_info["deletions"],
                    changes=file_info["changes"],
                    before_content=before_content or "",
                    after_content="",
                    patch=file_info.get("patch", ""),
                )

            elif file_info["status"] == "added":
                # File was added
                after_content = self.get_file_content(
                    repo_owner, repo_name, file_info["filename"], pr["head"]["sha"]
                )

                file_data = FileData(
                    filename=file_info["filename"],
                    status=file_info["status"],
                    additions=file_info["additions"],
                    deletions=file_info["deletions"],
                    changes=file_info["changes"],
                    before_content="",
                    after_content=after_content or "",
                    patch=file_info.get("patch", ""),
                )

            else:
                # File was modified
                before_content = self.get_file_content(
                    repo_owner, repo_name, file_info["filename"], pr["base"]["sha"]
                )
                after_content = self.get_file_content(
                    repo_owner, repo_name, file_info["filename"], pr["head"]["sha"]
                )

                file_data = FileData(
                    filename=file_info["filename"],
                    status=file_info["status"],
                    additions=file_info["additions"],
                    deletions=file_info["deletions"],
                    changes=file_info["changes"],
                    before_content=before_content or "",
                    after_content=after_content or "",
                    patch=file_info.get("patch", ""),
                )

            training_data.files.append(file_data)

            # Avoid making requests too quickly
            time.sleep(0.1)

        return training_data

    def format_question(self, pr: dict[str, Any]) -> str:
        """Format a question based on PR information.

        Args:
            pr (Dict[str, Any]): Pull request data from GitHub API

        Returns:
            str: Formatted question string
        """
        question = f"PR #{pr['number']}: {pr['title']}"
        if pr["body"]:
            question += f"\n\nDescription:\n{pr['body']}"
        return question

    def save_to_json(self, data: ExtractionResult, filename: str) -> None:
        """Save extraction result to JSON file.

        Args:
            data (ExtractionResult): Extraction result to save
            filename (str): Output filename
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data.model_dump(), f, ensure_ascii=False, indent=2)
        logfire.info(f"Data saved to {filename}")

    def extract_all_pr_data(self, repo_url: str) -> ExtractionResult:
        """Extract all PR data from a repository.

        Args:
            repo_url (str): GitHub repository URL

        Returns:
            ExtractionResult: Complete extraction result
        """
        # Parse repository URL
        parts = repo_url.replace("https://github.com/", "").split("/")
        repo_owner, repo_name = parts[0], parts[1]
        output_file = Path(f"./data/{repo_owner}_{repo_name}_pr_training_data.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        logfire.info(f"Extracting data from {repo_owner}/{repo_name}")

        # Get all merged PRs
        merged_prs = self.get_merged_prs(repo_owner=repo_owner, repo_name=repo_name)
        logfire.info(f"Found {len(merged_prs)} merged PRs")

        # Extract detailed data for each PR
        all_training_data: list[TrainingData] = []

        for idx, pr in enumerate(merged_prs):
            pr_data = self.extract_pr_data(repo_owner, repo_name, pr)
            if pr_data:
                all_training_data.append(pr_data)

            logfire.info(f"Processed {idx + 1}/{len(merged_prs)} PRs")

            # Save every 10 PRs to prevent data loss
            if (idx + 1) % 10 == 0:
                temp_result = ExtractionResult(
                    repository=f"{repo_owner}/{repo_name}",
                    extracted_at=datetime.now().isoformat(),
                    total_prs=len(all_training_data),
                    prs=all_training_data,
                )
                temp_file = f"temp_{output_file}"
                self.save_to_json(temp_result, temp_file)

        # Create final result
        final_data = ExtractionResult(
            repository=f"{repo_owner}/{repo_name}",
            extracted_at=datetime.now().isoformat(),
            total_prs=len(all_training_data),
            prs=all_training_data,
        )

        self.save_to_json(final_data, output_file)

        # Clean up temporary file
        temp_file = f"temp_{output_file}"
        if os.path.exists(temp_file):
            os.remove(temp_file)

        return final_data
