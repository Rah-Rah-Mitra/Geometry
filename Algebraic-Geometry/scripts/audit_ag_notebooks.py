"""Audit Hartshorne Algebraic Geometry notebooks for standalone depth.

This audit is intentionally stricter than a presence check. It rejects the
generic bootstrap phrases and renderer-named artifacts that can make a notebook
look complete while leaving the chapter-specific mathematics thin.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import nbformat


BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ag_inventory as inventory


GENERIC_MARKERS = [
    "local generated lab",
    "primary-visual.png",
    "secondary-visual-2.png",
    "secondary-visual-3.png",
    "interactive-lab.html",
    "working language is varieties, schemes, sheaves, divisors, cohomology, and finite algebraic tests",
    "assert_artifact is defined for audits",
    "the static figure gives one durable view of the central object",
    "source-specific inspection notes",
    "additional source span inspection contract",
]

REQUIRED_MARKERS = [
    "source coverage ledger",
    "visual storyboard",
    "library routing",
    "translation guide",
    "final_sanity",
    "source-coverage.json",
    "visual-storyboard.json",
    "final-sanity.json",
    "display_artifact",
    "artifacts/",
]


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def text_of(nb: nbformat.NotebookNode, cell_type: str) -> str:
    return "\n".join("".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == cell_type)


def section_coverage(markdown: str, entry: dict[str, object]) -> list[str]:
    norm = normalize(markdown)
    missing: list[str] = []
    for item in entry.get("sections", []):
        title = normalize(str(item["title"]))
        if title and title not in norm:
            missing.append(str(item["title"]))
    return missing


def canonical_folder_findings() -> list[dict[str, str]]:
    findings = []
    for folder in [p for p in BOOK_ROOT.iterdir() if p.is_dir() and (p / "00-index.ipynb").exists()]:
        canonical = [p for p in folder.glob("*.ipynb") if p.name != "00-index.ipynb"]
        if len(canonical) != 1:
            findings.append(
                {
                    "path": str(folder.relative_to(BOOK_ROOT)).replace("\\", "/"),
                    "issue": f"expected one canonical notebook, found {len(canonical)}",
                }
            )
    return findings


def audit_notebook(entry: dict[str, object], min_words: int, min_code_cells: int) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    path = BOOK_ROOT / str(entry["folder"]) / str(entry["notebook"])
    rel = str(path.relative_to(BOOK_ROOT)).replace("\\", "/")
    if not path.exists():
        return [{"path": rel, "issue": "missing canonical notebook"}]

    nb = nbformat.read(path, as_version=4)
    markdown = text_of(nb, "markdown")
    code = text_of(nb, "code")
    combined = f"{markdown}\n{code}"
    lower = combined.lower()
    normalized_paths = combined.replace("\\", "/")

    word_count = len(re.findall(r"\b\w+\b", markdown))
    if word_count < min_words:
        findings.append({"path": rel, "issue": f"too little standalone prose ({word_count} markdown words)"})

    code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]
    if len(code_cells) < min_code_cells:
        findings.append({"path": rel, "issue": f"too few code cells for a computational chapter ({len(code_cells)})"})

    if str(entry["printed_span"]) not in markdown or str(entry["pdf_span"]) not in markdown:
        findings.append({"path": rel, "issue": "verified printed/pdf source span is not stated"})

    for marker in REQUIRED_MARKERS:
        if marker.lower() not in lower and marker not in normalized_paths:
            findings.append({"path": rel, "issue": f"missing required notebook marker: {marker}"})

    for marker in GENERIC_MARKERS:
        if marker in lower:
            findings.append({"path": rel, "issue": f"generic bootstrap marker remains: {marker}"})

    missing_sections = section_coverage(markdown, entry)
    if missing_sections:
        findings.append(
            {
                "path": rel,
                "issue": "source coverage ledger omits inventory section titles",
                "missing": missing_sections[:12],
                "missing_count": len(missing_sections),
            }
        )

    visual_save_calls = code.count("save_matplotlib(") + code.count("save_plotly_html(")
    display_calls = code.count("display_artifact(")
    if visual_save_calls < 2:
        findings.append({"path": rel, "issue": f"too few visual save calls ({visual_save_calls})"})
    if display_calls < visual_save_calls:
        findings.append(
            {
                "path": rel,
                "issue": f"not all saved visuals are displayed near the lesson ({display_calls}/{visual_save_calls})",
            }
        )

    if re.search(r"(?<![A-Za-z])[A-Za-z]:[\\/]", combined):
        findings.append({"path": rel, "issue": "notebook contains a hardcoded absolute Windows path"})
    if "algebraic geometry.pdf" in lower:
        findings.append({"path": rel, "issue": "notebook mentions the source PDF filename"})

    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=1100)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()

    findings: list[dict[str, object]] = []
    for entry in inventory.ENTRIES:
        findings.extend(audit_notebook(entry, args.min_words, args.min_code_cells))
    findings.extend(canonical_folder_findings())

    report = {"notebook_count": len(inventory.ENTRIES), "failing_count": len(findings), "findings": findings}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Audited {len(inventory.ENTRIES)} Algebraic Geometry canonical notebooks.")
        for item in findings:
            print(f"FAIL: {item['path']}: {item['issue']}")
    raise SystemExit(1 if findings else 0)


if __name__ == "__main__":
    main()
