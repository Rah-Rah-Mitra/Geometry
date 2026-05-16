"""Artifact helpers for the symplectic topology course."""

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


def artifact_dir(unit_slug: str, kind: str, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = Path(root) / slugify(unit_slug) / slugify(kind)
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(unit_slug: str, kind: str, filename: str, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_dir(unit_slug, kind, root) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Any, unit_slug: str, kind: str, filename: str, *, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_path(unit_slug, kind, filename, root)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def save_matplotlib(figure: Any, unit_slug: str, kind: str, filename: str, *, dpi: int = 160, root: str | Path = ARTIFACT_ROOT, **kwargs: Any) -> Path:
    path = artifact_path(unit_slug, kind, filename, root)
    figure.savefig(path, dpi=dpi, bbox_inches="tight", **kwargs)
    return path


def save_plotly_html(figure: Any, unit_slug: str, kind: str, filename: str, *, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_path(unit_slug, kind, filename, root)
    figure.write_html(path, include_plotlyjs="cdn", full_html=True)
    return path


def image_stats(path: str | Path) -> dict[str, float | int | str]:
    path = Path(path)
    payload: dict[str, float | int | str] = {"file_size": path.stat().st_size, "suffix": path.suffix.lower()}
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        image = PILImage.open(path)
        array = np.asarray(image.convert("RGB"), dtype=float)
        payload.update(
            {
                "width": int(image.width),
                "height": int(image.height),
                "pixel_std": float(array.std()),
                "pixel_mean": float(array.mean()),
            }
        )
    return payload


def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
    from IPython.display import HTML, IFrame, Image, display

    resolved = Path(path)
    suffix = resolved.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        return display(Image(filename=str(resolved), width=width, height=height))
    if suffix in {".html", ".htm"}:
        return display(IFrame(src=str(resolved), width=width or "100%", height=height or 520))
    link = escape(resolved.as_posix(), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))
