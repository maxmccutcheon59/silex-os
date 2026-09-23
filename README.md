# Silex OS

Authorized work operating system. Software that is allowed to finish work.

> Nothing consequential moves unless this kernel issued a writ and this kernel logged what the world did.

Not a chatbot. Not a humanoid. Not a model lab. Models propose. Cells execute. **This repo is the control plane.**

Private company kernel. Public brand name is still open.

## Objects

| Object | Job |
|---|---|
| **Actor** | Robot, AMR, cell, human, policy — signed identity |
| **Graph** | Live typed state of the operation |
| **Writ** | Capability token: who may do which action on which resource, until when |
| **Runtime** | Durable job. Finish or halt. Never close incomplete work. |
| **Ledger** | Hash-chained record of every grant, deny, step, halt |
| **Adapter** | Thin driver to a simulated or real controller. Kernel does not own metal. |

First wedge: **high-mix kitting cell** — release → confirm parts/cell → pick → place → quality → close.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
silex demo
silex demo --fail-quality
pytest -q
```

## Company

See [COMPANY.md](COMPANY.md) and [DOCTRINE.md](DOCTRINE.md).
