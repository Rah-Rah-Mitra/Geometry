"""Audit robotics notebook visual calls and generated PNG artifacts."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

from robotics_inventory import ENTRIES

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-book-index.ipynb", "00-part-index.ipynb", "00-index.ipynb"}
VISUAL_CALLS = {"build_storyboard", "build_visual", "save_matplotlib", "save_image", "save_plotly_html"}


def _relative(path: Path) -> str:
    return path.resolve().relative_to(BOOK_ROOT.resolve()).as_posix()


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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
        if visual_calls == 0:
            findings.append({"check": "missing-visual-save", "path": _relative(path), "message": "Notebook has no visual generation call."})
        if display_calls == 0:
            findings.append({"check": "missing-display", "path": _relative(path), "message": "Notebook does not display generated artifacts."})
    return findings


def image_findings(min_width: int, min_height: int, blank_stddev: float) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    findings = []
    stats = []
    by_hash: dict[str, list[str]] = {}
    for entry in ENTRIES:
        topic = str(entry["artifact"])
        root = BOOK_ROOT / "artifacts" / topic
        pngs = sorted(root.rglob("*.png")) if root.exists() else []
        if not pngs:
            findings.append({"check": "missing-topic-png", "path": f"artifacts/{topic}", "message": "No PNG artifacts were generated for this topic."})
            continue
        for path in pngs:
            try:
                with Image.open(path) as image:
                    rgb = image.convert("RGB")
                    stat = ImageStat.Stat(rgb)
                    item = {
                        "path": _relative(path),
                        "width": image.width,
                        "height": image.height,
                        "bytes": path.stat().st_size,
                        "max_channel_stddev": max(stat.stddev),
                        "sha256": _sha(path),
                    }
            except OSError as exc:
                findings.append({"check": "unreadable-image", "path": _relative(path), "message": str(exc)})
                continue
            stats.append(item)
            by_hash.setdefault(item["sha256"], []).append(item["path"])
            if item["width"] < min_width or item["height"] < min_height:
                findings.append({"check": "tiny-image", "path": item["path"], "message": f"{item['width']}x{item['height']} is below threshold."})
            if item["max_channel_stddev"] <= blank_stddev:
                findings.append({"check": "blank-image", "path": item["path"], "message": "PNG appears blank or nearly constant."})
    for digest, paths in by_hash.items():
        if len(paths) > 1:
            findings.append({"check": "duplicate-png-hash", "path": paths[0], "message": f"Duplicate PNG hash also at {paths[1:]}", "details": {"sha256": digest}})
    return findings, stats


def audit_visuals(book_root: Path = BOOK_ROOT, *, min_width: int = 64, min_height: int = 64, blank_stddev: float = 1.0) -> dict[str, Any]:
    findings = notebook_findings()
    img_findings, stats = image_findings(min_width, min_height, blank_stddev)
    findings.extend(img_findings)
    return {"findings": findings, "image_stats": stats}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit_visuals()
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(report['image_stats'])} PNG artifacts")
    if report["findings"]:
        for finding in report["findings"]:
            print(f"- {finding['check']} {finding['path']}: {finding['message']}")
        raise SystemExit(1)
    print("Visual audit passed: notebooks generate/display artifacts and PNGs are nonblank.")


if __name__ == "__main__":
    main()
