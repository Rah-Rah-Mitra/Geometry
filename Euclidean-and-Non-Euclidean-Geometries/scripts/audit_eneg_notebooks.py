"""Audit ENEG notebooks for standalone depth and required structure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import canonical_notebooks, code_sources, ensure_one_canonical_per_work_unit, markdown_sources, relative  # noqa: E402


def stats(path: Path) -> dict[str, object]:
    markdown = markdown_sources(path)
    code = code_sources(path)
    text = "\n".join(markdown)
    code_text = "\n".join(code)
    return {
        "path": relative(path),
        "markdown_words": len(text.split()),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "has_setup": "BOOK_ROOT" in code_text,
        "has_sanity": "final_sanity" in code_text,
        "has_chapter_sanity": "chapter_sanity" in code_text,
        "has_takeaways": "Takeaways" in text,
        "has_applied_lab": "Applied Lab" in text,
        "has_source_span": "Source Span" in text,
        "has_definition_bank": "Definition Bank" in text,
        "has_worked_example": "Worked Example" in text,
        "has_equation_marker": "$" in text,
        "uses_generic_artifact_names": any(name in code_text for name in ["relationship-map.png", "geometric-scene.png", "applied-lab.png"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()

    items = [stats(path) for path in canonical_notebooks(BOOK_ROOT)]
    findings = []
    for item in items:
        if item["markdown_words"] < args.min_words:
            findings.append({**item, "finding": "below word threshold"})
        if item["code_cells"] < args.min_code_cells:
            findings.append({**item, "finding": "below code-cell threshold"})
        for marker in [
            "has_setup",
            "has_sanity",
            "has_chapter_sanity",
            "has_takeaways",
            "has_applied_lab",
            "has_source_span",
            "has_definition_bank",
            "has_worked_example",
            "has_equation_marker",
        ]:
            if not item[marker]:
                findings.append({**item, "finding": f"missing {marker}"})
        if item["uses_generic_artifact_names"]:
            findings.append({**item, "finding": "uses generic artifact filenames"})
    for finding in ensure_one_canonical_per_work_unit(BOOK_ROOT):
        findings.append({"path": "", "finding": finding})

    report = {"notebook_count": len(items), "finding_count": len(findings), "findings": findings, "stats": items}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Audited {len(items)} canonical notebooks")
        if findings:
            print(f"{len(findings)} finding(s):")
            for finding in findings:
                print(f"- {finding.get('path', '')}: {finding['finding']}")
        else:
            print("All ENEG notebooks meet the configured depth and shape checks.")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
