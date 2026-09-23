"""Neutral shape every adapter must normalize into, and the adapter interface.

No mapping logic lives here or in any adapter — adapters only translate a
vendor's raw payload into this shape. `engine/resolver.py` is the only
consumer that knows about finban states.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ExternalEvent(BaseModel):
    system: str  # e.g. "lexware_office"
    type: str  # e.g. "quotation", "invoice", "order_confirmation"
    external_id: str
    state: str  # raw vendor state string, e.g. "open", "archived"
    updated_at: datetime
    data: dict[str, Any] = {}  # extra fields predicates may need (amounts, flags)


class BaseAdapter(ABC):
    """One subclass per external system (see adapters/lexware_office/)."""

    system_name: str

    @abstractmethod
    async def fetch_events(self, since: datetime | None = None) -> list[ExternalEvent]:
        """Return normalized events updated since the given timestamp."""
        raise NotImplementedError
