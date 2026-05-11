from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

import ppg_inventory as inv

BOOK_ROOT = Path(__file__).resolve().parents[1]


def raster_ok(path: Path) -> tuple[bool, str]:
    image = Image.open(path).convert("RGB")
    extrema = image.getextrema()
    varied = any(lo != hi for lo, hi in extrema)
    if image.width < 200 or image.height < 150:
        return False, "image too small"
    if not varied:
        return False, "image appears blank"
    return True, "ok"


def main() -> None:
    failures: list[str] = []
    total = 0
    png_hashes: dict[str, Path] = {}
    for chapter in inv.CHAPTERS:
        root = inv.artifact_root(chapter)
        storyboard = root / "checks" / "storyboard.json"
        visual_checks = root / "checks" / "visual-checks.json"
        final_sanity = root / "checks" / "final-sanity.json"
        for required in [storyboard, visual_checks, final_sanity]:
            if not required.exists():
                failures.append(f"missing {required.relative_to(BOOK_ROOT)}")
            elif required.suffix == ".json":
                raw_required = required.read_text(encoding="utf-8")
                if ":\\\\" in raw_required or "D:/" in raw_required or "D:\\" in raw_required:
                    failures.append(f"{required.relative_to(BOOK_ROOT)} contains absolute paths")
        artifacts = list((root / "figures").glob("*.png")) + list((root / "html").glob("*.html")) + list((root / "tables").glob("*.csv"))
        if len(artifacts) < 5:
            failures.append(f"{root.relative_to(BOOK_ROOT)} has only {len(artifacts)} visual artifacts")
        for path in artifacts:
            total += 1
            if path.stat().st_size < 256:
                failures.append(f"{path.relative_to(BOOK_ROOT)} is too small")
            if path.suffix.lower() == ".png":
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                if digest in png_hashes:
                    failures.append(
                        f"{path.relative_to(BOOK_ROOT)} duplicates {png_hashes[digest].relative_to(BOOK_ROOT)}"
                    )
                else:
                    png_hashes[digest] = path
                ok, reason = raster_ok(path)
                if not ok:
                    failures.append(f"{path.relative_to(BOOK_ROOT)} failed raster check: {reason}")
        if visual_checks.exists():
            raw = visual_checks.read_text(encoding="utf-8")
            data = json.loads(raw)
            if not data.get("all_files_exist"):
                failures.append(f"{visual_checks.relative_to(BOOK_ROOT)} reports missing files")
            cross_ratio_error = data.get("cross_ratio_error")
            if cross_ratio_error is None:
                cross_ratio_error = data.get("numeric_checks", {}).get("complex_cross_ratio_residual", 1)
            if cross_ratio_error > 1e-9:
                failures.append(f"{visual_checks.relative_to(BOOK_ROOT)} cross-ratio check is too large")
    print(f"Audited {total} visual artifacts across {len(inv.CHAPTERS)} chapters.")
    if failures:
        for failure in failures:
            print("FAIL:", failure)
        raise SystemExit(1)
    print("All visual artifacts are present, nonblank, and linked to checks.")


if __name__ == "__main__":
    main()
