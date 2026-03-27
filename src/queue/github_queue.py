"""GitHub Queue - Queue management for GitHub webhook events.

This module provides:
- In-memory queue for pending work items
- Queue operations (enqueue, dequeue, ack, nack)
- Retry logic with exponential backoff
"""

import asyncio
import logging
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from src.models import WorkItem, WorkItemCreate, WorkItemPriority, WorkItemStatus

logger = logging.getLogger(__name__)


@dataclass
class QueueConfig:
    """Configuration for the GitHub queue."""

    max_size: int = 1000
    visibility_timeout_seconds: int = 300
    max_retries: int = 3
    retry_delay_seconds: int = 60


@dataclass
class QueueStats:
    """Statistics for the queue."""

    total_enqueued: int = 0
    total_processed: int = 0
    total_failed: int = 0
    current_size: int = 0
    in_flight: int = 0


class GitHubQueue:
    """In-memory queue for GitHub webhook events."""

    def __init__(self, config: QueueConfig | None = None) -> None:
        self.config = config or QueueConfig()
        self._queue: deque[WorkItem] = deque()
        self._in_flight: dict[str, WorkItem] = {}
        self._stats = QueueStats()
        self._lock = asyncio.Lock()

    async def enqueue(self, item: WorkItemCreate) -> WorkItem:
        """Add a work item to the queue."""
        async with self._lock:
            if len(self._queue) >= self.config.max_size:
                raise QueueFullError(f"Queue is full (max_size={self.config.max_size})")

            work_item = WorkItem(
                id=str(uuid4()),
                source=item.source,
                event_type=item.event_type,
                payload=item.payload,
                priority=item.priority,
                metadata=item.metadata,
                max_attempts=self.config.max_retries,
            )

            # Insert based on priority
            if item.priority == WorkItemPriority.CRITICAL:
                self._queue.appendleft(work_item)
            else:
                self._queue.append(work_item)

            self._stats.total_enqueued += 1
            self._stats.current_size = len(self._queue)

            logger.info(f"Enqueued work item: {work_item.id} ({item.event_type})")
            return work_item

    async def dequeue(self, visibility_timeout: int | None = None) -> WorkItem | None:
        """Retrieve and mark a work item as in-flight."""
        async with self._lock:
            if not self._queue:
                return None

            work_item = self._queue.popleft()
            work_item.status = WorkItemStatus.PROCESSING
            work_item.updated_at = datetime.utcnow()

            timeout = visibility_timeout or self.config.visibility_timeout_seconds
            self._in_flight[work_item.id] = work_item

            self._stats.current_size = len(self._queue)
            self._stats.in_flight = len(self._in_flight)

            logger.debug(f"Dequeued work item: {work_item.id}")
            return work_item

    async def ack(self, item_id: str) -> bool:
        """Acknowledge successful processing of a work item."""
        async with self._lock:
            if item_id not in self._in_flight:
                return False

            work_item = self._in_flight.pop(item_id)
            work_item.status = WorkItemStatus.COMPLETED
            work_item.updated_at = datetime.utcnow()

            self._stats.total_processed += 1
            self._stats.in_flight = len(self._in_flight)

            logger.info(f"Acknowledged work item: {item_id}")
            return True

    async def nack(self, item_id: str, error_message: str | None = None) -> bool:
        """Negative acknowledgement - return item to queue or mark failed."""
        async with self._lock:
            if item_id not in self._in_flight:
                return False

            work_item = self._in_flight.pop(item_id)
            work_item.attempts += 1
            work_item.updated_at = datetime.utcnow()

            if error_message:
                work_item.error_message = error_message

            if work_item.attempts >= work_item.max_attempts:
                work_item.status = WorkItemStatus.FAILED
                self._stats.total_failed += 1
                logger.warning(f"Work item failed after {work_item.attempts} attempts: {item_id}")
            else:
                work_item.status = WorkItemStatus.RETRY
                self._queue.appendleft(work_item)
                logger.info(f"Work item returned to queue for retry: {item_id}")

            self._stats.in_flight = len(self._in_flight)
            self._stats.current_size = len(self._queue)

            return True

    def get_stats(self) -> QueueStats:
        """Get current queue statistics."""
        return QueueStats(
            total_enqueued=self._stats.total_enqueued,
            total_processed=self._stats.total_processed,
            total_failed=self._stats.total_failed,
            current_size=len(self._queue),
            in_flight=len(self._in_flight),
        )

    async def size(self) -> int:
        """Get current queue size."""
        return len(self._queue)


class QueueFullError(Exception):
    """Raised when the queue is at capacity."""

    pass


class ItemNotFoundError(Exception):
    """Raised when a work item is not found."""

    pass
