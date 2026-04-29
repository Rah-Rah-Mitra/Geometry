"""Audit IVA notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import nbformat

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-index.ipynb", "00-book-index.ipynb"}


def discover_notebooks() -> list[Path]:
    artifact_root = BOOK_ROOT / "artifacts"
    return [
        path
        for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED
    ]


def notebook_stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    return {
        "path": str(path.relative_to(BOOK_ROOT)).replace("\\", "/"),
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "visual_save_calls": sum(source.count("save_matplotlib(") + source.count("save_plotly_html(") for source in code),
        "display_artifact_calls": sum(source.count("display_artifact(") for source in code),
        "has_final_sanity": any("final_sanity" in source for source in code),
    }


def canonical_folder_findings() -> list[dict[str, str]]:
    findings = []
    for folder in [p for p in BOOK_ROOT.rglob("*") if p.is_dir() and (p / "00-index.ipynb").exists()]:
        canonical = [p for p in folder.glob("*.ipynb") if p.name != "00-index.ipynb"]
        if len(canonical) != 1:
            findings.append({"path": str(folder.relative_to(BOOK_ROOT)), "message": f"expected one canonical notebook, found {len(canonical)}"})
    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()
    stats = [notebook_stats(path) for path in discover_notebooks()]
    failing = [
        item
        for item in stats
        if item["markdown_words"] < args.min_words
        or item["code_cells"] < args.min_code_cells
        or item["visual_save_calls"] == 0
        or item["display_artifact_calls"] < item["visual_save_calls"]
        or not item["has_final_sanity"]
    ]
    structure = canonical_folder_findings()
    report = {"notebook_count": len(stats), "failing_count": len(failing), "failing": failing, "structure_findings": structure, "stats": stats}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(stats)} canonical notebooks")
    if failing or structure:
        for item in failing:
            print(f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells, {item['visual_save_calls']} visual saves, {item['display_artifact_calls']} displays")
        for item in structure:
            print(f"- {item['path']}: {item['message']}")
        raise SystemExit(1)
    print("All IVA canonical notebooks meet standalone structure thresholds.")


if __name__ == "__main__":
    main()
