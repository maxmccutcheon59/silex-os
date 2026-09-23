# Security

## Threat model

Models, scripts, and adapters will try to act without permission. The kernel fails closed.

## Kernel

- No graph mutation without a live writ for `(actor, action, resource)`.
- Agents propose. Executing actors are separate identities.
- Denied or failed steps restore the prior graph.
- Step names are allow-listed. Unknown verbs are dropped.
- Proposal text is capped. Provider payloads and API keys are not logged.

## Console

- Binds to `127.0.0.1` by default.
- Non-local binds require `SILEX_ALLOW_REMOTE=1`.
- POST bodies capped at 16 KiB.
- JSON-only object bodies.
- Generic 500 responses. No stack traces to the client.
- `nosniff`, `DENY` framing, `no-store`, strict CSP for the local page.

## Export

- Ledger export paths must resolve under the current working directory.

## Secrets

- `SILEX_LLM_KEY` is environment-only. Never commit it.
- Do not file public issues that include plant data or credentials.

## Reporting

Notify the repository owner privately.
