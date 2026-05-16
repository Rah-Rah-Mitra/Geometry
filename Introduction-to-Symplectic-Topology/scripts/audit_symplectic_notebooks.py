"""Audit canonical notebooks for standalone depth and source-map coverage."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import nbformat

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.course_data import COURSE_UNITS


def notebook_stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    text = "\n".join(markdown + code)
    return {
        "path": str(path.relative_to(BOOK_ROOT)),
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "has_source_span": "printed pages" in text and "PDF pages" in text,
        "has_visual_call": "build_unit_artifacts" in text or "display_artifact" in text,
        "has_final_sanity": "final-sanity.json" in text,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=650)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()

    expected = [BOOK_ROOT / unit.notebook_relpath for unit in COURSE_UNITS]
    missing = [str(path.relative_to(BOOK_ROOT)) for path in expected if not path.exists()]
    stats = [notebook_stats(path) for path in expected if path.exists()]
    failing = [
        item
        for item in stats
        if item["markdown_words"] < args.min_words
        or item["code_cells"] < args.min_code_cells
        or not item["has_source_span"]
        or not item["has_visual_call"]
        or not item["has_final_sanity"]
    ]
    report = {"expected_count": len(expected), "missing": missing, "failing_count": len(failing), "failing": failing, "stats": stats}
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Audited {len(stats)} canonical notebooks")
        if missing:
            print("Missing notebooks:")
            for path in missing:
                print(f"- {path}")
        if failing:
            print("Notebook audit failures:")
            for item in failing:
                print(f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells")
        if missing or failing:
            raise SystemExit(1)
        print("All canonical notebooks meet the configured standalone thresholds.")


if __name__ == "__main__":
    main()
