"""Publishes a domain event after a state change is committed.

Swap the body of `publish()` for a real SQS/SNS client in production;
this stub logs so local dev and tests don't need AWS credentials.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass

logger = logging.getLogger("finban_mapper.events")


@dataclass
class DomainEvent:
    entity_type: str
    entity_id: str
    old_state: str | None
    new_state: str
    rule_id: str


class EventPublisher:
    def publish(self, event: DomainEvent) -> None:
        logger.info("domain_event %s", json.dumps(asdict(event)))
