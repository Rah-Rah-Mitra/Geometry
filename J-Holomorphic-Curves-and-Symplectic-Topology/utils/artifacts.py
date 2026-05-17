"""Artifact helpers for the JHCST notebook course."""

from __future__ import annotations

import json
import io
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


def artifact_dir(unit: str, kind: str | None = None, root: str | Path = ARTIFACT_ROOT) -> Path:
    parts = [slugify(unit)]
    if kind:
        parts.append(slugify(kind))
    path = Path(root).joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(unit: str, kind: str | None, filename: str, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_dir(unit, kind, root) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Any, unit: str, kind: str | None, filename: str = "data.json", *, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_path(unit, kind, filename, root)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def save_matplotlib(figure: Any, unit: str, kind: str | None, filename: str, *, dpi: int = 160, root: str | Path = ARTIFACT_ROOT, **kwargs: Any) -> Path:
    path = artifact_path(unit, kind, filename, root)
    save_kwargs = {"dpi": dpi, **kwargs}
    save_kwargs.setdefault("bbox_inches", "tight")
    save_kwargs.setdefault("format", path.suffix.lower().lstrip(".") or "png")

    def render_bytes(render_kwargs: dict[str, Any]) -> bytes:
        buffer = io.BytesIO()
        figure.savefig(buffer, **render_kwargs)
        return buffer.getvalue()

    try:
        image_bytes = render_bytes(save_kwargs)
    except OSError:
        if save_kwargs.get("bbox_inches") != "tight":
            raise
        # Tight bboxes can fail for text-heavy Matplotlib artists on Windows.
        fallback_kwargs = dict(save_kwargs)
        fallback_kwargs["bbox_inches"] = None
        image_bytes = render_bytes(fallback_kwargs)
    path.write_bytes(image_bytes)
    return path


def save_image(image: Any, unit: str, kind: str | None, filename: str, *, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_path(unit, kind, filename, root)
    if isinstance(image, PILImage.Image):
        image.save(path)
        return path
    array = np.asarray(image)
    if array.dtype != np.uint8:
        if np.issubdtype(array.dtype, np.floating) and array.size and float(np.nanmax(array)) <= 1.0:
            array = array * 255.0
        array = np.clip(array, 0, 255).astype(np.uint8)
    PILImage.fromarray(array).save(path)
    return path


def _effective_min_bytes(path: Path, min_bytes: int) -> int:
    if path.suffix.lower() in {".json", ".csv", ".txt", ".md"}:
        return min(min_bytes, 64)
    return min_bytes


def assert_artifact(path: str | Path, *, min_bytes: int = 512) -> Path:
    resolved = Path(path)
    if not resolved.exists():
        raise FileNotFoundError(resolved)
    size = resolved.stat().st_size
    required_size = _effective_min_bytes(resolved, min_bytes)
    if size < required_size:
        raise AssertionError(f"{resolved} is unexpectedly small: {size} bytes")
    return resolved


def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
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
