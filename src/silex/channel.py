from __future__ import annotations

import hashlib
import hmac
import os
import secrets

from silex.errors import SilexError


class Channel:
    """Shared-secret adapter channel. Stand-in for mTLS until a plant CA exists."""

    def __init__(self, secret: str | None = None) -> None:
        raw = secret or os.environ.get("SILEX_ADAPTER_SECRET") or secrets.token_hex(32)
        if len(raw) < 16:
            raise SilexError("adapter channel secret is too short")
        self.secret = raw.encode()

    def ticket(self, actor_id: str, step: str, writ_id: str) -> str:
        body = f"{actor_id}|{step}|{writ_id}".encode()
        return hmac.new(self.secret, body, hashlib.sha256).hexdigest()

    def accept(self, actor_id: str, step: str, writ_id: str, ticket: str) -> None:
        expected = self.ticket(actor_id, step, writ_id)
        if not ticket or not hmac.compare_digest(expected, ticket):
            raise SilexError("adapter channel rejected ticket")
