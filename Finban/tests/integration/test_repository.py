from finban_mapper.persistence.models import EntityState, StateChange
from finban_mapper.persistence.repository import apply_state_change
from tests.conftest import make_event


def test_first_write_creates_entity_and_history(db_session):
    event = make_event(external_id="offer-1", state="draft")
    applied = apply_state_change(db_session, event, "offer", "draft", "r-offer-001")

    assert applied is True
    row = db_session.get(EntityState, ("offer", "offer-1"))
    assert row.current_state == "draft"

    history = db_session.query(StateChange).filter_by(entity_id="offer-1").all()
    assert len(history) == 1
    assert history[0].rule_id == "r-offer-001"
    assert history[0].old_state is None


def test_duplicate_event_is_a_noop(db_session):
    event = make_event(external_id="offer-2", state="draft")

    first = apply_state_change(db_session, event, "offer", "draft", "r-offer-001")
    second = apply_state_change(db_session, event, "offer", "draft", "r-offer-001")

    assert first is True
    assert second is False  # same (system, external_id, updated_at) -> no-op

    history = db_session.query(StateChange).filter_by(entity_id="offer-2").all()
    assert len(history) == 1  # not duplicated


def test_state_transition_updates_current_state_and_appends_history(db_session):
    first_event = make_event(external_id="offer-3", state="draft")
    apply_state_change(db_session, first_event, "offer", "draft", "r-offer-001")

    second_event = make_event(external_id="offer-3", state="open")
    second_event = second_event.model_copy(
        update={"updated_at": first_event.updated_at.replace(day=2)}
    )
    apply_state_change(db_session, second_event, "offer", "sent", "r-offer-002")

    row = db_session.get(EntityState, ("offer", "offer-3"))
    assert row.current_state == "sent"

    history = (
        db_session.query(StateChange)
        .filter_by(entity_id="offer-3")
        .order_by(StateChange.id)
        .all()
    )
    assert [h.new_state for h in history] == ["draft", "sent"]
    assert history[1].old_state == "draft"
