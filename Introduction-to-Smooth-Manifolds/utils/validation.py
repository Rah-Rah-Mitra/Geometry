"""Validation helpers for this visualization-first notebook course."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from PIL import Image, ImageStat
from .source import COURSE_MAP
BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-book-index.ipynb"}
def relative(path: Path, root: Path | None = None) -> str:
    base = BOOK_ROOT if root is None else root
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
def canonical_notebooks(book_root: Path = BOOK_ROOT) -> list[Path]:
    artifact_root = book_root / "artifacts"
    return [p for p in sorted(book_root.rglob("*.ipynb")) if artifact_root not in p.parents and p.name not in IGNORED_NOTEBOOKS]
def index_notebooks(book_root: Path = BOOK_ROOT) -> list[Path]:
    artifact_root = book_root / "artifacts"
    return [p for p in sorted(book_root.rglob("*.ipynb")) if artifact_root not in p.parents and p.name in IGNORED_NOTEBOOKS]
def notebook_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
def markdown_sources(path: Path) -> list[str]:
    data = notebook_json(path)
    return ["".join(c.get("source", "")) for c in data.get("cells", []) if c.get("cell_type") == "markdown"]
def code_sources(path: Path) -> list[str]:
    data = notebook_json(path)
    return ["".join(c.get("source", "")) for c in data.get("cells", []) if c.get("cell_type") == "code"]
def artifact_topics() -> list[str]:
    return [item["artifact_key"] for item in COURSE_MAP]
def image_stats(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        width, height = image.size
        stat = ImageStat.Stat(image.convert("RGB"))
    return {"path": relative(path), "width": width, "height": height, "bytes": path.stat().st_size, "max_channel_stddev": max(stat.stddev) if stat.stddev else 0.0}
def ensure_one_canonical_per_unit(book_root: Path = BOOK_ROOT) -> list[str]:
    findings: list[str] = []
    for item in COURSE_MAP:
        folder = book_root / item["folder_path"]
        if not folder.exists():
            findings.append(f"{item['folder_path']} is missing")
            continue
        notebooks = sorted(p.name for p in folder.glob("*.ipynb") if p.name != "00-index.ipynb")
        if notebooks != [item["notebook"]]:
            findings.append(f"{item['folder_path']} canonical notebooks should be {[item['notebook']]} but found {notebooks}")
        if not (folder / "00-index.ipynb").exists():
            findings.append(f"{item['folder_path']} is missing 00-index.ipynb")
    return findings
