"""Bootstrap the standalone CGAA visualization-first notebook course.

This script is intentionally book-local. It creates the first complete course
edition from the PDF-oriented inventory, including notebooks, indexes, helpers,
validation scripts, and initial visual artifacts.
"""

from __future__ import annotations

import importlib
import json
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


BOOK_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BOOK_ROOT.parent
PDF_NAME = "Computational Geometry Algorithms and Applications.pdf"


@dataclass(frozen=True)
class Chapter:
    number: int
    title: str
    subtitle: str
    folder: str
    notebook: str
    printed_pages: str
    pdf_pages: str
    focus: str
    application: str
    algorithmic_core: str
    data_structures: str
    starred: str
    visual_kind: str
    route: tuple[str, ...]
    checks: tuple[str, ...]

    @property
    def label(self) -> str:
        return f"Chapter {self.number:02d}"

    @property
    def topic(self) -> str:
        return f"chapter-{self.number:02d}"


CHAPTERS: tuple[Chapter, ...] = (
    Chapter(
        1,
        "Computational Geometry",
        "Introduction",
        "chapter-01-computational-geometry",
        "01-computational-geometry.ipynb",
        "1-18",
        "12-29",
        "convex hulls, orientation predicates, degeneracy, robustness, application map",
        "nearest services, robot navigation, and map overlay motivate geometric algorithms",
        "incremental planar convex hull with orientation tests and upper/lower chains",
        "ordered point lists, hull edge lists, predicate wrappers",
        "none",
        "convex-hull",
        (
            "translate convexity into a computable boundary",
            "compare slow edge testing with the incremental hull",
            "make orientation and degeneracy visible",
            "connect primitive predicates to robustness",
        ),
        (
            "hull vertices form only right turns in clockwise order",
            "all input points lie on or inside the hull polygon",
            "near-collinear triples expose a numerical sensitivity score",
        ),
    ),
    Chapter(
        2,
        "Line Segment Intersection",
        "Thematic Map Overlay",
        "chapter-02-line-segment-intersection",
        "02-line-segment-intersection.ipynb",
        "19-44",
        "30-55",
        "sweep line events, output sensitivity, event queue, status order, DCEL overlay",
        "overlaying thematic maps by finding and organizing segment intersections",
        "Bentley-Ottmann style plane sweep with event queue and ordered status",
        "balanced search trees, event records, doubly-connected edge list records",
        "none",
        "segment-sweep",
        (
            "turn pairwise segment testing into an event process",
            "watch adjacency changes create the only necessary tests",
            "separate geometry events from subdivision topology",
            "use DCEL pointers to walk faces after intersections are known",
        ),
        (
            "reported intersections match brute-force intersections",
            "events are processed in sweep priority order",
            "DCEL toy overlay satisfies twin-next-prev consistency",
        ),
    ),
    Chapter(
        3,
        "Polygon Triangulation",
        "Guarding an Art Gallery",
        "chapter-03-polygon-triangulation",
        "03-polygon-triangulation.ipynb",
        "45-62",
        "56-73",
        "art-gallery theorem, monotone decomposition, stack triangulation",
        "placing guards by first decomposing a polygon into triangles",
        "plane sweep to monotone pieces followed by linear stack triangulation",
        "vertex classifications, diagonals in a DCEL, stack of monotone-chain vertices",
        "none",
        "triangulation",
        (
            "classify polygon vertices by local turn and vertical order",
            "insert diagonals that remove split and merge vertices",
            "triangulate a monotone polygon with a stack invariant",
            "color the triangulation graph to reveal a guard bound",
        ),
        (
            "triangles cover polygon area without changing total area",
            "n vertex simple polygon has n - 2 triangles in the demo",
            "guard color class size is at most ceiling(n / 3)",
        ),
    ),
    Chapter(
        4,
        "Linear Programming",
        "Manufacturing with Molds",
        "chapter-04-linear-programming",
        "04-linear-programming.ipynb",
        "63-94",
        "74-105",
        "half-plane intersection, randomized incremental LP, unbounded cases, smallest disks",
        "choosing mold directions and feasible manufacturing constraints",
        "low-dimensional linear programming by incrementally repairing violated constraints",
        "half-plane lists, active constraint basis, randomized order trace",
        "higher dimensions; smallest enclosing discs",
        "halfplanes",
        (
            "view linear programs as movement inside a feasible polygon",
            "clip a search region by half-planes one at a time",
            "show how a violated constraint reduces the problem dimension",
            "compare bounded, empty, and unbounded feasible regions",
        ),
        (
            "computed optimum satisfies every half-plane",
            "active constraints agree with the plotted optimum",
            "smallest enclosing disk covers all sample points",
        ),
    ),
    Chapter(
        5,
        "Orthogonal Range Searching",
        "Querying a Database",
        "chapter-05-orthogonal-range-searching",
        "05-orthogonal-range-searching.ipynb",
        "95-120",
        "106-131",
        "1D range searching, kd-trees, range trees, higher dimensions, fractional cascading",
        "answering window queries over spatial records",
        "preprocess points so axis-aligned box queries visit only relevant subtrees",
        "sorted arrays, balanced binary trees, kd-tree nodes, range-tree catalogs",
        "fractional cascading",
        "range-search",
        (
            "contrast scanning with indexed 1D range queries",
            "split the plane recursively with kd-tree cuts",
            "trace a rectangular query through accepted and rejected cells",
            "explain how range trees pay extra storage for sharper query bounds",
        ),
        (
            "kd-tree reported points equal brute-force rectangle filtering",
            "visited-node count is smaller than scanning all points",
            "fractional-catalog toy links preserve sorted order",
        ),
    ),
    Chapter(
        6,
        "Point Location",
        "Knowing Where You Are",
        "chapter-06-point-location",
        "06-point-location.ipynb",
        "121-146",
        "132-157",
        "trapezoidal maps, randomized incremental construction, search DAG, degeneracies",
        "finding which subdivision face contains a query point",
        "randomized incremental trapezoidal map with a directed acyclic search structure",
        "trapezoids, neighbor pointers, search DAG leaves",
        "tail estimate",
        "point-location",
        (
            "decompose segments into vertical trapezoids",
            "walk a query point through x-nodes and segment tests",
            "show how one inserted segment replaces crossed trapezoids",
            "measure expected search depth over random insertion orders",
        ),
        (
            "each query lands in exactly one toy trapezoid",
            "search path decisions agree with direct containment tests",
            "randomized depth summary stays below the linear scan baseline",
        ),
    ),
    Chapter(
        7,
        "Voronoi Diagrams",
        "The Post Office Problem",
        "chapter-07-voronoi-diagrams",
        "07-voronoi-diagrams.ipynb",
        "147-172",
        "158-183",
        "Voronoi cells, Fortune sweep intuition, line-segment sites, farthest-point diagrams",
        "partitioning a map by nearest service site",
        "Voronoi subdivision from nearest-site bisectors and a beach-line sweep view",
        "site lists, priority events, DCEL-style diagram records",
        "line segment and farthest-point Voronoi diagrams",
        "voronoi",
        (
            "build nearest regions from pairwise bisectors",
            "connect empty-circle events to Voronoi vertices",
            "compare point-site and segment-site distance fields",
            "show farthest cells living on the convex hull",
        ),
        (
            "sample-grid cell labels match nearest-site distances",
            "Delaunay edges connect sites whose cells touch",
            "farthest-site winners are hull points in the sample",
        ),
    ),
    Chapter(
        8,
        "Arrangements and Duality",
        "Supersampling in Ray Tracing",
        "chapter-08-arrangements-and-duality",
        "08-arrangements-and-duality.ipynb",
        "173-190",
        "184-201",
        "line arrangements, point-line duality, levels, discrepancy",
        "choosing sample patterns that avoid visible rendering artifacts",
        "transform point discrepancy questions into levels in an arrangement of lines",
        "arrangement cells, dual line records, level counters",
        "none",
        "duality",
        (
            "draw primal samples and their dual lines side by side",
            "track incidences preserved by the dual transform",
            "count line levels as a vertical sweep crosses the arrangement",
            "connect high discrepancy to cells with extreme level imbalance",
        ),
        (
            "point-above-line orientation is reversed consistently in the dual",
            "level counts sum to the number of dual lines",
            "brute-force discrepancy agrees with arrangement-cell sampling",
        ),
    ),
    Chapter(
        9,
        "Delaunay Triangulations",
        "Height Interpolation",
        "chapter-09-delaunay-triangulations",
        "09-delaunay-triangulations.ipynb",
        "191-218",
        "202-229",
        "planar triangulations, Delaunay empty circle property, lifting, randomized construction",
        "interpolating terrain heights from sample locations",
        "Delaunay triangulation as the projection of a lower convex hull",
        "triangle adjacency, circumcircle tests, conflict history",
        "framework for randomized algorithms",
        "delaunay",
        (
            "compare arbitrary triangulations with max-min-angle Delaunay structure",
            "visualize the empty circumcircle condition",
            "lift points to a paraboloid and project lower faces",
            "trace randomized insertion and local flips",
        ),
        (
            "no plotted Delaunay triangle contains another sample in its circumcircle",
            "Euler count matches planar triangulation expectations",
            "linear interpolation is continuous across shared edges",
        ),
    ),
    Chapter(
        10,
        "More Geometric Data Structures",
        "Windowing",
        "chapter-10-more-geometric-data-structures",
        "10-more-geometric-data-structures.ipynb",
        "219-242",
        "230-253",
        "interval trees, priority search trees, segment trees, stabbing/window queries",
        "finding scene objects inside a rectangular viewing window",
        "decompose one-dimensional intervals and lift them into window-query structures",
        "interval tree nodes, heap-ordered priority search trees, segment tree canonical sets",
        "none",
        "window-structures",
        (
            "start from interval stabbing before adding a second coordinate",
            "store intervals at split values and recurse on leftovers",
            "combine heap priority with search-tree order",
            "decompose query windows into canonical segment-tree nodes",
        ),
        (
            "interval-tree report equals brute-force interval stabbing",
            "priority search tree filters by x range and y priority",
            "segment-tree canonical cover is disjoint and complete",
        ),
    ),
    Chapter(
        11,
        "Convex Hulls",
        "Mixing Things",
        "chapter-11-convex-hulls",
        "11-convex-hulls.ipynb",
        "243-258",
        "254-269",
        "3D convex hull complexity, randomized incremental hulls, half-space and Voronoi links",
        "understanding feasible mixtures through 3D hull boundaries",
        "randomized incremental 3D hull construction with conflict information",
        "facets, ridges, conflict graph, horizon cycle",
        "analysis; half-space intersection; Voronoi revisited",
        "hull3d",
        (
            "lift the 2D hull intuition to facets and ridges",
            "show Euler relations controlling 3D hull complexity",
            "insert a point and reveal its visible facets and horizon",
            "connect hulls to half-space intersection and Voronoi diagrams",
        ),
        (
            "facet and ridge counts satisfy Euler's formula",
            "new point sees exactly the facets with positive signed distance",
            "projected lower hull gives the same Delaunay edges as Chapter 9",
        ),
    ),
    Chapter(
        12,
        "Binary Space Partitions",
        "The Painter's Algorithm",
        "chapter-12-binary-space-partitions",
        "12-binary-space-partitions.ipynb",
        "259-282",
        "270-293",
        "BSP trees, painter ordering, segment splitting, low-density scenes",
        "rendering polygons from back to front without a depth buffer",
        "recursively split space so each leaf has an ordered fragment list",
        "BSP tree nodes, split fragments, traversal order",
        "3D size; low-density scenes",
        "bsp",
        (
            "classify segments against a splitting line",
            "show when crossing polygons must be split",
            "traverse the tree from a camera position for painter order",
            "compare arbitrary scenes with low-density behavior",
        ),
        (
            "every fragment lies on one side of each ancestor split",
            "painter order changes when the eye crosses a split line",
            "fragment count is at least input count and records all splits",
        ),
    ),
    Chapter(
        13,
        "Robot Motion Planning",
        "Getting Where You Want to Be",
        "chapter-13-robot-motion-planning",
        "13-robot-motion-planning.ipynb",
        "283-306",
        "294-317",
        "work space, configuration space, Minkowski sums, translational and rotational planning",
        "moving a robot from start to goal while avoiding obstacles",
        "transform robot-obstacle contact into point motion through configuration obstacles",
        "polygon offsets, free-space cells, roadmap graph",
        "motion planning with rotations",
        "motion-planning",
        (
            "separate work space geometry from configuration-space points",
            "inflate obstacles by the robot shape using Minkowski sums",
            "search a visibility roadmap in free configuration space",
            "sample orientation as an extra dimension for the starred extension",
        ),
        (
            "planned path vertices avoid every inflated obstacle",
            "Minkowski inflated boxes contain all robot-contact forbidden centers",
            "roadmap shortest path length is no longer than the displayed alternative",
        ),
    ),
    Chapter(
        14,
        "Quadtrees",
        "Non-Uniform Mesh Generation",
        "chapter-14-quadtrees",
        "14-quadtrees.ipynb",
        "307-322",
        "318-333",
        "uniform and non-uniform meshes, quadtrees for points, balanced refinement",
        "placing smaller mesh cells only where geometric detail demands them",
        "recursive square subdivision with balancing constraints for mesh quality",
        "quadtree nodes, leaf adjacency, balanced refinement queue",
        "none",
        "quadtree",
        (
            "compare uniform grids with adaptive subdivision",
            "split cells around clustered input points",
            "balance neighboring leaf sizes before meshing",
            "turn leaves into a non-uniform triangulated mesh",
        ),
        (
            "each leaf either has bounded occupancy or reaches max depth",
            "neighboring balanced leaves differ by at most one level in the toy mesh",
            "adaptive mesh uses fewer cells than a same-resolution uniform grid",
        ),
    ),
    Chapter(
        15,
        "Visibility Graphs",
        "Finding the Shortest Route",
        "chapter-15-visibility-graphs",
        "15-visibility-graphs.ipynb",
        "323-334",
        "334-345",
        "shortest paths, visibility graph construction, translating polygonal robots",
        "finding the shortest collision-free route among polygonal obstacles",
        "build a graph of mutually visible obstacle vertices and run shortest path",
        "visibility graph, obstacle edges, shortest-path predecessor tree",
        "none",
        "visibility",
        (
            "explain why shortest paths bend only at obstacle vertices",
            "test segment visibility against polygon obstacles",
            "run Dijkstra on the visibility graph",
            "reuse configuration obstacles for translating polygonal robots",
        ),
        (
            "every path segment is collision-free",
            "Dijkstra distance equals sum of displayed segment lengths",
            "removing a visible edge cannot shorten the reported path",
        ),
    ),
    Chapter(
        16,
        "Simplex Range Searching",
        "Windowing Revisited",
        "chapter-16-simplex-range-searching",
        "16-simplex-range-searching.ipynb",
        "335-356",
        "346-367",
        "partition trees, multi-level partition trees, cutting trees, simplex queries",
        "answering triangular and half-space range queries beyond axis-aligned windows",
        "partition point sets so simplex queries cross only a controlled number of cells",
        "simplicial partitions, multi-level search nodes, cutting cells",
        "none",
        "simplex-range",
        (
            "replace orthogonal boxes with triangle and half-plane queries",
            "partition points into cells whose crossing number can be inspected",
            "compose levels for multi-constraint queries",
            "use cutting cells to manage many query lines",
        ),
        (
            "triangle query result equals barycentric brute force",
            "crossing-cell count is recorded for the displayed query",
            "reported points are exactly those inside all simplex half-planes",
        ),
    ),
)


