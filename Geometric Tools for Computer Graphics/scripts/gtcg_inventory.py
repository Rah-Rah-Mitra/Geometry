"""Inventory for the Geometric Tools for Computer Graphics notebook course."""

from __future__ import annotations

PARTS = [
    {
        "folder": "part-01-foundations",
        "title": "Part I: Foundations",
        "description": "Numerical robustness, linear algebra, vector algebra, affine frames, and transformations."
    },
    {
        "folder": "part-02-2d-geometric-tools",
        "title": "Part II: 2D Geometric Tools",
        "description": "Planar primitives, distance queries, intersection queries, and classical construction problems."
    },
    {
        "folder": "part-03-3d-geometric-tools",
        "title": "Part III: 3D Geometric Tools",
        "description": "Spatial primitives, meshes, quadrics, surfaces, 3D distance, 3D intersection, and projection tools."
    },
    {
        "folder": "part-04-computational-geometry",
        "title": "Part IV: Computational Geometry",
        "description": "BSP trees, containment, Boolean operations, convex hulls, Delaunay triangulation, partitioning, bounds, area, and volume."
    },
    {
        "folder": "part-05-appendices",
        "title": "Part V: Appendices",
        "description": "Numerical methods, trigonometric tools, and a formula atlas for common geometric primitives."
    }
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
            "robust implementations record assumptions, tolerances, and symmetry checks explicitly"
        ],
        "visuals": [
            "floating-point cancellation and stable quadratic roots",
            "parameter-domain search for closest points",
            "near-boundary point classification under tolerance changes",
            "query pipeline from primitive model to numeric verdict"
        ],
        "checks": [
            "stable quadratic roots agree with polynomial residuals",
            "closest-point parameters remain inside their allowed domain",
            "orientation classification is symmetric after reversing inputs",
            "tolerance bands are reported rather than hidden"
        ]
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
            "least squares replaces impossible exact constraints with a projection onto a column space"
        ],
        "visuals": [
            "grid deformation by a linear map",
            "row-reduction pivots and rank",
            "determinant area scale and orientation",
            "least-squares residual as an orthogonal component"
        ],
        "checks": [
            "matrix area scale matches the determinant",
            "least-squares residual is orthogonal to the column space",
            "row-reduction rank matches numpy matrix rank",
            "eigenvectors reproduce their scaled directions"
        ]
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
            "barycentric coordinates describe simplexes with weights that sum to one"
        ],
        "visuals": [
            "head-to-tail vector arithmetic",
            "basis change inside an affine frame",
            "oriented area and scalar triple product",
            "barycentric coordinates over a triangle and tetrahedron"
        ],
        "checks": [
            "barycentric weights sum to one",
            "orientation changes sign when two vertices are swapped",
            "cross product is perpendicular to both inputs",
            "affine combinations are invariant under translation"
        ]
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
            "normal vectors transform by inverse transpose because they represent plane constraints"
        ],
        "visuals": [
            "point and vector homogeneous weights",
            "composition of translation, rotation, scale, reflection, and shear",
            "projection comparison panel",
            "normal transform failure and inverse-transpose correction"
        ],
        "checks": [
            "vectors are unchanged by pure translation in homogeneous form",
            "composed transforms match stepwise application",
            "perspective division preserves cross-ratio in a line example",
            "corrected normals remain perpendicular to transformed tangents"
        ]
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
            "free-form curves trade exact algebra for controlled local shape and subdivision"
        ],
        "visuals": [
            "implicit versus parametric line forms",
            "polygon classification gallery",
            "conic level sets",
            "Bezier and B-spline control polygon comparison"
        ],
        "checks": [
            "points sampled from a parametric line satisfy the implicit equation",
            "polygon signed area reports orientation",
            "Bezier endpoints match the first and last control points",
            "curve bounding boxes contain sampled points"
        ]
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
            "the returned closest features are as important as the scalar distance"
        ],
        "visuals": [
            "point-to-segment projection with clamped parameter",
            "triangle closest-feature regions",
            "distance-to-polygon isolines",
            "GJK simplex walk toward the origin"
        ],
        "checks": [
            "clamped closest-point parameter lies in [0, 1]",
            "gradient points toward the closest feature away from medial events",
            "Minkowski difference origin distance matches direct convex distance",
            "feature labels are stable away from boundaries"
        ]
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
            "contact sets record whether the meeting is vertex, edge, transverse, or tangential"
        ],
        "visuals": [
            "segment-segment orientation tests",
            "ellipse-line root panel",
            "separating-axis interval projections",
            "moving polygon contact timeline"
        ],
        "checks": [
            "segment intersection is symmetric in both inputs",
            "roots substituted into curve equations have small residual",
            "all separating-axis overlaps agree with polygon intersection",
            "first-contact time lies inside the reported interval"
        ]
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
            "a robust implementation must return zero, one, two, or four solutions without surprise"
        ],
        "visuals": [
            "circle through three points",
            "offset-line tangent construction",
            "two-circle tangent families",
            "solution-count phase diagram"
        ],
        "checks": [
            "constructed circle centers are equidistant from constraints",
            "tangent radius is perpendicular to the tangent line at contact",
            "solution counts match distance thresholds",
            "perpendicular and parallel constructed lines satisfy dot-product tests"
        ]
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
            "quadrics and parametric surfaces expose shape through eigenstructure and parameter grids"
        ],
        "visuals": [
            "plane basis and embedded polygon",
            "mesh incidence and manifold checks",
            "quadric surface gallery",
            "torus and parametric surface coordinates"
        ],
        "checks": [
            "plane basis vectors are orthonormal and perpendicular to the normal",
            "mesh Euler counts match the constructed example",
            "quadric samples satisfy their implicit equation",
            "surface normals are perpendicular to parameter tangents"
        ]
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
            "surface distance often requires iterative minimization with residual diagnostics"
        ],
        "visuals": [
            "point-to-triangle closest-feature map",
            "segment-segment closest connector",
            "oriented-box local coordinates",
            "ellipsoid distance iteration trace"
        ],
        "checks": [
            "closest connector is perpendicular to active unconstrained features",
            "barycentric coordinates classify triangle features",
            "local-frame and world-frame distances agree",
            "iterative residuals decrease for the shown surface example"
        ]
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
            "separating-axis tests generalize to face normals and edge-cross-edge axes"
        ],
        "visuals": [
            "ray and plane intersection parameters",
            "triangle-plane clipping",
            "slab interval clipping for boxes",
            "sphere, cylinder, cone, and torus section diagnostics"
        ],
        "checks": [
            "reported intersection points satisfy both object equations",
            "ray-box entry parameter is no larger than the exit parameter",
            "triangle-plane clipped vertices lie in the plane within tolerance",
            "SAT overlap decisions are invariant under swapping objects"
        ]
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
            "small utilities are valuable when they expose sign conventions and units"
        ],
        "visuals": [
            "point projection onto a plane",
            "vector projection and rejection",
            "line-plane and plane-plane angle panel",
            "plane through three points with normal orientation"
        ],
        "checks": [
            "projection residual is parallel to the plane normal",
            "projected vectors are perpendicular to the normal",
            "angle calculations are unchanged by vector scaling",
            "three-point plane equation vanishes at all three inputs"
        ]
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
            "area, volume, and bounding primitives are diagnostics for the geometry pipeline"
        ],
        "visuals": [
            "BSP partitioning trace",
            "point-in-polygon ray parity and winding comparison",
            "convex hull and Delaunay dual panel",
            "minimum bounding rectangle and circle"
        ],
        "checks": [
            "hull vertices contain all points on the nonpositive side of each edge",
            "Delaunay triangles satisfy an empty-circumcircle sample check",
            "polygon area is invariant under cyclic vertex shifts",
            "bounding primitives contain all input points"
        ]
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
            "fitting routines should report both model parameters and geometric residuals"
        ],
        "visuals": [
            "Gaussian elimination and conditioning",
            "stable quadratic formula comparison",
            "QR, SVD, and polar decomposition geometry",
            "root-finding and minimization traces"
        ],
        "checks": [
            "decomposition reconstructions match the original matrix",
            "stable roots have smaller residuals for cancellation cases",
            "least-squares fitted primitives reduce orthogonal residual",
            "subdivision samples respect the selected stopping rule"
        ]
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
            "derivatives and integrals explain how circular motion becomes curvature and arc length"
        ],
        "visuals": [
            "unit circle with sine and cosine projections",
            "trig function graphs and phase shifts",
            "law of cosines triangle lab",
            "inverse-branch comparison"
        ],
        "checks": [
            "sin squared plus cos squared is one on sampled angles",
            "law-of-cosines reconstruction matches side lengths",
            "atan2 branch recovers the correct quadrant",
            "finite-difference derivatives match analytic derivatives"
        ]
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
            "primitive formulas should be checked against sampled geometry, not trusted as isolated text"
        ],
        "visuals": [
            "triangle notation and area formulas",
            "quadrilateral decomposition",
            "circle sector and segment formulas",
            "sphere and torus parameter atlas"
        ],
        "checks": [
            "triangle area agrees between determinant and Heron formulas",
            "circle sector area scales linearly with angle",
            "box, prism, pyramid, cylinder, cone, sphere, and torus dimensions are positive",
            "sampled torus surface area approximates the analytic expression"
        ]
    }
]

SMOKE_NOTEBOOKS = {
    "00-book-index.ipynb",
    "01-introduction.ipynb",
    "02-matrices-and-linear-systems.ipynb",
    "05-geometric-primitives-in-2d.ipynb",
    "07-intersection-in-2d.ipynb",
    "09-geometric-primitives-in-3d.ipynb",
    "11-intersection-in-3d.ipynb",
    "13-computational-geometry-topics.ipynb",
    "appendix-a-numerical-methods.ipynb",
}

def canonical_entries() -> list[dict]:
    return list(ENTRIES)

def parts() -> list[dict]:
    return list(PARTS)
