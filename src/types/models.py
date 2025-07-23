"""Pydantic models for GitHub PR data extraction."""

import json
from pathlib import Path
from datetime import datetime

from pydantic import Field, BaseModel

from src.types.prs import PullRequest


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
    before_content: str = Field(default="", description="File content before changes")
    after_content: str = Field(default="", description="File content after changes")
    patch: str = Field(default="", description="Git patch/diff")


class TrainingData(BaseModel):
    pr_info: PullRequest = Field(..., description="Pull request information")
    question: str = Field(..., description="Formatted question based on PR title and description")
    files: list[FileData] = Field(default_factory=list, description="List of modified files")


class ExtractionResult(BaseModel):
    repository: str = Field(..., description="Repository name in format owner/repo")
    extracted_at: str = Field(..., description="Extraction timestamp")
    total_prs: int = Field(..., description="Total number of PRs processed")
    prs: list[TrainingData] = Field(
        default_factory=list, description="List of training data for each PR"
    )

    def save(self) -> Path:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_log = Path(f"./data/{self.repository}/log_{now}.json")
        output_log.parent.mkdir(parents=True, exist_ok=True)
        log_dict = self.model_dump(mode="json", exclude_none=True, exclude_unset=True)
        with open(output_log, "w", encoding="utf-8") as f:
            json.dump(log_dict, f, ensure_ascii=False, indent=2)
        return output_log
