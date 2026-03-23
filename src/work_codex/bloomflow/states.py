"""BloomFlow v2 state machine.

Defines valid statuses and allowed transitions for briefs and queue items.
"""

from __future__ import annotations

from enum import Enum


class InvalidTransition(Exception):
    """Raised when a status transition is not allowed."""


class BriefStatus(str, Enum):
    DRAFTING_READY = "drafting_ready"
    APPROVED_FOR_DRAFTING = "approved_for_drafting"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    PAUSED = "paused"


class QueueStatus(str, Enum):
    BACKLOG = "backlog"
    PLANNED = "planned"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    PAUSED = "paused"


_BRIEF_TRANSITIONS: dict[BriefStatus, frozenset[BriefStatus]] = {
    BriefStatus.DRAFTING_READY: frozenset({
        BriefStatus.APPROVED_FOR_DRAFTING,
        BriefStatus.PAUSED,
    }),
    BriefStatus.APPROVED_FOR_DRAFTING: frozenset({
        BriefStatus.IN_REVIEW,
        BriefStatus.PAUSED,
    }),
    BriefStatus.IN_REVIEW: frozenset({
        BriefStatus.APPROVED,
        BriefStatus.DRAFTING_READY,
        BriefStatus.PAUSED,
    }),
    BriefStatus.APPROVED: frozenset({
        BriefStatus.SCHEDULED,
        BriefStatus.IN_REVIEW,
        BriefStatus.PAUSED,
    }),
    BriefStatus.SCHEDULED: frozenset({
        BriefStatus.PUBLISHED,
        BriefStatus.APPROVED,
        BriefStatus.PAUSED,
    }),
    BriefStatus.PUBLISHED: frozenset(),
    BriefStatus.PAUSED: frozenset({
        BriefStatus.DRAFTING_READY,
        BriefStatus.IN_REVIEW,
        BriefStatus.APPROVED,
    }),
}

_QUEUE_TRANSITIONS: dict[QueueStatus, frozenset[QueueStatus]] = {
    QueueStatus.BACKLOG: frozenset({
        QueueStatus.PLANNED,
        QueueStatus.IN_REVIEW,
        QueueStatus.PAUSED,
    }),
    QueueStatus.PLANNED: frozenset({
        QueueStatus.IN_REVIEW,
        QueueStatus.SCHEDULED,
        QueueStatus.PAUSED,
    }),
    QueueStatus.IN_REVIEW: frozenset({
        QueueStatus.APPROVED,
        QueueStatus.BACKLOG,
        QueueStatus.PAUSED,
    }),
    QueueStatus.APPROVED: frozenset({
        QueueStatus.SCHEDULED,
        QueueStatus.IN_REVIEW,
        QueueStatus.PAUSED,
    }),
    QueueStatus.SCHEDULED: frozenset({
        QueueStatus.PUBLISHED,
        QueueStatus.APPROVED,
        QueueStatus.PAUSED,
    }),
    QueueStatus.PUBLISHED: frozenset(),
    QueueStatus.PAUSED: frozenset({
        QueueStatus.BACKLOG,
        QueueStatus.PLANNED,
    }),
}

# Map brief status -> queue status for sync
_BRIEF_TO_QUEUE: dict[BriefStatus, QueueStatus] = {
    BriefStatus.DRAFTING_READY: QueueStatus.BACKLOG,
    BriefStatus.APPROVED_FOR_DRAFTING: QueueStatus.BACKLOG,
    BriefStatus.IN_REVIEW: QueueStatus.IN_REVIEW,
    BriefStatus.APPROVED: QueueStatus.APPROVED,
    BriefStatus.SCHEDULED: QueueStatus.SCHEDULED,
    BriefStatus.PUBLISHED: QueueStatus.PUBLISHED,
    BriefStatus.PAUSED: QueueStatus.PAUSED,
}


def validate_brief_transition(current: BriefStatus, target: BriefStatus) -> None:
    """Raise InvalidTransition if moving from current to target is not allowed."""
    allowed = _BRIEF_TRANSITIONS.get(current, frozenset())
    if target not in allowed:
        raise InvalidTransition(
            f"cannot move brief from {current.value!r} to {target.value!r}; "
            f"allowed: {sorted(s.value for s in allowed)}"
        )


def validate_queue_transition(current: QueueStatus, target: QueueStatus) -> None:
    """Raise InvalidTransition if moving from current to target is not allowed."""
    allowed = _QUEUE_TRANSITIONS.get(current, frozenset())
    if target not in allowed:
        raise InvalidTransition(
            f"cannot move queue item from {current.value!r} to {target.value!r}; "
            f"allowed: {sorted(s.value for s in allowed)}"
        )


def queue_status_for_brief(brief_status: BriefStatus) -> QueueStatus:
    """Return the corresponding queue status for a brief status."""
    return _BRIEF_TO_QUEUE[brief_status]
