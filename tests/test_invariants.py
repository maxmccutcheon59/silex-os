"""Conformance: the kernel cannot be walked around."""

from silex.graph import Node
from silex.runtime import Job, Runtime, Status
from silex.wedge import KITTING_STEPS, build_kitting_cell
from silex.writ import Issuer


def test_denied_writ_does_not_mutate_graph():
    graph, _ledger, runtime, issuer, actor = build_kitting_cell()
    before = graph.snapshot()
    job = runtime.submit("kit", KITTING_STEPS)
    writ = issuer.issue(actor.id, ["observe"], "order-1")
    runtime.tick(job, writ, actor=actor.id)
    assert job.status == Status.HALTED
    assert graph.get("order-1").attrs == before["order-1"].attrs


def test_wrong_actor_does_not_run():
    graph, _ledger, runtime, issuer, _actor = build_kitting_cell()
    before = graph.get("order-1").attrs.copy()
    job = runtime.submit("kit", KITTING_STEPS)
    writ = issuer.issue("cell-1", KITTING_STEPS, "order-1")
    runtime.tick(job, writ, actor="cell-9")
    assert job.status == Status.HALTED
    assert "not cell-9" in (job.reason or "")
    assert graph.get("order-1").attrs == before


def test_failed_step_rolls_back_partial_mutation():
    graph, ledger, runtime, issuer, actor = build_kitting_cell()

    def poison(job: Job, g, writ) -> None:
        g.upsert(Node("order-1", "work_order", {"status": "corrupt"}))
        raise RuntimeError("adapter exploded")

    runtime.handlers["release"] = poison
    before = graph.get("order-1").attrs.copy()
    job = runtime.submit("kit", ["release"])
    runtime.tick(job, issuer.issue(actor.id, ["release"], "order-1"))
    assert job.status == Status.HALTED
    assert graph.get("order-1").attrs == before
    assert ledger.verify()
