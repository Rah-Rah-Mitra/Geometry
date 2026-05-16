"""Audit canonical notebooks for source grounding, structure, and visual links."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import nbformat

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))

from utils.course_manifest import CHAPTERS


def cell_source(cell: object) -> str:
    return "".join(cell.get("source", ""))


def stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = [cell_source(cell) for cell in nb.cells if cell.cell_type == "markdown"]
    code = [cell_source(cell) for cell in nb.cells if cell.cell_type == "code"]
    joined = "\n".join(markdown + code)
    return {
        "path": str(path.relative_to(BOOK_ROOT)),
        "markdown_words": sum(len(text.split()) for text in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "display_artifact_calls": joined.count("display_artifact("),
        "has_source_span": "Source span" in joined,
        "has_translation_guide": "Translation guide" in joined,
        "has_final_sanity": "final_sanity" in joined,
        "has_book_root": "BOOK_ROOT" in joined,
        "mentions_originality": "original" in joined.lower() or "no copied" in joined.lower(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=550)
    parser.add_argument("--min-code-cells", type=int, default=4)
    args = parser.parse_args()

    records = []
    missing = []
    for chapter in CHAPTERS:
        if not chapter.path.exists():
            missing.append(str(chapter.path.relative_to(BOOK_ROOT)))
            continue
        records.append(stats(chapter.path))
    failing = [
        item
        for item in records
        if item["markdown_words"] < args.min_words
        or item["code_cells"] < args.min_code_cells
        or item["display_artifact_calls"] < 2
        or not item["has_source_span"]
        or not item["has_translation_guide"]
        or not item["has_final_sanity"]
        or not item["has_book_root"]
    ]
    report = {"notebook_count": len(records), "missing": missing, "failing": failing, "stats": records}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(records)} canonical notebooks")
    if missing:
        print("Missing notebooks:")
        for path in missing:
            print(f"- {path}")
    if failing:
        print("Notebook findings:")
        for item in failing:
            print(
                f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells, "
                f"{item['display_artifact_calls']} display calls"
            )
    if missing or failing:
        raise SystemExit(1)
    print("All canonical notebooks meet source, structure, and visual-link checks.")


if __name__ == "__main__":
    main()
