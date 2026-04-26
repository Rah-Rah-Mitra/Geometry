"""Validate generated notebooks by executing them with nbclient."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOK_ROOT = REPO_ROOT / "Geometric-Algebra-for-Computer-Science"

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def notebook_paths(all_notebooks: bool, limit: int | None) -> list[Path]:
    artifact_root = BOOK_ROOT / "artifacts"
    paths = [
        path
        for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
        if artifact_root not in path.parents
    ]
    generated = [
        path
        for path in paths
        if path.name not in {"legacy-seed-why-geometric-algebra.ipynb"}
    ]
    if not all_notebooks:
        smoke_names = {
            "00-book-index.ipynb",
            "02-spanning-oriented-subspaces.ipynb",
            "11-the-homogeneous-model.ipynb",
            "13-conformal-model-operational-euclidean-geometry.ipynb",
            "19-basis-blades-and-operations.ipynb",
            "23-ray-tracing-with-conformal-geometry.ipynb",
            "appendix-a-metrics-and-null-vectors.ipynb",
            "appendix-d-common-equations.ipynb",
        }
        generated = [path for path in generated if path.name in smoke_names]
    if limit is not None:
        generated = generated[:limit]
    return generated


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
    parser.add_argument("--all", action="store_true", help="execute every generated notebook")
    parser.add_argument("--limit", type=int, default=None, help="limit the number of notebooks")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    failures: list[tuple[Path, str]] = []
    paths = notebook_paths(args.all, args.limit)
    if not paths:
        raise SystemExit("no notebooks found to validate")
    for index, path in enumerate(paths, start=1):
        print(f"[{index}/{len(paths)}] {path.relative_to(REPO_ROOT)}")
        try:
            execute_notebook(path, args.timeout)
        except Exception as exc:  # noqa: BLE001
            failures.append((path, repr(exc)))

    if failures:
        for path, error in failures:
            print(f"FAILED {path}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(paths)} notebooks successfully")


if __name__ == "__main__":
    main()
