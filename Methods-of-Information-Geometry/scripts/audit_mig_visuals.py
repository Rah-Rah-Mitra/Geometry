"""Audit Methods of Information Geometry notebooks for chapter-specific visual language."""

from __future__ import annotations

import json
from pathlib import Path

import nbformat

import mig_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def rel(path: Path) -> str:
    return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


def main() -> None:
    findings = []
    stats = []
    for entry in inventory.ENTRIES:
        path = BOOK_ROOT / entry["folder"] / entry["notebook"]
        if not path.exists():
            findings.append(f"{rel(path)}: missing notebook")
            continue
        nb = nbformat.read(path, as_version=4)
        text = "\n".join("".join(cell.get("source", "")) for cell in nb.cells)
        term_hits = [term for term in entry["terms"] if term.lower() in text.lower()]
        artifact_hits = text.count("artifacts/") + text.count("artifact_path(") + text.count("save_matplotlib(")
        inspect_hits = text.lower().count("inspect") + text.lower().count("notice") + text.lower().count("read the")
        stats.append({"path": rel(path), "term_hits": term_hits, "artifact_hits": artifact_hits, "inspection_language_hits": inspect_hits})
        if len(term_hits) < 3:
            findings.append(f"{rel(path)}: fewer than three source-specific terms found")
        if artifact_hits < 3:
            findings.append(f"{rel(path)}: weak artifact integration")
        if inspect_hits < 2:
            findings.append(f"{rel(path)}: nearby visual inspection language appears thin")
    print(json.dumps(stats, indent=2))
    if findings:
        for finding in findings:
            print(f"- {finding}")
        raise SystemExit(1)
    print("Visual audit passed.")


if __name__ == "__main__":
    main()

