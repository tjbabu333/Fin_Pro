"""Canonical finban state enums.

These are derived purely from finban's own vocabulary — nothing here
should ever import from `adapters/` or know that Lexware Office exists.
"""

from enum import StrEnum


class LeadState(StrEnum):
    POTENTIAL = "potential"
    WON = "won"
    LOST = "lost"
    DELETED = "deleted"
    ARCHIVED = "archived"


class OfferState(StrEnum):
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    PARTIALLY_CALCULATED = "partially_calculated"
    CALCULATED = "calculated"
    ARCHIVED = "archived"
    REJECTED = "rejected"


class OrderState(StrEnum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    PARTIALLY_CALCULATED = "partially_calculated"
    CALCULATED = "calculated"
    ARCHIVED = "archived"


class SalesInvoiceState(StrEnum):
    DRAFT = "draft"
    OPEN = "open"
    SENT = "sent"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    CANCELED = "canceled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    WRITTEN_OFF = "written_off"
    ON_HOLD = "on_hold"
    UNDEFINED = "undefined"


class CreditNoteState(StrEnum):
    OPEN = "open"
    PAID = "paid"
    PARTIALLY_PAID = "partially_paid"
    VOIDED = "voided"
    ARCHIVED = "archived"


class PurchaseInvoiceState(StrEnum):
    DRAFT_OPEN = "draft_open"
    PAID = "paid"
    CANCELED = "canceled"


class BankTransactionState(StrEnum):
    BOOKED = "booked"
    PENDING = "pending"
