from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable
from uuid import uuid4

from silex.graph import Graph
from silex.ledger import Ledger
from silex.writ import Issuer, Writ


class Status(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    CLOSED = "closed"
    HALTED = "halted"


class HaltCode(str, Enum):
    DENIED = "denied"
    WRONG_ACTOR = "wrong_actor"
    REVOKED = "revoked"
    EXPIRED = "expired"
    NO_HANDLER = "no_handler"
    ADAPTER = "adapter"
    BAD_SIGNATURE = "bad_signature"
    INCOMPLETE = "incomplete"


@dataclass
class Job:
    id: str
    goal: str
    steps: list[str]
    resource: str = "order-1"
    status: Status = Status.PENDING
    reason: str | None = None
    halt_code: str | None = None
    cursor: int = 0
    events: list[str] = field(default_factory=list)

    def close(self, reason: str = "completed") -> None:
        if self.cursor < len(self.steps):
            raise RuntimeError("refusing to close incomplete job")
        self.status = Status.CLOSED
        self.reason = reason
        self.halt_code = None

    def halt(self, reason: str, code: HaltCode = HaltCode.DENIED) -> None:
        self.status = Status.HALTED
        self.reason = reason
        self.halt_code = code.value


StepFn = Callable[[Job, Graph, Writ], None]


def _code_from_reason(reason: str) -> HaltCode:
    if "revoked" in reason:
        return HaltCode.REVOKED
    if "expired" in reason:
        return HaltCode.EXPIRED
    if ", not " in reason:
        return HaltCode.WRONG_ACTOR
    return HaltCode.DENIED


class Runtime:
    def __init__(self, graph: Graph, ledger: Ledger, issuer: Issuer | None = None) -> None:
        self.graph = graph
        self.ledger = ledger
        self.issuer = issuer
        self.jobs: dict[str, Job] = {}
        self.handlers: dict[str, StepFn] = {}

    def register(self, step: str, fn: StepFn) -> None:
        self.handlers[step] = fn

    def submit(self, goal: str, steps: list[str], resource: str = "order-1") -> Job:
        job = Job(id=str(uuid4()), goal=goal, steps=list(steps), resource=resource)
        self.jobs[job.id] = job
        self.ledger.append(
            "job.submitted",
            {"goal": goal, "steps": list(steps), "resource": resource},
            job_id=job.id,
        )
        return job

    def tick(self, job: Job, writ: Writ, *, actor: str) -> Job:
        if job.status in {Status.CLOSED, Status.HALTED}:
            return job
        if job.cursor >= len(job.steps):
            job.close()
            self.ledger.append("job.closed", {"reason": job.reason}, writ_id=writ.id, job_id=job.id)
            return job

        if self.issuer is not None and not self.issuer.verify(writ):
            job.halt("writ signature invalid", HaltCode.BAD_SIGNATURE)
            self.ledger.append(
                "job.halted",
                {"reason": job.reason, "code": job.halt_code},
                writ_id=writ.id,
                job_id=job.id,
            )
            return job

        step = job.steps[job.cursor]
        if not writ.allows(actor, step, job.resource):
            reason = writ.deny_reason(actor, step, job.resource) or f"writ {writ.id} does not allow {step}"
            job.halt(reason, _code_from_reason(reason))
            self.ledger.append(
                "job.halted",
                {"reason": job.reason, "code": job.halt_code, "step": step, "actor": actor},
                writ_id=writ.id,
                job_id=job.id,
            )
            return job

        fn = self.handlers.get(step)
        if fn is None:
            job.halt(f"no handler for {step}", HaltCode.NO_HANDLER)
            self.ledger.append(
                "job.halted",
                {"reason": job.reason, "code": job.halt_code, "step": step},
                writ_id=writ.id,
                job_id=job.id,
            )
            return job

        prior = self.graph.snapshot()
        job.status = Status.RUNNING
        try:
            fn(job, self.graph, writ)
        except Exception as exc:
            self.graph.restore(prior)
            job.halt(str(exc)[:200], HaltCode.ADAPTER)
            self.ledger.append(
                "job.halted",
                {"reason": job.reason, "code": job.halt_code, "step": step},
                writ_id=writ.id,
                job_id=job.id,
            )
            return job

        job.cursor += 1
        self.ledger.append("job.step", {"step": step, "actor": actor}, writ_id=writ.id, job_id=job.id)
        if job.cursor >= len(job.steps):
            job.close()
            self.ledger.append("job.closed", {"reason": job.reason}, writ_id=writ.id, job_id=job.id)
        return job

    def run(self, job: Job, writ: Writ, *, actor: str) -> Job:
        while job.status not in {Status.CLOSED, Status.HALTED}:
            self.tick(job, writ, actor=actor)
        return job
