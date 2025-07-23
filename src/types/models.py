"""Pydantic models for GitHub PR data extraction."""

from pydantic import Field, BaseModel


class UserInfo(BaseModel):
    """GitHub user information.

    Attributes:
        login (str): GitHub username
    """

    login: str = Field(..., description="GitHub username")


class BranchInfo(BaseModel):
    """Git branch information.

    Attributes:
        ref (str): Branch reference name
        sha (str): Git commit SHA
    """

    ref: str = Field(..., description="Branch reference name")
    sha: str = Field(..., description="Git commit SHA")


class PRInfo(BaseModel):
    """Pull request information.

    Attributes:
        number (int): PR number
        title (str): PR title
        body (str): PR description body
        url (str): PR HTML URL
        created_at (str): PR creation timestamp
        merged_at (Optional[str]): PR merge timestamp
        author (str): PR author username
        base_branch (str): Base branch name
        head_branch (str): Head branch name
        base_sha (str): Base branch commit SHA
        head_sha (str): Head branch commit SHA
    """

    number: int = Field(..., description="PR number")
    title: str = Field(..., description="PR title")
    body: str = Field(default="", description="PR description body")
    url: str = Field(..., description="PR HTML URL")
    created_at: str = Field(..., description="PR creation timestamp")
    merged_at: str | None = Field(default=None, description="PR merge timestamp")
    author: str = Field(..., description="PR author username")
    base_branch: str = Field(..., description="Base branch name")
    head_branch: str = Field(..., description="Head branch name")
    base_sha: str = Field(..., description="Base branch commit SHA")
    head_sha: str = Field(..., description="Head branch commit SHA")


class FileData(BaseModel):
    """File modification data.

    Attributes:
        filename (str): File path and name
        status (str): File status (added, modified, removed)
        additions (int): Number of lines added
        deletions (int): Number of lines deleted
        changes (int): Total number of changes
        before_content (str): File content before changes
        after_content (str): File content after changes
        patch (str): Git patch/diff
    """

    filename: str = Field(..., description="File path and name")
    status: str = Field(..., description="File status (added, modified, removed)")
    additions: int = Field(..., description="Number of lines added")
    deletions: int = Field(..., description="Number of lines deleted")
    changes: int = Field(..., description="Total number of changes")
    before_content: str = Field(default="", description="File content before changes")
    after_content: str = Field(default="", description="File content after changes")
    patch: str = Field(default="", description="Git patch/diff")


class TrainingData(BaseModel):
    """Training data for a single PR.

    Attributes:
        pr_info (PRInfo): Pull request information
        question (str): Formatted question based on PR title and description
        files (List[FileData]): List of modified files
    """

    pr_info: PRInfo = Field(..., description="Pull request information")
    question: str = Field(..., description="Formatted question based on PR title and description")
    files: list[FileData] = Field(default_factory=list, description="List of modified files")


class ExtractionResult(BaseModel):
    """Final extraction result.

    Attributes:
        repository (str): Repository name in format owner/repo
        extracted_at (str): Extraction timestamp
        total_prs (int): Total number of PRs processed
        prs (List[TrainingData]): List of training data for each PR
    """

    repository: str = Field(..., description="Repository name in format owner/repo")
    extracted_at: str = Field(..., description="Extraction timestamp")
    total_prs: int = Field(..., description="Total number of PRs processed")
    prs: list[TrainingData] = Field(
        default_factory=list, description="List of training data for each PR"
    )
