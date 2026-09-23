"""Periodic live-API check for vendor schema drift.

Run on a schedule (e.g. a separate cron GitHub Action) against a Lexware
Office sandbox account — deliberately kept out of the main CI pipeline
(tests/contract uses recorded fixtures instead) so vendor flakiness never
blocks a merge.

Usage: python scripts/canary_check.py
"""

from __future__ import annotations

import asyncio
import logging
import sys

from finban_mapper.adapters.lexware_office.client import LexwareOfficeClient
from finban_mapper.adapters.lexware_office.endpoints import LexwareOfficeAdapter
from finban_mapper.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("canary_check")


async def main() -> int:
    client = LexwareOfficeClient(api_key=settings.lexware_office_api_key)
    adapter = LexwareOfficeAdapter(client)
    try:
        events = await adapter.fetch_events()
        logger.info("Fetched %d events without normalization errors.", len(events))
        return 0
    except Exception:
        logger.exception("Canary check failed — possible vendor schema drift.")
        return 1
    finally:
        await client.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
