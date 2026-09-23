# Silex

Authorization, execution, and audit kernel for mixed robot and agent fleets.

A job is an ordered list of steps. A writ is a capability for `(actor, action, resource)`. The runtime runs the next step only when a live writ allows it. Failed or denied steps restore prior world state. The ledger is hash-chained.

Silex is not a safety-certified motion controller. OEM safety systems remain in the loop. See [LEGAL.md](LEGAL.md).

**Brief:** [docs/index.html](docs/index.html) (GitHub Pages: Settings → Pages → Deploy from branch `main` / folder `/docs`).

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

## Present

| Asset | Use |
|---|---|
| [docs/index.html](docs/index.html) | One-page brief |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Control flow |
| [PROTOCOL.md](PROTOCOL.md) | Adapter contract |
| `silex demo` / `silex serve` | Live walkthrough |

## Layout

| Path | Role |
|---|---|
| `src/silex/runtime.py` | Job lifecycle |
| `src/silex/writ.py` | Capability tokens |
| `src/silex/ledger.py` | Append-only record |
| `src/silex/replay.py` | Controller-log adapter |
| `SECURITY.md` | Threat model |
