from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base
from src.database.models.enums import OutboxStatus


class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    __table_args__ = (
        CheckConstraint(
            "attempts >= 0",
            name="ck_outbox_events_attempts_non_negative",
        ),
        UniqueConstraint(
            "aggregate_type",
            "aggregate_id",
            "event_type",
            name="uq_outbox_events_aggregate_event",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    aggregate_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    aggregate_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    payload: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    status: Mapped[OutboxStatus] = mapped_column(
        Enum(
            OutboxStatus,
            name="outbox_status",
            native_enum=False,
            create_constraint=True,
        ),
        nullable=False,
        default=OutboxStatus.PENDING,
    )

    attempts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    available_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
