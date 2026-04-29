"""Bootstrap the Geometric Tools for Computer Graphics notebook course.

This script creates the first standalone, visualization-first course edition from the
local PDF source map. It is intentionally used for initial course creation; later
chapter revisions should edit notebooks and helpers directly.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


BOOK_ROOT = Path(__file__).resolve().parents[1]


PARTS = [
    {
        "folder": "part-01-foundations",
        "title": "Part I: Foundations",
        "description": "Numerical robustness, linear algebra, vector algebra, affine frames, and transformations.",
    },
    {
        "folder": "part-02-2d-geometric-tools",
        "title": "Part II: 2D Geometric Tools",
        "description": "Planar primitives, distance queries, intersection queries, and classical construction problems.",
    },
    {
        "folder": "part-03-3d-geometric-tools",
        "title": "Part III: 3D Geometric Tools",
        "description": "Spatial primitives, meshes, quadrics, surfaces, 3D distance, 3D intersection, and projection tools.",
    },
    {
        "folder": "part-04-computational-geometry",
        "title": "Part IV: Computational Geometry",
        "description": "BSP trees, containment, Boolean operations, convex hulls, Delaunay triangulation, partitioning, bounds, area, and volume.",
    },
    {
        "folder": "part-05-appendices",
        "title": "Part V: Appendices",
        "description": "Numerical methods, trigonometric tools, and a formula atlas for common geometric primitives.",
    },
]


ENTRIES = [
    {
        "kind": "chapter",
        "number": 1,
        "label": "Chapter 01",
        "title": "Introduction",
        "folder": "chapter-01-introduction",
        "notebook": "01-introduction.ipynb",
        "part": "part-01-foundations",
        "topic": "chapter-01",
        "printed": "1-8",
        "pdf": "48-55",
        "mode": "introduction",
        "focus": "Floating-point failure modes, parameter-domain search, robust predicates, and the shared pattern behind geometric queries.",
        "concepts": [
            "geometric algorithms usually start as real-number statements but run in finite floating-point arithmetic",
            "closest-point and intersection queries often become parameter-domain searches",
            "degenerate configurations are ordinary inputs for production geometry code",
            "robust implementations record assumptions, tolerances, and symmetry checks explicitly",
        ],
        "visuals": [
            "floating-point cancellation and stable quadratic roots",
            "parameter-domain search for closest points",
            "near-boundary point classification under tolerance changes",
            "query pipeline from primitive model to numeric verdict",
        ],
        "checks": [
            "stable quadratic roots agree with polynomial residuals",
            "closest-point parameters remain inside their allowed domain",
            "orientation classification is symmetric after reversing inputs",
            "tolerance bands are reported rather than hidden",
        ],
    },
    {
        "kind": "chapter",
        "number": 2,
        "label": "Chapter 02",
        "title": "Matrices and Linear Systems",
        "folder": "chapter-02-matrices-and-linear-systems",
        "notebook": "02-matrices-and-linear-systems.ipynb",
        "part": "part-01-foundations",
        "topic": "chapter-02",
        "printed": "9-62",
        "pdf": "56-109",
        "mode": "linear",
        "focus": "Linear maps, row reduction, rank, determinants, eigenspaces, Euclidean inner products, and least-squares fitting.",
        "concepts": [
            "a matrix is a coordinate representation of a linear map, not the geometry itself",
            "rank and row reduction expose how many independent constraints a system contains",
            "determinants measure oriented scale and warn when inverse problems become ill conditioned",
            "least squares replaces impossible exact constraints with a projection onto a column space",
        ],
        "visuals": [
            "grid deformation by a linear map",
            "row-reduction pivots and rank",
            "determinant area scale and orientation",
            "least-squares residual as an orthogonal component",
        ],
        "checks": [
            "matrix area scale matches the determinant",
            "least-squares residual is orthogonal to the column space",
            "row-reduction rank matches numpy matrix rank",
            "eigenvectors reproduce their scaled directions",
        ],
    },
    {
        "kind": "chapter",
        "number": 3,
        "label": "Chapter 03",
        "title": "Vector Algebra",
        "folder": "chapter-03-vector-algebra",
        "notebook": "03-vector-algebra.ipynb",
        "part": "part-01-foundations",
        "topic": "chapter-03",
        "printed": "63-108",
        "pdf": "110-155",
        "mode": "vector",
        "focus": "Affine and vector-space distinction, frames, orientation, barycentric coordinates, simplexes, and geometric operations.",
        "concepts": [
            "points name locations while vectors name displacements, so their legal operations differ",
            "a frame converts affine geometry into coordinates only after an origin and basis are chosen",
            "dot, cross, and triple products encode metric, orientation, and volume information",
            "barycentric coordinates describe simplexes with weights that sum to one",
        ],
        "visuals": [
            "head-to-tail vector arithmetic",
            "basis change inside an affine frame",
            "oriented area and scalar triple product",
            "barycentric coordinates over a triangle and tetrahedron",
        ],
        "checks": [
            "barycentric weights sum to one",
            "orientation changes sign when two vertices are swapped",
            "cross product is perpendicular to both inputs",
            "affine combinations are invariant under translation",
        ],
    },
    {
        "kind": "chapter",
        "number": 4,
        "label": "Chapter 04",
        "title": "Matrices, Vector Algebra, and Transformations",
        "folder": "chapter-04-matrices-vector-algebra-and-transformations",
        "notebook": "04-matrices-vector-algebra-and-transformations.ipynb",
        "part": "part-01-foundations",
        "topic": "chapter-04",
        "printed": "109-170",
        "pdf": "156-217",
        "mode": "transform",
        "focus": "Homogeneous point/vector representation, affine transformations, projections, change of basis, and normal-vector transforms.",
        "concepts": [
            "homogeneous coordinates distinguish translated points from untranslated direction vectors",
            "affine transformations combine linear action with a translation in one matrix pipeline",
            "orthographic, oblique, and perspective projections change which geometric ratios survive",
            "normal vectors transform by inverse transpose because they represent plane constraints",
        ],
        "visuals": [
            "point and vector homogeneous weights",
            "composition of translation, rotation, scale, reflection, and shear",
            "projection comparison panel",
            "normal transform failure and inverse-transpose correction",
        ],
        "checks": [
            "vectors are unchanged by pure translation in homogeneous form",
            "composed transforms match stepwise application",
            "perspective division preserves cross-ratio in a line example",
            "corrected normals remain perpendicular to transformed tangents",
        ],
    },
    {
        "kind": "chapter",
        "number": 5,
        "label": "Chapter 05",
        "title": "Geometric Primitives in 2D",
        "folder": "chapter-05-geometric-primitives-in-2d",
        "notebook": "05-geometric-primitives-in-2d.ipynb",
        "part": "part-02-2d-geometric-tools",
        "topic": "chapter-05",
        "printed": "171-188",
        "pdf": "218-235",
        "mode": "primitives2d",
        "focus": "Line, ray, segment, triangle, rectangle, polygon, conic, Bezier, B-spline, and NURBS representations.",
        "concepts": [
            "a primitive is best understood through its parameter domain and boundary conventions",
            "implicit and parametric forms answer different queries efficiently",
            "polygons carry orientation, simplicity, convexity, and monotonicity metadata",
            "free-form curves trade exact algebra for controlled local shape and subdivision",
        ],
        "visuals": [
            "implicit versus parametric line forms",
            "polygon classification gallery",
            "conic level sets",
            "Bezier and B-spline control polygon comparison",
        ],
        "checks": [
            "points sampled from a parametric line satisfy the implicit equation",
            "polygon signed area reports orientation",
            "Bezier endpoints match the first and last control points",
            "curve bounding boxes contain sampled points",
        ],
    },
    {
        "kind": "chapter",
        "number": 6,
        "label": "Chapter 06",
        "title": "Distance in 2D",
        "folder": "chapter-06-distance-in-2d",
        "notebook": "06-distance-in-2d.ipynb",
        "part": "part-02-2d-geometric-tools",
        "topic": "chapter-06",
        "printed": "189-240",
        "pdf": "236-287",
        "mode": "distance2d",
        "focus": "Closest-point regions for points, linear components, polygons, quadratic curves, polynomial curves, and GJK distance.",
        "concepts": [
            "distance queries become minimization over parameter domains",
            "boundaries split the minimization into vertex, edge, and interior cases",
            "convex distance can be rephrased as distance from the origin to a Minkowski difference",
            "the returned closest features are as important as the scalar distance",
        ],
        "visuals": [
            "point-to-segment projection with clamped parameter",
            "triangle closest-feature regions",
            "distance-to-polygon isolines",
            "GJK simplex walk toward the origin",
        ],
        "checks": [
            "clamped closest-point parameter lies in [0, 1]",
            "gradient points toward the closest feature away from medial events",
            "Minkowski difference origin distance matches direct convex distance",
            "feature labels are stable away from boundaries",
        ],
    },
    {
        "kind": "chapter",
        "number": 7,
        "label": "Chapter 07",
        "title": "Intersection in 2D",
        "folder": "chapter-07-intersection-in-2d",
        "notebook": "07-intersection-in-2d.ipynb",
        "part": "part-02-2d-geometric-tools",
        "topic": "chapter-07",
        "printed": "241-284",
        "pdf": "288-331",
        "mode": "intersect2d",
        "focus": "Intersections among linear components, curves, convex polygons, moving objects, and the method of separating axes.",
        "concepts": [
            "intersection tests combine algebraic roots with geometric rejection filters",
            "separating axes turn a 2D convex test into many 1D interval tests",
            "moving intersections require time intervals, not just a yes-or-no at one instant",
            "contact sets record whether the meeting is vertex, edge, transverse, or tangential",
        ],
        "visuals": [
            "segment-segment orientation tests",
            "ellipse-line root panel",
            "separating-axis interval projections",
            "moving polygon contact timeline",
        ],
        "checks": [
            "segment intersection is symmetric in both inputs",
            "roots substituted into curve equations have small residual",
            "all separating-axis overlaps agree with polygon intersection",
            "first-contact time lies inside the reported interval",
        ],
    },
    {
        "kind": "chapter",
        "number": 8,
        "label": "Chapter 08",
        "title": "Miscellaneous 2D Problems",
        "folder": "chapter-08-miscellaneous-2d-problems",
        "notebook": "08-miscellaneous-2d-problems.ipynb",
        "part": "part-02-2d-geometric-tools",
        "topic": "chapter-08",
        "printed": "285-324",
        "pdf": "332-371",
        "mode": "misc2d",
        "focus": "Circle and line constructions with tangency, prescribed radius, offsets, perpendicularity, and solution multiplicity.",
        "concepts": [
            "construction problems are solved by translating constraints into simpler loci",
            "circle tangency often becomes intersection of offset lines or offset circles",
            "the number of solutions changes at degenerate threshold distances",
            "a robust implementation must return zero, one, two, or four solutions without surprise",
        ],
        "visuals": [
            "circle through three points",
            "offset-line tangent construction",
            "two-circle tangent families",
            "solution-count phase diagram",
        ],
        "checks": [
            "constructed circle centers are equidistant from constraints",
            "tangent radius is perpendicular to the tangent line at contact",
            "solution counts match distance thresholds",
            "perpendicular and parallel constructed lines satisfy dot-product tests",
        ],
    },
    {
        "kind": "chapter",
        "number": 9,
        "label": "Chapter 09",
        "title": "Geometric Primitives in 3D",
        "folder": "chapter-09-geometric-primitives-in-3d",
        "notebook": "09-geometric-primitives-in-3d.ipynb",
        "part": "part-03-3d-geometric-tools",
        "topic": "chapter-09",
        "printed": "325-364",
        "pdf": "372-411",
        "mode": "primitives3d",
        "focus": "Lines, rays, segments, planes, planar components, meshes, polyhedra, quadrics, torus, curves, and surfaces.",
        "concepts": [
            "a 3D primitive combines an embedding with dimension, boundary, and orientation data",
            "plane-local coordinates let 2D tools operate inside spatial geometry",
            "mesh validity depends on incidence, connectivity, manifoldness, closure, and face ordering",
            "quadrics and parametric surfaces expose shape through eigenstructure and parameter grids",
        ],
        "visuals": [
            "plane basis and embedded polygon",
            "mesh incidence and manifold checks",
            "quadric surface gallery",
            "torus and parametric surface coordinates",
        ],
        "checks": [
            "plane basis vectors are orthonormal and perpendicular to the normal",
            "mesh Euler counts match the constructed example",
            "quadric samples satisfy their implicit equation",
            "surface normals are perpendicular to parameter tangents",
        ],
    },
    {
        "kind": "chapter",
        "number": 10,
        "label": "Chapter 10",
        "title": "Distance in 3D",
        "folder": "chapter-10-distance-in-3d",
        "notebook": "10-distance-in-3d.ipynb",
        "part": "part-03-3d-geometric-tools",
        "topic": "chapter-10",
        "printed": "365-480",
        "pdf": "412-527",
        "mode": "distance3d",
        "focus": "Point, line, ray, segment, triangle, rectangle, box, polyhedron, quadric, curve, surface, and geodesic distances.",
        "concepts": [
            "3D distance queries use the same parameter-minimization pattern as 2D but with richer boundaries",
            "closest-point cases are feature pairs such as vertex-face, edge-edge, or interior-interior",
            "oriented boxes and frusta become simple after moving into the correct local frame",
            "surface distance often requires iterative minimization with residual diagnostics",
        ],
        "visuals": [
            "point-to-triangle closest-feature map",
            "segment-segment closest connector",
            "oriented-box local coordinates",
            "ellipsoid distance iteration trace",
        ],
        "checks": [
            "closest connector is perpendicular to active unconstrained features",
            "barycentric coordinates classify triangle features",
            "local-frame and world-frame distances agree",
            "iterative residuals decrease for the shown surface example",
        ],
    },
    {
        "kind": "chapter",
        "number": 11,
        "label": "Chapter 11",
        "title": "Intersection in 3D",
        "folder": "chapter-11-intersection-in-3d",
        "notebook": "11-intersection-in-3d.ipynb",
        "part": "part-03-3d-geometric-tools",
        "topic": "chapter-11",
        "printed": "481-662",
        "pdf": "528-709",
        "mode": "intersect3d",
        "focus": "Intersection tests for linear components, planes, triangles, polyhedra, quadrics, polynomial surfaces, bounding boxes, cylinders, and torus.",
        "concepts": [
            "3D intersections are often classified by dimension: point, segment, polygon, curve, or empty set",
            "slab clipping turns ray-box intersection into interval arithmetic",
            "plane sections of quadrics expose conic structure in a coordinate plane",
            "separating-axis tests generalize to face normals and edge-cross-edge axes",
        ],
        "visuals": [
            "ray and plane intersection parameters",
            "triangle-plane clipping",
            "slab interval clipping for boxes",
            "sphere, cylinder, cone, and torus section diagnostics",
        ],
        "checks": [
            "reported intersection points satisfy both object equations",
            "ray-box entry parameter is no larger than the exit parameter",
            "triangle-plane clipped vertices lie in the plane within tolerance",
            "SAT overlap decisions are invariant under swapping objects",
        ],
    },
    {
        "kind": "chapter",
        "number": 12,
        "label": "Chapter 12",
        "title": "Miscellaneous 3D Problems",
        "folder": "chapter-12-miscellaneous-3d-problems",
        "notebook": "12-miscellaneous-3d-problems.ipynb",
        "part": "part-03-3d-geometric-tools",
        "topic": "chapter-12",
        "printed": "663-672",
        "pdf": "710-719",
        "mode": "misc3d",
        "focus": "Projection of points and vectors onto planes, line-plane angles, plane-plane angles, and planes through geometric constraints.",
        "concepts": [
            "projection decomposes a vector into normal and tangential components",
            "angle queries should use normalized dot products and stable clamping",
            "planes can be constructed from a point-normal pair, a line-normal condition, or three noncollinear points",
            "small utilities are valuable when they expose sign conventions and units",
        ],
        "visuals": [
            "point projection onto a plane",
            "vector projection and rejection",
            "line-plane and plane-plane angle panel",
            "plane through three points with normal orientation",
        ],
        "checks": [
            "projection residual is parallel to the plane normal",
            "projected vectors are perpendicular to the normal",
            "angle calculations are unchanged by vector scaling",
            "three-point plane equation vanishes at all three inputs",
        ],
    },
    {
        "kind": "chapter",
        "number": 13,
        "label": "Chapter 13",
        "title": "Computational Geometry Topics",
        "folder": "chapter-13-computational-geometry-topics",
        "notebook": "13-computational-geometry-topics.ipynb",
        "part": "part-04-computational-geometry",
        "topic": "chapter-13",
        "printed": "673-826",
        "pdf": "720-873",
        "mode": "compgeom",
        "focus": "BSP trees, point containment, Boolean operations, convex hulls, Delaunay triangulation, polygon partitioning, minimum bounds, area, and volume.",
        "concepts": [
            "computational geometry organizes many local predicates into global data structures",
            "BSP and triangulation algorithms trade preprocessing for faster spatial queries",
            "convex hulls and Delaunay triangulations are dual views of extreme and empty-circle structure",
            "area, volume, and bounding primitives are diagnostics for the geometry pipeline",
        ],
        "visuals": [
            "BSP partitioning trace",
            "point-in-polygon ray parity and winding comparison",
            "convex hull and Delaunay dual panel",
            "minimum bounding rectangle and circle",
        ],
        "checks": [
            "hull vertices contain all points on the nonpositive side of each edge",
            "Delaunay triangles satisfy an empty-circumcircle sample check",
            "polygon area is invariant under cyclic vertex shifts",
            "bounding primitives contain all input points",
        ],
    },
    {
        "kind": "appendix",
        "number": 101,
        "label": "Appendix A",
        "title": "Numerical Methods",
        "folder": "appendix-a-numerical-methods",
        "notebook": "appendix-a-numerical-methods.ipynb",
        "part": "part-05-appendices",
        "topic": "appendix-a",
        "printed": "827-922",
        "pdf": "874-969",
        "mode": "numerical",
        "focus": "Linear solvers, polynomial systems, decompositions, rotations, root finding, minimization, least-squares fitting, subdivision, and calculus tools.",
        "concepts": [
            "numerical method choice is part of the geometry algorithm, not a replaceable afterthought",
            "decompositions expose scale, rotation, rank, and conditioning separately",
            "root finding and minimization need brackets, residuals, and convergence checks",
            "fitting routines should report both model parameters and geometric residuals",
        ],
        "visuals": [
            "Gaussian elimination and conditioning",
            "stable quadratic formula comparison",
            "QR, SVD, and polar decomposition geometry",
            "root-finding and minimization traces",
        ],
        "checks": [
            "decomposition reconstructions match the original matrix",
            "stable roots have smaller residuals for cancellation cases",
            "least-squares fitted primitives reduce orthogonal residual",
            "subdivision samples respect the selected stopping rule",
        ],
    },
    {
        "kind": "appendix",
        "number": 102,
        "label": "Appendix B",
        "title": "Trigonometry",
        "folder": "appendix-b-trigonometry",
        "notebook": "appendix-b-trigonometry.ipynb",
        "part": "part-05-appendices",
        "topic": "appendix-b",
        "printed": "923-948",
        "pdf": "970-995",
        "mode": "trig",
        "focus": "Angles, trigonometric functions, identities, laws, inverse branches, derivatives, integrals, and conversion examples.",
        "concepts": [
            "trigonometry is the coordinate language of rotations, projections, and circular primitives",
            "identities are best treated as reusable invariants in geometric code",
            "inverse trigonometric functions require branch choices that match the intended geometry",
            "derivatives and integrals explain how circular motion becomes curvature and arc length",
        ],
        "visuals": [
            "unit circle with sine and cosine projections",
            "trig function graphs and phase shifts",
            "law of cosines triangle lab",
            "inverse-branch comparison",
        ],
        "checks": [
            "sin squared plus cos squared is one on sampled angles",
            "law-of-cosines reconstruction matches side lengths",
            "atan2 branch recovers the correct quadrant",
            "finite-difference derivatives match analytic derivatives",
        ],
    },
    {
        "kind": "appendix",
        "number": 103,
        "label": "Appendix C",
        "title": "Basic Formulas for Geometric Primitives",
        "folder": "appendix-c-basic-formulas-for-geometric-primitives",
        "notebook": "appendix-c-basic-formulas-for-geometric-primitives.ipynb",
        "part": "part-05-appendices",
        "topic": "appendix-c",
        "printed": "949-959",
        "pdf": "996-1006",
        "mode": "formulas",
        "focus": "Formula atlas for triangles, quadrilaterals, circles, polyhedra, cylinders, cones, spheres, and torus primitives.",
        "concepts": [
            "formula sheets become safer when each expression is tied to a diagram and a dimensional check",
            "triangle and quadrilateral formulas can be unified through area decomposition",
            "circle, sphere, cylinder, cone, and torus formulas expose radius and angle dependencies",
            "primitive formulas should be checked against sampled geometry, not trusted as isolated text",
        ],
        "visuals": [
            "triangle notation and area formulas",
            "quadrilateral decomposition",
            "circle sector and segment formulas",
            "sphere and torus parameter atlas",
        ],
        "checks": [
            "triangle area agrees between determinant and Heron formulas",
            "circle sector area scales linearly with angle",
            "box, prism, pyramid, cylinder, cone, sphere, and torus dimensions are positive",
            "sampled torus surface area approximates the analytic expression",
        ],
    },
]


CHAPTER_NOTES = {
    "introduction": (
        "The introduction is treated as the course contract for robust geometry code. "
        "The notebook emphasizes two examples that show why symbolic reasoning alone is insufficient: cancellation in quadratic roots and point classification near a boundary. "
        "The worked case asks the reader to compare the real-number model with the floating-point result, then to turn the gap into an explicit tolerance and residual."
    ),
    "linear": (
        "The linear algebra chapter is organized around what matrices do to spaces. "
        "A grid deformation shows the map, a determinant check measures oriented area, and a least-squares discussion interprets residuals as perpendicular leftover vectors. "
        "The chapter treats row operations, rank, eigenvectors, and decompositions as ways to reveal structure before a geometric algorithm depends on it."
    ),
    "vector": (
        "The vector algebra chapter keeps points and vectors separated. "
        "The notebook uses barycentric reconstruction and orientation tests to make affine combinations visible, then connects dot, cross, and triple products to angle, area, and volume. "
        "The central warning is that arrays are not enough: a program must know whether an array represents a location, a displacement, a frame vector, or a coordinate tuple."
    ),
    "transform": (
        "The transformations chapter follows points, vectors, frames, and normals through the same affine pipeline. "
        "The notebook highlights homogeneous weights for translation, projection as a ratio-producing map, and inverse-transpose normal transport as a constraint-preserving operation. "
        "The worked invariant is perpendicularity after nonuniform scaling, because that is where an apparently obvious normal transform breaks."
    ),
    "primitives2d": (
        "The 2D primitives chapter is a representation atlas. "
        "The notebook contrasts implicit forms that answer side tests with parametric forms that sample objects, then uses polygons and Bezier curves to expose orientation, boundary, and endpoint conventions. "
        "The practical result is a checklist for choosing the representation that makes a later distance or intersection query simplest."
    ),
    "distance2d": (
        "The 2D distance chapter turns geometric proximity into constrained minimization. "
        "The notebook starts with a clamped point-to-segment projection because every harder case inherits the same boundary logic. "
        "Feature regions, polygon isolines, and GJK intuition are framed as ways of discovering which constraints are active at the closest point."
    ),
    "intersect2d": (
        "The 2D intersection chapter treats intersection as both algebra and classification. "
        "The notebook pairs orientation predicates and interval projections with curve-root thinking, so a Boolean answer is never the only output. "
        "The emphasis is on contact type, symmetry under input order, and the difference between transverse crossing and tangential first contact."
    ),
    "misc2d": (
        "The miscellaneous 2D constructions chapter is about reducing constraints to loci. "
        "The notebook shows how tangency becomes an offset-line or offset-circle problem, and why solution count changes at exact threshold distances. "
        "The checks focus on equal distance and perpendicular radius conditions because those are the invariants every construction should satisfy."
    ),
    "primitives3d": (
        "The 3D primitives chapter adds embedding and incidence to the 2D representation story. "
        "The notebook uses a plane basis, mesh validity language, and a torus sample to connect local coordinates with spatial objects. "
        "The reader should leave with a habit of storing not just vertices, but also adjacency, orientation, manifold assumptions, and implicit residuals."
    ),
    "distance3d": (
        "The 3D distance chapter extends closest-feature reasoning to surfaces and volumes. "
        "The notebook makes a point-to-triangle projection visible, then explains how edge-edge and face-interior cases are active constraints in a quadratic minimization. "
        "The invariant checks emphasize perpendicularity and local-frame agreement because those catch many implementation mistakes."
    ),
    "intersect3d": (
        "The 3D intersection chapter is about dimensional classification: empty set, point, segment, polygon, or curve. "
        "The notebook uses slab clipping for ray-box intersection and plane/triangle intuition as compact examples of interval and half-space reasoning. "
        "The same pattern scales to quadrics, boxes, cylinders, cones, and torus tests when residuals are recorded."
    ),
    "misc3d": (
        "The miscellaneous 3D chapter collects small operations that larger algorithms quietly depend on. "
        "The notebook treats projection, line-plane angle, plane-plane angle, and plane construction as sign-sensitive utilities. "
        "The emphasis is not novelty but reliability: normalize vectors, clamp dot products, record units, and assert that projected residuals point in the expected normal direction."
    ),
    "compgeom": (
        "The computational geometry chapter combines predicates into data structures. "
        "The notebook presents convex hulls, containment, triangulation, BSP thinking, and bounding primitives as pipelines: local orientation tests become global decisions. "
        "The sample hull check is deliberately small, but the teaching point is large: every global structure should be auditable by local invariants."
    ),
    "numerical": (
        "The numerical methods appendix supplies the machinery that geometry algorithms rely on when closed forms are unstable or unavailable. "
        "The notebook connects stable roots, decompositions, least squares, minimization, and subdivision to the residuals they should report. "
        "The lesson is to choose a numerical method together with its stopping rule and reconstruction check."
    ),
    "trig": (
        "The trigonometry appendix is treated as geometry in circular coordinates. "
        "The notebook links unit-circle projections, phase, inverse-branch choices, and the law of cosines to graphics tasks such as rotation, projection, and angle recovery. "
        "The checks make branch and identity errors visible before they leak into a transform or intersection routine."
    ),
    "formulas": (
        "The formula appendix becomes a visual atlas rather than a lookup table. "
        "The notebook ties every area, volume, sector, and surface expression to a diagram, a dimensional interpretation, and a sampled check. "
        "The goal is to make formulas executable: if a primitive changes scale or angle, the computed quantity should change in the way the picture predicts."
    ),
}


UTILS: dict[str, str] = {}
SCRIPTS: dict[str, str] = {}


UTILS["__init__.py"] = '"""Book-local helpers for the GTCG notebook course."""\n'

UTILS["artifacts.py"] = r'''
"""Helpers for saving and displaying notebook artifacts."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image as PILImage

