"""Audit ACMG notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import (  # noqa: E402
    canonical_notebooks,
    code_sources,
    ensure_one_canonical_per_chapter,
    markdown_sources,
    relative,
)


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
        "has_takeaways": "Takeaways" in text,
        "has_storyboard": "Visual Storyboard" in text and "visual-storyboard.json" in code_text,
        "has_lab": "Applied Lab" in text,
        "has_source_span": "Source Span" in text,
        "has_library_routing": "Library Routing" in text,
        "has_display_calls": "display_artifact" in code_text,
    }


def markdown_fingerprints(paths: list[Path]) -> list[dict[str, object]]:
    by_hash: dict[str, list[str]] = {}
    for path in paths:
        for source in markdown_sources(path):
            normalized = " ".join(source.lower().split())
            if len(normalized.split()) < 35:
                continue
            digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
            by_hash.setdefault(digest, []).append(relative(path))
    findings = []
    for digest, owners in by_hash.items():
        unique = sorted(set(owners))
        if len(unique) > 1:
            findings.append({"finding": "repeated long markdown cell", "sha256": digest, "paths": unique})
    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=900)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()

    notebooks = canonical_notebooks(BOOK_ROOT)
    items = [stats(path) for path in notebooks]
    findings: list[dict[str, object]] = []
    for item in items:
        if item["markdown_words"] < args.min_words:
            findings.append({**item, "finding": "below word threshold"})
        if item["code_cells"] < args.min_code_cells:
            findings.append({**item, "finding": "below code-cell threshold"})
        for marker in [
            "has_setup",
            "has_sanity",
            "has_takeaways",
            "has_storyboard",
            "has_lab",
            "has_source_span",
            "has_library_routing",
            "has_display_calls",
        ]:
            if not item[marker]:
                findings.append({**item, "finding": f"missing required marker: {marker}"})
    for finding in ensure_one_canonical_per_chapter(BOOK_ROOT):
        findings.append({"path": "", "finding": finding})
    findings.extend(markdown_fingerprints(notebooks))

    report = {"notebook_count": len(items), "finding_count": len(findings), "findings": findings, "stats": items}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Audited {len(items)} canonical notebooks")
        if findings:
            print(f"{len(findings)} finding(s):")
            for finding in findings:
                print(f"- {finding.get('path', finding.get('paths', ''))}: {finding['finding']}")
        else:
            print("All ACMG notebooks meet the configured depth and shape checks.")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

