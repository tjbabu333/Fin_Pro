"""Regression safety net: every direct-lookup rule in seed_rules.yaml must
still resolve to the finban_state recorded in expected_results.json.

Rules that require a predicate (conditional rows) are exercised by
tests/unit/test_resolver.py instead, since they need synthetic `data`
payloads rather than a bare state match. If this test starts failing
after an edit to seed_rules.yaml, it means a direct mapping changed —
confirm that's intentional before updating expected_results.json.
"""

import json
from pathlib import Path

from finban_mapper.engine.resolver import resolve_state
from tests.conftest import make_event

EXPECTED_PATH = Path(__file__).parent / "expected_results.json"


def test_direct_lookup_rules_match_snapshot(rules):
    with open(EXPECTED_PATH, encoding="utf-8") as f:
        expected = json.load(f)

    direct_rules = [r for r in rules if r.predicate is None and not r.is_fallback]

    # Every direct rule we snapshot should still be present in seed_rules.yaml.
    checked = set()
    for rule in direct_rules:
        if rule.id not in expected:
            continue  # not every direct rule needs a snapshot entry
        event = make_event(type=rule.external_type, state=rule.external_state)
        state, matched_rule_id = resolve_state(event, rules)
        assert state == expected[rule.id]["finban_state"], (
            f"{rule.id} regressed: expected {expected[rule.id]['finban_state']}, "
            f"got {state}"
        )
        assert matched_rule_id == rule.id
        checked.add(rule.id)

    missing = set(expected.keys()) - checked
    assert not missing, f"expected_results.json references rules no longer in seed_rules.yaml: {missing}"
