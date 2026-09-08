"""Lookup from predicate name (as referenced in seed_rules.yaml) to function."""

from finban_mapper.mapping import predicates

PREDICATES = {
    "offer_related_invoice_below_value": predicates.offer_related_invoice_below_value,
    "offer_related_invoice_at_or_above_value": predicates.offer_related_invoice_at_or_above_value,
    "order_archived_no_related_invoice": predicates.order_archived_no_related_invoice,
    "order_archived_partially_invoiced": predicates.order_archived_partially_invoiced,
    "order_archived_fully_invoiced": predicates.order_archived_fully_invoiced,
    "invoice_open_and_partially_paid": predicates.invoice_open_and_partially_paid,
}
