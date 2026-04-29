"""Execute UAG canonical notebooks with nbclient."""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient

import uag_inventory as inventory


BOOK_ROOT = Path(__file__).resolve().parents[1]


def notebook_paths(all_notebooks: bool, limit: int | None) -> list[Path]:
    paths = inventory.canonical_notebooks(BOOK_ROOT)
    if all_notebooks:
        return paths
    return paths[: limit or len(paths)]


def execute_notebook(path: Path, timeout: int) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    paths = notebook_paths(args.all, args.limit)
    for index, path in enumerate(paths, start=1):
        print(f"[{index}/{len(paths)}] {path.relative_to(BOOK_ROOT)}")
        execute_notebook(path, args.timeout)
    print(f"Executed {len(paths)} notebooks successfully.")


if __name__ == "__main__":
    main()
