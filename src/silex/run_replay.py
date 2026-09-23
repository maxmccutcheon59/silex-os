from __future__ import annotations

from pathlib import Path

from silex.actors import Actor, ActorKind
from silex.graph import Graph, Node
from silex.ledger import Ledger
from silex.policy import KITTING
from silex.replay import ReplayAdapter, load_log
from silex.runtime import Job, Runtime, Status
from silex.writ import Issuer, Writ

FIXTURES = Path(__file__).parent / "fixtures"


def build_replay(path: str | Path) -> tuple[Runtime, Issuer, Actor, ReplayAdapter, Ledger, Graph]:
    events = load_log(path)
    graph = Graph()
    graph.upsert(Node("order-1", "work_order", {"status": "ready", "sku": "KIT-A"}))
    graph.upsert(Node("parts-1", "parts", {"present": True}))
    graph.upsert(Node("cell-1", "cell", {"ready": True, "busy": False, "vendor": "log"}))
    graph.upsert(Node("quality-1", "gate", {"pass": True}))
    ledger = Ledger()
    runtime = Runtime(graph, ledger)
    adapter = ReplayAdapter(events)

    def bind(step: str):
        def _fn(job: Job, g: Graph, writ: Writ) -> None:
            adapter.execute(step, job, g, writ)

        return _fn

    for step in KITTING.actions:
        runtime.register(step, bind(step))
    actor = Actor(id="cell-1", kind=ActorKind.CELL, vendor="log")
    return runtime, Issuer(), actor, adapter, ledger, graph


def run_file(path: str | Path) -> Status:
    runtime, issuer, actor, _adapter, ledger, graph = build_replay(path)
    job = runtime.submit(f"replay {path}", list(KITTING.actions))
    writ = issuer.issue(actor.id, list(KITTING.actions), KITTING.resource)
    runtime.run(job, writ)
    print(f"status   {job.status.value}")
    print(f"reason   {job.reason}")
    print(f"ledger   {len(ledger.entries)} chain_ok={ledger.verify()}")
    print(f"order    {graph.get('order-1').attrs if graph.get('order-1') else None}")
    return job.status
