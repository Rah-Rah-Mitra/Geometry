"""Validation helpers for Convex Analysis notebooks and artifacts."""

from __future__ import annotations

from pathlib import Path

import nbformat


def relative(path: Path, root: Path | None = None) -> str:
    base = Path.cwd() if root is None else Path(root)
    try:
        return Path(path).resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return Path(path).as_posix()


def canonical_notebooks(book_root: Path) -> list[Path]:
    return sorted(
        path
        for path in book_root.glob("part-*/section-*/*.ipynb")
        if path.name != "00-index.ipynb"
    )


def index_notebooks(book_root: Path) -> list[Path]:
    return sorted(
        [book_root / "00-book-index.ipynb"]
        + list(book_root.glob("part-*/00-part-index.ipynb"))
        + list(book_root.glob("part-*/section-*/00-index.ipynb"))
    )


def markdown_sources(path: Path) -> list[str]:
    nb = nbformat.read(path, as_version=4)
    return [cell.source for cell in nb.cells if cell.cell_type == "markdown"]


def code_sources(path: Path) -> list[str]:
    nb = nbformat.read(path, as_version=4)
    return [cell.source for cell in nb.cells if cell.cell_type == "code"]


def ensure_one_canonical_per_section(book_root: Path, expected_count: int = 39) -> list[str]:
    findings: list[str] = []
    notebooks = canonical_notebooks(book_root)
    if len(notebooks) != expected_count:
        findings.append(f"expected {expected_count} canonical notebooks, found {len(notebooks)}")
    for folder in sorted(book_root.glob("part-*/section-*")):
        canonical = [path for path in folder.glob("*.ipynb") if path.name != "00-index.ipynb"]
        if len(canonical) != 1:
            findings.append(f"{relative(folder, book_root)} has {len(canonical)} canonical notebooks")
    return findings

