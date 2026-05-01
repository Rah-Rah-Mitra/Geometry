"""Shared plotting defaults and visual checks."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageStat

PALETTE = {
    "ink": "#1f2933",
    "blue": "#2f6fbb",
    "teal": "#2a9d8f",
    "green": "#6a994e",
    "gold": "#d59f0f",
    "red": "#c44e52",
    "violet": "#7b5ea7",
    "gray": "#7a8793",
    "paper": "#fbfcfe",
}

def style_axis(ax: Any, title: str, *, equal: bool = False, xlabel: str | None = None, ylabel: str | None = None) -> None:
    ax.set_title(title, fontsize=11, color=PALETTE["ink"])
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(True, color="#d7dde5", linewidth=0.7, alpha=0.8)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color("#b6c0ca")

def add_note(ax: Any, text: str) -> None:
    ax.text(0.02, 0.98, text, transform=ax.transAxes, va="top", ha="left", fontsize=8, color=PALETTE["ink"], bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#d0d7de", "alpha": 0.92})

def arrow2(ax: Any, origin: np.ndarray, vector: np.ndarray, *, color: str = PALETTE["blue"], label: str | None = None) -> None:
    origin = np.asarray(origin, dtype=float)
    vector = np.asarray(vector, dtype=float)
    ax.arrow(origin[0], origin[1], vector[0], vector[1], head_width=0.06, head_length=0.08, length_includes_head=True, color=color)
    if label:
        tip = origin + vector
        ax.text(tip[0], tip[1], label, color=color, fontsize=9)

def image_stats(path: str | Path) -> dict[str, float | int | str]:
    p = Path(path)
    with Image.open(p) as image:
        image.load()
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
        arr = np.asarray(rgb, dtype=float)
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    return {"path": p.as_posix(), "width": int(rgb.width), "height": int(rgb.height), "bytes": int(p.stat().st_size), "sha256": digest, "pixel_std": float(arr.std()), "max_channel_stddev": float(max(stat.stddev) if stat.stddev else 0.0)}

def close(fig: Any) -> None:
    plt.close(fig)
