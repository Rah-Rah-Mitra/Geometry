"""Audit Methods of Information Geometry notebooks for standalone structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import nbformat

import mig_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-index.ipynb", "00-book-index.ipynb"}


def rel(path: Path) -> str:
    return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


def expected_paths() -> list[Path]:
    return [BOOK_ROOT / entry["folder"] / entry["notebook"] for entry in inventory.ENTRIES]


def notebook_stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    joined = "\n".join(markdown + code)
    visual_saves = sum(
        source.count("save_matplotlib(") + source.count("write_html(") + source.count("save_json(")
        for source in code
    )
    displays = sum(source.count("display_artifact(") + source.count("Image(") + source.count("display(") for source in code)
    return {
        "path": rel(path),
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "visual_save_calls": visual_saves,
        "display_calls": displays,
        "has_book_root": "BOOK_ROOT" in joined,
        "has_source_span": "Source span" in joined or "source span" in joined,
        "has_final_sanity": "final_sanity" in joined,
        "mentions_fisher_or_divergence": "Fisher" in joined or "divergence" in joined,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=800)
    parser.add_argument("--min-code-cells", type=int, default=4)
    args = parser.parse_args()

    missing = [rel(path) for path in expected_paths() if not path.exists()]
    stats = [notebook_stats(path) for path in expected_paths() if path.exists()]
    failing = [
        item
        for item in stats
        if item["markdown_words"] < args.min_words
        or item["code_cells"] < args.min_code_cells
        or item["visual_save_calls"] < 2
        or item["display_calls"] < 1
        or not item["has_book_root"]
        or not item["has_source_span"]
        or not item["has_final_sanity"]
        or not item["mentions_fisher_or_divergence"]
    ]
    report = {"notebook_count": len(stats), "missing": missing, "failing": failing, "stats": stats}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(stats)} Methods of Information Geometry canonical notebooks")
    for path in missing:
        print(f"- missing: {path}")
    for item in failing:
        print(
            f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells, "
            f"{item['visual_save_calls']} save calls, {item['display_calls']} display calls"
        )
    if missing or failing:
        raise SystemExit(1)
    print("All canonical notebooks meet the standalone structure thresholds.")


if __name__ == "__main__":
    main()

