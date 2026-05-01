"""Audit MVG notebooks for generated sameness and weak chapter specificity."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import nbformat

import mvg_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]

GENERIC_ARTIFACT_NAMES = {
    "concept-map.png",
    "geometry-scene.png",
    "diagnostic-dashboard.png",
    "constraint-dashboard.png",
    "numeric-summary.json",
}

GENERIC_BUILDER_CALLS = {
    "concept_map_figure(",
    "vision_scene_figure(",
    "diagnostic_figure(",
    "constraint_dashboard_figure(",
}

ALLOWED_REPEATED_HEADINGS = {
    "## Translation Guide",
    "## Route Through The Chapter",
    "## Applied Lab",
    "## Takeaways",
}


def entry_folder(entry: dict[str, Any]) -> Path:
    if entry["part"] is None:
        return BOOK_ROOT / entry["folder"]
    return BOOK_ROOT / entry["part"] / entry["folder"]


def notebook_paths() -> list[tuple[dict[str, Any], Path]]:
    return [(entry, entry_folder(entry) / entry["notebook"]) for entry in inventory.ENTRIES]


def rel(path: Path) -> str:
    return path.relative_to(BOOK_ROOT).as_posix()


def normalize(source: str) -> str:
    return re.sub(r"\s+", " ", source).strip()


def fingerprint(source: str) -> str:
    return hashlib.sha1(normalize(source).encode("utf-8")).hexdigest()


def chapter_terms(entry: dict[str, Any]) -> set[str]:
    words: set[str] = set()
    text = " ".join([entry["title"], entry["focus"], *entry.get("concepts", []), *entry.get("visuals", [])])
    for token in re.findall(r"[A-Za-z][A-Za-z0-9-]{3,}", text.lower()):
        if token not in {"chapter", "appendix", "geometry", "projective", "multiple", "view"}:
            words.add(token)
    return words


def audit(args: argparse.Namespace) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    markdown_fingerprints: dict[str, list[dict[str, Any]]] = defaultdict(list)
    code_fingerprints: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for entry, path in notebook_paths():
        nb = nbformat.read(path, as_version=4)
        joined_markdown = "\n".join("".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown")
        joined_code = "\n".join("".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code")
        lower_text = (joined_markdown + "\n" + joined_code).lower()
        terms = chapter_terms(entry)
        present_terms = sorted(term for term in terms if term in lower_text)

        if len(present_terms) < args.min_terms:
            findings.append(
                {
                    "check": "weak-chapter-specificity",
                    "path": rel(path),
                    "message": f"only {len(present_terms)} chapter-specific terms found",
                    "details": {"present_terms": present_terms[:20]},
                }
            )

        if "library routing" not in lower_text and "libraries used" not in lower_text:
            findings.append(
                {
                    "check": "missing-library-routing-note",
                    "path": rel(path),
                    "message": "notebook does not explain why its visualization libraries fit the chapter",
                }
            )

        for name in GENERIC_ARTIFACT_NAMES:
            if name in joined_code:
                findings.append(
                    {
                        "check": "generic-artifact-name",
                        "path": rel(path),
                        "message": f"uses generic artifact name {name}",
                    }
                )

        for call in GENERIC_BUILDER_CALLS:
            if call in joined_code:
                findings.append(
                    {
                        "check": "generic-visual-builder",
                        "path": rel(path),
                        "message": f"uses generic visual builder {call.rstrip('(')}",
                    }
                )

        for index, cell in enumerate(nb.cells, start=1):
            source = "".join(cell.get("source", ""))
            normalized = normalize(source)
            if len(normalized) < 80 or normalized in ALLOWED_REPEATED_HEADINGS:
                continue
            item = {"path": rel(path), "cell": index, "preview": normalized[:160]}
            if cell.cell_type == "markdown":
                markdown_fingerprints[fingerprint(source)].append(item)
            elif cell.cell_type == "code":
                code_fingerprints[fingerprint(source)].append(item)

    for cell_type, groups in [("markdown", markdown_fingerprints), ("code", code_fingerprints)]:
        for digest, hits in groups.items():
            if len(hits) >= args.min_repeat:
                findings.append(
                    {
                        "check": f"repeated-{cell_type}-cell",
                        "path": hits[0]["path"],
                        "message": f"{len(hits)} notebooks share cell fingerprint {digest[:12]}",
                        "details": hits[: args.max_details],
                    }
                )

    by_check = Counter(finding["check"] for finding in findings)
    return {
        "summary": {
            "notebook_count": len(inventory.ENTRIES),
            "finding_count": len(findings),
            "findings_by_check": dict(sorted(by_check.items())),
        },
        "findings": findings,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-repeat", type=int, default=10)
    parser.add_argument("--min-terms", type=int, default=8)
    parser.add_argument("--max-details", type=int, default=12)
    parser.add_argument("--no-fail", action="store_true")
    args = parser.parse_args()

    report = audit(args)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        summary = report["summary"]
        print(f"Audited {summary['notebook_count']} canonical notebooks for generic content")
        if report["findings"]:
            for finding in report["findings"]:
                print(f"- {finding['check']} [{finding.get('path', '')}]: {finding['message']}")
        else:
            print("No generic-content findings.")
    if report["findings"] and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
