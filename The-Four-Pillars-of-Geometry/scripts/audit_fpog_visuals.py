from __future__ import annotations

import argparse
import sys
from pathlib import Path

import fpog_inventory as inv

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import png_stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-width", type=int, default=300)
    parser.add_argument("--min-height", type=int, default=240)
    parser.add_argument("--min-std", type=float, default=2.0)
    args = parser.parse_args()
    failures: list[str] = []
    hashes: dict[str, list[Path]] = {}
    for chapter in inv.CHAPTERS:
        root = BOOK_ROOT / "artifacts" / chapter["artifact"]
        pngs = sorted((root / "figures").glob("*.png"))
        if len(pngs) < 5:
            failures.append(f"{root.relative_to(BOOK_ROOT)} has only {len(pngs)} PNG figures")
        for path in pngs:
            item = png_stats(path)
            hashes.setdefault(str(item["sha"]), []).append(path)
            if item["width"] < args.min_width or item["height"] < args.min_height:
                failures.append(f"{path.relative_to(BOOK_ROOT)} is too small: {item['width']}x{item['height']}")
            if item["pixel_std"] < args.min_std:
                failures.append(f"{path.relative_to(BOOK_ROOT)} appears blank: std={item['pixel_std']:.3f}")
        if not list((root / "html").glob("*.html")):
            failures.append(f"{root.relative_to(BOOK_ROOT)} has no HTML lab artifact")
        if len(list((root / "checks").glob("*.json"))) < 2:
            failures.append(f"{root.relative_to(BOOK_ROOT)} has too few JSON checks")
    for paths in hashes.values():
        if len(paths) > 1:
            failures.append("duplicate PNG hash: " + ", ".join(str(path.relative_to(BOOK_ROOT)) for path in paths))
    print(f"Audited visuals for {len(inv.CHAPTERS)} chapters.")
    if failures:
        for failure in failures:
            print("FAIL:", failure)
        raise SystemExit(1)
    print("All visual artifacts are present, nonblank, and uniquely rendered.")


if __name__ == "__main__":
    main()
