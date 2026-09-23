from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from silex.errors import SilexError
from silex.graph import Graph, Node
from silex.runtime import Job
from silex.writ import Writ


def load_log(path: str | Path) -> list[dict[str, Any]]:
    lines: list[dict[str, Any]] = []
    for raw in Path(path).read_text().splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        lines.append(json.loads(raw))
    if not lines:
        raise SilexError(f"empty controller log: {path}")
    return lines


def _apply_effects(graph: Graph, effects: dict[str, dict[str, Any]]) -> None:
    for node_id, attrs in effects.items():
        existing = graph.get(node_id)
        kind = str(attrs.get("_kind") or (existing.kind if existing else "node"))
        merged = dict(existing.attrs) if existing else {}
        merged.update({k: v for k, v in attrs.items() if k != "_kind"})
        graph.upsert(Node(node_id, kind, merged))


class ReplayAdapter:
    """Apply a recorded controller log. Each line must match the authorized step."""

    def __init__(self, events: list[dict[str, Any]], actor_id: str = "cell-1") -> None:
        self.actor_id = actor_id
        self.events = events
        self.cursor = 0

    def execute(self, step: str, job: Job, graph: Graph, writ: Writ) -> None:
        if self.cursor >= len(self.events):
            raise SilexError("controller log exhausted before job finished")
        event = self.events[self.cursor]
        logged = str(event.get("step", ""))
        if logged != step:
            raise SilexError(f"log step {logged!r} does not match authorized {step!r}")
        if event.get("ok", True) is False:
            raise SilexError(str(event.get("error") or f"controller failed on {step}"))
        _apply_effects(graph, event.get("effects") or {})
        self.cursor += 1
