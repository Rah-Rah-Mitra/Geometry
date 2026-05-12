"""Validation helpers shared by Pressley course scripts."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import nbformat
from PIL import Image, ImageStat

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-book-index.ipynb"}


@dataclass(frozen=True)
class NotebookStats:
    path: str
    markdown_words: int
    markdown_cells: int
    code_cells: int
    display_artifact_calls: int
    visual_builder_calls: int
    direct_visual_calls: int
    visual_generation_calls: int


def discover_notebooks(book_root: Path = BOOK_ROOT, *, canonical_only: bool = True) -> list[Path]:
    artifact_root = Path(book_root) / "artifacts"
    paths = [path for path in sorted(Path(book_root).rglob("*.ipynb")) if artifact_root not in path.parents]
    if canonical_only:
        paths = [path for path in paths if path.name not in IGNORED_NOTEBOOKS]
    return paths


def notebook_stats(path: Path, book_root: Path = BOOK_ROOT) -> NotebookStats:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    joined_code = "\n".join(code)
    visual_builder_calls = joined_code.count("build_visual_storyboard") + joined_code.count("build_unit_visuals")
    direct_visual_calls = sum(
        joined_code.count(token)
        for token in (
            "save_fig(",
            "save_matplotlib(",
            "save_plotly_html(",
            ".write_html(",
            ".savefig(",
            "plt.subplots(",
            "go.Figure(",
        )
    )
    return NotebookStats(
        path=path.relative_to(book_root).as_posix(),
        markdown_words=sum(len(source.split()) for source in markdown),
        markdown_cells=len(markdown),
        code_cells=len(code),
        display_artifact_calls=joined_code.count("display_artifact"),
        visual_builder_calls=visual_builder_calls,
        direct_visual_calls=direct_visual_calls,
        visual_generation_calls=visual_builder_calls + direct_visual_calls,
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_stats(path: Path, book_root: Path = BOOK_ROOT) -> dict[str, object]:
    with Image.open(path) as image:
        image.load()
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
    return {
        "path": path.relative_to(book_root).as_posix(),
        "width": rgb.width,
        "height": rgb.height,
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
        "max_channel_stddev": max(stat.stddev) if stat.stddev else 0.0,
    }


def local_links_in_notebook(path: Path) -> Iterable[str]:
    nb = nbformat.read(path, as_version=4)
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        source = "".join(cell.get("source", ""))
        for match in re.finditer(r"\[[^\]]+\]\((?!https?://)([^)#]+)(?:#[^)]+)?\)", source):
            yield match.group(1)


def validate_local_links(book_root: Path = BOOK_ROOT) -> list[dict[str, str]]:
    findings = []
    for notebook in discover_notebooks(book_root, canonical_only=False):
        for link in local_links_in_notebook(notebook):
            target = (notebook.parent / link).resolve()
            if not target.exists():
                findings.append({"path": notebook.relative_to(book_root).as_posix(), "link": link})
    return findings