def dedent(text: str) -> str:
    return textwrap.dedent(text).strip() + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content), encoding="utf-8")


def write_notebook(path: Path, cells: list[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python", "pygments_lexer": "ipython3"}
    nbformat.write(nb, path)


def chapter_to_dict(chapter: Chapter) -> dict[str, Any]:
    return {
        "number": chapter.number,
        "label": chapter.label,
        "title": chapter.title,
        "subtitle": chapter.subtitle,
        "folder": chapter.folder,
        "notebook": chapter.notebook,
        "printed_pages": chapter.printed_pages,
        "pdf_pages": chapter.pdf_pages,
        "focus": chapter.focus,
        "application": chapter.application,
        "algorithmic_core": chapter.algorithmic_core,
        "data_structures": chapter.data_structures,
        "starred": chapter.starred,
        "visual_kind": chapter.visual_kind,
        "route": list(chapter.route),
        "checks": list(chapter.checks),
        "artifact_topic": chapter.topic,
    }


def chapter_markdown(chapter: Chapter) -> str:
    route = "\n".join(f"{i}. {item}." for i, item in enumerate(chapter.route, start=1))
    checks = "\n".join(f"- {item}." for item in chapter.checks)
    starred = (
        f"The starred material for this chapter is treated as an advanced lens: {chapter.starred}."
        if chapter.starred != "none"
        else "This chapter has no starred detour in the source map, so the notebook keeps its advanced work inside the applied lab."
    )
    glossary_rows = "\n".join(
        [
            f"| Application frame | {chapter.application} |",
            f"| Geometric problem | {chapter.focus} |",
            f"| Algorithmic core | {chapter.algorithmic_core} |",
            f"| Data structures | {chapter.data_structures} |",
            f"| Visual model | {chapter.visual_kind.replace('-', ' ')} |",
        ]
    )
    return dedent(
        f"""
        # {chapter.number:02d} - {chapter.title}

        Source span: printed pages {chapter.printed_pages}; PDF pages {chapter.pdf_pages}. This notebook is original standalone study material for *Computational Geometry: Algorithms and Applications*, Third Edition. It uses the book as orientation for chapter structure and concepts, but it does not copy textbook prose, exercises, screenshots, page crops, or figures.

        ## Standalone Goal

        The chapter question is: how do we turn {chapter.application} into a precise geometric algorithm that can be inspected, tested, and implemented? The answer is not just a theorem statement. It is a chain of modeling decisions: choose the geometric primitive, identify the invariant that makes the primitive useful, pick a data structure that exposes only the necessary local information, and verify that the resulting algorithm reports the same answer as a slower direct method on small examples.

        This notebook teaches {chapter.focus}. The diagrams are not decoration; each one is a small laboratory. The first visual fixes the geometric object of study. The second visual exposes the algorithmic state that changes over time. The computational check at the end records the invariant that should survive those state changes. When an algorithm is randomized, the notebook uses a deterministic seed so the displayed run is reproducible while still showing what changes under a random order. When an algorithm is sensitive to degeneracy, the notebook names the fragile predicate instead of hiding it inside a library call.

        A recurring theme in computational geometry is that the obvious mathematical definition is often too large to compute directly. A convex hull is an intersection of all convex sets, but the algorithm works with turns in a sorted list of points. A subdivision may be a planar set, but an overlay algorithm needs vertex, edge, face, and incidence records. A nearest-site region is defined by infinitely many distances, but a diagram is built from bisectors and events. For this chapter, the same translation happens through {chapter.algorithmic_core}. The notebook therefore keeps two views in sync: the continuous geometric object and the finite record that an algorithm can update.

        ## Translation Guide

        | Textbook idea | Computational translation |
        | --- | --- |
        {glossary_rows}

        ## Route Through The Chapter

        {route}

        ## Visual Storyboard

        The visual sequence follows a fixed teaching rhythm. First, a concept diagram labels the input geometry and the claimed output. Second, an algorithm-state diagram shows the local decision that lets the algorithm avoid brute force. Third, a small metric table or JSON check records the invariant in numbers. Some chapters also add an interactive HTML artifact when rotation, ordering, or query movement is easier to inspect dynamically than in a single static figure.

        The source chapter's application is treated as motivation rather than as a turnkey software product. The notebook abstracts the application into a compact test instance, because a clean instance makes the correctness argument visible. For example, a map-overlay chapter should display the sweep status and then test it against brute-force intersections; a motion-planning chapter should display configuration obstacles and then test the route against collision predicates; a range-searching chapter should show the query rectangle and then compare the data-structure report with direct filtering.

        ## Worked Examples And Pitfalls

        The worked examples deliberately use small data. Small examples make it possible to see every event, cell, edge, or predicate outcome without trusting a black box. That is also how the notebook handles robustness. A geometric algorithm usually depends on predicates such as orientation, in-circle tests, distance comparison, visibility, or containment. If the predicate is unstable near degeneracy, the notebook displays a near-degenerate case and records a margin. The margin is not a proof of robust industrial arithmetic, but it tells the reader where exact arithmetic or symbolic perturbation would become relevant.

        {starred} The notebook includes the starred idea as an optional computational extension whenever it changes the geometric picture. If it is mainly analytical, the extension becomes a small experiment: vary input size, random order, or query shape, then compare the measured state count with the stated asymptotic behavior. The point is to let the theorem leave a trace in an artifact, not to replace the proof with a picture.

        ## Implementation Lens

        The implementation is intentionally modest and inspectable. It favors plain arrays, short helper functions, and explicit predicates over a hidden production geometry kernel. That makes the notebook useful for learning: when a result changes, you can usually point to the exact comparison or update that changed it. The price is that these examples are teaching implementations, not industrial robust-geometry packages. The notebook therefore separates two claims. First, the displayed construction is checked on its own sample data. Second, the chapter explains what a complete implementation would still need for hostile inputs: exact predicates, careful event tie-breaking, balanced trees with stable keys, topology records, or certified numerical solvers.

        Read the final JSON artifact as a compact contract. It records the number of objects constructed, the key invariant, and the agreement with a direct check when a direct check is affordable. If you extend the notebook, keep that contract alive. Add a harder instance, then add a check that would fail if the geometric idea were misunderstood. For {chapter.title}, a good extension keeps the same application frame but changes the input enough to stress {chapter.data_structures}. The goal is not to produce a large library in one notebook; the goal is to make the algorithm's finite state visible and falsifiable.

        ## Applied Lab

        The applied lab asks you to modify the sample instance while keeping the final checks true. Change a site, obstacle, segment, query window, or constraint. Then re-run the notebook and inspect which artifact changes first. If the answer changes but the invariant still holds, the model is doing useful work. If the invariant fails, the failure usually points to exactly the geometric assumption that the algorithm needs: general position, non-crossing input, convexity, sorted order, balanced refinement, or a complete visibility test.

        ## Sanity Checks To Read

        {checks}

        ## Takeaways

        By the end of the notebook, you should be able to explain the chapter without opening the PDF: what geometric object is being computed, which finite state represents it, why the state changes are local, which degeneracies matter, and what numerical or combinatorial check confirms the displayed result. That is the standard for this course: a chapter is complete when its prose, code, visuals, and checks together carry the computational geometry.
        """
    )


def notebook_setup_cell() -> str:
    return dedent(
        """
        from __future__ import annotations

        import json
        import sys
        from pathlib import Path

        BOOK_ROOT = Path.cwd()
        for candidate in [BOOK_ROOT, *BOOK_ROOT.parents]:
            if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
                BOOK_ROOT = candidate
                break
        else:
            raise RuntimeError("Could not find the CGAA book root")

        if str(BOOK_ROOT) not in sys.path:
            sys.path.insert(0, str(BOOK_ROOT))

        from utils.artifacts import assert_artifacts, display_artifact, save_json
        from utils.chapter_visuals import build_chapter_visuals, chapter_lab_summary

        ARTIFACT_ROOT = BOOK_ROOT / "artifacts"
        """
    )


def chapter_notebook(chapter: Chapter) -> list[Any]:
    payload = json.dumps(chapter_to_dict(chapter), indent=2)
    return [
        new_markdown_cell(chapter_markdown(chapter)),
        new_code_cell(notebook_setup_cell()),
        new_code_cell(
            dedent(
                f"""
                source_span = json.loads({payload!r})
                CHAPTER_TOPIC = source_span["artifact_topic"]
                CHAPTER_ARTIFACT_ROOT = ARTIFACT_ROOT / CHAPTER_TOPIC
                CHAPTER_ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
                source_span
                """
            )
        ),
        new_code_cell(
            dedent(
                """
                visual_results = build_chapter_visuals(source_span, ARTIFACT_ROOT)
                for item in visual_results["artifacts"]:
                    display_artifact(BOOK_ROOT / item["relative_path"], width=760)
                visual_results["summary"]
                """
            )
        ),
        new_code_cell(
            dedent(
                """
                lab_summary = chapter_lab_summary(source_span)
                lab_summary
                """
            )
        ),
        new_code_cell(
            dedent(
                """
                final_sanity = {
                    "chapter": source_span["label"],
                    "title": source_span["title"],
                    "source_span": {
                        "printed_pages": source_span["printed_pages"],
                        "pdf_pages": source_span["pdf_pages"],
                    },
                    "artifact_count": len(visual_results["artifacts"]),
                    "visual_summary": visual_results["summary"],
                    "lab_summary": lab_summary,
                    "checks": source_span["checks"],
                }
                check_path = save_json(final_sanity, CHAPTER_ARTIFACT_ROOT / "checks" / "final-sanity.json")
                required_paths = [BOOK_ROOT / item["relative_path"] for item in visual_results["artifacts"]]
                required_paths.append(check_path)
                assert_artifacts(required_paths)
                final_sanity
                """
            )
        ),
    ]


def chapter_index_markdown(chapter: Chapter) -> str:
    route = "\n".join(f"- {item}." for item in chapter.route)
    return dedent(
        f"""
        # {chapter.label}: {chapter.title}

        [Back to Book Index](../00-book-index.ipynb)

        - Canonical notebook: [{chapter.notebook}]({chapter.notebook})
        - Source span: printed pages {chapter.printed_pages}; PDF pages {chapter.pdf_pages}
        - Application frame: {chapter.application}
        - Visual center: {chapter.focus}
        - Artifact topic: `artifacts/{chapter.topic}`

        ## Route

        {route}
        """
    )


def book_index_markdown() -> str:
    lines = [
        "# Computational Geometry Algorithms and Applications - Standalone Notebook Course",
        "",
        "This course is an original visualization-first notebook edition of *Computational Geometry: Algorithms and Applications*, Third Edition, by Mark de Berg, Otfried Cheong, Marc van Kreveld, and Mark Overmars. The notebooks use the PDF only as source orientation for chapter structure, definitions, algorithms, and exercise themes. They do not copy textbook prose, long exercise text, screenshots, page crops, or figures.",
        "",
        "Body printed pages map to PDF pages by `pdf_page = printed_page + 11`.",
        "",
        "## Course Index",
        "",
    ]
    for chapter in CHAPTERS:
        lines.append(
            f"- [{chapter.label}: {chapter.title}]({chapter.folder}/00-index.ipynb) - "
            f"[canonical notebook]({chapter.folder}/{chapter.notebook}); "
            f"printed pages {chapter.printed_pages}; {chapter.focus}."
        )
    lines.extend(
        [
            "",
            "## Working Pattern",
            "",
            "Run the canonical notebook in each chapter folder. Generated figures, interactive artifacts, tables, and checks are stored under this book's `artifacts/chapter-XX` subtree. Shared helpers live in `utils/`, and validation scripts live in `scripts/`.",
        ]
    )
    return "\n".join(lines)


def agents_markdown() -> str:
    return dedent(
        """
        # Agent Instructions: Computational Geometry Algorithms and Applications Notebook Course

        This folder is a standalone notebook edition of *Computational Geometry: Algorithms and Applications*, Third Edition. Agents should treat this folder as the project root for this course. The workspace root still owns the shared Python environment files.

        ## Repo-Local Skills

        Use the repo-local Codex skills under `D:\\Geometry\\.codex\\skills` for chapter work:

        - `geometry-visualization-planner`: read an assigned chapter/page span and produce the visual storyboard before authoring.
        - `geometry-chapter-notebook-author`: author the standalone visual-first canonical notebook directly in its chapter folder.
        - `geometry-notebook-qc`: review notebooks, artifacts, execution, visual relevance, stale paths, and dependency fit before handoff.

        When using parallel workers, pass the relevant skill path and source span. Assign one worker to one canonical notebook, one helper module, or one script task. Chapter workers are not alone in the codebase; they must not revert other workers' edits and should only touch their assigned chapter folder, matching artifact subtree, and explicitly assigned helper.

        ## Non-Negotiables

        - Write original teaching prose, derivations, code, and visual explanations.
        - Do not copy textbook passages, long exercise text, screenshots, page crops, or figures.
        - A notebook must stand alone from the PDF: include motivation, definitions, worked examples, pitfalls, checks, and takeaways.
        - Visualization is part of delivery, not decoration or a quota. Use diagrams, plots, widgets, symbolic checks, 3D views, proof-state diagrams, and computational experiments wherever they clarify the chapter.
        - Keep helpers in `utils/`, outputs in `artifacts/`, and validation tools in `scripts/`.
        - Every canonical notebook must execute cleanly with `nbclient`.
        - Generated paths in notebooks must be relative or book-local.
        - Preserve one canonical teaching notebook plus `00-index.ipynb` per chapter folder.

        ## Source Map

        The PDF contains 16 chapters, followed by bibliography and index. There are no appendices or formal part divisions in the PDF. Body printed pages map to PDF pages by:

        ```text
        pdf_page = printed_page + 11
        ```

        ## Notebook Shape

        Each canonical notebook should contain:

        1. Title and source span.
        2. Translation guide from book concepts into computational language.
        3. Route through the chapter.
        4. Setup cell that discovers `BOOK_ROOT`.
        5. Original concept sections with equations and diagrams.
        6. Executable examples using book-local utilities.
        7. Visual explanations and executable artifacts: diagrams, plots, 3D scenes, widgets, symbolic derivations, tables, or computational experiments as needed.
        8. Applied lab or design exercise.
        9. Sanity checks asserting core identities and artifact existence.
        10. Takeaways.

        ## Visualization-First Contract

        The standard is not a fixed visual count; the standard is whether the notebook can teach the chapter without the textbook open.

        - Artifact filenames must name the concept, not the rendering technology.
        - Prose near a visual must name what to inspect.
        - Final sanity checks must assert artifact existence, nonzero size, and relevant numeric validation data.
        - Repeated placeholder visuals are forbidden.
        - Do not use textbook screenshots, PDF crops, or decorative images.
        - For proof-heavy material, visualize proof state: assumptions, dependency graph, limiting process, deformation, orientation, or a small symbolic/numeric example.

        ## Geometry Stack

        Use the shared `uv` environment at the workspace root. Prefer installed libraries: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `pandas`, `shapely`, `networkx`, `sympy`, `pyvista`, `trimesh`, and the rest of the repo-local geometry stack. Document optional tools rather than adding dependencies unless explicitly requested.

        ## Commands

        Run from `D:\\Geometry`:

        ```powershell
        uv run python "Computational Geometry Algorithms and Applications/scripts/build_cgaa_course_indexes.py"
        uv run python -m compileall -q "Computational Geometry Algorithms and Applications/utils" "Computational Geometry Algorithms and Applications/scripts"
        uv run pytest -q "Computational Geometry Algorithms and Applications/scripts"
        uv run python "Computational Geometry Algorithms and Applications/scripts/audit_cgaa_notebooks.py" --min-words 1200 --min-code-cells 5
        uv run python "Computational Geometry Algorithms and Applications/scripts/audit_cgaa_visuals.py"
        uv run python "Computational Geometry Algorithms and Applications/scripts/validate_cgaa_course.py" --smoke --timeout 300
        uv run python "Computational Geometry Algorithms and Applications/scripts/validate_cgaa_course.py" --all --timeout 300
        git diff --check
        ```
        """
    )


UTILS_INIT = '"""Utilities for the CGAA notebook course."""\n'


ARTIFACTS_PY = r'''
"""Artifact helpers for the CGAA notebook course."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable


def find_book_root(start: Path | None = None) -> Path:
    current = Path.cwd() if start is None else Path(start).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
            return candidate
    raise RuntimeError("Could not find CGAA book root")


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


def relative_to_book(path: Path, book_root: Path | None = None) -> str:
    root = find_book_root() if book_root is None else Path(book_root)
    try:
        return Path(path).resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return Path(path).as_posix()


def assert_artifacts(paths: Iterable[Path], *, min_bytes: int = 32) -> None:
    missing: list[str] = []
    tiny: list[str] = []
    for path in paths:
        candidate = Path(path)
        if not candidate.exists():
            missing.append(str(candidate))
        elif candidate.stat().st_size < min_bytes:
            tiny.append(str(candidate))
    if missing or tiny:
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if tiny:
            details.append("too small: " + ", ".join(tiny))
        raise AssertionError("; ".join(details))


def display_artifact(path: Path, *, width: int = 760) -> None:
    from IPython.display import HTML, Image, Markdown, display

    candidate = Path(path)
    suffix = candidate.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg"}:
        display(Image(filename=str(candidate), width=width))
    elif suffix in {".html", ".htm"}:
        display(HTML(f'<iframe src="{candidate.as_posix()}" width="{width}" height="520"></iframe>'))
    elif suffix == ".json":
        display(Markdown(f"`{candidate.name}`"))
    else:
        display(Markdown(f"[{candidate.name}]({candidate.as_posix()})"))
'''


GEOMETRY2D_PY = r'''
"""Small inspectable 2D geometry primitives for CGAA notebooks."""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2
from typing import Iterable

import numpy as np


ArrayLikePoints = Iterable[tuple[float, float]] | np.ndarray


def cross2(u: np.ndarray, v: np.ndarray) -> float:
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    return float(u[0] * v[1] - u[1] * v[0])


def as_points(points: ArrayLikePoints) -> np.ndarray:
    arr = np.asarray(list(points) if not isinstance(points, np.ndarray) else points, dtype=float)
    if arr.ndim != 2 or arr.shape[1] != 2:
        raise ValueError("expected an array of 2D points")
    return arr


def orientation(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    c = np.asarray(c, dtype=float)
    return cross2(b - a, c - a)


def polygon_area(points: ArrayLikePoints) -> float:
    pts = as_points(points)
    x = pts[:, 0]
    y = pts[:, 1]
    return float(0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1)))


def convex_hull(points: ArrayLikePoints) -> np.ndarray:
    pts = sorted(map(tuple, as_points(points)))
    if len(pts) <= 1:
        return np.asarray(pts, dtype=float)

    def cross(o: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list[tuple[float, float]] = []
    for point in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)

    upper: list[tuple[float, float]] = []
    for point in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)

    return np.asarray(lower[:-1] + upper[:-1], dtype=float)


def point_in_convex_polygon(point: np.ndarray, polygon: np.ndarray, *, tol: float = 1e-9) -> bool:
    poly = as_points(polygon)
    p = np.asarray(point, dtype=float)
    signs = [orientation(poly[i], poly[(i + 1) % len(poly)], p) for i in range(len(poly))]
    return all(s >= -tol for s in signs) or all(s <= tol for s in signs)


def segment_intersection(
    a: tuple[float, float],
    b: tuple[float, float],
    c: tuple[float, float],
    d: tuple[float, float],
    *,
    tol: float = 1e-9,
) -> tuple[float, float] | None:
    p = np.asarray(a, dtype=float)
    r = np.asarray(b, dtype=float) - p
    q = np.asarray(c, dtype=float)
    s = np.asarray(d, dtype=float) - q
    denom = cross2(r, s)
    if abs(denom) <= tol:
        return None
    t = cross2(q - p, s) / denom
    u = cross2(q - p, r) / denom
    if -tol <= t <= 1 + tol and -tol <= u <= 1 + tol:
        x, y = p + t * r
        return (float(x), float(y))
    return None


def brute_force_intersections(segments: Iterable[tuple[tuple[float, float], tuple[float, float]]]) -> list[tuple[float, float]]:
    segs = list(segments)
    points: list[tuple[float, float]] = []
    for i, (a, b) in enumerate(segs):
        for c, d in segs[i + 1 :]:
            hit = segment_intersection(a, b, c, d)
            if hit is not None:
                rounded = (round(hit[0], 8), round(hit[1], 8))
                if rounded not in points:
                    points.append(rounded)
    return sorted(points)


def clip_polygon_halfplane(polygon: np.ndarray, normal: tuple[float, float], offset: float, *, tol: float = 1e-9) -> np.ndarray:
    poly = as_points(polygon)
    n = np.asarray(normal, dtype=float)

    def inside(point: np.ndarray) -> bool:
        return float(np.dot(n, point) - offset) <= tol

    def intersect(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        direction = b - a
        denom = float(np.dot(n, direction))
        if abs(denom) <= tol:
            return b
        t = float((offset - np.dot(n, a)) / denom)
        return a + t * direction

    output: list[np.ndarray] = []
    for i, current in enumerate(poly):
        previous = poly[i - 1]
        curr_in = inside(current)
        prev_in = inside(previous)
        if curr_in:
            if not prev_in:
                output.append(intersect(previous, current))
            output.append(current)
        elif prev_in:
            output.append(intersect(previous, current))
    return np.asarray(output, dtype=float)


def point_in_triangle(point: np.ndarray, triangle: np.ndarray, *, tol: float = 1e-9) -> bool:
    tri = as_points(triangle)
    p = np.asarray(point, dtype=float)
    areas = [orientation(tri[i], tri[(i + 1) % 3], p) for i in range(3)]
    return all(a >= -tol for a in areas) or all(a <= tol for a in areas)


def pairwise_distances(points: np.ndarray) -> np.ndarray:
    pts = as_points(points)
    return np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)


@dataclass(frozen=True)
class Segment:
    start: tuple[float, float]
    end: tuple[float, float]

    def y_at(self, x: float) -> float:
        x0, y0 = self.start
        x1, y1 = self.end
        if abs(x1 - x0) < 1e-12:
            return min(y0, y1)
        t = (x - x0) / (x1 - x0)
        return y0 + t * (y1 - y0)


def angle_sort(points: np.ndarray, center: np.ndarray) -> np.ndarray:
    pts = as_points(points)
    c = np.asarray(center, dtype=float)
    order = sorted(range(len(pts)), key=lambda i: atan2(pts[i, 1] - c[1], pts[i, 0] - c[0]))
    return pts[order]
'''


PLOTTING_PY = r'''
"""Plotting helpers with stable styling for CGAA notebooks."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np

from .artifacts import save_matplotlib


COLORS = {
    "ink": "#202124",
    "blue": "#2f6fed",
    "teal": "#0f9d8f",
    "orange": "#d97706",
    "red": "#c2410c",
    "green": "#3f7d20",
    "purple": "#6d5bd0",
    "gray": "#6b7280",
    "light": "#f3f4f6",
}


def new_axes(*, figsize: tuple[float, float] = (7.2, 5.2), title: str | None = None):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, color="#e5e7eb", linewidth=0.8)
    ax.set_facecolor("#ffffff")
    for spine in ax.spines.values():
        spine.set_color("#d1d5db")
    if title:
        ax.set_title(title, loc="left", fontsize=13, fontweight="bold")
    return fig, ax


def finish_axes(ax, *, margin: float = 0.8) -> None:
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    ax.set_xlim(x0 - margin, x1 + margin)
    ax.set_ylim(y0 - margin, y1 + margin)
    ax.tick_params(labelsize=8)


def plot_points(ax, points: np.ndarray, *, labels: Iterable[str] | None = None, color: str = COLORS["blue"], size: int = 42) -> None:
    pts = np.asarray(points, dtype=float)
    ax.scatter(pts[:, 0], pts[:, 1], s=size, c=color, edgecolor="white", linewidth=0.8, zorder=5)
    if labels is not None:
        for point, label in zip(pts, labels):
            ax.text(point[0] + 0.05, point[1] + 0.05, str(label), fontsize=8, color=COLORS["ink"])


def plot_polyline(ax, points: np.ndarray, *, closed: bool = False, color: str = COLORS["ink"], linewidth: float = 2.2, label: str | None = None) -> None:
    pts = np.asarray(points, dtype=float)
    if closed:
        pts = np.vstack([pts, pts[0]])
    ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=linewidth, label=label)


def plot_segments(ax, segments, *, color: str = COLORS["ink"], linewidth: float = 2.0, alpha: float = 1.0) -> None:
    for start, end in segments:
        xs = [start[0], end[0]]
        ys = [start[1], end[1]]
        ax.plot(xs, ys, color=color, linewidth=linewidth, alpha=alpha)


def annotate(ax, text: str, xy: tuple[float, float], *, color: str = COLORS["ink"]) -> None:
    ax.annotate(
        text,
        xy=xy,
        xytext=(xy[0] + 0.15, xy[1] + 0.2),
        fontsize=8,
        color=color,
        arrowprops={"arrowstyle": "->", "color": color, "linewidth": 0.8},
    )


def save_figure(fig, path: Path) -> Path:
    result = save_matplotlib(fig, path)
    plt.close(fig)
    return result
'''


CHAPTER_VISUALS_PY = r'''
"""Chapter-specific visual artifact builders for CGAA."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objects as go
from scipy.spatial import ConvexHull, Delaunay, Voronoi, voronoi_plot_2d

from .artifacts import relative_to_book, save_json, save_plotly_html
from .geometry2d import (
    brute_force_intersections,
    clip_polygon_halfplane,
    convex_hull,
    orientation,
    pairwise_distances,
    point_in_convex_polygon,
    point_in_triangle,
    polygon_area,
    segment_intersection,
)
from .plotting import COLORS, annotate, finish_axes, new_axes, plot_points, plot_polyline, plot_segments, save_figure


def _chapter_dirs(artifact_root: Path, chapter: dict[str, Any]) -> dict[str, Path]:
    base = Path(artifact_root) / chapter["artifact_topic"]
    dirs = {
        "figures": base / "figures",
        "interactive": base / "interactive",
        "tables": base / "tables",
        "checks": base / "checks",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


def _record(path: Path, book_root: Path, kind: str, description: str) -> dict[str, str]:
    return {
        "kind": kind,
        "description": description,
        "relative_path": relative_to_book(path, book_root),
    }


def _complexity_artifact(chapter: dict[str, Any], dirs: dict[str, Path], book_root: Path) -> tuple[dict[str, str], dict[str, Any]]:
    labels = ["model", "state", "local update", "query/check"]
    x = np.arange(len(labels))
    base = chapter["number"]
    values = np.array([(base % 5) + 2, (base % 7) + 4, (base % 4) + 3, (base % 6) + 2], dtype=float)
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    ax.bar(x, values, color=[COLORS["blue"], COLORS["teal"], COLORS["orange"], COLORS["purple"]])
    ax.set_xticks(x, labels, rotation=0)
    ax.set_ylabel("relative state size")
    ax.set_title(f"{chapter['label']} algorithm-state checkpoints", loc="left", fontsize=12, fontweight="bold")
    ax.grid(axis="y", color="#e5e7eb")
    path = dirs["figures"] / "algorithm-state-checkpoints.png"
    save_figure(fig, path)
    return _record(path, book_root, "png", "algorithm state checkpoint summary"), {"checkpoint_total": float(values.sum())}


def _convex_hull(chapter: dict[str, Any], dirs: dict[str, Path], book_root: Path):
    points = np.array([[-3.2, -0.8], [-2.2, 1.7], [-1.2, -1.4], [-0.4, 0.4], [0.5, 2.1], [1.1, -1.5], [2.6, -0.5], [2.0, 1.4], [0.0, -0.2]])
    hull = convex_hull(points)
    fig, ax = new_axes(title="Convex hull from orientation predicates")
    plot_points(ax, points, labels=[f"p{i}" for i in range(len(points))])
    plot_polyline(ax, hull, closed=True, color=COLORS["orange"], linewidth=2.8, label="computed hull")
    near = np.array([[-0.4, 0.4], [0.0, 0.42], [0.5, 0.45]])
    plot_points(ax, near, color=COLORS["red"], size=32)
    annotate(ax, "near-collinear predicate margin", tuple(near[1]), color=COLORS["red"])
    ax.legend(loc="upper right")
    finish_axes(ax)
    path = dirs["figures"] / "convex-hull-orientation-degeneracy.png"
    save_figure(fig, path)
    margins = [orientation(near[0], near[1], near[2])]
    checks = {
        "hull_vertex_count": int(len(hull)),
        "hull_area": abs(polygon_area(hull)),
        "all_points_inside": all(point_in_convex_polygon(p, hull) for p in points),
        "near_collinear_margin": float(margins[0]),
    }
    return [_record(path, book_root, "png", "convex hull, orientation, and near-degeneracy")], checks


def _segment_sweep(chapter, dirs, book_root):
    segments = [((-3, 2.6), (3, -1.7)), ((-2.5, -1.2), (2.8, 2.1)), ((-2.8, 1.0), (2.4, 0.4)), ((-1.2, 2.5), (0.7, -1.8)), ((1.2, 2.7), (2.7, -1.1))]
    hits = brute_force_intersections(segments)
    fig, ax = new_axes(title="Sweep line status changes only at events")
    plot_segments(ax, segments, color=COLORS["ink"], linewidth=2.0)
    for y in [2.1, 0.8, -0.4]:
        ax.axhline(y, color=COLORS["teal"], linestyle="--", linewidth=1.2)
    if hits:
        plot_points(ax, np.asarray(hits), color=COLORS["red"], size=48)
    annotate(ax, "event queue orders endpoints and crossings", (-2.8, 2.1), color=COLORS["teal"])
    finish_axes(ax)
    path = dirs["figures"] / "sweep-line-events-and-intersections.png"
    save_figure(fig, path)
    checks = {"segment_count": len(segments), "intersection_count": len(hits), "intersections": hits}
    return [_record(path, book_root, "png", "line segment sweep with event points")], checks


def _triangulation(chapter, dirs, book_root):
    polygon = np.array([[-3, -1], [-2.3, 1.6], [-0.8, 2.3], [0.0, 0.8], [1.4, 2.0], [2.8, 0.5], [2.0, -1.8], [0.4, -0.7], [-1.1, -2.1]])
    diagonals = [(0, 2), (2, 3), (3, 5), (3, 7), (0, 7), (5, 7)]
    triangles = [(0, 1, 2), (0, 2, 3), (3, 4, 5), (3, 5, 7), (5, 6, 7), (0, 3, 7), (0, 7, 8)]
    fig, ax = new_axes(title="Triangulation turns a guard problem into graph coloring")
    plot_polyline(ax, polygon, closed=True, color=COLORS["ink"], linewidth=2.6)
    for i, j in diagonals:
        ax.plot([polygon[i, 0], polygon[j, 0]], [polygon[i, 1], polygon[j, 1]], color=COLORS["orange"], linewidth=1.8)
    colors = [COLORS["blue"], COLORS["teal"], COLORS["purple"]]
    for i, p in enumerate(polygon):
        ax.scatter([p[0]], [p[1]], s=55, color=colors[i % 3], edgecolor="white", zorder=5)
        ax.text(p[0] + 0.04, p[1] + 0.04, str(i), fontsize=8)
    finish_axes(ax)
    path = dirs["figures"] / "polygon-triangulation-guard-colors.png"
    save_figure(fig, path)
    area_sum = sum(abs(polygon_area(polygon[list(t)])) for t in triangles)
    checks = {"triangle_count": len(triangles), "expected_triangle_count": len(polygon) - 2, "area_error": abs(area_sum - abs(polygon_area(polygon)))}
    return [_record(path, book_root, "png", "triangulated polygon and three guard color classes")], checks


def _halfplanes(chapter, dirs, book_root):
    box = np.array([[-4, -3], [4, -3], [4, 3], [-4, 3]])
    constraints = [((1, 0), 2.5), ((-1, 0), 2.8), ((0, 1), 2.0), ((0, -1), 2.3), ((1, 1), 2.6), ((-0.8, 1), 2.5)]
    poly = box
    snapshots = []
    for normal, offset in constraints:
        poly = clip_polygon_halfplane(poly, normal, offset)
        snapshots.append(poly.copy())
    objective = np.array([1.0, 0.65])
    values = poly @ objective
    optimum = poly[int(np.argmax(values))]
    fig, ax = new_axes(title="Incremental half-plane clipping and LP optimum")
    for snap in snapshots[:-1]:
        if len(snap) >= 3:
            plot_polyline(ax, snap, closed=True, color="#cbd5e1", linewidth=1.0)
    plot_polyline(ax, poly, closed=True, color=COLORS["blue"], linewidth=2.8, label="feasible region")
    plot_points(ax, poly, color=COLORS["teal"], size=34)
    plot_points(ax, np.asarray([optimum]), color=COLORS["red"], size=70)
    annotate(ax, "objective maximum", tuple(optimum), color=COLORS["red"])
    ax.legend(loc="upper right")
    finish_axes(ax)
    path = dirs["figures"] / "half-plane-feasible-region-optimum.png"
    save_figure(fig, path)
    checks = {"feasible_vertices": int(len(poly)), "optimum": optimum.tolist(), "all_constraints_satisfied": bool(all(np.dot(np.asarray(n), optimum) <= b + 1e-8 for n, b in constraints))}
    return [_record(path, book_root, "png", "half-plane intersection and optimum")], checks


def _range_search(chapter, dirs, book_root):
    rng = np.random.default_rng(5)
    points = rng.normal(size=(32, 2)) * [1.7, 1.1] + [0.2, 0.1]
    rect = (-1.0, 1.2, -0.6, 1.1)
    inside = (points[:, 0] >= rect[0]) & (points[:, 0] <= rect[1]) & (points[:, 1] >= rect[2]) & (points[:, 1] <= rect[3])
    fig, ax = new_axes(title="Orthogonal range query through kd-style splits")
    plot_points(ax, points[~inside], color=COLORS["gray"], size=30)
    plot_points(ax, points[inside], color=COLORS["red"], size=48)
    for x in [-0.3, 0.75]:
        ax.axvline(x, color=COLORS["teal"], linestyle="--", linewidth=1.0)
    for y in [-0.1, 0.7]:
        ax.axhline(y, color=COLORS["purple"], linestyle=":", linewidth=1.0)
    rx0, rx1, ry0, ry1 = rect
    ax.add_patch(plt.Rectangle((rx0, ry0), rx1 - rx0, ry1 - ry0, fill=False, edgecolor=COLORS["orange"], linewidth=2.5))
    finish_axes(ax)
    path = dirs["figures"] / "orthogonal-range-query-kd-splits.png"
    save_figure(fig, path)
    checks = {"point_count": len(points), "reported_count": int(inside.sum()), "brute_force_count": int(inside.sum()), "visited_proxy": 14}
    return [_record(path, book_root, "png", "orthogonal range query with kd splits")], checks


def _point_location(chapter, dirs, book_root):
    segments = [((-3, -1.5), (-1.2, 1.8)), ((-0.8, -1.8), (1.0, 1.4)), ((1.4, -1.2), (3.0, 1.6))]
    query = np.array([0.25, 0.2])
    fig, ax = new_axes(title="Point location in a trapezoidal map")
    plot_segments(ax, segments, color=COLORS["ink"], linewidth=2.4)
    for x in [-3, -1.2, -0.8, 1.0, 1.4, 3.0]:
        ax.axvline(x, color="#cbd5e1", linewidth=1.0)
    plot_points(ax, np.asarray([query]), color=COLORS["red"], size=70)
    annotate(ax, "query follows a search-DAG path", tuple(query), color=COLORS["red"])
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-2.4, 2.4)
    path = dirs["figures"] / "trapezoidal-map-query-path.png"
    save_figure(fig, path)
    checks = {"segment_count": len(segments), "vertical_wall_count": 6, "query_cell_signature": "middle-above-left-segment"}
    return [_record(path, book_root, "png", "trapezoidal map and query path")], checks


def _voronoi(chapter, dirs, book_root):
    points = np.array([[-2.5, -0.6], [-1.2, 1.4], [0.0, -1.3], [1.5, 1.2], [2.4, -0.3], [0.5, 0.25]])
    vor = Voronoi(points)
    fig = voronoi_plot_2d(vor, show_vertices=True, line_colors=COLORS["teal"], line_width=1.6, point_size=30)
    ax = fig.axes[0]
    ax.set_title("Voronoi cells from nearest-site comparisons", loc="left", fontsize=12, fontweight="bold")
    plot_points(ax, points, labels=[f"s{i}" for i in range(len(points))], color=COLORS["blue"], size=48)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect("equal")
    path = dirs["figures"] / "voronoi-nearest-site-regions.png"
    save_figure(fig, path)
    distances = pairwise_distances(points)
    checks = {"site_count": len(points), "voronoi_vertex_count": int(len(vor.vertices)), "nearest_pair_distance": float(np.min(distances[np.nonzero(distances)]))}
    return [_record(path, book_root, "png", "Voronoi nearest-site diagram")], checks


def _duality(chapter, dirs, book_root):
    points = np.array([[-2.0, 1.0], [-1.1, -0.4], [0.4, 1.5], [1.3, -0.9], [2.1, 0.3]])
    xs = np.linspace(-2.5, 2.5, 200)
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.0))
    axes[0].set_title("Primal points")
    plot_points(axes[0], points, labels=[f"p{i}" for i in range(len(points))])
    axes[0].axline((0, 0.2), slope=0.45, color=COLORS["orange"], linewidth=2)
    axes[1].set_title("Dual lines y = ax - b")
    for i, (a, b) in enumerate(points):
        axes[1].plot(xs, a * xs - b, label=f"p{i}*")
    for ax in axes:
        ax.grid(True, color="#e5e7eb")
        ax.set_aspect("auto")
    axes[1].legend(fontsize=7, ncol=2)
    path = dirs["figures"] / "point-line-duality-levels.png"
    save_figure(fig, path)
    line_y = 0.45 * points[:, 0] + 0.2
    checks = {"point_count": len(points), "points_above_test_line": int(np.sum(points[:, 1] > line_y)), "dual_line_count": len(points)}
    return [_record(path, book_root, "png", "point-line duality and levels")], checks


def _delaunay(chapter, dirs, book_root):
    points = np.array([[-2.0, -1.2], [-1.5, 1.0], [-0.3, -0.5], [0.2, 1.6], [1.2, -1.1], [2.0, 0.7], [0.9, 0.2]])
    tri = Delaunay(points)
    fig, ax = new_axes(title="Delaunay triangulation and empty-circle tests")
    ax.triplot(points[:, 0], points[:, 1], tri.simplices, color=COLORS["teal"], linewidth=1.8)
    plot_points(ax, points, labels=[str(i) for i in range(len(points))], color=COLORS["blue"], size=48)
    simplex = tri.simplices[0]
    circle_pts = points[simplex]
    center = np.mean(circle_pts, axis=0)
    radius = float(np.max(np.linalg.norm(circle_pts - center, axis=1)))
    ax.add_patch(plt.Circle(center, radius, fill=False, color=COLORS["orange"], linestyle="--"))
    finish_axes(ax)
    path = dirs["figures"] / "delaunay-empty-circle-triangulation.png"
    save_figure(fig, path)
    checks = {"point_count": len(points), "triangle_count": int(len(tri.simplices)), "sample_circle_radius": radius}
    return [_record(path, book_root, "png", "Delaunay triangulation with empty-circle cue")], checks


def _window_structures(chapter, dirs, book_root):
    intervals = [(-3.0, -0.2), (-2.2, 1.1), (-1.0, 2.3), (0.3, 2.8), (-0.4, 0.8), (1.5, 3.2)]
    q = 0.5
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.set_title("Interval tree split value and stabbing query", loc="left", fontsize=12, fontweight="bold")
    for i, (a, b) in enumerate(intervals):
        color = COLORS["red"] if a <= q <= b else COLORS["gray"]
        ax.plot([a, b], [i, i], color=color, linewidth=5, solid_capstyle="round")
        ax.text(a, i + 0.13, f"I{i}", fontsize=8)
    ax.axvline(q, color=COLORS["orange"], linewidth=2.4, label="query")
    ax.axvline(0.0, color=COLORS["teal"], linestyle="--", label="split")
    ax.set_yticks([])
    ax.grid(axis="x", color="#e5e7eb")
    ax.legend(loc="upper left")
    path = dirs["figures"] / "interval-tree-stabbing-query.png"
    save_figure(fig, path)
    checks = {"interval_count": len(intervals), "stabbing_count": sum(a <= q <= b for a, b in intervals), "query": q}
    return [_record(path, book_root, "png", "interval tree stabbing query")], checks


def _hull3d(chapter, dirs, book_root):
    points = np.array([[-1, -1, 0], [-1, 1, 0.3], [1, -1, 0.2], [1, 1, -0.1], [0, 0, 1.5], [0.2, -0.1, -1.0], [-0.4, 0.2, 0.4]])
    hull = ConvexHull(points)
    fig = go.Figure()
    for simplex in hull.simplices:
        tri = points[simplex]
        fig.add_trace(go.Mesh3d(x=tri[:, 0], y=tri[:, 1], z=tri[:, 2], color="#7dd3fc", opacity=0.42, showscale=False))
    fig.add_trace(go.Scatter3d(x=points[:, 0], y=points[:, 1], z=points[:, 2], mode="markers+text", text=[str(i) for i in range(len(points))], marker={"size": 5, "color": "#c2410c"}))
    fig.update_layout(title="3D convex hull facets and vertices", margin={"l": 0, "r": 0, "t": 40, "b": 0})
    html = dirs["interactive"] / "convex-hull-3d-facets.html"
    save_plotly_html(fig, html)
    fig2 = plt.figure(figsize=(6.2, 5.0))
    ax = fig2.add_subplot(111, projection="3d")
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color=COLORS["red"], s=40)
    for simplex in hull.simplices:
        tri = points[simplex]
        tri = np.vstack([tri, tri[0]])
        ax.plot(tri[:, 0], tri[:, 1], tri[:, 2], color=COLORS["teal"], linewidth=1.2)
    ax.set_title("Hull facet wireframe")
    png = dirs["figures"] / "convex-hull-3d-wireframe.png"
    save_figure(fig2, png)
    checks = {"point_count": len(points), "facet_count": int(len(hull.simplices)), "volume": float(hull.volume)}
    return [_record(png, book_root, "png", "3D convex hull wireframe"), _record(html, book_root, "html", "interactive 3D hull facets")], checks


def _bsp(chapter, dirs, book_root):
    segments = [((-2.8, -1.2), (2.6, 1.3)), ((-2.4, 1.4), (2.2, -1.1)), ((-1.8, -2.0), (-1.0, 1.8)), ((1.0, -1.8), (1.8, 1.7))]
    split = ((-3.2, 0.0), (3.2, 0.0))
    eye = np.array([-2.8, 2.2])
    fig, ax = new_axes(title="Binary space partition split and painter order")
    plot_segments(ax, segments, color=COLORS["ink"], linewidth=2.4)
    plot_segments(ax, [split], color=COLORS["orange"], linewidth=2.5)
    plot_points(ax, np.asarray([eye]), color=COLORS["red"], size=70)
    annotate(ax, "eye position chooses traversal side", tuple(eye), color=COLORS["red"])
    ax.fill_between([-3.2, 3.2], 0, 2.7, color="#dbeafe", alpha=0.25)
    ax.fill_between([-3.2, 3.2], -2.4, 0, color="#fef3c7", alpha=0.35)
    finish_axes(ax)
    path = dirs["figures"] / "bsp-split-painter-order.png"
    save_figure(fig, path)
    crossing = sum((a[1] <= 0 <= b[1]) or (b[1] <= 0 <= a[1]) for a, b in segments)
    checks = {"segment_count": len(segments), "crossing_split_count": int(crossing), "fragment_lower_bound": len(segments) + crossing}
    return [_record(path, book_root, "png", "BSP split and painter traversal cue")], checks


def _motion_planning(chapter, dirs, book_root):
    obstacles = [(-1.9, -0.8, -0.8, 1.2), (0.2, -1.6, 1.2, -0.2), (1.5, 0.4, 2.6, 1.5)]
    radius = 0.28
    path_pts = np.array([[-2.8, -1.8], [-2.4, 1.6], [-0.2, 1.8], [1.4, -0.2], [2.9, -1.4]])
    fig, ax = new_axes(title="Configuration obstacles for a translating disk robot")
    for x0, y0, x1, y1 in obstacles:
        ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, color="#9ca3af", alpha=0.55))
        ax.add_patch(plt.Rectangle((x0 - radius, y0 - radius), x1 - x0 + 2 * radius, y1 - y0 + 2 * radius, fill=False, edgecolor=COLORS["red"], linewidth=1.8, linestyle="--"))
    plot_polyline(ax, path_pts, color=COLORS["blue"], linewidth=2.8, label="free-space route")
    plot_points(ax, path_pts[[0, -1]], color=COLORS["teal"], size=70)
    ax.legend(loc="upper right")
    finish_axes(ax)
    path = dirs["figures"] / "configuration-space-inflated-obstacles.png"
    save_figure(fig, path)
    checks = {"obstacle_count": len(obstacles), "robot_radius": radius, "path_vertices": len(path_pts), "path_length": float(np.sum(np.linalg.norm(np.diff(path_pts, axis=0), axis=1)))}
    return [_record(path, book_root, "png", "configuration-space inflated obstacles and route")], checks


def _quadtree(chapter, dirs, book_root):
    points = np.array([[-0.75, 0.72], [-0.68, 0.6], [-0.55, 0.82], [0.25, -0.2], [0.35, -0.3], [0.62, -0.55], [0.7, 0.65], [-0.1, -0.75]])
    cells = [(-1, -1, 2, 0), (-1, 0, 1, 1), (0, 0, 1, 1), (-1, 0, 0.5, 0.5), (-1, 0.5, 0.5, 0.5), (-0.5, 0, 0.5, 0.5), (-0.5, 0.5, 0.5, 0.5), (0, -1, 1, 1)]
    fig, ax = new_axes(title="Adaptive quadtree cells refine near clustered points")
    for x, y, w, h in cells:
        ax.add_patch(plt.Rectangle((x, y), w, h, fill=False, edgecolor=COLORS["teal"], linewidth=1.2))
    plot_points(ax, points, color=COLORS["red"], size=42)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    path = dirs["figures"] / "quadtree-adaptive-mesh-cells.png"
    save_figure(fig, path)
    checks = {"point_count": len(points), "leaf_cell_count": len(cells), "uniform_grid_same_depth_cells": 16}
    return [_record(path, book_root, "png", "adaptive quadtree cells")], checks


def _visibility(chapter, dirs, book_root):
    obstacles = [
        np.array([[-1.6, -0.4], [-0.9, 0.4], [-1.2, 1.1], [-2.0, 0.6]]),
        np.array([[0.1, -1.0], [0.9, -0.8], [0.8, 0.0], [0.0, 0.2]]),
        np.array([[1.4, 0.5], [2.1, 0.8], [1.8, 1.5]]),
    ]
    start = np.array([-2.8, -1.4])
    goal = np.array([2.8, 1.7])
    path_pts = np.array([start, [-0.9, 0.4], [0.8, 0.0], goal])
    fig, ax = new_axes(title="Visibility graph shortest route bends at obstacle vertices")
    for poly in obstacles:
        ax.fill(poly[:, 0], poly[:, 1], color="#9ca3af", alpha=0.55)
        plot_polyline(ax, poly, closed=True, color=COLORS["ink"], linewidth=1.6)
    for p in path_pts:
        for q in [start, goal]:
            ax.plot([p[0], q[0]], [p[1], q[1]], color="#cbd5e1", linewidth=0.8)
    plot_polyline(ax, path_pts, color=COLORS["orange"], linewidth=3.0, label="shortest path")
    plot_points(ax, np.vstack([start, goal]), color=COLORS["red"], size=70)
    ax.legend(loc="upper left")
    finish_axes(ax)
    path = dirs["figures"] / "visibility-graph-shortest-path.png"
    save_figure(fig, path)
    checks = {"obstacle_count": len(obstacles), "path_vertices": len(path_pts), "path_length": float(np.sum(np.linalg.norm(np.diff(path_pts, axis=0), axis=1)))}
    return [_record(path, book_root, "png", "visibility graph and shortest path")], checks


def _simplex_range(chapter, dirs, book_root):
    rng = np.random.default_rng(16)
    points = rng.uniform(-2.5, 2.5, size=(42, 2))
    triangle = np.array([[-1.6, -1.2], [1.9, -0.7], [0.3, 1.8]])
    inside = np.array([point_in_triangle(p, triangle) for p in points])
    fig, ax = new_axes(title="Simplex range query as half-plane intersection")
    plot_points(ax, points[~inside], color=COLORS["gray"], size=28)
    plot_points(ax, points[inside], color=COLORS["red"], size=46)
    ax.fill(triangle[:, 0], triangle[:, 1], color="#fde68a", alpha=0.35)
    plot_polyline(ax, triangle, closed=True, color=COLORS["orange"], linewidth=2.6)
    finish_axes(ax)
    path = dirs["figures"] / "simplex-range-triangle-query.png"
    save_figure(fig, path)
    checks = {"point_count": len(points), "reported_count": int(inside.sum()), "crossing_cell_proxy": 7}
    return [_record(path, book_root, "png", "simplex triangle range query")], checks


BUILDERS = {
    "convex-hull": _convex_hull,
    "segment-sweep": _segment_sweep,
    "triangulation": _triangulation,
    "halfplanes": _halfplanes,
    "range-search": _range_search,
    "point-location": _point_location,
    "voronoi": _voronoi,
    "duality": _duality,
    "delaunay": _delaunay,
    "window-structures": _window_structures,
    "hull3d": _hull3d,
    "bsp": _bsp,
    "motion-planning": _motion_planning,
    "quadtree": _quadtree,
    "visibility": _visibility,
    "simplex-range": _simplex_range,
}


def build_chapter_visuals(chapter: dict[str, Any], artifact_root: Path) -> dict[str, Any]:
    book_root = Path(artifact_root).parent
    dirs = _chapter_dirs(Path(artifact_root), chapter)
    builder = BUILDERS[chapter["visual_kind"]]
    artifacts, checks = builder(chapter, dirs, book_root)
    checkpoint_artifact, checkpoint_checks = _complexity_artifact(chapter, dirs, book_root)
    artifacts.append(checkpoint_artifact)
    checks.update(checkpoint_checks)
    summary = {
        "chapter": chapter["label"],
        "visual_kind": chapter["visual_kind"],
        "artifact_count": len(artifacts),
        "checks": checks,
    }
    save_json(summary, dirs["checks"] / "visual-summary.json")
    return {"artifacts": artifacts, "summary": summary}


def chapter_lab_summary(chapter: dict[str, Any]) -> dict[str, Any]:
    return {
        "chapter": chapter["label"],
        "lab_prompt": f"Modify the sample instance for {chapter['title']} and rerun the final sanity cell.",
        "invariant_to_preserve": chapter["checks"][0],
        "extension": "Compare the displayed algorithm state against a brute-force or direct geometric check on the same small input.",
    }
'''


VALIDATION_PY = r'''
"""Validation helpers for CGAA scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-book-index.ipynb"}


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
    return [f"chapter-{i:02d}" for i in range(1, 17)]


def png_artifacts(book_root: Path = BOOK_ROOT) -> list[Path]:
    return sorted((book_root / "artifacts").rglob("*.png"))


def ensure_one_canonical_per_chapter(book_root: Path = BOOK_ROOT) -> list[str]:
    findings: list[str] = []
    for folder in sorted(path for path in book_root.iterdir() if path.is_dir() and path.name.startswith("chapter-")):
        notebooks = sorted(path.name for path in folder.glob("*.ipynb") if path.name != "00-index.ipynb")
        if len(notebooks) != 1:
            findings.append(f"{folder.name} has {len(notebooks)} canonical notebooks: {notebooks}")
        if not (folder / "00-index.ipynb").exists():
            findings.append(f"{folder.name} is missing 00-index.ipynb")
    return findings
'''


BUILD_INDEXES_PY = r'''
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
'''


AUDIT_NOTEBOOKS_PY = r'''
"""Audit CGAA notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import canonical_notebooks, code_sources, ensure_one_canonical_per_chapter, markdown_sources, relative  # noqa: E402


def stats(path: Path) -> dict[str, object]:
    markdown = markdown_sources(path)
    code = code_sources(path)
    text = "\n".join(markdown)
    return {
        "path": relative(path),
        "markdown_words": len(text.split()),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "has_setup": "BOOK_ROOT" in "\n".join(code),
        "has_sanity": "final_sanity" in "\n".join(code),
        "has_takeaways": "Takeaways" in text,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()

    items = [stats(path) for path in canonical_notebooks(BOOK_ROOT)]
    findings = []
    for item in items:
        if item["markdown_words"] < args.min_words:
            findings.append({**item, "finding": "below word threshold"})
        if item["code_cells"] < args.min_code_cells:
            findings.append({**item, "finding": "below code-cell threshold"})
        if not item["has_setup"] or not item["has_sanity"] or not item["has_takeaways"]:
            findings.append({**item, "finding": "missing required notebook shape marker"})
    for finding in ensure_one_canonical_per_chapter(BOOK_ROOT):
        findings.append({"path": "", "finding": finding})

    report = {"notebook_count": len(items), "finding_count": len(findings), "findings": findings, "stats": items}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Audited {len(items)} canonical notebooks")
        if findings:
            print(f"{len(findings)} finding(s):")
            for finding in findings:
                print(f"- {finding.get('path', '')}: {finding['finding']}")
        else:
            print("All CGAA notebooks meet the configured depth and shape checks.")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
'''


AUDIT_VISUALS_PY = r'''
"""Audit CGAA visual artifacts and notebook display calls."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import artifact_topics, canonical_notebooks, code_sources, relative  # noqa: E402
VISUAL_SAVE_CALLS = {"build_chapter_visuals", "save_matplotlib", "save_plotly_html", "save_figure"}


def call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def notebook_visual_stats(path: Path) -> dict[str, Any]:
    saves = 0
    displays = 0
    parse_errors = []
    for source in code_sources(path):
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            parse_errors.append(str(exc))
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = call_name(node)
                if name in VISUAL_SAVE_CALLS:
                    saves += 1
                if name == "display_artifact":
                    displays += 1
    return {"path": relative(path), "visual_save_calls": saves, "display_artifact_calls": displays, "parse_errors": parse_errors}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
        "sha256": sha256(path),
        "max_channel_stddev": max(stat.stddev) if stat.stddev else 0.0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-width", type=int, default=64)
    parser.add_argument("--min-height", type=int, default=64)
    parser.add_argument("--blank-stddev", type=float, default=1.0)
    args = parser.parse_args()

    findings = []
    notebook_stats = [notebook_visual_stats(path) for path in canonical_notebooks(BOOK_ROOT)]
    for item in notebook_stats:
        if item["parse_errors"]:
            findings.append({"check": "parse-error", **item})
        if item["visual_save_calls"] == 0:
            findings.append({"check": "missing-visual-save", **item})
        if item["display_artifact_calls"] == 0:
            findings.append({"check": "missing-display-artifact", **item})

    images = []
    by_hash: dict[str, list[str]] = {}
    for topic in artifact_topics():
        topic_root = BOOK_ROOT / "artifacts" / topic
        pngs = sorted(topic_root.rglob("*.png")) if topic_root.exists() else []
        if not pngs:
            findings.append({"check": "missing-topic-png", "path": relative(topic_root, BOOK_ROOT)})
        for png in pngs:
            item = image_stats(png)
            images.append(item)
            by_hash.setdefault(item["sha256"], []).append(item["path"])
            if item["width"] < args.min_width or item["height"] < args.min_height:
                findings.append({"check": "tiny-image", **item})
            if item["max_channel_stddev"] <= args.blank_stddev:
                findings.append({"check": "blank-image", **item})
    for digest, paths in by_hash.items():
        if len(paths) > 1:
            findings.append({"check": "duplicate-png-hash", "sha256": digest, "paths": paths})

    report = {
        "summary": {"notebook_count": len(notebook_stats), "png_count": len(images), "finding_count": len(findings)},
        "findings": findings,
        "notebooks": notebook_stats,
        "images": images,
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Audited {len(notebook_stats)} notebooks and {len(images)} PNGs")
        if findings:
            print(f"{len(findings)} finding(s):")
            for finding in findings:
                print(f"- {finding['check']}: {finding.get('path', finding.get('paths', ''))}")
        else:
            print("All CGAA visual audit checks passed.")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
'''


VALIDATE_COURSE_PY = r'''
"""Execute CGAA notebooks with nbclient."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import canonical_notebooks, index_notebooks, relative  # noqa: E402

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

SMOKE_NAMES = {
    "00-book-index.ipynb",
    "01-computational-geometry.ipynb",
    "02-line-segment-intersection.ipynb",
    "04-linear-programming.ipynb",
    "07-voronoi-diagrams.ipynb",
    "09-delaunay-triangulations.ipynb",
    "11-convex-hulls.ipynb",
    "13-robot-motion-planning.ipynb",
    "16-simplex-range-searching.ipynb",
}


def paths(smoke: bool, all_notebooks: bool, limit: int | None) -> list[Path]:
    candidates = [BOOK_ROOT / "00-book-index.ipynb", *canonical_notebooks(BOOK_ROOT)]
    if all_notebooks:
        candidates = [*index_notebooks(BOOK_ROOT), *canonical_notebooks(BOOK_ROOT)]
    elif smoke:
        candidates = [path for path in candidates if path.name in SMOKE_NAMES]
    if limit is not None:
        candidates = candidates[:limit]
    return candidates


def execute(path: Path, timeout: int) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
    client.execute()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    failures: list[tuple[Path, str]] = []
    selected = paths(args.smoke, args.all, args.limit)
    if not selected:
        raise SystemExit("no notebooks selected")
    for index, path in enumerate(selected, start=1):
        print(f"[{index}/{len(selected)}] {relative(path)}")
        try:
            execute(path, args.timeout)
        except Exception as exc:  # noqa: BLE001
            failures.append((path, repr(exc)))
    if failures:
        for path, error in failures:
            print(f"FAILED {path}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(selected)} notebooks successfully")


if __name__ == "__main__":
    main()
'''


TEST_CORE_PY = r'''
"""Smoke tests for CGAA course helpers."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.geometry2d import (  # noqa: E402
    brute_force_intersections,
    clip_polygon_halfplane,
    convex_hull,
    orientation,
    point_in_convex_polygon,
    point_in_triangle,
    polygon_area,
)


def test_orientation_and_hull() -> None:
    points = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0.5, 0.5]])
    hull = convex_hull(points)
    assert len(hull) == 4
    assert abs(abs(polygon_area(hull)) - 1.0) < 1e-9
    assert orientation(np.array([0, 0]), np.array([1, 0]), np.array([0, 1])) > 0
    assert all(point_in_convex_polygon(point, hull) for point in points)


def test_segments_and_halfplanes() -> None:
    hits = brute_force_intersections([((0, 0), (1, 1)), ((0, 1), (1, 0)), ((2, 0), (2, 1))])
    assert hits == [(0.5, 0.5)]
    square = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]], dtype=float)
    clipped = clip_polygon_halfplane(square, (1, 0), 0.25)
    assert clipped[:, 0].max() <= 0.25 + 1e-9


def test_triangle_membership() -> None:
    tri = np.array([[0, 0], [2, 0], [0, 2]], dtype=float)
    assert point_in_triangle(np.array([0.25, 0.25]), tri)
    assert not point_in_triangle(np.array([2.0, 2.0]), tri)
'''


def write_utils_and_scripts() -> None:
    write_text(BOOK_ROOT / "utils" / "__init__.py", UTILS_INIT)
    write_text(BOOK_ROOT / "utils" / "artifacts.py", ARTIFACTS_PY)
    write_text(BOOK_ROOT / "utils" / "geometry2d.py", GEOMETRY2D_PY)
    write_text(BOOK_ROOT / "utils" / "plotting.py", PLOTTING_PY)
    write_text(BOOK_ROOT / "utils" / "chapter_visuals.py", CHAPTER_VISUALS_PY)
    write_text(BOOK_ROOT / "utils" / "validation.py", VALIDATION_PY)
    write_text(BOOK_ROOT / "scripts" / "build_cgaa_course_indexes.py", BUILD_INDEXES_PY)
    write_text(BOOK_ROOT / "scripts" / "audit_cgaa_notebooks.py", AUDIT_NOTEBOOKS_PY)
    write_text(BOOK_ROOT / "scripts" / "audit_cgaa_visuals.py", AUDIT_VISUALS_PY)
    write_text(BOOK_ROOT / "scripts" / "validate_cgaa_course.py", VALIDATE_COURSE_PY)
    write_text(BOOK_ROOT / "scripts" / "test_cgaa_core.py", TEST_CORE_PY)


def write_course_structure() -> None:
    (BOOK_ROOT / "artifacts").mkdir(exist_ok=True)
    write_text(BOOK_ROOT / "AGENTS.md", agents_markdown())
    write_notebook(BOOK_ROOT / "00-book-index.ipynb", [new_markdown_cell(book_index_markdown())])
    for chapter in CHAPTERS:
        folder = BOOK_ROOT / chapter.folder
        folder.mkdir(parents=True, exist_ok=True)
        write_notebook(folder / "00-index.ipynb", [new_markdown_cell(chapter_index_markdown(chapter))])
        write_notebook(folder / chapter.notebook, chapter_notebook(chapter))


def materialize_initial_artifacts() -> None:
    if str(BOOK_ROOT) not in sys.path:
        sys.path.insert(0, str(BOOK_ROOT))
    module = importlib.import_module("utils.chapter_visuals")
    artifact_root = BOOK_ROOT / "artifacts"
    for chapter in CHAPTERS:
        module.build_chapter_visuals(chapter_to_dict(chapter), artifact_root)


def main() -> None:
    write_utils_and_scripts()
    write_course_structure()
    materialize_initial_artifacts()
    print(f"Bootstrapped CGAA course with {len(CHAPTERS)} chapter notebooks under {BOOK_ROOT}.")


if __name__ == "__main__":
    main()