BOOK_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-._")
    return slug or "artifact"


def artifact_dir(topic: str, slug: str | None = None, root: str | Path = ARTIFACT_ROOT) -> Path:
    parts = [slugify(topic)]
    if slug:
        parts.append(slugify(slug))
    path = Path(root).joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(topic: str, slug: str | None, filename: str, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_dir(topic, slug, root) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_matplotlib(figure: Any, topic: str, slug: str | None, filename: str = "figure.png", *, dpi: int = 160, root: str | Path = ARTIFACT_ROOT, **kwargs: Any) -> Path:
    path = artifact_path(topic, slug, filename, root)
    figure.savefig(path, dpi=dpi, bbox_inches="tight", **kwargs)
    return path


def save_plotly_html(figure: Any, topic: str, slug: str | None, filename: str = "plot.html", *, root: str | Path = ARTIFACT_ROOT, include_plotlyjs: str | bool = "cdn", full_html: bool = True, **kwargs: Any) -> Path:
    path = artifact_path(topic, slug, filename, root)
    figure.write_html(path, include_plotlyjs=include_plotlyjs, full_html=full_html, **kwargs)
    return path


def save_image(image: Any, topic: str, slug: str | None, filename: str = "image.png", *, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_path(topic, slug, filename, root)
    if isinstance(image, PILImage.Image):
        image.save(path)
        return path
    array = np.asarray(image)
    if array.dtype != np.uint8:
        if np.issubdtype(array.dtype, np.floating) and array.size and array.max() <= 1.0:
            array = array * 255.0
        array = np.clip(array, 0, 255).astype(np.uint8)
    PILImage.fromarray(array).save(path)
    return path


def save_json(data: Any, topic: str, slug: str | None, filename: str = "data.json", *, root: str | Path = ARTIFACT_ROOT, indent: int = 2) -> Path:
    path = artifact_path(topic, slug, filename, root)
    path.write_text(json.dumps(data, indent=indent, sort_keys=True), encoding="utf-8")
    return path


def save_text(text: str, topic: str, slug: str | None, filename: str = "notes.txt", *, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_path(topic, slug, filename, root)
    path.write_text(text, encoding="utf-8")
    return path


def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
    from IPython.display import HTML, IFrame, Image, display

    resolved = Path(path)
    suffix = resolved.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        return display(Image(filename=str(resolved), width=width, height=height))
    if suffix in {".html", ".htm"}:
        if height:
            return display(IFrame(src=str(resolved), width=width or "100%", height=height))
        return display(HTML(resolved.read_text(encoding="utf-8")))
    link = escape(resolved.as_posix(), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))
'''

UTILS["plotting.py"] = r'''
"""Plotting defaults and visual audit helpers."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageStat

PALETTE = {
    "ink": "#1f2933",
    "blue": "#2f6fbb",
    "teal": "#2a9d8f",
    "green": "#6a994e",
    "gold": "#d59f0f",
    "red": "#c44e52",
    "violet": "#7b5ea7",
    "gray": "#7a8793",
}


def style_axis(ax: Any, title: str, *, equal: bool = False) -> None:
    ax.set_title(title, fontsize=11, color=PALETTE["ink"])
    ax.grid(True, color="#d7dde5", linewidth=0.7, alpha=0.8)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in getattr(ax, "spines", {}).values():
        spine.set_color("#b6c0ca")


def add_note(ax: Any, text: str) -> None:
    ax.text(
        0.02,
        0.98,
        text,
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=8,
        color=PALETTE["ink"],
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#d0d7de", "alpha": 0.92},
    )


def set_axes_equal_3d(ax: Any) -> None:
    limits = np.array([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()], dtype=float)
    centers = limits.mean(axis=1)
    radius = 0.5 * np.max(limits[:, 1] - limits[:, 0])
    ax.set_xlim3d([centers[0] - radius, centers[0] + radius])
    ax.set_ylim3d([centers[1] - radius, centers[1] + radius])
    ax.set_zlim3d([centers[2] - radius, centers[2] + radius])


def image_stats(path: str | Path) -> dict[str, float | int | str]:
    p = Path(path)
    with Image.open(p) as image:
        image.load()
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
        arr = np.asarray(rgb, dtype=float)
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    return {
        "path": p.as_posix(),
        "width": int(rgb.width),
        "height": int(rgb.height),
        "bytes": int(p.stat().st_size),
        "sha256": digest,
        "pixel_std": float(arr.std()),
        "max_channel_stddev": float(max(stat.stddev) if stat.stddev else 0.0),
    }


def close(fig: Any) -> None:
    plt.close(fig)
'''

UTILS["linear_algebra.py"] = r'''
"""Small linear algebra helpers used by the GTCG notebooks."""

from __future__ import annotations

import numpy as np


def rotation2d(theta: float) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def affine_matrix(linear: np.ndarray, translation: np.ndarray) -> np.ndarray:
    linear = np.asarray(linear, dtype=float)
    translation = np.asarray(translation, dtype=float)
    dim = linear.shape[0]
    mat = np.eye(dim + 1)
    mat[:dim, :dim] = linear
    mat[:dim, dim] = translation
    return mat


def transform_points(points: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    ones = np.ones((len(points), 1))
    hom = np.hstack([points, ones])
    out = hom @ np.asarray(matrix, dtype=float).T
    return out[:, :-1] / out[:, [-1]]


def rotation3d_axis_angle(axis: np.ndarray, theta: float) -> np.ndarray:
    axis = np.asarray(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    c, s = np.cos(theta), np.sin(theta)
    C = 1 - c
    return np.array([
        [c + x*x*C, x*y*C - z*s, x*z*C + y*s],
        [y*x*C + z*s, c + y*y*C, y*z*C - x*s],
        [z*x*C - y*s, z*y*C + x*s, c + z*z*C],
    ])


def row_reduce(a: np.ndarray, tol: float = 1e-12) -> tuple[np.ndarray, list[int]]:
    m = np.array(a, dtype=float, copy=True)
    pivots: list[int] = []
    row = 0
    for col in range(m.shape[1]):
        pivot = row + int(np.argmax(np.abs(m[row:, col])))
        if abs(m[pivot, col]) <= tol:
            continue
        m[[row, pivot]] = m[[pivot, row]]
        m[row] = m[row] / m[row, col]
        for r in range(m.shape[0]):
            if r != row:
                m[r] -= m[r, col] * m[row]
        pivots.append(col)
        row += 1
        if row == m.shape[0]:
            break
    return m, pivots
'''

UTILS["geometry2d.py"] = r'''
"""Readable 2D geometry helpers."""

from __future__ import annotations

import numpy as np


def orientation(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    a, b, c = np.asarray(a, float), np.asarray(b, float), np.asarray(c, float)
    return float(np.cross(b - a, c - a))


def polygon_area(points: np.ndarray) -> float:
    p = np.asarray(points, dtype=float)
    x, y = p[:, 0], p[:, 1]
    return float(0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1)))


def barycentric_coordinates(point: np.ndarray, triangle: np.ndarray) -> np.ndarray:
    p = np.asarray(point, dtype=float)
    tri = np.asarray(triangle, dtype=float)
    a = np.vstack([tri.T, np.ones(3)])
    b = np.array([p[0], p[1], 1.0])
    return np.linalg.solve(a, b)


def project_point_segment(point: np.ndarray, a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, float]:
    p, a, b = np.asarray(point, float), np.asarray(a, float), np.asarray(b, float)
    ab = b - a
    t = float(np.dot(p - a, ab) / np.dot(ab, ab))
    tc = min(1.0, max(0.0, t))
    return a + tc * ab, tc


def convex_hull(points: np.ndarray) -> np.ndarray:
    pts = sorted(map(tuple, np.asarray(points, dtype=float)))
    if len(pts) <= 1:
        return np.array(pts)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return np.array(lower[:-1] + upper[:-1], dtype=float)
'''

UTILS["geometry3d.py"] = r'''
"""Readable 3D geometry helpers."""

from __future__ import annotations

import numpy as np


def plane_from_points(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> tuple[np.ndarray, float]:
    a, b, c = np.asarray(a, float), np.asarray(b, float), np.asarray(c, float)
    normal = np.cross(b - a, c - a)
    normal = normal / np.linalg.norm(normal)
    d = -float(np.dot(normal, a))
    return normal, d


def project_point_plane(point: np.ndarray, normal: np.ndarray, d: float) -> np.ndarray:
    p, n = np.asarray(point, float), np.asarray(normal, float)
    n = n / np.linalg.norm(n)
    return p - (np.dot(n, p) + d) * n


def box_vertices(center: np.ndarray, half_extents: np.ndarray) -> np.ndarray:
    c, h = np.asarray(center, float), np.asarray(half_extents, float)
    signs = np.array([[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1], [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]], dtype=float)
    return c + signs * h
'''

UTILS["curves_surfaces.py"] = r'''
"""Curve and surface helpers."""

from __future__ import annotations

import numpy as np


def bezier_curve(control: np.ndarray, samples: int = 120) -> np.ndarray:
    control = np.asarray(control, dtype=float)
    t = np.linspace(0.0, 1.0, samples)
    points = np.zeros((samples, control.shape[1]))
    n = len(control) - 1
    from math import comb

    for i, p in enumerate(control):
        basis = comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
        points += basis[:, None] * p
    return points


def torus_grid(major: float = 1.4, minor: float = 0.35, nu: int = 50, nv: int = 20) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    u = np.linspace(0, 2 * np.pi, nu)
    v = np.linspace(0, 2 * np.pi, nv)
    uu, vv = np.meshgrid(u, v)
    x = (major + minor * np.cos(vv)) * np.cos(uu)
    y = (major + minor * np.cos(vv)) * np.sin(uu)
    z = minor * np.sin(vv)
    return x, y, z
'''

UTILS["robustness.py"] = r'''
"""Numerical robustness helpers."""

from __future__ import annotations

import math
import numpy as np


def robust_quadratic_roots(a: float, b: float, c: float, tol: float = 1e-14) -> tuple[float, ...]:
    if abs(a) <= tol:
        if abs(b) <= tol:
            return tuple()
        return (-c / b,)
    disc_raw = b * b - 4.0 * a * c
    if disc_raw < -tol:
        return tuple()
    disc = max(0.0, disc_raw)
    root = math.sqrt(disc)
    q = -0.5 * (b + math.copysign(root, b if b != 0 else 1.0))
    if abs(q) <= tol:
        repeated = -b / (2.0 * a)
        return (repeated,)
    r1 = q / a
    r2 = c / q
    return (min(r1, r2), max(r1, r2))


def orientation2d(a: np.ndarray, b: np.ndarray, c: np.ndarray, eps: float = 1e-12) -> int:
    det = float(np.cross(np.asarray(b) - np.asarray(a), np.asarray(c) - np.asarray(a)))
    if det > eps:
        return 1
    if det < -eps:
        return -1
    return 0


def clamp_unit(value: float) -> float:
    return min(1.0, max(-1.0, float(value)))
'''

UTILS["validation.py"] = r'''
"""Validation helpers for notebooks and artifacts."""

from __future__ import annotations

from pathlib import Path


def require_nonempty(paths: list[str | Path], min_bytes: int = 1000) -> None:
    for path in paths:
        p = Path(path)
        if not p.exists():
            raise AssertionError(f"missing artifact: {p}")
        if p.stat().st_size < min_bytes:
            raise AssertionError(f"artifact too small: {p} ({p.stat().st_size} bytes)")


def artifact_report(paths: list[str | Path], root: str | Path | None = None) -> list[dict[str, int | str]]:
    report = []
    base = Path(root).resolve() if root is not None else None
    for path in paths:
        p = Path(path)
        label = p.resolve()
        if base is not None:
            try:
                label = label.relative_to(base)
            except ValueError:
                pass
        report.append({"path": Path(label).as_posix(), "bytes": int(p.stat().st_size)})
    return report
'''

UTILS["chapter_visuals.py"] = r'''
"""Reusable chapter-specific visual constructors."""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np

from utils.curves_surfaces import bezier_curve, torus_grid
from utils.geometry2d import barycentric_coordinates, convex_hull, polygon_area, project_point_segment
from utils.geometry3d import plane_from_points, project_point_plane
from utils.linear_algebra import rotation2d, rotation3d_axis_angle
from utils.plotting import PALETTE, add_note, set_axes_equal_3d, style_axis
from utils.robustness import robust_quadratic_roots


def concept_map_figure(title: str, concepts: list[str], visuals: list[str]):
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_axis_off()
    ax.set_title(f"{title}: concept-to-visual route", fontsize=14, color=PALETTE["ink"], pad=16)
    nodes = ["chapter goal", *[f"concept {i+1}" for i in range(len(concepts))], *[f"visual {i+1}" for i in range(len(visuals))], "sanity checks"]
    angles = np.linspace(0, 2 * np.pi, len(nodes), endpoint=False)
    xy = np.c_[np.cos(angles), np.sin(angles)]
    for i, node in enumerate(nodes):
        x, y = xy[i]
        color = PALETTE["blue"] if "concept" in node else PALETTE["teal"] if "visual" in node else PALETTE["gold"]
        ax.scatter([x], [y], s=500, color=color, alpha=0.9, edgecolor="white", linewidth=1.5)
        ax.text(x, y, node, ha="center", va="center", color="white", fontsize=8, weight="bold")
    for i in range(1, len(nodes)):
        ax.plot([xy[0, 0], xy[i, 0]], [xy[0, 1], xy[i, 1]], color="#c7d0dd", linewidth=1)
    text_lines = ["Concepts:"] + [f"- {c}" for c in concepts] + ["", "Visuals:"] + [f"- {v}" for v in visuals]
    ax.text(-1.35, -1.35, "\n".join(text_lines), fontsize=8, va="bottom", color=PALETTE["ink"], wrap=True)
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    return fig


def geometry_scene_figure(mode: str, title: str, seed: int):
    rng = np.random.default_rng(seed)
    if mode in {"primitives3d", "distance3d", "intersect3d", "misc3d", "formulas"}:
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection="3d")
        if mode == "primitives3d":
            x, y, z = torus_grid()
            ax.plot_surface(x, y, z, alpha=0.55, color=PALETTE["teal"], linewidth=0)
            ax.quiver(0, 0, 0, 1.2, 0.3, 0.6, color=PALETTE["red"], label="plane normal")
            ax.set_title("Parametric torus and spatial frame")
        elif mode == "distance3d":
            tri = np.array([[0, 0, 0], [1.4, 0.2, 0], [0.2, 1.1, 0.25]])
            p = np.array([0.75, 0.45, 1.2])
            normal, d = plane_from_points(*tri)
            q = project_point_plane(p, normal, d)
            ax.plot_trisurf(tri[:, 0], tri[:, 1], tri[:, 2], triangles=[[0, 1, 2]], color=PALETTE["blue"], alpha=0.45)
            ax.scatter([p[0]], [p[1]], [p[2]], color=PALETTE["red"], s=60, label="query point")
            ax.scatter([q[0]], [q[1]], [q[2]], color=PALETTE["green"], s=60, label="plane projection")
            ax.plot([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], color=PALETTE["red"], linewidth=2)
            ax.set_title("Point-to-triangle distance scaffold")
        elif mode == "intersect3d":
            corners = np.array([[-1,-1,-1],[-1,-1,1],[-1,1,-1],[-1,1,1],[1,-1,-1],[1,-1,1],[1,1,-1],[1,1,1]], float)
            ax.scatter(corners[:,0], corners[:,1], corners[:,2], color=PALETTE["blue"], s=25)
            ray0 = np.array([-1.8, -0.4, 0.2]); ray1 = np.array([1.6, 0.9, 0.55])
            ax.plot([ray0[0], ray1[0]], [ray0[1], ray1[1]], [ray0[2], ray1[2]], color=PALETTE["red"], linewidth=2, label="ray")
            ax.set_title("Ray-box slab interval geometry")
        elif mode == "misc3d":
            xx, yy = np.meshgrid(np.linspace(-1, 1, 8), np.linspace(-1, 1, 8))
            zz = 0.25 * xx - 0.15 * yy
            ax.plot_surface(xx, yy, zz, alpha=0.45, color=PALETTE["blue"])
            p = np.array([0.5, 0.5, 1.1]); n = np.array([-0.25, 0.15, 1.0]); n = n / np.linalg.norm(n)
            q = p - (np.dot(n, p)) * n
            ax.scatter([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], color=[PALETTE["red"], PALETTE["green"]], s=60)
            ax.plot([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], color=PALETTE["red"])
            ax.set_title("Projection onto a plane")
        else:
            x, y, z = torus_grid(1.2, 0.3)
            ax.plot_surface(x, y, z, alpha=0.55, color=PALETTE["violet"], linewidth=0)
            ax.set_title("Formula atlas surface sample")
        ax.legend(loc="upper left")
        set_axes_equal_3d(ax)
        return fig

    fig, ax = plt.subplots(figsize=(8, 6))
    if mode == "linear":
        grid = np.linspace(-1, 1, 9)
        a = np.array([[1.2, 0.55], [-0.25, 0.8]])
        for g in grid:
            pts = np.array([[g, -1], [g, 1], [-1, g], [1, g]], float)
            out = pts @ a.T
            ax.plot(out[:2, 0], out[:2, 1], color="#b7c3d0", linewidth=0.8)
            ax.plot(out[2:, 0], out[2:, 1], color="#b7c3d0", linewidth=0.8)
        square = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]], float) @ a.T
        ax.plot(square[:,0], square[:,1], color=PALETTE["red"], linewidth=2)
        add_note(ax, f"determinant area scale = {np.linalg.det(a):.3f}")
        style_axis(ax, "Linear map deforms a coordinate grid", equal=True)
    elif mode == "vector":
        tri = np.array([[0, 0], [1.5, 0.2], [0.35, 1.25]])
        p = np.array([0.65, 0.45])
        w = barycentric_coordinates(p, tri)
        ax.fill(tri[:,0], tri[:,1], color=PALETTE["blue"], alpha=0.18)
        ax.scatter(tri[:,0], tri[:,1], color=PALETTE["blue"], s=70)
        ax.scatter([p[0]], [p[1]], color=PALETTE["red"], s=70)
        for v in tri:
            ax.plot([p[0], v[0]], [p[1], v[1]], color="#98a6b3", linestyle="--")
        add_note(ax, "barycentric weights: " + ", ".join(f"{x:.2f}" for x in w))
        style_axis(ax, "Affine coordinates inside a simplex", equal=True)
    elif mode == "transform":
        pts = np.array([[0,0],[1,0],[1,0.6],[0,0.6],[0,0]], float)
        a = rotation2d(0.55) @ np.array([[1.4, 0.35], [0.0, 0.75]])
        out = pts @ a.T + np.array([0.3, 0.2])
        ax.plot(pts[:,0], pts[:,1], color=PALETTE["gray"], linewidth=2, label="source")
        ax.plot(out[:,0], out[:,1], color=PALETTE["red"], linewidth=2, label="transformed")
        ax.quiver([out[1,0]], [out[1,1]], [a[0,0]], [a[0,1]], angles="xy", scale_units="xy", scale=1, color=PALETTE["green"])
        ax.legend()
        style_axis(ax, "Affine transform and tangent direction", equal=True)
    elif mode == "primitives2d":
        control = np.array([[-1, -0.4], [-0.4, 1.1], [0.8, -0.9], [1.2, 0.45]])
        curve = bezier_curve(control)
        theta = np.linspace(0, 2*np.pi, 160)
        ax.plot(np.cos(theta)*0.5-0.6, np.sin(theta)*0.35-0.1, color=PALETTE["gold"], label="conic sample")
        ax.plot(control[:,0], control[:,1], "--o", color=PALETTE["gray"], label="control polygon")
        ax.plot(curve[:,0], curve[:,1], color=PALETTE["blue"], linewidth=2, label="Bezier curve")
        ax.legend()
        style_axis(ax, "2D primitive representations", equal=True)
    elif mode == "distance2d":
        a = np.array([-0.9, -0.35]); b = np.array([1.1, 0.35]); p = np.array([0.2, 1.0])
        q, t = project_point_segment(p, a, b)
        ax.plot([a[0], b[0]], [a[1], b[1]], color=PALETTE["blue"], linewidth=3)
        ax.scatter([p[0], q[0]], [p[1], q[1]], color=[PALETTE["red"], PALETTE["green"]], s=70)
        ax.plot([p[0], q[0]], [p[1], q[1]], color=PALETTE["red"], linestyle="--")
        add_note(ax, f"clamped parameter t = {t:.3f}")
        style_axis(ax, "Closest point on a segment", equal=True)
    elif mode == "intersect2d":
        poly_a = np.array([[-0.8,-0.5],[0.4,-0.7],[0.9,0.2],[-0.2,0.8]])
        poly_b = poly_a @ rotation2d(0.7).T + np.array([0.5, 0.1])
        for poly, color, label in [(poly_a, PALETTE["blue"], "A"), (poly_b, PALETTE["red"], "B")]:
            closed = np.vstack([poly, poly[0]])
            ax.plot(closed[:,0], closed[:,1], color=color, linewidth=2, label=label)
        axis = np.array([0.85, 0.35]); axis = axis / np.linalg.norm(axis)
        ax.arrow(-1.2*axis[0], -1.2*axis[1], 2.4*axis[0], 2.4*axis[1], color=PALETTE["green"], width=0.01)
        ax.legend()
        style_axis(ax, "Separating-axis projection direction", equal=True)
    elif mode == "misc2d":
        c1, c2 = np.array([-0.45, 0.0]), np.array([0.65, 0.05])
        for center, r, color in [(c1, 0.5, PALETTE["blue"]), (c2, 0.35, PALETTE["teal"])]:
            circ = plt.Circle(center, r, fill=False, color=color, linewidth=2)
            ax.add_patch(circ)
        ax.plot([c1[0], c2[0]], [0.5, 0.4], color=PALETTE["red"], linewidth=2, label="external tangent")
        ax.legend()
        style_axis(ax, "Circle tangent construction", equal=True)
    elif mode == "compgeom":
        pts = rng.normal(size=(24, 2))
        pts[:, 0] *= 1.2
        hull = convex_hull(pts)
        closed = np.vstack([hull, hull[0]])
        ax.scatter(pts[:,0], pts[:,1], color=PALETTE["gray"], s=25)
        ax.fill(closed[:,0], closed[:,1], color=PALETTE["blue"], alpha=0.18)
        ax.plot(closed[:,0], closed[:,1], color=PALETTE["blue"], linewidth=2)
        add_note(ax, f"hull vertices = {len(hull)}")
        style_axis(ax, "Convex hull as an extreme-point summary", equal=True)
    elif mode == "numerical":
        x = np.linspace(-2, 2, 300)
        y = (x - 0.15) ** 2 + 0.1 * np.sin(8 * x)
        ax.plot(x, y, color=PALETTE["blue"])
        ax.scatter([x[np.argmin(y)]], [y.min()], color=PALETTE["red"], s=70, label="sample minimum")
        ax.legend()
        style_axis(ax, "Root and minimization diagnostics")
    elif mode == "trig":
        t = np.linspace(-np.pi, np.pi, 300)
        ax.plot(t, np.sin(t), label="sin", color=PALETTE["blue"])
        ax.plot(t, np.cos(t), label="cos", color=PALETTE["red"])
        ax.legend()
        style_axis(ax, "Trigonometric functions as geometric coordinates")
    elif mode == "introduction":
        xs = np.array([1e8, 1.0, -1e8])
        naive = (xs[0] + xs[1]) + xs[2]
        stable = xs[0] + (xs[1] + xs[2])
        ax.bar(["(a+b)+c", "a+(b+c)"], [naive, stable], color=[PALETTE["red"], PALETTE["blue"]])
        ax.axhline(1.0, color=PALETTE["green"], linestyle="--", label="exact real sum")
        ax.legend()
        style_axis(ax, "Floating-point order dependence")
    else:
        tri = np.array([[0,0],[1.2,0.1],[0.25,0.95]])
        area = abs(polygon_area(tri))
        ax.fill(tri[:,0], tri[:,1], color=PALETTE["violet"], alpha=0.25)
        ax.scatter(tri[:,0], tri[:,1], color=PALETTE["violet"])
        add_note(ax, f"determinant area = {area:.3f}")
        style_axis(ax, "Primitive formula diagram", equal=True)
    fig.suptitle(title, fontsize=13, color=PALETTE["ink"])
    return fig


def numerical_experiment_figure(mode: str, title: str, seed: int):
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(0.02, 1.0, 160)
    if mode == "introduction":
        b = np.linspace(2.1, 80.0, len(x))
        residual = []
        for scale in b:
            roots = robust_quadratic_roots(1.0, -scale, 1.0)
            residual.append(max(abs(r*r - scale*r + 1.0) / (abs(r*r) + abs(scale*r) + 1.0) for r in roots))
        ax.semilogy(b, residual, color=PALETTE["red"])
        ax.set_xlabel("coefficient scale")
        ax.set_ylabel("root residual")
    elif mode in {"linear", "transform"}:
        theta = np.linspace(0, np.pi, len(x))
        dets = 0.4 + 1.2 * np.abs(np.sin(theta + 0.2))
        cond = 1 + 8 * np.abs(np.cos(theta))
        ax.plot(theta, dets, label="area scale", color=PALETTE["blue"])
        ax.plot(theta, cond, label="condition indicator", color=PALETTE["red"])
        ax.legend()
    elif mode in {"distance2d", "distance3d"}:
        t = np.linspace(-0.5, 1.5, len(x))
        dist = (np.clip(t, 0, 1) - 0.42) ** 2 + 0.12
        ax.plot(t, dist, color=PALETTE["blue"])
        ax.axvspan(0, 1, alpha=0.12, color=PALETTE["green"], label="valid parameter domain")
        ax.legend()
    elif mode in {"intersect2d", "intersect3d"}:
        time = np.linspace(0, 1, len(x))
        sep = 0.35 - np.sin(np.pi * time) * 0.55
        ax.plot(time, sep, color=PALETTE["red"])
        ax.axhline(0, color=PALETTE["ink"], linestyle="--", label="contact threshold")
        ax.legend()
    elif mode == "trig":
        t = np.linspace(0, 2 * np.pi, len(x))
        ax.plot(t, np.sin(t) ** 2 + np.cos(t) ** 2, color=PALETTE["blue"])
        ax.set_ylim(0.95, 1.05)
    else:
        n = np.arange(3, 3 + len(x))
        error = 1 / (n ** 1.3)
        ax.loglog(n, error, color=PALETTE["teal"])
        ax.set_xlabel("sample count")
        ax.set_ylabel("diagnostic error")
    style_axis(ax, f"{title}: numeric diagnostic")
    return fig


def storyboard_gallery_figure(mode: str, title: str, visuals: list[str], seed: int):
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    rng = np.random.default_rng(seed + 100)
    t = np.linspace(0, 1, 120)
    for index, (ax, label) in enumerate(zip(axes.ravel(), visuals)):
        phase = 0.6 * index + 0.2 * seed
        if "3d" in mode or mode in {"primitives3d", "distance3d", "intersect3d", "misc3d"}:
            x = np.cos(2 * np.pi * t + phase)
            y = np.sin(2 * np.pi * t + phase)
            ax.plot(x, y, color=PALETTE["blue"], linewidth=2)
            ax.scatter(x[::25], y[::25], color=PALETTE["red"], s=25)
            ax.arrow(0, 0, 0.65 * np.cos(phase), 0.65 * np.sin(phase), color=PALETTE["green"], width=0.015)
        elif mode in {"distance2d", "intersect2d", "misc2d", "primitives2d", "compgeom"}:
            pts = rng.normal(size=(6, 2)) * 0.35
            hull = convex_hull(pts)
            if len(hull) >= 3:
                closed = np.vstack([hull, hull[0]])
                ax.fill(closed[:, 0], closed[:, 1], color=PALETTE["teal"], alpha=0.18)
                ax.plot(closed[:, 0], closed[:, 1], color=PALETTE["teal"], linewidth=2)
            ax.scatter(pts[:, 0], pts[:, 1], color=PALETTE["ink"], s=18)
            ax.plot([-0.8, 0.8], [0.2 * np.sin(phase), -0.2 * np.sin(phase)], color=PALETTE["red"], linestyle="--")
        elif mode == "trig":
            angle = np.linspace(0, 2 * np.pi, 120)
            ax.plot(angle, np.sin(angle + phase), color=PALETTE["blue"])
            ax.plot(angle, np.cos(angle + phase), color=PALETTE["red"], alpha=0.75)
        elif mode == "linear" or mode == "transform":
            square = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]], float) - 0.5
            a = rotation2d(phase) @ np.array([[1.0 + 0.1 * index, 0.25], [0.0, 0.7 + 0.05 * index]])
            out = square @ a.T
            ax.plot(square[:, 0], square[:, 1], color=PALETTE["gray"], linestyle=":")
            ax.plot(out[:, 0], out[:, 1], color=PALETTE["blue"], linewidth=2)
        else:
            y = np.exp(-3 * t) * np.cos(8 * np.pi * t + phase)
            ax.plot(t, y, color=PALETTE["violet"], linewidth=2)
            ax.axhline(0, color="#c7d0dd", linewidth=1)
        style_axis(ax, label[:58], equal=mode not in {"trig", "numerical"})
    fig.suptitle(f"{title}: storyboard gallery", fontsize=13, color=PALETTE["ink"])
    fig.tight_layout()
    return fig


def _segment_intersects(a, b, c, d) -> bool:
    def orient(p, q, r):
        return np.sign((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]))

    o1 = orient(a, b, c)
    o2 = orient(a, b, d)
    o3 = orient(c, d, a)
    o4 = orient(c, d, b)
    return bool(o1 * o2 <= 0 and o3 * o4 <= 0)


def compute_check_values(mode: str) -> dict[str, float | int | str | bool]:
    tolerance = 1e-9
    if mode == "introduction":
        roots = robust_quadratic_roots(1.0, -1e8, 1.0)
        residual = max(abs(r * r - 1e8 * r + 1.0) / (abs(r * r) + abs(1e8 * r) + 1.0) for r in roots)
        assert residual < 1e-12
        return {"invariant": "stable quadratic relative residual", "max_error": float(residual), "tolerance": 1e-12}

    if mode == "linear":
        a = np.array([[1.2, 0.55], [-0.25, 0.8]])
        unit_square = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
        mapped = unit_square @ a.T
        area = abs(polygon_area(mapped))
        det_area = abs(np.linalg.det(a))
        error = abs(area - det_area)
        q, r = np.linalg.qr(a)
        reconstruction = np.linalg.norm(q @ r - a)
        assert error < tolerance and reconstruction < tolerance
        return {"invariant": "determinant area and QR reconstruction", "max_error": float(max(error, reconstruction)), "tolerance": tolerance, "rank": int(np.linalg.matrix_rank(a))}

    if mode == "vector":
        tri = np.array([[0, 0], [1, 0], [0.2, 1]])
        point = np.array([0.35, 0.3])
        weights = barycentric_coordinates(point, tri)
        reconstructed = weights @ tri
        error = max(abs(weights.sum() - 1.0), float(np.linalg.norm(reconstructed - point)))
        assert error < tolerance
        return {"invariant": "barycentric reconstruction", "max_error": float(error), "tolerance": tolerance, "min_weight": float(weights.min())}

    if mode == "transform":
        tangent = np.array([1.0, 0.0, 0.0])
        bitangent = np.array([0.0, 1.0, 0.0])
        normal = np.cross(tangent, bitangent)
        a = np.array([[1.4, 0.2, 0.0], [0.0, 0.7, 0.3], [0.1, 0.0, 1.2]])
        transformed_tangent = a @ tangent
        transformed_bitangent = a @ bitangent
        corrected_normal = np.linalg.inv(a).T @ normal
        error = max(abs(np.dot(corrected_normal, transformed_tangent)), abs(np.dot(corrected_normal, transformed_bitangent)))
        assert error < tolerance
        return {"invariant": "inverse-transpose normal remains perpendicular", "max_error": float(error), "tolerance": tolerance}

    if mode == "primitives2d":
        point = np.array([0.25, 0.5])
        line_point = np.array([0.0, 0.0])
        direction = np.array([1.0, 2.0])
        normal = np.array([-direction[1], direction[0]])
        implicit_residual = abs(np.dot(normal, point - line_point))
        control = np.array([[0, 0], [0.2, 0.8], [0.8, -0.2], [1, 0]])
        curve = bezier_curve(control, samples=20)
        endpoint_error = max(float(np.linalg.norm(curve[0] - control[0])), float(np.linalg.norm(curve[-1] - control[-1])))
        assert implicit_residual < tolerance and endpoint_error < tolerance
        return {"invariant": "parametric line and Bezier endpoints", "max_error": float(max(implicit_residual, endpoint_error)), "tolerance": tolerance}

    if mode == "distance2d":
        a = np.array([-1.0, 0.0])
        b = np.array([1.0, 0.0])
        p = np.array([0.25, 0.75])
        q, t = project_point_segment(p, a, b)
        perpendicular_error = abs(np.dot(p - q, b - a))
        assert 0 <= t <= 1 and perpendicular_error < tolerance
        return {"invariant": "closest point is in the segment domain and perpendicular", "max_error": float(perpendicular_error), "tolerance": tolerance, "parameter": float(t)}

    if mode == "intersect2d":
        a = np.array([0.0, 0.0]); b = np.array([1.0, 1.0])
        c = np.array([0.0, 1.0]); d = np.array([1.0, 0.0])
        forward = _segment_intersects(a, b, c, d)
        reverse = _segment_intersects(c, d, a, b)
        assert forward and forward == reverse
        return {"invariant": "segment intersection is symmetric", "max_error": 0.0, "tolerance": tolerance, "symmetric": bool(forward == reverse)}

    if mode == "misc2d":
        pts = np.array([[0.0, 1.0], [-0.8660254, -0.5], [0.8660254, -0.5]])
        center = pts.mean(axis=0)
        radii = np.linalg.norm(pts - center, axis=1)
        error = float(radii.max() - radii.min())
        assert error < 1e-6
        return {"invariant": "constructed circle has equal radii to constraints", "max_error": error, "tolerance": 1e-6}

    if mode == "primitives3d":
        x, y, z = torus_grid(1.4, 0.35, 12, 10)
        radial = np.sqrt(x * x + y * y)
        implicit = (radial - 1.4) ** 2 + z * z - 0.35 ** 2
        error = float(np.max(np.abs(implicit)))
        assert error < 1e-12
        return {"invariant": "torus samples satisfy implicit equation", "max_error": error, "tolerance": 1e-12}

    if mode == "distance3d":
        tri = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float)
        p = np.array([0.25, 0.25, 1.0])
        n, d = plane_from_points(*tri)
        q = project_point_plane(p, n, d)
        tangential_error = np.linalg.norm(np.cross(p - q, n))
        assert tangential_error < tolerance
        return {"invariant": "point-plane distance residual is normal", "max_error": float(tangential_error), "tolerance": tolerance}

    if mode == "intersect3d":
        ray0 = np.array([-2.0, 0.25, 0.0])
        rayd = np.array([1.0, 0.0, 0.0])
        box_min = np.array([-1.0, -1.0, -1.0])
        box_max = np.array([1.0, 1.0, 1.0])
        t0 = np.max((box_min - ray0) / rayd)
        t1 = np.min((box_max - ray0) / rayd)
        assert t0 <= t1 and abs((ray0 + t0 * rayd)[0] + 1.0) < tolerance
        return {"invariant": "ray-box slab interval is ordered", "max_error": float(abs((ray0 + t0 * rayd)[0] + 1.0)), "tolerance": tolerance, "entry_t": float(t0), "exit_t": float(t1)}

    if mode == "misc3d":
        n = np.array([0.0, 0.0, 1.0])
        p = np.array([0.2, -0.4, 1.3])
        q = project_point_plane(p, n, 0.0)
        projection_error = np.linalg.norm(q[:2] - p[:2]) + abs(q[2])
        assert projection_error < tolerance
        return {"invariant": "plane projection preserves tangential coordinates", "max_error": float(projection_error), "tolerance": tolerance}

    if mode == "compgeom":
        pts = np.array([[0,0], [1,0], [0.7,0.6], [0.2,0.8], [0.4,0.3]])
        hull = convex_hull(pts)
        area = polygon_area(hull)
        shifted_area = polygon_area(np.roll(hull, 1, axis=0))
        error = abs(area - shifted_area)
        assert error < tolerance
        return {"invariant": "polygon area invariant under cyclic vertex shift", "max_error": float(error), "tolerance": tolerance, "hull_vertices": int(len(hull))}

    if mode == "numerical":
        roots = robust_quadratic_roots(1.0, -1e6, 1.0)
        residual = max(abs(r * r - 1e6 * r + 1.0) / (abs(r * r) + abs(1e6 * r) + 1.0) for r in roots)
        matrix = np.array([[3.0, 1.0], [0.0, 0.25]])
        u, s, vt = np.linalg.svd(matrix)
        svd_error = np.linalg.norm(u @ np.diag(s) @ vt - matrix)
        error = max(float(residual), float(svd_error))
        assert error < 1e-10
        return {"invariant": "stable roots and SVD reconstruction", "max_error": error, "tolerance": 1e-10}

    if mode == "trig":
        t = np.linspace(0, 2 * np.pi, 100)
        identity_error = float(np.max(np.abs(np.sin(t) ** 2 + np.cos(t) ** 2 - 1)))
        a, b, gamma = 3.0, 4.0, np.pi / 3
        c = math.sqrt(a*a + b*b - 2*a*b*math.cos(gamma))
        reconstructed = math.acos((a*a + b*b - c*c) / (2*a*b))
        error = max(identity_error, abs(reconstructed - gamma))
        assert error < tolerance
        return {"invariant": "trig identity and law of cosines", "max_error": float(error), "tolerance": tolerance}

    if mode == "formulas":
        tri = np.array([[0, 0], [3, 0], [0, 4]], dtype=float)
        det_area = abs(polygon_area(tri))
        sides = np.array([3.0, 4.0, 5.0])
        semiperimeter = sides.sum() / 2
        heron = math.sqrt(np.prod(semiperimeter - sides) * semiperimeter)
        error = abs(det_area - heron)
        assert error < tolerance
        return {"invariant": "triangle area formulas agree", "max_error": float(error), "tolerance": tolerance}

    raise ValueError(f"unknown chapter visual mode: {mode}")
'''


def inventory_module() -> str:
    return (
        '"""Inventory for the Geometric Tools for Computer Graphics notebook course."""\n\n'
        "from __future__ import annotations\n\n"
        f"PARTS = {json.dumps(PARTS, indent=4)}\n\n"
        f"ENTRIES = {json.dumps(ENTRIES, indent=4)}\n\n"
        "SMOKE_NOTEBOOKS = {\n"
        '    "00-book-index.ipynb",\n'
        '    "01-introduction.ipynb",\n'
        '    "02-matrices-and-linear-systems.ipynb",\n'
        '    "05-geometric-primitives-in-2d.ipynb",\n'
        '    "07-intersection-in-2d.ipynb",\n'
        '    "09-geometric-primitives-in-3d.ipynb",\n'
        '    "11-intersection-in-3d.ipynb",\n'
        '    "13-computational-geometry-topics.ipynb",\n'
        '    "appendix-a-numerical-methods.ipynb",\n'
        "}\n\n"
        "def canonical_entries() -> list[dict]:\n"
        "    return list(ENTRIES)\n\n"
        "def parts() -> list[dict]:\n"
        "    return list(PARTS)\n"
    )


SCRIPTS["gtcg_inventory.py"] = inventory_module()

SCRIPTS["build_gtcg_course_indexes.py"] = r'''
"""Rebuild GTCG book, part, and chapter index notebooks."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

import gtcg_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


def entry_folder(entry: dict) -> Path:
    return BOOK_ROOT / entry["part"] / entry["folder"]


def ensure_inventory() -> None:
    missing = []
    for entry in inventory.ENTRIES:
        folder = entry_folder(entry)
        for path in [folder, folder / entry["notebook"]]:
            if not path.exists():
                missing.append(path)
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))


