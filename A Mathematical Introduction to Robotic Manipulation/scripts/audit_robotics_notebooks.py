"""Audit robotics notebooks for standalone depth and executable structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import nbformat

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-book-index.ipynb", "00-part-index.ipynb", "00-index.ipynb"}


def discover_notebooks() -> list[Path]:
    artifact_root = BOOK_ROOT / "artifacts"
    return [path for path in sorted(BOOK_ROOT.rglob("*.ipynb")) if artifact_root not in path.parents and path.name not in IGNORED]


def stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    text = "\n".join(markdown + code)
    forbidden = ["Figure 1.", "Courtesy of", "This manuscript is for personal use only"]
    return {
        "path": str(path.relative_to(BOOK_ROOT)),
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "artifact_refs": sum(source.count("build_storyboard") + source.count("display_artifact") + source.count("save_json") for source in code),
        "forbidden_hits": [item for item in forbidden if item in text],
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
    print("All canonical notebooks meet the configured depth thresholds.")


if __name__ == "__main__":
    main()
