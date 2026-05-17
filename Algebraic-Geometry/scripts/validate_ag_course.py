"""Execute Hartshorne Algebraic Geometry notebooks with nbclient."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

import ag_inventory as inventory


BOOK_ROOT = Path(__file__).resolve().parents[1]

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def notebook_paths(all_notebooks: bool, limit: int | None, include_indexes: bool) -> list[Path]:
    paths = inventory.canonical_notebooks(BOOK_ROOT)
    if include_indexes:
        index_paths = [BOOK_ROOT / "00-book-index.ipynb"]
        index_paths.extend(BOOK_ROOT / str(entry["folder"]) / "00-index.ipynb" for entry in inventory.ENTRIES)
        paths = index_paths + paths
    if all_notebooks:
        return paths
    return paths[: limit or len(paths)]


def execute_notebook(path: Path, timeout: int, write_executed: bool) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()
    if write_executed:
        nbformat.write(nb, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--include-indexes", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--write-executed", action="store_true")
    args = parser.parse_args()

    paths = notebook_paths(args.all, args.limit, args.include_indexes)
    executed: list[str] = []
    for index, path in enumerate(paths, start=1):
        rel = str(path.relative_to(BOOK_ROOT)).replace("\\", "/")
        print(f"[{index}/{len(paths)}] {rel}")
        execute_notebook(path, args.timeout, args.write_executed)
        executed.append(rel)
    print(json.dumps({"executed": len(executed), "notebooks": executed}, indent=2))


if __name__ == "__main__":
    main()
