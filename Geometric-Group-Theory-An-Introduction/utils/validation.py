"""Validation helpers for the geometric group theory course scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import nbformat

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-book-index.ipynb", "00-part-index.ipynb"}
STALE_PATH_PATTERNS = (
    "D:/Geometry/artifacts",
    "D:\\Geometry\\artifacts",
    "/mnt/d/Geometry/artifacts",
    "D:/Geometry/utils",
    "D:\\Geometry\\utils",
    "/mnt/d/Geometry/utils",
)


def discover_canonical_notebooks(book_root: Path = BOOK_ROOT) -> list[Path]:
    """Return canonical teaching notebooks, excluding indexes and artifacts."""

    artifact_root = book_root / "artifacts"
    return [
        path
        for path in sorted(book_root.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED_NOTEBOOKS
    ]


def notebook_stats(path: Path, book_root: Path = BOOK_ROOT) -> dict[str, Any]:
    """Collect structural stats for a notebook."""

    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    source = "\n".join(markdown + code)
    visual_tokens = (
        "build_intro_cayley_gallery(",
        "build_generating_groups_visuals(",
        "build_cayley_graph_visuals(",
        "build_group_action_visuals(",
        "build_quasi_isometry_visuals(",
        "build_growth_visuals(",
        "build_hyperbolic_visuals(",
        "build_ends_boundary_visuals(",
        "build_amenability_visuals(",
        "build_appendix_visuals(",
        "plt.subplots(",
        "go.Figure(",
        ".write_html(",
        ".savefig(",
    )
    generic_warnings = []
    if source.count("build_unit_visuals("):
        generic_warnings.append("uses generic build_unit_visuals")
    if source.count("TODO") or source.count("placeholder"):
        generic_warnings.append("contains TODO/placeholder marker")
    return {
        "path": path.relative_to(book_root).as_posix(),
        "markdown_words": sum(len(text.split()) for text in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "display_artifact_calls": source.count("display_artifact("),
        "visual_generation_calls": sum(source.count(token) for token in visual_tokens),
        "final_sanity_refs": source.count("final-sanity.json"),
        "source_span_refs": source.count("Source span"),
        "library_routing_refs": source.count("Library routing"),
        "stale_paths": [pattern for pattern in STALE_PATH_PATTERNS if pattern in source],
        "generic_warnings": generic_warnings,
    }


def write_report(path: Path, data: Any) -> None:
    """Write a JSON report."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")

