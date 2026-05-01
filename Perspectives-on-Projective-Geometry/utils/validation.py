from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .artifacts import assert_artifacts, image_stats


def discover_book_root(start: str | Path) -> Path:
    path = Path(start).resolve()
    for candidate in [path, *path.parents]:
        if (candidate / "AGENTS.md").exists() and (
            candidate / "Perspectives on Projective Geometry.pdf"
        ).exists():
            return candidate
    raise RuntimeError("Could not discover the Perspectives course root")


def artifact_report(paths: Iterable[str | Path]) -> list[dict[str, object]]:
    report = []
    for path in paths:
        p = Path(path)
        item: dict[str, object] = {"path": p.as_posix(), "size": p.stat().st_size}
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            item.update(image_stats(p))
        report.append(item)
    return report


def write_sanity(path: str | Path, payload: dict[str, object]) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return out


def assert_course_artifacts(paths: Iterable[str | Path], min_size: int = 256) -> None:
    assert_artifacts(paths, min_size=min_size)

