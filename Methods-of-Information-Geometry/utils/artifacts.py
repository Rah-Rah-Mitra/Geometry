"""Small artifact helpers for the Methods of Information Geometry course."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def find_book_root(start: Path | None = None) -> Path:
    """Walk upward until the course root marker is found."""
    path = (start or Path.cwd()).resolve()
    for candidate in [path, *path.parents]:
        if (candidate / "Methods of Information Geometry.djvu").exists() and (candidate / "AGENTS.md").exists():
            return candidate
    raise RuntimeError("Could not locate Methods-of-Information-Geometry course root")


BOOK_ROOT = find_book_root()
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"


def artifact_path(chapter: str, kind: str, filename: str) -> Path:
    path = ARTIFACT_ROOT / chapter / kind / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_matplotlib(fig: Any, chapter: str, filename: str, *, kind: str = "figures", dpi: int = 160) -> Path:
    path = artifact_path(chapter, kind, filename)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return path


def save_json(payload: Any, chapter: str, filename: str, *, kind: str = "checks") -> Path:
    path = artifact_path(chapter, kind, filename)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def save_text(text: str, chapter: str, filename: str, *, kind: str = "tables") -> Path:
    path = artifact_path(chapter, kind, filename)
    path.write_text(text, encoding="utf-8")
    return path


def require_artifacts(paths: list[Path], *, min_size: int = 100) -> dict[str, int]:
    sizes: dict[str, int] = {}
    for path in paths:
        if not path.exists():
            raise AssertionError(f"Missing artifact: {path}")
        size = path.stat().st_size
        if size < min_size:
            raise AssertionError(f"Artifact too small: {path} ({size} bytes)")
        sizes[str(path.relative_to(BOOK_ROOT)).replace("\\", "/")] = size
    return sizes


def display_artifact(path: Path) -> None:
    """Display a local artifact when running in Jupyter, otherwise print a path."""
    rel = path.relative_to(BOOK_ROOT)
    try:
        from IPython.display import HTML, Image, display

        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"}:
            display(Image(filename=str(path)))
        elif path.suffix.lower() in {".html", ".svg"}:
            display(HTML(path.read_text(encoding="utf-8")))
        else:
            print(rel)
    except Exception:
        print(rel)

