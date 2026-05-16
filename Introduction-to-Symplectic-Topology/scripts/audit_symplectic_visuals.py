"""Audit generated visual artifacts and invariant check payloads."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.course_data import COURSE_UNITS


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    failures: list[str] = []
    hashes: dict[str, list[str]] = {}
    unit_reports = []
    for unit in COURSE_UNITS:
        check_path = BOOK_ROOT / "artifacts" / unit.slug / "checks" / "final-sanity.json"
        if not check_path.exists():
            failures.append(f"{unit.slug}: missing final-sanity.json")
            continue
        payload = json.loads(check_path.read_text(encoding="utf-8"))
        assertions = payload.get("assertions", {})
        if not assertions or not all(assertions.values()):
            failures.append(f"{unit.slug}: failed assertion in final-sanity.json")
        artifact_paths = [BOOK_ROOT / rel for rel in payload.get("visual_artifacts", [])]
        if not artifact_paths:
            failures.append(f"{unit.slug}: no visual artifacts recorded")
        for path in artifact_paths:
            if not path.exists():
                failures.append(f"{unit.slug}: missing artifact {path.relative_to(BOOK_ROOT)}")
                continue
            if path.stat().st_size < 1000:
                failures.append(f"{unit.slug}: tiny artifact {path.relative_to(BOOK_ROOT)}")
            hashes.setdefault(file_hash(path), []).append(path.relative_to(BOOK_ROOT).as_posix())
        unit_reports.append({"unit": unit.slug, "artifact_count": len(artifact_paths), "assertions": assertions})
    duplicates = {digest: paths for digest, paths in hashes.items() if len(paths) > 1}
    if duplicates:
        failures.append(f"duplicate artifact hashes: {duplicates}")
    report = {"unit_count": len(COURSE_UNITS), "failures": failures, "units": unit_reports}
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"Audited visual artifacts for {len(unit_reports)} units")
        if failures:
            print("Visual audit failures:")
            for failure in failures:
                print(f"- {failure}")
            raise SystemExit(1)
        print("All visual artifacts and invariant payloads passed.")


if __name__ == "__main__":
    main()
