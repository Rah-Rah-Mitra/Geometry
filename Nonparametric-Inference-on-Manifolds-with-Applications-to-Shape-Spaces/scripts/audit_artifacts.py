"""Audit expected generated artifacts and numeric check files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))

from utils.course_manifest import CHAPTERS


def expected_path(chapter_key: str, filename: str) -> Path:
    subdir = "interactive" if filename.endswith(".html") else "figures"
    return BOOK_ROOT / "artifacts" / chapter_key / subdir / filename


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-bytes", type=int, default=500)
    args = parser.parse_args()

    findings = []
    records = []
    for chapter in CHAPTERS:
        for filename in chapter.visuals:
            path = expected_path(chapter.key, filename)
            if not path.exists():
                findings.append({"path": str(path.relative_to(BOOK_ROOT)), "message": "missing expected artifact"})
                continue
            size = path.stat().st_size
            records.append({"path": str(path.relative_to(BOOK_ROOT)), "size": size})
            if size < args.min_bytes:
                findings.append({"path": str(path.relative_to(BOOK_ROOT)), "message": f"artifact too small: {size} bytes"})
        for filename in ["numeric-checks.json", "final-sanity.json"]:
            path = BOOK_ROOT / "artifacts" / chapter.key / "checks" / filename
            if not path.exists():
                findings.append({"path": str(path.relative_to(BOOK_ROOT)), "message": "missing check file"})
                continue
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                findings.append({"path": str(path.relative_to(BOOK_ROOT)), "message": f"invalid JSON: {exc}"})
    report = {"artifact_count": len(records), "findings": findings, "records": records}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(records)} expected visual artifacts")
    if findings:
        for item in findings:
            print(f"- {item['path']}: {item['message']}")
        raise SystemExit(1)
    print("All expected artifacts and JSON checks are present.")


if __name__ == "__main__":
    main()
