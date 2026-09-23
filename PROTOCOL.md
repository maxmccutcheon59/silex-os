# Silex protocol

This is the product. Adapters, OEMs, and models speak this. They do not bypass it.

## Law

1. An action exists only as a named step on a job.
2. A step runs only if a live writ allows `(actor, action, resource)` at that instant.
3. If the step fails or is denied, world state rolls back to the pre-step graph.
4. A job closes only after every step has succeeded.
5. The ledger is append-only and hash-chained. If verification fails, the record is not evidence.

## Objects

**Writ.** Capability token: `actor`, `actions`, `resource`, `expires_at`, `revoked`.
A writ is not a prompt and not a role name.

**Job.** Ordered steps plus a resource. Cursor only advances after a successful authorized step.

**Graph.** Typed live state. The only world the kernel admits.

**Ledger entry.** `{kind, payload, at, prev, digest, writ_id, job_id}`.
`digest = sha256(prev|kind|canonical_json(payload)|at|id)`.

**Adapter.** `execute(step, job, graph, writ)`. May touch metal or a log. May not grant itself permission.

## Conformance

An implementation is Silex-compatible only if:

- A missing, revoked, expired, or wrong-actor writ never mutates the graph.
- A handler exception never leaves a partial step applied.
- `job.close()` on an incomplete cursor raises.
- `ledger.verify()` is true after every successful run.

See `tests/test_invariants.py`.
