from __future__ import annotations

import argparse
from pathlib import Path

from silex.demo import run_demo
from silex.run_replay import FIXTURES, run_file
from silex.server import serve


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="silex", description="Silex authorized work OS")
    sub = parser.add_subparsers(dest="cmd", required=True)
    demo = sub.add_parser("demo", help="run the simulated kitting cell")
    demo.add_argument("--fail-quality", action="store_true")
    replay = sub.add_parser("replay", help="authorize and replay a controller log")
    replay.add_argument("path", nargs="?", default=str(FIXTURES / "kitting_ok.jsonl"))
    web = sub.add_parser("serve", help="operator console")
    web.add_argument("--host", default="127.0.0.1")
    web.add_argument("--port", type=int, default=8080)
    args = parser.parse_args(argv)
    if args.cmd == "demo":
        run_demo(fail_quality=args.fail_quality)
        return 0
    if args.cmd == "replay":
        status = run_file(Path(args.path))
        return 0 if status.value == "closed" else 2
    if args.cmd == "serve":
        serve(args.host, args.port)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
