"""Command-line interface for validation, execution and synthetic demonstrations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from laborix.ledger import Ledger
from laborix.plan import plan_from_json, topological_order


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="laborix")
    sub = p.add_subparsers(dest="command", required=True)
    for name in (
        "validate",
        "plan",
        "run",
        "resume",
        "schedule",
        "ablate",
        "ledger",
        "verify",
        "report",
        "demo",
    ):
        q = sub.add_parser(name)
        q.add_argument("path", nargs="?")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command in {"validate", "plan"}:
        plan = plan_from_json(Path(args.path).read_text())
        print("valid" if args.command == "validate" else " ".join(topological_order(plan)))
        return 0
    if args.command == "verify":
        ok, message = Ledger(Path(args.path)).verify()
        print(message)
        return 0 if ok else 2
    if args.command == "demo":
        from laborix.demo import run_demo

        print(json.dumps(run_demo(Path(args.path or "laborix-demo")), sort_keys=True))
        return 0
    print(f"{args.command}: provide command-specific input", flush=True)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
