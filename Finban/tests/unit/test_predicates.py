from finban_mapper.mapping import predicates


def test_offer_related_invoice_below_value_true():
    data = {"related_invoice_value": 50.0, "offer_value": 100.0}
    assert predicates.offer_related_invoice_below_value(data) is True
    assert predicates.offer_related_invoice_at_or_above_value(data) is False


def test_offer_related_invoice_at_value_counts_as_at_or_above():
    data = {"related_invoice_value": 100.0, "offer_value": 100.0}
    assert predicates.offer_related_invoice_at_or_above_value(data) is True
    assert predicates.offer_related_invoice_below_value(data) is False


def test_offer_related_invoice_above_value():
    data = {"related_invoice_value": 150.0, "offer_value": 100.0}
    assert predicates.offer_related_invoice_at_or_above_value(data) is True


def test_order_archived_no_related_invoice():
    data = {"archived": True, "related_invoice_value": 0, "order_value": 500.0}
    assert predicates.order_archived_no_related_invoice(data) is True
    assert predicates.order_archived_partially_invoiced(data) is False
    assert predicates.order_archived_fully_invoiced(data) is False


def test_order_archived_partially_invoiced():
    data = {"archived": True, "related_invoice_value": 200.0, "order_value": 500.0}
    assert predicates.order_archived_partially_invoiced(data) is True
    assert predicates.order_archived_no_related_invoice(data) is False
    assert predicates.order_archived_fully_invoiced(data) is False


def test_order_archived_fully_invoiced():
    data = {"archived": True, "related_invoice_value": 500.0, "order_value": 500.0}
    assert predicates.order_archived_fully_invoiced(data) is True
    assert predicates.order_archived_partially_invoiced(data) is False


def test_order_not_archived_never_matches():
    data = {"archived": False, "related_invoice_value": 0, "order_value": 500.0}
    assert predicates.order_archived_no_related_invoice(data) is False
    assert predicates.order_archived_partially_invoiced(data) is False
    assert predicates.order_archived_fully_invoiced(data) is False


def test_invoice_open_and_partially_paid_true():
    data = {"state": "open", "open_amount": 40.0, "total_gross_amount": 100.0}
    assert predicates.invoice_open_and_partially_paid(data) is True


def test_invoice_open_and_fully_open_is_not_partially_paid():
    data = {"state": "open", "open_amount": 100.0, "total_gross_amount": 100.0}
    assert predicates.invoice_open_and_partially_paid(data) is False
