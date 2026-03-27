"""Tests for Work Item models."""

import pytest
from datetime import datetime

from src.models import (
    WorkItem,
    WorkItemCreate,
    WorkItemPriority,
    WorkItemStatus,
)


class TestWorkItemCreate:
    """Tests for WorkItemCreate model."""

    def test_create_minimal(self) -> None:
        """Test creating a work item with minimal fields."""
        item = WorkItemCreate(
            source="github",
            event_type="issues",
        )
        assert item.source == "github"
        assert item.event_type == "issues"
        assert item.priority == WorkItemPriority.NORMAL
        assert item.payload == {}
        assert item.metadata == {}

    def test_create_with_payload(self) -> None:
        """Test creating a work item with payload."""
        item = WorkItemCreate(
            source="github",
            event_type="pull_request",
            payload={"number": 42, "action": "opened"},
            priority=WorkItemPriority.HIGH,
        )
        assert item.payload["number"] == 42
        assert item.priority == WorkItemPriority.HIGH


class TestWorkItem:
    """Tests for WorkItem model."""

    def test_create_with_defaults(self) -> None:
        """Test creating a work item with default values."""
        item = WorkItem(
            id="test-123",
            source="github",
            event_type="issues",
        )
        assert item.id == "test-123"
        assert item.status == WorkItemStatus.PENDING
        assert item.attempts == 0
        assert item.max_attempts == 3
        assert isinstance(item.created_at, datetime)
        assert isinstance(item.updated_at, datetime)

    def test_status_transitions(self) -> None:
        """Test work item status can be updated."""
        item = WorkItem(
            id="test-456",
            source="github",
            event_type="issues",
        )
        assert item.status == WorkItemStatus.PENDING

        item.status = WorkItemStatus.PROCESSING
        assert item.status == WorkItemStatus.PROCESSING

        item.status = WorkItemStatus.COMPLETED
        assert item.status == WorkItemStatus.COMPLETED
