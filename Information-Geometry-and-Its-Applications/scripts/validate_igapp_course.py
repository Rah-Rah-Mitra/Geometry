"""Execute Information Geometry notebooks with nbclient."""

from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

import igapp_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def expected_paths() -> list[Path]:
    return [BOOK_ROOT / entry["part"] / entry["folder"] / entry["notebook"] for entry in inventory.ENTRIES]


def strip_trailing_whitespace(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    cleaned = "\n".join(line.rstrip() for line in text.splitlines())
    if text:
        cleaned += "\n"
    if cleaned != text:
        for attempt in range(3):
            try:
                path.write_text(cleaned, encoding="utf-8")
                break
            except OSError:
                if attempt == 2:
                    return
                time.sleep(0.2)


def clean_html_artifacts() -> None:
    if not ARTIFACT_ROOT.exists():
        return
    for path in ARTIFACT_ROOT.rglob("*.html"):
        strip_trailing_whitespace(path)


def notebook_paths(all_notebooks: bool, limit: int | None, include_indexes: bool) -> list[Path]:
    artifact_root = BOOK_ROOT / "artifacts"
    if all_notebooks:
        paths = [path for path in sorted(BOOK_ROOT.rglob("*.ipynb")) if artifact_root not in path.parents]
    else:
        smoke_names = {
            "00-book-index.ipynb",
            "01-manifold-divergence-dually-flat-structure.ipynb",
            "03-invariant-geometry-of-probability-distributions.ipynb",
            "06-dual-affine-connections-dually-flat-manifold.ipynb",
            "08-hidden-variables-and-em.ipynb",
            "11-machine-learning.ipynb",
            "12-natural-gradient-and-singular-learning.ipynb",
            "13-signal-processing-and-optimization.ipynb",
        }
        paths = [path for path in expected_paths() if path.exists() and path.name in smoke_names]
        if include_indexes and (BOOK_ROOT / "00-book-index.ipynb").exists():
            paths.insert(0, BOOK_ROOT / "00-book-index.ipynb")
    if limit is not None:
        paths = paths[:limit]
    return paths


def execute_notebook(path: Path, timeout: int) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3", shutdown_kernel="immediate", resources={"metadata": {"path": str(path.parent)}})
    try:
        client.execute()
    finally:
        if getattr(client, "km", None) is not None:
            client._cleanup_kernel()
    clean_html_artifacts()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--include-indexes", action="store_true")
    parser.add_argument("--allow-empty", action="store_true")
    args = parser.parse_args()

    paths = notebook_paths(args.all, args.limit, args.include_indexes)
    if not paths:
        if args.allow_empty:
            print("No authored notebooks found; validation skipped.")
            return
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
