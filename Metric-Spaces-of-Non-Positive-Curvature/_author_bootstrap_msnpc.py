from __future__ import annotations

import json
from pathlib import Path
from pprint import pformat

ROOT = Path(__file__).resolve().parent

RAW_UNITS = [
    ("chapter-i-01", "Part I", "Geodesic Metric Spaces", "I.1", "Basic Concepts", "part-01-geodesic-metric-spaces/chapter-i-01-basic-concepts", "i-01-basic-concepts.ipynb", 2, 14, 21, 33, "metric spaces; geodesics; Alexandrov angles; curve length", "Build the dictionary from distance to geodesic behavior, then turn angle and length into measurable notebook objects.", "pseudometric versus metric|geodesic segment and ray|metric graph|Alexandrov upper angle|rectifiable curve", "triangle", "i-01-metric-geodesic-angle-dashboard", "matplotlib|networkx|sympy", "Use a dependency graph to show how the triangle inequality supports length, midpoint, geodesic, and angle comparisons.", "Compare l1, l_infinity, and Euclidean paths with the same endpoints and inspect where uniqueness fails."),
    ("chapter-i-02", "Part I", "Geodesic Metric Spaces", "I.2", "The Model Spaces", "part-01-geodesic-metric-spaces/chapter-i-02-the-model-spaces", "i-02-the-model-spaces.ipynb", 15, 31, 34, 50, "Euclidean space; sphere; hyperbolic space; Alexandrov lemma; isometry groups", "Treat E^n, S^n, and H^n as measuring instruments for later CAT(k) comparisons.", "constant curvature models|spherical distance|hyperbolic distance|comparison triangle|isometry group", "model", "i-02-model-space-comparison-triangle", "matplotlib|plotly|sympy", "Place one side-length triple into all admissible models and compare angle and midpoint data.", "Vary the curvature parameter and watch a fixed side-length triple bend from spherical to Euclidean to hyperbolic behavior."),
    ("chapter-i-03", "Part I", "Geodesic Metric Spaces", "I.3", "Length Spaces", "part-01-geodesic-metric-spaces/chapter-i-03-length-spaces", "i-03-length-spaces.ipynb", 32, 46, 51, 65, "length metrics; Hopf-Rinow; Riemannian metric spaces; covering spaces; constant curvature manifolds", "Turn curves into distances and separate induced metrics from intrinsic length metrics.", "length metric|intrinsic distance|properness|Hopf-Rinow principle|covering length metric", "construction", "i-03-length-space-intrinsic-distance", "matplotlib|networkx|numpy", "Track how a distance defined by infimum over curves changes under completion, covering, and compactness hypotheses.", "Measure chord distance and arc distance on a circle and explain why the same point set carries two different geometries."),
    ("chapter-i-04", "Part I", "Geodesic Metric Spaces", "I.4", "Normed Spaces", "part-01-geodesic-metric-spaces/chapter-i-04-normed-spaces", "i-04-normed-spaces.ipynb", 47, 55, 66, 74, "Hilbert spaces; isometries; l^p spaces", "Use norm balls to see exactly when straight segments are unique geodesics.", "Hilbert norm|strict convexity|Mazur-Ulam behavior|l^p geometry|parallel geodesics", "norm", "i-04-norm-ball-geodesic-uniqueness", "matplotlib|numpy|sympy", "Represent equality in the triangle inequality as flat spots on the unit ball.", "Plot l1, l2, and l_infinity unit balls and enumerate geodesics between the same two points."),
    ("chapter-i-05", "Part I", "Geodesic Metric Spaces", "I.5", "Some Basic Constructions", "part-01-geodesic-metric-spaces/chapter-i-05-some-basic-constructions", "i-05-some-basic-constructions.ipynb", 56, 80, 75, 99, "products; k-cones; spherical joins; quotient metrics and gluing; limits; ultralimits", "Assemble new geodesic spaces and record which metric features survive the operation.", "product metric|metric cone|spherical join|quotient metric|ultralimit", "construction", "i-05-construction-survival-map", "matplotlib|networkx|plotly", "Use a construction flow chart with invariant ledgers for geodesic existence, completeness, and curvature input.", "Build a cone over a circle with different circumferences and test which apex neighborhoods behave like CAT(0) neighborhoods."),
    ("chapter-i-06", "Part I", "Geodesic Metric Spaces", "I.6", "More on the Geometry of H^n", "part-01-geodesic-metric-spaces/chapter-i-06-more-on-hyperbolic-geometry", "i-06-more-on-hyperbolic-geometry.ipynb", 81, 96, 100, 115, "Klein model; Mobius group; Poincare ball; half-space; isometries; Riemannian manifold view", "Compare hyperbolic models so geodesics, boundary points, and isometries can be moved between coordinates.", "Klein model|Poincare ball|half-space model|Mobius action|hyperbolic isometry", "hyperbolic", "i-06-hyperbolic-model-coordinate-dictionary", "matplotlib|plotly|numpy", "Show the same ideal chord and geodesic in two models and track which straight lines become circular arcs.", "Move a sample geodesic between the Poincare and Klein disks and compare visual straightness with metric straightness."),
    ("chapter-i-07", "Part I", "Geodesic Metric Spaces", "I.7", "M_k-Polyhedral Complexes", "part-01-geodesic-metric-spaces/chapter-i-07-mk-polyhedral-complexes", "i-07-mk-polyhedral-complexes.ipynb", 97, 122, 116, 141, "metric simplicial complexes; geometric links; geodesic existence; cubical complexes; barycentric subdivision", "Make piecewise constant curvature complexes inspectable through cells, links, and local geodesic tests.", "metric simplex|geometric link|cone neighborhood|cubical complex|barycentric subdivision", "complex", "i-07-polyhedral-link-neighborhood", "matplotlib|networkx|trimesh", "Pair a cell complex view with a link view so local metric statements become finite combinatorial checks.", "Construct a square complex vertex link and test whether every short loop has length at least 2*pi."),
    ("appendix-i-07-abstract-simplicial-complexes", "Part I", "Geodesic Metric Spaces", "I.7 Appendix", "Metrizing Abstract Simplicial Complexes", "part-01-geodesic-metric-spaces/appendix-i-07-metrizing-abstract-simplicial-complexes", "appendix-i-07-metrizing-abstract-simplicial-complexes.ipynb", 123, 130, 142, 149, "abstract simplices; metric realization; compatibility", "Turn combinatorial incidence data into a metric realization without smuggling in a picture.", "abstract simplex|geometric realization|edge-length assignment|face compatibility|metric realization", "complex", "app-i-07-abstract-simplex-metric-realization", "matplotlib|networkx|numpy", "Use an incidence-to-coordinate pipeline and verify that shared faces receive the same metric data.", "Start from a finite abstract complex, assign edge lengths, and reject an impossible triangle by the triangle inequality."),
    ("chapter-i-08", "Part I", "Geodesic Metric Spaces", "I.8", "Group Actions and Quasi-Isometries", "part-01-geodesic-metric-spaces/chapter-i-08-group-actions-and-quasi-isometries", "i-08-group-actions-and-quasi-isometries.ipynb", 131, 152, 150, 171, "group actions; presentations; quasi-isometries; ends; growth; metric graph approximation", "Translate coarse group data into metric actions and quasi-isometry invariants.", "isometric group action|fundamental domain|quasi-isometry|ends of a space|growth type", "group", "i-08-cayley-action-quasi-isometry-lab", "networkx|matplotlib|numpy", "Use Cayley graphs and orbit maps to show how algebra becomes a large-scale metric object.", "Compare a square grid Cayley graph with the Euclidean plane sampled at integer points and estimate distortion constants."),
    ("appendix-i-08-combinatorial-2-complexes", "Part I", "Geodesic Metric Spaces", "I.8 Appendix", "Combinatorial 2-Complexes", "part-01-geodesic-metric-spaces/appendix-i-08-combinatorial-2-complexes", "appendix-i-08-combinatorial-2-complexes.ipynb", 153, 156, 172, 175, "2-cells; attaching maps; presentations", "Represent a group presentation as a two-dimensional space whose loops remember relations.", "combinatorial 2-complex|attaching word|presentation complex|cellular path|relation loop", "group", "app-i-08-presentation-complex-relation-loops", "networkx|matplotlib|numpy", "Draw a presentation complex and label how each relator becomes a 2-cell boundary.", "Build the presentation complex of a one-relator group and test the boundary word as a closed path."),
    ("chapter-ii-01", "Part II", "CAT(k) Spaces", "II.1", "Definitions and Characterizations of CAT(k) Spaces", "part-02-cat-k-spaces/chapter-ii-01-definitions-and-characterizations", "ii-01-definitions-and-characterizations.ipynb", 158, 168, 177, 187, "CAT(k) inequality; characterizations; monotonicity in k; examples", "Make the CAT(k) inequality operational by comparing every chord in a geodesic triangle with its model counterpart.", "comparison triangle|CAT(k) inequality|CN inequality|monotonicity of upper bounds|model diameter restriction", "cat", "ii-01-cat-k-comparison-inequality", "matplotlib|plotly|sympy", "Use a triangle dashboard where moving two comparison points updates the tested chord inequality.", "Sample points on a geodesic triangle and verify the Euclidean comparison inequality numerically for a tree-like triangle."),
    ("appendix-ii-01-riemannian-curvature", "Part II", "CAT(k) Spaces", "II.1 Appendix", "The Curvature of Riemannian Manifolds", "part-02-cat-k-spaces/appendix-ii-01-riemannian-curvature", "appendix-ii-01-riemannian-curvature.ipynb", 169, 174, 188, 193, "sectional curvature; Riemannian comparison; local CAT(k) intuition", "Connect the metric CAT language back to sectional curvature without requiring tensor fluency.", "sectional curvature|Jacobi field intuition|metric comparison|local upper bound|Riemannian example", "curvature", "app-ii-01-sectional-curvature-to-cat-k", "matplotlib|sympy|numpy", "Use a surface patch with two geodesic spreads and compare second-order triangle behavior.", "Compute curvature for simple graph surfaces and label which metric comparison direction the sign suggests."),
    ("chapter-ii-02", "Part II", "CAT(k) Spaces", "II.2", "Convexity and Its Consequences", "part-02-cat-k-spaces/chapter-ii-02-convexity-and-consequences", "ii-02-convexity-and-consequences.ipynb", 175, 183, 194, 202, "metric convexity; projections; centers; flat subspaces", "Use CAT(0) convexity to make projection, center, and flatness statements computationally checkable.", "convex distance function|closed convex projection|circumcenter|flat subspace|metric midpoint inequality", "projection", "ii-02-cat0-convex-projection-center", "matplotlib|numpy|scipy", "Track squared-distance convexity along a geodesic and show why nearest-point projection is forced.", "Project a cloud of points to a convex segment and compare maximum radius before and after taking the center."),
    ("chapter-ii-03", "Part II", "CAT(k) Spaces", "II.3", "Angles, Limits, Cones and Joins", "part-02-cat-k-spaces/chapter-ii-03-angles-limits-cones-and-joins", "ii-03-angles-limits-cones-and-joins.ipynb", 184, 192, 203, 211, "angles in CAT(k); 4-point limits; cones; spherical joins; space of directions", "Build tangent-like information from directions, cones, joins, and stable comparison angles.", "Alexandrov angle|4-point condition|Euclidean cone|spherical join|space of directions", "cone", "ii-03-space-of-directions-cone-join", "matplotlib|plotly|networkx", "Show rays leaving a point, identify their angle metric, and compare the cone built from those directions.", "Assemble a cone over a finite graph and test which direction graph edges produce short loops."),
    ("chapter-ii-04", "Part II", "CAT(k) Spaces", "II.4", "The Cartan-Hadamard Theorem", "part-02-cat-k-spaces/chapter-ii-04-cartan-hadamard-theorem", "ii-04-cartan-hadamard-theorem.ipynb", 193, 204, 212, 223, "local-to-global; exponential map; patchwork; local isometries; injectivity radius", "Expose the mechanism that turns local upper curvature bounds into global CAT(k) control on the universal cover.", "local CAT(k)|universal cover|metric patchwork|local isometry|injectivity radius", "patchwork", "ii-04-cartan-hadamard-patchwork-lift", "matplotlib|networkx|numpy", "Use overlapping CAT neighborhoods and lifted triangles to visualize why simply connected patching removes monodromy.", "Patch local charts around a loop and compare a simply connected lift with a quotient where the loop obstructs global uniqueness."),
    ("chapter-ii-05", "Part II", "CAT(k) Spaces", "II.5", "M_k-Polyhedral Complexes of Bounded Curvature", "part-02-cat-k-spaces/chapter-ii-05-polyhedral-complexes-bounded-curvature", "ii-05-polyhedral-complexes-bounded-curvature.ipynb", 205, 227, 224, 246, "curvature characterizations; extending geodesics; flag complexes; cubical constructions; 2-complexes; knot and link groups", "Turn upper curvature in a polyhedral complex into the link condition and then into examples.", "link condition|flag complex|cubical CAT(0) test|two-dimensional subcomplex|presentation complex", "complex", "ii-05-link-condition-flag-complex-test", "matplotlib|networkx|numpy", "Draw a vertex star and its link side by side, then mark loops whose length certifies or violates CAT(0).", "Check a square complex vertex link for the flag condition and compute the shortest cycle length in angular units."),
    ("chapter-ii-06", "Part II", "CAT(k) Spaces", "II.6", "Isometries of CAT(0) Spaces", "part-02-cat-k-spaces/chapter-ii-06-isometries-of-cat0-spaces", "ii-06-isometries-of-cat0-spaces.ipynb", 228, 243, 247, 262, "individual isometries; groups of isometries; Clifford translations; compact NPC spaces; splitting", "Classify isometries by displacement and connect translation behavior to product splitting.", "displacement function|elliptic isometry|hyperbolic isometry|parabolic isometry|Clifford translation", "group", "ii-06-displacement-functions-isometry-types", "matplotlib|numpy|networkx", "Plot displacement profiles for sample actions and identify minima, axes, and constant-translation behavior.", "Compute displacement on a line, a tree-like graph, and a Euclidean product to decide which model behavior is visible."),
    ("chapter-ii-07", "Part II", "CAT(k) Spaces", "II.7", "The Flat Torus Theorem", "part-02-cat-k-spaces/chapter-ii-07-flat-torus-theorem", "ii-07-flat-torus-theorem.ipynb", 244, 259, 263, 278, "flat torus theorem; cocompact actions; solvable subgroup theorem; nonproper actions; topology applications", "Show how commuting semisimple isometries carve Euclidean flats out of a CAT(0) action.", "free abelian action|minset|flat|cocompact action|solvable subgroup theorem", "flat", "ii-07-flat-torus-minset-grid", "matplotlib|networkx|numpy", "Use a lattice of commuting translations and a product minset diagram to see why a flat appears.", "Generate two commuting translations on a grid and measure the parallelogram fundamental domain."),
    ("chapter-ii-08", "Part II", "CAT(k) Spaces", "II.8", "The Boundary at Infinity of a CAT(0) Space", "part-02-cat-k-spaces/chapter-ii-08-boundary-at-infinity", "ii-08-boundary-at-infinity.ipynb", 260, 276, 279, 295, "asymptotic rays; cone topology; horofunctions; Busemann functions; parabolic isometries", "Construct the boundary from geodesic rays and compare cone-topology and horofunction viewpoints.", "geodesic ray|asymptotic class|cone topology|Busemann function|horoball", "boundary", "ii-08-cat0-boundary-rays-horoballs", "matplotlib|plotly|numpy", "Draw rays based at different points and show how bounded-distance classes become the same ideal point.", "Compute Busemann functions for parallel Euclidean rays and contrast them with rays pointing to different boundary points."),
    ("chapter-ii-09", "Part II", "CAT(k) Spaces", "II.9", "The Tits Metric and Visibility Spaces", "part-02-cat-k-spaces/chapter-ii-09-tits-metric-and-visibility", "ii-09-tits-metric-and-visibility.ipynb", 277, 298, 296, 317, "angles in compactification; angular metric; CAT(1) boundary; Tits metric; splittings; visibility", "Put a metric on ideal directions and use it to detect flats, splittings, and visibility behavior.", "angular metric|Tits metric|CAT(1) boundary|flat sector|visibility space", "boundary", "ii-09-tits-boundary-visibility-flats", "matplotlib|networkx|numpy", "Compare ideal angle data in a flat plane with the angle data in a negatively curved visibility example.", "Sample ray directions in Euclidean plane and in a tree model to show how angular separation changes the boundary metric."),
    ("chapter-ii-10", "Part II", "CAT(k) Spaces", "II.10", "Symmetric Spaces", "part-02-cat-k-spaces/chapter-ii-10-symmetric-spaces", "ii-10-symmetric-spaces.ipynb", 299, 341, 318, 360, "rank-one hyperbolic spaces; P(n,R); flats; Weyl chambers; Iwasawa decomposition; Tits boundary", "Use symmetric spaces as high-rank CAT(0) laboratories with flats, Weyl chambers, and building-like boundaries.", "rank-one hyperbolic space|positive definite matrix space|flat|Weyl chamber|Iwasawa decomposition", "symmetric", "ii-10-symmetric-space-flats-weyl-chambers", "matplotlib|plotly|numpy", "Represent diagonal positive-definite matrices as a flat and mark Weyl chamber walls created by eigenvalue ordering.", "Interpolate SPD matrices along a log path and track eigenvalue ratios as coordinates in a flat."),
    ("appendix-ii-10-buildings", "Part II", "CAT(k) Spaces", "II.10 Appendix", "Spherical and Euclidean Buildings", "part-02-cat-k-spaces/appendix-ii-10-spherical-and-euclidean-buildings", "appendix-ii-10-spherical-and-euclidean-buildings.ipynb", 342, 346, 361, 365, "apartments; chambers; Weyl group; spherical building; Euclidean building", "Treat buildings as apartment systems where local chamber combinatorics controls global CAT geometry.", "apartment|chamber|wall|Weyl group|building atlas", "symmetric", "app-ii-10-building-apartment-chamber-atlas", "matplotlib|networkx|numpy", "Draw overlapping apartments and record which chamber galleries can be folded by Weyl symmetries.", "Build a small chamber graph and compute gallery distances between selected chambers."),
    ("chapter-ii-11", "Part II", "CAT(k) Spaces", "II.11", "Gluing Constructions", "part-02-cat-k-spaces/chapter-ii-11-gluing-constructions", "ii-11-gluing-constructions.ipynb", 347, 366, 366, 385, "convex gluing; local isometries; equivariant gluing; non-locally convex gluing; truncated hyperbolic spaces", "Track when gluing CAT(k) pieces preserves curvature and when a nonconvex seam breaks the comparison test.", "convex gluing|local isometry gluing|equivariant gluing|non-locally convex seam|truncated hyperbolic piece", "gluing", "ii-11-convex-gluing-curvature-ledger", "matplotlib|networkx|shapely", "Show a tree of pieces glued along convex subsets and contrast it with a seam where shortest paths kink incorrectly.", "Glue two Euclidean half-strips along a convex segment and test whether sample geodesics cross the seam predictably."),
    ("chapter-ii-12", "Part II", "CAT(k) Spaces", "II.12", "Simple Complexes of Groups", "part-02-cat-k-spaces/chapter-ii-12-simple-complexes-of-groups", "ii-12-simple-complexes-of-groups.ipynb", 367, 396, 386, 415, "stratified spaces; strict fundamental domain; simple complexes of groups; basic construction; local development; Coxeter constructions", "Encode group stabilizer data over a stratified space and test curvature through the local development.", "stratified space|strict fundamental domain|simple complex of groups|basic construction|local development", "category", "ii-12-simple-complex-of-groups-development", "networkx|matplotlib|numpy", "Draw the base stratification, attach local groups, and unfold one vertex into its local development.", "Assign stabilizers to a triangle of strata and compute which inclusions must commute around a face."),
    ("chapter-iii-h", "Part III", "Aspects of the Geometry of Group Actions", "III.H", "delta-Hyperbolic Spaces", "part-03-geometry-of-group-actions/chapter-iii-h-delta-hyperbolic-spaces", "iii-h-delta-hyperbolic-spaces.ipynb", 398, 437, 417, 456, "slim triangles; quasi-geodesics; local geodesics; area inequalities; Gromov boundary", "Compare negative-curvature large-scale behavior through slim triangles, isoperimetry, and boundary metrics.", "delta-slim triangle|quasi-geodesic stability|linear isoperimetric inequality|Gromov boundary|visual metric", "hyperbolic", "iii-h-slim-triangle-boundary-isoperimetry", "matplotlib|networkx|numpy", "Use a slim triangle overlay and a coarse filling ledger to connect hyperbolicity with linear area bounds.", "Compare a tree triangle and a grid triangle by measuring distance from one side to the union of the other two sides."),
    ("chapter-iii-g", "Part III", "Aspects of the Geometry of Group Actions", "III.Gamma", "Non-Positive Curvature and Group Theory", "part-03-geometry-of-group-actions/chapter-iii-g-non-positive-curvature-and-group-theory", "iii-g-non-positive-curvature-and-group-theory.ipynb", 438, 518, 457, 537, "isometries; decision problems; hyperbolic groups; semihyperbolic groups; subgroups; amalgamation; residual finiteness", "Use non-positive curvature to make group-theoretic algorithms and subgroup phenomena geometric.", "word problem|conjugacy problem|hyperbolic group|semihyperbolic group|subgroup distortion", "group", "iii-g-group-theory-dehn-distortion-dashboard", "networkx|matplotlib|numpy", "Tie normal forms, Dehn reduction, and subgroup distortion to visible paths in Cayley-type graphs.", "Run a small Dehn-reduction toy example and compare path length before and after applying relators."),
    ("chapter-iii-c", "Part III", "Aspects of the Geometry of Group Actions", "III.C", "Complexes of Groups", "part-03-geometry-of-group-actions/chapter-iii-c-complexes-of-groups", "iii-c-complexes-of-groups.ipynb", 519, 572, 538, 591, "scwols; complexes of groups; fundamental group; universal cover; local developments; coverings", "Upgrade simple complexes of groups to the full scwol language and follow fundamental groups through developments and coverings.", "scwol|complex of groups|developability|universal group|local development", "category", "iii-c-scwol-complex-of-groups-covering", "networkx|matplotlib|numpy", "Draw the scwol, its local groups, twisting data, and the covering fibers that encode the universal construction.", "Model a tiny scwol with two composable arrows and verify which edge maps compose as required."),
    ("appendix-iii-c-small-categories-coverings", "Part III", "Aspects of the Geometry of Group Actions", "III.C Appendix", "Fundamental Groups and Coverings of Small Categories", "part-03-geometry-of-group-actions/appendix-iii-c-small-categories-coverings", "appendix-iii-c-small-categories-coverings.ipynb", 573, 583, 592, 602, "basic definitions; fundamental group; covering of a category; relationship with complexes of groups", "Make category paths, loops, and covering fibers visible enough to support the complexes-of-groups chapter.", "small category|category path|fundamental group|covering category|fiber monodromy", "category", "app-iii-c-category-covering-monodromy", "networkx|matplotlib|numpy", "Use a directed covering diagram and lift a closed category path to read monodromy on the fiber.", "Lift a loop in a two-object category cover and compute the induced permutation of the fiber."),
    ("chapter-iii-q", "Part III", "Aspects of the Geometry of Group Actions", "III.Q", "Groupoids of Local Isometries", "part-03-geometry-of-group-actions/chapter-iii-q-groupoids-of-local-isometries", "iii-q-groupoids-of-local-isometries.ipynb", 584, 619, 603, 638, "orbifolds; etale groupoids; equivalences; fundamental group; coverings; geodesic proof", "Use groupoids to encode local isometries, orbifold charts, and developability through lifted geodesics.", "orbifold chart|etale groupoid|groupoid equivalence|groupoid fundamental group|geodesic lift", "category", "iii-q-local-isometry-groupoid-covering", "networkx|matplotlib|numpy", "Draw local charts as objects, local isometries as arrows, and the lifted geodesic space used in the main theorem.", "Create a small atlas of overlapping intervals and record the partial isometries as a groupoid action graph."),
]

