"""Execute JHCST notebooks with nbclient."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import discover_canonical_notebooks  # noqa: E402

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

SMOKE_NAMES = {
    "01-introduction.ipynb",
    "02-j-holomorphic-curves.ipynb",
    "04-compactness.ipynb",
    "07-gromov-witten-invariants.ipynb",
    "10-gluing.ipynb",
    "11-quantum-cohomology.ipynb",
    "e-singularities-and-intersections.ipynb",
}
INDEX_NAMES = {"00-index.ipynb", "00-book-index.ipynb"}


def notebook_paths(all_notebooks: bool, smoke: bool, include_indexes: bool, limit: int | None) -> list[Path]:
    paths = discover_canonical_notebooks(BOOK_ROOT)
    if include_indexes:
        index_paths = [
            path
            for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
            if path.name in INDEX_NAMES and BOOK_ROOT / "artifacts" not in path.parents
        ]
        paths = index_paths + paths
    if smoke:
        paths = [path for path in paths if path.name in SMOKE_NAMES]
    if limit is not None:
        paths = paths[:limit]
    return paths


def execute_notebook(path: Path, timeout: int, write_executed: bool = False) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        shutdown_kernel="immediate",
        resources={"metadata": {"path": str(path.parent)}},
    )
    try:
        client.execute()
    finally:
        if getattr(client, "km", None) is not None:
            client._cleanup_kernel()
    if write_executed:
        nbformat.write(nb, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--include-indexes", action="store_true")
    parser.add_argument("--write-executed", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    paths = notebook_paths(args.all, args.smoke, args.include_indexes, args.limit)
    if not paths:
        raise SystemExit("no notebooks found")
    failures: list[tuple[Path, str]] = []
    for index, path in enumerate(paths, start=1):
        print(f"[{index}/{len(paths)}] {path.relative_to(BOOK_ROOT)}")
        try:
            execute_notebook(path, args.timeout, write_executed=args.write_executed)
        except Exception as exc:
            failures.append((path, repr(exc)))
    if failures:
        for path, error in failures:
            print(f"FAILED {path}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(paths)} notebooks successfully")


if __name__ == "__main__":
    main()
