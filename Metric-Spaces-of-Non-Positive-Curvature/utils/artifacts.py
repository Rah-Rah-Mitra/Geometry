"""Artifact helpers for the Bridson-Haefliger notebook course."""
from __future__ import annotations
import json, re
from html import escape
from pathlib import Path
from typing import Any
BOOK_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"
def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    return re.sub(r"-+", "-", slug).strip("-._") or "artifact"
def artifact_dir(unit_id: str, kind: str | None = None) -> Path:
    path = ARTIFACT_ROOT / slugify(unit_id)
    if kind:
        path = path / slugify(kind)
    path.mkdir(parents=True, exist_ok=True)
    return path
def artifact_path(unit_id: str, kind: str | None, filename: str) -> Path:
    return artifact_dir(unit_id, kind) / filename
def save_json(data: Any, unit_id: str, kind: str | None, filename: str) -> Path:
    path = artifact_path(unit_id, kind, filename)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path
def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))
def assert_artifact(path: str | Path, *, min_bytes: int = 512) -> Path:
    resolved = Path(path)
    if not resolved.exists():
        raise FileNotFoundError(resolved)
    if resolved.stat().st_size < min_bytes:
        raise AssertionError(f"{resolved} is unexpectedly small")
    return resolved
def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
    from IPython.display import HTML, IFrame, Image, display
    resolved = Path(path)
    suffix = resolved.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        return display(Image(filename=str(resolved), width=width, height=height))
    if suffix in {".html", ".htm"}:
        return display(IFrame(src=str(resolved), width=width or "100%", height=height or 360))
    link = escape(resolved.as_posix(), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))