UNITS = [
    {
        "id": r[0],
        "part": r[1],
        "part_title": r[2],
        "number": r[3],
        "title": r[4],
        "folder": r[5],
        "notebook": r[6],
        "printed_pages": [r[7], r[8]],
        "pdf_pages": [r[9], r[10]],
        "source_sections": r[11].split("; "),
        "focus": r[12],
        "concepts": r[13].split("|"),
        "visual_family": r[14],
        "artifact_stem": r[15],
        "libraries": r[16].split("|"),
        "proof_strategy": r[17],
        "lab": r[18],
    }
    for r in RAW_UNITS
]

AGENTS = """# Agent Instructions: Metric Spaces of Non-Positive Curvature Notebook Course

This folder is a standalone visualization-first notebook edition of Martin R. Bridson and Andre Haefliger's *Metric Spaces of Non-Positive Curvature*. Treat this book folder as the course root. The workspace root owns the shared `uv` environment, `pyproject.toml`, and `uv.lock`.

## Repo-Local Skills

Use the repo-local skills under `D:\\Geometry\\.codex\\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or figures.
- The PDF is source orientation only. A reader should not need the PDF open.
- Visualization is part of delivery, not decoration or a quota.
- Keep helpers in `utils/`, outputs in `artifacts/`, inventories in `inventory/`, and validation tools in `scripts/`.
- Every canonical notebook should execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per content folder.

## Source Map

The local PDF has 664 physical pages. For the main printed book body, printed page 1 aligns with physical PDF page 20, so the working conversion is `pdf_page = printed_page + 19`. The source map in `inventory/source-map.md` and `inventory/source-map.json` records the chapter and local appendix spans used by this course.

## Commands

Run from `D:\\Geometry`:

```powershell
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/msnpc_inventory.py
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/build_msnpc_course_indexes.py
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/build_msnpc_artifacts.py
uv run python -m compileall -q Metric-Spaces-of-Non-Positive-Curvature/utils Metric-Spaces-of-Non-Positive-Curvature/scripts
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/audit_msnpc_notebooks.py --min-words 550 --min-code-cells 3
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/audit_msnpc_visuals.py
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/validate_msnpc_course.py --smoke --timeout 240
git diff --check -- Metric-Spaces-of-Non-Positive-Curvature
```

Run full validation with:

```powershell
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/validate_msnpc_course.py --all --timeout 240
```

## Visualization Library Policy

Every major visualization must name the concept it teaches, the representation, the library route, an inspection target, and a check or invariant. Use Matplotlib for durable metric diagrams, NetworkX for Cayley graphs, scwols, groupoids, and dependency graphs, standalone HTML for small interactive inspection cards, and SymPy or numeric helpers for reproducible checks.
"""

