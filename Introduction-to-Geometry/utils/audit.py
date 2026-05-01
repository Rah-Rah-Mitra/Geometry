"""Reusable audit helpers for Introduction to Geometry notebooks."""

from __future__ import annotations

import ast
import hashlib
import re
from pathlib import Path
from typing import Any

from .course import (
    BOOK_ROOT,
    VISUAL_EXTENSIONS,
    canonical_notebooks,
    chapter_inventory,
    code_sources,
    ensure_one_canonical_per_chapter,
    first_markdown_heading,
    iter_artifacts,
    markdown_sources,
    relative,
)

VISUAL_SAVE_CALLS = {
    "save_matplotlib",
    "save_plotly_html",
    "save_figure",
    "savefig",
    "write_html",
    "write_image",
    "write_json",
}

DISPLAY_CALLS = {
    "display_artifact",
    "display",
    "Image",
    "HTML",
    "SVG",
}

PDF_RASTERIZATION_MARKERS = {
    "pdf2image",
    "convert_from_path",
    "get_pixmap",
    "page.get_pixmap",
    "fitz.open",
    "pymupdf",
}

TAKEAWAY_MARKERS = {
    "takeaways",
    "what to remember",
    "summary",
}

SANITY_MARKERS = {
    "assert_artifacts",
    "final_sanity",
    "sanity",
    "assert ",
}

WINDOWS_PATH_RE = re.compile(r"[A-Za-z]:[\\/][^\s)'\"<>]+")
POSIX_HOME_RE = re.compile(r"(?<![A-Za-z0-9_])/(?:home|users|mnt|tmp)/[^\s)'\"<>]+")


def call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def notebook_metrics(path: Path) -> dict[str, Any]:
    markdown = markdown_sources(path)
    code = code_sources(path)
    markdown_text = "\n".join(markdown)
    code_text = "\n".join(code)
    return {
        "path": relative(path),
        "title": first_markdown_heading(path),
        "markdown_words": len(markdown_text.split()),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "has_setup": "BOOK_ROOT" in code_text or "find_book_root" in code_text,
        "has_artifact_root": "ARTIFACT_ROOT" in code_text or "artifact_path" in code_text,
        "has_sanity": any(marker in code_text for marker in SANITY_MARKERS),
        "has_takeaways": any(marker in markdown_text.lower() for marker in TAKEAWAY_MARKERS),
        "hardcoded_paths": hardcoded_paths([markdown_text, code_text]),
        "pdf_rasterization_markers": pdf_rasterization_markers(code_text),
    }


def hardcoded_paths(sources: list[str]) -> list[str]:
    matches: list[str] = []
    for source in sources:
        matches.extend(WINDOWS_PATH_RE.findall(source))
        matches.extend(POSIX_HOME_RE.findall(source))
        if "file://" in source:
            matches.append("file://")
    return sorted(set(matches))


def pdf_rasterization_markers(source: str) -> list[str]:
    lowered = source.lower()
    return sorted(marker for marker in PDF_RASTERIZATION_MARKERS if marker in lowered)


def audit_notebook_depth(
    *,
    book_root: Path = BOOK_ROOT,
    min_words: int = 1200,
    min_code_cells: int = 5,
) -> dict[str, Any]:
    notebooks = canonical_notebooks(book_root)
    stats = [notebook_metrics(path) for path in notebooks]
    findings: list[dict[str, Any]] = []

    for item in stats:
        if item["markdown_words"] < min_words:
            findings.append({**item, "check": "below-word-threshold"})
        if item["code_cells"] < min_code_cells:
            findings.append({**item, "check": "below-code-cell-threshold"})
        if not item["has_setup"]:
            findings.append({**item, "check": "missing-book-root-setup"})
        if not item["has_artifact_root"]:
            findings.append({**item, "check": "missing-artifact-root"})
        if not item["has_sanity"]:
            findings.append({**item, "check": "missing-sanity-check"})
        if not item["has_takeaways"]:
            findings.append({**item, "check": "missing-takeaways"})
        if item["hardcoded_paths"]:
            findings.append({**item, "check": "hardcoded-path"})
        if item["pdf_rasterization_markers"]:
            findings.append({**item, "check": "possible-pdf-rasterization"})

    findings.extend(ensure_one_canonical_per_chapter(book_root))
    return {
        "summary": {
            "notebook_count": len(stats),
            "chapter_folder_count": len(chapter_inventory(book_root)),
            "finding_count": len(findings),
        },
        "findings": findings,
        "notebooks": stats,
    }


