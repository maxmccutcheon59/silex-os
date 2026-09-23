# Silex

Authorized work operating system.

Nothing consequential moves unless this kernel issued a writ and recorded the result. Models may propose work. They cannot execute it.

The product is the protocol in [PROTOCOL.md](PROTOCOL.md). This repo is the reference kernel.

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
silex replay
silex replay src/silex/fixtures/kitting_fail.jsonl
silex serve --port 8080
```

## Kernel laws

- No action without a live writ for `(actor, action, resource)`.
- Failed or denied steps roll the graph back.
- Jobs do not close incomplete.
- The ledger verifies or it is not evidence.

Company: [COMPANY.md](COMPANY.md). Doctrine: [DOCTRINE.md](DOCTRINE.md).
