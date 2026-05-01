"""Audit Modern Robotics visual calls and generated artifacts."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image
import numpy as np

SCRIPT_ROOT = Path(__file__).resolve().parent
BOOK_ROOT = SCRIPT_ROOT.parent
sys.path.insert(0, str(SCRIPT_ROOT))

from modern_robotics_inventory import CHAPTERS

IGNORED = {"00-book-index.ipynb", "00-part-index.ipynb", "00-index.ipynb"}
VISUAL_CALLS = {"build_storyboard", "build_chapter_visuals", "display_artifact", "save_matplotlib", "save_json"}


def _relative(path: Path) -> str:
    return path.resolve().relative_to(BOOK_ROOT.resolve()).as_posix()


def _call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def notebook_findings() -> list[dict[str, Any]]:
    findings = []
    for path in sorted(BOOK_ROOT.rglob("*.ipynb")):
        if path.name in IGNORED or (BOOK_ROOT / "artifacts") in path.parents:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        visual_calls = 0
        display_calls = 0
        for index, cell in enumerate(data.get("cells", []), start=1):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", ""))
            try:
                tree = ast.parse(source)
            except SyntaxError as exc:
                findings.append({"check": "parse-error", "path": _relative(path), "message": f"cell {index}: {exc.msg}"})
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    name = _call_name(node)
                    if name in VISUAL_CALLS:
                        visual_calls += 1
                    if name == "display_artifact":
                        display_calls += 1
        if visual_calls < 2:
            findings.append({"check": "few-visual-calls", "path": _relative(path), "message": "Notebook has too few visual or artifact calls."})
        if display_calls == 0:
            findings.append({"check": "missing-display", "path": _relative(path), "message": "Notebook does not display generated artifacts."})
    return findings


def artifact_findings() -> list[dict[str, Any]]:
    findings = []
    for chapter in CHAPTERS:
        root = BOOK_ROOT / "artifacts" / chapter.slug
        pngs = sorted((root / "figures").glob("*.png"))
        if len(pngs) < 3:
            findings.append({"check": "missing-pngs", "path": _relative(root), "message": f"Expected at least 3 PNG artifacts, found {len(pngs)}."})
        for path in pngs:
            image = Image.open(path).convert("RGB")
            arr = np.asarray(image, dtype=float)
            if path.stat().st_size < 1000:
                findings.append({"check": "small-image", "path": _relative(path), "message": "Image is too small."})
            if float(arr.std()) < 2.0:
                findings.append({"check": "low-variation", "path": _relative(path), "message": "Image appears blank or nearly blank."})
        checks = root / "checks" / "final-sanity.json"
        if not checks.exists():
            findings.append({"check": "missing-checks", "path": _relative(root), "message": "Missing final-sanity.json."})
    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    findings = notebook_findings() + artifact_findings()
    report = {"finding_count": len(findings), "findings": findings}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    if findings:
        print(f"Visual audit found {len(findings)} issue(s)")
        for item in findings:
            print(f"- {item['check']}: {item['path']} - {item['message']}")
        raise SystemExit(1)
    print("Visual audit passed: notebooks generate/display visuals and artifacts are nonblank.")


if __name__ == "__main__":
    main()

