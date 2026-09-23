from __future__ import annotations

import argparse

from silex.demo import run_demo
from silex.server import serve


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="silex", description="Silex authorized work OS")
    sub = parser.add_subparsers(dest="cmd", required=True)
    demo = sub.add_parser("demo", help="run the high-mix kitting cell simulation")
    demo.add_argument("--fail-quality", action="store_true")
    web = sub.add_parser("serve", help="operator console")
    web.add_argument("--host", default="127.0.0.1")
    web.add_argument("--port", type=int, default=8080)
    args = parser.parse_args(argv)
    if args.cmd == "demo":
        run_demo(fail_quality=args.fail_quality)
        return 0
    if args.cmd == "serve":
        serve(args.host, args.port)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