def visual_call_stats(path: Path) -> dict[str, Any]:
    saves = 0
    displays = 0
    parse_errors: list[str] = []
    calls: list[str] = []

    for source in code_sources(path):
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            parse_errors.append(str(exc))
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = call_name(node)
                if name is None:
                    continue
                calls.append(name)
                if name in VISUAL_SAVE_CALLS:
                    saves += 1
                if name in DISPLAY_CALLS:
                    displays += 1

    return {
        "path": relative(path),
        "visual_save_calls": saves,
        "display_calls": displays,
        "parse_errors": parse_errors,
        "calls": sorted(set(calls)),
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_stats(path: Path) -> dict[str, Any]:
    from PIL import Image, ImageStat

    with Image.open(path) as image:
        image.load()
        width, height = image.size
        stat = ImageStat.Stat(image.convert("RGB"))
    return {
        "path": relative(path, BOOK_ROOT),
        "width": width,
        "height": height,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "max_channel_stddev": max(stat.stddev) if stat.stddev else 0.0,
    }


def artifact_file_stats(path: Path) -> dict[str, Any]:
    item = {
        "path": relative(path, BOOK_ROOT),
        "bytes": path.stat().st_size,
        "suffix": path.suffix.lower(),
        "sha256": sha256(path),
    }
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        item.update(image_stats(path))
    return item


def audit_visuals(
    *,
    book_root: Path = BOOK_ROOT,
    min_width: int = 64,
    min_height: int = 64,
    blank_stddev: float = 1.0,
) -> dict[str, Any]:
    notebooks = canonical_notebooks(book_root)
    notebook_stats = [visual_call_stats(path) for path in notebooks]
    findings: list[dict[str, Any]] = []

    for item in notebook_stats:
        if item["parse_errors"]:
            findings.append({"check": "parse-error", **item})
        if item["visual_save_calls"] == 0:
            findings.append({"check": "missing-visual-save", **item})
        if item["display_calls"] == 0:
            findings.append({"check": "missing-visual-display", **item})

    artifact_paths = iter_artifacts(book_root, VISUAL_EXTENSIONS)
    artifact_stats = [artifact_file_stats(path) for path in artifact_paths]
    by_hash: dict[str, list[str]] = {}

    for item in artifact_stats:
        by_hash.setdefault(item["sha256"], []).append(item["path"])
        if item["bytes"] < 32:
            findings.append({"check": "tiny-artifact", **item})
        if "width" in item:
            if item["width"] < min_width or item["height"] < min_height:
                findings.append({"check": "tiny-image", **item})
            if item["max_channel_stddev"] <= blank_stddev:
                findings.append({"check": "blank-image", **item})

    for digest, paths in by_hash.items():
        if len(paths) > 1:
            findings.append({"check": "duplicate-artifact-hash", "sha256": digest, "paths": paths})

    for chapter in chapter_inventory(book_root):
        if chapter["canonical_notebooks"]:
            topic_root = book_root / "artifacts" / chapter["artifact_topic"]
            if not topic_root.exists():
                findings.append(
                    {
                        "check": "missing-chapter-artifact-root",
                        "path": relative(topic_root),
                    }
                )

    return {
        "summary": {
            "notebook_count": len(notebook_stats),
            "visual_artifact_count": len(artifact_stats),
            "finding_count": len(findings),
        },
        "findings": findings,
        "notebooks": notebook_stats,
        "artifacts": artifact_stats,
    }