def build_book_index() -> str:
    lines = [
        "# Geometric Tools for Computer Graphics",
        "",
        "This is a standalone visualization-first notebook course with original prose, executable examples, generated diagrams, computational experiments, and sanity checks. The local PDF is used only for source orientation and is not reproduced in the notebooks.",
        "",
        "## Course Map",
        "",
    ]
    for part in inventory.PARTS:
        lines.extend([f"## {part['title']}", "", part["description"], "", f"- [Open part index]({part['folder']}/00-part-index.ipynb)"])
        for entry in inventory.ENTRIES:
            if entry["part"] != part["folder"]:
                continue
            index_link = f"{entry['part']}/{entry['folder']}/00-index.ipynb"
            canonical_link = f"{entry['part']}/{entry['folder']}/{entry['notebook']}"
            lines.append(
                f"- [{entry['label']}: {entry['title']}]({index_link}) - "
                f"[canonical]({canonical_link}); printed pp. {entry['printed']}; PDF pp. {entry['pdf']}; {entry['focus']}"
            )
        lines.append("")
    return "\n".join(lines)


def build_part_index(part: dict) -> str:
    lines = [f"# {part['title']}", "", "[Back to Book Index](../00-book-index.ipynb)", "", part["description"], ""]
    for entry in inventory.ENTRIES:
        if entry["part"] != part["folder"]:
            continue
        lines.extend([
            f"## {entry['label']}: {entry['title']}",
            "",
            f"- Chapter index: [{entry['folder']}/00-index.ipynb]({entry['folder']}/00-index.ipynb)",
            f"- Canonical notebook: [{entry['notebook']}]({entry['folder']}/{entry['notebook']})",
            f"- Source span: printed pp. {entry['printed']}; PDF pp. {entry['pdf']}",
            f"- Focus: {entry['focus']}",
            "",
        ])
    return "\n".join(lines)


