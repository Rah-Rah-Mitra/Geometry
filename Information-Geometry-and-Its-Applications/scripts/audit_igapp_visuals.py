"""Audit generated visual artifacts for Information Geometry."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

import igapp_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}
VISUAL_SAVE_CALLS = {"save_matplotlib", "save_plotly_html", "save_image"}


def relative(path: Path) -> str:
    return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


def call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def notebook_visual_stats(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    visual_saves = 0
    displays = 0
    outputs = 0
    errors = []
    for cell_index, cell in enumerate(data.get("cells", []), start=1):
        if cell.get("cell_type") != "code":
            continue
        outputs += len(cell.get("outputs", []))
        source = "".join(cell.get("source", ""))
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            errors.append(f"cell {cell_index}: {exc.msg}")
            visual_saves += sum(source.count(f"{name}(") for name in VISUAL_SAVE_CALLS)
            displays += source.count("display_artifact(")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = call_name(node)
                if name in VISUAL_SAVE_CALLS:
                    visual_saves += 1
                elif name in {"display_artifact", "display", "Image", "HTML", "IFrame"}:
                    displays += 1
        visual_saves += source.count(".savefig(") + source.count(".write_html(")
    return {"path": relative(path), "visual_save_calls": visual_saves, "display_artifact_calls": displays, "output_count": outputs, "parse_errors": errors}


def entry_for_path(path: Path) -> dict | None:
    for entry in inventory.ENTRIES:
        if path == BOOK_ROOT / entry["part"] / entry["folder"] / entry["notebook"]:
            return entry
    return None


def topic_visual_count(entry: dict | None) -> int:
    if entry is None:
        return 0
    root = BOOK_ROOT / "artifacts" / entry["topic"]
    if not root.exists():
        return 0
    return len(list(root.rglob("*.png"))) + len(list(root.rglob("*.jpg"))) + len(list(root.rglob("*.jpeg"))) + len(list(root.rglob("*.svg"))) + len(list(root.rglob("*.html")))


def image_stats(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
    return {
        "path": relative(path),
        "width": rgb.width,
        "height": rgb.height,
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "max_channel_stddev": max(stat.stddev) if stat.stddev else 0.0,
    }


def audit() -> dict[str, Any]:
    findings = []
    artifact_root = BOOK_ROOT / "artifacts"
    notebooks = [
        notebook_visual_stats(path)
        for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED
    ]
    for item in notebooks:
        for error in item["parse_errors"]:
            findings.append({"check": "notebook-parse-error", "path": item["path"], "message": error})
        artifact_count = topic_visual_count(entry_for_path(BOOK_ROOT / item["path"]))
        if item["visual_save_calls"] == 0 and artifact_count == 0:
            findings.append({"check": "missing-visual-save", "path": item["path"], "message": "no visual save call"})
        if item["display_artifact_calls"] == 0 and item["output_count"] == 0:
            findings.append({"check": "missing-display", "path": item["path"], "message": "no visible display call or executed output"})

    images = []
    for entry in inventory.ENTRIES:
        topic_root = artifact_root / entry["topic"]
        pngs = sorted(topic_root.rglob("*.png")) if topic_root.exists() else []
        if not pngs:
            findings.append({"check": "missing-topic-png", "path": relative(topic_root), "message": f"{entry['topic']} has no PNG artifacts"})
        for path in pngs:
            try:
                stat = image_stats(path)
            except OSError as exc:
                findings.append({"check": "unreadable-image", "path": relative(path), "message": str(exc)})
                continue
            images.append(stat)
            if stat["width"] < 96 or stat["height"] < 96 or stat["bytes"] < 1500:
                findings.append({"check": "tiny-image", "path": stat["path"], "message": f"{stat['width']}x{stat['height']} {stat['bytes']} bytes"})
            if stat["max_channel_stddev"] <= 1.0:
                findings.append({"check": "blank-image", "path": stat["path"], "message": f"stddev {stat['max_channel_stddev']:.3f}"})

    by_hash: dict[str, list[str]] = {}
    for image in images:
        by_hash.setdefault(image["sha256"], []).append(image["path"])
    for digest, paths in by_hash.items():
        if len(paths) > 1:
            findings.append({"check": "duplicate-png-hash", "path": paths[0], "message": f"{len(paths)} images share {digest[:12]}", "details": paths})

    return {"summary": {"notebook_count": len(notebooks), "png_count": len(images), "finding_count": len(findings)}, "findings": findings, "notebooks": notebooks, "images": images}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-fail", action="store_true")
    args = parser.parse_args()
    report = audit()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        summary = report["summary"]
        print(f"Audited {summary['notebook_count']} notebooks and {summary['png_count']} PNGs")
        if report["findings"]:
            for finding in report["findings"]:
                print(f"- {finding['check']} [{finding.get('path', '')}]: {finding['message']}")
        else:
            print("All Information Geometry visual checks passed.")
    if report["findings"] and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
