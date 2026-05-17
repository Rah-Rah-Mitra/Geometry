"""Artifact helpers for the Geometry II notebook course."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable


def find_book_root(start: Path | None = None) -> Path:
    """Find the Geometry II course root by walking upward from ``start``."""

    current = Path.cwd() if start is None else Path(start).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
            return candidate
    raise RuntimeError("Could not find the Geometry II book root")


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(chapter: int, kind: str, filename: str, *, book_root: Path | None = None) -> Path:
    root = find_book_root() if book_root is None else Path(book_root)
    return root / "artifacts" / f"chapter-{chapter:02d}" / kind / filename


def save_json(data: Any, path: Path) -> Path:
    path = ensure_parent(Path(path))
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def save_csv(rows: Iterable[dict[str, Any]], path: Path) -> Path:
    path = ensure_parent(Path(path))
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def save_matplotlib(fig: Any, path: Path, *, dpi: int = 160) -> Path:
    path = ensure_parent(Path(path))
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    return path


def save_plotly_html(fig: Any, path: Path) -> Path:
    path = ensure_parent(Path(path))
    fig.write_html(str(path), include_plotlyjs="cdn", full_html=True)
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


def display_artifact(path: Path, *, width: int = 760, height: int = 520) -> None:
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