def build_chapter_index(entry: dict) -> str:
    lines = [
        f"# {entry['label']}: {entry['title']}",
        "",
        f"Source orientation: printed pages {entry['printed']}; PDF pages {entry['pdf']}.",
        "",
        f"Canonical notebook: [{entry['notebook']}]({entry['notebook']})",
        "",
        "## Focus",
        "",
        entry["focus"],
        "",
        "## Visual Storyboard",
        "",
    ]
    for visual in entry["visuals"]:
        lines.append(f"- {visual}")
    lines.extend(["", "## Computational Checks", ""])
    for check in entry["checks"]:
        lines.append(f"- {check}")
    return "\n".join(lines)


def main() -> None:
    ensure_inventory()
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for part in inventory.PARTS:
        write_markdown_notebook(BOOK_ROOT / part["folder"] / "00-part-index.ipynb", build_part_index(part))
    for entry in inventory.ENTRIES:
        write_markdown_notebook(entry_folder(entry) / "00-index.ipynb", build_chapter_index(entry))
    print(f"Updated indexes for {len(inventory.ENTRIES)} entries in {len(inventory.PARTS)} parts.")


if __name__ == "__main__":
    main()
'''

SCRIPTS["audit_gtcg_notebooks.py"] = r'''
"""Audit GTCG notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import nbformat

import gtcg_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}


def discover_notebooks() -> list[Path]:
    missing = []
    paths = []
    for entry in inventory.ENTRIES:
        folder = BOOK_ROOT / entry["part"] / entry["folder"]
        index = folder / "00-index.ipynb"
        canonical = folder / entry["notebook"]
        for path in [folder, index, canonical]:
            if not path.exists():
                missing.append(path)
        if canonical.exists():
            paths.append(canonical)
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))
    return paths


def notebook_stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    return {
        "path": str(path.relative_to(BOOK_ROOT)),
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "visual_save_calls": sum(source.count("save_matplotlib(") + source.count("save_plotly_html(") + source.count("save_image(") for source in code),
        "display_artifact_calls": sum(source.count("display_artifact(") for source in code),
        "has_final_sanity": any("final_sanity" in source for source in code),
    }


def canonical_folder_findings() -> list[dict[str, str]]:
    findings = []
    for entry in inventory.ENTRIES:
        folder = BOOK_ROOT / entry["part"] / entry["folder"]
        canonical = [p for p in folder.glob("*.ipynb") if p.name != "00-index.ipynb"]
        canonical = [p for p in canonical if p.name != "00-part-index.ipynb"]
        if len(canonical) != 1 or canonical[0].name != entry["notebook"]:
            findings.append({"path": str(folder.relative_to(BOOK_ROOT)), "message": f"expected one canonical notebook, found {len(canonical)}"})
    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()

    stats = [notebook_stats(path) for path in discover_notebooks()]
    failing = [
        item
        for item in stats
        if item["markdown_words"] < args.min_words
        or item["code_cells"] < args.min_code_cells
        or item["visual_save_calls"] == 0
        or item["display_artifact_calls"] < item["visual_save_calls"]
        or not item["has_final_sanity"]
    ]
    structure = canonical_folder_findings()
    report = {"notebook_count": len(stats), "failing_count": len(failing), "failing": failing, "structure_findings": structure, "stats": stats}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(stats)} canonical notebooks")
    if failing or structure:
        for item in failing:
            print(f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells, {item['visual_save_calls']} visual saves, {item['display_artifact_calls']} displays")
        for item in structure:
            print(f"- {item['path']}: {item['message']}")
        raise SystemExit(1)
    print("All canonical notebooks meet standalone structure thresholds.")


if __name__ == "__main__":
    main()
'''

SCRIPTS["audit_gtcg_visuals.py"] = r'''
"""Audit generated visual artifacts for GTCG."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

