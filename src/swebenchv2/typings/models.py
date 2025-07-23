"""Pydantic models for GitHub PR data extraction."""

import json
import asyncio
from pathlib import Path
from datetime import datetime

from pydantic import Field, BaseModel

from swebenchv2.typings.prs import PullRequest


class FileData(BaseModel):
    sha: str = Field(..., description="File SHA")
    filename: str = Field(..., description="File path and name")
    status: str = Field(..., description="File status (added, modified, removed)")
    additions: int = Field(..., description="Number of lines added")
    deletions: int = Field(..., description="Number of lines deleted")
    changes: int = Field(..., description="Total number of changes")
    blob_url: str = Field(..., description="Blob URL for the file")
    raw_url: str = Field(..., description="Raw URL for the file content")
    contents_url: str = Field(..., description="Contents URL for the file")
    before_edit: str = Field(default="", description="File content before changes")
    after_edit: str = Field(default="", description="File content after changes")
    patch: str = Field(default="", description="Git patch/diff")


class TrainingData(BaseModel):
    pr_info: PullRequest = Field(..., description="Pull request information", exclude=True)
    question: str = Field(..., description="Formatted question based on PR title and description")
    files: list[FileData] = Field(default=[], description="List of modified files")


class ExtractionResult(BaseModel):
    repository: str = Field(..., description="Repository name in format owner/repo")
    extracted_at: str = Field(..., description="Extraction timestamp")
    total_prs: int = Field(..., description="Total number of PRs processed")
    prs: list[TrainingData] = Field(default=[], description="List of training data for each PR")

    def save_log(self) -> Path:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_log = Path(f"./data/{self.repository}/log_{now}.json")
        output_log.parent.mkdir(parents=True, exist_ok=True)
        log_dict = self.model_dump(mode="json", exclude_none=True, exclude_unset=True)
        output_log.write_text(json.dumps(log_dict, ensure_ascii=False, indent=2), encoding="utf-8")
        return output_log

    async def a_save_log(self) -> Path:
        return await asyncio.to_thread(self.save_log)
