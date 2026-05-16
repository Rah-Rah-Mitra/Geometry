"""Audit generated artifact files for Methods of Information Geometry."""

from __future__ import annotations

import json
from pathlib import Path

import mig_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"
VISUAL_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".html"}


def rel(path: Path) -> str:
    return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


def main() -> None:
    findings = []
    summary = {}
    for entry in inventory.ENTRIES:
        root = ARTIFACT_ROOT / entry["topic"]
        files = list(root.rglob("*")) if root.exists() else []
        visuals = [path for path in files if path.is_file() and path.suffix.lower() in VISUAL_EXTS]
        checks = [path for path in files if path.is_file() and path.suffix.lower() == ".json"]
        small = [path for path in visuals + checks if path.stat().st_size <= 100]
        summary[entry["topic"]] = {"visual_count": len(visuals), "check_count": len(checks)}
        if len(visuals) < 2:
            findings.append(f"{entry['topic']}: expected at least 2 visual artifacts, found {len(visuals)}")
        if not checks:
            findings.append(f"{entry['topic']}: missing JSON check artifact")
        for path in small:
            findings.append(f"{rel(path)}: artifact is unexpectedly small")
    print(json.dumps(summary, indent=2))
    if findings:
        for finding in findings:
            print(f"- {finding}")
        raise SystemExit(1)
    print("Artifact audit passed.")


if __name__ == "__main__":
    main()

