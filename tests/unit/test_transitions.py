from finban_mapper.domain.transitions import is_transition_allowed


def test_first_write_always_allowed():
    assert is_transition_allowed("sales_invoice", None, "open") is True


def test_same_state_is_allowed_noop():
    assert is_transition_allowed("sales_invoice", "open", "open") is True


def test_paid_to_canceled_is_allowed_backward_transition():
    assert is_transition_allowed("sales_invoice", "paid", "canceled") is True


def test_paid_to_refunded_is_allowed_backward_transition():
    assert is_transition_allowed("sales_invoice", "paid", "refunded") is True


def test_forward_transition_always_allowed():
    assert is_transition_allowed("sales_invoice", "draft", "open") is True
