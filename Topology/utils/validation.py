"""Validation helpers for Topology notebooks and artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from utils.artifacts import image_stats


def assert_png_nonblank(path: str | Path, *, min_width: int = 300, min_height: int = 240, min_std: float = 2.0) -> dict[str, object]:
    stats = image_stats(path)
    if stats["width"] < min_width or stats["height"] < min_height:
        raise AssertionError(f"{path} is too small: {stats['width']}x{stats['height']}")
    if stats["pixel_std"] < min_std:
        raise AssertionError(f"{path} appears blank: std={stats['pixel_std']:.3f}")
    return stats


def assert_many_artifacts(paths: Iterable[str | Path], *, min_count: int = 3) -> None:
    values = [Path(p) for p in paths]
    if len(values) < min_count:
        raise AssertionError(f"Expected at least {min_count} artifacts, found {len(values)}")
    for path in values:
        if not path.exists() or path.stat().st_size <= 256:
            raise AssertionError(f"Artifact missing or too small: {path}")
