"""Validation helpers for the GMAM notebook course."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat


BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-book-index.ipynb"}
COURSE_MAP = [
    {
        "number": 1,
        "title": "Preliminary Notions",
        "slug": "preliminary-notions",
        "folder": "chapter-01-preliminary-notions",
        "notebook": "01-preliminary-notions.ipynb",
        "printed": "1-16",
        "pdf": "16-31",
        "sections": "1.1-1.3",
        "focus": "Axioms, models, equivalence relations, and functions."
    },
    {
        "number": 2,
        "title": "Incidence and Metric Geometry",
        "slug": "incidence-and-metric-geometry",
        "folder": "chapter-02-incidence-and-metric-geometry",
        "notebook": "02-incidence-and-metric-geometry.ipynb",
        "printed": "17-41",
        "pdf": "32-56",
        "sections": "2.1-2.3",
        "focus": "Incidence models, metric geometry, and special coordinate systems."
    },
    {
        "number": 3,
        "title": "Betweenness and Elementary Figures",
        "slug": "betweenness-and-elementary-figures",
        "folder": "chapter-03-betweenness-and-elementary-figures",
        "notebook": "03-betweenness-and-elementary-figures.ipynb",
        "printed": "42-62",
        "pdf": "57-77",
        "sections": "3.1-3.4",
        "focus": "Alternative Cartesian descriptions, betweenness, segments, rays, angles, and triangles."
    },
    {
        "number": 4,
        "title": "Plane Separation",
        "slug": "plane-separation",
        "folder": "chapter-04-plane-separation",
        "notebook": "04-plane-separation.ipynb",
        "printed": "63-89",
        "pdf": "78-104",
        "sections": "4.1-4.5",
        "focus": "Plane separation, Pasch geometries, interiors, crossbar theorem, and convex quadrilaterals."
    },
    {
        "number": 5,
        "title": "Angle Measure",
        "slug": "angle-measure",
        "folder": "chapter-05-angle-measure",
        "notebook": "05-angle-measure.ipynb",
        "printed": "90-123",
        "pdf": "105-138",
        "sections": "5.1-5.4",
        "focus": "Angle measure, Molton plane, perpendicularity, angle congruence, and Poincare angle measure."
    },
    {
        "number": 6,
        "title": "Neutral Geometry",
        "slug": "neutral-geometry",
        "folder": "chapter-06-neutral-geometry",
        "notebook": "06-neutral-geometry.ipynb",
        "printed": "124-168",
        "pdf": "139-183",
        "sections": "6.1-6.7",
        "focus": "SAS, triangle congruence, exterior angle theorem, right triangles, circles and tangent lines, and synthetic proof flow."
    },
    {
        "number": 7,
        "title": "The Theory of Parallels",
        "slug": "the-theory-of-parallels",
        "folder": "chapter-07-the-theory-of-parallels",
        "notebook": "07-the-theory-of-parallels.ipynb",
        "printed": "169-195",
        "pdf": "184-210",
        "sections": "7.1-7.3",
        "focus": "Parallel lines, Saccheri quadrilaterals, and the critical function."
    },
    {
        "number": 8,
        "title": "Hyperbolic Geometry",
        "slug": "hyperbolic-geometry",
        "folder": "chapter-08-hyperbolic-geometry",
        "notebook": "08-hyperbolic-geometry.ipynb",
        "printed": "196-223",
        "pdf": "211-238",
        "sections": "8.1-8.3",
        "focus": "Asymptotic rays, triangle defect, and distance between parallel lines."
    },
    {
        "number": 9,
        "title": "Euclidean Geometry",
        "slug": "euclidean-geometry",
        "folder": "chapter-09-euclidean-geometry",
        "notebook": "09-euclidean-geometry.ipynb",
        "printed": "224-247",
        "pdf": "239-262",
        "sections": "9.1-9.3",
        "focus": "Equivalent forms of the Euclidean parallel postulate, similarity theory, and classical Euclidean theorems."
    },
    {
        "number": 10,
        "title": "Area",
        "slug": "area",
        "folder": "chapter-10-area",
        "notebook": "10-area.ipynb",
        "printed": "248-284",
        "pdf": "263-299",
        "sections": "10.1-10.4",
        "focus": "Area functions, Euclidean area, hyperbolic area, and Bolyai's theorem."
    },
    {
        "number": 11,
        "title": "The Theory of Isometries",
        "slug": "the-theory-of-isometries",
        "folder": "chapter-11-the-theory-of-isometries",
        "notebook": "11-the-theory-of-isometries.ipynb",
        "printed": "285-358",
        "pdf": "300-373",
        "sections": "11.1-11.9",
        "focus": "Collineations, Klein and Poincare disk models, reflections, pencils, cycles, double reflections, classification, and isometry groups."
    }
]


def relative(path: Path, root: Path | None = None) -> str:
    base = BOOK_ROOT.parent if root is None else root
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def canonical_notebooks(book_root: Path = BOOK_ROOT) -> list[Path]:
    artifact_root = book_root / "artifacts"
    return [
        path
        for path in sorted(book_root.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED_NOTEBOOKS
    ]


def index_notebooks(book_root: Path = BOOK_ROOT) -> list[Path]:
    artifact_root = book_root / "artifacts"
    return [
        path
        for path in sorted(book_root.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name in IGNORED_NOTEBOOKS
    ]


def notebook_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_sources(path: Path) -> list[str]:
    data = notebook_json(path)
    return ["".join(cell.get("source", "")) for cell in data.get("cells", []) if cell.get("cell_type") == "markdown"]


def code_sources(path: Path) -> list[str]:
    data = notebook_json(path)
    return ["".join(cell.get("source", "")) for cell in data.get("cells", []) if cell.get("cell_type") == "code"]


def artifact_topics() -> list[str]:
    return [f"chapter-{i:02d}" for i in range(1, 12)]


def png_artifacts(book_root: Path = BOOK_ROOT) -> list[Path]:
    return sorted((book_root / "artifacts").rglob("*.png"))


def image_stats(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        width, height = image.size
        stat = ImageStat.Stat(image.convert("RGB"))
    return {
        "path": relative(path, BOOK_ROOT),
        "width": width,
        "height": height,
        "bytes": path.stat().st_size,
        "max_channel_stddev": max(stat.stddev) if stat.stddev else 0.0,
    }


def ensure_one_canonical_per_chapter(book_root: Path = BOOK_ROOT) -> list[str]:
    findings: list[str] = []
    for item in COURSE_MAP:
        folder = book_root / item["folder"]
        if not folder.exists():
            findings.append(f"{item['folder']} is missing")
            continue
        notebooks = sorted(path.name for path in folder.glob("*.ipynb") if path.name != "00-index.ipynb")
        if notebooks != [item["notebook"]]:
            findings.append(f"{folder.name} canonical notebooks should be {[item['notebook']]} but found {notebooks}")
        if not (folder / "00-index.ipynb").exists():
            findings.append(f"{folder.name} is missing 00-index.ipynb")
    return findings
