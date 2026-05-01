"""Execute MVG notebooks with nbclient."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

import mvg_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def entry_folder(entry: dict) -> Path:
    if entry["part"] is None:
        return BOOK_ROOT / entry["folder"]
    return BOOK_ROOT / entry["part"] / entry["folder"]


def notebook_paths(*, smoke: bool, all_notebooks: bool, limit: int | None) -> list[Path]:
    missing = []
    paths: list[Path] = []
    book_index = BOOK_ROOT / "00-book-index.ipynb"
    if book_index.exists():
        paths.append(book_index)
    else:
        missing.append(book_index)
    if all_notebooks:
        for part in inventory.PARTS:
            part_index = BOOK_ROOT / part["folder"] / "00-part-index.ipynb"
            if part_index.exists():
                paths.append(part_index)
            else:
                missing.append(part_index)
    for entry in inventory.ENTRIES:
        folder = entry_folder(entry)
        index = folder / "00-index.ipynb"
        canonical = folder / entry["notebook"]
        for path in [folder, index, canonical]:
            if not path.exists():
                missing.append(path)
        include = all_notebooks or (smoke and canonical.name in inventory.SMOKE_NOTEBOOKS) or (not smoke and not all_notebooks)
        if include:
            if all_notebooks and index.exists():
                paths.append(index)
            if canonical.exists():
                paths.append(canonical)
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))
    if limit is not None:
        paths = paths[:limit]
    return paths


def execute_notebook(path: Path, timeout: int) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
    client.execute()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    paths = notebook_paths(smoke=args.smoke, all_notebooks=args.all, limit=args.limit)
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
