"""Validation helpers shared by notebooks and audit scripts."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


def assert_artifact(path: str | Path, min_size: int = 1000) -> Path:
    resolved = Path(path)
    assert resolved.exists(), f"missing artifact: {resolved}"
    assert resolved.stat().st_size >= min_size, f"artifact too small: {resolved}"
    return resolved


def image_stats(path: str | Path) -> dict[str, float | int]:
    image = Image.open(path).convert("RGB")
    arr = np.asarray(image, dtype=float)
    return {
        "width": image.width,
        "height": image.height,
        "file_size": Path(path).stat().st_size,
        "pixel_std": float(arr.std()),
    }

