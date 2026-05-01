"""Audit Modern Robotics notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import nbformat

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-book-index.ipynb", "00-part-index.ipynb", "00-index.ipynb"}
FORBIDDEN = [
    "This document is the preprint",
    "May 2017 preprint",
    "Figure 2.",
    "Figure 3.",
    "used with permission",
]


def discover_notebooks() -> list[Path]:
    artifact_root = BOOK_ROOT / "artifacts"
    return [path for path in sorted(BOOK_ROOT.rglob("*.ipynb")) if artifact_root not in path.parents and path.name not in IGNORED]


def stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    text = "\n".join(markdown + code)
    return {
        "path": str(path.relative_to(BOOK_ROOT)),
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "visual_refs": sum(source.count("build_chapter_visuals") + source.count("display_artifact") for source in code),
        "forbidden_hits": [item for item in FORBIDDEN if item in text],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()
    items = [stats(path) for path in discover_notebooks()]
    failing = [
        item
        for item in items
        if item["markdown_words"] < args.min_words or item["code_cells"] < args.min_code_cells or item["forbidden_hits"]
    ]
    report = {"notebook_count": len(items), "failing_count": len(failing), "failing": failing, "stats": items}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(items)} canonical notebooks")
    if failing:
        for item in failing:
            print(f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells, forbidden={item['forbidden_hits']}")
        raise SystemExit(1)
    print("All canonical notebooks meet the configured standalone thresholds.")


if __name__ == "__main__":
    main()

