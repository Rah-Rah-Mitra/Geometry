"""Artifact helpers for the Hodge theory notebook course."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .course_data import Chapter, course_root_from


def chapter_artifact_dir(chapter: Chapter, course_root: Path | None = None) -> Path:
    root = course_root or course_root_from()
    return root / "artifacts" / f"volume-{chapter.volume:02d}" / chapter.id


def ensure_artifact_dirs(chapter: Chapter, course_root: Path | None = None) -> dict[str, Path]:
    base = chapter_artifact_dir(chapter, course_root)
    paths = {
        "base": base,
        "figures": base / "figures",
        "checks": base / "checks",
        "interactive": base / "interactive",
        "tables": base / "tables",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def artifact_manifest_entry(path: Path, root: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "path": path.relative_to(root).as_posix(),
        "bytes": stat.st_size,
        "suffix": path.suffix.lower(),
    }


def display_artifact(path: str | Path, width: int = 780) -> None:
    """Display a local artifact in a notebook when IPython is available."""
    artifact_path = Path(path)
    try:
        from IPython.display import HTML, Image, display
    except Exception:
        print(artifact_path.as_posix())
        return

    suffix = artifact_path.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif"}:
        display(Image(filename=str(artifact_path), width=width))
    elif suffix == ".svg":
        display(HTML(artifact_path.read_text(encoding="utf-8")))
    elif suffix == ".html":
        display(
            HTML(
                f'<iframe src="{artifact_path.as_posix()}" '
                f'width="{width}" height="520" style="border:1px solid #ddd"></iframe>'
            )
        )
    else:
        print(artifact_path.as_posix())

