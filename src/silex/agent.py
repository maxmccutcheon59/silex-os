from __future__ import annotations

from silex.actors import Actor, ActorKind
from silex.plant import Plant
from silex.runtime import Status

AGENT = Actor(id="agent-1", kind=ActorKind.AGENT, vendor="silex")


def run_prompt(text: str, plant: Plant | None = None) -> dict:
    """Agent proposes. Cell writ still required to move."""
    plant = plant or Plant()
    plant.propose(text)
    plant.submit()
    plant.issue()
    plant.run()
    snap = plant.snapshot()
    snap["agent"] = {"id": AGENT.id, "kind": AGENT.kind.value}
    return snap


def main_text(text: str) -> int:
    snap = run_prompt(text)
    job = snap.get("job") or {}
    print(f"agent    {AGENT.id}")
    print(f"proposal {snap.get('proposal')}")
    print(f"status   {job.get('status')}")
    print(f"reason   {job.get('reason')}")
    status = job.get("status")
    return 0 if status == Status.CLOSED.value else 2
