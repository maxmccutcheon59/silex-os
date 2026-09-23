from pathlib import Path

import pytest

from silex.cli import _safe_out
from silex.errors import SilexError
from silex.ledger import Ledger
from silex.server import serve
from silex.wedge import KITTING_STEPS, build_kitting_cell
from silex.runtime import HaltCode, Status


def test_remote_bind_refused(monkeypatch):
    monkeypatch.delenv("SILEX_ALLOW_REMOTE", raising=False)
    with pytest.raises(SilexError, match="non-local bind"):
        serve("0.0.0.0", 8080)


def test_export_rejects_parent(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SilexError, match="current directory"):
        _safe_out("../outside.json")


def test_ledger_roundtrip(tmp_path):
    ledger = Ledger()
    ledger.append("job.submitted", {"goal": "kit"})
    path = tmp_path / "ledger.json"
    ledger.save(path)
    loaded = Ledger.load(path)
    assert loaded.verify()
    assert loaded.entries[0].kind == "job.submitted"


def test_tampered_signature_halts():
    _, _, runtime, issuer, actor = build_kitting_cell()
    job = runtime.submit("kit", KITTING_STEPS)
    writ = issuer.issue(actor.id, KITTING_STEPS, "order-1")
    writ.signature = "ab" * 32
    runtime.tick(job, writ, actor=actor.id)
    assert job.status == Status.HALTED
    assert job.halt_code == HaltCode.BAD_SIGNATURE.value
