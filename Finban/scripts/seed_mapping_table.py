"""Load seed_rules.yaml into a `mapping_rule` table in Postgres.

Run after migrations: `python scripts/seed_mapping_table.py`

Note: the resolver in this reference implementation reads rules directly
from the YAML file (via mapping.rules.load_rules) for simplicity. This
script is for the alternative path described in the design doc §5 —
storing the mapping table in Postgres so it can be edited without a
deploy. Wire load_rules() to query this table instead of the YAML file
if you adopt that approach.
"""

from __future__ import annotations

from sqlalchemy import Column, MetaData, String, Table, create_engine, insert

from finban_mapper.config import settings
from finban_mapper.mapping.rules import load_rules

metadata = MetaData()

mapping_rule_table = Table(
    "mapping_rule",
    metadata,
    Column("id", String(64), primary_key=True),
    Column("external_system", String(64)),
    Column("external_type", String(64)),
    Column("external_state", String(64)),
    Column("predicate", String(128), nullable=True),
    Column("finban_entity_type", String(64)),
    Column("finban_state", String(64)),
    Column("is_fallback", String(8)),
)


def main() -> None:
    engine = create_engine(settings.database_url)
    metadata.create_all(engine)

    rules = load_rules(settings.mapping_rules_path)
    with engine.begin() as conn:
        conn.execute(mapping_rule_table.delete())
        conn.execute(
            insert(mapping_rule_table),
            [
                {
                    "id": r.id,
                    "external_system": r.external_system,
                    "external_type": r.external_type,
                    "external_state": r.external_state,
                    "predicate": r.predicate,
                    "finban_entity_type": r.finban_entity_type,
                    "finban_state": r.finban_state,
                    "is_fallback": str(r.is_fallback),
                }
                for r in rules
            ],
        )
    print(f"Seeded {len(rules)} mapping rules.")


if __name__ == "__main__":
    main()