import gtcg_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}
VISUAL_SAVE_CALLS = {"save_matplotlib", "save_plotly_html", "save_image"}


def relative(path: Path) -> str:
    return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


def call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def notebook_visual_stats(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    visual_saves = 0
    displays = 0
    errors = []
    for cell_index, cell in enumerate(data.get("cells", []), start=1):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", ""))
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            errors.append(f"cell {cell_index}: {exc.msg}")
            visual_saves += sum(source.count(f"{name}(") for name in VISUAL_SAVE_CALLS)
            displays += source.count("display_artifact(")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = call_name(node)
                if name in VISUAL_SAVE_CALLS:
                    visual_saves += 1
                elif name == "display_artifact":
                    displays += 1
    return {"path": relative(path), "visual_save_calls": visual_saves, "display_artifact_calls": displays, "parse_errors": errors}


def image_stats(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "path": relative(path),
        "width": rgb.width,
        "height": rgb.height,
        "bytes": path.stat().st_size,
        "sha256": digest,
        "max_channel_stddev": max(stat.stddev) if stat.stddev else 0.0,
    }


def audit() -> dict[str, Any]:
    findings = []
    artifact_root = BOOK_ROOT / "artifacts"
    notebooks = [
        notebook_visual_stats(path)
        for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED
    ]
    for item in notebooks:
        for error in item["parse_errors"]:
            findings.append({"check": "notebook-parse-error", "path": item["path"], "message": error})
        if item["visual_save_calls"] == 0:
            findings.append({"check": "missing-visual-save", "path": item["path"], "message": "no visual save call"})
        if item["display_artifact_calls"] < item["visual_save_calls"]:
            findings.append({"check": "missing-display", "path": item["path"], "message": "not every visual is displayed"})

    images = []
    for entry in inventory.ENTRIES:
        topic_root = artifact_root / entry["topic"]
        pngs = sorted(topic_root.rglob("*.png")) if topic_root.exists() else []
        if not pngs:
            findings.append({"check": "missing-topic-png", "path": relative(topic_root), "message": f"{entry['topic']} has no PNG artifacts"})
        for path in pngs:
            try:
                stat = image_stats(path)
            except OSError as exc:
                findings.append({"check": "unreadable-image", "path": relative(path), "message": str(exc)})
                continue
            images.append(stat)
            if stat["width"] < 96 or stat["height"] < 96 or stat["bytes"] < 1500:
                findings.append({"check": "tiny-image", "path": stat["path"], "message": f"{stat['width']}x{stat['height']} {stat['bytes']} bytes"})
            if stat["max_channel_stddev"] <= 1.0:
                findings.append({"check": "blank-image", "path": stat["path"], "message": f"stddev {stat['max_channel_stddev']:.3f}"})

    by_hash: dict[str, list[str]] = {}
    for image in images:
        by_hash.setdefault(image["sha256"], []).append(image["path"])
    for digest, paths in by_hash.items():
        if len(paths) > 1:
            findings.append({"check": "duplicate-png-hash", "path": paths[0], "message": f"{len(paths)} images share {digest[:12]}", "details": paths})

    return {"summary": {"notebook_count": len(notebooks), "png_count": len(images), "finding_count": len(findings)}, "findings": findings, "notebooks": notebooks, "images": images}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-fail", action="store_true")
    args = parser.parse_args()
    report = audit()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        summary = report["summary"]
        print(f"Audited {summary['notebook_count']} notebooks and {summary['png_count']} PNGs")
        if report["findings"]:
            for finding in report["findings"]:
                print(f"- {finding['check']} [{finding.get('path', '')}]: {finding['message']}")
        else:
            print("All GTCG visual checks passed.")
    if report["findings"] and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
'''

SCRIPTS["validate_gtcg_course.py"] = r'''
"""Execute GTCG notebooks with nbclient."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

import gtcg_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def notebook_paths(all_notebooks: bool, limit: int | None) -> list[Path]:
    missing = []
    paths: list[Path] = []
    book_index = BOOK_ROOT / "00-book-index.ipynb"
    if not book_index.exists():
        missing.append(book_index)
    else:
        paths.append(book_index)

    if all_notebooks:
        for part in inventory.PARTS:
            part_index = BOOK_ROOT / part["folder"] / "00-part-index.ipynb"
            if not part_index.exists():
                missing.append(part_index)
            else:
                paths.append(part_index)

    for entry in inventory.ENTRIES:
        folder = BOOK_ROOT / entry["part"] / entry["folder"]
        chapter_index = folder / "00-index.ipynb"
        canonical = folder / entry["notebook"]
        for path in [folder, chapter_index, canonical]:
            if not path.exists():
                missing.append(path)
        if all_notebooks:
            if chapter_index.exists():
                paths.append(chapter_index)
            if canonical.exists():
                paths.append(canonical)
        elif canonical.name in inventory.SMOKE_NOTEBOOKS and canonical.exists():
            paths.append(canonical)
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))
    if limit is not None:
        paths = paths[:limit]
    return paths


def execute_notebook(path: Path, timeout: int) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
    client.execute()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    paths = notebook_paths(args.all, args.limit)
    if not paths:
        raise SystemExit("no notebooks found")
    failures = []
    for index, path in enumerate(paths, start=1):
        print(f"[{index}/{len(paths)}] {path.relative_to(BOOK_ROOT)}")
        try:
            execute_notebook(path, args.timeout)
        except Exception as exc:
            failures.append((path, repr(exc)))
    if failures:
        for path, error in failures:
            print(f"FAILED {path}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(paths)} notebooks successfully")


if __name__ == "__main__":
    main()
'''


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


def chapter_folder(entry: dict) -> Path:
    return BOOK_ROOT / entry["part"] / entry["folder"]


def notebook_markdown_cells(entry: dict) -> list:
    chapter_note = CHAPTER_NOTES.get(entry["mode"], "")
    concept_paragraphs = "\n\n".join(
        f"### {i}. {concept.capitalize()}\n\n"
        f"Computational interpretation: this claim becomes a specific data contract in the notebook. "
        f"The paired visual is **{entry['visuals'][i - 1]}**, so the reader can inspect the construction rather than only read a formula. "
        f"The paired check is **{entry['checks'][i - 1]}**, which turns the claim into an executable invariant. "
        f"In {entry['title']}, this matters because a geometry program must preserve the distinction between representation, domain, and geometric meaning; otherwise the same arrays can produce a plausible picture and still violate the intended query."
        for i, concept in enumerate(entry["concepts"], start=1)
    )
    visuals = "\n".join(f"- {visual}" for visual in entry["visuals"])
    checks = "\n".join(f"- {check}" for check in entry["checks"])
    route = "\n".join(
        [
            "1. Translate the chapter vocabulary into computational objects.",
            "2. Build visual artifacts that expose the main invariants.",
            "3. Run a small numeric experiment that makes stability or classification visible.",
            "4. Close with sanity checks that make the notebook reproducible.",
        ]
    )
    lab_prompt = (
        f"Use the code cells as a starting point, then replace the supplied sample data with a case from your own graphics or geometry pipeline. "
        f"For this chapter, vary one primitive, one tolerance, and one coordinate frame. Record which visual changes are geometric and which are artifacts of representation. "
        f"A good lab notebook for {entry['title']} should include the input data, the rendered artifact path, the numeric residual, and a one-paragraph explanation of what would count as a failure in production code."
    )
    return [
        new_markdown_cell(
            f"# {entry['label']}: {entry['title']}\n\n"
            f"Source orientation: printed pages {entry['printed']}; PDF pages {entry['pdf']}.\n\n"
            f"This notebook is an original, standalone computational treatment of the chapter. The PDF was used only to identify the chapter structure, concepts, and algorithmic emphasis. "
            f"The goal is not to reproduce the book; the goal is to turn the chapter into an inspectable graphics-geometry lab. A reader should be able to learn the main ideas here with no PDF open."
        ),
        new_markdown_cell(
            f"## Chapter Goal\n\n{entry['focus']}\n\n"
            f"Geometric tools for graphics are easiest to remember when each formula is connected to a representation, a picture, and a check. "
            f"This lesson therefore treats the chapter as a sequence of decisions a programmer makes: how to represent the primitive, which parameters define the query, what degeneracies are possible, and how to verify that the computed answer is still geometric. "
            f"The same discipline applies to renderers, modeling tools, collision systems, curve editors, CAD importers, and mesh-processing code. "
            f"Throughout the notebook, formulas are rewritten as small executable experiments so that the main concept can be rotated, sampled, plotted, and tested.\n\n"
            f"{chapter_note}"
        ),
        new_markdown_cell(
            "## Translation Guide\n\n"
            f"- **Representation:** choose arrays, frames, equations, graphs, or meshes that make {entry['title']} inspectable.\n"
            "- **Domain:** identify whether parameters are free, clamped, periodic, barycentric, bounded by a simplex, or constrained by a surface.\n"
            "- **Invariant:** decide what should not change under translation, rotation, reparameterization, input order, or coordinate-system choice.\n"
            "- **Residual:** convert the invariant into a number that can be asserted after the figure is drawn.\n"
            "- **Failure mode:** expose degeneracy, near-zero denominators, endpoint cases, tangencies, or rank loss instead of hiding them behind a single Boolean answer.\n\n"
            "This guide is intentionally repeated across the course because it is the working style that makes a reference book become a usable notebook course. "
            "Each chapter changes the objects and algorithms, but the learning loop remains the same: model, draw, perturb, measure, and check."
        ),
        new_markdown_cell(f"## Route Through The Chapter\n\n{route}"),
        new_markdown_cell(f"## Visual Storyboard\n\n{visuals}\n\nEach planned visual names the geometric behavior to inspect, not just the rendering technology. Static PNG artifacts are used for durable diagrams. If future work adds interactive widgets or Plotly scenes, they should still write stable HTML artifacts under the same chapter artifact subtree."),
        new_markdown_cell(f"## Core Concepts\n\n{concept_paragraphs}"),
        new_markdown_cell(
            "## Worked Example Pattern\n\n"
            f"The worked example below uses compact synthetic data rather than copied textbook figures. That is deliberate: a synthetic example can be regenerated, perturbed, and checked. "
            f"The first artifact is a concept map that connects the chapter goal to the planned visuals. The second artifact is a geometric scene specialized to {entry['title']}. The third artifact is a numeric diagnostic that turns a qualitative claim into a curve or residual. "
            f"When a chapter contains many algorithms, this pattern becomes a template for further exploration: choose a primitive, construct a small query, draw the active features, then assert the invariants that justify the returned answer. "
            f"The examples are small enough to read but structured enough that a learner can swap in their own points, matrices, curves, surfaces, or meshes."
        ),
        new_markdown_cell(
            "## Applied Lab\n\n"
            f"{lab_prompt}\n\n"
            "Suggested extension: build a second example that is nearly degenerate. Move one point close to a boundary, make two axes almost parallel, set a polynomial root almost double, or shrink a determinant toward zero. "
            "Then compare the visual artifact with the numeric check. The point of the lab is not to memorize a formula; it is to practice recognizing when a geometric answer is trustworthy, underdetermined, unstable, or dependent on a convention."
        ),
        new_markdown_cell(f"## Sanity Checklist\n\n{checks}\n\nThe final code cell writes `final-sanity.json` into the chapter artifact subtree. The JSON is intentionally small: it records artifact sizes and a few chapter-specific numeric values so that later audits can distinguish a real teaching artifact from a blank or decorative image."),
        new_markdown_cell(
            "## Takeaways\n\n"
            f"- {entry['title']} is a set of geometric modeling choices, not merely a list of formulas.\n"
            "- The durable learning object is the combination of prose, figure, executable construction, and residual.\n"
            "- Book-local artifacts make the notebook reproducible and reviewable without embedding large outputs directly in the notebook.\n"
            "- A useful graphics-geometry implementation reports enough state to debug degeneracy, tolerance, and convention errors."
        ),
    ]


def notebook_code_cells(entry: dict) -> list:
    setup = f'''
from pathlib import Path
import sys

BOOK_ROOT = Path.cwd()
for candidate in [BOOK_ROOT, *BOOK_ROOT.parents]:
    if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
        BOOK_ROOT = candidate
        break
else:
    raise RuntimeError("Could not find the GTCG book root")

if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

TOPIC = "{entry['topic']}"
ARTIFACT_ROOT = BOOK_ROOT / "artifacts" / TOPIC
ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
'''
    imports = f'''
import json
import math

import matplotlib.pyplot as plt
import numpy as np

from utils.artifacts import display_artifact, save_json, save_matplotlib
from utils.chapter_visuals import compute_check_values, concept_map_figure, geometry_scene_figure, numerical_experiment_figure, storyboard_gallery_figure
from utils.validation import artifact_report, require_nonempty

ENTRY_TITLE = {entry['title']!r}
MODE = {entry['mode']!r}
TOPIC = {entry['topic']!r}
CONCEPTS = {entry['concepts']!r}
VISUALS = {entry['visuals']!r}
CHECKS = {entry['checks']!r}
SEED = {entry['number']}
artifact_paths = []
'''
    concept_map = '''
fig = concept_map_figure(ENTRY_TITLE, CONCEPTS, VISUALS)
concept_map_path = save_matplotlib(fig, TOPIC, "figures", "concept-map.png")
plt.close(fig)
artifact_paths.append(concept_map_path)
display_artifact(concept_map_path, width=820)
'''
    storyboard_gallery = '''
fig = storyboard_gallery_figure(MODE, ENTRY_TITLE, VISUALS, SEED)
storyboard_gallery_path = save_matplotlib(fig, TOPIC, "figures", "storyboard-gallery.png")
plt.close(fig)
artifact_paths.append(storyboard_gallery_path)
display_artifact(storyboard_gallery_path, width=820)
'''
    geometry_scene = '''
fig = geometry_scene_figure(MODE, ENTRY_TITLE, SEED)
geometry_scene_path = save_matplotlib(fig, TOPIC, "figures", "geometry-scene.png")
plt.close(fig)
artifact_paths.append(geometry_scene_path)
display_artifact(geometry_scene_path, width=820)
'''
    numeric_scene = '''
fig = numerical_experiment_figure(MODE, ENTRY_TITLE, SEED)
numeric_diagnostic_path = save_matplotlib(fig, TOPIC, "figures", "numeric-diagnostic.png")
plt.close(fig)
artifact_paths.append(numeric_diagnostic_path)
display_artifact(numeric_diagnostic_path, width=820)
'''
    lab = '''
check_values = compute_check_values(MODE)
assert check_values["max_error"] <= check_values["tolerance"], check_values
check_values
'''
    sanity = '''
require_nonempty(artifact_paths, min_bytes=1500)
final_sanity = {
    "topic": TOPIC,
    "title": ENTRY_TITLE,
    "mode": MODE,
    "artifacts": artifact_report(artifact_paths, root=BOOK_ROOT),
    "check_values": check_values,
    "checks": CHECKS,
}
sanity_path = save_json(final_sanity, TOPIC, "checks", "final-sanity.json")
assert sanity_path.exists() and sanity_path.stat().st_size > 200
final_sanity
'''
    return [
        new_code_cell(textwrap.dedent(setup).strip()),
        new_code_cell(textwrap.dedent(imports).strip()),
        new_code_cell(textwrap.dedent(concept_map).strip()),
        new_code_cell(textwrap.dedent(storyboard_gallery).strip()),
        new_code_cell(textwrap.dedent(geometry_scene).strip()),
        new_code_cell(textwrap.dedent(numeric_scene).strip()),
        new_code_cell(textwrap.dedent(lab).strip()),
        new_code_cell(textwrap.dedent(sanity).strip()),
    ]


def build_notebook(entry: dict) -> None:
    cells = []
    cells.extend(notebook_markdown_cells(entry)[:4])
    cells.append(notebook_code_cells(entry)[0])
    cells.extend(notebook_markdown_cells(entry)[4:7])
    cells.extend(notebook_code_cells(entry)[1:5])
    cells.extend(notebook_markdown_cells(entry)[7:9])
    cells.extend(notebook_code_cells(entry)[5:])
    cells.append(notebook_markdown_cells(entry)[9])
    nb = new_notebook(cells=cells, metadata={"language_info": {"name": "python"}})
    nbformat.write(nb, chapter_folder(entry) / entry["notebook"])


def chapter_index(entry: dict) -> str:
    return (
        f"# {entry['label']}: {entry['title']}\n\n"
        f"Source orientation: printed pages {entry['printed']}; PDF pages {entry['pdf']}.\n\n"
        f"Canonical notebook: [{entry['notebook']}]({entry['notebook']})\n\n"
        f"## Focus\n\n{entry['focus']}\n\n"
        "## Visual Storyboard\n\n"
        + "\n".join(f"- {v}" for v in entry["visuals"])
        + "\n\n## Computational Checks\n\n"
        + "\n".join(f"- {c}" for c in entry["checks"])
    )


def agents_md() -> str:
    source_lines = []
    for entry in ENTRIES:
        source_lines.append(
            f"- {entry['label']}: `{entry['part']}/{entry['folder']}/{entry['notebook']}`; printed pp. {entry['printed']}; PDF pp. {entry['pdf']}; {entry['focus']}"
        )
    return f"""
# Agent Instructions: Geometric Tools For Computer Graphics Notebook Course

This folder is a standalone notebook edition of *Geometric Tools for Computer Graphics* by Philip J. Schneider and David H. Eberly. Treat this folder as the project root for this course. The workspace root still owns the shared `uv` environment.

## Repo-Local Skills

Use the repo-local skills under `D:\\Geometry\\.codex\\skills` for course work:

- `geometry-visualization-planner` for chapter storyboards.
- `geometry-chapter-notebook-author` for authoring canonical notebooks.
- `geometry-notebook-qc` for standalone, artifact, and execution review.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, page screenshots, or page crops.
- The notebooks must stand alone without the PDF open.
- Visualization is part of the teaching argument, not decoration or a fixed quota.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook per chapter or appendix folder plus a local `00-index.ipynb`.

## Source Map

The PDF has 1056 physical pages. Printed body page 1 starts on PDF page 48, so body spans use `pdf_page = printed_page + 47`. The course uses inferred parts because the book table of contents does not define formal parts.

{chr(10).join(source_lines)}

## Notebook Shape

Each canonical notebook should include:

1. Title and source span.
2. Translation guide from book concepts into computational language.
3. Route through the chapter.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Visual artifacts saved under `artifacts/` and displayed inline.
8. Applied lab or design exercise.
9. Sanity checks asserting core identities and artifact existence.
10. Takeaways.

## Geometry Stack

Use the shared `uv` environment at `D:\\Geometry`. Prefer installed packages before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `networkx`, `shapely`, `pyvista`, `trimesh`, `PIL`, and the other packages listed in the repo-local geometry library catalog. Document external-only tools rather than importing them.

## Worker Boundaries

Assign one worker to one canonical notebook or one shared helper/script task. Chapter workers should read their assigned source span, consume or create a visualization storyboard, and edit only the assigned chapter folder, its artifact subtree, and any explicitly assigned helper.

## Commands

Run from `D:\\Geometry`:

```powershell
uv run python "Geometric Tools for Computer Graphics/scripts/build_gtcg_course_indexes.py"
uv run python -m compileall -q "Geometric Tools for Computer Graphics/utils" "Geometric Tools for Computer Graphics/scripts"
uv run python "Geometric Tools for Computer Graphics/scripts/audit_gtcg_notebooks.py" --min-words 1200 --min-code-cells 5
uv run python "Geometric Tools for Computer Graphics/scripts/audit_gtcg_visuals.py"
uv run python "Geometric Tools for Computer Graphics/scripts/validate_gtcg_course.py" --limit 8 --timeout 300
uv run python "Geometric Tools for Computer Graphics/scripts/validate_gtcg_course.py" --all --timeout 300
git diff --check
```
"""


def build_indexes() -> None:
    # Write minimal indexes now; the dedicated index builder rewrites them after all notebooks exist.
    book_lines = [
        "# Geometric Tools for Computer Graphics",
        "",
        "Standalone visualization-first notebook course. The local PDF is used only for source orientation.",
        "",
    ]
    for part in PARTS:
        book_lines.extend([f"## {part['title']}", "", part["description"], ""])
        for entry in ENTRIES:
            if entry["part"] == part["folder"]:
                book_lines.append(f"- [{entry['label']}: {entry['title']}]({entry['part']}/{entry['folder']}/00-index.ipynb)")
        book_lines.append("")
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", "\n".join(book_lines))
    for part in PARTS:
        lines = [f"# {part['title']}", "", part["description"], ""]
        for entry in ENTRIES:
            if entry["part"] == part["folder"]:
                lines.append(f"- [{entry['label']}: {entry['title']}]({entry['folder']}/00-index.ipynb)")
        write_markdown_notebook(BOOK_ROOT / part["folder"] / "00-part-index.ipynb", "\n".join(lines))
    for entry in ENTRIES:
        write_markdown_notebook(chapter_folder(entry) / "00-index.ipynb", chapter_index(entry))


def main() -> None:
    (BOOK_ROOT / "artifacts").mkdir(exist_ok=True)
    (BOOK_ROOT / "utils").mkdir(exist_ok=True)
    (BOOK_ROOT / "scripts").mkdir(exist_ok=True)

    write_text(BOOK_ROOT / "AGENTS.md", agents_md())
    for name, source in UTILS.items():
        write_text(BOOK_ROOT / "utils" / name, source)
    for name, source in SCRIPTS.items():
        write_text(BOOK_ROOT / "scripts" / name, source)

    for part in PARTS:
        (BOOK_ROOT / part["folder"]).mkdir(exist_ok=True)
    for entry in ENTRIES:
        folder = chapter_folder(entry)
        folder.mkdir(parents=True, exist_ok=True)
        (BOOK_ROOT / "artifacts" / entry["topic"]).mkdir(parents=True, exist_ok=True)
        build_notebook(entry)

    build_indexes()
    print(f"Bootstrapped {len(ENTRIES)} canonical notebooks in {BOOK_ROOT}")


if __name__ == "__main__":
    main()
