from __future__ import annotations

from silex.adapters import SimulatedCell
from silex.actors import Actor, ActorKind
from silex.channel import Channel
from silex.graph import Graph, Node
from silex.ledger import Ledger
from silex.runtime import Job, Runtime
from silex.writ import Issuer, Writ

KITTING_STEPS = ["release", "confirm", "pick", "place", "quality", "close"]


def build_kitting_cell(*, quality_pass: bool = True) -> tuple[Graph, Ledger, Runtime, Issuer, Actor]:
    graph = Graph()
    graph.upsert(Node("order-1", "work_order", {"status": "ready", "sku": "KIT-A"}))
    graph.upsert(Node("parts-1", "parts", {"present": True, "sku": "KIT-A"}))
    graph.upsert(Node("cell-1", "cell", {"ready": True, "busy": False, "vendor": "sim"}))
    graph.upsert(Node("quality-1", "gate", {"pass": quality_pass}))
    ledger = Ledger()
    issuer = Issuer()
    runtime = Runtime(graph, ledger, issuer)
    channel = Channel()
    cell = SimulatedCell("cell-1", channel)

    def bind(step: str):
        def _fn(job: Job, g: Graph, writ: Writ) -> None:
            cell.execute(step, job, g, writ, ticket=channel.ticket(cell.actor_id, step, writ.id))

        return _fn

    for step in KITTING_STEPS:
        runtime.register(step, bind(step))
    actor = Actor(id="cell-1", kind=ActorKind.CELL, vendor="sim")
    return graph, ledger, runtime, issuer, actor
