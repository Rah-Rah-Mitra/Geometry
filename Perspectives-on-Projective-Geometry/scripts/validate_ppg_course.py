from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

import ppg_inventory as inv

BOOK_ROOT = Path(__file__).resolve().parents[1]

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def selected_notebooks(args: argparse.Namespace) -> list[Path]:
    if args.chapter:
        chapters = [inv.chapter_by_number(number) for number in args.chapter]
    elif args.smoke:
        chapters = [inv.chapter_by_number(number) for number in inv.SMOKE_CHAPTERS]
    else:
        chapters = list(inv.CHAPTERS)
    paths = [inv.canonical_notebook_path(chapter) for chapter in chapters]
    if args.limit is not None:
        paths = paths[: args.limit]
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="execute all notebooks")
    parser.add_argument("--smoke", action="store_true", help="execute representative notebooks")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--chapter", type=int, action="append")
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    if args.all:
        args.smoke = False
        args.limit = None
    paths = selected_notebooks(args)
    for index, path in enumerate(paths, start=1):
        print(f"[{index}/{len(paths)}] {path.relative_to(BOOK_ROOT)}")
        nb = nbformat.read(path, as_version=4)
        NotebookClient(
            nb,
            timeout=args.timeout,
            kernel_name="python3",
            resources={"metadata": {"path": str(path.parent)}},
        ).execute()
    print(f"Executed {len(paths)} notebooks successfully.")


if __name__ == "__main__":
    main()

