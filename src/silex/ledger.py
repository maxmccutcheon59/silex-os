from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any
from uuid import uuid4

from silex.errors import SilexError


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


def canonical(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, default=str, separators=(",", ":"))


def digest_for(prev: str, kind: str, payload: dict[str, Any], at: str, entry_id: str) -> str:
    raw = f"{prev}|{kind}|{canonical(payload)}|{at}|{entry_id}".encode()
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
        payload = deepcopy(payload)
        prev = self.entries[-1].digest if self.entries else self.GENESIS
        at = datetime.now(timezone.utc).isoformat()
        entry_id = str(uuid4())
        entry = Entry(
            id=entry_id,
            kind=kind,
            payload=payload,
            at=at,
            prev=prev,
            digest=digest_for(prev, kind, payload, at, entry_id),
            writ_id=writ_id,
            job_id=job_id,
        )
        self.entries.append(entry)
        return entry

    def verify(self) -> bool:
        prev = self.GENESIS
        for entry in self.entries:
            expected = digest_for(prev, entry.kind, entry.payload, entry.at, entry.id)
            if entry.prev != prev or entry.digest != expected:
                return False
            prev = entry.digest
        return True

    def save(self, path: str | Path) -> Path:
        if not self.verify():
            raise SilexError("refusing to save a broken ledger")
        dest = Path(path)
        dest.write_text(json.dumps([asdict(e) for e in self.entries], indent=2))
        return dest

    @classmethod
    def load(cls, path: str | Path) -> Ledger:
        ledger = cls()
        raw = json.loads(Path(path).read_text())
        for item in raw:
            ledger.entries.append(Entry(**item))
        if not ledger.verify():
            raise SilexError("ledger failed verification on load")
        return ledger
