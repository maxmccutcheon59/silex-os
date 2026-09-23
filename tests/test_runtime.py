import pytest

from silex.runtime import Status
from silex.wedge import KITTING_STEPS, build_kitting_cell


def test_happy_path_closes():
    _, ledger, runtime, issuer, actor = build_kitting_cell()
    job = runtime.submit("kit order-1", KITTING_STEPS)
    runtime.run(job, issuer.issue(actor.id, KITTING_STEPS, "order-1"), actor=actor.id)
    assert job.status == Status.CLOSED
    assert any(e.kind == "job.closed" for e in ledger.entries)
    assert ledger.verify()


def test_quality_fail_halts():
    _, _, runtime, issuer, actor = build_kitting_cell(quality_pass=False)
    job = runtime.submit("kit order-1", KITTING_STEPS)
    runtime.run(job, issuer.issue(actor.id, KITTING_STEPS, "order-1"), actor=actor.id)
    assert job.status == Status.HALTED
    assert job.halt_code == "adapter"
    assert "quality" in (job.reason or "")


def test_refuse_close_incomplete():
    _, _, runtime, issuer, actor = build_kitting_cell()
    job = runtime.submit("kit order-1", KITTING_STEPS)
    runtime.tick(job, issuer.issue(actor.id, KITTING_STEPS, "order-1"), actor=actor.id)
    with pytest.raises(RuntimeError):
        job.close()
