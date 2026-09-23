"""Idempotent writes + provenance recording.

apply_state_change() is the single write path the engine calls after
resolving a state. It is the enforcement point for:
  - idempotency (duplicate events are a no-op, via ProcessedEvent's
    unique constraint)
  - the audit trail (every change recorded in StateChange)
  - backward-transition guardrails (domain/transitions.py)
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from finban_mapper.adapters.base import ExternalEvent
from finban_mapper.domain.transitions import is_transition_allowed
from finban_mapper.persistence.models import EntityState, ProcessedEvent
from finban_mapper.persistence.models import StateChange as StateChangeORM


class TransitionRejected(Exception):
    """Raised when a proposed state change is not an allowed transition."""


def apply_state_change(
    session: Session,
    event: ExternalEvent,
    entity_type: str,
    new_state: str,
    rule_id: str,
) -> bool:
    """Apply a resolved state change atomically. Returns False if it was a
    duplicate (already processed) and True if it was newly applied.
    """
    # 1. Idempotency check — same event redelivered is a no-op.
    processed = ProcessedEvent(
        system=event.system,
        external_id=event.external_id,
        updated_at=event.updated_at,
        processed_at=datetime.utcnow(),
    )
    session.add(processed)
    try:
        session.flush()  # triggers the unique constraint if this is a dup
    except IntegrityError:
        session.rollback()
        return False

    # 2. Look up current state, enforce transition guardrails.
    current = session.get(EntityState, (entity_type, event.external_id))
    old_state = current.current_state if current else None

    if not is_transition_allowed(entity_type, old_state, new_state):
        session.rollback()
        raise TransitionRejected(
            f"{entity_type}/{event.external_id}: {old_state} -> {new_state} not allowed"
        )

    # 3. Upsert current state.
    if current:
        current.current_state = new_state
        current.updated_at = event.updated_at
    else:
        session.add(
            EntityState(
                entity_type=entity_type,
                entity_id=event.external_id,
                current_state=new_state,
                updated_at=event.updated_at,
            )
        )

    # 4. Record the audit trail entry.
    session.add(
        StateChangeORM(
            entity_type=entity_type,
            entity_id=event.external_id,
            old_state=old_state,
            new_state=new_state,
            source_system=event.system,
            source_event_id=event.external_id,
            rule_id=rule_id,
            occurred_at=datetime.utcnow(),
        )
    )
    session.commit()
    return True
