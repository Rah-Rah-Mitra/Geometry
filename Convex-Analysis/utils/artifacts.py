"""Artifact IO helpers for the Convex Analysis notebook course."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable


def find_book_root(start: Path | None = None) -> Path:
    current = Path.cwd() if start is None else Path(start).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "AGENTS.md").exists() and (candidate / "Convex Analysis.pdf").exists():
            return candidate
    raise RuntimeError("Could not find Convex Analysis book root")


def ensure_parent(path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Any, path: Path) -> Path:
    path = ensure_parent(path)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def save_csv(rows: Iterable[dict[str, Any]], path: Path) -> Path:
    path = ensure_parent(path)
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def save_matplotlib(fig: Any, path: Path, *, dpi: int = 160) -> Path:
    path = ensure_parent(path)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    return path


def relative_to_book(path: Path, book_root: Path | None = None) -> str:
    root = find_book_root() if book_root is None else Path(book_root).resolve()
    try:
        return Path(path).resolve().relative_to(root).as_posix()
    except ValueError:
        return Path(path).as_posix()


def assert_artifacts(paths: Iterable[Path], *, min_bytes: int = 64) -> None:
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


def display_artifact(path: Path, *, width: int = 760) -> None:
    from IPython.display import Image, Markdown, display

    candidate = Path(path)
    suffix = candidate.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg"}:
        display(Image(filename=str(candidate), width=width))
    else:
        display(Markdown(f"[{candidate.name}]({candidate.as_posix()})"))

