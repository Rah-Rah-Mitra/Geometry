"""Execute Methods of Information Geometry notebooks with nbclient."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

import mig_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def expected_paths() -> list[Path]:
    return [BOOK_ROOT / entry["folder"] / entry["notebook"] for entry in inventory.ENTRIES]


def notebook_paths(all_notebooks: bool, include_indexes: bool, limit: int | None) -> list[Path]:
    if all_notebooks:
        artifact_root = BOOK_ROOT / "artifacts"
        paths = [path for path in sorted(BOOK_ROOT.rglob("*.ipynb")) if artifact_root not in path.parents]
    else:
        paths = [path for path in expected_paths() if path.exists()]
        if include_indexes and (BOOK_ROOT / "00-book-index.ipynb").exists():
            paths = [BOOK_ROOT / "00-book-index.ipynb", *paths]
    if limit is not None:
        paths = paths[:limit]
    return paths


def execute_notebook(path: Path, timeout: int) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
    client.execute()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--include-indexes", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    paths = notebook_paths(args.all, args.include_indexes, args.limit)
    if not paths:
        raise SystemExit("no notebooks found")
    failures = []
    for index, path in enumerate(paths, start=1):
        print(f"[{index}/{len(paths)}] {path.relative_to(BOOK_ROOT)}")
        try:
            execute_notebook(path, args.timeout)
        except Exception as exc:
            failures.append((path, repr(exc)))
    if failures:
        for path, error in failures:
            print(f"FAILED {path}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(paths)} notebooks successfully")


if __name__ == "__main__":
    main()

