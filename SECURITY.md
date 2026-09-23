# Security

## Threat model

Models, scripts, and adapters will try to act without permission. The kernel fails closed.

## Kernel

- No graph mutation without a live writ for `(actor, action, resource)`.
- `runtime.tick` requires an explicit `actor` argument.
- Writs are HMAC-SHA256 signed. Tampered signatures halt with `bad_signature`.
- Empty action sets are rejected.
- Denied or failed steps restore the prior graph.
- Halt codes: `denied`, `wrong_actor`, `revoked`, `expired`, `no_handler`, `adapter`, `bad_signature`.
- Agents propose. Executing actors are separate identities.
- Step names are allow-listed.

## Ledger

- Hash-chained, payload-copied entries.
- `save` refuses a broken chain.
- `load` verifies or raises.

## Console

- Binds to `127.0.0.1` by default.
- Non-local binds require `SILEX_ALLOW_REMOTE=1`.
- Session token required on `/api/*` (`X-Silex-Token`).
- POST bodies capped at 16 KiB.
- Generic 500 responses.

## Export

- Paths must resolve under the current working directory.

## Secrets

- `SILEX_LLM_KEY` and `SILEX_ISSUER_SECRET` are environment-only.
