from pathlib import Path

from silex.export import write_ledger
from silex.ledger import Ledger


def test_export_roundtrip(tmp_path: Path):
    ledger = Ledger()
    ledger.append("job.submitted", {"goal": "kit"})
    dest = write_ledger(ledger, tmp_path / "ledger.json")
    text = dest.read_text()
    assert "job.submitted" in text
    assert "verified" in text
