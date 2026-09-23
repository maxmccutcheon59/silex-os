# Security

## Threat model

Silex assumes models, scripts, and adapters will try to act without permission. The kernel must fail closed.

## Rules

- No step mutates the graph without a live writ for `(actor, action, resource)`.
- Agents propose. Executing actors are separate identities.
- Denied or failed steps roll the graph back.
- API keys live in environment variables only. Never in the repo, ledger, or UI.
- Planner output is allow-listed to known step names. Unknown tokens are dropped.
- Ledger payloads must not include `SILEX_LLM_KEY` or raw provider secrets.
- The console binds to 127.0.0.1 by default. Do not expose it to a plant network without auth in front.

## Reporting

Privately notify the repository owner. Do not file public issues that include plant data or credentials.