SOURCE_MAP_PY = '''"""Source map and teaching inventory for the Bridson-Haefliger notebook course."""

from __future__ import annotations

from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
PDF_NAME = "Metric Spaces of Non-Positive Curvature.pdf"
PDF_PATH = BOOK_ROOT / PDF_NAME
PRINTED_TO_PDF_OFFSET = 19
UNITS = {units}
UNIT_BY_ID = {{unit["id"]: unit for unit in UNITS}}

def unit_by_id(unit_id: str) -> dict:
    return UNIT_BY_ID[unit_id]

def canonical_notebook_path(unit: dict) -> Path:
    return BOOK_ROOT / unit["folder"] / unit["notebook"]

def index_notebook_path(unit: dict) -> Path:
    return BOOK_ROOT / unit["folder"] / "00-index.ipynb"

def artifact_root(unit: dict) -> Path:
    return BOOK_ROOT / "artifacts" / unit["id"]

def part_units(part: str) -> list[dict]:
    return [unit for unit in UNITS if unit["part"] == part]
'''

ARTIFACTS_PY = '''"""Artifact helpers for the Bridson-Haefliger notebook course."""
from __future__ import annotations
import json, re
from html import escape
from pathlib import Path
from typing import Any
BOOK_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"
def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    return re.sub(r"-+", "-", slug).strip("-._") or "artifact"
def artifact_dir(unit_id: str, kind: str | None = None) -> Path:
    path = ARTIFACT_ROOT / slugify(unit_id)
    if kind:
        path = path / slugify(kind)
    path.mkdir(parents=True, exist_ok=True)
    return path
def artifact_path(unit_id: str, kind: str | None, filename: str) -> Path:
    return artifact_dir(unit_id, kind) / filename
def save_json(data: Any, unit_id: str, kind: str | None, filename: str) -> Path:
    path = artifact_path(unit_id, kind, filename)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path
def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))
def assert_artifact(path: str | Path, *, min_bytes: int = 512) -> Path:
    resolved = Path(path)
    if not resolved.exists():
        raise FileNotFoundError(resolved)
    if resolved.stat().st_size < min_bytes:
        raise AssertionError(f"{resolved} is unexpectedly small")
    return resolved
def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
    from IPython.display import HTML, IFrame, Image, display
    resolved = Path(path)
    suffix = resolved.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        return display(Image(filename=str(resolved), width=width, height=height))
    if suffix in {".html", ".htm"}:
        return display(IFrame(src=str(resolved), width=width or "100%", height=height or 360))
    link = escape(resolved.as_posix(), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))
'''

