"""Audit Pressley notebook visual calls and generated PNG artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = BOOK_ROOT / "scripts"
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import pressley_inventory as inventory  # noqa: E402
from utils.validation import discover_notebooks, image_stats, notebook_stats  # noqa: E402


def audit_visuals(book_root: Path = BOOK_ROOT) -> dict[str, object]:
    findings = []
    notebook_reports = []
    for path in discover_notebooks(book_root):
        stats = notebook_stats(path, book_root)
        notebook_reports.append(stats.__dict__)
        if stats.visual_generation_calls < 1:
            findings.append({"check": "missing-visual-generation", "path": stats.path, "message": "Notebook does not generate or build visual artifacts."})
        if stats.display_artifact_calls < 1:
            findings.append({"check": "missing-display-artifact", "path": stats.path, "message": "Notebook does not display generated artifacts inline."})
    image_reports = []
    hashes: dict[str, list[str]] = {}
    for entry in inventory.ENTRIES:
        topic = entry["artifact"]
        topic_root = book_root / "artifacts" / str(topic)
        pngs = sorted(topic_root.rglob("*.png")) if topic_root.exists() else []
        if not pngs:
            findings.append({"check": "missing-topic-png", "path": f"artifacts/{topic}", "message": "No PNG visual artifact found for unit."})
        for png in pngs:
            try:
                stats = image_stats(png, book_root)
            except Exception as exc:  # pragma: no cover
                findings.append({"check": "unreadable-png", "path": png.as_posix(), "message": str(exc)})
                continue
            image_reports.append(stats)
            if stats["width"] < 64 or stats["height"] < 64:
                findings.append({"check": "tiny-image", "path": stats["path"], "message": "PNG is too small."})
            if stats["max_channel_stddev"] <= 1.0:
                findings.append({"check": "blank-image", "path": stats["path"], "message": "PNG appears blank."})
            hashes.setdefault(str(stats["sha256"]), []).append(str(stats["path"]))
    for digest, paths in hashes.items():
        if len(paths) > 1:
            findings.append({"check": "duplicate-png-hash", "path": paths[0], "message": f"{len(paths)} PNG files share {digest[:12]}", "details": paths})
    return {
        "summary": {"notebook_count": len(notebook_reports), "png_count": len(image_reports), "finding_count": len(findings)},
        "findings": findings,
        "notebooks": notebook_reports,
        "images": image_reports,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-fail", action="store_true")
    args = parser.parse_args()
    report = audit_visuals()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        summary = report["summary"]
        print(f"Audited {summary['notebook_count']} notebooks and {summary['png_count']} PNGs")
        if report["findings"]:
            for finding in report["findings"]:
                print(f"- {finding['check']} [{finding.get('path', '')}]: {finding['message']}")
        else:
            print("All Pressley visual audit checks passed.")
    if report["summary"]["finding_count"] and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
