from silex.policy import KITTING
from silex.run_replay import FIXTURES, build_replay
from silex.runtime import Status


def test_replay_ok_closes():
    runtime, issuer, actor, adapter, ledger, _graph = build_replay(FIXTURES / "kitting_ok.jsonl")
    job = runtime.submit("replay ok", list(KITTING.actions))
    runtime.run(job, issuer.issue(actor.id, list(KITTING.actions), KITTING.resource), actor=actor.id)
    assert job.status == Status.CLOSED
    assert adapter.cursor == 6
    assert ledger.verify()


def test_replay_quality_fail_halts():
    runtime, issuer, actor, _adapter, _ledger, _graph = build_replay(FIXTURES / "kitting_fail.jsonl")
    job = runtime.submit("replay fail", list(KITTING.actions))
    runtime.run(job, issuer.issue(actor.id, list(KITTING.actions), KITTING.resource), actor=actor.id)
    assert job.status == Status.HALTED
    assert "quality" in (job.reason or "")
