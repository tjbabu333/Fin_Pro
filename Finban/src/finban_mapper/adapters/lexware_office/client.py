"""Thin HTTP client for the Lexware Office API.

Handles auth, pagination, and rate-limit backoff only. No mapping logic —
see normalize.py for turning raw responses into ExternalEvent.
"""

from __future__ import annotations

import asyncio
from typing import Any

import httpx

BASE_URL = "https://api.lexoffice.io"
MAX_RETRIES = 5


class LexwareOfficeClient:
    def __init__(self, api_key: str, base_url: str = BASE_URL, timeout: float = 10.0):
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
            timeout=timeout,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        for attempt in range(MAX_RETRIES):
            resp = await self._client.get(path, params=params)
            if resp.status_code == 429:
                retry_after = float(resp.headers.get("Retry-After", 2**attempt))
                await asyncio.sleep(retry_after)
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError(f"Exceeded retries fetching {path}")

    async def list_vouchers(self, voucher_type: str, page: int = 0) -> dict[str, Any]:
        return await self._get(
            "/v1/voucherlist", params={"voucherType": voucher_type, "page": page}
        )

    async def get_quotation(self, quotation_id: str) -> dict[str, Any]:
        return await self._get(f"/v1/quotations/{quotation_id}")

    async def get_invoice(self, invoice_id: str) -> dict[str, Any]:
        return await self._get(f"/v1/invoices/{invoice_id}")

    async def get_order_confirmation(self, order_id: str) -> dict[str, Any]:
        return await self._get(f"/v1/order-confirmations/{order_id}")

    async def list_all_pages(self, voucher_type: str) -> list[dict[str, Any]]:
        """Follow pagination until the last page, returning all voucher entries."""
        page = 0
        results: list[dict[str, Any]] = []
        while True:
            body = await self.list_vouchers(voucher_type, page=page)
            content = body.get("content", [])
            results.extend(content)
            if body.get("last", True):
                break
            page += 1
        return results
