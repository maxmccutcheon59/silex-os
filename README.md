# Silex

The operating system hardware companies have to call before a robot — or an agent — is allowed to act.

Windows sold software to PC makers. Silex sells authorization, completion, and proof. Models and agents propose. This kernel decides.

Protocol: [PROTOCOL.md](PROTOCOL.md). Company: [COMPANY.md](COMPANY.md). Legal: [LEGAL.md](LEGAL.md). Security: [SECURITY.md](SECURITY.md).

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
silex agent "kit order-1"
silex serve --port 8080
```

This software is proprietary, unwarranted, and not a safety-certified controller. See LEGAL.md.
