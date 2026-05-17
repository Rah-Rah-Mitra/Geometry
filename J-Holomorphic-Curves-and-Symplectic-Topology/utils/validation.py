"""Validation helpers for the JHCST course scripts."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Any

import nbformat

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-book-index.ipynb"}
STALE_PATH_PATTERNS = (
    "D:/Geometry/artifacts",
    "D:\\Geometry\\artifacts",
    "/mnt/d/Geometry/artifacts",
    "D:/Geometry/utils",
    "D:\\Geometry\\utils",
    "/mnt/d/Geometry/utils",
)
GENERIC_NOTEBOOK_PHRASES = (
    "The graph below is a compact proof-state diagram.",
    "This section builds a small model for one core mechanism",
    "The ledger records the chapter vocabulary as computational objects",
    "The intended workflow is to change one parameter",
    "If the visual impression and the invariant check disagree",
    "The final cell asserts that the generated figures, ledgers, and JSON checks exist",
)
REQUIRED_STANDALONE_MARKERS = {
    "source_coverage": ("source-coverage.json", "## Source Coverage"),
    "visual_storyboard": ("visual-storyboard.json", "## Visualization Storyboard"),
    "library_routing": ("## Library Routing", "library routing"),
    "final_sanity": ("final-sanity.json", "final_sanity"),
}


def discover_canonical_notebooks(book_root: Path = BOOK_ROOT) -> list[Path]:
    artifact_root = book_root / "artifacts"
    return [
        path
        for path in sorted(book_root.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED_NOTEBOOKS
    ]


def notebook_stats(path: Path, book_root: Path = BOOK_ROOT) -> dict[str, Any]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    source = "\n".join(markdown + code)
    normalized_markdown_hashes = [
        hashlib.sha256(" ".join(text.lower().split()).encode("utf-8")).hexdigest()[:16]
        for text in markdown
        if text.strip()
    ]
    direct_visual_calls = sum(
        source.count(token)
        for token in (
            "save_matplotlib(",
            ".savefig(",
            "plt.subplots(",
            "imshow(",
            "plot(",
            "nx.draw",
        )
    )
    return {
        "path": path.relative_to(book_root).as_posix(),
        "markdown_words": sum(len(text.split()) for text in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "display_artifact_calls": source.count("display_artifact("),
        "direct_visual_calls": direct_visual_calls,
        "visual_generation_calls": direct_visual_calls,
        "assert_artifact_calls": source.count("assert_artifact("),
        "has_applied_lab": "## Applied Lab" in source,
        "has_takeaways": "## Takeaways" in source,
        "generic_phrase_hits": [phrase for phrase in GENERIC_NOTEBOOK_PHRASES if phrase in source],
        "required_markers": {
            name: any(marker in source for marker in markers)
            for name, markers in REQUIRED_STANDALONE_MARKERS.items()
        },
        "markdown_hashes": normalized_markdown_hashes,
        "stale_paths": [pattern for pattern in STALE_PATH_PATTERNS if pattern in source],
    }


def write_report(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
