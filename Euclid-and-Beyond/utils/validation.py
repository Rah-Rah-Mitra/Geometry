"""Validation helpers for the Euclid and Beyond course scripts."""

from __future__ import annotations

import json
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
    visual_builder_calls = source.count("build_unit_visuals(")
    direct_visual_calls = sum(
        source.count(token)
        for token in (
            "save_matplotlib(",
            "save_plotly_html(",
            "save_json(",
            ".savefig(",
            ".write_html(",
            "plt.subplots(",
            "plt.figure(",
            "go.Figure(",
        )
    )
    return {
        "path": path.relative_to(book_root).as_posix(),
        "markdown_words": sum(len(text.split()) for text in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "display_artifact_calls": source.count("display_artifact("),
        "visual_builder_calls": visual_builder_calls,
        "direct_visual_calls": direct_visual_calls,
        "visual_generation_calls": visual_builder_calls + direct_visual_calls,
        "stale_paths": [pattern for pattern in STALE_PATH_PATTERNS if pattern in source],
    }


def write_report(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
