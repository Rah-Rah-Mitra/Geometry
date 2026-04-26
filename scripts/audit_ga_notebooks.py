"""Audit authored GA course notebooks for depth and executable structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import nbformat

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_ROOT = PROJECT_ROOT / "Geometric-Algebra-for-Computer-Science"


def notebook_stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    headings = [
        line.strip()
        for source in markdown
        for line in source.splitlines()
        if line.lstrip().startswith("#")
    ]
    artifact_refs = sum(source.count("save_") + source.count("display_artifact") for source in code)
    interactive_refs = sum(
        source.count("plotly") + source.count("go.Figure") + source.count("ipywidgets")
        for source in code
    )
    return {
        "path": str(path.relative_to(PROJECT_ROOT)),
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "headings": headings,
        "artifact_refs": artifact_refs,
        "interactive_refs": interactive_refs,
    }


def discover_notebooks() -> list[Path]:
    candidates = sorted(BOOK_ROOT.rglob("*.ipynb"))
    ignored_names = {
        "00-index.ipynb",
        "00-part-index.ipynb",
        "00-book-index.ipynb",
        "legacy-seed-why-geometric-algebra.ipynb",
    }
    return [path for path in candidates if path.name not in ignored_names]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=4)
    args = parser.parse_args()

    stats = [notebook_stats(path) for path in discover_notebooks()]
    failing = [
        item
        for item in stats
        if item["markdown_words"] < args.min_words or item["code_cells"] < args.min_code_cells
    ]
    report = {
        "notebook_count": len(stats),
        "failing_count": len(failing),
        "failing": failing,
        "stats": stats,
    }
    if args.json:
        print(json.dumps(report, indent=2))
        return

    print(f"Audited {len(stats)} notebooks")
    if failing:
        print(f"{len(failing)} notebooks are below depth thresholds:")
        for item in failing:
            print(
                f"- {item['path']}: {item['markdown_words']} words, "
                f"{item['code_cells']} code cells"
            )
    else:
        print("All notebooks meet the configured depth thresholds.")


if __name__ == "__main__":
    main()
