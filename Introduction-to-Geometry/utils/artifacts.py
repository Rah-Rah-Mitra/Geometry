from __future__ import annotations
import csv, json
from pathlib import Path
from typing import Any, Iterable
from IPython.display import HTML, Image, display
from .course import book_root
ARTIFACT_KINDS = ("figures", "html", "checks", "tables", "data")
def artifact_dir(chapter_no: int, kind: str = "figures", root: Path | None = None) -> Path:
    if kind not in ARTIFACT_KINDS:
        raise ValueError(f"unknown artifact kind {kind!r}")
    base = (root or book_root()) / "artifacts" / f"chapter-{chapter_no:02d}" / kind
    base.mkdir(parents=True, exist_ok=True)
    return base
def artifact_path(chapter_no: int, kind: str, filename: str, root: Path | None = None) -> Path:
    return artifact_dir(chapter_no, kind, root) / filename
def ensure_chapter_artifact_dirs(chapter_no: int, root: Path | None = None) -> dict[str, Path]:
    return {kind: artifact_dir(chapter_no, kind, root) for kind in ARTIFACT_KINDS}
def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"); return path
def write_csv(path: Path, rows: Iterable[dict[str, Any]]) -> Path:
    rows = list(rows); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        if not rows:
            handle.write(""); return path
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys())); writer.writeheader(); writer.writerows(rows)
    return path
def display_artifact(path: str | Path, width: int | None = None) -> None:
    path = Path(path); suffix = path.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif"}: display(Image(filename=str(path), width=width))
    elif suffix in {".svg", ".html"}: display(HTML(path.read_text(encoding="utf-8")))
    else: display(HTML(f'<a href="{path.as_posix()}">{path.name}</a>'))
def assert_artifacts(paths: Iterable[str | Path], min_bytes: int = 100) -> None:
    missing, small = [], []
    for raw in paths:
        path = Path(raw)
        if not path.exists(): missing.append(str(path))
        elif path.stat().st_size < min_bytes: small.append(str(path))
    if missing or small: raise AssertionError({"missing": missing, "too_small": small})