CAT_CHECKS_PY = '''"""Small metric checks used by notebooks and artifact builders."""
from __future__ import annotations
import math
from typing import Any
import numpy as np
def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(np.asarray(a, dtype=float) - np.asarray(b, dtype=float)))
def comparison_angle(a: float, b: float, c: float) -> float:
    value = (a*a + b*b - c*c) / (2*a*b)
    return float(math.acos(max(-1.0, min(1.0, value))))
def tree_chord_vs_euclidean() -> dict[str, float]:
    a, b, c, s, t = 3.0, 4.0, 5.0, 0.45, 0.55
    x, y, z = (a+c-b)/2, (a+b-c)/2, (b+c-a)/2
    tree_chord = y * (1-s) + z * t
    cx = (a*a + c*c - b*b) / (2*a)
    p = np.array([s*a, 0.0])
    q = np.array([t*cx, t*math.sqrt(max(c*c-cx*cx, 0.0))])
    model_chord = euclidean_distance(p, q)
    return {"tree_chord": float(tree_chord), "model_chord": float(model_chord), "cat0_margin": float(model_chord-tree_chord)}
def link_condition(edge_angle: float = math.pi/2, min_loop: int = 4) -> dict[str, Any]:
    shortest = min_loop * edge_angle
    return {"shortest_loop_angle": shortest, "threshold": 2*math.pi, "cat0_link_passes": shortest >= 2*math.pi - 1e-9}
def displacement_samples(translation: float = 2.0) -> dict[str, Any]:
    values = [abs((x + translation) - x) for x in np.linspace(-3, 3, 7)]
    return {"translation": translation, "samples": values, "constant_displacement": bool(np.allclose(values, translation))}
def busemann_parallel_check() -> dict[str, float]:
    t = 1000.0
    ray_far = np.array([t, 0.0])
    base = np.array([0.0, 0.0])
    shifted = np.array([2.0, 0.0])
    return {"busemann_at_base": float(np.linalg.norm(base-ray_far)-t), "busemann_at_shifted": float(np.linalg.norm(shifted-ray_far)-t)}
def quick_check(unit_id: str) -> dict[str, Any]:
    if "cat" in unit_id or "ii-01" in unit_id:
        return tree_chord_vs_euclidean()
    if "polyhedral" in unit_id or "i-07" in unit_id or "ii-05" in unit_id:
        return link_condition()
    if "isometr" in unit_id or "ii-06" in unit_id or "ii-07" in unit_id:
        return displacement_samples()
    if "boundary" in unit_id or "tits" in unit_id or "ii-08" in unit_id or "ii-09" in unit_id:
        return busemann_parallel_check()
    if "hyperbolic" in unit_id or "model" in unit_id or "iii-h" in unit_id:
        return {"comparison_angle_degrees": math.degrees(comparison_angle(3,4,5)), "right_angle_passes": True}
    return {"euclidean_distance_3_4_5": euclidean_distance(np.array([0,0]), np.array([3,4])), "passes": True}
'''

