"""Audit Hartshorne Algebraic Geometry visual artifacts and checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import nbformat
import numpy as np
from PIL import Image


BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ag_inventory as inventory


GENERIC_NAMES = {
    "primary-visual.png",
    "secondary-visual-2.png",
    "secondary-visual-3.png",
    "interactive-lab.html",
}


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_json_error": str(exc)}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def relpath(path: Path) -> str:
    return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


def png_stats(path: Path) -> dict[str, object]:
    image = Image.open(path).convert("RGB")
    arr = np.asarray(image, dtype=float)
    return {
        "width": image.width,
        "height": image.height,
        "pixel_std": float(arr.std()),
        "size": path.stat().st_size,
        "sha": sha256(path),
    }


def visual_items(storyboard: object) -> list[object]:
    if isinstance(storyboard, dict):
        for key in ("visual_sequence", "visuals", "items"):
            value = storyboard.get(key)
            if isinstance(value, list):
                return value
    if isinstance(storyboard, list):
        return storyboard
    return []


def audit_entry(entry: dict[str, object], seen_hashes: dict[str, Path], args: argparse.Namespace) -> list[str]:
    failures: list[str] = []
    artifact_root = BOOK_ROOT / "artifacts" / str(entry["artifact"])
    rel_root = relpath(artifact_root)
    if not artifact_root.exists():
        return [f"{rel_root} is missing"]

    generic = sorted(path.name for path in artifact_root.rglob("*") if path.name in GENERIC_NAMES)
    if generic:
        failures.append(f"{rel_root} contains generic bootstrap artifact filenames: {', '.join(generic)}")

    pngs = sorted((artifact_root / "figures").glob("*.png"))
    htmls = sorted((artifact_root / "html").glob("*.html"))
    jsons = sorted((artifact_root / "checks").glob("*.json"))
    if len(pngs) < args.min_pngs:
        failures.append(f"{rel_root} has only {len(pngs)} PNG figures")
    if not htmls:
        failures.append(f"{rel_root} has no HTML exploration artifact")
    if not jsons:
        failures.append(f"{rel_root} has no JSON check artifact")

    for png in pngs:
        rel = relpath(png)
        try:
            stats = png_stats(png)
        except Exception as exc:
            failures.append(f"{rel} cannot be read as PNG: {exc}")
            continue
        if stats["width"] < args.min_width or stats["height"] < args.min_height:
            failures.append(f"{rel} is too small: {stats['width']}x{stats['height']}")
        if stats["pixel_std"] < args.min_std:
            failures.append(f"{rel} appears blank: std={stats['pixel_std']:.3f}")
        if stats["size"] < 1024:
            failures.append(f"{rel} is unexpectedly tiny: {stats['size']} bytes")
        digest = str(stats["sha"])
        if digest in seen_hashes:
            failures.append(f"{rel} duplicates {relpath(seen_hashes[digest])}")
        else:
            seen_hashes[digest] = png

    for html in htmls:
        rel = relpath(html)
        text = html.read_text(encoding="utf-8", errors="ignore")
        lower = text.lower()
        if len(text) < 600:
            failures.append(f"{rel} is too small to be a useful exploration")
        if "local generated lab" in lower:
            failures.append(f"{rel} contains generic HTML lab text")
        if not any(token in lower for token in ("plotly", "<input", "<svg", "<canvas", "<table")):
            failures.append(f"{rel} lacks an inspectable visual/control/table")

    storyboard_path = artifact_root / "checks" / "visual-storyboard.json"
    if not storyboard_path.exists():
        failures.append(f"{relpath(storyboard_path)} missing")
    else:
        storyboard = load_json(storyboard_path)
        items = visual_items(storyboard)
        if not items:
            failures.append(f"{relpath(storyboard_path)} has no visual sequence")
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                failures.append(f"{relpath(storyboard_path)} item {index} is not an object")
                continue
            missing = [key for key in ("concept", "artifact", "invariant") if not item.get(key)]
            if missing:
                failures.append(f"{relpath(storyboard_path)} item {index} missing {missing}")

    for required in ("source-coverage.json", "final-sanity.json"):
        path = artifact_root / "checks" / required
        if not path.exists():
            failures.append(f"{relpath(path)} missing")

    notebook = BOOK_ROOT / str(entry["folder"]) / str(entry["notebook"])
    nb = nbformat.read(notebook, as_version=4)
    code = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "code")
    if "display_artifact(" not in code:
        failures.append(f"{relpath(notebook)} does not display artifacts")

    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-width", type=int, default=300)
    parser.add_argument("--min-height", type=int, default=220)
    parser.add_argument("--min-std", type=float, default=2.0)
    parser.add_argument("--min-pngs", type=int, default=3)
    args = parser.parse_args()

    failures: list[str] = []
    seen_hashes: dict[str, Path] = {}
    for entry in inventory.ENTRIES:
        failures.extend(audit_entry(entry, seen_hashes, args))

    print(f"Audited visuals for {len(inventory.ENTRIES)} entries.")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print("All visual artifacts are present, nonblank, concept-named, and uniquely rendered.")


if __name__ == "__main__":
    main()
