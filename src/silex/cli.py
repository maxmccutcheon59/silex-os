from __future__ import annotations

import argparse
from pathlib import Path

from silex import __version__
from silex.agent import main_text
from silex.demo import run_demo
from silex.export import write_ledger
from silex.run_replay import FIXTURES, build_replay
from silex.run_replay import run_file
from silex.runtime import Status
from silex.server import serve
from silex.policy import KITTING


def _export(path: str, out: str) -> int:
    runtime, issuer, actor, _adapter, ledger, _graph = build_replay(path)
    job = runtime.submit(f"export {path}", list(KITTING.actions))
    runtime.run(job, issuer.issue(actor.id, list(KITTING.actions), KITTING.resource))
    dest = write_ledger(ledger, out)
    print(f"wrote {dest} status={job.status.value} verified={ledger.verify()}")
    return 0 if job.status == Status.CLOSED else 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="silex",
        description="Silex — authorization and audit kernel for robots and agents",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("version", help="print version")

    demo = sub.add_parser("demo", help="run the simulated kitting cell")
    demo.add_argument("--fail-quality", action="store_true")

    replay = sub.add_parser("replay", help="authorize and replay a controller log")
    replay.add_argument("path", nargs="?", default=str(FIXTURES / "kitting_ok.jsonl"))

    agent = sub.add_parser("agent", help="propose steps, then run under a cell writ")
    agent.add_argument("text", nargs="?", default="kit order-1")

    export = sub.add_parser("export", help="replay a log and write the ledger as JSON")
    export.add_argument("path", nargs="?", default=str(FIXTURES / "kitting_ok.jsonl"))
    export.add_argument("--out", default="ledger.json")

    web = sub.add_parser("serve", help="local operator console")
    web.add_argument("--host", default="127.0.0.1")
    web.add_argument("--port", type=int, default=8080)

    args = parser.parse_args(argv)
    if args.cmd == "version":
        print(__version__)
        return 0
    if args.cmd == "demo":
        run_demo(fail_quality=args.fail_quality)
        return 0
    if args.cmd == "replay":
        status = run_file(Path(args.path))
        return 0 if status.value == "closed" else 2
    if args.cmd == "agent":
        return main_text(args.text)
    if args.cmd == "export":
        return _export(args.path, args.out)
    if args.cmd == "serve":
        serve(args.host, args.port)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
