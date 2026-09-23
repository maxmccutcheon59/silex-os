from __future__ import annotations

import json
from pathlib import Path

from silex.ledger import Ledger


def ledger_to_dict(ledger: Ledger) -> dict:
    return {
        "verified": ledger.verify(),
        "entries": [
            {
                "id": e.id,
                "kind": e.kind,
                "payload": e.payload,
                "at": e.at,
                "prev": e.prev,
                "digest": e.digest,
                "writ_id": e.writ_id,
                "job_id": e.job_id,
            }
            for e in ledger.entries
        ],
    }


def write_ledger(ledger: Ledger, path: str | Path) -> Path:
    dest = Path(path)
    dest.write_text(json.dumps(ledger_to_dict(ledger), indent=2))
    return dest
