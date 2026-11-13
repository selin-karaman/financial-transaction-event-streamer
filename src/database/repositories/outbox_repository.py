from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.database.models.enums import OutboxStatus
from src.database.models.outbox_event import OutboxEvent


def get_by_id(db: Session, event_id: UUID) -> OutboxEvent | None:
    statement = select(OutboxEvent).where(
        OutboxEvent.id == event_id
    )
    return db.scalar(statement)


def get_pending(
    db: Session,
    limit: int = 100,
) -> list[OutboxEvent]:
    statement = (
        select(OutboxEvent)
        .where(
            OutboxEvent.status == OutboxStatus.PENDING,
            OutboxEvent.available_at <= func.now(),
        )
        .order_by(
            OutboxEvent.available_at,
            OutboxEvent.created_at,
        )
        .limit(limit)
        .with_for_update(skip_locked=True)
    )
    return list(db.scalars(statement).all())


def create(db: Session, event: OutboxEvent) -> OutboxEvent:
    db.add(event)
    db.flush()
    return event


def mark_published(
    db: Session,
    event: OutboxEvent,
) -> OutboxEvent:
    event.status = OutboxStatus.PUBLISHED
    event.published_at = datetime.now(timezone.utc)
    event.last_error = None

    db.flush()
    return event


def mark_failed(
    db: Session,
    event: OutboxEvent,
    error: str,
    retry_delay: timedelta = timedelta(seconds=30),
) -> OutboxEvent:
    event.attempts += 1
    event.last_error = error
    event.available_at = datetime.now(timezone.utc) + retry_delay

    db.flush()
    return event
