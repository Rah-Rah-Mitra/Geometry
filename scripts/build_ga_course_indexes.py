"""Rebuild the GA course book and part index notebooks.

The authored chapter notebooks live one per chapter/appendix folder.  This
script keeps the navigation notebooks aligned with that canonical inventory.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOK_ROOT = REPO_ROOT / "Geometric-Algebra-for-Computer-Science"


@dataclass(frozen=True)
class Entry:
    label: str
    title: str
    folder: str
    notebook: str
    pages: str
    focus: str


@dataclass(frozen=True)
class Part:
    folder: str
    title: str
    entries: tuple[Entry, ...]


PARTS: tuple[Part, ...] = (
    Part(
        "part-01-geometric-algebra",
        "Part I: Geometric Algebra",
        (
            Entry("Chapter 01", "Why Geometric Algebra?", "chapter-01-why-geometric-algebra", "01-why-geometric-algebra.ipynb", "pp. 1-22", "motivation, constructions, transformations, invariants"),
            Entry("Chapter 02", "Spanning Oriented Subspaces", "chapter-02-spanning-oriented-subspaces", "02-spanning-oriented-subspaces.ipynb", "pp. 23-64", "outer products, blades, Grassmann algebra, programming labs"),
            Entry("Chapter 03", "Metric Products of Subspaces", "chapter-03-metric-products-of-subspaces", "03-metric-products-of-subspaces.ipynb", "pp. 65-98", "metrics, contractions, duality, projections, reciprocal frames"),
            Entry("Chapter 04", "Linear Transformations of Subspaces", "chapter-04-linear-transformations-of-subspaces", "04-linear-transformations-of-subspaces.ipynb", "pp. 99-124", "outermorphisms, determinants, adjoints, transformed products"),
            Entry("Chapter 05", "Intersection and Union of Subspaces", "chapter-05-intersection-and-union-of-subspaces", "05-intersection-and-union-of-subspaces.ipynb", "pp. 125-140", "meet, join, signs, linearity, homogeneous offsets"),
            Entry("Chapter 06", "The Fundamental Product of Geometric Algebra", "chapter-06-the-fundamental-product-of-geometric-algebra", "06-the-fundamental-product-of-geometric-algebra.ipynb", "pp. 141-166", "geometric product, division, projection, reflection, Gram-Schmidt"),
            Entry("Chapter 07", "Orthogonal Transformations as Versors", "chapter-07-orthogonal-transformations-as-versors", "07-rotations-rotors-and-versors.ipynb", "pp. 167-212", "reflections, rotors, 4pi sense, composition, exponentials, versors"),
            Entry("Chapter 08", "Geometric Differentiation", "chapter-08-geometric-differentiation", "08-geometric-differentiation.ipynb", "pp. 213-244", "commutators, parametric/scalar/directional/vector derivatives"),
        ),
    ),
    Part(
        "part-02-models-of-geometry",
        "Part II: Models of Geometry",
        (
            Entry("Chapter 09", "Modeling Geometries", "chapter-09-modeling-geometries", "09-modeling-geometries.ipynb", "pp. 245-246", "model-selection bridge and geometry workflows"),
            Entry("Chapter 10", "The Vector Space Model: The Algebra of Directions", "chapter-10-the-vector-space-model-the-algebra-of-directions", "10-vector-space-model-algebra-of-directions.ipynb", "pp. 247-270", "directions, angular relationships, interpolation, point groups"),
            Entry("Chapter 11", "The Homogeneous Model", "chapter-11-the-homogeneous-model", "11-the-homogeneous-model.ipynb", "pp. 271-326", "points, flats, incidence, cross ratios, conics, perspective"),
            Entry("Chapter 12", "Applications of the Homogeneous Model", "chapter-12-applications-of-the-homogeneous-model", "12-applications-of-the-homogeneous-model.ipynb", "pp. 327-354", "Plucker lines, camera geometry, epipolar constraints, reconstruction"),
            Entry("Chapter 13", "The Conformal Model: Operational Euclidean Geometry", "chapter-13-the-conformal-model-operational-euclidean-geometry", "13-conformal-model-operational-euclidean-geometry.ipynb", "pp. 355-396", "null embedding, probes, flats, motors, screw interpolation"),
            Entry("Chapter 14", "New Primitives for Euclidean Geometry", "chapter-14-new-primitives-for-euclidean-geometry", "14-new-primitives-for-euclidean-geometry.ipynb", "pp. 397-436", "rounds, tangents, paraboloids, Voronoi, fitting, kinematics"),
            Entry("Chapter 15", "Constructions in Euclidean Geometry", "chapter-15-constructions-in-euclidean-geometry", "15-constructions-in-euclidean-geometry.ipynb", "pp. 437-464", "incidence, meet/plunge, tangents, factorization, affine combinations"),
            Entry("Chapter 16", "Conformal Operators", "chapter-16-conformal-operators", "16-conformal-operators.ipynb", "pp. 465-496", "inversion, spherical reflection, translations, loxodromes, non-Euclidean models"),
            Entry("Chapter 17", "Operational Models for Geometries", "chapter-17-operational-models-for-geometries", "17-operational-models-for-geometries.ipynb", "pp. 497-502", "model synthesis and implementation decision workflow"),
        ),
    ),
    Part(
        "part-03-implementation",
        "Part III: Implementation",
        (
            Entry("Chapter 18", "Implementation Issues", "chapter-18-implementation-issues", "18-implementation-issues.ipynb", "pp. 503-510", "implementation levels, matrices, dense/sparse and symbolic/numeric tradeoffs"),
            Entry("Chapter 19", "Basis Blades and Operations", "chapter-19-basis-blades-and-operations", "19-basis-blades-and-operations.ipynb", "pp. 511-520", "bitmap blades, signs, basis products, nonorthogonal metrics"),
            Entry("Chapter 20", "The Linear Products and Operations", "chapter-20-the-linear-products-and-operations", "20-the-linear-products-and-operations.ipynb", "pp. 521-528", "linear products as matrices, sparse operations, contractions"),
            Entry("Chapter 21", "Fundamental Algorithms for Nonlinear Products", "chapter-21-fundamental-algorithms-for-nonlinear-products", "21-fundamental-algorithms-for-nonlinear-products.ipynb", "pp. 529-540", "inverses, factorization, delta product, robust meet/join"),
            Entry("Chapter 22", "Specializing the Structure for Efficiency", "chapter-22-specializing-the-structure-for-efficiency", "22-specializing-the-structure-for-efficiency.ipynb", "pp. 541-556", "specialization, code generation, optimized kernels, benchmarks"),
            Entry("Chapter 23", "Using the Geometry in a Ray-Tracing Application", "chapter-23-using-the-geometry-in-a-ray-tracing-application", "23-ray-tracing-with-conformal-geometry.ipynb", "pp. 557-584", "meshes, rays, BSP, intersections, shading, mini render"),
        ),
    ),
    Part(
        "part-04-appendices",
        "Part IV: Appendices",
        (
            Entry("Appendix A", "Metrics and Null Vectors", "appendix-a-metrics-and-null-vectors", "appendix-a-metrics-and-null-vectors.ipynb", "pp. 585-588", "metrics, signatures, null vectors, degeneracy checks"),
            Entry("Appendix B", "Contractions and Other Inner Products", "appendix-b-contractions-and-other-inner-products", "appendix-b-contractions-and-other-inner-products.ipynb", "pp. 589-596", "contraction conventions, grade behavior, projection tests"),
            Entry("Appendix C", "Subspace Products Retrieved", "appendix-c-subspace-products-retrieved", "appendix-c-subspace-products-retrieved.ipynb", "pp. 597-602", "grade selection identities and product retrieval"),
            Entry("Appendix D", "Common Equations", "appendix-d-common-equations", "appendix-d-common-equations.ipynb", "pp. 603-608", "executable formula sheet and sign checks"),
        ),
    ),
)


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook(cells=[new_markdown_cell(text.strip() + "\n")])
    nbformat.write(nb, path)


def ensure_inventory() -> None:
    missing: list[Path] = []
    for part in PARTS:
        for entry in part.entries:
            notebook = BOOK_ROOT / part.folder / entry.folder / entry.notebook
            index = notebook.parent / "00-index.ipynb"
            if not notebook.exists():
                missing.append(notebook)
            if not index.exists():
                missing.append(index)
    if missing:
        details = "\n".join(str(path) for path in missing)
        raise FileNotFoundError(f"Missing course notebooks or indexes:\n{details}")


def build_book_index() -> str:
    lines = [
        "# Geometric Algebra for Computer Science - Standalone Notebook Edition",
        "",
        "This is an original, executable notebook course organized around the textbook's 23 chapters and four appendices. It is written as a study replacement in the practical sense: the notebooks explain the concepts in fresh prose, derive the working formulas, generate their own diagrams and artifacts, and finish with executable checks. The textbook PDF is not redistributed in the repository.",
        "",
        "## How To Use This Course",
        "",
        "- Start with the canonical notebook in each chapter folder; each chapter also has a local `00-index.ipynb` with page-span notes and artifact pointers.",
        "- Run notebooks top to bottom. Generated figures and checks are written under this book's `artifacts/chapter-XX` and `artifacts/appendices` folders.",
        "- Shared inspectable code lives under this book's `utils` package, including `utils.ga` and chapter-specific helper modules.",
        "- The notebooks use original explanations and paraphrased problem framing; they avoid copied textbook prose, page scans, and long verbatim passages.",
        "",
    ]
    for part in PARTS:
        lines.extend([f"## {part.title}", ""])
        part_index = f"{part.folder}/00-part-index.ipynb"
        lines.append(f"- [Open {part.title} Index]({part_index})")
        for entry in part.entries:
            chapter_index = f"{part.folder}/{entry.folder}/00-index.ipynb"
            canonical = f"{part.folder}/{entry.folder}/{entry.notebook}"
            lines.append(
                f"- [{entry.label}: {entry.title}]({chapter_index}) - "
                f"[canonical notebook]({canonical}); {entry.pages}; {entry.focus}"
            )
        lines.append("")
    return "\n".join(lines)


def build_part_index(part: Part) -> str:
    lines = [
        f"# {part.title}",
        "",
        "[Back to Book Index](../00-book-index.ipynb)",
        "",
        "Each entry links to the chapter or appendix index and directly to the canonical authored notebook.",
        "",
    ]
    for entry in part.entries:
        chapter_index = f"{entry.folder}/00-index.ipynb"
        canonical = f"{entry.folder}/{entry.notebook}"
        lines.append(f"## {entry.label}: {entry.title}")
        lines.append("")
        lines.append(f"- Index: [{entry.folder}]({chapter_index})")
        lines.append(f"- Canonical notebook: [{entry.notebook}]({canonical})")
        lines.append(f"- Source span: {entry.pages}")
        lines.append(f"- Focus: {entry.focus}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    ensure_inventory()
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for part in PARTS:
        write_markdown_notebook(BOOK_ROOT / part.folder / "00-part-index.ipynb", build_part_index(part))
    print(f"Updated book index and {len(PARTS)} part indexes for {sum(len(p.entries) for p in PARTS)} notebooks.")


if __name__ == "__main__":
    main()
