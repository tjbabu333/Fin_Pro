"""The normalization engine: ExternalEvent -> (finban_state, rule_id).

This is the single seam that knows both "the mapping table" and
"what a predicate needs to see" — keep it small and exhaustively
unit tested (see tests/unit/test_resolver.py).
"""

from __future__ import annotations

from finban_mapper.adapters.base import ExternalEvent
from finban_mapper.engine.errors import AmbiguousRuleError, UnmappedStateError
from finban_mapper.mapping.registry import PREDICATES
from finban_mapper.mapping.rules import MappingRule


def resolve_state(event: ExternalEvent, rules: list[MappingRule]) -> tuple[str, str]:
    """Return (finban_state, rule_id) for the given event.

    Matching order:
      1. Exact (system, type, state) rules with a predicate — first
         predicate that returns True wins.
      2. Exact (system, type, state) rule with no predicate (direct lookup).
      3. The (system, type) fallback row (external_state == "*",
         is_fallback == True).
    Raises UnmappedStateError if none of the above match.
    """
    candidates = [
        r
        for r in rules
        if r.external_system == event.system
        and r.external_type == event.type
        and r.external_state == event.state
        and not r.is_fallback
    ]

    predicate_matches = []
    direct_matches = []
    for rule in candidates:
        if rule.predicate is None:
            direct_matches.append(rule)
        elif PREDICATES[rule.predicate](event.data):
            predicate_matches.append(rule)

    if len(predicate_matches) > 1:
        raise AmbiguousRuleError(
            f"Multiple predicates matched for {event.system}/{event.type}/{event.state}: "
            f"{[r.id for r in predicate_matches]}"
        )
    if predicate_matches:
        rule = predicate_matches[0]
        return rule.finban_state, rule.id

    if direct_matches:
        rule = direct_matches[0]
        return rule.finban_state, rule.id

    fallback = next(
        (
            r
            for r in rules
            if r.external_system == event.system
            and r.external_type == event.type
            and r.is_fallback
        ),
        None,
    )
    if fallback:
        return fallback.finban_state, fallback.id

    raise UnmappedStateError(
        f"No mapping rule (including fallback) for "
        f"{event.system}/{event.type}/{event.state}"
    )
