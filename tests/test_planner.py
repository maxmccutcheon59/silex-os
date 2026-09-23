from silex.planner import local_propose


def test_local_propose_defaults_to_kitting():
    p = local_propose("please run the cell")
    assert p.source == "local"
    assert "pick" in p.steps
    assert "close" in p.steps
