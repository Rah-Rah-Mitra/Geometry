"""Execute symplectic topology notebooks with nbclient."""

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

from utils.course_data import COURSE_UNITS

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


SMOKE_SLUGS = {
    "introduction",
    "chapter-01-from-classical-to-modern",
    "chapter-05-symplectic-group-actions",
    "chapter-06-symplectic-fibrations",
    "chapter-12-symplectic-capacities",
    "appendix-a-smooth-maps",
}


def notebook_paths(all_notebooks: bool, limit: int | None) -> list[Path]:
    if all_notebooks:
        paths = [BOOK_ROOT / "00-book-index.ipynb"]
        paths.extend(BOOK_ROOT / unit.notebook_relpath for unit in COURSE_UNITS)
    else:
        paths = [BOOK_ROOT / "00-book-index.ipynb"]
        paths.extend(BOOK_ROOT / unit.notebook_relpath for unit in COURSE_UNITS if unit.slug in SMOKE_SLUGS)
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
    args = parser.parse_args()

    paths = notebook_paths(args.all, args.limit)
    failures: list[tuple[Path, str]] = []
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
    print(f"Executed {len(paths)} notebooks successfully")


if __name__ == "__main__":
    main()
