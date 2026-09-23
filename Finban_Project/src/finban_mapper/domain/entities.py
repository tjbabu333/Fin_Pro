"""Canonical finban entities.

Pydantic models representing the vendor-agnostic domain. Adapters translate
vendor payloads into ExternalEvent (see adapters/base.py); the engine turns
an ExternalEvent into a state on one of these entities.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from finban_mapper.domain.states import (
    BankTransactionState,
    CreditNoteState,
    LeadState,
    OfferState,
    OrderState,
    PurchaseInvoiceState,
    SalesInvoiceState,
)


class Lead(BaseModel):
    id: str
    state: LeadState
    updated_at: datetime


class Offer(BaseModel):
    id: str
    state: OfferState
    value: float
    related_invoice_value: float = 0.0
    updated_at: datetime


class Order(BaseModel):
    id: str
    state: OrderState
    value: float
    related_invoice_value: float = 0.0
    archived: bool = False
    updated_at: datetime


class SalesInvoice(BaseModel):
    id: str
    state: SalesInvoiceState
    total_gross_amount: float
    open_amount: float
    updated_at: datetime


class CreditNote(BaseModel):
    id: str
    state: CreditNoteState
    updated_at: datetime


class PurchaseInvoice(BaseModel):
    id: str
    state: PurchaseInvoiceState
    updated_at: datetime


class BankTransaction(BaseModel):
    id: str
    state: BankTransactionState
    updated_at: datetime


class StateChange(BaseModel):
    """A single, auditable state transition — the provenance record.

    This is what makes "why does finban say this is calculated" a lookup
    instead of an investigation (see design doc §3.5).
    """

    entity_type: str
    entity_id: str
    old_state: Optional[str] = None
    new_state: str
    source_system: str
    source_event_id: str
    rule_id: str
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
