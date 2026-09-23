from silex.loop import STEPS, build_demo_world
from silex.runtime import Status


def test_happy_path_closes():
    _, ledger, runtime, issuer = build_demo_world()
    job = runtime.submit("close work order 1", STEPS)
    for step in STEPS:
        runtime.tick(job, issuer.issue("cell-1", step, "order-1"))
    assert job.status == Status.CLOSED
    assert any(e.kind == "job.closed" for e in ledger.entries)


def test_quality_fail_halts():
    graph, _, runtime, issuer = build_demo_world()
    graph.upsert(graph.get("quality-1").__class__("quality-1", "gate", {"pass": False}))
    job = runtime.submit("close work order 1", STEPS)
    for step in STEPS:
        runtime.tick(job, issuer.issue("cell-1", step, "order-1"))
        if job.status == Status.HALTED:
            break
    assert job.status == Status.HALTED
    assert "quality" in (job.reason or "")
