from __future__ import annotations

from typing import Protocol

from silex.graph import Graph, Node
from silex.runtime import Job
from silex.writ import Writ


class ActorAdapter(Protocol):
    actor_id: str

    def execute(self, step: str, job: Job, graph: Graph, writ: Writ) -> None: ...


class SimulatedCell:
    """Stand-in for a real OEM controller. Kernel never talks to metal directly."""

    def __init__(self, actor_id: str = "cell-1") -> None:
        self.actor_id = actor_id

    def execute(self, step: str, job: Job, graph: Graph, writ: Writ) -> None:
        if step == "release":
            graph.require("order-1", status="ready")
            graph.upsert(Node("order-1", "work_order", {"status": "released"}))
            return
        if step == "confirm":
            graph.require("parts-1", present=True)
            graph.require("cell-1", ready=True)
            return
        if step == "pick":
            graph.require("cell-1", ready=True)
            graph.upsert(Node("cell-1", "cell", {"ready": True, "busy": True}))
            graph.upsert(Node("tote-1", "tote", {"held": True}))
            return
        if step == "place":
            graph.require("tote-1", held=True)
            graph.upsert(Node("kit-1", "kit", {"complete": True}))
            return
        if step == "quality":
            gate = graph.require("quality-1")
            if not gate.attrs.get("pass"):
                raise ValueError("quality gate failed")
            return
        if step == "close":
            graph.upsert(Node("order-1", "work_order", {"status": "closed"}))
            graph.upsert(Node("cell-1", "cell", {"ready": True, "busy": False}))
            return
        raise ValueError(f"unknown step {step}")
