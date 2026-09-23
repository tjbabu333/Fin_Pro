from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from finban_mapper.adapters.base import ExternalEvent
from finban_mapper.mapping.rules import load_rules
from finban_mapper.persistence.models import Base

RULES_PATH = str(
    Path(__file__).parent.parent / "src" / "finban_mapper" / "mapping" / "seed_rules.yaml"
)


@pytest.fixture(scope="session")
def rules():
    return load_rules(RULES_PATH)


@pytest.fixture()
def db_session():
    """In-memory SQLite session for fast, isolated persistence tests."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def make_event(
    system: str = "lexware_office",
    type: str = "quotation",
    external_id: str = "ext-1",
    state: str = "quotation",
    data: dict | None = None,
) -> ExternalEvent:
    return ExternalEvent(
        system=system,
        type=type,
        external_id=external_id,
        state=state,
        updated_at=datetime(2026, 1, 1),
        data=data or {},
    )
