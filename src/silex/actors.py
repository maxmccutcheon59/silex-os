from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ActorKind(str, Enum):
    CELL = "cell"
    ARM = "arm"
    AMR = "amr"
    HUMANOID = "humanoid"
    HUMAN = "human"
    POLICY = "policy"


@dataclass(frozen=True)
class Actor:
    id: str
    kind: ActorKind
    vendor: str = "sim"
