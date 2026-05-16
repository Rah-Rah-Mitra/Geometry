"""Source inventory for Clara Loeh's Geometric Group Theory course."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BOOK_ROOT = Path(__file__).resolve().parents[1]
PDF_SOURCE = "Geometric Group Theory An Introduction.pdf"

SOURCE_SPAN_NOTES = [
    "The local PDF is used only for source orientation, terminology, and coverage.",
    "The PDF has 390 physical pages.",
    "Body and back-matter printed pages map to physical PDF pages by pdf_page = printed_page + 11.",
    "Front matter occupies physical PDF pages 1-11.",
    "No textbook prose, figures, screenshots, page crops, or long exercise text are copied into the course.",
]

PARTS = [
    {
        "label": "Part 00",
        "title": "Orientation",
        "folder": "part-00-orientation",
        "printed_span": "1-6",
        "pdf_span": "12-17",
        "focus": "course motivation and the group-to-geometry pipeline",
    },
    {
        "label": "Part I",
        "title": "Groups",
        "folder": "part-01-groups",
        "printed_span": "7-50",
        "pdf_span": "18-61",
        "focus": "algebraic raw material for geometric group theory",
    },
    {
        "label": "Part II",
        "title": "Groups to Geometry",
        "folder": "part-02-groups-to-geometry",
        "printed_span": "51-164",
        "pdf_span": "62-175",
        "focus": "Cayley graphs, actions, word metrics, and quasi-isometry",
    },
    {
        "label": "Part III",
        "title": "Geometry of Groups",
        "folder": "part-03-geometry-of-groups",
        "printed_span": "165-316",
        "pdf_span": "176-327",
        "focus": "growth, hyperbolicity, ends, boundaries, and amenability",
    },
    {
        "label": "Part IV",
        "title": "Reference Material",
        "folder": "part-04-reference-material",
        "printed_span": "317-352",
        "pdf_span": "328-363",
        "focus": "topological and hyperbolic background plus programming tasks",
    },
]

ENTRIES: list[dict[str, Any]] = [
    {
        "label": "Chapter 01",
        "title": "Introduction",
        "folder": "part-00-orientation/chapter-01-introduction",
        "notebook": "01-introduction.ipynb",
        "artifact": "chapter-01",
        "printed_span": "1-6",
        "pdf_span": "12-17",
        "sections": "Chapter 1",
        "focus": "the geometric group theory workflow, Cayley graph intuition, and large-scale invariants",
        "topics": [
            "groups as sources of geometric spaces",
            "Cayley graphs for Z, Z^2, and a free group",
            "large-scale geometry as the comparison language",
            "applications that translate algebra into geometry and back",
        ],
    },
    {
        "label": "Chapter 02",
        "title": "Generating Groups",
        "folder": "part-01-groups/chapter-02-generating-groups",
        "notebook": "02-generating-groups.ipynb",
        "artifact": "chapter-02",
        "printed_span": "9-50",
        "pdf_span": "20-61",
        "sections": "2.1-2.3 and 2.E",
        "focus": "abstract groups, automorphism groups, quotients, generators, relations, free groups, products, and extensions",
        "topics": [
            "subgroups, quotients, kernels, and normality",
            "free groups and reduced words",
            "presentations and finite presentation",
            "products, semidirect products, free products, and amalgamated products",
        ],
    },
    {
        "label": "Chapter 03",
        "title": "Cayley Graphs",
        "folder": "part-02-groups-to-geometry/chapter-03-cayley-graphs",
        "notebook": "03-cayley-graphs.ipynb",
        "artifact": "chapter-03",
        "printed_span": "53-74",
        "pdf_span": "64-85",
        "sections": "3.1-3.3 and 3.E",
        "focus": "graph notation, Cayley graph construction, word length, and free groups as trees",
        "topics": [
            "vertices as group elements and edges as generator steps",
            "word metrics from graph distance",
            "free group reduced words",
            "trees as a geometry detecting freeness",
        ],
    },
    {
        "label": "Chapter 04",
        "title": "Group Actions",
        "folder": "part-02-groups-to-geometry/chapter-04-group-actions",
        "notebook": "04-group-actions.ipynb",
        "artifact": "chapter-04",
        "printed_span": "75-114",
        "pdf_span": "86-125",
        "sections": "4.1-4.4 and 4.E",
        "focus": "group actions, orbits, stabilisers, tree actions, ping-pong, and matrix-group applications",
        "topics": [
            "free, transitive, and orbit-stabiliser behavior",
            "actions on trees and subgroup structure",
            "ping-pong domains as a visual freeness criterion",
            "matrix group examples and large-girth graph intuition",
        ],
    },
    {
        "label": "Chapter 05",
        "title": "Quasi-Isometry",
        "folder": "part-02-groups-to-geometry/chapter-05-quasi-isometry",
        "notebook": "05-quasi-isometry.ipynb",
        "artifact": "chapter-05",
        "printed_span": "115-164",
        "pdf_span": "126-175",
        "sections": "5.1-5.6 and 5.E",
        "focus": "coarse equivalence of metric spaces and groups, quasi-geodesics, Svarc-Milnor, and invariants",
        "topics": [
            "quasi-isometric embeddings and coarse inverses",
            "word metrics from different generating sets",
            "quasi-geodesics and graph realisations",
            "Svarc-Milnor and quasi-isometry invariants",
        ],
    },
    {
        "label": "Chapter 06",
        "title": "Growth Types of Groups",
        "folder": "part-03-geometry-of-groups/chapter-06-growth-types-of-groups",
        "notebook": "06-growth-types-of-groups.ipynb",
        "artifact": "chapter-06",
        "printed_span": "167-202",
        "pdf_span": "178-213",
        "sections": "6.1-6.4 and 6.E",
        "focus": "growth functions, growth types, polynomial growth, nilpotence, and uniform exponential growth",
        "topics": [
            "ball cardinalities in word metrics",
            "coarse comparison of growth functions",
            "polynomial growth and virtual nilpotence",
            "exponential and uniform exponential growth",
        ],
    },
    {
        "label": "Chapter 07",
        "title": "Hyperbolic Groups",
        "folder": "part-03-geometry-of-groups/chapter-07-hyperbolic-groups",
        "notebook": "07-hyperbolic-groups.ipynb",
        "artifact": "chapter-07",
        "printed_span": "203-256",
        "pdf_span": "214-267",
        "sections": "7.1-7.6 and 7.E",
        "focus": "Gromov hyperbolicity, quasi-geodesics, hyperbolic graphs, word problem ideas, and negative-curvature consequences",
        "topics": [
            "thin triangles and four-point hyperbolicity",
            "quasi-geodesics in hyperbolic spaces",
            "hyperbolic groups through Cayley graphs",
            "word problem heuristics, centralisers, quasi-convexity, and products",
        ],
    },
    {
        "label": "Chapter 08",
        "title": "Ends and Boundaries",
        "folder": "part-03-geometry-of-groups/chapter-08-ends-and-boundaries",
        "notebook": "08-ends-and-boundaries.ipynb",
        "artifact": "chapter-08",
        "printed_span": "257-288",
        "pdf_span": "268-299",
        "sections": "8.1-8.4 and 8.E",
        "focus": "ends, Gromov boundaries, free subgroups in hyperbolic groups, and rigidity at infinity",
        "topics": [
            "components that remain after removing large balls",
            "ends of quasi-geodesic spaces and groups",
            "boundary classes of rays in hyperbolic spaces",
            "boundary maps as rigidity data",
        ],
    },
    {
        "label": "Chapter 09",
        "title": "Amenable Groups",
        "folder": "part-03-geometry-of-groups/chapter-09-amenable-groups",
        "notebook": "09-amenable-groups.ipynb",
        "artifact": "chapter-09",
        "printed_span": "289-316",
        "pdf_span": "300-327",
        "sections": "9.1-9.4 and 9.E",
        "focus": "amenability via means, Folner sets, paradoxical decompositions, and quasi-isometry invariance",
        "topics": [
            "invariant averaging intuition",
            "Folner boundary-to-volume tests",
            "paradoxical decomposition as non-amenability signal",
            "quasi-isometry invariance and bilipschitz comparison",
        ],
    },
    {
        "label": "Appendix A",
        "title": "Reference Material",
        "folder": "part-04-reference-material/appendix-a-reference-material",
        "notebook": "appendix-a-reference-material.ipynb",
        "artifact": "appendix-a",
        "printed_span": "319-352",
        "pdf_span": "330-363",
        "sections": "A.1-A.4",
        "focus": "fundamental groups, covering theory, group cohomology, hyperbolic plane models, and programming tasks",
        "topics": [
            "fundamental groups and covering spaces",
            "group cohomology as algebraic bookkeeping",
            "hyperbolic plane models, geodesics, and distance checks",
            "programming tasks as computational laboratories",
        ],
    },
]

BACK_MATTER = [
    {"title": "Bibliography", "printed_span": "353-366", "pdf_span": "364-377"},
    {"title": "Index of notation", "printed_span": "367-372", "pdf_span": "378-383"},
    {"title": "Index", "printed_span": "373-379", "pdf_span": "384-390"},
]


def source_map() -> dict[str, Any]:
    """Return the book-local source map as serialisable data."""

    return {
        "book": "Geometric Group Theory: An Introduction",
        "author": "Clara Loeh",
        "source_pdf": PDF_SOURCE,
        "physical_pdf_pages": 390,
        "body_pdf_page_formula": "pdf_page = printed_page + 11",
        "notes": SOURCE_SPAN_NOTES,
        "parts": PARTS,
        "entries": ENTRIES,
        "back_matter": BACK_MATTER,
    }


def write_source_map(path: Path | None = None) -> Path:
    """Write the source map under the book-local artifacts tree."""

    target = path or BOOK_ROOT / "artifacts" / "source-map" / "checks" / "source-map.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(source_map(), indent=2, sort_keys=True), encoding="utf-8")
    return target


if __name__ == "__main__":
    written = write_source_map()
    print(written.relative_to(BOOK_ROOT).as_posix())
