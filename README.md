# Silex

Authorization, execution, and audit kernel for mixed robot and agent fleets.

A job is an ordered list of steps. A writ is a capability for `(actor, action, resource)`. The runtime advances a job only when a live writ allows the next step. Failed or denied steps roll world state back. The ledger is hash-chained.

This is not a safety-certified motion controller. OEM safety systems stay in the loop. See [LEGAL.md](LEGAL.md).

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
silex serve --host 127.0.0.1 --port 8080
```

Export the last run's ledger after `demo` by using the Python API, or `silex export` after a replay.

```bash
silex replay
silex export --out ledger.json
```

## Layout

| Path | Role |
|---|---|
| `src/silex/runtime.py` | Job lifecycle |
| `src/silex/writ.py` | Capability tokens |
| `src/silex/ledger.py` | Append-only record |
| `src/silex/adapters.py` | Simulated cell |
| `src/silex/replay.py` | Controller log adapter |
| `PROTOCOL.md` | Adapter contract |
| `SECURITY.md` | Threat model |
