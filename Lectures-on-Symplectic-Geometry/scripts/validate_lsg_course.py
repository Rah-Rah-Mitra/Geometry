"""Execute LSG notebooks with nbclient."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

BOOK_ROOT = Path(__file__).resolve().parents[1]

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def notebook_paths(all_notebooks: bool, limit: int | None) -> list[Path]:
    artifact_root = BOOK_ROOT / "artifacts"
    paths = [path for path in sorted(BOOK_ROOT.rglob("*.ipynb")) if artifact_root not in path.parents]
    if not all_notebooks:
        smoke_names = {
            "00-book-index.ipynb",
            "01-symplectic-forms.ipynb",
            "08-darboux-moser-weinstein-theory.ipynb",
            "18-hamiltonian-vector-fields.ipynb",
            "22-hamiltonian-actions.ipynb",
            "28-classification-of-symplectic-toric-manifolds.ipynb",
        }
        paths = [path for path in paths if path.name in smoke_names]
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
            print(f"FAILED {path.relative_to(BOOK_ROOT)}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(paths)} notebooks successfully")


if __name__ == "__main__":
    main()
