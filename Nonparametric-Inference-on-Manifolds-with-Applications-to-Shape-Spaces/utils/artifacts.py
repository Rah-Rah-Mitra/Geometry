"""Book-local artifact and notebook display helpers."""

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
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-._")
    return slug or "artifact"


def artifact_dir(topic: str, slug: str | None = None) -> Path:
    parts = [slugify(topic)]
    if slug:
        parts.append(slugify(slug))
    path = ARTIFACT_ROOT.joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(topic: str, slug: str | None, filename: str) -> Path:
    path = artifact_dir(topic, slug) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Any, topic: str, slug: str | None, filename: str = "data.json") -> Path:
    path = artifact_path(topic, slug, filename)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_matplotlib(figure: Any, topic: str, slug: str | None, filename: str, *, dpi: int = 160) -> Path:
    path = artifact_path(topic, slug, filename)
    figure.savefig(path, dpi=dpi, bbox_inches="tight")
    return path


def save_plotly_html(figure: Any, topic: str, slug: str | None, filename: str) -> Path:
    path = artifact_path(topic, slug, filename)
    figure.write_html(path, include_plotlyjs="cdn", full_html=True)
    return path


def save_image(image: Any, topic: str, slug: str | None, filename: str) -> Path:
    path = artifact_path(topic, slug, filename)
    if isinstance(image, PILImage.Image):
        image.save(path)
        return path
    array = np.asarray(image)
    if array.dtype != np.uint8:
        if np.issubdtype(array.dtype, np.floating) and array.size and float(array.max()) <= 1.0:
            array = array * 255.0
        array = np.clip(array, 0, 255).astype(np.uint8)
    PILImage.fromarray(array).save(path)
    return path


def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
    """Display a course-local artifact inside a notebook."""

    from IPython.display import HTML, IFrame, Image, display

    resolved = Path(path)
    suffix = resolved.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        return display(Image(filename=str(resolved), width=width, height=height))
    if suffix in {".html", ".htm"}:
        return display(IFrame(src=str(resolved), width=width or "100%", height=height or 520))
    link = escape(resolved.as_posix(), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))


def require_artifacts(paths: list[str | Path], *, min_bytes: int = 500) -> dict[str, int]:
    sizes: dict[str, int] = {}
    for raw in paths:
        path = Path(raw)
        if not path.exists():
            raise FileNotFoundError(path)
        size = path.stat().st_size
        if size < min_bytes:
            raise AssertionError(f"{path} is too small to be a useful artifact: {size} bytes")
        sizes[str(path)] = size
    return sizes
