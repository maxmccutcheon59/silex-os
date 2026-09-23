# Security

## Threat model

Models, scripts, and adapters will try to act without permission. The kernel fails closed.

## Kernel

- Explicit `actor` on every tick.
- HMAC-signed writs. Tamper → `bad_signature`.
- Issuer secret from `SILEX_ISSUER_SECRET` or `SILEX_ISSUER_SECRET_FILE` (min 16 chars).
- Adapter channel ticket required before a simulated cell executes.
- Halt codes are structured.

## Console

- Localhost default.
- `X-Silex-Token` on `/api/*`.
- Roles: operator / supervisor / admin (`X-Silex-Role`).
  Operators cannot issue, revoke, or reset. Supervisors cannot reset.
- Remote bind requires `SILEX_ALLOW_REMOTE=1` **and** `SILEX_CONSOLE_TOKEN`.

## Not yet

Mutual TLS with a plant CA, SSO (OIDC), and HSM-backed keys. Those need a real site. The channel ticket and secret file are the local stand-ins.
