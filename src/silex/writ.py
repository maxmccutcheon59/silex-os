from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class Writ:
    id: str
    actor: str
    action: str
    resource: str
    constraints: dict
    issued_at: str
    expires_at: str | None = None

    def allows(self, actor: str, action: str, resource: str) -> bool:
        return self.actor == actor and self.action == action and self.resource == resource


class Issuer:
    def issue(self, actor: str, action: str, resource: str, **constraints) -> Writ:
        return Writ(
            id=str(uuid4()),
            actor=actor,
            action=action,
            resource=resource,
            constraints=constraints,
            issued_at=datetime.now(timezone.utc).isoformat(),
        )
