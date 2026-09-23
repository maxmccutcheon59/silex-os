from __future__ import annotations

import argparse

from silex.demo import run_demo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="silex", description="Silex authorized work OS")
    sub = parser.add_subparsers(dest="cmd", required=True)
    demo = sub.add_parser("demo", help="run the high-mix kitting cell simulation")
    demo.add_argument("--fail-quality", action="store_true", help="force quality halt")
    args = parser.parse_args(argv)
    if args.cmd == "demo":
        run_demo(fail_quality=args.fail_quality)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
