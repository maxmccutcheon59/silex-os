from __future__ import annotations

from silex.errors import SilexError
from silex.planner import Proposal, propose
from silex.runtime import Job, Status
from silex.wedge import KITTING_STEPS, build_kitting_cell
from silex.writ import Writ


class Plant:
    def __init__(self) -> None:
        self.reset(quality_pass=True)

    def reset(self, quality_pass: bool = True) -> None:
        self.graph, self.ledger, self.runtime, self.issuer, self.actor = build_kitting_cell(
            quality_pass=quality_pass
        )
        self.quality_pass = quality_pass
        self.active_writ: Writ | None = None
        self.last_proposal: Proposal | None = None
        self.job_id: str | None = None

    def snapshot(self) -> dict:
        job = self._job()
        writ = self.active_writ
        return {
            "actor": {"id": self.actor.id, "kind": self.actor.kind.value, "vendor": self.actor.vendor},
            "quality_pass": self.quality_pass,
            "graph": {nid: {"kind": n.kind, "attrs": n.attrs} for nid, n in self.graph.nodes.items()},
            "job": None
            if job is None
            else {
                "id": job.id,
                "goal": job.goal,
                "steps": job.steps,
                "cursor": job.cursor,
                "status": job.status.value,
                "reason": job.reason,
            },
            "writ": None
            if writ is None
            else {
                "id": writ.id,
                "actor": writ.actor,
                "actions": sorted(writ.actions),
                "resource": writ.resource,
                "revoked": writ.revoked,
                "expires_at": writ.expires_at,
            },
            "ledger": [
                {
                    "kind": e.kind,
                    "payload": e.payload,
                    "at": e.at,
                    "digest": e.digest[:12],
                    "writ_id": e.writ_id,
                    "job_id": e.job_id,
                }
                for e in self.ledger.entries[-40:]
            ],
            "chain_ok": self.ledger.verify(),
            "proposal": None if self.last_proposal is None else self.last_proposal.as_dict(),
            "allowed_steps": list(KITTING_STEPS),
        }

    def _job(self) -> Job | None:
        if self.job_id is None:
            return None
        return self.runtime.jobs.get(self.job_id)

    def set_quality(self, passed: bool) -> dict:
        self.graph.require("quality-1").attrs["pass"] = passed
        self.quality_pass = passed
        self.ledger.append("quality.set", {"pass": passed})
        return self.snapshot()

    def propose(self, text: str) -> dict:
        self.last_proposal = propose(text)
        self.ledger.append("plan.proposed", self.last_proposal.as_dict())
        return self.snapshot()

    def submit(self, goal: str | None = None, steps: list[str] | None = None) -> dict:
        if self.last_proposal is not None:
            goal = goal or self.last_proposal.goal
            steps = steps or self.last_proposal.steps
        job = self.runtime.submit(goal or "kit order-1", steps or list(KITTING_STEPS))
        self.job_id = job.id
        return self.snapshot()

    def issue(self, actions: list[str] | None = None) -> dict:
        job = self._job()
        actions = actions or (job.steps if job else list(KITTING_STEPS))
        self.active_writ = self.issuer.issue(self.actor.id, actions, "order-1")
        self.ledger.append(
            "writ.issued",
            {"actions": sorted(self.active_writ.actions), "resource": "order-1"},
            writ_id=self.active_writ.id,
            job_id=self.job_id,
        )
        return self.snapshot()

    def revoke(self) -> dict:
        if self.active_writ is None:
            raise SilexError("no writ to revoke")
        self.issuer.revoke(self.active_writ.id)
        self.ledger.append("writ.revoked", {}, writ_id=self.active_writ.id, job_id=self.job_id)
        return self.snapshot()

    def tick(self) -> dict:
        job = self._require_job()
        writ = self._require_writ()
        if job.status not in {Status.CLOSED, Status.HALTED}:
            self.runtime.tick(job, writ)
        return self.snapshot()

    def run(self) -> dict:
        self.runtime.run(self._require_job(), self._require_writ())
        return self.snapshot()

    def _require_job(self) -> Job:
        job = self._job()
        if job is None:
            raise SilexError("no job submitted")
        return job

    def _require_writ(self) -> Writ:
        if self.active_writ is None:
            raise SilexError("no writ issued")
        return self.active_writ
