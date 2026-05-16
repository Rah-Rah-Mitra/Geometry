"""Book-local artifact helpers."""

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


def book_relative(path: str | Path) -> str:
    resolved = Path(path).resolve()
    try:
        return resolved.relative_to(BOOK_ROOT).as_posix()
    except ValueError:
        return Path(path).as_posix()


def artifact_dir(topic: str, slug: str | None = None, root: str | Path = ARTIFACT_ROOT) -> Path:
    pieces = [slugify(topic)]
    if slug:
        pieces.append(slugify(slug))
    path = Path(root).joinpath(*pieces)
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(topic: str, slug: str | None, filename: str, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_dir(topic, slug, root) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Any, topic: str, slug: str | None, filename: str = "checks.json") -> Path:
    path = artifact_path(topic, slug, filename)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def save_matplotlib(figure: Any, topic: str, slug: str | None, filename: str = "figure.png", *, dpi: int = 160) -> Path:
    path = artifact_path(topic, slug, filename)
    figure.savefig(path, dpi=dpi, bbox_inches="tight")
    return path


def save_image(image: Any, topic: str, slug: str | None, filename: str = "image.png") -> Path:
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


def artifact_record(path: str | Path) -> dict[str, object]:
    p = Path(path)
    return {
        "path": book_relative(p),
        "exists": p.exists(),
        "bytes": int(p.stat().st_size) if p.exists() else 0,
    }


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
    link = escape(book_relative(resolved), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))

