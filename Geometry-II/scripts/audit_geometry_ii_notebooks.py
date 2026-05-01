"""Audit Geometry II notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import canonical_notebooks, code_sources, ensure_one_canonical_per_chapter, markdown_sources, relative  # noqa: E402


STALE_PATTERNS = [
    "D:/Geometry/artifacts",
    r"D:\Geometry\artifacts",
    "/mnt/d/Geometry/artifacts",
    "D:/Geometry/utils",
    r"D:\Geometry\utils",
    "/mnt/d/Geometry/utils",
    "D:/Geometry/scripts",
    r"D:\Geometry\scripts",
    "/mnt/d/Geometry/scripts",
]


def stats(path: Path) -> dict[str, object]:
    markdown = markdown_sources(path)
    code = code_sources(path)
    text = "\n".join(markdown)
    code_text = "\n".join(code)
    full_text = text + "\n" + code_text
    lower_text = text.lower()
    return {
        "path": relative(path),
        "markdown_words": len(text.split()),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "has_setup": "BOOK_ROOT" in code_text,
        "has_sanity": "final_sanity" in code_text,
        "has_takeaways": "takeaways" in lower_text,
        "has_translation_guide": "translation guide" in lower_text,
        "has_storyboard": "visualization storyboard" in lower_text,
        "has_stale_paths": any(pattern in full_text for pattern in STALE_PATTERNS),
        "mentions_pdf_crop": "page crop" in text.lower() or "screenshot" in text.lower(),
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
        if not item["has_setup"] or not item["has_sanity"] or not item["has_takeaways"]:
            findings.append({**item, "finding": "missing required notebook shape marker"})
        if not item["has_translation_guide"] or not item["has_storyboard"]:
            findings.append({**item, "finding": "missing standalone teaching scaffold"})
        if item["has_stale_paths"]:
            findings.append({**item, "finding": "contains stale root-level path"})
        if item["mentions_pdf_crop"]:
            findings.append({**item, "finding": "mentions screenshots/page crops"})
    for finding in ensure_one_canonical_per_chapter(BOOK_ROOT):
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
            print("All Geometry II notebooks meet the configured depth and shape checks.")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
