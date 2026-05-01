"""Execute GMAM notebooks with nbclient."""

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


SMOKE_NAMES = {
    "00-book-index.ipynb",
    "01-preliminary-notions.ipynb",
    "02-incidence-and-metric-geometry.ipynb",
    "05-angle-measure.ipynb",
    "08-hyperbolic-geometry.ipynb",
    "10-area.ipynb",
    "11-the-theory-of-isometries.ipynb",
}


def paths(smoke: bool, all_notebooks: bool, limit: int | None) -> list[Path]:
    candidates = [BOOK_ROOT / "00-book-index.ipynb", *canonical_notebooks(BOOK_ROOT)]
    if all_notebooks:
        candidates = [*index_notebooks(BOOK_ROOT), *canonical_notebooks(BOOK_ROOT)]
    elif smoke:
        candidates = [path for path in candidates if path.name in SMOKE_NAMES]
    if limit is not None:
        candidates = candidates[:limit]
    return candidates


def execute(path: Path, timeout: int) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
    client.execute()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    failures: list[tuple[Path, str]] = []
    selected = paths(args.smoke, args.all, args.limit)
    if not selected:
        raise SystemExit("no notebooks selected")
    for index, path in enumerate(selected, start=1):
        print(f"[{index}/{len(selected)}] {relative(path)}")
        try:
            execute(path, args.timeout)
        except Exception as exc:  # noqa: BLE001
            failures.append((path, repr(exc)))
    if failures:
        for path, error in failures:
            print(f"FAILED {path}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(selected)} notebooks successfully")


if __name__ == "__main__":
    main()
