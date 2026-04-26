"""Helpers for saving and reloading notebook artifacts.

The notebook workflow in this workspace is intentionally artifact-first:
large or reusable outputs should be written to disk, then displayed from a
stable path instead of embedded directly in notebook cell output.
"""

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


def slugify(value: str) -> str:
    """Convert a label into a stable lowercase path segment."""
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-._")
    return slug or "artifact"


def artifact_dir(topic: str, slug: str | None = None, root: str | Path = ARTIFACT_ROOT) -> Path:
    """Create and return an artifact directory such as artifacts/topic/slug."""
    parts = [slugify(topic)]
    if slug:
        parts.append(slugify(slug))

    path = Path(root).joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(
    topic: str,
    slug: str | None,
    filename: str,
    root: str | Path = ARTIFACT_ROOT,
) -> Path:
    """Return a stable artifact file path and ensure its parent exists."""
    path = artifact_dir(topic, slug, root) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_matplotlib(
    figure: Any,
    topic: str,
    slug: str | None,
    filename: str = "figure.png",
    *,
    dpi: int = 160,
    root: str | Path = ARTIFACT_ROOT,
    **savefig_kwargs: Any,
) -> Path:
    """Save a Matplotlib figure and return the written path."""
    path = artifact_path(topic, slug, filename, root)
    figure.savefig(path, dpi=dpi, bbox_inches="tight", **savefig_kwargs)
    return path


def save_image(
    image: Any,
    topic: str,
    slug: str | None,
    filename: str = "image.png",
    *,
    root: str | Path = ARTIFACT_ROOT,
) -> Path:
    """Save a PIL image or numpy-like array and return the written path."""
    path = artifact_path(topic, slug, filename, root)

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
    topic: str,
    slug: str | None,
    filename: str = "plot.html",
    *,
    root: str | Path = ARTIFACT_ROOT,
    include_plotlyjs: str | bool = "cdn",
    full_html: bool = True,
    **write_html_kwargs: Any,
) -> Path:
    """Save a Plotly figure as standalone HTML and return the written path."""
    path = artifact_path(topic, slug, filename, root)
    figure.write_html(
        path,
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
        **write_html_kwargs,
    )
    return path


def save_json(
    data: Any,
    topic: str,
    slug: str | None,
    filename: str = "data.json",
    *,
    root: str | Path = ARTIFACT_ROOT,
    indent: int = 2,
) -> Path:
    """Save JSON-serializable data and return the written path."""
    path = artifact_path(topic, slug, filename, root)
    path.write_text(json.dumps(data, indent=indent, sort_keys=True), encoding="utf-8")
    return path


def save_text(
    text: str,
    topic: str,
    slug: str | None,
    filename: str = "notes.txt",
    *,
    root: str | Path = ARTIFACT_ROOT,
) -> Path:
    """Save text and return the written path."""
    path = artifact_path(topic, slug, filename, root)
    path.write_text(text, encoding="utf-8")
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

    link = escape(resolved.as_posix(), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))
