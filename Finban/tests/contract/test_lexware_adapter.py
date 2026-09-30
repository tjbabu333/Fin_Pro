"""Replays recorded, sanitized Lexware Office responses — no live network calls.

Run scripts/canary_check.py separately (outside main CI) to catch real
vendor schema drift against a live sandbox account.
"""

import json
from pathlib import Path

from finban_mapper.adapters.lexware_office.normalize import normalize_quotation

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict:
    with open(FIXTURES_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def test_normalize_quotation_draft():
    fixture = load_fixture("voucherlist_quotation_page0.json")
    raw = fixture["content"][0]

    event = normalize_quotation(raw)

    assert event.system == "lexware_office"
    assert event.type == "quotation"
    assert event.external_id == "quo-0001"
    assert event.state == "draft"
    assert event.data["offer_value"] == 1000.0
    assert event.data["related_invoice_value"] == 0.0


def test_normalize_quotation_with_partial_related_invoice():
    fixture = load_fixture("voucherlist_quotation_page0.json")
    raw = fixture["content"][1]

    event = normalize_quotation(raw)

    assert event.state == "quotation"
    assert event.data["offer_value"] == 500.0
    assert event.data["related_invoice_value"] == 200.0
