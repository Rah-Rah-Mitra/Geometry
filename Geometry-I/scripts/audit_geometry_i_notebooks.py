"""Audit Geometry I notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = Path(__file__).resolve().parent
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import geometry_i_inventory as inventory  # noqa: E402
from utils.validation import canonical_notebooks, code_sources, ensure_one_canonical_per_source, markdown_sources, relative  # noqa: E402


def notebook_stats(path: Path) -> dict[str, object]:
    markdown = markdown_sources(path)
    code = code_sources(path)
    text = "\n".join(markdown)
    return {
        "path": relative(path),
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "display_artifact_refs": sum(source.count("display_artifact") for source in code),
        "visual_builder_refs": sum(source.count("build_visual_suite") for source in code),
        "has_takeaways": "takeaways" in text.lower(),
        "has_applied_lab": "applied lab" in text.lower(),
        "has_sanity_checks": "sanity check" in text.lower() or "sanity checks" in text.lower(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()

    expected_folders = [BOOK_ROOT / entry["folder"] for entry in inventory.ENTRIES]
    structure_findings = ensure_one_canonical_per_source(expected_folders)
    stats = [notebook_stats(path) for path in canonical_notebooks(BOOK_ROOT)]
    failing = [
        item
        for item in stats
        if item["markdown_words"] < args.min_words
        or item["code_cells"] < args.min_code_cells
        or item["display_artifact_refs"] == 0
        or item["visual_builder_refs"] == 0
        or not item["has_takeaways"]
        or not item["has_applied_lab"]
        or not item["has_sanity_checks"]
    ]
    report = {
        "expected_units": len(inventory.ENTRIES),
        "notebook_count": len(stats),
        "structure_findings": structure_findings,
        "failing_count": len(failing),
        "failing": failing,
        "stats": stats,
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Audited {len(stats)} canonical notebooks")
        if structure_findings:
            print("Structure findings:")
            for finding in structure_findings:
                print(f"- {finding}")
        if failing:
            print(f"{len(failing)} notebooks failed depth or structure checks:")
            for item in failing:
                print(f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells")
        if not structure_findings and not failing:
            print("All canonical notebooks meet the configured structure and depth thresholds.")
    if structure_findings or failing or len(stats) != len(inventory.ENTRIES):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

