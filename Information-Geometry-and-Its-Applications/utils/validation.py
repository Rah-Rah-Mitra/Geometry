"""Validation helpers shared by notebooks and audits."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageStat


def assert_probability_vector(values: Any, *, atol: float = 1e-8) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if np.any(array < -atol):
        raise AssertionError("probability vector has negative entries")
    total = float(array.sum())
    if not np.isclose(total, 1.0, atol=atol):
        raise AssertionError(f"probability vector sums to {total}, not 1")
    return array


def assert_symmetric_positive_semidefinite(matrix: Any, *, atol: float = 1e-8) -> np.ndarray:
    array = np.asarray(matrix, dtype=float)
    if array.ndim != 2 or array.shape[0] != array.shape[1]:
        raise AssertionError("matrix must be square")
    if not np.allclose(array, array.T, atol=atol):
        raise AssertionError("matrix must be symmetric")
    eigvals = np.linalg.eigvalsh(array)
    if eigvals.min() < -atol:
        raise AssertionError(f"matrix has negative eigenvalue {eigvals.min()}")
    return eigvals


def assert_artifacts_exist(paths: list[str | Path], *, min_bytes: int = 1) -> list[dict[str, object]]:
    records = []
    for path in paths:
        p = Path(path)
        exists = p.exists()
        size = int(p.stat().st_size) if exists else 0
        if not exists:
            raise AssertionError(f"missing artifact: {p}")
        if size < min_bytes:
            raise AssertionError(f"artifact too small: {p} ({size} bytes)")
        records.append({"path": p.as_posix(), "exists": exists, "bytes": size})
    return records


def image_stats(path: str | Path) -> dict[str, float | int | str]:
    p = Path(path)
    with Image.open(p) as image:
        image.load()
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
        arr = np.asarray(rgb, dtype=float)
    return {
        "path": p.as_posix(),
        "width": int(rgb.width),
        "height": int(rgb.height),
        "bytes": int(p.stat().st_size),
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        "pixel_std": float(arr.std()),
        "max_channel_stddev": float(max(stat.stddev) if stat.stddev else 0.0),
    }


def assert_nonblank_image(path: str | Path, *, min_side: int = 96, min_stddev: float = 1.0) -> dict[str, float | int | str]:
    stats = image_stats(path)
    if stats["width"] < min_side or stats["height"] < min_side:
        raise AssertionError(f"image is too small: {stats}")
    if stats["max_channel_stddev"] <= min_stddev:
        raise AssertionError(f"image appears blank: {stats}")
    return stats
