"""Audit Convex Analysis notebooks for source grounding and standalone shape."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = BOOK_ROOT.parent
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.section_catalog import sections  # noqa: E402
from utils.validation import (  # noqa: E402
    canonical_notebooks,
    code_sources,
    ensure_one_canonical_per_section,
    markdown_sources,
    relative,
)


def stats(path: Path) -> dict[str, object]:
    markdown = markdown_sources(path)
    code = code_sources(path)
    text = "\n".join(markdown)
    text_lower = text.lower()
    source = "\n".join(code)
    return {
        "path": relative(path, WORKSPACE_ROOT),
        "markdown_words": len(text.split()),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "has_setup": "BOOK_ROOT" in source,
        "has_artifact_call": "create_section_artifacts" in source,
        "has_sanity": "final_sanity" in source,
        "has_source_span": "source span" in text_lower,
        "has_library_routing": "library routing" in text_lower,
        "has_takeaways": "takeaways" in text_lower,
        "mentions_no_copy_guard": "no copied" in text_lower or "synthetic" in text_lower,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=650)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()

    expected = {section["number"]: section for section in sections()}
    items = [stats(path) for path in canonical_notebooks(BOOK_ROOT)]
    findings: list[dict[str, object]] = []
    for item in items:
        if item["markdown_words"] < args.min_words:
            findings.append({**item, "finding": "below standalone prose threshold"})
        if item["code_cells"] < args.min_code_cells:
            findings.append({**item, "finding": "below executable code-cell threshold"})
        for marker in [
            "has_setup",
            "has_artifact_call",
            "has_sanity",
            "has_source_span",
            "has_library_routing",
            "has_takeaways",
            "mentions_no_copy_guard",
        ]:
            if not item[marker]:
                findings.append({**item, "finding": f"missing marker: {marker}"})
    for finding in ensure_one_canonical_per_section(BOOK_ROOT, expected_count=len(expected)):
        findings.append({"path": relative(BOOK_ROOT, WORKSPACE_ROOT), "finding": finding})

    source_map = BOOK_ROOT / "inventory" / "source_map.json"
    if not source_map.exists():
        findings.append({"path": relative(source_map, WORKSPACE_ROOT), "finding": "missing source map"})

    report = {"notebook_count": len(items), "finding_count": len(findings), "findings": findings, "stats": items}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Audited {len(items)} canonical Convex Analysis notebooks")
        if findings:
            print(f"{len(findings)} finding(s):")
            for finding in findings:
                print(f"- {finding.get('path', '')}: {finding['finding']}")
        else:
            print("All notebooks meet the configured source, shape, and standalone checks.")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
