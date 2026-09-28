"""Query API: current state + full provenance trail per entity."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from finban_mapper.persistence.db import get_session
from finban_mapper.persistence.models import EntityState
from finban_mapper.persistence.models import StateChange as StateChangeORM

router = APIRouter(prefix="/entities", tags=["entities"])


@router.get("/{entity_type}/{entity_id}/state")
def get_current_state(
    entity_type: str, entity_id: str, session: Session = Depends(get_session)
):
    row = session.get(EntityState, (entity_type, entity_id))
    if row is None:
        raise HTTPException(status_code=404, detail="entity not found")
    return {
        "entity_type": row.entity_type,
        "entity_id": row.entity_id,
        "current_state": row.current_state,
        "updated_at": row.updated_at,
    }


@router.get("/{entity_type}/{entity_id}/history")
def get_state_history(
    entity_type: str, entity_id: str, session: Session = Depends(get_session)
):
    stmt = (
        select(StateChangeORM)
        .where(
            StateChangeORM.entity_type == entity_type,
            StateChangeORM.entity_id == entity_id,
        )
        .order_by(StateChangeORM.occurred_at.asc())
    )
    rows = session.execute(stmt).scalars().all()
    return [
        {
            "old_state": r.old_state,
            "new_state": r.new_state,
            "source_system": r.source_system,
            "source_event_id": r.source_event_id,
            "rule_id": r.rule_id,
            "occurred_at": r.occurred_at,
        }
        for r in rows
    ]
