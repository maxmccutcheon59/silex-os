# Silex

Authorized work operating system. Nothing consequential moves unless this kernel issued a writ and recorded the result.

This repository is the control plane: identity, permission, execution, proof. Models may propose work. They cannot execute it.

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
silex serve --port 8080
```

Console: http://127.0.0.1:8080

Optional proposer (still cannot skip writs):

```bash
export SILEX_LLM_URL=https://api.x.ai/v1/chat/completions
export SILEX_LLM_KEY=...
export SILEX_LLM_MODEL=grok-4
```

## Architecture

| Component | Responsibility |
|---|---|
| Actor | Who is acting |
| Graph | What is true now |
| Writ | What that actor may do |
| Runtime | Advance a job or halt |
| Ledger | Hash-chained record |
| Adapter | Talk to a cell without owning it |
| Planner | Propose steps only |

Wedge: high-mix kitting cell (`release → confirm → pick → place → quality → close`).

Company rules: [COMPANY.md](COMPANY.md). Kernel laws: [DOCTRINE.md](DOCTRINE.md).
