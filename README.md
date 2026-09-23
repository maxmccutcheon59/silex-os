# Silex

Authorization, execution, and audit kernel for mixed robot and agent fleets.

A job is an ordered list of steps. A writ is a capability for `(actor, action, resource)`. The runtime runs the next step only when a live writ allows it. Failed or denied steps restore prior world state. The ledger is hash-chained.

Silex is not a safety-certified motion controller. OEM safety systems remain in the loop. See [LEGAL.md](LEGAL.md).

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

## Usage

```bash
silex version
silex demo
silex replay src/silex/fixtures/kitting_ok.jsonl
silex agent "kit order-1"
silex export --out ledger.json
silex serve --host 127.0.0.1 --port 8080
```

The console binds to localhost by default.

## Layout

| Path | Role |
|---|---|
| `PROTOCOL.md` | Adapter contract |
| `SECURITY.md` | Threat model |
| `src/silex/runtime.py` | Job lifecycle |
| `src/silex/writ.py` | Capability tokens |
| `src/silex/ledger.py` | Append-only record |
| `src/silex/replay.py` | Controller-log adapter |
