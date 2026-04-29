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


def artifact_dir(topic: str, kind: str = "figures", *, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = Path(root) / slugify(topic) / slugify(kind)
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(topic: str, kind: str, filename: str, *, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_dir(topic, kind, root=root) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Any, topic: str, filename: str = "checks.json", *, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_path(topic, "checks", filename, root=root)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def save_table_csv(rows: list[dict[str, Any]], topic: str, filename: str, *, root: str | Path = ARTIFACT_ROOT) -> Path:
    import csv

    path = artifact_path(topic, "tables", filename, root=root)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def save_matplotlib(
    figure: Any,
    topic: str,
    filename: str,
    *,
    kind: str = "figures",
    dpi: int = 160,
    root: str | Path = ARTIFACT_ROOT,
    **kwargs: Any,
) -> Path:
    path = artifact_path(topic, kind, filename, root=root)
    figure.savefig(path, dpi=dpi, bbox_inches="tight", **kwargs)
    return path


def save_plotly_html(
    figure: Any,
    topic: str,
    filename: str,
    *,
    root: str | Path = ARTIFACT_ROOT,
    include_plotlyjs: str | bool = "cdn",
    full_html: bool = True,
    **kwargs: Any,
) -> Path:
    path = artifact_path(topic, "html", filename, root=root)
    figure.write_html(path, include_plotlyjs=include_plotlyjs, full_html=full_html, **kwargs)
    return path


def save_image(image: Any, topic: str, filename: str, *, kind: str = "figures", root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_path(topic, kind, filename, root=root)
    save_kwargs = {"compress_level": 1} if path.suffix.lower() == ".png" else {}
    if isinstance(image, PILImage.Image):
        image.save(path, **save_kwargs)
        return path
    array = np.asarray(image)
    if array.dtype != np.uint8:
        if np.issubdtype(array.dtype, np.floating) and array.size and float(np.nanmax(array)) <= 1.0:
            array = array * 255.0
        array = np.clip(array, 0, 255).astype(np.uint8)
    if array.ndim == 2:
        PILImage.fromarray(array, mode="L").save(path, **save_kwargs)
    else:
        PILImage.fromarray(array).save(path, **save_kwargs)
    return path


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


def assert_artifacts(paths: list[str | Path], *, min_bytes: int = 1200) -> list[dict[str, Any]]:
    records = []
    for raw in paths:
        path = Path(raw)
        size = path.stat().st_size if path.exists() else 0
        threshold = 40 if path.suffix.lower() in {".json", ".csv", ".txt"} else min_bytes
        assert path.exists(), f"missing artifact: {path}"
        assert size >= threshold, f"artifact too small: {path} ({size} bytes)"
        records.append({"path": path.as_posix(), "bytes": int(size)})
    return records
