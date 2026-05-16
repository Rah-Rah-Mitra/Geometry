"""Audit notebooks for visual explanations and artifact display calls."""

from __future__ import annotations

from pathlib import Path
import sys

import nbformat

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))

from scripts import otonn_inventory as inventory


def main() -> None:
    findings = []
    for unit in inventory.UNITS:
        path = inventory.unit_path(unit)
        if not path.exists():
            findings.append(f"{inventory.rel(path)}: missing canonical notebook")
            continue
        nb = nbformat.read(path, as_version=4)
        markdown = "\n".join(cell.source for cell in nb.cells if cell.cell_type == "markdown")
        code = "\n".join(cell.source for cell in nb.cells if cell.cell_type == "code")
        lower_markdown = markdown.lower()
        if "what to inspect" not in lower_markdown:
            findings.append(f"{inventory.rel(path)}: missing explicit visual inspection cue")
        if str(unit["mode"]) not in code:
            findings.append(f"{inventory.rel(path)}: visual mode not present in code")
        if "display_artifact(" not in code:
            findings.append(f"{inventory.rel(path)}: artifact is not displayed inline")
        if str(unit["visual"]).split()[0].lower() not in lower_markdown:
            findings.append(f"{inventory.rel(path)}: visual storyboard is not echoed in prose")
    if findings:
        for finding in findings:
            print(f"- {finding}")
        raise SystemExit(1)
    print(f"Visual audit passed for {len(inventory.UNITS)} canonical notebooks.")


if __name__ == "__main__":
    main()