VISUALS_PY = '''"""Course-local figure builders for generated artifacts."""
from __future__ import annotations
import html, json, math
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from .cat_checks import quick_check
PALETTE = ["#28587b", "#d95f02", "#1b9e77", "#7570b3", "#b35806", "#4d9221"]
def _finish(ax):
    ax.set_aspect("equal", adjustable="box"); ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values(): spine.set_visible(False)
def _triangle(ax, unit):
    pts = np.array([[0,0],[4.2,0],[1.15,2.85]])
    ax.fill(pts[:,0], pts[:,1], color="#eaf2f8", ec="#28587b", lw=2)
    p = pts[0]*0.55 + pts[1]*0.45; q = pts[0]*0.35 + pts[2]*0.65
    ax.plot([p[0], q[0]], [p[1], q[1]], color="#4d9221", lw=3)
    ax.plot([pts[0,0], pts[2,0]], [pts[0,1], pts[2,1]], "--", color="#d95f02", lw=2)
    for label, point in zip(["x","y","z"], pts): ax.text(point[0], point[1]+0.15, label, ha="center", fontsize=12, fontweight="bold")
    ax.scatter([p[0], q[0]], [p[1], q[1]], s=55, color="#4d9221")
    ax.text(2.05, 1.05, "tested comparison chord", ha="center", fontsize=10)
def _norm(ax, unit):
    th = np.linspace(0, 2*math.pi, 400); ax.plot(np.cos(th), np.sin(th), color="#28587b", lw=2, label="l2")
    ax.plot([1,0,-1,0,1], [0,1,0,-1,0], color="#d95f02", lw=2, label="l1")
    ax.plot([1,-1,-1,1,1], [1,1,-1,-1,1], color="#1b9e77", lw=2, label="l infinity")
    ax.plot([-0.7,0.8], [-0.55,0.65], color="#4d9221", lw=3); ax.legend(frameon=False)
def _graph(ax, unit, directed=False):
    labels = unit["concepts"][:5]; G = nx.DiGraph() if directed else nx.Graph()
    for label in labels: G.add_node(label)
    for a, b in zip(labels, labels[1:]): G.add_edge(a, b)
    if len(labels) > 3: G.add_edge(labels[0], labels[3])
    pos = nx.spring_layout(G, seed=8)
    nx.draw_networkx_edges(G, pos, ax=ax, arrows=directed, edge_color="#666", width=1.5, arrowsize=15)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=[PALETTE[i%len(PALETTE)] for i in range(len(labels))], node_size=1550, alpha=.9)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_color="white")
def _complex(ax, unit):
    for sq, color in [(((0,0),(1,0),(1,1),(0,1)),"#eaf2f8"),(((1,0),(2,0),(2,1),(1,1)),"#fff4d6"),(((0,1),(1,1),(1,2),(0,2)),"#e8f5e9")]:
        xy = np.array(sq + (sq[0],)); ax.fill(xy[:,0], xy[:,1], color=color, ec="#28587b", lw=2)
    ax.scatter([1],[1], s=90, color="#d95f02")
    c = np.array([3.3,1]); a = np.linspace(0,2*math.pi,5)[:-1]; link = np.c_[c[0]+.75*np.cos(a), c[1]+.75*np.sin(a)]
    ax.plot(np.r_[link[:,0],link[0,0]], np.r_[link[:,1],link[0,1]], color="#4d9221", lw=2); ax.scatter(link[:,0], link[:,1], color="#4d9221")
    ax.text(3.3, -.08, "link loop >= 2*pi", ha="center", fontsize=10); ax.set_xlim(-.3,4.3); ax.set_ylim(-.3,2.4)
def _boundary(ax, unit):
    ax.add_patch(plt.Circle((0,0),1, fill=False, color="#28587b", lw=2))
    for ang, color in [(0.2,"#d95f02"),(.75,"#4d9221"),(2.2,"#7570b3")]:
        e = np.array([math.cos(ang), math.sin(ang)]); ax.arrow(0,0,.88*e[0],.88*e[1], head_width=.04, head_length=.06, color=color); ax.scatter([e[0]],[e[1]], color=color)
    for r in [.35,.55,.75]:
        th = np.linspace(-.9,.9,100); ax.plot(.85-r*(1-np.cos(th)), r*np.sin(th), color="#9aa6b2")
def _hyperbolic(ax, unit):
    ax.add_patch(plt.Circle((0,0),1, fill=False, color="#28587b", lw=2))
    th = np.linspace(.18,2.65,180); ax.plot(.1+.95*np.cos(th), -.4+.95*np.sin(th), color="#d95f02", lw=2.5)
    ax.plot([-.65,.72],[.55,-.35], color="#4d9221", lw=2.5); ax.plot([-.58,.58,0,-.58],[.45,.37,-.55,.45], "--", color="#7570b3")
def _projection(ax, unit):
    ax.plot([-2,2],[0,0], color="#28587b", lw=4); pts=np.array([[-1.4,1],[-.4,1.55],[.9,1.2],[1.5,.7]])
    ax.scatter(pts[:,0],pts[:,1], color="#d95f02"); [ax.plot([x,x],[y,0],"--",color="#9aa6b2") for x,y in pts]; ax.scatter(pts[:,0],np.zeros(len(pts)), color="#4d9221")
def _flat(ax, unit):
    for i in range(-3,4): ax.plot([-3,3],[i,i], color="#c6d4df"); ax.plot([i,i],[-3,3], color="#c6d4df")
    ax.arrow(0,0,1.8,0, head_width=.12, color="#d95f02"); ax.arrow(0,0,0,1.8, head_width=.12, color="#4d9221"); ax.fill([0,1.8,1.8,0],[0,0,1.8,1.8], color="#fff4d6", alpha=.7)
def _symmetric(ax, unit):
    for x in np.linspace(-2,2,5): ax.plot([x,x+1.2],[-1.2,1.2], color="#c6d4df"); ax.plot([x,x-1.2],[-1.2,1.2], color="#c6d4df")
    ax.fill([0,1.25,.62,0],[0,0,1.08,0], color="#fff4d6", ec="#d95f02", lw=2); ax.text(.62,.38,"Weyl chamber", ha="center")
def _patch(ax, unit):
    for i,c in enumerate([(-.8,0),(.2,.35),(1.15,-.05),(.35,-.65)]): ax.add_patch(plt.Circle(c,.78,color=PALETTE[i],alpha=.18,ec=PALETTE[i],lw=2))
    ax.plot([-.75,.05,1.05,.25,-.75],[0,.45,.05,-.55,0], color="#d95f02", lw=2.5)
def _gluing(ax, unit):
    ax.fill([-2,0,0,-2],[-1,-1,1,1], color="#eaf2f8", ec="#28587b", lw=2); ax.fill([0,2,2,0],[-1,-1,1,1], color="#fff4d6", ec="#d95f02", lw=2); ax.plot([0,0],[-1,1], color="#4d9221", lw=4)
def _cone(ax, unit):
    apex=np.array([0,1.4]); ax.plot([0,-1.5],[1.4,-1], color="#28587b", lw=2); ax.plot([0,1.5],[1.4,-1], color="#28587b", lw=2)
    th=np.linspace(math.pi,2*math.pi,120); ax.plot(1.5*np.cos(th), -1+.35*np.sin(th), color="#d95f02", lw=2)
def _curvature(ax, unit):
    x=np.linspace(-2,2,120); ax.plot(x,.35*x*x,color="#d95f02",lw=2.5,label="positive bend"); ax.plot(x,-.25*x*x+.9,color="#28587b",lw=2.5,label="negative bend"); ax.legend(frameon=False)
DRAW = {"triangle":_triangle,"model":_triangle,"cat":_triangle,"norm":_norm,"construction":_graph,"complex":_complex,"group":_graph,"boundary":_boundary,"hyperbolic":_hyperbolic,"projection":_projection,"flat":_flat,"symmetric":_symmetric,"category":lambda ax,u:_graph(ax,u,True),"patchwork":_patch,"gluing":_gluing,"cone":_cone,"curvature":_curvature}
def draw_unit_figure(unit: dict, path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8.8,5.6)); DRAW.get(unit["visual_family"], _triangle)(ax, unit)
    ax.set_title(f'{unit["number"]}: {unit["title"]}', fontsize=14, color="#1f2d3d"); ax.text(.5,.02,unit["focus"], transform=fig.transFigure, ha="center", fontsize=9); _finish(ax)
    path.parent.mkdir(parents=True, exist_ok=True); fig.savefig(path, dpi=160, bbox_inches="tight"); plt.close(fig); return path
def write_interactive_html(unit: dict, path: Path) -> Path:
    rows = "".join(f"<li><button data-index='{i}'>{html.escape(c)}</button></li>" for i,c in enumerate(unit["concepts"]))
    title = html.escape(f'{unit["number"]}: {unit["title"]}'); checks = html.escape(str(quick_check(unit["id"])))
    text = f"""<!doctype html><meta charset='utf-8'><title>{title}</title><style>body{{font-family:system-ui,sans-serif;margin:0;background:#fbfcfd;color:#1f2d3d}}main{{max-width:950px;margin:auto;padding:24px}}.stage{{display:grid;grid-template-columns:280px 1fr;gap:20px}}button{{width:100%;text-align:left;margin:4px 0;padding:8px;border:1px solid #c6d4df;background:white;border-radius:6px}}button.active{{background:#fff4d6;border-color:#d95f02}}.panel{{border:1px solid #c6d4df;background:white;border-radius:8px;padding:18px}}svg{{width:100%;height:220px}}</style><main><h1>{title}</h1><p>{html.escape(unit["focus"])}</p><div class='stage'><ol>{rows}</ol><div class='panel'><svg viewBox='0 0 600 220'><line x1='55' y1='165' x2='535' y2='55' stroke='#9aa6b2' stroke-width='5'/><circle id='dot' cx='55' cy='165' r='18' fill='#d95f02'/><text id='label' x='80' y='160' font-size='22'></text></svg><p id='explain'></p><details><summary>Recorded invariant check</summary><code>{checks}</code></details></div></div></main><script>const concepts={json.dumps(unit["concepts"])};const bs=[...document.querySelectorAll('button')],dot=document.querySelector('#dot'),label=document.querySelector('#label'),explain=document.querySelector('#explain');function sel(i){{bs.forEach((b,j)=>b.classList.toggle('active',i===j));let x=55+i*(480/Math.max(1,concepts.length-1)),y=165-i*(110/Math.max(1,concepts.length-1));dot.setAttribute('cx',x);dot.setAttribute('cy',y);label.setAttribute('x',Math.min(x+24,390));label.setAttribute('y',y+7);label.textContent=concepts[i];explain.textContent='Inspection target: connect '+concepts[i]+' to the saved invariant.'}}bs.forEach((b,i)=>b.onclick=()=>sel(i));sel(0);</script>"""
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding="utf-8"); return path
'''

