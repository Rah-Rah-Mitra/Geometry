"""Artifact helpers for the Multiple View Geometry notebook course."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable


BOOK_ROOT = Path(__file__).resolve().parents[1]


def find_book_root(start: Path | None = None) -> Path:
    current = Path.cwd() if start is None else Path(start).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
            return candidate
    return BOOK_ROOT


def artifact_path(topic: str, *parts: str, create: bool = True) -> Path:
    path = BOOK_ROOT / "artifacts" / topic
    for part in parts:
        path = path / part
    if create:
        path.parent.mkdir(parents=True, exist_ok=True)
    return path


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_matplotlib(fig: Any, topic: str, *parts: str, dpi: int = 160) -> Path:
    path = ensure_parent(artifact_path(topic, *parts))
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    return path


def save_plotly_html(fig: Any, topic: str, *parts: str) -> Path:
    path = ensure_parent(artifact_path(topic, *parts))
    fig.write_html(str(path), include_plotlyjs=True, full_html=True)
    return path


def save_image(image: Any, topic: str, *parts: str) -> Path:
    path = ensure_parent(artifact_path(topic, *parts))
    image.save(path)
    return path


def save_json(data: Any, topic: str, *parts: str) -> Path:
    path = ensure_parent(artifact_path(topic, *parts))
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def save_csv(rows: Iterable[dict[str, Any]], topic: str, *parts: str) -> Path:
    path = ensure_parent(artifact_path(topic, *parts))
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def save_text(text: str, topic: str, *parts: str) -> Path:
    path = ensure_parent(artifact_path(topic, *parts))
    path.write_text(text, encoding="utf-8")
    return path


def relative_to_book(path: Path, book_root: Path | None = None) -> str:
    root = find_book_root() if book_root is None else Path(book_root)
    try:
        return Path(path).resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return Path(path).as_posix()


def assert_artifacts(paths: Iterable[Path], *, min_bytes: int = 32) -> None:
    missing: list[str] = []
    tiny: list[str] = []
    for path in paths:
        candidate = Path(path)
        if not candidate.exists():
            missing.append(str(candidate))
        elif candidate.stat().st_size < min_bytes:
            tiny.append(str(candidate))
    if missing or tiny:
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if tiny:
            details.append("too small: " + ", ".join(tiny))
        raise AssertionError("; ".join(details))


def display_artifact(path: Path, *, width: int = 820, height: int = 540) -> None:
    from IPython.display import HTML, Image, Markdown, display

    candidate = Path(path)
    suffix = candidate.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg"}:
        display(Image(filename=str(candidate), width=width))
    elif suffix in {".html", ".htm"}:
        display(HTML(f'<iframe src="{candidate.as_posix()}" width="{width}" height="{height}"></iframe>'))
    elif suffix == ".json":
        display(Markdown(f"`{relative_to_book(candidate)}`"))
    else:
        display(Markdown(f"[{candidate.name}]({candidate.as_posix()})"))
