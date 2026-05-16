"""Execute Convex Analysis notebooks with nbclient."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

BOOK_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = BOOK_ROOT.parent
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import canonical_notebooks, index_notebooks, relative  # noqa: E402

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

SMOKE_NAMES = {
    "00-book-index.ipynb",
    "01-affine-sets.ipynb",
    "04-convex-functions.ipynb",
    "11-separation-theorems.ipynb",
    "23-directional-derivatives-and-subgradients.ipynb",
    "28-ordinary-convex-programs-and-lagrange-multipliers.ipynb",
    "31-fenchels-duality-theorem.ipynb",
    "33-saddle-functions.ipynb",
    "39-convex-processes.ipynb",
}


def selected_paths(smoke: bool, all_notebooks: bool, limit: int | None) -> list[Path]:
    paths = [BOOK_ROOT / "00-book-index.ipynb", *canonical_notebooks(BOOK_ROOT)]
    if all_notebooks:
        paths = [*index_notebooks(BOOK_ROOT), *canonical_notebooks(BOOK_ROOT)]
    elif smoke:
        paths = [path for path in paths if path.name in SMOKE_NAMES]
    if limit is not None:
        paths = paths[:limit]
    return paths


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
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    paths = selected_paths(args.smoke, args.all, args.limit)
    if not paths:
        raise SystemExit("no notebooks selected")
    failures: list[tuple[Path, str]] = []
    for index, path in enumerate(paths, start=1):
        print(f"[{index}/{len(paths)}] {relative(path, WORKSPACE_ROOT)}")
        try:
            execute(path, args.timeout)
        except Exception as exc:  # noqa: BLE001
            failures.append((path, repr(exc)))
    if failures:
        for path, error in failures:
            print(f"FAILED {relative(path, WORKSPACE_ROOT)}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(paths)} notebooks successfully")


if __name__ == "__main__":
    main()

