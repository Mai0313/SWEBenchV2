from enum import Enum
from datetime import datetime

from pydantic import Field, BaseModel, ConfigDict


class UserType(str, Enum):
    user = "user"
    bot = "bot"
    org = "organization"


class PRState(str, Enum):
    open = "open"
    closed = "closed"


class Visibility(str, Enum):
    public = "public"
    private = "private"
    limited = "limited"


class GiteaUser(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: int = Field(..., description="Unique user ID")
    login: str = Field(..., description="Username")
    login_name: str = Field(default="", description="Login name (often empty)")
    source_id: int = Field(default=0, description="Source ID for external auth")
    full_name: str = Field(default="", description="User's full display name")
    email: str = Field(default="", description="User's email address")
    avatar_url: str = Field(..., description="URL to user's avatar image")
    html_url: str = Field(..., description="Gitea profile URL")
    language: str = Field(default="", description="User's preferred language")
    is_admin: bool = Field(default=False, description="Whether user is a Gitea admin")
    last_login: datetime = Field(..., description="Last login timestamp")
    created: datetime = Field(..., description="Account creation timestamp")
    restricted: bool = Field(default=False, description="Whether user is restricted")
    active: bool = Field(default=True, description="Whether user account is active")
    prohibit_login: bool = Field(default=False, description="Whether login is prohibited")
    location: str = Field(default="", description="User's location")
    website: str = Field(default="", description="User's website URL")
    description: str = Field(default="", description="User's bio/description")
    visibility: Visibility = Field(default=Visibility.public, description="User visibility")
    followers_count: int = Field(default=0, description="Number of followers")
    following_count: int = Field(default=0, description="Number of users following")
    starred_repos_count: int = Field(default=0, description="Number of starred repositories")
    username: str = Field(..., description="Username (alias for login)")


class GiteaPermissions(BaseModel):
    admin: bool = Field(default=False, description="Whether user has admin permissions")
    push: bool = Field(default=False, description="Whether user can push to repository")
    pull: bool = Field(default=True, description="Whether user can pull from repository")


class GiteaRepository(BaseModel):
    id: int = Field(..., description="Unique repository ID")
    owner: GiteaUser = Field(..., description="Repository owner")
    name: str = Field(..., description="Repository name")
    full_name: str = Field(..., description="Full repository name (owner/repo)")
    description: str = Field(default="", description="Repository description")
    empty: bool = Field(default=False, description="Whether repository is empty")
    private: bool = Field(default=False, description="Whether repository is private")
    fork: bool = Field(default=False, description="Whether repository is a fork")
    template: bool = Field(default=False, description="Whether repository is a template")
    parent: dict | None = Field(default=None, description="Parent repository if fork")
    mirror: bool = Field(default=False, description="Whether repository is a mirror")
    size: int = Field(default=0, description="Repository size in KB")
    language: str = Field(default="", description="Primary programming language")
    languages_url: str = Field(..., description="API URL for repository languages")
    html_url: str = Field(..., description="Gitea repository URL")
    url: str = Field(..., description="API URL for repository")
    link: str = Field(default="", description="Repository link")
    ssh_url: str = Field(..., description="SSH clone URL")
    clone_url: str = Field(..., description="HTTPS clone URL")
    original_url: str = Field(default="", description="Original repository URL")
    website: str = Field(default="", description="Repository homepage URL")
    stars_count: int = Field(default=0, description="Number of stars")
    forks_count: int = Field(default=0, description="Number of forks")
    watchers_count: int = Field(default=0, description="Number of watchers")
    open_issues_count: int = Field(default=0, description="Number of open issues")
    open_pr_counter: int = Field(default=0, description="Number of open pull requests")
    release_counter: int = Field(default=0, description="Number of releases")
    default_branch: str = Field(default="main", description="Default branch name")
    archived: bool = Field(default=False, description="Whether repository is archived")
    created_at: datetime = Field(..., description="Repository creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    archived_at: datetime = Field(..., description="Archive timestamp")
    permissions: GiteaPermissions = Field(
        default_factory=GiteaPermissions, description="User permissions on repository"
    )
    has_issues: bool = Field(default=True, description="Whether issues are enabled")
    has_wiki: bool = Field(default=False, description="Whether wiki is enabled")
    has_pull_requests: bool = Field(default=True, description="Whether PRs are enabled")
    has_projects: bool = Field(default=True, description="Whether projects are enabled")
    projects_mode: str = Field(default="all", description="Projects mode setting")
    has_releases: bool = Field(default=True, description="Whether releases are enabled")
    has_packages: bool = Field(default=False, description="Whether packages are enabled")
    has_actions: bool = Field(default=True, description="Whether actions are enabled")
    ignore_whitespace_conflicts: bool = Field(
        default=False, description="Whether to ignore whitespace conflicts"
    )
    allow_merge_commits: bool = Field(
        default=False, description="Whether merge commits are allowed"
    )
    allow_rebase: bool = Field(default=False, description="Whether rebase is allowed")
    allow_rebase_explicit: bool = Field(
        default=False, description="Whether explicit rebase is allowed"
    )
    allow_squash_merge: bool = Field(default=True, description="Whether squash merge is allowed")
    allow_fast_forward_only_merge: bool = Field(
        default=False, description="Whether fast-forward only merge is allowed"
    )
    allow_rebase_update: bool = Field(default=True, description="Whether rebase update is allowed")
    allow_manual_merge: bool = Field(default=False, description="Whether manual merge is allowed")
    autodetect_manual_merge: bool = Field(
        default=False, description="Whether to autodetect manual merge"
    )
    default_delete_branch_after_merge: bool = Field(
        default=True, description="Whether to delete branch after merge by default"
    )
    default_merge_style: str = Field(default="squash", description="Default merge style")
    default_allow_maintainer_edit: bool = Field(
        default=False, description="Whether maintainer edit is allowed by default"
    )
    avatar_url: str = Field(default="", description="Repository avatar URL")
    internal: bool = Field(default=False, description="Whether repository is internal")
    mirror_interval: str = Field(default="", description="Mirror sync interval")
    object_format_name: str = Field(default="sha1", description="Git object format")
    mirror_updated: datetime = Field(..., description="Last mirror update timestamp")
    repo_transfer: dict | None = Field(default=None, description="Repository transfer info")
    topics: list[str] = Field(default_factory=list, description="Repository topics")
    licenses: list[str] = Field(default_factory=list, description="Repository licenses")


class GiteaBranchReference(BaseModel):
    label: str = Field(..., description="Branch label")
    ref: str = Field(..., description="Branch reference name")
    sha: str = Field(..., description="Commit SHA")
    repo_id: int = Field(..., description="Repository ID")
    repo: GiteaRepository = Field(..., description="Repository containing the branch")


class GiteaPullRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    id: int = Field(..., description="Unique pull request ID")
    url: str = Field(..., description="Gitea URL for pull request")
    number: int = Field(..., description="Pull request number")
    user: GiteaUser = Field(..., description="User who created the pull request")
    title: str = Field(..., description="Pull request title")
    body: str = Field(default="", description="Pull request body/description")
    labels: list[dict] = Field(default_factory=list, description="Labels applied to pull request")
    milestone: dict | None = Field(default=None, description="Associated milestone")
    assignee: GiteaUser | None = Field(default=None, description="Primary assignee")
    assignees: list[GiteaUser] | None = Field(default=None, description="All assignees")
    requested_reviewers: list[GiteaUser] | None = Field(
        default=None, description="Requested reviewers"
    )
    requested_reviewers_teams: list[dict] | None = Field(
        default=None, description="Requested team reviewers"
    )
    state: PRState = Field(..., description="Pull request state")
    draft: bool = Field(default=False, description="Whether pull request is a draft")
    is_locked: bool = Field(default=False, description="Whether pull request is locked")
    comments: int = Field(default=0, description="Number of comments")
    html_url: str = Field(..., description="Gitea web URL for pull request")
    diff_url: str = Field(..., description="Diff URL for pull request")
    patch_url: str = Field(..., description="Patch URL for pull request")
    mergeable: bool = Field(default=True, description="Whether pull request can be merged")
    merged: bool = Field(default=False, description="Whether pull request has been merged")
    merged_at: datetime | None = Field(default=None, description="Merge timestamp")
    merge_commit_sha: str | None = Field(default=None, description="SHA of merge commit")
    merged_by: GiteaUser | None = Field(default=None, description="User who performed merge")
    allow_maintainer_edit: bool = Field(default=False, description="Whether maintainers can edit")
    base: GiteaBranchReference = Field(..., description="Base branch (target)")
    head: GiteaBranchReference = Field(..., description="Head branch (source)")
    merge_base: str = Field(..., description="Base commit for merge")
    due_date: datetime | None = Field(default=None, description="Due date")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    closed_at: datetime | None = Field(default=None, description="Close timestamp")
    pin_order: int = Field(default=0, description="Pin order")
