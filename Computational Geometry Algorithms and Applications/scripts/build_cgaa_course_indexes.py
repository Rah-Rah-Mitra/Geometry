"""Rebuild CGAA book and chapter index notebooks."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

BOOK_ROOT = Path(__file__).resolve().parents[1]

CHAPTERS = [
    (1, "Computational Geometry", "chapter-01-computational-geometry", "01-computational-geometry.ipynb", "1-18", "convex hulls, orientation predicates, degeneracy, robustness, application map"),
    (2, "Line Segment Intersection", "chapter-02-line-segment-intersection", "02-line-segment-intersection.ipynb", "19-44", "sweep line events, output sensitivity, event queue, status order, DCEL overlay"),
    (3, "Polygon Triangulation", "chapter-03-polygon-triangulation", "03-polygon-triangulation.ipynb", "45-62", "art-gallery theorem, monotone decomposition, stack triangulation"),
    (4, "Linear Programming", "chapter-04-linear-programming", "04-linear-programming.ipynb", "63-94", "half-plane intersection, randomized incremental LP, unbounded cases, smallest disks"),
    (5, "Orthogonal Range Searching", "chapter-05-orthogonal-range-searching", "05-orthogonal-range-searching.ipynb", "95-120", "1D range searching, kd-trees, range trees, higher dimensions, fractional cascading"),
    (6, "Point Location", "chapter-06-point-location", "06-point-location.ipynb", "121-146", "trapezoidal maps, randomized incremental construction, search DAG, degeneracies"),
    (7, "Voronoi Diagrams", "chapter-07-voronoi-diagrams", "07-voronoi-diagrams.ipynb", "147-172", "Voronoi cells, Fortune sweep intuition, line-segment sites, farthest-point diagrams"),
    (8, "Arrangements and Duality", "chapter-08-arrangements-and-duality", "08-arrangements-and-duality.ipynb", "173-190", "line arrangements, point-line duality, levels, discrepancy"),
    (9, "Delaunay Triangulations", "chapter-09-delaunay-triangulations", "09-delaunay-triangulations.ipynb", "191-218", "planar triangulations, Delaunay empty circle property, lifting, randomized construction"),
    (10, "More Geometric Data Structures", "chapter-10-more-geometric-data-structures", "10-more-geometric-data-structures.ipynb", "219-242", "interval trees, priority search trees, segment trees, stabbing/window queries"),
    (11, "Convex Hulls", "chapter-11-convex-hulls", "11-convex-hulls.ipynb", "243-258", "3D convex hull complexity, randomized incremental hulls, half-space and Voronoi links"),
    (12, "Binary Space Partitions", "chapter-12-binary-space-partitions", "12-binary-space-partitions.ipynb", "259-282", "BSP trees, painter ordering, segment splitting, low-density scenes"),
    (13, "Robot Motion Planning", "chapter-13-robot-motion-planning", "13-robot-motion-planning.ipynb", "283-306", "work space, configuration space, Minkowski sums, translational and rotational planning"),
    (14, "Quadtrees", "chapter-14-quadtrees", "14-quadtrees.ipynb", "307-322", "uniform and non-uniform meshes, quadtrees for points, balanced refinement"),
    (15, "Visibility Graphs", "chapter-15-visibility-graphs", "15-visibility-graphs.ipynb", "323-334", "shortest paths, visibility graph construction, translating polygonal robots"),
    (16, "Simplex Range Searching", "chapter-16-simplex-range-searching", "16-simplex-range-searching.ipynb", "335-356", "partition trees, multi-level partition trees, cutting trees, simplex queries"),
]


def write_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook(cells=[new_markdown_cell(text.strip() + "\n")])
    nbformat.write(nb, path)


def main() -> None:
    lines = [
        "# Computational Geometry Algorithms and Applications - Standalone Notebook Course",
        "",
        "This original visualization-first course follows the 16-chapter structure of the third edition. Generated artifacts live under `artifacts/chapter-XX`.",
        "",
        "Body printed pages map to PDF pages by `pdf_page = printed_page + 11`.",
        "",
    ]
    for number, title, folder, notebook, pages, focus in CHAPTERS:
        lines.append(f"- [Chapter {number:02d}: {title}]({folder}/00-index.ipynb) - [canonical notebook]({folder}/{notebook}); printed pages {pages}; {focus}.")
        chapter_index = f"""# Chapter {number:02d}: {title}

[Back to Book Index](../00-book-index.ipynb)

- Canonical notebook: [{notebook}]({notebook})
- Source span: printed pages {pages}; PDF pages {int(pages.split('-')[0]) + 11}-{int(pages.split('-')[1]) + 11}
- Visual center: {focus}
- Artifact topic: `artifacts/chapter-{number:02d}`
"""
        write_notebook(BOOK_ROOT / folder / "00-index.ipynb", chapter_index)
    write_notebook(BOOK_ROOT / "00-book-index.ipynb", "\n".join(lines))
    print(f"Updated CGAA book index and {len(CHAPTERS)} chapter indexes.")


if __name__ == "__main__":
    main()
