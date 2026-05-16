"""Audit generated visual artifacts for coverage, size, hashes, and checks."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.artifacts import chapter_artifact_dir
from utils.course_data import CHAPTERS
from utils.visuals import file_sha256


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-png-bytes", type=int, default=5000)
    parser.add_argument("--allow-duplicate-hashes", action="store_true")
    args = parser.parse_args()

    issues: list[str] = []
    hash_to_paths: dict[str, list[str]] = defaultdict(list)
    total_files = 0
    for chapter in CHAPTERS:
        base = chapter_artifact_dir(chapter, ROOT)
        if not base.exists():
            issues.append(f"{base}: missing artifact directory")
            continue
        pngs = sorted((base / "figures").glob("*.png"))
        checks = sorted((base / "checks").glob("*.json"))
        if len(pngs) < 2:
            issues.append(f"{base}: expected at least two PNG figures, found {len(pngs)}")
        if not (base / "checks" / "source-span.json").exists():
            issues.append(f"{base}: missing source-span.json")
        if not (base / "checks" / "visual-storyboard.json").exists():
            issues.append(f"{base}: missing visual-storyboard.json")
        if not (base / "checks" / "final-sanity.json").exists():
            issues.append(f"{base}: missing final-sanity.json")
        for path in [*pngs, *checks, *((base / "tables").glob("*.csv")), *((base / "interactive").glob("*.html"))]:
            total_files += 1
            if path.stat().st_size == 0:
                issues.append(f"{path}: zero-byte artifact")
            if path.suffix.lower() == ".png" and path.stat().st_size < args.min_png_bytes:
                issues.append(f"{path}: PNG size {path.stat().st_size} < {args.min_png_bytes}")
            if path.suffix.lower() == ".png":
                hash_to_paths[file_sha256(path)].append(path.relative_to(ROOT).as_posix())

    if not args.allow_duplicate_hashes:
        for digest, paths in hash_to_paths.items():
            if len(paths) > 1:
                issues.append(f"duplicate PNG hash {digest}: {paths}")

    report = {
        "chapters": len(CHAPTERS),
        "artifact_files": total_files,
        "issues": issues,
        "status": "pass" if not issues else "fail",
    }
    print(json.dumps(report, indent=2))
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

