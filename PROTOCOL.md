# Protocol

Adapters implement this contract. The kernel does not grant adapters permission.

## Objects

- **Writ** — capability: actor, actions, resource, expiry, revoke flag.
- **Job** — ordered steps and a resource. Cursor advances only after an authorized success.
- **Graph** — typed live state.
- **Ledger entry** — `{kind, payload, at, prev, digest, writ_id, job_id}`.
  `digest = sha256(prev|kind|canonical_json(payload)|at|id)`.
- **Adapter** — `execute(step, job, graph, writ)`.

## Rules

1. A step runs only if a live writ allows `(actor, action, resource)`.
2. On handler failure the graph is restored to the pre-step snapshot.
3. `job.close()` on an incomplete cursor raises.
4. `ledger.verify()` must be true after a successful run.

Conformance tests: `tests/test_invariants.py`.
