# Kernel rules

1. No graph mutation without a live writ for `(actor, action, resource)`.
2. Denied or failed steps restore the prior graph.
3. A job does not close if any step is unfinished.
4. The ledger verifies or it is not treated as evidence.
5. Adapters execute. The kernel authorizes and records.
