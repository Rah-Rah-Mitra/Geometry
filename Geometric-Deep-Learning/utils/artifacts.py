"""Artifact helpers for the Geometric Deep Learning notebook course."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image as PILImage

BOOK_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"


def book_relative(path: str | Path) -> str:
    """Return a stable book-local path when an artifact lives inside this course."""
    resolved = Path(path).resolve()
    try:
        return resolved.relative_to(BOOK_ROOT).as_posix()
    except ValueError:
        return Path(path).as_posix()


def slugify(value: str) -> str:
    """Convert a label into a stable lowercase path segment."""
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-._")
    return slug or "artifact"


def artifact_dir(chapter: int | str, kind: str, root: str | Path = ARTIFACT_ROOT) -> Path:
    """Return and create an artifact directory such as artifacts/chapter-03/figures."""
    if isinstance(chapter, int):
        chapter_part = f"chapter-{chapter:02d}"
    else:
        chapter_part = slugify(str(chapter))
    path = Path(root) / chapter_part / slugify(kind)
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(
    chapter: int | str,
    kind: str,
    filename: str,
    root: str | Path = ARTIFACT_ROOT,
) -> Path:
    """Return a stable artifact file path and ensure its parent exists."""
    path = artifact_dir(chapter, kind, root) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_matplotlib(
    figure: Any,
    chapter: int | str,
    filename: str,
    *,
    kind: str = "figures",
    dpi: int = 160,
    root: str | Path = ARTIFACT_ROOT,
    **savefig_kwargs: Any,
) -> Path:
    """Save a Matplotlib figure and return the written path."""
    path = artifact_path(chapter, kind, filename, root)
    figure.savefig(path, dpi=dpi, bbox_inches="tight", **savefig_kwargs)
    return path


def save_image(
    image: Any,
    chapter: int | str,
    filename: str,
    *,
    kind: str = "figures",
    root: str | Path = ARTIFACT_ROOT,
) -> Path:
    """Save a PIL image or numpy-like array and return the written path."""
    path = artifact_path(chapter, kind, filename, root)
    if isinstance(image, PILImage.Image):
        image.save(path)
        return path

    array = np.asarray(image)
    if array.dtype != np.uint8:
        if np.issubdtype(array.dtype, np.floating) and array.size and array.max() <= 1.0:
            array = array * 255.0
        array = np.clip(array, 0, 255).astype(np.uint8)
    PILImage.fromarray(array).save(path)
    return path


def save_plotly_html(
    figure: Any,
    chapter: int | str,
    filename: str,
    *,
    kind: str = "html",
    root: str | Path = ARTIFACT_ROOT,
    include_plotlyjs: str | bool = "cdn",
    full_html: bool = True,
    **write_html_kwargs: Any,
) -> Path:
    """Save a Plotly figure as standalone HTML and return the written path."""
    path = artifact_path(chapter, kind, filename, root)
    figure.write_html(
        path,
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
        **write_html_kwargs,
    )
    return path


def save_json(
    data: Any,
    chapter: int | str,
    filename: str,
    *,
    kind: str = "checks",
    root: str | Path = ARTIFACT_ROOT,
    indent: int = 2,
) -> Path:
    """Save JSON-serializable data and return the written path."""
    path = artifact_path(chapter, kind, filename, root)
    path.write_text(json.dumps(data, indent=indent, sort_keys=True), encoding="utf-8")
    return path


def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
    """Display an artifact inside a notebook, falling back to a file link."""
    from IPython.display import HTML, IFrame, Image, display

    resolved = Path(path)
    suffix = resolved.suffix.lower()

    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        return display(Image(filename=str(resolved), width=width, height=height))
    if suffix in {".html", ".htm"}:
        if height:
            return display(IFrame(src=str(resolved), width=width or "100%", height=height))
        return display(HTML(resolved.read_text(encoding="utf-8")))

    link = escape(book_relative(resolved), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))


def assert_artifacts(paths: list[str | Path], *, min_bytes: int = 100) -> dict[str, int]:
    """Assert that artifact files exist and are nonempty; return their sizes."""
    sizes: dict[str, int] = {}
    for item in paths:
        path = Path(item)
        if not path.exists():
            raise AssertionError(f"Missing artifact: {path}")
        size = path.stat().st_size
        if size < min_bytes:
            raise AssertionError(f"Artifact too small: {path} ({size} bytes)")
        sizes[book_relative(path)] = size
    return sizes
