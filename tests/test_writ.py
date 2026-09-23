from datetime import datetime, timedelta, timezone

import pytest

from silex.errors import SilexError
from silex.runtime import Status
from silex.wedge import KITTING_STEPS, build_kitting_cell
from silex.writ import Issuer


def test_revoke_halts():
    _, _, runtime, issuer, actor = build_kitting_cell()
    job = runtime.submit("kit order-1", KITTING_STEPS)
    writ = issuer.issue(actor.id, KITTING_STEPS, "order-1")
    issuer.revoke(writ.id)
    runtime.tick(job, writ, actor=actor.id)
    assert job.status == Status.HALTED
    assert "revoked" in (job.reason or "")


def test_wrong_action_denied():
    issuer = Issuer()
    writ = issuer.issue("cell-1", ["pick"], "order-1")
    assert not writ.allows("cell-1", "place", "order-1")


def test_expiry():
    issuer = Issuer()
    writ = issuer.issue("cell-1", ["pick"], "order-1", ttl_seconds=1)
    past = datetime.now(timezone.utc) + timedelta(seconds=5)
    assert not writ.allows("cell-1", "pick", "order-1", at=past)


def test_signature_roundtrip():
    issuer = Issuer(secret="a" * 32)
    writ = issuer.issue("cell-1", ["pick"], "order-1")
    assert issuer.verify(writ)
    writ.signature = "00" * 32
    assert not issuer.verify(writ)


def test_empty_actions_rejected():
    with pytest.raises(SilexError):
        Issuer().issue("cell-1", [], "order-1")
