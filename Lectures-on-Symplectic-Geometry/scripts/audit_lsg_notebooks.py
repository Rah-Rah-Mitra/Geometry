"""Audit LSG notebooks for standalone depth and course-local structure."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

import nbformat
import lsg_inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-book-index.ipynb", "00-part-index.ipynb", "00-index.ipynb"}
STALE_PATH_PATTERNS = (
    "D:/Geometry",
    "D:\\Geometry",
    "/mnt/d/Geometry",
    "file://",
)
GENERIC_BUILDER_PATTERNS = (
    "build_visual_storyboard(",
    "create_lecture_artifacts(",
    "build_lsg_artifacts",
)


def source_entries_by_notebook() -> dict[str, dict[str, object]]:
    return {
        f"{entry['part']}/{entry['folder']}/{entry['notebook']}": entry
        for entry in lsg_inventory.ENTRIES
    }


def source_terms(entry: dict[str, object]) -> list[str]:
    terms = [str(entry["title"]), str(entry["focus"])]
    terms.extend(str(section) for section in entry.get("sections", []))
    terms.extend(str(concept) for concept in entry.get("concepts", []))
    return terms


def term_present(term: str, haystack: str) -> bool:
    tokens = [token for token in re.findall(r"[a-zA-Z][a-zA-Z-]{3,}", term.lower()) if token not in {"lecture", "symplectic"}]
    if not tokens:
        return True
    return sum(token in haystack for token in tokens) >= max(1, min(2, len(tokens)))


def discover_notebooks() -> list[Path]:
    artifact_root = BOOK_ROOT / "artifacts"
    return [
        path
        for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED
    ]


def normalize_cell(source: str) -> str:
    return re.sub(r"\s+", " ", source).strip()


def cell_digest(source: str) -> str:
    return hashlib.sha1(normalize_cell(source).encode("utf-8")).hexdigest()


def notebook_stats(path: Path, source_map: dict[str, dict[str, object]]) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    joined = "\n".join(markdown + code)
    rel = path.relative_to(BOOK_ROOT).as_posix()
    entry = source_map.get(rel)
    lower_joined = joined.lower()
    missing_terms = [] if entry is None else [term for term in source_terms(entry) if not term_present(term, lower_joined)]
    return {
        "path": rel,
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "display_artifact_calls": joined.count("display_artifact("),
        "has_source_span": "Source span" in joined and "physical PDF pages" in joined,
        "has_final_sanity": "final_sanity" in joined,
        "has_library_routing": "Library Routing" in joined or "library routing" in joined.lower(),
        "assert_count": joined.count("assert "),
        "generic_builder_calls": sum(joined.count(pattern) for pattern in GENERIC_BUILDER_PATTERNS),
        "has_stale_path": any(pattern in joined for pattern in STALE_PATH_PATTERNS),
        "source_terms_missing": missing_terms,
    }


def anti_generic_findings(paths: list[Path], *, min_repeat: int) -> list[dict[str, object]]:
    markdown_hashes: dict[str, list[dict[str, object]]] = defaultdict(list)
    code_hashes: dict[str, list[dict[str, object]]] = defaultdict(list)
    findings: list[dict[str, object]] = []

    for path in paths:
        nb = nbformat.read(path, as_version=4)
        rel = path.relative_to(BOOK_ROOT).as_posix()
        for index, cell in enumerate(nb.cells, start=1):
            source = "".join(cell.get("source", ""))
            normalized = normalize_cell(source)
            if len(normalized) < 120:
                continue
            item = {"path": rel, "cell": index, "preview": normalized[:140]}
            if cell.cell_type == "markdown":
                markdown_hashes[cell_digest(source)].append(item)
            elif cell.cell_type == "code":
                code_hashes[cell_digest(source)].append(item)

    for cell_type, groups in (("markdown", markdown_hashes), ("code", code_hashes)):
        for digest, hits in groups.items():
            notebook_count = len({hit["path"] for hit in hits})
            if notebook_count >= min_repeat:
                findings.append(
                    {
                        "finding": f"repeated {cell_type} cell",
                        "sha1": digest[:12],
                        "notebook_count": notebook_count,
                        "sample": hits[:8],
                    }
                )
    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=650)
    parser.add_argument("--min-code-cells", type=int, default=4)
    parser.add_argument("--strict", action="store_true", help="fail on generic scaffolding, stale paths, and weak sanity checks")
    parser.add_argument("--min-repeat", type=int, default=8)
    args = parser.parse_args()

    notebooks = discover_notebooks()
    source_map = source_entries_by_notebook()
    stats = [notebook_stats(path, source_map) for path in notebooks]
    failing = [
        item
        for item in stats
        if item["markdown_words"] < args.min_words
        or item["code_cells"] < args.min_code_cells
        or item["display_artifact_calls"] < 1
        or not item["has_source_span"]
        or not item["has_final_sanity"]
    ]
    strict_failing: list[dict[str, object]] = []
    if args.strict:
        for item in stats:
            for field in ("has_library_routing",):
                if not item[field]:
                    strict_failing.append({**item, "finding": f"missing strict marker: {field}"})
            if item["assert_count"] < 3:
                strict_failing.append({**item, "finding": "fewer than 3 explicit assertions"})
            if item["generic_builder_calls"]:
                strict_failing.append({**item, "finding": "generic builder call in canonical notebook"})
            if item["has_stale_path"]:
                strict_failing.append({**item, "finding": "stale absolute/local path"})
            if len(item["source_terms_missing"]) > 2:
                strict_failing.append({**item, "finding": "source-map terms underrepresented"})
        strict_failing.extend(anti_generic_findings(notebooks, min_repeat=args.min_repeat))

    report = {
        "notebook_count": len(stats),
        "failing_count": len(failing),
        "strict_failing_count": len(strict_failing),
        "failing": failing,
        "strict_failing": strict_failing,
        "stats": stats,
    }
    if args.json:
        print(json.dumps(report, indent=2))
        if failing or strict_failing:
            raise SystemExit(1)
        return
    print(f"Audited {len(stats)} canonical notebooks")
    if failing or strict_failing:
        if failing:
            print(f"{len(failing)} notebooks failed:")
        for item in failing:
            print(f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells")
        if strict_failing:
            print(f"{len(strict_failing)} strict finding(s):")
        for item in strict_failing:
            location = item.get("path", item.get("sample", ""))
            print(f"- {location}: {item['finding']}")
        raise SystemExit(1)
    print("All canonical notebooks meet the configured standalone thresholds.")


if __name__ == "__main__":
    main()
