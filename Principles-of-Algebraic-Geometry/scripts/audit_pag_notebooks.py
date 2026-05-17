import json
import re
import sys
from pathlib import Path

import nbformat

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pag_inventory as inv


GENERIC_MARKERS = [
    "printed pages verify",
    "physical source pages verify",
    "local generated lab",
    "primary-visual.png",
    "interactive-lab.html",
    "visual and computational reconstruction of",
    "working language is complex varieties, divisors, residues, surfaces, and cohomological ledgers",
    "assert_artifact is defined for audits",
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
]


def text_of(nb, cell_type):
    return "\n".join("".join(cell.source) for cell in nb.cells if cell.cell_type == cell_type)


def normalize(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def section_coverage(markdown, entry):
    norm = normalize(markdown)
    missing = []
    for item in entry.get("sections", []):
        title = normalize(item["title"])
        if title and title not in norm:
            missing.append(item["title"])
    return missing


def audit_notebook(entry):
    findings = []
    path = BOOK_ROOT / entry["folder"] / entry["notebook"]
    if not path.exists():
        return [{"path": str(path), "issue": "missing notebook"}]

    nb = nbformat.read(path, as_version=4)
    markdown = text_of(nb, "markdown")
    code = text_of(nb, "code")
    combined = f"{markdown}\n{code}"
    lower = combined.lower()

    word_count = len(re.findall(r"\b\w+\b", markdown))
    if word_count < 1200:
        findings.append({"path": str(path), "issue": f"too little standalone prose ({word_count} markdown words)"})

    if entry["printed_span"] not in markdown or entry["pdf_span"] not in markdown:
        findings.append({"path": str(path), "issue": "verified printed/pdf source span is not stated"})

    for marker in REQUIRED_MARKERS:
        if marker.lower() not in lower:
            findings.append({"path": str(path), "issue": f"missing required notebook marker: {marker}"})

    for marker in GENERIC_MARKERS:
        if marker in lower:
            findings.append({"path": str(path), "issue": f"generic bootstrap marker remains: {marker}"})

    missing_sections = section_coverage(markdown, entry)
    if missing_sections:
        findings.append(
            {
                "path": str(path),
                "issue": "source coverage ledger omits section titles",
                "missing": missing_sections[:12],
                "missing_count": len(missing_sections),
            }
        )

    code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]
    if len(code_cells) < 6:
        findings.append({"path": str(path), "issue": f"too few code cells for a computational chapter ({len(code_cells)})"})

    if re.search(r"(?<![A-Za-z])[A-Za-z]:[\\/]", combined):
        findings.append({"path": str(path), "issue": "notebook contains a hardcoded absolute Windows path"})

    if "artifacts/" not in combined.replace("\\", "/"):
        findings.append({"path": str(path), "issue": "notebook does not reference book-local artifact paths"})

    return findings


def main():
    findings = []
    for entry in inv.ENTRIES:
        findings.extend(audit_notebook(entry))
    print(json.dumps({"notebook_count": len(inv.ENTRIES), "findings": findings}, indent=2))
    raise SystemExit(1 if findings else 0)


if __name__ == "__main__":
    main()
