"""Pure, unit-testable predicates for the conditional mapping rows.

Every function here takes only the fields it needs from an ExternalEvent's
`data` payload and returns True/False. No I/O, no side effects — this is
what makes §6.1 of the design doc ("both branches of every conditional
row") cheap to test exhaustively.
"""

from __future__ import annotations

from typing import Any


def offer_related_invoice_below_value(data: dict[str, Any]) -> bool:
    """True when the related invoice value is strictly below the offer value.

    Maps to finban's `offer.partially_calculated`.
    """
    return data["related_invoice_value"] < data["offer_value"]


def offer_related_invoice_at_or_above_value(data: dict[str, Any]) -> bool:
    """True when the related invoice value meets or exceeds the offer value.

    Maps to finban's `offer.calculated`.
    """
    return data["related_invoice_value"] >= data["offer_value"]


def order_archived_no_related_invoice(data: dict[str, Any]) -> bool:
    """Archived order with no related invoice at all."""
    return data.get("archived", False) and data.get("related_invoice_value", 0) == 0


def order_archived_partially_invoiced(data: dict[str, Any]) -> bool:
    """Archived order, partially invoiced (0 < related invoice < order value)."""
    return (
        data.get("archived", False)
        and 0 < data.get("related_invoice_value", 0) < data["order_value"]
    )


def order_archived_fully_invoiced(data: dict[str, Any]) -> bool:
    """Archived order, related invoice value meets or exceeds order value."""
    return (
        data.get("archived", False)
        and data.get("related_invoice_value", 0) >= data["order_value"]
    )


def invoice_open_and_partially_paid(data: dict[str, Any]) -> bool:
    """Open invoice where the open amount is less than the total gross amount."""
    return data["state"] == "open" and data["open_amount"] < data["total_gross_amount"]
