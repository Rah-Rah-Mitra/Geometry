"""Audit ACMG notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
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
from utils.source import COURSE_MAP  # noqa: E402


GENERIC_MARKERS = [
    "primary-visual.png",
    "interactive-lab.html",
    "Local generated lab",
    "source-specific diagram",
    "static visual and slider artifact",
    "The working language is metric spaces, length structures, comparison geometry, and curvature bounds.",
]


def stats(path: Path) -> dict[str, object]:
    markdown = markdown_sources(path)
    code = code_sources(path)
    text = "\n".join(markdown)
    code_text = "\n".join(code)
    text_lower = text.lower()
    code_lower = code_text.lower()
    return {
        "path": relative(path),
        "markdown_words": len(text.split()),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "has_setup": "BOOK_ROOT" in code_text,
        "has_sanity": "final_sanity" in code_text,
        "has_takeaways": "takeaways" in text_lower,
        "has_storyboard": (
            "storyboard" in text_lower
            and ("storyboard" in code_lower or "source-coverage" in code_lower)
        )
        or ("source-coverage" in code_lower and "library_routing" in code_lower),
        "has_lab": "lab" in text_lower,
        "has_source_span": "source span" in text_lower or "source_span" in code_lower,
        "has_library_routing": "library routing" in text_lower or "library_routing" in code_lower,
        "has_display_calls": "display_artifact" in code_text,
    }


def normalize(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def chapter_entry(path: Path) -> dict[str, object] | None:
    for item in COURSE_MAP:
        if path.name == item["notebook"]:
            return item
    return None


def source_coverage_sections(path: Path) -> set[str]:
    entry = chapter_entry(path)
    if entry is None:
        return set()
    checks_root = BOOK_ROOT / "artifacts" / f"chapter-{entry['number']:02d}" / "checks"
    section_numbers: set[str] = set()
    for coverage_path in sorted(checks_root.glob("*source-coverage.json")):
        try:
            data = json.loads(coverage_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        rows = data.get("source_sections", data.get("sections", []))
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            section = row.get("section") or row.get("number") or row.get("source_section")
            if section is not None:
                section_numbers.add(str(section))
    return section_numbers


def strict_findings(path: Path) -> list[dict[str, object]]:
    markdown = markdown_sources(path)
    code = code_sources(path)
    text = "\n".join(markdown)
    code_text = "\n".join(code)
    combined = f"{text}\n{code_text}"
    findings: list[dict[str, object]] = []
    for marker in GENERIC_MARKERS:
        if marker in combined:
            findings.append({"path": relative(path), "finding": f"generic scaffold marker remains: {marker}"})
    if "source-coverage.json" not in code_text:
        findings.append({"path": relative(path), "finding": "missing source-coverage.json check artifact"})
    if "final-sanity.json" not in code_text:
        findings.append({"path": relative(path), "finding": "missing final-sanity.json check artifact"})
    if "D:\\Geometry" in combined or "D:/Geometry" in combined or "C:\\Users" in combined or "C:/Users" in combined:
        findings.append({"path": relative(path), "finding": "hardcoded workspace path"})

    entry = chapter_entry(path)
    if entry is not None:
        coverage_sections = source_coverage_sections(path)
        text_norm = normalize(text)
        for section in entry["sections"]:
            section_number = str(section["number"])
            if coverage_sections and any(
                covered == section_number or covered.startswith(f"{section_number} ") for covered in coverage_sections
            ):
                continue
            title = str(section["title"])
            tokens = [token for token in normalize(title).split() if len(token) >= 5]
            if not tokens:
                continue
            present = sum(1 for token in tokens if token in text_norm)
            if present < max(1, len(tokens) - 1):
                findings.append(
                    {
                        "path": relative(path),
                        "finding": f"missing source-section coverage marker: {section['number']} {title}",
                    }
                )
    return findings


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
    parser.add_argument("--strict", action="store_true")
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
    if args.strict:
        for path in notebooks:
            findings.extend(strict_findings(path))

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
