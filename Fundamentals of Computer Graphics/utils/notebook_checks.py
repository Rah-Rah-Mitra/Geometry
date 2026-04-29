"""Validation helpers called from canonical notebooks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from .plotting import image_stats


def assert_close(name: str, value: Any, expected: Any, *, atol: float = 1e-8) -> dict[str, Any]:
    ok = bool(np.allclose(value, expected, atol=atol))
    assert ok, f"{name}: {value!r} != {expected!r}"
    return {"name": name, "ok": ok, "atol": atol}


def assert_nonblank_image(path: str | Path, *, min_std: float = 1.0) -> dict[str, Any]:
    stats = image_stats(path)
    assert stats["bytes"] > 1200, f"image too small: {path}"
    assert stats["max_channel_stddev"] > min_std, f"image appears blank: {path}"
    return stats
