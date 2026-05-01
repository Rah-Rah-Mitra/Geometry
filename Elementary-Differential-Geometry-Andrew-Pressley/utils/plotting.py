"""Plotting helpers and visual quality checks for the Pressley course."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageStat

PALETTE = {
    "ink": "#1d2733",
    "blue": "#2f6fbb",
    "teal": "#2a9d8f",
    "green": "#6a994e",
    "gold": "#d59f0f",
    "red": "#c44e52",
    "violet": "#7b5ea7",
    "gray": "#7a8793",
    "paper": "#fbfcfe",
}


def set_defaults() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": PALETTE["paper"],
            "axes.facecolor": "white",
            "savefig.facecolor": PALETTE["paper"],
            "font.size": 10,
        }
    )


def style_axis(ax: Any, title: str, *, equal: bool = False, grid: bool = True) -> None:
    ax.set_title(title, fontsize=11, color=PALETTE["ink"])
    if grid:
        ax.grid(True, color="#d7dde5", linewidth=0.7, alpha=0.75)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in getattr(ax, "spines", {}).values():
        spine.set_color("#b6c0ca")


def note(ax: Any, text: str) -> None:
    ax.text(
        0.02,
        0.98,
        text,
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=8,
        color=PALETTE["ink"],
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "#d0d7de", "alpha": 0.92},
    )


def image_stats(path: str | Path) -> dict[str, Any]:
    resolved = Path(path)
    with Image.open(resolved) as image:
        image.load()
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
        arr = np.asarray(rgb, dtype=float)
    return {
        "width": int(rgb.width),
        "height": int(rgb.height),
        "bytes": resolved.stat().st_size,
        "pixel_std": float(arr.std()),
        "max_channel_stddev": float(max(stat.stddev) if stat.stddev else 0.0),
    }


def require_nonblank_png(path: str | Path, *, min_width: int = 64, min_height: int = 64, min_std: float = 1.0) -> dict[str, Any]:
    stats = image_stats(path)
    if stats["width"] < min_width or stats["height"] < min_height:
        raise ValueError(f"image too small: {path}")
    if stats["max_channel_stddev"] <= min_std:
        raise ValueError(f"image appears blank: {path}")
    return stats
