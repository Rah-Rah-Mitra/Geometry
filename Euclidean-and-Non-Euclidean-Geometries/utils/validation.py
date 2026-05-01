"""Validation helpers for the ENEG course scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-book-index.ipynb"}

SOURCE_MAP = [
    {
        "number": "00",
        "kind": "Introduction",
        "title": "Introduction",
        "folder": "chapter-00-introduction",
        "notebook": "00-introduction.ipynb",
        "printed": "1-5",
        "pdf": "19-23",
        "focus": "parallel problem, Euclidean vs non-Euclidean course map",
    },
    {
        "number": "01",
        "kind": "Chapter",
        "title": "Euclid's Geometry",
        "folder": "chapter-01-euclids-geometry",
        "notebook": "01-euclids-geometry.ipynb",
        "printed": "6-37",
        "pdf": "24-55",
        "focus": "postulates, construction diagrams, diagram ambiguity, parallel-postulate attempts",
    },
    {
        "number": "02",
        "kind": "Chapter",
        "title": "Logic and Incidence Geometry",
        "folder": "chapter-02-logic-and-incidence-geometry",
        "notebook": "02-logic-and-incidence-geometry.ipynb",
        "printed": "38-69",
        "pdf": "56-87",
        "focus": "proof-state diagrams, truth tables, finite incidence/projective/affine models",
    },
    {
        "number": "03",
        "kind": "Chapter",
        "title": "Hilbert's Axioms",
        "folder": "chapter-03-hilberts-axioms",
        "notebook": "03-hilberts-axioms.ipynb",
        "printed": "70-114",
        "pdf": "88-132",
        "focus": "axiom-family dependency graph, betweenness, congruence, continuity, parallelism",
    },
    {
        "number": "04",
        "kind": "Chapter",
        "title": "Neutral Geometry",
        "folder": "chapter-04-neutral-geometry",
        "notebook": "04-neutral-geometry.ipynb",
        "printed": "115-147",
        "pdf": "133-165",
        "focus": "Saccheri-Legendre, angle sums, equivalent parallel postulates",
    },
    {
        "number": "05",
        "kind": "Chapter",
        "title": "History of the Parallel Postulate",
        "folder": "chapter-05-history-of-the-parallel-postulate",
        "notebook": "05-history-of-the-parallel-postulate.ipynb",
        "printed": "148-176",
        "pdf": "166-194",
        "focus": "historical timeline, hidden assumptions, Saccheri/Lambert quadrilateral lab",
    },
    {
        "number": "06",
        "kind": "Chapter",
        "title": "Discovery of Non-Euclidean Geometry",
        "folder": "chapter-06-discovery-of-non-euclidean-geometry",
        "notebook": "06-discovery-of-non-euclidean-geometry.ipynb",
        "printed": "177-222",
        "pdf": "195-240",
        "focus": "hyperbolic geodesics, angle defect, limiting parallels, similar-triangle rigidity",
    },
    {
        "number": "07",
        "kind": "Chapter",
        "title": "Independence of the Parallel Postulate",
        "folder": "chapter-07-independence-of-the-parallel-postulate",
        "notebook": "07-independence-of-the-parallel-postulate.ipynb",
        "printed": "223-289",
        "pdf": "241-307",
        "focus": "Beltrami-Klein/Poincare models, inversion, cross-ratio distance, consistency",
    },
    {
        "number": "08",
        "kind": "Chapter",
        "title": "Philosophical Implications",
        "folder": "chapter-08-philosophical-implications",
        "notebook": "08-philosophical-implications.ipynb",
        "printed": "290-308",
        "pdf": "308-326",
        "focus": "physical-space models, axiom-choice diagrams, foundations map",
    },
    {
        "number": "09",
        "kind": "Chapter",
        "title": "Geometric Transformations",
        "folder": "chapter-09-geometric-transformations",
        "notebook": "09-geometric-transformations.ipynb",
        "printed": "309-385",
        "pdf": "327-403",
        "focus": "groups, reflections, motions, Mobius transformations, symmetry classification",
    },
    {
        "number": "10",
        "kind": "Chapter",
        "title": "Further Results in Hyperbolic Geometry",
        "folder": "chapter-10-further-results-in-hyperbolic-geometry",
        "notebook": "10-further-results-in-hyperbolic-geometry.ipynb",
        "printed": "386-437",
        "pdf": "404-455",
        "focus": "area defect, angle of parallelism, cycles, hyperbolic trig, pseudosphere mesh",
    },
    {
        "number": "A",
        "kind": "Appendix",
        "title": "Elliptic and Other Riemannian Geometries",
        "folder": "appendix-a-elliptic-and-other-riemannian-geometries",
        "notebook": "appendix-a-elliptic-and-other-riemannian-geometries.ipynb",
        "printed": "438-453",
        "pdf": "456-471",
        "focus": "elliptic/spherical/projective models, curvature, Riemannian metric intuition",
    },
    {
        "number": "B",
        "kind": "Appendix",
        "title": "Geometry Without Continuity",
        "folder": "appendix-b-geometry-without-continuity",
        "notebook": "appendix-b-geometry-without-continuity.ipynb",
        "printed": "454-460",
        "pdf": "472-478",
        "focus": "finite/non-continuous models, continuity failure examples",
    },
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


def notebook_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_sources(path: Path) -> list[str]:
    data = notebook_json(path)
    return ["".join(cell.get("source", "")) for cell in data.get("cells", []) if cell.get("cell_type") == "markdown"]


def code_sources(path: Path) -> list[str]:
    data = notebook_json(path)
    return ["".join(cell.get("source", "")) for cell in data.get("cells", []) if cell.get("cell_type") == "code"]


def artifact_topics() -> list[str]:
    return [item["folder"] for item in SOURCE_MAP]


def png_artifacts(book_root: Path = BOOK_ROOT) -> list[Path]:
    return sorted((book_root / "artifacts").rglob("*.png"))


def expected_canonical_paths(book_root: Path = BOOK_ROOT) -> list[Path]:
    return [book_root / item["folder"] / item["notebook"] for item in SOURCE_MAP]


def ensure_one_canonical_per_work_unit(book_root: Path = BOOK_ROOT) -> list[str]:
    findings: list[str] = []
    for item in SOURCE_MAP:
        folder = book_root / item["folder"]
        notebooks = sorted(path.name for path in folder.glob("*.ipynb") if path.name != "00-index.ipynb")
        if notebooks != [item["notebook"]]:
            findings.append(f"{item['folder']} has canonical notebooks {notebooks}, expected {item['notebook']}")
        if not (folder / "00-index.ipynb").exists():
            findings.append(f"{item['folder']} is missing 00-index.ipynb")
    return findings

