from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from silex.errors import SilexError


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _canonical(actor: str, actions: frozenset[str], resource: str, issued_at: str, expires_at: str | None, writ_id: str) -> bytes:
    payload = {
        "id": writ_id,
        "actor": actor,
        "actions": sorted(actions),
        "resource": resource,
        "issued_at": issued_at,
        "expires_at": expires_at,
    }
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()


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
    signature: str = ""

    def allows(self, actor: str, action: str, resource: str, at: datetime | None = None) -> bool:
        return self.deny_reason(actor, action, resource, at) is None

    def deny_reason(self, actor: str, action: str, resource: str, at: datetime | None = None) -> str | None:
        if self.revoked:
            return f"writ {self.id} revoked"
        if self.actor != actor:
            return f"writ {self.id} issued to {self.actor}, not {actor}"
        if self.resource != resource:
            return f"writ {self.id} covers {self.resource}, not {resource}"
        if action not in self.actions:
            return f"writ {self.id} does not allow {action}"
        if self.expires_at:
            moment = at or _now()
            if moment > datetime.fromisoformat(self.expires_at):
                return f"writ {self.id} expired"
        return None


class Issuer:
    def __init__(self, secret: str | None = None) -> None:
        self.secret = (secret or os.environ.get("SILEX_ISSUER_SECRET") or secrets.token_hex(32)).encode()
        self.issued: dict[str, Writ] = {}

    def _sign(self, writ: Writ) -> str:
        body = _canonical(writ.actor, writ.actions, writ.resource, writ.issued_at, writ.expires_at, writ.id)
        return hmac.new(self.secret, body, hashlib.sha256).hexdigest()

    def verify(self, writ: Writ) -> bool:
        if not writ.signature:
            return False
        expected = self._sign(writ)
        return hmac.compare_digest(expected, writ.signature)

    def issue(
        self,
        actor: str,
        actions: str | list[str] | set[str],
        resource: str,
        ttl_seconds: int | None = 3600,
        **constraints,
    ) -> Writ:
        action_set = frozenset([actions] if isinstance(actions, str) else actions)
        if not action_set:
            raise SilexError("refusing empty action set")
        if not actor or not resource:
            raise SilexError("actor and resource are required")
        now = _now()
        expires = (now + timedelta(seconds=ttl_seconds)).isoformat() if ttl_seconds else None
        writ = Writ(
            id=str(uuid4()),
            actor=actor,
            actions=action_set,
            resource=resource,
            constraints=dict(constraints),
            issued_at=now.isoformat(),
            expires_at=expires,
        )
        writ.signature = self._sign(writ)
        self.issued[writ.id] = writ
        return writ

    def revoke(self, writ_id: str) -> Writ:
        writ = self.issued[writ_id]
        writ.revoked = True
        return writ
