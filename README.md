# Silex OS

Working name for the **action operating system**: software that is allowed to finish work.

> Nothing consequential moves unless this kernel issued it and this kernel logged what the world did.

This is not a chatbot. Not a humanoid. Not a foundation-model lab.
Models propose. Robots and tools execute. **This repo is the brainstem.**

## The four objects

| Object | Job |
|---|---|
| **Graph** | Live typed state of the operation |
| **Writ** | Scoped permission to act |
| **Runtime** | Durable job that survives failure |
| **Ledger** | Signed record of what happened |

First loop (v0): `release → confirm → execute step list → quality → close or halt`.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m silex.demo
pytest -q
```

## Doctrine

See [DOCTRINE.md](DOCTRINE.md). Quality bar: short speech, no slop, never close a job you did not finish.

## Name

`silex-os` is the **repo**. Public flagship name is still open on purpose. Do not ship a colliding brand (Lux, Veyra, Iron, Aevum, Keystone, Median are taken).