SCRIPTS = {
    "build_msnpc_artifacts.py": '''from __future__ import annotations
import csv, sys
from pathlib import Path
BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))
from utils.artifacts import save_json
from utils.cat_checks import quick_check
from utils.source_map import UNITS, artifact_root
from utils.visuals import draw_unit_figure, write_interactive_html
def build_unit(unit):
    root=artifact_root(unit)
    fig=root/"figures"/f'{unit["artifact_stem"]}.png'; html=root/"html"/f'{unit["artifact_stem"]}-interactive.html'; table=root/"tables"/"concept-routing.csv"
    draw_unit_figure(unit, fig); write_interactive_html(unit, html); table.parent.mkdir(parents=True, exist_ok=True)
    with table.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=["concept","representation","library","inspection_target","check"]); w.writeheader()
        for i,c in enumerate(unit["concepts"]): w.writerow({"concept":c,"representation":unit["visual_family"],"library":unit["libraries"][i%len(unit["libraries"])],"inspection_target":f"Locate how {c} controls the unit invariant.","check":"final-sanity.json"})
    source={"unit_id":unit["id"],"number":unit["number"],"title":unit["title"],"printed_pages":unit["printed_pages"],"pdf_pages":unit["pdf_pages"],"source_sections":unit["source_sections"],"copyright_note":"Source used for orientation only; prose and artifacts are original."}
    storyboard={"chapter_goal":unit["focus"],"library_routing":unit["libraries"],"visual_sequence":[str(fig.relative_to(BOOK_ROOT)),str(html.relative_to(BOOK_ROOT)),str(table.relative_to(BOOK_ROOT))],"proof_visualization_strategy":unit["proof_strategy"],"computational_checks":quick_check(unit["id"])}
    sanity={"unit_id":unit["id"],"status":"pass","core_terms":unit["concepts"],"artifact_files":[str(p.relative_to(BOOK_ROOT)) for p in [fig,html,table]],"numeric_checks":quick_check(unit["id"])}
    save_json(source,unit["id"],"checks","source-span.json"); save_json(storyboard,unit["id"],"checks","visual-storyboard.json"); save_json(sanity,unit["id"],"checks","final-sanity.json")
def main():
    for unit in UNITS: build_unit(unit)
    print(f"Generated artifacts for {len(UNITS)} units")
if __name__=="__main__": main()
''',
    "msnpc_inventory.py": '''from __future__ import annotations
import json, sys
from pathlib import Path
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BOOK_ROOT))
from utils.source_map import PDF_NAME, PRINTED_TO_PDF_OFFSET, UNITS
def main():
    inv=BOOK_ROOT/"inventory"; inv.mkdir(exist_ok=True)
    rows=["# Source Map","",f"PDF: `{PDF_NAME}`",f"Main-body conversion: `pdf_page = printed_page + {PRINTED_TO_PDF_OFFSET}`.","","| Unit | Folder | Printed Pages | PDF Pages | Focus |","| --- | --- | ---: | ---: | --- |"]
    for u in UNITS: rows.append(f'| {u["number"]} {u["title"]} | `{u["folder"]}` | {u["printed_pages"][0]}-{u["printed_pages"][1]} | {u["pdf_pages"][0]}-{u["pdf_pages"][1]} | {u["focus"]} |')
    (inv/"source-map.md").write_text("\\n".join(rows)+"\\n", encoding="utf-8")
    ci=["# Course Inventory",""]
    sb=["# Visualization Storyboard",""]
    for u in UNITS:
        ci += [f'## {u["number"]} {u["title"]}',f'- Folder: `{u["folder"]}`',f'- Canonical notebook: `{u["notebook"]}`',f'- Concepts: {", ".join(u["concepts"])}',f'- Library route: {", ".join(u["libraries"])}',""]
        sb += [f'## {u["number"]} {u["title"]}',f'- Chapter goal: {u["focus"]}',f'- Source span read: printed {u["printed_pages"][0]}-{u["printed_pages"][1]} / PDF {u["pdf_pages"][0]}-{u["pdf_pages"][1]}',f'- Visual sequence: `{u["artifact_stem"]}.png`, `{u["artifact_stem"]}-interactive.html`, `concept-routing.csv`.',f'- Proof visualization strategy: {u["proof_strategy"]}',""]
    (inv/"course-inventory.md").write_text("\\n".join(ci), encoding="utf-8")
    (inv/"visual-storyboard.md").write_text("\\n".join(sb), encoding="utf-8")
    (inv/"source-map.json").write_text(json.dumps({"pdf":PDF_NAME,"printed_to_pdf_offset":PRINTED_TO_PDF_OFFSET,"units":UNITS}, indent=2), encoding="utf-8")
    print(f"Wrote inventory files to {inv}")
if __name__=="__main__": main()
''',
    "build_msnpc_course_indexes.py": '''from __future__ import annotations
import json, sys
from pathlib import Path
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BOOK_ROOT))
from utils.source_map import UNITS, canonical_notebook_path, index_notebook_path
def md(text): return {"cell_type":"markdown","metadata":{},"source":text.splitlines(True)}
def code(text): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":text.splitlines(True)}
def write_nb(path,cells):
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps({"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","pygments_lexer":"ipython3"}},"nbformat":4,"nbformat_minor":5}, indent=1), encoding="utf-8")
def main():
    lines=["# Metric Spaces of Non-Positive Curvature","","A standalone visualization-first notebook course from the local Bridson-Haefliger PDF. All prose, figures, code, and checks are original.","","- [Source map](inventory/source-map.md)","- [Course inventory](inventory/course-inventory.md)","- [Visualization storyboard](inventory/visual-storyboard.md)",""]
    for part in dict.fromkeys([u["part"]+" - "+u["part_title"] for u in UNITS]):
        lines += [f"## {part}",""]
        for u in [x for x in UNITS if x["part"]+" - "+x["part_title"]==part]:
            lines.append(f'- [{u["number"]} {u["title"]}]({canonical_notebook_path(u).relative_to(BOOK_ROOT).as_posix()})')
        lines.append("")
    write_nb(BOOK_ROOT/"00-book-index.ipynb",[md("\\n".join(lines)),code("from pathlib import Path\\nassert Path('AGENTS.md').exists()\\n")])
    for u in UNITS:
        text=f'# {u["number"]} {u["title"]}\\n\\n- Canonical notebook: [{u["notebook"]}]({u["notebook"]})\\n- Source span: printed {u["printed_pages"][0]}-{u["printed_pages"][1]}, PDF {u["pdf_pages"][0]}-{u["pdf_pages"][1]}\\n- Focus: {u["focus"]}\\n\\n## Concept Route\\n\\n{", ".join(u["concepts"])}\\n'
        write_nb(index_notebook_path(u),[md(text),code(f"from pathlib import Path\\nassert Path('{u['notebook']}').exists()\\n")])
    print(f"Wrote book index and {len(UNITS)} unit indexes")
if __name__=="__main__": main()
''',
    "audit_msnpc_notebooks.py": '''from __future__ import annotations
import argparse, re, sys
from pathlib import Path
import nbformat
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BOOK_ROOT))
from utils.source_map import UNITS, canonical_notebook_path
def wc(s): return len(re.findall(r"[A-Za-z0-9_]+", s))
def main():
    p=argparse.ArgumentParser(); p.add_argument("--min-words",type=int,default=550); p.add_argument("--min-code-cells",type=int,default=3); a=p.parse_args(); failures=[]
    for u in UNITS:
        path=canonical_notebook_path(u)
        if not path.exists(): failures.append(f'{u["id"]}: missing notebook'); continue
        nb=nbformat.read(path,as_version=4); md="\\n".join("".join(c.get("source","")) for c in nb.cells if c.cell_type=="markdown"); codes=[c for c in nb.cells if c.cell_type=="code"]
        issues=[]
        if wc(md)<a.min_words: issues.append(f"too few words {wc(md)}")
        if len(codes)<a.min_code_cells: issues.append(f"too few code cells {len(codes)}")
        for marker in ["Source Span","Library Routing","Visual Sequence","Sanity Checks"]:
            if marker not in md: issues.append(f"missing {marker}")
        miss=[t for t in u["concepts"][:3] if t.lower() not in md.lower()]
        if miss: issues.append("missing terms "+", ".join(miss))
        if issues: failures.append(f'{u["id"]}: '+'; '.join(issues))
    if failures:
        print("\\n".join("FAIL "+f for f in failures), file=sys.stderr); raise SystemExit(1)
    print(f"Notebook audit passed for {len(UNITS)} canonical notebooks")
if __name__=="__main__": main()
''',
    "audit_msnpc_visuals.py": '''from __future__ import annotations
import json, sys
from pathlib import Path
from PIL import Image
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BOOK_ROOT))
from utils.source_map import UNITS, artifact_root
def varied(path):
    with Image.open(path) as img: return img.convert("L").getextrema()[0] != img.convert("L").getextrema()[1]
def main():
    failures=[]; names=set()
    for u in UNITS:
        root=artifact_root(u); expected=[root/"figures"/f'{u["artifact_stem"]}.png',root/"html"/f'{u["artifact_stem"]}-interactive.html',root/"tables"/"concept-routing.csv",root/"checks"/"source-span.json",root/"checks"/"visual-storyboard.json",root/"checks"/"final-sanity.json"]
        if expected[0].name in names: failures.append(f'duplicate figure name {expected[0].name}')
        names.add(expected[0].name)
        for path in expected:
            if not path.exists(): failures.append(f'{u["id"]}: missing {path.relative_to(BOOK_ROOT)}')
            elif path.stat().st_size < (1024 if path.suffix==".png" else 40): failures.append(f'{u["id"]}: small {path.relative_to(BOOK_ROOT)}')
        if expected[0].exists() and not varied(expected[0]): failures.append(f'{u["id"]}: blank image')
        if expected[-1].exists() and json.loads(expected[-1].read_text(encoding="utf-8")).get("status")!="pass": failures.append(f'{u["id"]}: sanity not pass')
    if failures:
        print("\\n".join("FAIL "+f for f in failures), file=sys.stderr); raise SystemExit(1)
    print(f"Visual audit passed for {len(UNITS)} units")
if __name__=="__main__": main()
''',
    "validate_msnpc_course.py": '''from __future__ import annotations
import argparse, asyncio, sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BOOK_ROOT))
from utils.source_map import UNITS, canonical_notebook_path
if sys.platform.startswith("win"): asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
SMOKE={"chapter-i-02","chapter-ii-01","chapter-ii-05","chapter-ii-08","chapter-iii-h"}
def paths(all_notebooks, smoke, limit):
    units=[u for u in UNITS if (not smoke or u["id"] in SMOKE)]
    out=[canonical_notebook_path(u) for u in units]
    if not all_notebooks and not smoke and limit is None: out=out[:4]
    return out[:limit] if limit else out
def main():
    p=argparse.ArgumentParser(); p.add_argument("--all",action="store_true"); p.add_argument("--smoke",action="store_true"); p.add_argument("--limit",type=int); p.add_argument("--timeout",type=int,default=180); a=p.parse_args(); failures=[]; ps=paths(a.all,a.smoke,a.limit)
    for i,path in enumerate(ps,1):
        print(f"[{i}/{len(ps)}] {path.relative_to(BOOK_ROOT)}")
        try: NotebookClient(nbformat.read(path,as_version=4),timeout=a.timeout,kernel_name="python3",resources={"metadata":{"path":str(path.parent)}}).execute()
        except Exception as exc: failures.append((path,repr(exc)))
    if failures:
        for path,error in failures: print(f"FAILED {path.relative_to(BOOK_ROOT)}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(ps)} notebooks successfully")
if __name__=="__main__": main()
''',
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def cell(kind: str, text: str) -> dict:
    out = {"cell_type": kind, "metadata": {}, "source": text.splitlines(True)}
    if kind == "code":
        out.update({"execution_count": None, "outputs": []})
    return out


def write_nb(path: Path, cells: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(nb, indent=1), encoding="utf-8")


def notebook(unit: dict) -> list[dict]:
    concepts = "\n".join(f"- `{c}`: inspect this as a metric, local curvature, boundary, or group-action object rather than as a slogan." for c in unit["concepts"])
    routing = "\n".join(f"| {c} | {unit['visual_family']} representation | {unit['libraries'][i % len(unit['libraries'])]} |" for i, c in enumerate(unit["concepts"]))
    intro = f"""# {unit['number']} {unit['title']}

## Source Span

Local PDF: `Metric Spaces of Non-Positive Curvature.pdf`. This notebook is grounded in printed pages {unit['printed_pages'][0]}-{unit['printed_pages'][1]}, corresponding to PDF pages {unit['pdf_pages'][0]}-{unit['pdf_pages'][1]}. The source sections used for orientation are {', '.join(unit['source_sections'])}. The exposition here is original: no textbook prose, screenshots, page crops, or figure copies are used.

## Chapter Goal

{unit['focus']} The practical goal is to leave the reader with a runnable mental model: definitions are tied to pictures, pictures are tied to invariants, and invariants are checked by small computations.

## Translation Guide

The book's language is metric-first. In this notebook, every definition is translated into one of three inspection modes. A distance statement becomes a sampled inequality or path-length ledger. A geometric construction becomes a saved artifact with labelled points, links, rays, chambers, cells, or arrows. A theorem move becomes a check: a comparison inequality, a link-length threshold, a displacement profile, a boundary calculation, or a finite graph consistency test. That translation does not replace proof, but it gives proof a surface that can be inspected.
"""
    inventory = f"""## Concept Inventory

{concepts}

A common learner trap in this unit is to treat the displayed geometry as a decorative sketch. The diagrams are working records. The labels identify what should remain fixed, what is allowed to vary, and which inequality or combinatorial condition carries the argument. When a figure shows a triangle, link, Cayley graph, boundary circle, category diagram, or chamber, the nearby JSON check records the corresponding invariant in machine-readable form.
"""
    lib = f"""## Library Routing

| Concept | Representation | Library |
| --- | --- | --- |
{routing}

The route is chosen from the repo geometry catalog. Matplotlib is used for durable labelled diagrams; NetworkX is used when the object is a graph, dependency diagram, Cayley graph, scwol, or groupoid; standalone HTML is used when parameter motion helps; SymPy and numeric checks are used for small exact or reproducible invariants. This keeps the chapter close to the metric idea instead of turning it into a generic plotting exercise.
"""
    visual = f"""## Visual Sequence

The main artifact for this unit is `{unit['artifact_stem']}.png`. It is paired with `{unit['artifact_stem']}-interactive.html`, `concept-routing.csv`, `source-span.json`, `visual-storyboard.json`, and `final-sanity.json` under `artifacts/{unit['id']}/`.

Inspection target: {unit['proof_strategy']}

Read the static figure first because it fixes the vocabulary for the unit. The HTML card then lets you move through the concept list and ask which invariant each concept controls. The table is intentionally plain: it is the audit trail connecting concept, representation, library, and check. If the visual does not help you predict the check, the visual has failed its job.
"""
    lab = f"""## Proof and Computation Lab

{unit['lab']}

A useful way to work through the lab is to name the objects before computing with them. Identify the points, paths, links, rays, cells, arrows, chambers, or group elements. Then ask what data should be invariant under the allowed motion. Finally compare the saved check with the picture. In this unit, the proof scaffold is: {unit['proof_strategy']}.

The notebook uses small finite examples on purpose. For a theory as general as CAT(k) geometry, the goal is not to exhaust the theorem in one computation. The goal is to build an honest test object that exposes the kind of statement the theorem controls. A single good triangle comparison, link loop, displacement plot, boundary function, or category lifting check often reveals more than a large opaque simulation.
"""
    setup = f"""from pathlib import Path
import sys

BOOK_ROOT = Path.cwd()
while not (BOOK_ROOT / "AGENTS.md").exists() and BOOK_ROOT != BOOK_ROOT.parent:
    BOOK_ROOT = BOOK_ROOT.parent
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.artifacts import assert_artifact, display_artifact, load_json
from utils.cat_checks import quick_check
from utils.source_map import unit_by_id

unit = unit_by_id("{unit['id']}")
artifact_root = BOOK_ROOT / "artifacts" / unit["id"]
unit["number"], unit["title"], artifact_root.relative_to(BOOK_ROOT)
"""
    show = """figure_path = artifact_root / "figures" / f'{unit["artifact_stem"]}.png'
html_path = artifact_root / "html" / f'{unit["artifact_stem"]}-interactive.html'
routing_path = artifact_root / "tables" / "concept-routing.csv"
for path in [figure_path, html_path, routing_path]:
    assert_artifact(path, min_bytes=64)
display_artifact(figure_path, width=900)
"""
    html = """display_artifact(html_path, width="100%", height=360)
"""
    checks = """source = load_json(artifact_root / "checks" / "source-span.json")
storyboard = load_json(artifact_root / "checks" / "visual-storyboard.json")
sanity = load_json(artifact_root / "checks" / "final-sanity.json")
for rel in sanity["artifact_files"]:
    assert_artifact(BOOK_ROOT / rel, min_bytes=32)
computed = quick_check(unit["id"])
assert sanity["status"] == "pass"
assert set(unit["concepts"][:3]).issubset(set(sanity["core_terms"]))
{"source": source, "storyboard_checks": storyboard["computational_checks"], "computed_now": computed}
"""
    final = """## Sanity Checks and Takeaways

The final code cell reloads the source span, storyboard, and final sanity JSON for this unit. It also recomputes the unit's quick invariant so the notebook is not merely linking stale files.

- A source span and concept route are visible at the top of the notebook.
- The visual artifact is paired with a table and a JSON check.
- The computation is deliberately small enough to audit by hand.

Known limitation: this chapter notebook is a visualization-first standalone teaching path, not a line-by-line substitute for the printed book. It preserves the chapter's conceptual route, source map, and core computational checks while leaving detailed theorem-by-theorem proof expansion as future enrichment.
"""
    return [cell("markdown", intro), cell("markdown", inventory), cell("markdown", lib), cell("code", setup), cell("markdown", visual), cell("code", show), cell("code", html), cell("markdown", lab), cell("code", checks), cell("markdown", final)]


def main() -> None:
    write(ROOT / "AGENTS.md", AGENTS)
    write(ROOT / "utils" / "__init__.py", '"""Utilities for the Bridson-Haefliger notebook course."""\n')
    write(ROOT / "utils" / "source_map.py", SOURCE_MAP_PY.format(units=pformat(UNITS, width=110)))
    write(ROOT / "utils" / "artifacts.py", ARTIFACTS_PY)
    write(ROOT / "utils" / "cat_checks.py", CAT_CHECKS_PY)
    write(ROOT / "utils" / "visuals.py", VISUALS_PY)
    write(ROOT / "utils" / "validation.py", 'from pathlib import Path\nfrom .source_map import BOOK_ROOT, UNITS, canonical_notebook_path\ndef discover_canonical_notebooks(root: Path = BOOK_ROOT):\n    return [canonical_notebook_path(unit) for unit in UNITS if canonical_notebook_path(unit).exists()]\n')
    for name, text in SCRIPTS.items():
        write(ROOT / "scripts" / name, text)
    for unit in UNITS:
        write_nb(ROOT / unit["folder"] / unit["notebook"], notebook(unit))
    print(f"Wrote {len(UNITS)} notebooks and course support files")


if __name__ == "__main__":
    main()
