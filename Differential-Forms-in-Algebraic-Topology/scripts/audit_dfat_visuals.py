from __future__ import annotations
import argparse, ast, hashlib, json, sys
from pathlib import Path
BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path: sys.path.insert(0, str(BOOK_ROOT))
from utils.validation import artifact_topics, canonical_notebooks, code_sources, image_stats, relative
def call_name(node: ast.Call) -> str | None:
    return node.func.id if isinstance(node.func, ast.Name) else (node.func.attr if isinstance(node.func, ast.Attribute) else None)
def nb_stats(path: Path) -> dict:
    saves = displays = 0; errors = []
    for source in code_sources(path):
        try: tree = ast.parse(source)
        except SyntaxError as exc: errors.append(str(exc)); continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = call_name(node)
                if name in {"save_matplotlib", "save_plotly_html"}: saves += 1
                if name == "display_artifact": displays += 1
    return {"path": relative(path), "visual_save_calls": saves, "display_artifact_calls": displays, "parse_errors": errors}
def sha256(path: Path) -> str:
    h = hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()
def main() -> None:
    p = argparse.ArgumentParser(); p.add_argument("--json", action="store_true"); p.add_argument("--min-width", type=int, default=64); p.add_argument("--min-height", type=int, default=64); p.add_argument("--blank-stddev", type=float, default=1.0); args = p.parse_args()
    findings = []; notebooks = [nb_stats(p) for p in canonical_notebooks(BOOK_ROOT)]
    for item in notebooks:
        if item["parse_errors"]: findings.append({"check": "parse-error", **item})
        if item["visual_save_calls"] == 0: findings.append({"check": "missing-visual-save", **item})
        if item["display_artifact_calls"] == 0: findings.append({"check": "missing-display-artifact", **item})
    images = []; hashes: dict[str, list[str]] = {}
    for topic in artifact_topics():
        root = BOOK_ROOT / "artifacts" / topic; pngs = sorted(root.rglob("*.png")) if root.exists() else []
        if not pngs: findings.append({"check": "missing-topic-png", "path": relative(root, BOOK_ROOT)})
        for png in pngs:
            item = image_stats(png); item["sha256"] = sha256(png); images.append(item); hashes.setdefault(item["sha256"], []).append(item["path"])
            if item["width"] < args.min_width or item["height"] < args.min_height: findings.append({"check": "tiny-image", **item})
            if item["max_channel_stddev"] <= args.blank_stddev: findings.append({"check": "blank-image", **item})
    for digest, paths in hashes.items():
        if len(paths) > 1: findings.append({"check": "duplicate-png-hash", "sha256": digest, "paths": paths})
    report = {"summary": {"notebook_count": len(notebooks), "png_count": len(images), "finding_count": len(findings)}, "findings": findings}
    print(json.dumps(report, indent=2) if args.json else f"Audited {len(notebooks)} notebooks and {len(images)} PNGs; findings={len(findings)}")
    if findings: raise SystemExit(1)
if __name__ == "__main__": main()
