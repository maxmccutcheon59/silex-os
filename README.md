# Silex

Authorized work operating system. Nothing consequential moves unless this kernel issued a writ and recorded the result.

Models may propose work. They cannot execute it.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

## Commands

```bash
silex demo
silex demo --fail-quality
silex replay
silex replay src/silex/fixtures/kitting_fail.jsonl
silex serve --port 8080
```

`replay` runs a recorded controller log through the same writ + ledger path as a live cell. That is how a plant demo starts without buying hardware.

## Architecture

| Component | Responsibility |
|---|---|
| Actor | Who is acting |
| Graph | What is true now |
| Writ | What that actor may do |
| Policy | Which actions exist for a wedge |
| Runtime | Advance a job or halt |
| Ledger | Hash-chained record |
| Adapter | Simulated cell or controller log |
| Planner | Propose steps only |

Company rules: [COMPANY.md](COMPANY.md). Kernel laws: [DOCTRINE.md](DOCTRINE.md).
