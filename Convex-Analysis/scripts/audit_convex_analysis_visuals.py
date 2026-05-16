"""Audit Convex Analysis artifact presence, size, and duplicate hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = BOOK_ROOT.parent
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.section_catalog import sections  # noqa: E402
from utils.validation import relative  # noqa: E402


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_paths(section: dict[str, object]) -> list[Path]:
    root = BOOK_ROOT / "artifacts" / str(section["artifact_key"])
    slug = str(section["slug"])
    return [
        root / "figures" / f"{slug}-primary-visual.png",
        root / "figures" / f"{slug}-dependency-map.png",
        root / "checks" / f"{slug}-checks.json",
        root / "tables" / f"{slug}-inspection-targets.csv",
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-bytes", type=int, default=64)
    args = parser.parse_args()

    findings: list[dict[str, object]] = []
    hashes: dict[str, list[str]] = {}
    checked = 0
    for section in sections():
        for path in expected_paths(section):
            checked += 1
            rel = relative(path, WORKSPACE_ROOT)
            if not path.exists():
                findings.append({"path": rel, "finding": "missing artifact"})
                continue
            size = path.stat().st_size
            if size < args.min_bytes:
                findings.append({"path": rel, "finding": f"artifact too small: {size} bytes"})
            if path.suffix.lower() == ".png":
                hashes.setdefault(digest(path), []).append(rel)
            if path.name.endswith("-checks.json"):
                data = json.loads(path.read_text(encoding="utf-8"))
                if not data.get("primary_invariant_ok", False):
                    findings.append({"path": rel, "finding": "primary invariant check is false"})

    for paths in hashes.values():
        if len(paths) > 1:
            findings.append({"path": ", ".join(paths), "finding": "duplicate PNG hash"})

    report = {"artifact_count": checked, "finding_count": len(findings), "findings": findings}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Audited {checked} expected Convex Analysis artifacts")
        if findings:
            print(f"{len(findings)} finding(s):")
            for finding in findings:
                print(f"- {finding['path']}: {finding['finding']}")
        else:
            print("All expected artifacts are present, nonempty, unique where checked, and invariant-positive.")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

