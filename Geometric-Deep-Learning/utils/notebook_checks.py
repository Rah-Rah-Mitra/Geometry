"""Validation helpers used inside notebooks and audit scripts."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageStat


def image_nonblank(path: str | Path, *, min_stddev: float = 1.0) -> float:
    """Assert that an image exists and has visible channel variation."""
    path = Path(path)
    if not path.exists():
        raise AssertionError(f"Missing image: {path}")
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
    stddev = max(stat.stddev) if stat.stddev else 0.0
    if stddev < min_stddev:
        raise AssertionError(f"Image appears blank: {path} stddev={stddev:.3f}")
    return float(stddev)


def file_size(path: str | Path, *, min_bytes: int = 100) -> int:
    """Assert that a file exists and is large enough to be meaningful."""
    path = Path(path)
    if not path.exists():
        raise AssertionError(f"Missing file: {path}")
    size = path.stat().st_size
    if size < min_bytes:
        raise AssertionError(f"File too small: {path} ({size} bytes)")
    return size

