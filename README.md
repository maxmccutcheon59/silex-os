# Silex

Authorization, execution, and audit kernel for mixed robot and agent fleets.

A job is an ordered list of steps. A writ is a capability for `(actor, action, resource)`. The runtime runs the next step only when a live writ allows it. Failed or denied steps restore prior world state. The ledger is hash-chained.

Silex is not a safety-certified motion controller. OEM safety systems remain in the loop. See [LEGAL.md](LEGAL.md).

Brief: [docs/index.html](docs/index.html) · after Pages is enabled: https://maxmccutcheon59.github.io/silex-os/

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

```bash
silex version
silex demo
silex replay
silex serve --host 127.0.0.1 --port 8080
```

## Present

| Asset | Use |
|---|---|
| [docs/index.html](docs/index.html) | One-page brief |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Control flow |
| [PROTOCOL.md](PROTOCOL.md) | Adapter contract |
| `silex demo` / `silex serve` | Live walkthrough |
