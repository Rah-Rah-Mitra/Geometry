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


def notebook_paths(all_notebooks: bool, smoke: bool, limit: int | None) -> list[Path]:
    paths = discover_canonical_notebooks(BOOK_ROOT)
    if smoke:
        paths = [path for path in paths if path.name in SMOKE_NAMES]
    if limit is not None:
        paths = paths[:limit]
    return paths


def execute_notebook(path: Path, timeout: int) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()
    nbformat.write(nb, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    paths = notebook_paths(args.all, args.smoke, args.limit)
    if not paths:
        raise SystemExit("no notebooks found")
    failures: list[tuple[Path, str]] = []
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
