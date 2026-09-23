from silex.agent import run_prompt
from silex.planner import Proposal
from silex.runtime import Status


def test_agent_still_closes_through_writ():
    snap = run_prompt("kit order-1")
    assert snap["job"]["status"] == Status.CLOSED.value
    assert snap["proposal"]["source"] in {"local", "llm", "llm-fallback"}
    assert "raw" not in snap["proposal"]


def test_proposal_omits_provider_payload():
    p = Proposal("kit", ["pick"], "local")
    assert p.as_dict() == {"goal": "kit", "steps": ["pick"], "source": "local"}
