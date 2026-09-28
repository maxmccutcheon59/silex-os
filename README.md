# Silex

[![CI](https://github.com/maxmccutcheon59/silex-os/actions/workflows/test.yml/badge.svg)](https://github.com/maxmccutcheon59/silex-os/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Authorization, execution, and audit kernel for mixed robot and agent fleets.

A job is an ordered list of steps. A writ is a capability for `(actor, action, resource)`. The runtime runs the next step only when a live writ allows it. Failed or denied steps restore prior world state. The ledger is hash-chained.

Silex is not a safety-certified motion controller. OEM safety systems remain in the loop. See [LEGAL.md](LEGAL.md).

Project brief: [maxmccutcheon59.github.io/silex-os](https://maxmccutcheon59.github.io/silex-os/) (source: [docs/index.html](docs/index.html))

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

## Docs

| Asset | Use |
|---|---|
| [docs/index.html](docs/index.html) | One-page brief |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Control flow |
| [PROTOCOL.md](PROTOCOL.md) | Adapter contract |
| `silex demo` / `silex serve` | Live walkthrough |

## License

MIT © Max McCutcheon. See [LICENSE](LICENSE).
