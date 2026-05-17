import hashlib
import json
import sys
from pathlib import Path

import matplotlib.image as mpimg
import numpy as np

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pag_inventory as inv


GENERIC_NAMES = {"primary-visual.png", "interactive-lab.html"}


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_json_error": str(exc)}


def png_stats(path):
    image = mpimg.imread(path)
    if image.ndim == 3:
        sample = image[:, :, :3]
    else:
        sample = image
    return {
        "shape": tuple(int(v) for v in image.shape[:2]),
        "std": float(np.nanstd(sample)),
        "mean": float(np.nanmean(sample)),
    }


def visual_items(storyboard):
    if isinstance(storyboard, dict):
        for key in ("visual_sequence", "visuals", "items"):
            if isinstance(storyboard.get(key), list):
                return storyboard[key]
    if isinstance(storyboard, list):
        return storyboard
    return []


def audit_entry(entry, seen_hashes):
    findings = []
    root = BOOK_ROOT / "artifacts" / entry["topic"]
    if not root.exists():
        return [{"path": str(root), "issue": "missing artifact root"}]

    generic = [path.name for path in root.rglob("*") if path.name in GENERIC_NAMES]
    if generic:
        findings.append({"path": str(root), "issue": "generic bootstrap artifact filenames remain", "files": sorted(generic)})

    pngs = sorted(root.rglob("*.png"))
    htmls = sorted(root.rglob("*.html"))
    jsons = sorted(root.rglob("*.json"))
    if not pngs:
        findings.append({"path": str(root), "issue": "no PNG visual artifacts"})
    if not htmls:
        findings.append({"path": str(root), "issue": "no HTML exploration artifact"})
    if not jsons:
        findings.append({"path": str(root), "issue": "no JSON check artifacts"})

    for png in pngs:
        try:
            stats = png_stats(png)
        except Exception as exc:
            findings.append({"path": str(png), "issue": f"cannot read PNG: {exc}"})
            continue
        height, width = stats["shape"]
        if width < 320 or height < 220:
            findings.append({"path": str(png), "issue": f"PNG too small: {width}x{height}"})
        if stats["std"] < 0.005:
            findings.append({"path": str(png), "issue": f"PNG appears blank or nearly uniform: std={stats['std']:.4f}"})
        digest = hashlib.sha256(png.read_bytes()).hexdigest()
        if digest in seen_hashes:
            findings.append({"path": str(png), "issue": "PNG duplicates another chapter artifact", "duplicate_of": seen_hashes[digest]})
        else:
            seen_hashes[digest] = str(png)

    for html in htmls:
        text = html.read_text(encoding="utf-8", errors="ignore")
        lower = text.lower()
        if len(text) < 600:
            findings.append({"path": str(html), "issue": "HTML exploration is too small to be useful"})
        if "local generated lab" in lower:
            findings.append({"path": str(html), "issue": "generic HTML lab text remains"})
        if not any(token in lower for token in ("plotly", "<input", "<svg", "<canvas", "<table")):
            findings.append({"path": str(html), "issue": "HTML artifact lacks an inspectable visual or control"})

    storyboard_path = root / "checks" / "visual-storyboard.json"
    if not storyboard_path.exists():
        findings.append({"path": str(storyboard_path), "issue": "missing visual storyboard JSON"})
    else:
        storyboard = load_json(storyboard_path)
        items = visual_items(storyboard)
        if not items:
            findings.append({"path": str(storyboard_path), "issue": "storyboard has no visual sequence"})
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                findings.append({"path": str(storyboard_path), "issue": f"storyboard item {index} is not an object"})
                continue
            missing = [key for key in ("concept", "artifact", "invariant") if not item.get(key)]
            if missing:
                findings.append({"path": str(storyboard_path), "issue": f"storyboard item {index} missing {missing}"})

    for required in ("source-coverage.json", "final-sanity.json"):
        required_path = root / "checks" / required
        if not required_path.exists():
            findings.append({"path": str(required_path), "issue": f"missing required check artifact: {required}"})

    return findings


def main():
    findings = []
    seen_hashes = {}
    for entry in inv.ENTRIES:
        findings.extend(audit_entry(entry, seen_hashes))
    print(json.dumps({"findings": findings}, indent=2))
    raise SystemExit(1 if findings else 0)


if __name__ == "__main__":
    main()
