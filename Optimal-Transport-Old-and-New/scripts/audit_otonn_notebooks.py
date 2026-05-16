"""Audit Optimal Transport notebooks for standalone structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import nbformat

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))

from scripts import otonn_inventory as inventory

IGNORED = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}


def notebook_stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    joined = "\n".join(markdown + code)
    return {
        "path": inventory.rel(path),
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "has_book_root": "BOOK_ROOT" in joined,
        "has_source_span": "Source span" in joined or "source span" in joined,
        "has_display": "display_artifact(" in joined,
        "has_final_sanity": "final_sanity" in joined,
        "has_transport_vocab": any(term in joined for term in ["Wasserstein", "Monge", "Kantorovich", "Ricci", "coupling"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=650)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()

    structure = []
    stats = []
    for unit in inventory.UNITS:
        folder = inventory.unit_path(unit).parent
        if not (folder / "00-index.ipynb").exists():
            structure.append({"path": inventory.rel(folder), "message": "missing unit 00-index.ipynb"})
        path = inventory.unit_path(unit)
        if not path.exists():
            structure.append({"path": inventory.rel(path), "message": "canonical notebook missing"})
            continue
        canonicals = [p for p in folder.glob("*.ipynb") if p.name != "00-index.ipynb"]
        if len(canonicals) != 1:
            structure.append({"path": inventory.rel(folder), "message": f"expected one canonical notebook, found {len(canonicals)}"})
        stats.append(notebook_stats(path))

    failing = [
        item
        for item in stats
        if item["markdown_words"] < args.min_words
        or item["code_cells"] < args.min_code_cells
        or not item["has_book_root"]
        or not item["has_source_span"]
        or not item["has_display"]
        or not item["has_final_sanity"]
        or not item["has_transport_vocab"]
    ]
    report = {"notebook_count": len(stats), "failing_count": len(failing), "failing": failing, "structure": structure, "stats": stats}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(stats)} canonical notebooks.")
    if failing or structure:
        for item in failing:
            print(f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells")
        for item in structure:
            print(f"- {item['path']}: {item['message']}")
        raise SystemExit(1)
    print("All canonical notebooks meet standalone structure thresholds.")


if __name__ == "__main__":
    main()
