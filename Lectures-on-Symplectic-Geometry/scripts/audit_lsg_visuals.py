"""Audit generated LSG visual artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageStat

SCRIPT_DIR = Path(__file__).resolve().parent
BOOK_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lsg_inventory import ENTRIES


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_stats(path: Path) -> dict[str, object]:
    with Image.open(path) as image:
        image.load()
        width, height = image.size
        stat = ImageStat.Stat(image.convert("RGB"))
    return {
        "path": path.relative_to(BOOK_ROOT).as_posix(),
        "width": width,
        "height": height,
        "bytes": path.stat().st_size,
        "max_stddev": max(stat.stddev),
        "sha256": sha256(path),
    }


def final_sanity_passed(data: dict[str, object]) -> bool:
    if "passed" in data:
        return bool(data.get("passed"))
    assertions = data.get("assertions")
    if isinstance(assertions, dict):
        return all(bool(value) for value in assertions.values())
    diagnostic = data.get("diagnostic")
    if isinstance(diagnostic, dict):
        return bool(diagnostic.get("passed"))
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    findings: list[dict[str, object]] = []
    stats: list[dict[str, object]] = []
    hashes: dict[str, list[str]] = {}
    for entry in ENTRIES:
        topic_root = BOOK_ROOT / "artifacts" / str(entry["artifact_topic"])
        pngs = sorted(topic_root.rglob("*.png"))
        final = topic_root / "checks" / "final-sanity.json"
        if len(pngs) < 2:
            findings.append({"path": topic_root.relative_to(BOOK_ROOT).as_posix(), "check": "missing-pngs", "message": "Expected at least concept and primary PNG artifacts."})
        if not final.exists():
            findings.append({"path": topic_root.relative_to(BOOK_ROOT).as_posix(), "check": "missing-final-sanity", "message": "Missing final-sanity.json."})
        else:
            data = json.loads(final.read_text(encoding="utf-8"))
            if not final_sanity_passed(data):
                findings.append({"path": final.relative_to(BOOK_ROOT).as_posix(), "check": "failed-final-sanity", "message": "Recorded diagnostic/assertions did not pass."})
        for png in pngs:
            item = png_stats(png)
            stats.append(item)
            hashes.setdefault(str(item["sha256"]), []).append(str(item["path"]))
            if item["width"] < 300 or item["height"] < 240:
                findings.append({"path": item["path"], "check": "small-image", "message": f"Image is only {item['width']}x{item['height']}."})
            if item["max_stddev"] < 1.0:
                findings.append({"path": item["path"], "check": "blank-image", "message": "Image appears nearly constant."})
    for digest, paths in hashes.items():
        if len(paths) > 1:
            findings.append({"path": paths[0], "check": "duplicate-png-hash", "message": "Duplicate PNG hash.", "matches": paths})

    report = {"png_count": len(stats), "finding_count": len(findings), "findings": findings, "stats": stats}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(stats)} PNG artifacts")
    if findings:
        for finding in findings:
            print(f"- {finding['check']}: {finding['path']} - {finding['message']}")
        raise SystemExit(1)
    print("All visual artifacts passed basic integrity checks.")


if __name__ == "__main__":
    main()
