from __future__ import annotations

from silex.graph import Graph, Node
from silex.ledger import Ledger
from silex.runtime import Job, Runtime
from silex.writ import Issuer, Writ

STEPS = ["release", "confirm", "execute", "quality", "close"]


def _release(job: Job, graph: Graph, writ: Writ) -> None:
    graph.require("order-1", status="ready")
    graph.upsert(Node("order-1", "work_order", {"status": "released"}))


def _confirm(job: Job, graph: Graph, writ: Writ) -> None:
    graph.require("parts-1", present=True)
    graph.require("cell-1", ready=True)


def _execute(job: Job, graph: Graph, writ: Writ) -> None:
    graph.require("cell-1", ready=True)
    graph.upsert(Node("cell-1", "cell", {"ready": True, "busy": True}))


def _quality(job: Job, graph: Graph, writ: Writ) -> None:
    gate = graph.require("quality-1")
    if not gate.attrs.get("pass"):
        raise ValueError("quality gate failed")


def _close(job: Job, graph: Graph, writ: Writ) -> None:
    graph.upsert(Node("order-1", "work_order", {"status": "closed"}))
    graph.upsert(Node("cell-1", "cell", {"ready": True, "busy": False}))


def build_demo_world() -> tuple[Graph, Ledger, Runtime, Issuer]:
    graph = Graph()
    graph.upsert(Node("order-1", "work_order", {"status": "ready"}))
    graph.upsert(Node("parts-1", "parts", {"present": True}))
    graph.upsert(Node("cell-1", "cell", {"ready": True, "busy": False}))
    graph.upsert(Node("quality-1", "gate", {"pass": True}))
    ledger = Ledger()
    runtime = Runtime(graph, ledger)
    runtime.register("release", _release)
    runtime.register("confirm", _confirm)
    runtime.register("execute", _execute)
    runtime.register("quality", _quality)
    runtime.register("close", _close)
    return graph, ledger, runtime, Issuer()
