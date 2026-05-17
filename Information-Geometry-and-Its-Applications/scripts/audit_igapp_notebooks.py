"""Audit Information Geometry notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import nbformat

import igapp_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}


def rel(path: Path) -> str:
    return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


def expected_notebook_paths() -> list[Path]:
    return [BOOK_ROOT / entry["part"] / entry["folder"] / entry["notebook"] for entry in inventory.ENTRIES]


def entry_for_notebook(path: Path) -> dict | None:
    for entry in inventory.ENTRIES:
        if path == BOOK_ROOT / entry["part"] / entry["folder"] / entry["notebook"]:
            return entry
    return None


def artifact_visual_count(entry: dict | None) -> int:
    if entry is None:
        return 0
    root = BOOK_ROOT / "artifacts" / entry["topic"]
    if not root.exists():
        return 0
    return len(list(root.rglob("*.png"))) + len(list(root.rglob("*.jpg"))) + len(list(root.rglob("*.jpeg"))) + len(list(root.rglob("*.svg"))) + len(list(root.rglob("*.html")))


def discover_notebooks() -> list[Path]:
    artifact_root = BOOK_ROOT / "artifacts"
    return [
        path
        for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED
    ]


def notebook_stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    joined = "\n".join(markdown + code)
    source_visual_saves = sum(
        source.count("save_matplotlib(")
        + source.count("save_plotly_html(")
        + source.count("save_image(")
        + source.count(".savefig(")
        + source.count(".write_html(")
        for source in code
    )
    artifact_visuals = artifact_visual_count(entry_for_notebook(path))
    display_calls = sum(
        source.count("display_artifact(")
        + source.count("Image(")
        + source.count("IFrame(")
        + source.count("HTML(")
        + source.count("display(")
        for source in code
    )
    rich_outputs = sum(len(cell.get("outputs", [])) for cell in nb.cells if cell.cell_type == "code")
    return {
        "path": rel(path),
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "visual_save_calls": source_visual_saves,
        "artifact_visual_count": artifact_visuals,
        "display_artifact_calls": display_calls,
        "rich_output_count": rich_outputs,
        "has_final_sanity": any(
            marker in joined
            for marker in ("final_sanity", "final-sanity", "chapter_07_sanity", "sanity_path")
        ),
        "has_book_root": "BOOK_ROOT" in joined,
        "has_source_span": "Source span" in joined or "source span" in joined,
    }


def structure_findings() -> list[dict[str, str]]:
    findings = []
    for entry, path in zip(inventory.ENTRIES, expected_notebook_paths(), strict=True):
        folder = path.parent
        if not (folder / "00-index.ipynb").exists():
            findings.append({"path": rel(folder), "message": "missing chapter 00-index.ipynb"})
        canonical = [p for p in folder.glob("*.ipynb") if p.name != "00-index.ipynb"]
        if path.exists() and len(canonical) != 1:
            findings.append({"path": rel(folder), "message": f"expected one canonical notebook after authoring, found {len(canonical)}"})
        if not path.exists():
            findings.append({"path": rel(path), "message": "canonical notebook not yet authored"})
        elif path.name != entry["notebook"]:
            findings.append({"path": rel(path), "message": "canonical notebook name does not match inventory"})
    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()

    stats = [notebook_stats(path) for path in discover_notebooks()]
    failing = [
        item
        for item in stats
        if item["markdown_words"] < args.min_words
        or item["code_cells"] < args.min_code_cells
        or (item["visual_save_calls"] == 0 and item["artifact_visual_count"] == 0)
        or (item["display_artifact_calls"] == 0 and item["rich_output_count"] == 0)
        or not item["has_final_sanity"]
        or not item["has_book_root"]
        or not item["has_source_span"]
    ]
    structure = structure_findings()
    if args.allow_missing:
        structure = [item for item in structure if item["message"] != "canonical notebook not yet authored"]
    report = {"notebook_count": len(stats), "failing_count": len(failing), "failing": failing, "structure_findings": structure, "stats": stats}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(stats)} canonical notebooks")
    if failing or structure:
        for item in failing:
            print(f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells, {item['visual_save_calls']} source visual saves, {item['artifact_visual_count']} artifact visuals, {item['display_artifact_calls']} display calls")
        for item in structure:
            print(f"- {item['path']}: {item['message']}")
        raise SystemExit(1)
    print("All authored canonical notebooks meet standalone structure thresholds.")


if __name__ == "__main__":
    main()
