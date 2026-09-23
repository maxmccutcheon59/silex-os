from silex.ledger import Ledger


def test_chain_verifies():
    ledger = Ledger()
    ledger.append("a", {"n": 1})
    ledger.append("b", {"n": 2})
    assert ledger.verify()
    ledger.entries[1] = ledger.entries[1].__class__(
        **{**ledger.entries[1].__dict__, "payload": {"n": 99}}
    )
    assert not ledger.verify()
