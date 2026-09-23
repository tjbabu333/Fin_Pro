"""SQLAlchemy ORM models.

Two tables matter most:
  - entity_state: current state per finban entity (fast reads)
  - state_change: full audit trail (source event + rule id) per transition,
    used for the /history endpoint and for debugging mapping decisions.

The unique constraint on processed_event drives idempotency (§8 build
plan step 5 / design doc §6.3): the same external event redelivered is a
no-op.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class EntityState(Base):
    __tablename__ = "entity_state"

    entity_type: Mapped[str] = mapped_column(String(64), primary_key=True)
    entity_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    current_state: Mapped[str] = mapped_column(String(64), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class StateChange(Base):
    __tablename__ = "state_change"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(128), nullable=False)
    old_state: Mapped[str | None] = mapped_column(String(64), nullable=True)
    new_state: Mapped[str] = mapped_column(String(64), nullable=False)
    source_system: Mapped[str] = mapped_column(String(64), nullable=False)
    source_event_id: Mapped[str] = mapped_column(String(128), nullable=False)
    rule_id: Mapped[str] = mapped_column(String(64), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class ProcessedEvent(Base):
    """Idempotency ledger — one row per (system, external_id, updated_at)."""

    __tablename__ = "processed_event"
    __table_args__ = (
        UniqueConstraint("system", "external_id", "updated_at", name="uq_processed_event"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    system: Mapped[str] = mapped_column(String(64), nullable=False)
    external_id: Mapped[str] = mapped_column(String(128), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    processed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
