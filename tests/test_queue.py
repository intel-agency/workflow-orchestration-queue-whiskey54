"""Tests for GitHub Queue."""

import pytest

from src.queue import GitHubQueue, QueueConfig, QueueFullError
from src.models import WorkItemCreate, WorkItemPriority, WorkItemStatus


class TestGitHubQueue:
    """Tests for GitHubQueue."""

    @pytest.fixture
    def queue(self) -> GitHubQueue:
        """Create a fresh queue for each test."""
        config = QueueConfig(max_size=10)
        return GitHubQueue(config)

    @pytest.fixture
    def sample_item(self) -> WorkItemCreate:
        """Create a sample work item for testing."""
        return WorkItemCreate(
            source="github",
            event_type="issues",
            payload={"number": 1},
        )

    @pytest.mark.asyncio
    async def test_enqueue(self, queue: GitHubQueue, sample_item: WorkItemCreate) -> None:
        """Test enqueuing a work item."""
        result = await queue.enqueue(sample_item)

        assert result.id is not None
        assert result.source == "github"
        assert result.event_type == "issues"
        assert result.status == WorkItemStatus.PENDING

    @pytest.mark.asyncio
    async def test_dequeue(self, queue: GitHubQueue, sample_item: WorkItemCreate) -> None:
        """Test dequeuing a work item."""
        await queue.enqueue(sample_item)
        result = await queue.dequeue()

        assert result is not None
        assert result.status == WorkItemStatus.PROCESSING

    @pytest.mark.asyncio
    async def test_dequeue_empty(self, queue: GitHubQueue) -> None:
        """Test dequeuing from empty queue returns None."""
        result = await queue.dequeue()
        assert result is None

    @pytest.mark.asyncio
    async def test_ack(self, queue: GitHubQueue, sample_item: WorkItemCreate) -> None:
        """Test acknowledging a work item."""
        item = await queue.enqueue(sample_item)
        await queue.dequeue()
        result = await queue.ack(item.id)

        assert result is True
        stats = queue.get_stats()
        assert stats.total_processed == 1

    @pytest.mark.asyncio
    async def test_nack_retry(self, queue: GitHubQueue, sample_item: WorkItemCreate) -> None:
        """Test nack returns item to queue for retry."""
        item = await queue.enqueue(sample_item)
        await queue.dequeue()
        result = await queue.nack(item.id, "Test error")

        assert result is True
        stats = queue.get_stats()
        assert stats.current_size == 1

    @pytest.mark.asyncio
    async def test_queue_full(self, queue: GitHubQueue, sample_item: WorkItemCreate) -> None:
        """Test queue raises error when full."""
        for i in range(10):
            await queue.enqueue(WorkItemCreate(source="test", event_type=f"event-{i}"))

        with pytest.raises(QueueFullError):
            await queue.enqueue(sample_item)

    @pytest.mark.asyncio
    async def test_priority_enqueue(self, queue: GitHubQueue) -> None:
        """Test critical priority items are dequeued first."""
        await queue.enqueue(WorkItemCreate(source="test", event_type="normal"))
        await queue.enqueue(
            WorkItemCreate(
                source="test",
                event_type="critical",
                priority=WorkItemPriority.CRITICAL,
            )
        )

        result = await queue.dequeue()
        assert result is not None
        assert result.event_type == "critical"
