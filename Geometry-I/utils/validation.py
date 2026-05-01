"""Validation helpers for Geometry I scripts and notebooks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageStat


BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-book-index.ipynb", "00-part-index.ipynb"}


def relative(path: Path, root: Path | None = None) -> str:
    base = BOOK_ROOT if root is None else root
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def notebook_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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


def markdown_sources(path: Path) -> list[str]:
    data = notebook_json(path)
    return [
        "".join(cell.get("source", ""))
        for cell in data.get("cells", [])
        if cell.get("cell_type") == "markdown"
    ]


def code_sources(path: Path) -> list[str]:
    data = notebook_json(path)
    return [
        "".join(cell.get("source", ""))
        for cell in data.get("cells", [])
        if cell.get("cell_type") == "code"
    ]


def image_report(path: Path) -> dict[str, float | int | str]:
    with Image.open(path) as image:
        image.load()
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
    return {
        "path": relative(path),
        "width": int(rgb.width),
        "height": int(rgb.height),
        "bytes": int(path.stat().st_size),
        "max_channel_stddev": float(max(stat.stddev) if stat.stddev else 0.0),
    }


def png_artifacts(book_root: Path = BOOK_ROOT) -> list[Path]:
    return sorted((book_root / "artifacts").rglob("*.png"))


def artifact_report(paths: Iterable[Path]) -> list[dict[str, float | int | str]]:
    return [image_report(path) for path in paths]


def require_nonblank_images(paths: Iterable[Path], *, min_stddev: float = 1.0) -> None:
    for path in paths:
        report = image_report(path)
        if report["max_channel_stddev"] < min_stddev:
            raise AssertionError(f"{relative(path)} looks blank: {report}")


def ensure_one_canonical_per_source(source_folders: Iterable[Path]) -> list[str]:
    findings: list[str] = []
    for folder in sorted(source_folders):
        notebooks = sorted(path.name for path in folder.glob("*.ipynb") if path.name != "00-index.ipynb")
        if len(notebooks) != 1:
            findings.append(f"{relative(folder)} has {len(notebooks)} canonical notebooks: {notebooks}")
        if not (folder / "00-index.ipynb").exists():
            findings.append(f"{relative(folder)} is missing 00-index.ipynb")
    return findings

