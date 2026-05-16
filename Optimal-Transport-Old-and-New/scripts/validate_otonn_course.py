"""Execute Optimal Transport notebooks with nbclient."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))

from scripts import otonn_inventory as inventory

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def notebook_paths(all_notebooks: bool, limit: int | None, include_indexes: bool) -> list[Path]:
    if all_notebooks:
        paths = inventory.expected_notebooks(include_indexes=include_indexes)
    else:
        smoke = inventory.smoke_unit_ids()
        paths = [inventory.unit_path(unit) for unit in inventory.UNITS if unit["id"] in smoke]
        if include_indexes:
            paths.insert(0, BOOK_ROOT / "00-book-index.ipynb")
    paths = [path for path in paths if path.exists()]
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
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--include-indexes", action="store_true")
    args = parser.parse_args()

    paths = notebook_paths(args.all, args.limit, args.include_indexes)
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
            print(f"FAILED {path.relative_to(BOOK_ROOT)}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(paths)} notebooks successfully.")


if __name__ == "__main__":
    main()
