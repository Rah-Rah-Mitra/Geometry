"""Rebuild Geometry II book and chapter index notebooks."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook


BOOK_ROOT = Path(__file__).resolve().parents[1]

CHAPTERS = [
    (12, "Polytopes; Compact Convex Sets", "chapter-12-polytopes-compact-convex-sets", "12-polytopes-compact-convex-sets.ipynb", "1-85", "10-94", "convex hulls, regular polytopes, Euler characteristic, Cauchy rigidity, approximation, isoperimetry"),
    (13, "Quadratic Forms", "chapter-13-quadratic-forms", "13-quadratic-forms.ipynb", "86-115", "95-124", "signatures, isotropic cones, radicals, orthogonalization, Witt decomposition, reflections"),
    (14, "Projective Quadrics", "chapter-14-projective-quadrics", "14-projective-quadrics.ipynb", "116-145", "125-154", "homogeneous quadrics, pencils, topology, polarity, tangent geometry, projective actions"),
    (15, "Affine Quadrics", "chapter-15-affine-quadrics", "15-affine-quadrics.ipynb", "146-169", "155-178", "affine classification, real and complex quadrics, topology, polarity, Euclidean models"),
    (16, "Projective Conics", "chapter-16-projective-conics", "16-projective-conics.ipynb", "170-217", "179-226", "parametrized conics, cross-ratios, Pascal, homographies, Bezout, pencils"),
    (17, "Euclidean Conics", "chapter-17-euclidean-conics", "17-euclidean-conics.ipynb", "218-254", "227-263", "metric conics, focal/directrix views, cyclic points, tangential pencils, ellipses and hyperbolas"),
    (18, "The Sphere for Its Own Sake", "chapter-18-the-sphere-for-its-own-sake", "18-the-sphere-for-its-own-sake.ipynb", "255-317", "264-326", "charts, projections, measure, intrinsic metric, spherical triangles, Clifford parallelism, Mobius group"),
    (19, "Elliptic and Hyperbolic Geometry", "chapter-19-elliptic-and-hyperbolic-geometry", "19-elliptic-and-hyperbolic-geometry.ipynb", "318-348", "327-357", "elliptic geometry, projective and ball models, Poincare disk, distances, isometries"),
    (20, "The Space of Spheres", "chapter-20-the-space-of-spheres", "20-the-space-of-spheres.ipynb", "349-362", "358-371", "generalized spheres, sphere quadratic form, orthogonality, intersections, pencils, circular group"),
]


def write_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook(cells=[new_markdown_cell(text.strip() + "\n")])
    nbformat.write(nb, path)


def main() -> None:
    lines = [
        "# Geometry II - Visualization-First Notebook Course",
        "",
        "This original standalone course follows Volume II of Marcel Berger's *Geometry II* and covers Chapters 12-20. The notebooks are designed to teach without requiring the PDF open.",
        "",
        "Generated artifacts live under `artifacts/chapter-XX`. The source map uses `pdf_page = printed_volume_ii_page + 9`.",
        "",
    ]
    for number, title, folder, notebook, printed_pages, pdf_pages, focus in CHAPTERS:
        lines.append(
            f"- [Chapter {number}: {title}]({folder}/00-index.ipynb) - "
            f"[canonical notebook]({folder}/{notebook}); printed pages {printed_pages}; "
            f"PDF pages {pdf_pages}; {focus}."
        )
        chapter_index = f"""# Chapter {number}: {title}

[Back to Book Index](../00-book-index.ipynb)

- Canonical notebook: [{notebook}]({notebook})
- Source span: printed Volume II pages {printed_pages}; PDF pages {pdf_pages}
- Visual center: {focus}
- Artifact topic: `artifacts/chapter-{number:02d}`
"""
        write_notebook(BOOK_ROOT / folder / "00-index.ipynb", chapter_index)
    write_notebook(BOOK_ROOT / "00-book-index.ipynb", "\n".join(lines))
    print(f"Updated Geometry II book index and {len(CHAPTERS)} chapter indexes.")


if __name__ == "__main__":
    main()
