"""Check generated images and HTML visuals for basic integrity."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))

from utils.course_manifest import CHAPTERS


def image_stats(path: Path) -> dict[str, object]:
    with Image.open(path) as img:
        arr = np.asarray(img.convert("RGB"))
    return {
        "width": int(arr.shape[1]),
        "height": int(arr.shape[0]),
        "std": float(arr.std()),
        "unique_sample": int(len(np.unique(arr.reshape(-1, 3)[:: max(1, arr.size // 50000)], axis=0))),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    findings = []
    records = []
    hashes: dict[str, str] = {}
    for chapter in CHAPTERS:
        for filename in chapter.visuals:
            subdir = "interactive" if filename.endswith(".html") else "figures"
            path = BOOK_ROOT / "artifacts" / chapter.key / subdir / filename
            if not path.exists():
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest in hashes:
                findings.append({"path": str(path.relative_to(BOOK_ROOT)), "message": f"duplicate artifact bytes with {hashes[digest]}"})
            hashes[digest] = str(path.relative_to(BOOK_ROOT))
            if path.suffix.lower() == ".html":
                text = path.read_text(encoding="utf-8", errors="ignore")
                if "Plotly" not in text and "plotly" not in text:
                    findings.append({"path": str(path.relative_to(BOOK_ROOT)), "message": "HTML visual does not look like a Plotly artifact"})
                records.append({"path": str(path.relative_to(BOOK_ROOT)), "kind": "html", "size": path.stat().st_size})
            else:
                stats = image_stats(path)
                records.append({"path": str(path.relative_to(BOOK_ROOT)), "kind": "image", **stats})
                if stats["width"] < 300 or stats["height"] < 250:
                    findings.append({"path": str(path.relative_to(BOOK_ROOT)), "message": "image dimensions are too small"})
                if stats["std"] < 5 or stats["unique_sample"] < 10:
                    findings.append({"path": str(path.relative_to(BOOK_ROOT)), "message": "image appears blank or nearly constant"})
    report = {"visual_count": len(records), "findings": findings, "records": records}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(records)} visuals")
    if findings:
        for item in findings:
            print(f"- {item['path']}: {item['message']}")
        raise SystemExit(1)
    print("All image/HTML visuals passed integrity checks.")


if __name__ == "__main__":
    main()
