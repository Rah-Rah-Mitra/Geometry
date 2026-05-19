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

from utils.validation import canonical_notebooks, index_notebooks, relative  # noqa: E402

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def selected(all_notebooks: bool, limit: int | None) -> list[Path]:
    if all_notebooks:
        paths = [*index_notebooks(BOOK_ROOT), *canonical_notebooks(BOOK_ROOT)]
    else:
        paths = [BOOK_ROOT / "00-book-index.ipynb", *canonical_notebooks(BOOK_ROOT)]
    return paths[:limit] if limit is not None else paths


def execute(path: Path, timeout: int) -> None:
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
    parser.add_argument("--limit", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    limit = None if args.all and args.limit == 4 else args.limit
    failures: list[tuple[Path, str]] = []
    paths = selected(args.all, limit)
    for index, path in enumerate(paths, 1):
        print(f"[{index}/{len(paths)}] {relative(path)}")
        try:
            execute(path, args.timeout)
        except Exception as exc:
            failures.append((path, repr(exc)))
    if failures:
        for path, error in failures:
            print(f"FAILED {path}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(paths)} notebooks successfully")


if __name__ == "__main__":
    main()
