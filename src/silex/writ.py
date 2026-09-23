from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from uuid import uuid4


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Writ:
    id: str
    actor: str
    actions: frozenset[str]
    resource: str
    constraints: dict
    issued_at: str
    expires_at: str | None = None
    revoked: bool = False

    def allows(self, actor: str, action: str, resource: str, at: datetime | None = None) -> bool:
        if self.revoked:
            return False
        if self.actor != actor or self.resource != resource:
            return False
        if action not in self.actions:
            return False
        if self.expires_at:
            moment = at or _now()
            if moment > datetime.fromisoformat(self.expires_at):
                return False
        return True

    def deny_reason(self, actor: str, action: str, resource: str, at: datetime | None = None) -> str | None:
        if self.allows(actor, action, resource, at):
            return None
        if self.revoked:
            return f"writ {self.id} revoked"
        if self.actor != actor:
            return f"writ {self.id} issued to {self.actor}, not {actor}"
        if self.resource != resource:
            return f"writ {self.id} covers {self.resource}, not {resource}"
        if action not in self.actions:
            return f"writ {self.id} does not allow {action}"
        return f"writ {self.id} expired"


class Issuer:
    def __init__(self) -> None:
        self.issued: dict[str, Writ] = {}

    def issue(
        self,
        actor: str,
        actions: str | list[str] | set[str],
        resource: str,
        ttl_seconds: int | None = 3600,
        **constraints,
    ) -> Writ:
        if isinstance(actions, str):
            action_set = frozenset([actions])
        else:
            action_set = frozenset(actions)
        now = _now()
        expires = (now + timedelta(seconds=ttl_seconds)).isoformat() if ttl_seconds else None
        writ = Writ(
            id=str(uuid4()),
            actor=actor,
            actions=action_set,
            resource=resource,
            constraints=constraints,
            issued_at=now.isoformat(),
            expires_at=expires,
        )
        self.issued[writ.id] = writ
        return writ

    def revoke(self, writ_id: str) -> Writ:
        writ = self.issued[writ_id]
        writ.revoked = True
        return writ
