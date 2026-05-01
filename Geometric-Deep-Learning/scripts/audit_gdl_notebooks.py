"""Audit GDL course notebooks for depth and executable structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import nbformat

import gdl_inventory as inventory

BOOK_ROOT = inventory.BOOK_ROOT
REPO_ROOT = inventory.REPO_ROOT


def notebook_stats(path: Path) -> dict[str, Any]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    headings = [
        line.strip()
        for source in markdown
        for line in source.splitlines()
        if line.lstrip().startswith("#")
    ]
    artifact_refs = sum(
        source.count("save_matplotlib")
        + source.count("save_plotly_html")
        + source.count("save_json")
        + source.count("display_artifact")
        for source in code
    )
    return {
        "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "headings": headings,
        "artifact_refs": artifact_refs,
    }


def discover_notebooks() -> list[Path]:
    return [inventory.canonical_path(entry) for entry in inventory.ENTRIES]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()

    stats = [notebook_stats(path) for path in discover_notebooks()]
    failing = [
        item
        for item in stats
        if item["markdown_words"] < args.min_words
        or item["code_cells"] < args.min_code_cells
        or item["artifact_refs"] < 3
    ]
    report = {"notebook_count": len(stats), "failing_count": len(failing), "failing": failing, "stats": stats}
    if args.json:
        print(json.dumps(report, indent=2))
        return

    print(f"Audited {len(stats)} canonical notebooks")
    if failing:
        print(f"{len(failing)} notebooks are below thresholds:")
        for item in failing:
            print(
                f"- {item['path']}: {item['markdown_words']} words, "
                f"{item['code_cells']} code cells, {item['artifact_refs']} artifact refs"
            )
        raise SystemExit(1)
    print("All GDL notebooks meet the configured depth thresholds.")


if __name__ == "__main__":
    main()

