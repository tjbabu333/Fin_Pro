"""LexwareOfficeAdapter — the concrete BaseAdapter for this vendor.

Fetches vouchers of each type and normalizes them. Add a new voucher type
by adding one branch here plus one `normalize_*` function; no changes
needed in engine/ or mapping/.
"""

from __future__ import annotations

from datetime import datetime

from finban_mapper.adapters.base import BaseAdapter, ExternalEvent
from finban_mapper.adapters.lexware_office import normalize
from finban_mapper.adapters.lexware_office.client import LexwareOfficeClient

VOUCHER_TYPE_NORMALIZERS = {
    "quotation": normalize.normalize_quotation,
    "orderconfirmation": normalize.normalize_order_confirmation,
    "invoice": normalize.normalize_invoice,
}


class LexwareOfficeAdapter(BaseAdapter):
    system_name = "lexware_office"

    def __init__(self, client: LexwareOfficeClient):
        self._client = client

    async def fetch_events(self, since: datetime | None = None) -> list[ExternalEvent]:
        events: list[ExternalEvent] = []
        for voucher_type, normalizer in VOUCHER_TYPE_NORMALIZERS.items():
            raw_vouchers = await self._client.list_all_pages(voucher_type)
            for raw in raw_vouchers:
                event = normalizer(raw)
                if since is None or event.updated_at >= since:
                    events.append(event)
        return events
