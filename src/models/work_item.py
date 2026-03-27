"""Work Item models for the orchestration queue."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class WorkItemStatus(str, Enum):
    """Status of a work item in the queue."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkItemPriority(str, Enum):
    """Priority level for a work item."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class WorkItemBase(BaseModel):
    """Base model for work items."""

    source: str = Field(..., description="Source system (e.g., 'github')")
    event_type: str = Field(..., description="Type of event (e.g., 'issues', 'pull_request')")
    payload: dict[str, Any] = Field(default_factory=dict, description="Event payload data")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class WorkItemCreate(WorkItemBase):
    """Model for creating a new work item."""

    priority: WorkItemPriority = Field(
        default=WorkItemPriority.NORMAL, description="Priority level"
    )


class WorkItemUpdate(BaseModel):
    """Model for updating a work item."""

    status: Optional[WorkItemStatus] = None
    priority: Optional[WorkItemPriority] = None
    attempts: Optional[int] = None
    error_message: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class WorkItem(WorkItemBase):
    """Full work item model with all fields."""

    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier")
    status: WorkItemStatus = Field(default=WorkItemStatus.PENDING, description="Current status")
    priority: WorkItemPriority = Field(
        default=WorkItemPriority.NORMAL, description="Priority level"
    )
    attempts: int = Field(default=0, description="Number of processing attempts")
    max_attempts: int = Field(default=3, description="Maximum retry attempts")
    error_message: Optional[str] = Field(default=None, description="Error message if failed")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )

    def mark_processing(self) -> None:
        """Mark the item as processing."""
        self.status = WorkItemStatus.PROCESSING
        self.updated_at = datetime.utcnow()

    def mark_completed(self) -> None:
        """Mark the item as completed."""
        self.status = WorkItemStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def mark_failed(self, error_message: str) -> None:
        """Mark the item as failed with an error message."""
        self.status = WorkItemStatus.FAILED
        self.error_message = error_message
        self.attempts += 1
        self.updated_at = datetime.utcnow()

    def can_retry(self) -> bool:
        """Check if the item can be retried."""
        return self.attempts < self.max_attempts

    class Config:
        """Pydantic config."""

        use_enum_values = True
