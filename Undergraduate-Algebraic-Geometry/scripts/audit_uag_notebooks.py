"""Audit UAG canonical notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import nbformat

import uag_inventory as inventory


BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-book-index.ipynb", "00-index.ipynb"}


def canonical_notebooks() -> list[Path]:
    return inventory.canonical_notebooks(BOOK_ROOT)


def notebook_stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "markdown")
    code = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "code")
    words = re.findall(r"[A-Za-z][A-Za-z0-9'-]*", markdown)
    return {
        "path": path,
        "words": len(words),
        "code_cells": sum(1 for cell in nb.cells if cell.cell_type == "code"),
        "display_artifact": code.count("display_artifact("),
        "has_setup": "BOOK_ROOT" in code and "ARTIFACT_ROOT" in code,
        "has_takeaways": "Takeaways" in markdown,
        "has_sanity": "validate_chapter_outputs" in code and "final-sanity.json" in code,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()
    failures: list[str] = []
    chapter_dirs = [BOOK_ROOT / str(entry["folder"]) for entry in inventory.ENTRIES]
    for folder in chapter_dirs:
        notebooks = [p for p in folder.glob("*.ipynb") if p.name not in IGNORED]
        if len(notebooks) != 1:
            failures.append(f"{folder.relative_to(BOOK_ROOT)} has {len(notebooks)} canonical notebooks")
    for path in canonical_notebooks():
        if not path.exists():
            failures.append(f"missing notebook {path.relative_to(BOOK_ROOT)}")
            continue
        stats = notebook_stats(path)
        if int(stats["words"]) < args.min_words:
            failures.append(f"{path.relative_to(BOOK_ROOT)} has only {stats['words']} words")
        if int(stats["code_cells"]) < args.min_code_cells:
            failures.append(f"{path.relative_to(BOOK_ROOT)} has only {stats['code_cells']} code cells")
        if not stats["has_setup"]:
            failures.append(f"{path.relative_to(BOOK_ROOT)} is missing BOOK_ROOT/ARTIFACT_ROOT setup")
        if not stats["has_takeaways"]:
            failures.append(f"{path.relative_to(BOOK_ROOT)} is missing takeaways")
        if not stats["has_sanity"]:
            failures.append(f"{path.relative_to(BOOK_ROOT)} is missing final sanity validation")
        if int(stats["display_artifact"]) < 3:
            failures.append(f"{path.relative_to(BOOK_ROOT)} displays too few artifacts")
    print(f"Audited {len(canonical_notebooks())} canonical notebooks.")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print("All canonical notebooks meet the configured structure and depth thresholds.")


if __name__ == "__main__":
    main()
