from __future__ import annotations

from dataclasses import dataclass

from silex.wedge import KITTING_STEPS


@dataclass(frozen=True)
class PolicyPack:
    name: str
    resource: str
    actions: tuple[str, ...]

    def allows(self, action: str, resource: str) -> bool:
        return resource == self.resource and action in self.actions


KITTING = PolicyPack(
    name="kitting.v1",
    resource="order-1",
    actions=tuple(KITTING_STEPS),
)
