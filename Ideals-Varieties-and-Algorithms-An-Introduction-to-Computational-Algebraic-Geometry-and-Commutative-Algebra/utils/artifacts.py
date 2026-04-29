"""Book-local artifact helpers for the IVA course."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path
from typing import Any

from PIL import Image as PILImage
from PIL import ImageStat


BOOK_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-._")
    return slug or "artifact"


def ensure_parent(path: str | Path) -> Path:
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def save_json(data: Any, path: str | Path) -> Path:
    resolved = ensure_parent(path)
    resolved.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return resolved


def save_matplotlib(figure: Any, path: str | Path, *, dpi: int = 160, **kwargs: Any) -> Path:
    resolved = ensure_parent(path)
    figure.savefig(resolved, dpi=dpi, bbox_inches="tight", **kwargs)
    return resolved


def save_plotly_html(
    figure: Any,
    path: str | Path,
    *,
    include_plotlyjs: str | bool = True,
    full_html: bool = True,
    **kwargs: Any,
) -> Path:
    resolved = ensure_parent(path)
    figure.write_html(resolved, include_plotlyjs=include_plotlyjs, full_html=full_html, **kwargs)
    return resolved


def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
    from IPython.display import HTML, IFrame, Image, display

    resolved = Path(path)
    suffix = resolved.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        return display(Image(filename=str(resolved), width=width, height=height))
    if suffix in {".html", ".htm"}:
        html = resolved.read_text(encoding="utf-8")
        if height:
            return display(HTML(f'<div style="width:{width or "100%"};height:{height}px;overflow:auto">{html}</div>'))
        return display(HTML(html))
    link = escape(resolved.as_posix(), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))


def assert_artifacts_nonempty(paths: list[str | Path], *, min_bytes: int = 100) -> dict[str, int]:
    sizes: dict[str, int] = {}
    for path in paths:
        resolved = Path(path)
        if not resolved.exists():
            raise AssertionError(f"missing artifact: {resolved}")
        size = resolved.stat().st_size
        if size < min_bytes:
            raise AssertionError(f"artifact too small: {resolved} ({size} bytes)")
        sizes[resolved.name] = size
    return sizes


def image_nonblank(path: str | Path, *, min_stddev: float = 1.0) -> bool:
    with PILImage.open(path) as image:
        image.load()
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
    return max(stat.stddev) > min_stddev
