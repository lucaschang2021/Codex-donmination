"""Thin CLI adapter. Business and governance rules live outside transport."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mobius.bootstrap import build_container


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mobius")
    sub = parser.add_subparsers(dest="command", required=True)
    gate = sub.add_parser("gate", help="evaluate a repository against an Architecture Contract")
    gate.add_argument("root", type=Path)
    gate.add_argument("--contract", type=Path, default=Path("ARCHITECTURE.toml"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command != "gate":
        return 2

    container = build_container()
    contract = container.contract_loader.load(args.contract)
    report = container.architecture_gate.evaluate(root=args.root, contract=contract)
    payload = {
        "status": report.status.value,
        "findings": [
            {
                "rule_id": finding.rule_id,
                "severity": finding.severity.value,
                "path": finding.path,
                "evidence": finding.evidence,
                "remediation": finding.remediation,
            }
            for finding in report.findings
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if report.status.value == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
