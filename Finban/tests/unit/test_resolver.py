import pytest

from finban_mapper.engine.errors import UnmappedStateError
from finban_mapper.engine.resolver import resolve_state
from tests.conftest import make_event


def test_offer_partially_calculated_when_invoice_below_value(rules):
    event = make_event(
        type="quotation",
        state="quotation",
        data={"related_invoice_value": 50.0, "offer_value": 100.0},
    )
    state, rule_id = resolve_state(event, rules)
    assert state == "partially_calculated"
    assert rule_id == "r-offer-004"


def test_offer_calculated_when_invoice_at_or_above_value(rules):
    event = make_event(
        type="quotation",
        state="quotation",
        data={"related_invoice_value": 100.0, "offer_value": 100.0},
    )
    state, rule_id = resolve_state(event, rules)
    assert state == "calculated"
    assert rule_id == "r-offer-005"


def test_offer_direct_lookup_no_predicate(rules):
    event = make_event(type="quotation", state="draft")
    state, rule_id = resolve_state(event, rules)
    assert state == "draft"
    assert rule_id == "r-offer-001"


def test_order_archived_fully_invoiced(rules):
    event = make_event(
        type="order_confirmation",
        state="archived",
        data={"archived": True, "related_invoice_value": 500.0, "order_value": 500.0},
    )
    state, rule_id = resolve_state(event, rules)
    assert state == "calculated"
    assert rule_id == "r-order-005"


def test_invoice_open_partially_paid_takes_priority_over_plain_open(rules):
    event = make_event(
        type="invoice",
        state="open",
        data={"state": "open", "open_amount": 40.0, "total_gross_amount": 100.0},
    )
    state, rule_id = resolve_state(event, rules)
    assert state == "partially_paid"
    assert rule_id == "r-inv-002"


def test_invoice_fully_open_uses_plain_open_rule(rules):
    event = make_event(
        type="invoice",
        state="open",
        data={"state": "open", "open_amount": 100.0, "total_gross_amount": 100.0},
    )
    state, rule_id = resolve_state(event, rules)
    assert state == "open"
    assert rule_id == "r-inv-003"


def test_unknown_state_falls_back_instead_of_raising(rules):
    event = make_event(type="quotation", state="totally-unknown-vendor-state")
    state, rule_id = resolve_state(event, rules)
    assert state == "undefined"
    assert rule_id == "r-offer-fallback"


def test_unmapped_type_raises(rules):
    event = make_event(type="not_a_real_type", state="whatever")
    with pytest.raises(UnmappedStateError):
        resolve_state(event, rules)


def test_bank_transaction_flat_mapping(rules):
    event = make_event(type="bank_transaction", state="booked")
    state, rule_id = resolve_state(event, rules)
    assert state == "booked"
    assert rule_id == "r-bank-001"
