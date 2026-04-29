"""Audit VDGF notebook visuals and generated PNG artifacts."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageStat

import vdgf_inventory as inventory


BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}
PLACEHOLDER_NAME = "constant-curvature-circles.png"
VISUAL_SAVE_CALLS = frozenset(
    {"save_image", "save_matplotlib", "save_plotly_html", "build_chapter_visual", "build_visual_storyboard"}
)


@dataclass(frozen=True)
class NotebookVisualStats:
    path: str
    visual_save_calls: int
    display_artifact_calls: int
    parse_errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class ImageStats:
    path: str
    topic: str
    width: int
    height: int
    bytes: int
    sha256: str
    max_channel_stddev: float


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def expected_artifact_topics() -> list[str]:
    """Return canonical VDGF artifact topics in inventory order."""

    if hasattr(inventory, "INVENTORY"):
        items = list(inventory.INVENTORY)
        return ["prologue" if item["id"] == "prologue" else f"chapter-{int(item['id']):02d}" for item in items]
    return ["prologue" if int(entry["number"]) == 0 else f"chapter-{int(entry['number']):02d}" for entry in inventory.ENTRIES]


def discover_notebooks(book_root: Path = BOOK_ROOT) -> list[Path]:
    artifact_root = Path(book_root) / "artifacts"
    return [
        path
        for path in sorted(Path(book_root).rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED_NOTEBOOKS
    ]


def _notebook_code_sources(path: Path) -> Iterable[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    for cell in data.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", "")
        yield "".join(source) if isinstance(source, list) else str(source)


def _call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def notebook_visual_stats(path: Path, book_root: Path = BOOK_ROOT) -> NotebookVisualStats:
    visual_save_calls = 0
    display_artifact_calls = 0
    parse_errors: list[str] = []

    for cell_index, source in enumerate(_notebook_code_sources(path), start=1):
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            parse_errors.append(f"cell {cell_index}: {exc.msg}")
            visual_save_calls += sum(source.count(f"{name}(") for name in VISUAL_SAVE_CALLS)
            display_artifact_calls += source.count("display_artifact(")
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = _call_name(node)
            if name in VISUAL_SAVE_CALLS:
                visual_save_calls += 1
            elif name == "display_artifact":
                display_artifact_calls += 1

    return NotebookVisualStats(
        path=_relative(path, Path(book_root)),
        visual_save_calls=visual_save_calls,
        display_artifact_calls=display_artifact_calls,
        parse_errors=tuple(parse_errors),
    )


def audit_notebook_displays(book_root: Path = BOOK_ROOT) -> tuple[list[NotebookVisualStats], list[dict[str, Any]]]:
    stats = [notebook_visual_stats(path, book_root) for path in discover_notebooks(book_root)]
    findings: list[dict[str, Any]] = []
    for item in stats:
        for error in item.parse_errors:
            findings.append(
                {
                    "check": "notebook-parse-error",
                    "path": item.path,
                    "message": f"Could not parse notebook code for visual audit: {error}.",
                    "details": {"error": error},
                }
            )
        if item.visual_save_calls == 0:
            findings.append(
                {
                    "check": "missing-visual-save",
                    "path": item.path,
                    "message": "Notebook has no static or interactive visual save call.",
                    "details": {"visual_save_calls": item.visual_save_calls},
                }
            )
        if item.display_artifact_calls < item.visual_save_calls:
            findings.append(
                {
                    "check": "missing-display-artifact",
                    "path": item.path,
                    "message": (
                        f"Notebook saves {item.visual_save_calls} visual artifact(s) but calls "
                        f"display_artifact {item.display_artifact_calls} time(s)."
                    ),
                    "details": {
                        "visual_save_calls": item.visual_save_calls,
                        "display_artifact_calls": item.display_artifact_calls,
                    },
                }
            )
    return stats, findings


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_stats(path: Path, topic: str, book_root: Path = BOOK_ROOT) -> ImageStats:
    with Image.open(path) as image:
        image.load()
        width, height = image.size
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
    return ImageStats(
        path=_relative(path, Path(book_root)),
        topic=topic,
        width=width,
        height=height,
        bytes=path.stat().st_size,
        sha256=_sha256(path),
        max_channel_stddev=max(stat.stddev) if stat.stddev else 0.0,
    )


def _topic_pngs(artifact_root: Path, topic: str) -> list[Path]:
    topic_root = artifact_root / topic
    if not topic_root.exists():
        return []
    return sorted(topic_root.rglob("*.png"))


def audit_png_artifacts(
    book_root: Path = BOOK_ROOT,
    *,
    expected_topics: Iterable[str] | None = None,
    min_width: int = 64,
    min_height: int = 64,
    min_pixels: int = 4096,
    blank_stddev: float = 1.0,
    allowed_placeholder_count: int = 0,
) -> tuple[list[ImageStats], list[dict[str, Any]]]:
    root = Path(book_root)
    artifact_root = root / "artifacts"
    topics = expected_artifact_topics() if expected_topics is None else list(expected_topics)
    findings: list[dict[str, Any]] = []
    stats: list[ImageStats] = []
    png_paths: list[Path] = []

    for topic in topics:
        topic_pngs = _topic_pngs(artifact_root, topic)
        png_paths.extend(topic_pngs)
        chapter_specific_pngs = [path for path in topic_pngs if path.name != PLACEHOLDER_NAME]
        if not chapter_specific_pngs:
            findings.append(
                {
                    "check": "missing-chapter-specific-png",
                    "path": _relative(artifact_root / topic, root),
                    "message": f"{topic} has no non-placeholder PNG artifact.",
                    "details": {"png_count": len(topic_pngs)},
                }
            )

    for path in png_paths:
        topic = path.relative_to(artifact_root).parts[0]
        try:
            item = image_stats(path, topic, root)
        except OSError as exc:
            findings.append(
                {
                    "check": "unreadable-image",
                    "path": _relative(path, root),
                    "message": f"Could not read PNG image: {exc}.",
                    "details": {"error": str(exc)},
                }
            )
            continue
        stats.append(item)
        if item.width < min_width or item.height < min_height or item.width * item.height < min_pixels:
            findings.append(
                {
                    "check": "tiny-image",
                    "path": item.path,
                    "message": f"PNG is too small at {item.width}x{item.height}px.",
                    "details": {"width": item.width, "height": item.height},
                }
            )
        if item.max_channel_stddev <= blank_stddev:
            findings.append(
                {
                    "check": "blank-image",
                    "path": item.path,
                    "message": "PNG appears blank or nearly constant.",
                    "details": {"max_channel_stddev": item.max_channel_stddev},
                }
            )

    by_hash: dict[str, list[ImageStats]] = {}
    for item in stats:
        by_hash.setdefault(item.sha256, []).append(item)
    for digest, matches in sorted(by_hash.items(), key=lambda pair: pair[0]):
        if len(matches) <= 1:
            continue
        findings.append(
            {
                "check": "duplicate-png-hash",
                "path": matches[0].path,
                "message": f"{len(matches)} PNG artifacts share SHA256 {digest[:12]}.",
                "details": {"sha256": digest, "paths": [item.path for item in matches]},
            }
        )

    placeholder_paths = [item.path for item in stats if Path(item.path).name == PLACEHOLDER_NAME]
    if len(placeholder_paths) > allowed_placeholder_count:
        findings.append(
            {
                "check": "repeated-placeholder-png",
                "path": placeholder_paths[0],
                "message": f"Forbidden placeholder {PLACEHOLDER_NAME!r} appears {len(placeholder_paths)} time(s).",
                "details": {
                    "placeholder_name": PLACEHOLDER_NAME,
                    "allowed_count": allowed_placeholder_count,
                    "paths": placeholder_paths,
                },
            }
        )
    return stats, findings


def audit_visuals(
    book_root: Path = BOOK_ROOT,
    *,
    expected_topics: Iterable[str] | None = None,
    min_width: int = 64,
    min_height: int = 64,
    min_pixels: int = 4096,
    blank_stddev: float = 1.0,
    allowed_placeholder_count: int = 0,
) -> dict[str, Any]:
    notebooks, notebook_findings = audit_notebook_displays(book_root)
    images, image_findings = audit_png_artifacts(
        book_root,
        expected_topics=expected_topics,
        min_width=min_width,
        min_height=min_height,
        min_pixels=min_pixels,
        blank_stddev=blank_stddev,
        allowed_placeholder_count=allowed_placeholder_count,
    )
    findings = [*notebook_findings, *image_findings]
    return {
        "summary": {
            "notebook_count": len(notebooks),
            "png_count": len(images),
            "finding_count": len(findings),
        },
        "findings": findings,
        "notebooks": [asdict(item) for item in notebooks],
        "images": [asdict(item) for item in images],
    }


def print_text_report(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print(f"Audited {summary['notebook_count']} notebooks and {summary['png_count']} PNGs")
    findings = report["findings"]
    if not findings:
        print("All VDGF visual audit checks passed.")
        return
    print(f"{len(findings)} visual audit finding(s):")
    for finding in findings:
        path = finding.get("path", "")
        location = f" [{path}]" if path else ""
        print(f"- {finding['check']}{location}: {finding['message']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book-root", type=Path, default=BOOK_ROOT)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-fail", action="store_true", help="Report findings without a nonzero exit.")
    parser.add_argument("--min-width", type=int, default=64)
    parser.add_argument("--min-height", type=int, default=64)
    parser.add_argument("--min-pixels", type=int, default=4096)
    parser.add_argument("--blank-stddev", type=float, default=1.0)
    parser.add_argument("--allowed-placeholder-count", type=int, default=0)
    args = parser.parse_args()

    report = audit_visuals(
        args.book_root,
        min_width=args.min_width,
        min_height=args.min_height,
        min_pixels=args.min_pixels,
        blank_stddev=args.blank_stddev,
        allowed_placeholder_count=args.allowed_placeholder_count,
    )
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_text_report(report)
    if report["summary"]["finding_count"] and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
