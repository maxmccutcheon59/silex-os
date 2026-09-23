# Silex

The operating system hardware companies have to call before a robot is allowed to act.

Windows sold software to PC makers. Silex sells authorization, completion, and proof to anyone who moves metal — arms, AMRs, humanoids, cells. Models propose. This kernel decides.

The contract is [PROTOCOL.md](PROTOCOL.md). Positioning is [COMPANY.md](COMPANY.md).

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

```bash
silex demo
silex replay
silex serve --port 8080
```
