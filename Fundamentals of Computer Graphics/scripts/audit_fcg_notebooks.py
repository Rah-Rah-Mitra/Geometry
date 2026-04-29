"""Audit FCG notebook structure and standalone teaching density."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import fcg_inventory as inventory

BOOK_ROOT = inventory.BOOK_ROOT
IGNORED = {"00-book-index.ipynb", "00-index.ipynb"}
REQUIRED_PHRASES = ["Translation guide", "Visual storyboard", "Applied lab", "Sanity checks", "Takeaways"]


def markdown_words(cells: list[dict[str, Any]]) -> int:
    text = "\n".join("".join(cell.get("source", "")) for cell in cells if cell.get("cell_type") == "markdown")
    return len(re.findall(r"[A-Za-z][A-Za-z0-9'-]*", text))


def audit_notebook(path: Path, min_words: int, min_code_cells: int) -> list[dict[str, str]]:
    findings = []
    data = json.loads(path.read_text(encoding="utf-8"))
    cells = data.get("cells", [])
    words = markdown_words(cells)
    code_cells = sum(1 for cell in cells if cell.get("cell_type") == "code")
    source = "\n".join("".join(cell.get("source", "")) for cell in cells)
    if words < min_words:
        findings.append({"check": "too-few-words", "path": rel(path), "message": f"{words} words < {min_words}"})
    if code_cells < min_code_cells:
        findings.append({"check": "too-few-code-cells", "path": rel(path), "message": f"{code_cells} code cells < {min_code_cells}"})
    for phrase in REQUIRED_PHRASES:
        if phrase not in source:
            findings.append({"check": "missing-section", "path": rel(path), "message": phrase})
    if "display_artifact(" not in source:
        findings.append({"check": "missing-display-artifact", "path": rel(path), "message": "no display_artifact call"})
    if "D:/Geometry" in source or "D:\\Geometry" in source:
        findings.append({"check": "hardcoded-workspace-path", "path": rel(path), "message": "contains hardcoded workspace path"})
    return findings


def rel(path: Path) -> str:
    return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


def audit(min_words: int, min_code_cells: int) -> dict[str, Any]:
    findings = []
    for entry in inventory.ENTRIES:
        folder = BOOK_ROOT / str(entry["folder"])
        canonical = folder / str(entry["notebook"])
        index = folder / "00-index.ipynb"
        if not index.exists():
            findings.append({"check": "missing-index", "path": rel(index), "message": "chapter index missing"})
        canonicals = [path for path in folder.glob("*.ipynb") if path.name not in IGNORED]
        if canonical not in canonicals:
            findings.append({"check": "missing-canonical", "path": rel(canonical), "message": "canonical notebook missing"})
        if len(canonicals) != 1:
            findings.append({"check": "canonical-count", "path": rel(folder), "message": f"{len(canonicals)} canonical notebooks"})
        if canonical.exists():
            findings.extend(audit_notebook(canonical, min_words, min_code_cells))
    return {"summary": {"chapter_count": len(inventory.ENTRIES), "finding_count": len(findings)}, "findings": findings}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-fail", action="store_true")
    args = parser.parse_args()
    report = audit(args.min_words, args.min_code_cells)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Audited {report['summary']['chapter_count']} FCG chapter notebooks")
        if report["findings"]:
            for finding in report["findings"]:
                print(f"- {finding['check']} [{finding['path']}]: {finding['message']}")
        else:
            print("All FCG notebook checks passed.")
    if report["findings"] and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
