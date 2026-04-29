"""Artifact helpers for the GICT notebook course."""

from __future__ import annotations

import csv
import json
import re
from html import escape
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from PIL import Image as PILImage

BOOK_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-._")
    return slug or "artifact"


def ensure_artifact_root(root: str | Path) -> Path:
    path = Path(root)
    for child in ["figures", "html", "checks", "tables"]:
        (path / child).mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(root: str | Path, category: str, filename: str) -> Path:
    base = ensure_artifact_root(root)
    path = base / slugify(category) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Any, root: str | Path, category: str, filename: str = "data.json") -> Path:
    path = artifact_path(root, category, filename)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def save_table(rows: Iterable[dict[str, Any]], root: str | Path, category: str, filename: str = "table.csv") -> Path:
    path = artifact_path(root, category, filename)
    rows = list(rows)
    fieldnames: list[str] = sorted({key for row in rows for key in row.keys()})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def save_text(text: str, root: str | Path, category: str, filename: str = "notes.txt") -> Path:
    path = artifact_path(root, category, filename)
    path.write_text(text, encoding="utf-8")
    return path


def save_html(text: str, root: str | Path, category: str, filename: str = "view.html") -> Path:
    path = artifact_path(root, category, filename)
    path.write_text(text, encoding="utf-8")
    return path


def save_matplotlib(figure: Any, root: str | Path, category: str, filename: str, *, dpi: int = 155) -> Path:
    path = artifact_path(root, category, filename)
    figure.savefig(path, dpi=dpi, bbox_inches="tight")
    return path


def image_stats(path: str | Path) -> dict[str, Any]:
    resolved = Path(path)
    image = PILImage.open(resolved).convert("RGB")
    arr = np.asarray(image, dtype=float)
    return {
        "path": resolved.as_posix(),
        "width": int(image.width),
        "height": int(image.height),
        "pixel_std": float(arr.std()),
        "file_size": int(resolved.stat().st_size),
    }


def assert_artifacts(paths: Iterable[str | Path], *, min_size: int = 256) -> None:
    for item in paths:
        path = Path(item)
        if not path.exists():
            raise AssertionError(f"Missing artifact: {path}")
        if path.stat().st_size < min_size:
            raise AssertionError(f"Artifact too small: {path}")


def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
    from IPython.display import HTML, IFrame, Image, display

    resolved = Path(path)
    suffix = resolved.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        return display(Image(filename=str(resolved), width=width, height=height))
    if suffix == ".svg":
        return display(HTML(resolved.read_text(encoding="utf-8")))
    if suffix in {".html", ".htm"}:
        return display(IFrame(src=str(resolved), width=width or "100%", height=height or 420))
    link = escape(resolved.as_posix(), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))
