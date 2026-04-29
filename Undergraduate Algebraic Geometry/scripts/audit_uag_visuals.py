"""Audit UAG generated visuals and artifact integrity."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import nbformat
import numpy as np
from PIL import Image

import uag_inventory as inventory


BOOK_ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def png_stats(path: Path) -> dict[str, object]:
    image = Image.open(path).convert("RGB")
    arr = np.asarray(image, dtype=float)
    return {
        "path": path,
        "width": image.width,
        "height": image.height,
        "pixel_std": float(arr.std()),
        "size": path.stat().st_size,
        "sha": sha256(path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-width", type=int, default=300)
    parser.add_argument("--min-height", type=int, default=240)
    parser.add_argument("--min-std", type=float, default=2.0)
    args = parser.parse_args()
    failures: list[str] = []
    all_hashes: dict[str, list[Path]] = {}
    for entry in inventory.ENTRIES:
        artifact_root = BOOK_ROOT / "artifacts" / str(entry["artifact"])
        pngs = sorted((artifact_root / "figures").glob("*.png"))
        if len(pngs) < 4:
            failures.append(f"{artifact_root.relative_to(BOOK_ROOT)} has only {len(pngs)} PNG figures")
        for png in pngs:
            stats = png_stats(png)
            all_hashes.setdefault(str(stats["sha"]), []).append(png)
            if stats["width"] < args.min_width or stats["height"] < args.min_height:
                failures.append(f"{png.relative_to(BOOK_ROOT)} is too small: {stats['width']}x{stats['height']}")
            if stats["pixel_std"] < args.min_std:
                failures.append(f"{png.relative_to(BOOK_ROOT)} appears blank: std={stats['pixel_std']:.3f}")
        htmls = sorted((artifact_root / "html").glob("*.html"))
        if not htmls:
            failures.append(f"{artifact_root.relative_to(BOOK_ROOT)} has no HTML lab artifact")
        checks = sorted((artifact_root / "checks").glob("*.json"))
        if not checks:
            failures.append(f"{artifact_root.relative_to(BOOK_ROOT)} has no JSON check artifact")
        notebook = BOOK_ROOT / str(entry["folder"]) / str(entry["notebook"])
        nb = nbformat.read(notebook, as_version=4)
        code = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "code")
        if "display_artifact(" not in code:
            failures.append(f"{notebook.relative_to(BOOK_ROOT)} does not display artifacts")
    duplicates = [paths for paths in all_hashes.values() if len(paths) > 1]
    for paths in duplicates:
        joined = ", ".join(str(path.relative_to(BOOK_ROOT)) for path in paths)
        failures.append(f"duplicate PNG hash: {joined}")
    print(f"Audited visuals for {len(inventory.ENTRIES)} entries.")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print("All visual artifacts are present, nonblank, and uniquely rendered.")


if __name__ == "__main__":
    main()
