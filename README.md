# Silex OS

Authorized work operating system. Software that is allowed to finish work.

> Nothing consequential moves unless this kernel issued a writ and this kernel logged what the world did.

Not a chatbot. The console is an operator board. An LLM may **propose** a step list. It cannot execute.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
silex demo
silex serve --port 8080
```

Open http://127.0.0.1:8080

Optional proposer (still cannot skip writs):

```bash
export SILEX_LLM_URL=https://api.x.ai/v1/chat/completions
export SILEX_LLM_KEY=...
export SILEX_LLM_MODEL=grok-4
silex serve
```

If those are unset, the planner is a local rule engine.

## Objects

| Object | Job |
|---|---|
| Actor | Signed identity |
| Graph | Live state |
| Writ | Capability token |
| Runtime | Finish or halt |
| Ledger | Hash-chained proof |
| Adapter | Simulated or real controller |
| Planner | Propose only |

See [COMPANY.md](COMPANY.md) and [DOCTRINE.md](DOCTRINE.md).
