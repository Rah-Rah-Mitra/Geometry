"""Audit IVA generated visual artifacts."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

import iva_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-index.ipynb", "00-book-index.ipynb"}
VISUAL_SAVE_CALLS = {"save_matplotlib", "save_plotly_html"}


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
    errors = []
    for cell_index, cell in enumerate(data.get("cells", []), start=1):
        if cell.get("cell_type") != "code":
            continue
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
                elif name == "display_artifact":
                    displays += 1
    return {"path": relative(path), "visual_save_calls": visual_saves, "display_artifact_calls": displays, "parse_errors": errors}


def image_stats(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "path": relative(path),
        "width": rgb.width,
        "height": rgb.height,
        "bytes": path.stat().st_size,
        "sha256": digest,
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
        if item["visual_save_calls"] == 0:
            findings.append({"check": "missing-visual-save", "path": item["path"], "message": "no visual save call"})
        if item["display_artifact_calls"] < item["visual_save_calls"]:
            findings.append({"check": "missing-display", "path": item["path"], "message": "not every visual is displayed"})

    images = []
    html_count = 0
    json_count = 0
    for entry in inventory.ENTRIES:
        topic_root = artifact_root / entry["artifact"]
        pngs = sorted(topic_root.rglob("*.png")) if topic_root.exists() else []
        htmls = sorted(topic_root.rglob("*.html")) if topic_root.exists() else []
        jsons = sorted(topic_root.rglob("*.json")) if topic_root.exists() else []
        if not pngs:
            findings.append({"check": "missing-topic-png", "path": relative(topic_root), "message": f"{entry['artifact']} has no PNG artifacts"})
        if not htmls:
            findings.append({"check": "missing-topic-html", "path": relative(topic_root), "message": f"{entry['artifact']} has no HTML artifact"})
        if not jsons:
            findings.append({"check": "missing-topic-json", "path": relative(topic_root), "message": f"{entry['artifact']} has no JSON check"})
        html_count += len(htmls)
        json_count += len(jsons)
        for html in htmls:
            html_text = html.read_text(encoding="utf-8", errors="ignore")
            if html.stat().st_size < 500:
                findings.append({"check": "tiny-html", "path": relative(html), "message": f"{html.stat().st_size} bytes"})
            if re.search(r"<script[^>]+src=[\"']https?://cdn\.plot\.ly", html_text, flags=re.IGNORECASE):
                findings.append({"check": "external-plotly-cdn", "path": relative(html), "message": "HTML depends on the Plotly CDN"})
        final_sanity = topic_root / "checks" / "final-sanity.json"
        if final_sanity.exists():
            data = json.loads(final_sanity.read_text(encoding="utf-8"))
            if data.get("topic") != entry["artifact"]:
                findings.append({"check": "wrong-topic-sanity", "path": relative(final_sanity), "message": f"expected topic {entry['artifact']}"})
            topic_checks = data.get("topic_checks", {})
            if topic_checks.get("topic") != entry["artifact"]:
                findings.append({"check": "missing-topic-checks", "path": relative(final_sanity), "message": "final sanity lacks matching topic_checks"})
        else:
            findings.append({"check": "missing-final-sanity", "path": relative(topic_root), "message": "missing checks/final-sanity.json"})
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
    return {"summary": {"notebook_count": len(notebooks), "png_count": len(images), "html_count": html_count, "json_count": json_count, "finding_count": len(findings)}, "findings": findings, "notebooks": notebooks, "images": images}


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
        print(f"Audited {summary['notebook_count']} notebooks, {summary['png_count']} PNGs, {summary['html_count']} HTML files, and {summary['json_count']} JSON files")
        if report["findings"]:
            for finding in report["findings"]:
                print(f"- {finding['check']} [{finding.get('path', '')}]: {finding['message']}")
        else:
            print("All IVA visual checks passed.")
    if report["findings"] and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
