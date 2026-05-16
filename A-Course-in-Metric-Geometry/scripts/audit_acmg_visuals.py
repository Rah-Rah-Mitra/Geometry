"""Audit ACMG visual artifacts and notebook display calls."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import artifact_topics, canonical_notebooks, code_sources, image_stats, relative  # noqa: E402

VISUAL_SAVE_CALLS = {"save_matplotlib", "save_plotly_html"}


def call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def notebook_visual_stats(path: Path) -> dict[str, Any]:
    saves = 0
    displays = 0
    parse_errors = []
    for source in code_sources(path):
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            parse_errors.append(str(exc))
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = call_name(node)
                if name in VISUAL_SAVE_CALLS:
                    saves += 1
                if name == "display_artifact":
                    displays += 1
    return {"path": relative(path), "visual_save_calls": saves, "display_artifact_calls": displays, "parse_errors": parse_errors}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-width", type=int, default=64)
    parser.add_argument("--min-height", type=int, default=64)
    parser.add_argument("--blank-stddev", type=float, default=1.0)
    args = parser.parse_args()

    findings = []
    notebook_stats = [notebook_visual_stats(path) for path in canonical_notebooks(BOOK_ROOT)]
    for item in notebook_stats:
        if item["parse_errors"]:
            findings.append({"check": "parse-error", **item})
        if item["visual_save_calls"] == 0:
            findings.append({"check": "missing-visual-save", **item})
        if item["display_artifact_calls"] == 0:
            findings.append({"check": "missing-display-artifact", **item})

    images = []
    by_hash: dict[str, list[str]] = {}
    for topic in artifact_topics():
        topic_root = BOOK_ROOT / "artifacts" / topic
        pngs = sorted(topic_root.rglob("*.png")) if topic_root.exists() else []
        if not pngs:
            findings.append({"check": "missing-topic-png", "path": relative(topic_root, BOOK_ROOT)})
        for png in pngs:
            item = image_stats(png)
            item["sha256"] = sha256(png)
            images.append(item)
            by_hash.setdefault(item["sha256"], []).append(item["path"])
            if item["width"] < args.min_width or item["height"] < args.min_height:
                findings.append({"check": "tiny-image", **item})
            if item["max_channel_stddev"] <= args.blank_stddev:
                findings.append({"check": "blank-image", **item})
    for digest, paths in by_hash.items():
        if len(paths) > 1:
            findings.append({"check": "duplicate-png-hash", "sha256": digest, "paths": paths})

    report = {
        "summary": {"notebook_count": len(notebook_stats), "png_count": len(images), "finding_count": len(findings)},
        "findings": findings,
        "notebooks": notebook_stats,
        "images": images,
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Audited {len(notebook_stats)} notebooks and {len(images)} PNGs")
        if findings:
            print(f"{len(findings)} finding(s):")
            for finding in findings:
                print(f"- {finding['check']}: {finding.get('path', finding.get('paths', ''))}")
        else:
            print("All ACMG visual audit checks passed.")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

