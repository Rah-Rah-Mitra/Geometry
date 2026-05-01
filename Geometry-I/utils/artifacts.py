"""Artifact helpers for the Geometry I notebook course."""

from __future__ import annotations

import csv
import json
import re
from html import escape
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from PIL import Image as PILImage


def find_book_root(start: str | Path | None = None) -> Path:
    """Return the nearest parent containing the Geometry I PDF."""

    current = Path.cwd() if start is None else Path(start)
    current = current.resolve()
    candidates = [current, *current.parents]
    for candidate in candidates:
        if (candidate / "Geometry-I.pdf").exists():
            return candidate
    return Path(__file__).resolve().parents[1]


BOOK_ROOT = find_book_root(Path(__file__).resolve())
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-._")
    return slug or "artifact"


def ensure_parent(path: str | Path) -> Path:
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def artifact_dir(topic: str, kind: str = "figures", *, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = Path(root) / slugify(topic) / slugify(kind)
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(
    topic: str,
    filename: str,
    *,
    kind: str = "figures",
    root: str | Path = ARTIFACT_ROOT,
) -> Path:
    return ensure_parent(artifact_dir(topic, kind, root=root) / filename)


def save_json(
    data: Any,
    topic: str,
    filename: str = "data.json",
    *,
    kind: str = "checks",
    root: str | Path = ARTIFACT_ROOT,
) -> Path:
    path = artifact_path(topic, filename, kind=kind, root=root)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def save_csv(
    rows: Iterable[dict[str, Any]],
    topic: str,
    filename: str = "table.csv",
    *,
    kind: str = "tables",
    root: str | Path = ARTIFACT_ROOT,
) -> Path:
    rows = list(rows)
    path = artifact_path(topic, filename, kind=kind, root=root)
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
    close: bool = True,
    root: str | Path = ARTIFACT_ROOT,
    **kwargs: Any,
) -> Path:
    path = artifact_path(topic, filename, kind=kind, root=root)
    figure.savefig(path, dpi=dpi, bbox_inches="tight", **kwargs)
    if close:
        import matplotlib.pyplot as plt

        plt.close(figure)
    return path


def save_plotly_html(
    figure: Any,
    topic: str,
    filename: str,
    *,
    kind: str = "html",
    root: str | Path = ARTIFACT_ROOT,
    include_plotlyjs: str | bool = "cdn",
    full_html: bool = True,
    **kwargs: Any,
) -> Path:
    path = artifact_path(topic, filename, kind=kind, root=root)
    figure.write_html(path, include_plotlyjs=include_plotlyjs, full_html=full_html, **kwargs)
    return path


def save_image(
    image: Any,
    topic: str,
    filename: str,
    *,
    kind: str = "figures",
    root: str | Path = ARTIFACT_ROOT,
) -> Path:
    path = artifact_path(topic, filename, kind=kind, root=root)
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


def assert_artifacts_nonempty(paths: Iterable[str | Path], *, min_bytes: int = 32) -> dict[str, int]:
    report: dict[str, int] = {}
    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            raise AssertionError(f"missing artifact: {path}")
        size = path.stat().st_size
        if size < min_bytes:
            raise AssertionError(f"artifact too small: {path} ({size} bytes)")
        report[relative_to_book(path)] = size
    return report


def image_nonblank(path: str | Path, *, min_stddev: float = 1.0) -> dict[str, float | int]:
    with PILImage.open(path) as image:
        rgb = image.convert("RGB")
        array = np.asarray(rgb, dtype=float)
    stddev = float(array.std())
    if stddev < min_stddev:
        raise AssertionError(f"blank-looking image: {path} (stddev={stddev:.3f})")
    return {"width": int(rgb.width), "height": int(rgb.height), "pixel_stddev": stddev}


def relative_to_book(path: str | Path, *, root: str | Path = BOOK_ROOT) -> str:
    resolved = Path(path).resolve()
    try:
        return resolved.relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()
