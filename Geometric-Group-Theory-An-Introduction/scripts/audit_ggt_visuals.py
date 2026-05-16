"""Audit generated visual artifacts for the geometric group theory course."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

BOOK_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from ggt_inventory import ENTRIES  # noqa: E402


@dataclass(frozen=True)
class ImageStats:
    path: str
    width: int
    height: int
    bytes: int
    sha256: str
    max_channel_stddev: float


def _relative(path: Path) -> str:
    return path.relative_to(BOOK_ROOT).as_posix()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_stats(path: Path) -> ImageStats:
    with Image.open(path) as image:
        image.load()
        width, height = image.size
        stat = ImageStat.Stat(image.convert("RGB"))
    return ImageStats(
        path=_relative(path),
        width=width,
        height=height,
        bytes=path.stat().st_size,
        sha256=_sha256(path),
        max_channel_stddev=max(stat.stddev) if stat.stddev else 0.0,
    )


def audit() -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    image_items: list[ImageStats] = []
    artifact_root = BOOK_ROOT / "artifacts"
    for entry in ENTRIES:
        unit = str(entry["artifact"])
        unit_root = artifact_root / unit
        pngs = sorted(unit_root.rglob("*.png")) if unit_root.exists() else []
        htmls = sorted(unit_root.rglob("*.html")) if unit_root.exists() else []
        checks = sorted(unit_root.rglob("*.json")) if unit_root.exists() else []
        if len(pngs) < 2:
            findings.append({"check": "few-pngs", "path": _relative(unit_root), "message": f"{unit} has fewer than two PNG artifacts."})
        if not htmls:
            findings.append({"check": "missing-html", "path": _relative(unit_root), "message": f"{unit} has no interactive HTML artifact."})
        if len(checks) < 2:
            findings.append({"check": "missing-json-checks", "path": _relative(unit_root), "message": f"{unit} has fewer than two JSON check artifacts."})
        for html in htmls:
            if html.stat().st_size < 1024:
                findings.append({"check": "tiny-html", "path": _relative(html), "message": "Interactive HTML is unexpectedly small."})
        for png in pngs:
            try:
                item = image_stats(png)
            except OSError as exc:
                findings.append({"check": "unreadable-image", "path": _relative(png), "message": str(exc)})
                continue
            image_items.append(item)
            if item.width < 160 or item.height < 120:
                findings.append({"check": "tiny-image", "path": item.path, "message": f"Image is too small: {item.width}x{item.height}."})
            if item.max_channel_stddev <= 1.0:
                findings.append({"check": "blank-image", "path": item.path, "message": "Image appears blank or nearly constant."})
    by_hash: dict[str, list[ImageStats]] = {}
    for item in image_items:
        by_hash.setdefault(item.sha256, []).append(item)
    for digest, matches in by_hash.items():
        if len(matches) > 1:
            findings.append(
                {
                    "check": "duplicate-image",
                    "path": ", ".join(item.path for item in matches),
                    "message": f"{len(matches)} PNG artifacts share the same hash {digest[:12]}.",
                }
            )
    return {
        "image_count": len(image_items),
        "findings_count": len(findings),
        "findings": findings,
        "images": [asdict(item) for item in image_items],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit()
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {report['image_count']} PNG artifacts")
    if report["findings"]:
        print(f"{len(report['findings'])} visual audit findings:")
        for item in report["findings"]:
            print(f"- {item['check']} {item['path']}: {item['message']}")
        raise SystemExit(1)
    print("Visual artifacts are present, readable, nonblank, and nonduplicate.")


if __name__ == "__main__":
    main()

