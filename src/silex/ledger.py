from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class Entry:
    id: str
    kind: str
    payload: dict[str, Any]
    at: str
    prev: str
    digest: str
    writ_id: str | None = None
    job_id: str | None = None


def _digest(prev: str, kind: str, payload: dict[str, Any], at: str, entry_id: str) -> str:
    raw = f"{prev}|{kind}|{sorted(payload.items())}|{at}|{entry_id}".encode()
    return sha256(raw).hexdigest()


class Ledger:
    GENESIS = "0" * 64

    def __init__(self) -> None:
        self.entries: list[Entry] = []

    def append(
        self,
        kind: str,
        payload: dict[str, Any],
        writ_id: str | None = None,
        job_id: str | None = None,
    ) -> Entry:
        prev = self.entries[-1].digest if self.entries else self.GENESIS
        at = datetime.now(timezone.utc).isoformat()
        entry_id = str(uuid4())
        entry = Entry(
            id=entry_id,
            kind=kind,
            payload=payload,
            at=at,
            prev=prev,
            digest=_digest(prev, kind, payload, at, entry_id),
            writ_id=writ_id,
            job_id=job_id,
        )
        self.entries.append(entry)
        return entry

    def verify(self) -> bool:
        prev = self.GENESIS
        for entry in self.entries:
            if entry.prev != prev:
                return False
            if entry.digest != _digest(prev, entry.kind, entry.payload, entry.at, entry.id):
                return False
            prev = entry.digest
        return True
