# finban-mapping-service

Normalizes external accounting-system states (Lexware Office today) into
finban's canonical domain model (Lead, Offer, Order, Sales Invoice, Credit
Note, Bank Transaction).

See the accompanying design doc for the full architecture rationale. In short:

- `domain/` — the canonical model, zero vendor knowledge.
- `mapping/` — the mapping table as data (`seed_rules.yaml`) + predicates
  for conditional rows (e.g. offer value vs. related invoice value).
- `adapters/` — one subpackage per external system; only place vendor
  field names are known.
- `engine/` — `resolve_state()`, the seam that turns a normalized event
  into a finban state + rule id.
- `persistence/` — idempotent writes, current-state table, full audit
  trail (`state_change`).
- `api/` — query endpoints for current state and history.

## Local development

```bash
docker compose up --build
```

Then in another shell, run migrations and seed data:

```bash
docker compose exec app alembic upgrade head
docker compose exec app python scripts/seed_mapping_table.py
```

API available at `http://localhost:8000`, docs at `/docs`.

## Running tests

```bash
pip install -e ".[dev]"
pytest tests/unit tests/integration tests/contract tests/snapshot -v
```

Run the canary check separately (not part of CI) against a real sandbox:

```bash
python scripts/canary_check.py
```

## Adding a new external system

1. Add a subpackage under `adapters/` implementing `BaseAdapter`.
2. Add rows to a new mapping file (or extend `seed_rules.yaml`) — no
   changes needed in `engine/` or `domain/`.
3. Add contract tests with recorded fixtures for the new adapter.
4. Add a fallback row for every `(system, type)` pair so nothing is
   silently dropped — the CI completeness check enforces this.

## Adding a new conditional mapping rule

1. Write the predicate as a pure function in `mapping/predicates.py`.
2. Register it in `mapping/registry.py`.
3. Reference it by name in a `seed_rules.yaml` row.
4. Add unit tests for every branch in `tests/unit/test_predicates.py`
   and a resolution test in `tests/unit/test_resolver.py`.
