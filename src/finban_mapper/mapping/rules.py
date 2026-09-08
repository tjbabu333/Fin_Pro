"""The mapping table, represented as data.

Each row says: for this external system + type + raw state, produce this
finban state — optionally gated by a named predicate. Adding a new vendor
means inserting rows here, not writing new code paths in the engine.
"""

from __future__ import annotations

from typing import Optional

import yaml
from pydantic import BaseModel


class MappingRule(BaseModel):
    id: str
    external_system: str
    external_type: str
    external_state: str
    predicate: Optional[str] = None
    finban_entity_type: str
    finban_state: str
    is_fallback: bool = False


def load_rules(path: str) -> list[MappingRule]:
    """Load mapping rules from a YAML file (see seed_rules.yaml)."""
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return [MappingRule(**row) for row in raw["rules"]]
