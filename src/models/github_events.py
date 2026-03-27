"""Pydantic models for GitHub webhook events.

These models represent the structure of GitHub webhook payloads
received by the notifier service.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class GitHubEventType(str, Enum):
    """Supported GitHub event types."""

    ISSUES = "issues"
    ISSUE_COMMENT = "issue_comment"
    PULL_REQUEST = "pull_request"
    PULL_REQUEST_REVIEW = "pull_request_review"
    PULL_REQUEST_REVIEW_COMMENT = "pull_request_review_comment"
    PUSH = "push"
    WORKFLOW_RUN = "workflow_run"
    LABEL = "label"


class GitHubAction(str, Enum):
    """Common GitHub actions within events."""

    OPENED = "opened"
    EDITED = "edited"
    CLOSED = "closed"
    REOPENED = "reopened"
    LABELED = "labeled"
    UNLABELED = "unlabeled"
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    CREATED = "created"
    DELETED = "deleted"
    SUBMITTED = "submitted"
    DISMISSED = "dismissed"
    SYNCHRONIZE = "synchronize"


class GitHubUser(BaseModel):
    """GitHub user model."""

    id: int
    login: str
    node_id: str | None = None
    avatar_url: str | None = None
    html_url: str | None = None
    type: str | None = None


class GitHubLabel(BaseModel):
    """GitHub label model."""

    id: int
    name: str
    color: str | None = None
    description: str | None = None


class GitHubRepository(BaseModel):
    """GitHub repository model."""

    id: int
    name: str
    full_name: str
    owner: GitHubUser
    html_url: str
    private: bool = False
    default_branch: str = "main"


class GitHubIssue(BaseModel):
    """GitHub issue model."""

    id: int
    number: int
    title: str
    body: str | None = None
    state: str
    user: GitHubUser
    labels: list[GitHubLabel] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    html_url: str


class GitHubPullRequest(BaseModel):
    """GitHub pull request model."""

    id: int
    number: int
    title: str
    body: str | None = None
    state: str
    user: GitHubUser
    draft: bool = False
    merged: bool = False
    mergeable: bool | None = None
    labels: list[GitHubLabel] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    html_url: str
    base: dict[str, Any] | None = None
    head: dict[str, Any] | None = None


class GitHubWebhookEvent(BaseModel):
    """Base model for GitHub webhook events."""

    action: str | None = None
    sender: GitHubUser | None = None
    repository: GitHubRepository | None = None
    organization: dict[str, Any] | None = None
    installation: dict[str, Any] | None = None


class GitHubIssueEvent(GitHubWebhookEvent):
    """GitHub issues event payload."""

    issue: GitHubIssue


class GitHubPullRequestEvent(GitHubWebhookEvent):
    """GitHub pull_request event payload."""

    pull_request: GitHubPullRequest


class GitHubPushEvent(BaseModel):
    """GitHub push event payload."""

    ref: str
    before: str
    after: str
    created: bool = False
    deleted: bool = False
    forced: bool = False
    compare: str
    commits: list[dict[str, Any]] = Field(default_factory=list)
    head_commit: dict[str, Any] | None = None
    repository: GitHubRepository
    sender: GitHubUser
