"""Artifact helpers for the geometric group theory notebook course."""

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
    """Return a stable filesystem slug."""

    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-._")
    return slug or "artifact"


def artifact_dir(unit: str, kind: str | None = None, root: str | Path = ARTIFACT_ROOT) -> Path:
    """Create and return a book-local artifact directory."""

    parts = [slugify(unit)]
    if kind:
        parts.append(slugify(kind))
    path = Path(root).joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(unit: str, kind: str | None, filename: str, root: str | Path = ARTIFACT_ROOT) -> Path:
    """Return a book-local artifact path, creating its parent directory."""

    path = artifact_dir(unit, kind, root) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def write_json(data: Any, unit: str, kind: str | None, filename: str, *, root: str | Path = ARTIFACT_ROOT) -> Path:
    """Write sorted JSON to a book-local artifact path."""

    path = artifact_path(unit, kind, filename, root)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def read_json(path: str | Path) -> Any:
    """Read a JSON artifact."""

    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_figure(
    figure: Any,
    unit: str,
    kind: str | None,
    filename: str,
    *,
    dpi: int = 160,
    root: str | Path = ARTIFACT_ROOT,
    **kwargs: Any,
) -> Path:
    """Save a Matplotlib figure to a book-local artifact path."""

    path = artifact_path(unit, kind, filename, root)
    figure.savefig(path, dpi=dpi, bbox_inches="tight", **kwargs)
    return path


def save_plotly_html(
    figure: Any,
    unit: str,
    kind: str | None,
    filename: str,
    *,
    root: str | Path = ARTIFACT_ROOT,
    include_plotlyjs: str | bool = "cdn",
    full_html: bool = True,
    **kwargs: Any,
) -> Path:
    """Save a Plotly figure as standalone HTML."""

    path = artifact_path(unit, kind, filename, root)
    figure.write_html(path, include_plotlyjs=include_plotlyjs, full_html=full_html, **kwargs)
    return path


def save_image(image: Any, unit: str, kind: str | None, filename: str, *, root: str | Path = ARTIFACT_ROOT) -> Path:
    """Save a PIL image or array as an image artifact."""

    path = artifact_path(unit, kind, filename, root)
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


def image_nonblank(path: str | Path, *, min_stddev: float = 1.0) -> bool:
    """Return whether an image has enough channel variation to be useful."""

    with PILImage.open(path) as image:
        arr = np.asarray(image.convert("RGB"), dtype=float)
    return bool(arr.size and np.max(arr.std(axis=(0, 1))) > min_stddev)


def _effective_min_bytes(path: Path, min_bytes: int) -> int:
    if path.suffix.lower() in {".json", ".csv", ".txt", ".md"}:
        return min(min_bytes, 64)
    return min_bytes


def assert_artifact(path: str | Path, *, min_bytes: int = 512, nonblank_image: bool = False) -> Path:
    """Assert that an artifact exists and has useful content."""

    resolved = Path(path)
    if not resolved.exists():
        raise FileNotFoundError(resolved)
    size = resolved.stat().st_size
    required_size = _effective_min_bytes(resolved, min_bytes)
    if size < required_size:
        raise AssertionError(f"{resolved} is unexpectedly small: {size} bytes")
    if nonblank_image and resolved.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        if not image_nonblank(resolved):
            raise AssertionError(f"{resolved} appears blank or nearly constant")
    return resolved


def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
    """Display a local artifact inline in a notebook."""

    from IPython.display import HTML, IFrame, Image, display

    resolved = Path(path)
    suffix = resolved.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        return display(Image(filename=str(resolved), width=width, height=height))
    if suffix in {".html", ".htm"}:
        return display(IFrame(src=str(resolved), width=width or "100%", height=height or 520))
    link = escape(resolved.as_posix(), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))
