"""Audit Geometry I notebooks and generated visual artifacts."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

BOOK_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = Path(__file__).resolve().parent
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import geometry_i_inventory as inventory  # noqa: E402
from utils.validation import canonical_notebooks, code_sources, image_report, relative  # noqa: E402

VISUAL_SAVE_CALLS = {"save_image", "save_matplotlib", "save_plotly_html", "build_visual_suite"}


def call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def notebook_visual_stats(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    save_calls = 0
    display_calls = 0
    findings: list[dict[str, Any]] = []
    for index, source in enumerate(code_sources(path), start=1):
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            findings.append({"check": "parse-error", "path": relative(path), "message": f"cell {index}: {exc.msg}"})
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = call_name(node)
                if name in VISUAL_SAVE_CALLS:
                    save_calls += 1
                if name == "display_artifact":
                    display_calls += 1
    if save_calls == 0:
        findings.append({"check": "missing-visual-builder", "path": relative(path), "message": "Notebook has no visual save or builder call."})
    if display_calls == 0:
        findings.append({"check": "missing-display", "path": relative(path), "message": "Notebook does not display generated artifacts."})
    return {"path": relative(path), "visual_save_calls": save_calls, "display_artifact_calls": display_calls}, findings


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_pngs(min_width: int, min_height: int, min_pixels: int, blank_stddev: float) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    findings: list[dict[str, Any]] = []
    stats: list[dict[str, Any]] = []
    hash_to_paths: dict[str, list[str]] = defaultdict(list)
    for entry in inventory.ENTRIES:
        topic_root = BOOK_ROOT / "artifacts" / entry["artifact_topic"]
        pngs = sorted(topic_root.rglob("*.png"))
        if not pngs:
            findings.append({"check": "missing-topic-png", "path": relative(topic_root), "message": "No PNG artifact found for source unit."})
            continue
        for path in pngs:
            report = image_report(path)
            report["sha256"] = sha256(path)
            stats.append(report)
            hash_to_paths[str(report["sha256"])].append(str(report["path"]))
            if report["width"] < min_width or report["height"] < min_height or report["width"] * report["height"] < min_pixels:
                findings.append({"check": "tiny-image", "path": report["path"], "message": f"Image dimensions too small: {report}"})
            if report["max_channel_stddev"] < blank_stddev:
                findings.append({"check": "blank-image", "path": report["path"], "message": f"Image appears blank: {report}"})
    for digest, paths in hash_to_paths.items():
        if len(paths) > 1:
            findings.append({"check": "duplicate-png", "path": paths[0], "message": f"Duplicate PNG hash {digest}: {paths}"})
    return stats, findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-width", type=int, default=160)
    parser.add_argument("--min-height", type=int, default=120)
    parser.add_argument("--min-pixels", type=int, default=20_000)
    parser.add_argument("--blank-stddev", type=float, default=1.0)
    args = parser.parse_args()

    notebook_stats = []
    findings: list[dict[str, Any]] = []
    for notebook in canonical_notebooks(BOOK_ROOT):
        stats, notebook_findings = notebook_visual_stats(notebook)
        notebook_stats.append(stats)
        findings.extend(notebook_findings)
    png_stats, png_findings = audit_pngs(args.min_width, args.min_height, args.min_pixels, args.blank_stddev)
    findings.extend(png_findings)
    report = {
        "notebooks": notebook_stats,
        "png_count": len(png_stats),
        "pngs": png_stats,
        "finding_count": len(findings),
        "findings": findings,
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Audited {len(notebook_stats)} notebooks and {len(png_stats)} PNG artifacts")
        if findings:
            for finding in findings:
                print(f"- {finding['check']}: {finding['path']} - {finding['message']}")
        else:
            print("All visual checks passed.")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

