"""Audit generated visual artifacts for the GDL course."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

import gdl_inventory as inventory

BOOK_ROOT = inventory.BOOK_ROOT


def rel(path: Path) -> str:
    return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


def image_stats(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
    return {
        "path": rel(path),
        "width": rgb.width,
        "height": rgb.height,
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "max_channel_stddev": max(stat.stddev) if stat.stddev else 0.0,
    }


def audit() -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    artifact_root = BOOK_ROOT / "artifacts"
    images: list[dict[str, Any]] = []
    html_count = 0
    json_count = 0

    for entry in inventory.ENTRIES:
        topic_root = artifact_root / inventory.chapter_topic(int(entry["chapter"]))
        pngs = sorted(topic_root.rglob("*.png")) if topic_root.exists() else []
        svgs = sorted(topic_root.rglob("*.svg")) if topic_root.exists() else []
        htmls = sorted(topic_root.rglob("*.html")) if topic_root.exists() else []
        jsons = sorted(topic_root.rglob("*.json")) if topic_root.exists() else []
        html_count += len(htmls)
        json_count += len(jsons)
        if len(pngs) + len(svgs) + len(htmls) < 3:
            findings.append(
                {
                    "check": "too-few-visual-artifacts",
                    "path": rel(topic_root),
                    "message": "expected at least three visual artifacts for a visualization-first chapter",
                }
            )
        if not jsons:
            findings.append({"check": "missing-check-json", "path": rel(topic_root), "message": "no JSON checks found"})
        for path in pngs:
            try:
                stat = image_stats(path)
            except OSError as exc:
                findings.append({"check": "unreadable-image", "path": rel(path), "message": str(exc)})
                continue
            images.append(stat)
            if stat["width"] < 96 or stat["height"] < 96 or stat["bytes"] < 1500:
                findings.append(
                    {
                        "check": "tiny-image",
                        "path": stat["path"],
                        "message": f"{stat['width']}x{stat['height']} {stat['bytes']} bytes",
                    }
                )
            if stat["max_channel_stddev"] <= 1.0:
                findings.append(
                    {
                        "check": "blank-image",
                        "path": stat["path"],
                        "message": f"stddev {stat['max_channel_stddev']:.3f}",
                    }
                )
    by_hash: dict[str, list[str]] = {}
    for image in images:
        by_hash.setdefault(image["sha256"], []).append(image["path"])
    for digest, paths in by_hash.items():
        if len(paths) > 1:
            findings.append(
                {
                    "check": "duplicate-png-hash",
                    "path": paths[0],
                    "message": f"{len(paths)} images share {digest[:12]}",
                    "details": paths,
                }
            )
    return {
        "summary": {
            "chapter_count": len(inventory.ENTRIES),
            "png_count": len(images),
            "html_count": html_count,
            "json_count": json_count,
            "finding_count": len(findings),
        },
        "findings": findings,
        "images": images,
    }


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
        print(
            f"Audited {summary['chapter_count']} chapters, {summary['png_count']} PNGs, "
            f"{summary['html_count']} HTML artifacts, and {summary['json_count']} JSON checks"
        )
        if report["findings"]:
            for finding in report["findings"]:
                print(f"- {finding['check']} [{finding.get('path', '')}]: {finding['message']}")
        else:
            print("All GDL visual checks passed.")
    if report["findings"] and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

