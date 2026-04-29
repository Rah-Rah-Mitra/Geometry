"""Validation helpers shared by notebooks and audit scripts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .artifacts import assert_artifacts, image_stats, save_json


def validate_chapter_outputs(paths: dict[str, Any], *, min_pngs: int = 4) -> dict[str, Any]:
    figures = [Path(path) for path in paths.get("figures", [])]
    html = [Path(path) for path in paths.get("html", [])]
    checks = [Path(path) for path in paths.get("checks", [])]
    assert len(figures) >= min_pngs, f"expected at least {min_pngs} PNG figures"
    assert html, "expected at least one HTML artifact"
    assert checks, "expected at least one check artifact"
    assert_artifacts([*figures, *html, *checks])
    stats = [image_stats(path) for path in figures]
    for item in stats:
        if item["pixel_std"] < 2.0:
            raise AssertionError(f"image appears blank: {item['path']}")
    return {"figures": len(figures), "html": len(html), "checks": len(checks), "image_stats": stats}


def write_final_sanity(root: str | Path, paths: dict[str, Any], metrics: dict[str, Any]) -> Path:
    summary = validate_chapter_outputs(paths)
    summary["metrics"] = metrics
    return save_json(summary, root, "checks", "final-sanity.json")
