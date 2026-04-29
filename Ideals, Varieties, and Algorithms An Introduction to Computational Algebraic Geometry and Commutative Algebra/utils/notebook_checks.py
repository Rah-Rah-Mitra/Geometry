"""Notebook validation helpers."""

from __future__ import annotations

from pathlib import Path

from .artifacts import assert_artifacts_nonempty, image_nonblank


def find_book_root(start: str | Path | None = None) -> Path:
    current = Path.cwd() if start is None else Path(start)
    for candidate in [current, *current.parents]:
        if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
            return candidate
    raise RuntimeError("Could not find IVA book root")


def assert_visuals(paths: list[str | Path]) -> dict[str, int]:
    sizes = assert_artifacts_nonempty(paths)
    for path in paths:
        resolved = Path(path)
        if resolved.suffix.lower() == ".png" and not image_nonblank(resolved):
            raise AssertionError(f"blank image artifact: {resolved}")
    return sizes
