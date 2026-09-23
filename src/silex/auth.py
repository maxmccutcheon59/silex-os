from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from silex.errors import SilexError


class Role(str, Enum):
    OPERATOR = "operator"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"


# Least privilege for the local board. Supervisor may revoke. Admin may reset.
PERMISSIONS = {
    "/api/state": {Role.OPERATOR, Role.SUPERVISOR, Role.ADMIN},
    "/api/propose": {Role.OPERATOR, Role.SUPERVISOR, Role.ADMIN},
    "/api/submit": {Role.OPERATOR, Role.SUPERVISOR, Role.ADMIN},
    "/api/issue": {Role.SUPERVISOR, Role.ADMIN},
    "/api/tick": {Role.OPERATOR, Role.SUPERVISOR, Role.ADMIN},
    "/api/run": {Role.OPERATOR, Role.SUPERVISOR, Role.ADMIN},
    "/api/quality": {Role.SUPERVISOR, Role.ADMIN},
    "/api/revoke": {Role.SUPERVISOR, Role.ADMIN},
    "/api/reset": {Role.ADMIN},
}


@dataclass(frozen=True)
class Principal:
    name: str
    role: Role


def parse_role(value: str | None) -> Role:
    if not value:
        return Role.OPERATOR
    try:
        return Role(value)
    except ValueError as exc:
        raise SilexError(f"unknown role {value}") from exc


def require(path: str, role: Role) -> None:
    allowed = PERMISSIONS.get(path)
    if allowed is None:
        raise SilexError("unknown route")
    if role not in allowed:
        raise SilexError(f"role {role.value} cannot call {path}")
