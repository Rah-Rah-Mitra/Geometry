"""Artifact helpers for the Riemannian Geometry notebook course."""
from __future__ import annotations
import csv, json
from pathlib import Path
from typing import Any, Iterable

def find_book_root(start: Path | None = None) -> Path:
    current = Path.cwd() if start is None else Path(start).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "AGENTS.md").exists() and (candidate / "source_map.json").exists() and (candidate / "utils").exists():
            return candidate
    raise RuntimeError("Could not find book root")

def chapter_artifact_root(unit_key: str, book_root: Path | None = None) -> Path:
    root = find_book_root() if book_root is None else Path(book_root)
    path = root / "artifacts" / str(unit_key).replace("/", "__")
    for child in ["figures", "html", "checks", "tables"]:
        (path / child).mkdir(parents=True, exist_ok=True)
    return path

def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def save_json(data: Any, path: Path) -> Path:
    path = ensure_parent(Path(path))
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path

def save_csv(rows: Iterable[dict[str, Any]], path: Path) -> Path:
    path = ensure_parent(Path(path))
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path

def save_matplotlib(fig: Any, path: Path, *, dpi: int = 160) -> Path:
    path = ensure_parent(Path(path))
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    return path

def save_plotly_html(fig: Any, path: Path) -> Path:
    path = ensure_parent(Path(path))
    fig.write_html(str(path), include_plotlyjs="cdn", full_html=True)
    return path

def assert_artifacts(paths: Iterable[Path], *, min_bytes: int = 64) -> None:
    missing, tiny = [], []
    for path in paths:
        candidate = Path(path)
        if not candidate.exists():
            missing.append(str(candidate))
        elif candidate.stat().st_size < min_bytes:
            tiny.append(str(candidate))
    if missing or tiny:
        raise AssertionError("; ".join((["missing: " + ", ".join(missing)] if missing else []) + (["too small: " + ", ".join(tiny)] if tiny else [])))

def display_artifact(path: Path, *, width: int = 760, height: int = 520) -> None:
    from IPython.display import HTML, Image, Markdown, display
    candidate = Path(path)
    suffix = candidate.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg"}:
        display(Image(filename=str(candidate), width=width))
    elif suffix in {".html", ".htm"}:
        display(HTML(f'<iframe src="{candidate.as_posix()}" width="{width}" height="{height}"></iframe>'))
    elif suffix == ".json":
        display(Markdown(f"`{candidate.name}`"))
    else:
        display(Markdown(f"[{candidate.name}]({candidate.as_posix()})"))
