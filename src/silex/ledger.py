from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class Entry:
    id: str
    kind: str
    payload: dict[str, Any]
    at: str
    writ_id: str | None = None
    job_id: str | None = None


class Ledger:
    def __init__(self) -> None:
        self.entries: list[Entry] = field(default_factory=list) if False else []

    def append(
        self,
        kind: str,
        payload: dict[str, Any],
        writ_id: str | None = None,
        job_id: str | None = None,
    ) -> Entry:
        entry = Entry(
            id=str(uuid4()),
            kind=kind,
            payload=payload,
            at=datetime.now(timezone.utc).isoformat(),
            writ_id=writ_id,
            job_id=job_id,
        )
        self.entries.append(entry)
        return entry
