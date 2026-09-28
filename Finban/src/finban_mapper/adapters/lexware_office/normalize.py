"""Translate raw Lexware Office JSON into the neutral ExternalEvent shape.

This is the only file allowed to know the vendor's field names. Everything
downstream (engine, mapping) works only with ExternalEvent.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from finban_mapper.adapters.base import ExternalEvent

SYSTEM = "lexware_office"


def normalize_quotation(raw: dict[str, Any]) -> ExternalEvent:
    return ExternalEvent(
        system=SYSTEM,
        type="quotation",
        external_id=raw["id"],
        state=raw["voucherStatus"],
        updated_at=datetime.fromisoformat(raw["updatedDate"]),
        data={
            "offer_value": raw["totalPrice"]["totalGrossAmount"],
            "related_invoice_value": raw.get("relatedInvoiceValue", 0.0),
        },
    )


def normalize_order_confirmation(raw: dict[str, Any]) -> ExternalEvent:
    return ExternalEvent(
        system=SYSTEM,
        type="order_confirmation",
        external_id=raw["id"],
        state=raw["voucherStatus"],
        updated_at=datetime.fromisoformat(raw["updatedDate"]),
        data={
            "order_value": raw["totalPrice"]["totalGrossAmount"],
            "related_invoice_value": raw.get("relatedInvoiceValue", 0.0),
            "archived": raw.get("archived", False),
        },
    )


def normalize_invoice(raw: dict[str, Any]) -> ExternalEvent:
    return ExternalEvent(
        system=SYSTEM,
        type="invoice",
        external_id=raw["id"],
        state=raw["voucherStatus"],
        updated_at=datetime.fromisoformat(raw["updatedDate"]),
        data={
            "state": raw["voucherStatus"],
            "total_gross_amount": raw["totalPrice"]["totalGrossAmount"],
            "open_amount": raw.get("openAmount", 0.0),
        },
    )


def normalize_bank_transaction(raw: dict[str, Any]) -> ExternalEvent:
    return ExternalEvent(
        system=SYSTEM,
        type="bank_transaction",
        external_id=raw["id"],
        state=raw["status"],
        updated_at=datetime.fromisoformat(raw["updatedDate"]),
        data={},
    )
