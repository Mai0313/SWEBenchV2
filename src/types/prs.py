from enum import Enum
from datetime import datetime

from pydantic import Field, BaseModel, ConfigDict, AliasChoices


class UserType(str, Enum):
    user = "User"
    bot = "Bot"
    org = "Organization"


class PRState(str, Enum):
    open = "open"
    closed = "closed"


class AuthorAssociation(str, Enum):
    owner = "OWNER"
    collaborator = "COLLABORATOR"
    contributor = "CONTRIBUTOR"
    first_time_contributor = "FIRST_TIME_CONTRIBUTOR"
    first_timer = "FIRST_TIMER"
    member = "MEMBER"
    none = "NONE"


class User(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    login: str = Field(..., description="GitHub username")
    id: int = Field(..., description="Unique user ID")
    node_id: str = Field(..., description="GraphQL node ID")
    avatar_url: str = Field(..., description="URL to user's avatar image")
    gravatar_id: str = Field(..., description="Gravatar ID (usually empty)")
    url: str = Field(..., description="API URL for user")
    html_url: str = Field(..., description="GitHub profile URL")
    followers_url: str = Field(..., description="API URL for user's followers")
    following_url: str = Field(..., description="API URL for users this user follows")
    gists_url: str = Field(..., description="API URL for user's gists")
    starred_url: str = Field(..., description="API URL for user's starred repositories")
    subscriptions_url: str = Field(..., description="API URL for user's subscriptions")
    organizations_url: str = Field(..., description="API URL for user's organizations")
    repos_url: str = Field(..., description="API URL for user's repositories")
    events_url: str = Field(..., description="API URL for user's events")
    received_events_url: str = Field(..., description="API URL for events received by user")
    type: UserType = Field(..., description="Type of user account")
    site_admin: bool = Field(..., description="Whether user is a GitHub site admin")


class License(BaseModel):
    key: str = Field(default="", description="License key identifier")
    name: str = Field(default="", description="Full license name")
    url: str = Field(default="", description="API URL for license details")
    spdx_id: str = Field(default="", description="SPDX license identifier")
    node_id: str = Field(default="", description="GraphQL node ID")
    html_url: str = Field(default="", description="GitHub URL for license details")


class Permissions(BaseModel):
    admin: bool = Field(default=False, description="Whether user has admin permissions")
    push: bool = Field(default=False, description="Whether user can push to repository")
    pull: bool = Field(default=False, description="Whether user can pull from repository")


class Repository(BaseModel):
    id: int = Field(..., description="Unique repository ID")
    node_id: str = Field(..., description="GraphQL node ID")
    name: str = Field(..., description="Repository name")
    full_name: str = Field(..., description="Full repository name (owner/repo)")
    owner: User = Field(..., description="Repository owner")
    private: bool = Field(..., description="Whether repository is private")
    html_url: str = Field(..., description="GitHub repository URL")
    description: str | None = Field(default=None, description="Repository description")
    fork: bool = Field(..., description="Whether repository is a fork")
    url: str = Field(..., description="API URL for repository")
    archive_url: str = Field(..., description="API URL template for repository archives")
    assignees_url: str = Field(..., description="API URL template for assignees")
    blobs_url: str = Field(..., description="API URL template for blobs")
    branches_url: str = Field(..., description="API URL template for branches")
    collaborators_url: str = Field(..., description="API URL template for collaborators")
    comments_url: str = Field(..., description="API URL template for comments")
    commits_url: str = Field(..., description="API URL template for commits")
    compare_url: str = Field(..., description="API URL template for comparing branches")
    contents_url: str = Field(..., description="API URL template for repository contents")
    contributors_url: str = Field(..., description="API URL for contributors")
    deployments_url: str = Field(..., description="API URL for deployments")
    downloads_url: str = Field(..., description="API URL for downloads")
    events_url: str = Field(..., description="API URL for repository events")
    forks_url: str = Field(..., description="API URL for repository forks")
    git_commits_url: str = Field(..., description="API URL template for git commits")
    git_refs_url: str = Field(..., description="API URL template for git references")
    git_tags_url: str = Field(..., description="API URL template for git tags")
    git_url: str = Field(..., description="Git clone URL")
    issue_comment_url: str = Field(..., description="API URL template for issue comments")
    issue_events_url: str = Field(..., description="API URL template for issue events")
    issues_url: str = Field(..., description="API URL template for issues")
    keys_url: str = Field(..., description="API URL template for deploy keys")
    labels_url: str = Field(..., description="API URL template for labels")
    languages_url: str = Field(..., description="API URL for repository languages")
    merges_url: str = Field(..., description="API URL for merges")
    milestones_url: str = Field(..., description="API URL template for milestones")
    notifications_url: str = Field(..., description="API URL for notifications")
    pulls_url: str = Field(..., description="API URL template for pull requests")
    releases_url: str = Field(..., description="API URL template for releases")
    ssh_url: str = Field(..., description="SSH clone URL")
    stargazers_url: str = Field(..., description="API URL for stargazers")
    statuses_url: str = Field(..., description="API URL template for statuses")
    subscribers_url: str = Field(..., description="API URL for subscribers")
    subscription_url: str = Field(..., description="API URL for subscription")
    tags_url: str = Field(..., description="API URL for tags")
    teams_url: str = Field(..., description="API URL for teams")
    trees_url: str = Field(..., description="API URL template for git trees")
    clone_url: str = Field(..., description="HTTPS clone URL")
    mirror_url: str | None = Field(default=None, description="Mirror repository URL")
    hooks_url: str = Field(..., description="API URL for webhooks")
    svn_url: str = Field(..., description="SVN checkout URL")
    homepage: str | None = Field(default=None, description="Repository homepage URL")
    language: str | None = Field(default=None, description="Primary programming language")
    forks_count: int = Field(..., description="Number of forks")
    stargazers_count: int = Field(..., description="Number of stargazers")
    watchers_count: int = Field(..., description="Number of watchers")
    size: int = Field(..., description="Repository size in KB")
    default_branch: str = Field(..., description="Default branch name")
    open_issues_count: int = Field(..., description="Number of open issues")
    is_template: bool = Field(..., description="Whether repository is a template")
    topics: list[str] = Field(default_factory=list, description="Repository topics")
    has_issues: bool = Field(..., description="Whether issues are enabled")
    has_projects: bool = Field(..., description="Whether projects are enabled")
    has_wiki: bool = Field(..., description="Whether wiki is enabled")
    has_pages: bool = Field(..., description="Whether GitHub Pages is enabled")
    has_downloads: bool = Field(..., description="Whether downloads are enabled")
    archived: bool = Field(..., description="Whether repository is archived")
    disabled: bool = Field(..., description="Whether repository is disabled")
    visibility: str = Field(..., description="Repository visibility (public/private/internal)")
    pushed_at: datetime = Field(..., description="Last push timestamp")
    created_at: datetime = Field(..., description="Repository creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    permissions: Permissions = Field(
        default_factory=Permissions, description="User permissions on repository"
    )
    allow_rebase_merge: bool = Field(default=False, description="Whether rebase merge is allowed")
    template_repository: dict | None = Field(
        default=None, description="Template repository if this is from template"
    )
    temp_clone_token: str | None = Field(default=None, description="Temporary clone token")
    allow_squash_merge: bool = Field(default=False, description="Whether squash merge is allowed")
    allow_auto_merge: bool = Field(default=False, description="Whether auto-merge is allowed")
    delete_branch_on_merge: bool = Field(
        default=False, description="Whether to delete branch on merge"
    )
    allow_merge_commit: bool = Field(default=False, description="Whether merge commit is allowed")
    subscribers_count: int = Field(default=0, description="Number of subscribers")
    network_count: int = Field(default=0, description="Network count")
    license: License | None = Field(default=None, description="Repository license")
    forks: int = Field(..., description="Number of forks")
    open_issues: int = Field(..., description="Number of open issues")
    watchers: int = Field(..., description="Number of watchers")


class Label(BaseModel):
    id: int = Field(..., description="Unique label ID")
    node_id: str = Field(..., description="GraphQL node ID")
    url: str = Field(..., description="API URL for label")
    name: str = Field(..., description="Label name")
    description: str | None = Field(default=None, description="Label description")
    color: str = Field(..., description="Label color (hex code without #)")
    default: bool = Field(..., description="Whether this is a default label")


class Milestone(BaseModel):
    url: str = Field(..., description="API URL for milestone")
    html_url: str = Field(..., description="GitHub URL for milestone")
    labels_url: str = Field(..., description="API URL for milestone labels")
    id: int = Field(..., description="Unique milestone ID")
    node_id: str = Field(..., description="GraphQL node ID")
    number: int = Field(..., description="Milestone number")
    state: str = Field(..., description="Milestone state (open/closed)")
    title: str = Field(..., description="Milestone title")
    description: str | None = Field(default=None, description="Milestone description")
    creator: User = Field(..., description="User who created the milestone")
    open_issues: int = Field(..., description="Number of open issues in milestone")
    closed_issues: int = Field(..., description="Number of closed issues in milestone")
    created_at: datetime = Field(..., description="Milestone creation timestamp")
    updated_at: datetime = Field(..., description="Milestone last update timestamp")
    closed_at: datetime | None = Field(default=None, description="Milestone close timestamp")
    due_on: datetime | None = Field(default=None, description="Milestone due date")


class Team(BaseModel):
    id: int = Field(..., description="Unique team ID")
    node_id: str = Field(..., description="GraphQL node ID")
    url: str = Field(..., description="API URL for team")
    html_url: str = Field(..., description="GitHub URL for team")
    name: str = Field(..., description="Team name")
    slug: str = Field(..., description="Team slug")
    description: str | None = Field(default=None, description="Team description")
    privacy: str = Field(..., description="Team privacy setting (open/closed/secret)")
    permission: str = Field(..., description="Team permission level")
    notification_setting: str = Field(..., description="Team notification setting")
    members_url: str = Field(..., description="API URL template for team members")
    repositories_url: str = Field(..., description="API URL for team repositories")
    parent: dict | None = Field(default=None, description="Parent team if this is a child team")


class BranchReference(BaseModel):
    label: str = Field(..., description="Branch label (owner:branch)")
    ref: str = Field(..., description="Branch reference name")
    sha: str = Field(..., description="Commit SHA")
    user: User = Field(..., description="User who owns the branch")
    repo: Repository | None = Field(default=None, description="Repository containing the branch")


class Links(BaseModel):
    self_link: dict = Field(
        ..., validation_alias=AliasChoices("self", "self_link"), description="Self link"
    )
    html: dict = Field(..., description="HTML link")
    issue: dict = Field(..., description="Issue link")
    comments: dict = Field(..., description="Comments link")
    review_comments: dict = Field(..., description="Review comments link")
    review_comment: dict = Field(..., description="Review comment template link")
    commits: dict = Field(..., description="Commits link")
    statuses: dict = Field(..., description="Statuses link")


class PullRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    url: str = Field(..., description="API URL for pull request")
    id: int = Field(..., description="Unique pull request ID")
    node_id: str = Field(..., description="GraphQL node ID")
    html_url: str = Field(..., description="GitHub URL for pull request")
    diff_url: str = Field(..., description="Diff URL for pull request")
    patch_url: str = Field(..., description="Patch URL for pull request")
    issue_url: str = Field(..., description="API URL for associated issue")
    commits_url: str = Field(..., description="API URL for pull request commits")
    review_comments_url: str = Field(..., description="API URL for review comments")
    review_comment_url: str = Field(..., description="API URL template for review comments")
    comments_url: str = Field(..., description="API URL for issue comments")
    statuses_url: str = Field(..., description="API URL for commit statuses")
    number: int = Field(..., description="Pull request number")
    state: PRState = Field(..., description="Pull request state")
    locked: bool = Field(..., description="Whether pull request is locked")
    title: str = Field(..., description="Pull request title")
    user: User = Field(..., description="User who created the pull request")
    body: str | None = Field(default="", description="Pull request body/description")
    labels: list[Label] = Field(default_factory=list, description="Labels applied to pull request")
    milestone: Milestone | None = Field(
        default=None, description="Milestone assigned to pull request"
    )
    active_lock_reason: str | None = Field(
        default=None, description="Reason for locking (if locked)"
    )
    created_at: datetime = Field(..., description="Pull request creation timestamp")
    updated_at: datetime = Field(..., description="Pull request last update timestamp")
    closed_at: datetime | None = Field(default=None, description="Pull request close timestamp")
    merged_at: datetime | None = Field(default=None, description="Pull request merge timestamp")
    merge_commit_sha: str | None = Field(default=None, description="SHA of merge commit")
    assignee: User | None = Field(default=None, description="Primary assignee")
    assignees: list[User] = Field(default_factory=list, description="All assignees")
    requested_reviewers: list[User] = Field(
        default_factory=list, description="Requested reviewers"
    )
    requested_teams: list[Team] = Field(
        default_factory=list, description="Requested team reviewers"
    )
    head: BranchReference = Field(..., description="Head branch (source)")
    base: BranchReference = Field(..., description="Base branch (target)")
    links: Links = Field(
        ..., validation_alias=AliasChoices("_links", "links"), description="Related links"
    )
    author_association: AuthorAssociation = Field(
        ..., description="Author's association with repository"
    )
    auto_merge: dict | None = Field(default=None, description="Auto-merge configuration")
    draft: bool = Field(..., description="Whether pull request is a draft")
