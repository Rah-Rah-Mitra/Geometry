"""Validation helpers for CGAA scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-book-index.ipynb"}


def relative(path: Path, root: Path | None = None) -> str:
    base = BOOK_ROOT.parent if root is None else root
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def canonical_notebooks(book_root: Path = BOOK_ROOT) -> list[Path]:
    artifact_root = book_root / "artifacts"
    return [
        path
        for path in sorted(book_root.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED_NOTEBOOKS
    ]


def index_notebooks(book_root: Path = BOOK_ROOT) -> list[Path]:
    artifact_root = book_root / "artifacts"
    return [
        path
        for path in sorted(book_root.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name in IGNORED_NOTEBOOKS
    ]


def notebook_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_sources(path: Path) -> list[str]:
    data = notebook_json(path)
    return ["".join(cell.get("source", "")) for cell in data.get("cells", []) if cell.get("cell_type") == "markdown"]


def code_sources(path: Path) -> list[str]:
    data = notebook_json(path)
    return ["".join(cell.get("source", "")) for cell in data.get("cells", []) if cell.get("cell_type") == "code"]


def artifact_topics() -> list[str]:
    return [f"chapter-{i:02d}" for i in range(1, 17)]


def png_artifacts(book_root: Path = BOOK_ROOT) -> list[Path]:
    return sorted((book_root / "artifacts").rglob("*.png"))


def ensure_one_canonical_per_chapter(book_root: Path = BOOK_ROOT) -> list[str]:
    findings: list[str] = []
    for folder in sorted(path for path in book_root.iterdir() if path.is_dir() and path.name.startswith("chapter-")):
        notebooks = sorted(path.name for path in folder.glob("*.ipynb") if path.name != "00-index.ipynb")
        if len(notebooks) != 1:
            findings.append(f"{folder.name} has {len(notebooks)} canonical notebooks: {notebooks}")
        if not (folder / "00-index.ipynb").exists():
            findings.append(f"{folder.name} is missing 00-index.ipynb")
    return findings
