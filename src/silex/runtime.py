from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable
from uuid import uuid4

from silex.graph import Graph
from silex.ledger import Ledger
from silex.writ import Writ


class Status(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    CLOSED = "closed"
    HALTED = "halted"


@dataclass
class Job:
    id: str
    goal: str
    steps: list[str]
    status: Status = Status.PENDING
    reason: str | None = None
    cursor: int = 0
    events: list[str] = field(default_factory=list)

    def close(self, reason: str = "completed") -> None:
        if self.cursor < len(self.steps):
            raise RuntimeError("refusing to close incomplete job")
        self.status = Status.CLOSED
        self.reason = reason

    def halt(self, reason: str) -> None:
        self.status = Status.HALTED
        self.reason = reason


StepFn = Callable[[Job, Graph, Writ], None]


class Runtime:
    def __init__(self, graph: Graph, ledger: Ledger) -> None:
        self.graph = graph
        self.ledger = ledger
        self.jobs: dict[str, Job] = {}
        self.handlers: dict[str, StepFn] = {}

    def register(self, step: str, fn: StepFn) -> None:
        self.handlers[step] = fn

    def submit(self, goal: str, steps: list[str]) -> Job:
        job = Job(id=str(uuid4()), goal=goal, steps=steps)
        self.jobs[job.id] = job
        self.ledger.append("job.submitted", {"goal": goal, "steps": steps}, job_id=job.id)
        return job

    def tick(self, job: Job, writ: Writ) -> Job:
        if job.status in {Status.CLOSED, Status.HALTED}:
            return job
        if job.cursor >= len(job.steps):
            job.close()
            self.ledger.append("job.closed", {"reason": job.reason}, writ_id=writ.id, job_id=job.id)
            return job
        step = job.steps[job.cursor]
        if not writ.allows(writ.actor, step, writ.resource):
            reason = writ.deny_reason(writ.actor, step, writ.resource) or f"writ {writ.id} does not allow {step}"
            job.halt(reason)
            self.ledger.append("job.halted", {"reason": job.reason, "step": step}, writ_id=writ.id, job_id=job.id)
            return job
        job.status = Status.RUNNING
        fn = self.handlers.get(step)
        if fn is None:
            job.halt(f"no handler for {step}")
            self.ledger.append("job.halted", {"reason": job.reason, "step": step}, writ_id=writ.id, job_id=job.id)
            return job
        try:
            fn(job, self.graph, writ)
            job.cursor += 1
            self.ledger.append("job.step", {"step": step}, writ_id=writ.id, job_id=job.id)
        except Exception as exc:
            job.halt(str(exc))
            self.ledger.append("job.halted", {"reason": job.reason, "step": step}, writ_id=writ.id, job_id=job.id)
        if job.cursor >= len(job.steps) and job.status == Status.RUNNING:
            job.close()
            self.ledger.append("job.closed", {"reason": job.reason}, writ_id=writ.id, job_id=job.id)
        return job

    def run(self, job: Job, writ: Writ) -> Job:
        while job.status not in {Status.CLOSED, Status.HALTED}:
            self.tick(job, writ)
        return job
