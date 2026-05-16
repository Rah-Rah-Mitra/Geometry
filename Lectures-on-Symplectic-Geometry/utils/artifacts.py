"""Artifact helpers for the Lectures on Symplectic Geometry course."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path
from typing import Any

BOOK_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"


def slugify(value: str) -> str:
    """Return a filesystem-safe ASCII slug."""

    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-._")
    return slug or "artifact"


def artifact_dir(topic: str, *parts: str, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = Path(root) / slugify(topic)
    for part in parts:
        path /= slugify(part)
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(topic: str, subdir: str, filename: str, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_dir(topic, subdir, root=root) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Any, topic: str, subdir: str, filename: str, *, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_path(topic, subdir, filename, root=root)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_matplotlib(figure: Any, topic: str, subdir: str, filename: str, *, dpi: int = 160) -> Path:
    path = artifact_path(topic, subdir, filename)
    figure.savefig(path, dpi=dpi, bbox_inches="tight")
    return path


def save_plotly_html(figure: Any, topic: str, subdir: str, filename: str) -> Path:
    path = artifact_path(topic, subdir, filename)
    figure.write_html(path, include_plotlyjs="cdn", full_html=True)
    return path


def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
    """Display a local artifact in notebooks while keeping file paths explicit."""

    from IPython.display import HTML, IFrame, Image, display

    resolved = Path(path)
    suffix = resolved.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        return display(Image(filename=str(resolved), width=width, height=height))
    if suffix in {".html", ".htm"}:
        return display(IFrame(src=str(resolved), width=width or "100%", height=height or 420))
    link = escape(resolved.as_posix(), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))
