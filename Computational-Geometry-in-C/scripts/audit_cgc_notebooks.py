from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))
from utils.validation import canonical_notebooks, code_sources, ensure_one_canonical_per_unit, markdown_sources, relative
BOOTSTRAP_MARKERS = [
    "The source unit is phrased in the language of **Computational Geometry in C**",
    "Use the model above as a controlled experiment. Change one numerical parameter",
    "not merely around the general subject of Computational Geometry in C",
    "curvature_proxy",
    "vandermonde",
    "local-chart-curvature",
    "initial-model",
]
def stats(path: Path) -> dict[str, object]:
    md = markdown_sources(path); code = code_sources(path)
    text = "\n".join(md); code_text = "\n".join(code)
    return {"path": relative(path), "markdown_words": len(text.split()), "markdown_cells": len(md), "code_cells": len(code), "has_setup": "BOOK_ROOT" in code_text, "has_sanity": "final_sanity" in code_text, "has_takeaways": "Takeaways" in text, "has_storyboard": "Visual Storyboard" in text, "has_lab": "Applied Lab" in text, "has_source_span": "Source Span" in text, "has_library_routing": "Library Routing" in text, "has_display_calls": "display_artifact" in code_text}
def fingerprints(paths: list[Path]) -> list[dict[str, object]]:
    by_hash: dict[str, list[str]] = {}
    for path in paths:
        for source in markdown_sources(path):
            normalized = " ".join(source.lower().split())
            if len(normalized.split()) >= 55:
                by_hash.setdefault(hashlib.sha256(normalized.encode()).hexdigest(), []).append(relative(path))
    return [{"finding": "repeated long markdown cell", "paths": sorted(set(v)), "sha256": k} for k, v in by_hash.items() if len(set(v)) > 1]
def code_fingerprints(paths: list[Path]) -> list[dict[str, object]]:
    by_hash: dict[str, list[str]] = {}
    for path in paths:
        for source in code_sources(path):
            normalized = "\n".join(line.strip() for line in source.splitlines() if line.strip() and not line.strip().startswith("#"))
            if len(normalized.splitlines()) >= 8:
                by_hash.setdefault(hashlib.sha256(normalized.encode()).hexdigest(), []).append(relative(path))
    return [{"finding": "repeated long code cell", "paths": sorted(set(v)), "sha256": k} for k, v in by_hash.items() if len(set(v)) > 1]
def bootstrap_findings(path: Path) -> list[dict[str, object]]:
    text = "\n".join(markdown_sources(path) + code_sources(path))
    return [{"path": relative(path), "finding": f"bootstrap marker remains: {marker}"} for marker in BOOTSTRAP_MARKERS if marker in text]
def main() -> None:
    p = argparse.ArgumentParser(); p.add_argument("--json", action="store_true"); p.add_argument("--min-words", type=int, default=900); p.add_argument("--min-code-cells", type=int, default=5); args = p.parse_args()
    notebooks = canonical_notebooks(BOOK_ROOT); items = [stats(path) for path in notebooks]; findings = []
    for item in items:
        if item["markdown_words"] < args.min_words: findings.append({**item, "finding": "below word threshold"})
        if item["code_cells"] < args.min_code_cells: findings.append({**item, "finding": "below code-cell threshold"})
        for marker in ["has_setup", "has_sanity", "has_takeaways", "has_storyboard", "has_lab", "has_source_span", "has_library_routing", "has_display_calls"]:
            if not item[marker]: findings.append({**item, "finding": f"missing required marker: {marker}"})
    for path in notebooks:
        findings.extend(bootstrap_findings(path))
    findings.extend({"path": "", "finding": f} for f in ensure_one_canonical_per_unit(BOOK_ROOT)); findings.extend(fingerprints(notebooks)); findings.extend(code_fingerprints(notebooks))
    report = {"notebook_count": len(items), "finding_count": len(findings), "findings": findings, "stats": items}
    print(json.dumps(report, indent=2) if args.json else f"Audited {len(items)} canonical notebooks; findings={len(findings)}")
    if findings: raise SystemExit(1)
if __name__ == "__main__": main()
