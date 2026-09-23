from datetime import datetime, timedelta, timezone

from silex.runtime import Status
from silex.wedge import KITTING_STEPS, build_kitting_cell
from silex.writ import Issuer


def test_revoke_halts():
    _, _, runtime, issuer, actor = build_kitting_cell()
    job = runtime.submit("kit order-1", KITTING_STEPS)
    writ = issuer.issue(actor.id, KITTING_STEPS, "order-1")
    issuer.revoke(writ.id)
    runtime.tick(job, writ)
    assert job.status == Status.HALTED
    assert "revoked" in (job.reason or "")


def test_wrong_action_denied():
    issuer = Issuer()
    writ = issuer.issue("cell-1", ["pick"], "order-1")
    assert not writ.allows("cell-1", "place", "order-1")
    assert "does not allow place" in (writ.deny_reason("cell-1", "place", "order-1") or "")


def test_expiry():
    issuer = Issuer()
    writ = issuer.issue("cell-1", ["pick"], "order-1", ttl_seconds=1)
    past = datetime.now(timezone.utc) + timedelta(seconds=5)
    assert not writ.allows("cell-1", "pick", "order-1", at=past)
