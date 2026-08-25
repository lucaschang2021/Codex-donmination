from __future__ import annotations

import argparse
import json
import sys

from .discovery import ThreadDiscoveryService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codex-domination")
    subparsers = parser.add_subparsers(dest="command", required=True)

    threads = subparsers.add_parser("threads", help="List persistent Codex threads")
    threads.add_argument("--limit", type=int, default=None)
    threads.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command != "threads":
        return 2

    try:
        threads = ThreadDiscoveryService().list_threads(limit=args.limit)
    except Exception as exc:  # boundary: convert SDK/runtime failures into CLI failure
        print(f"codex-domination: failed to discover Codex threads: {exc}", file=sys.stderr)
        return 1

    if args.as_json:
        print(
            json.dumps(
                [
                    {
                        "id": thread.thread_id,
                        "name": thread.name,
                        "cwd": thread.cwd,
                        "preview": thread.preview,
                        "updatedAt": thread.updated_at,
                    }
                    for thread in threads
                ],
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if not threads:
        print("No persistent Codex threads found.")
        return 0

    for thread in threads:
        label = thread.name or thread.preview or "(unnamed)"
        cwd = f"  [{thread.cwd}]" if thread.cwd else ""
        print(f"{thread.thread_id}  {label}{cwd}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
