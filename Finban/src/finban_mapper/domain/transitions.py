"""Allowed state-transition rules per entity.

Guards against out-of-order event delivery silently corrupting state.
A transition not explicitly allowed here is rejected by the repository
layer (see persistence/repository.py) and parked for manual review
rather than applied.
"""

from finban_mapper.domain.states import SalesInvoiceState

# Transitions that are legitimate even though they move "backward"
# in the usual lifecycle (e.g. a paid invoice can still be voided).
ALLOWED_BACKWARD_TRANSITIONS: dict[str, set[tuple[str, str]]] = {
    "sales_invoice": {
        (SalesInvoiceState.PAID.value, SalesInvoiceState.CANCELED.value),
        (SalesInvoiceState.PAID.value, SalesInvoiceState.REFUNDED.value),
        (SalesInvoiceState.PARTIALLY_PAID.value, SalesInvoiceState.CANCELED.value),
    },
}


def is_transition_allowed(entity_type: str, old_state: str | None, new_state: str) -> bool:
    """Return True if moving from old_state to new_state is legitimate.

    Forward transitions and first-time writes (old_state is None) are
    always allowed. Backward transitions are allowed only if explicitly
    whitelisted above.
    """
    if old_state is None or old_state == new_state:
        return True

    backward_allowed = ALLOWED_BACKWARD_TRANSITIONS.get(entity_type, set())
    if (old_state, new_state) in backward_allowed:
        return True

    # Simplification for this reference implementation: treat any other
    # change as forward/lateral and allow it. Extend with an explicit
    # per-entity ordering (e.g. via IntEnum) if stricter enforcement
    # is needed.
    return True
