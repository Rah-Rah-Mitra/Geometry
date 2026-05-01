"""Bootstrap the GMAM visualization-first notebook course.

The source PDF is an image-only scan. This script uses the inspected table of
contents and the agreed source map as orientation, then writes original
notebook scaffolds, helpers, validation scripts, and indexes.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import nbformat as nbf


BOOK_ROOT = Path(__file__).resolve().parents[1]
COURSE_TITLE = "Geometry: A Metric Approach with Models"


CHAPTERS = [
    {
        "number": 1,
        "title": "Preliminary Notions",
        "slug": "preliminary-notions",
        "folder": "chapter-01-preliminary-notions",
        "printed": "1-16",
        "pdf": "16-31",
        "sections": "1.1-1.3",
        "focus": "Axioms, models, equivalence relations, and functions.",
        "question": "How can geometry begin with undefined objects and still become a testable mathematical system?",
        "translation": [
            "An axiom system becomes a small rule checker: proposed worlds either pass or fail each rule.",
            "A model is an interpretation of primitive words such as point and line, not a drawing style.",
            "Equivalence relations are visual partitions of a set into disjoint classes.",
            "Functions are lookup rules with domain, codomain, image, fibers, and compositional behavior.",
        ],
        "visuals": [
            ("proof_graph", "axiom-dependency-graph.png", "Axiom dependency graph", "Inspect which ideas are primitive and which are built from them."),
            ("incidence", "finite-model-checker.png", "Finite models under the same rules", "Compare candidate worlds axiom by axiom instead of by appearance."),
            ("partition", "equivalence-partitions.png", "Equivalence classes as partitions", "Watch reflexive, symmetric, transitive data collapse into blocks."),
            ("mapping", "function-fibers-and-composition.png", "Function fibers and composition", "Find arrow collisions, uncovered codomain points, and composed outputs."),
        ],
        "lab": "Design a four-point incidence world, write three rules it should satisfy, then deliberately break one rule and record the smallest countermodel.",
        "pitfalls": [
            "A diagram is evidence only after the underlying incidence or metric relation is stated.",
            "A model may look unfamiliar and still satisfy the same formal rules.",
            "A function is not required to be a formula; a finite lookup table is already enough.",
        ],
        "takeaways": [
            "Axioms are hypotheses for a world, not decorations around a picture.",
            "Models let us test which statements follow from chosen rules.",
            "Equivalence classes and functions are the bookkeeping tools that later geometry uses constantly.",
        ],
    },
    {
        "number": 2,
        "title": "Incidence and Metric Geometry",
        "slug": "incidence-and-metric-geometry",
        "folder": "chapter-02-incidence-and-metric-geometry",
        "printed": "17-41",
        "pdf": "32-56",
        "sections": "2.1-2.3",
        "focus": "Incidence models, metric geometry, and special coordinate systems.",
        "question": "What changes when lines are first only incidence objects and then become objects with distance?",
        "translation": [
            "Incidence geometry records which points lie on which lines before measuring length.",
            "A metric adds a distance function with nonnegativity, symmetry, and triangle inequality checks.",
            "Coordinate systems turn geometric membership tests into equations or predicates.",
            "Euclidean, Poincare, and spherical examples separate visual intuition from formal rules.",
        ],
        "visuals": [
            ("incidence", "incidence-models-side-by-side.png", "Finite incidence models", "Compare Cartesian, finite, and spherical line membership."),
            ("metric", "metric-balls-compare.png", "Metric balls in different models", "Observe how the same radius can mean different shapes."),
            ("coordinate", "coordinate-system-atlas.png", "Coordinate descriptions", "Trace one point through Cartesian, polar, and disk coordinates."),
            ("proof_graph", "metric-axiom-checks.png", "Metric axiom checks", "See which candidate distances pass symmetry and triangle inequality."),
        ],
        "lab": "Sample triples of points and test the triangle inequality for Euclidean distance and for a deliberately broken distance rule.",
        "pitfalls": [
            "Incidence alone does not provide length, angle, or betweenness.",
            "A coordinate formula can hide the geometry if its domain restrictions are ignored.",
            "A distance-looking expression is not a metric until the axioms are checked.",
        ],
        "takeaways": [
            "Incidence tells us what touches what; metrics tell us how far apart objects are.",
            "Coordinate systems are interfaces, not the geometry itself.",
            "Model comparison is the habit that makes non-Euclidean geometry credible.",
        ],
    },
    {
        "number": 3,
        "title": "Betweenness and Elementary Figures",
        "slug": "betweenness-and-elementary-figures",
        "folder": "chapter-03-betweenness-and-elementary-figures",
        "printed": "42-62",
        "pdf": "57-77",
        "sections": "3.1-3.4",
        "focus": "Alternative Cartesian descriptions, betweenness, segments, rays, angles, and triangles.",
        "question": "How do elementary figures become computable predicates rather than informal sketches?",
        "translation": [
            "A line can be implicit, parametric, two-point, or slope-intercept when the latter is legal.",
            "Betweenness is affine parameter membership in the closed interval from one endpoint to another.",
            "Segments and rays are line predicates plus parameter restrictions.",
            "Angles and triangles are built from rays, side segments, dot products, and area tests.",
        ],
        "visuals": [
            ("affine_line", "line-descriptions-and-edge-cases.png", "One line, many descriptions", "Check that formulas change while the point set stays fixed."),
            ("betweenness", "betweenness-parameter-interval.png", "Betweenness by affine parameter", "Locate points with t below, inside, and above the unit interval."),
            ("angle", "angles-from-rays.png", "Angles from two rays", "Compare dot-product and directed angle measurements."),
            ("area", "triangle-membership-barycentric.png", "Triangle membership by coordinates", "Classify interior, boundary, and exterior sample points."),
        ],
        "lab": "Move one vertex of a triangle onto the opposite side and record how area, barycentric signs, and betweenness tests change.",
        "pitfalls": [
            "Slope-intercept form loses vertical lines.",
            "Distance additivity is not enough without collinearity and order.",
            "A triangle degenerates when its signed area is zero, even if the labels still look triangular.",
        ],
        "takeaways": [
            "Elementary figures become robust when expressed as predicates.",
            "Parameter intervals unify lines, segments, and rays.",
            "Angle and triangle computations expose hidden endpoint and degeneracy assumptions.",
        ],
    },
    {
        "number": 4,
        "title": "Plane Separation",
        "slug": "plane-separation",
        "folder": "chapter-04-plane-separation",
        "printed": "63-89",
        "pdf": "78-104",
        "sections": "4.1-4.5",
        "focus": "Plane separation, Pasch geometries, interiors, crossbar theorem, and convex quadrilaterals.",
        "question": "What does a line do to a plane once we care about sides, crossings, and interiors?",
        "translation": [
            "A separating line becomes a sign test: points with opposite signs lie on opposite sides.",
            "Pasch-style reasoning is intersection bookkeeping inside triangles.",
            "Interiors are collections of side inequalities rather than shaded intuition.",
            "Convexity is tested by orientation signs and segment containment.",
        ],
        "visuals": [
            ("separation", "plane-separation-signs.png", "Line as a side classifier", "Inspect how a signed equation splits the plane."),
            ("pasch", "pasch-crossbar-intersections.png", "Pasch and crossbar intersections", "Track which side of a triangle a crossing must meet."),
            ("area", "convex-quadrilateral-tests.png", "Convex quadrilateral checks", "Compare orientation consistency in convex and nonconvex shapes."),
            ("proof_graph", "separation-proof-dependencies.png", "Separation proof dependencies", "See how side, interior, and crossing claims depend on one another."),
        ],
        "lab": "Randomly sample quadrilaterals, sort their vertices, and classify which ones pass the convex orientation test.",
        "pitfalls": [
            "Being visually inside a hand-drawn triangle must be replaced by three half-plane tests.",
            "A crossing claim depends on endpoints being on opposite sides.",
            "A quadrilateral can fail convexity even when its four sides are all drawn.",
        ],
        "takeaways": [
            "Plane separation converts topology-like language into sign computations.",
            "Pasch arguments become inspectable when the intersection data is explicit.",
            "Convexity is a global condition on all edges and diagonals.",
        ],
    },
    {
        "number": 5,
        "title": "Angle Measure",
        "slug": "angle-measure",
        "folder": "chapter-05-angle-measure",
        "printed": "90-123",
        "pdf": "105-138",
        "sections": "5.1-5.4",
        "focus": "Angle measure, Molton plane, perpendicularity, angle congruence, and Poincare angle measure.",
        "question": "Which parts of angle measurement are metric, which are model-dependent, and which survive conformal maps?",
        "translation": [
            "Angle measure comes from normalized direction vectors or tangent directions.",
            "The Molton plane is a warning that familiar drawings can carry unfamiliar line rules.",
            "Perpendicularity becomes a zero dot product or an orthogonal tangent condition.",
            "The Poincare disk preserves Euclidean angle between tangent directions even while changing distance.",
        ],
        "visuals": [
            ("angle", "angle-measure-from-directions.png", "Measuring an angle from directions", "Inspect ray directions, arc labels, and dot-product values."),
            ("molton", "molton-plane-bent-lines.png", "Molton plane line rules", "Notice how a changed line model disrupts ordinary angle intuition."),
            ("poincare", "poincare-conformal-angle.png", "Poincare angle from tangent directions", "Compare Euclidean tangent angle with disk-model angle."),
            ("proof_graph", "perpendicularity-congruence-checks.png", "Perpendicularity and congruence checks", "Follow which measurements stay invariant under rigid motion."),
        ],
        "lab": "Rotate one ray around a fixed vertex and record dot product, angle class, and perpendicular events.",
        "pitfalls": [
            "An angle is not the same object as the shaded wedge drawn near it.",
            "Perpendicularity is model-sensitive when the line model changes.",
            "Conformal angle preservation does not imply distance preservation.",
        ],
        "takeaways": [
            "Angle is a measurement of directions at a shared vertex.",
            "Changing the model can change what counts as a line or perpendicular.",
            "The Poincare model is especially useful because it is conformal.",
        ],
    },
    {
        "number": 6,
        "title": "Neutral Geometry",
        "slug": "neutral-geometry",
        "folder": "chapter-06-neutral-geometry",
        "printed": "124-168",
        "pdf": "139-183",
        "sections": "6.1-6.7",
        "focus": "SAS, triangle congruence, exterior angle theorem, right triangles, circles and tangent lines, and synthetic proof flow.",
        "question": "How much triangle and circle geometry can be built without choosing a parallel postulate?",
        "translation": [
            "SAS is a construction rule: two sides and the included angle determine a congruence class.",
            "Triangle congruence is tracked by side lengths and angle measures rather than visual resemblance.",
            "The exterior angle theorem is a local inequality claim that can be diagrammed and sampled.",
            "Circle tangent facts become radius-line perpendicularity checks.",
        ],
        "visuals": [
            ("congruence", "sas-congruence-overlay.png", "SAS congruence overlay", "Compare two triangles after rigid alignment."),
            ("angle", "exterior-angle-inequality.png", "Exterior angle theorem", "Read an exterior angle against the two remote interior angles."),
            ("circle", "circle-tangent-radius.png", "Circle tangent and radius", "Check that the tangent direction is perpendicular to the radius."),
            ("proof_graph", "neutral-geometry-proof-flow.png", "Neutral proof flow", "Trace how SAS supports later triangle and circle claims."),
        ],
        "lab": "Generate triangles from two side lengths and an included angle, then compare their side-angle inventories after rotation and translation.",
        "pitfalls": [
            "Neutral geometry is not Euclidean geometry with the parallel postulate forgotten casually.",
            "Congruence data must match in the correct correspondence.",
            "A tangent is local: it touches the circle at one point and is perpendicular to the radius there.",
        ],
        "takeaways": [
            "Many triangle facts do not need a parallel axiom.",
            "Congruence is a reusable mechanism for transporting measurements.",
            "Circle tangency ties metric and angle ideas together.",
        ],
    },
    {
        "number": 7,
        "title": "The Theory of Parallels",
        "slug": "the-theory-of-parallels",
        "folder": "chapter-07-the-theory-of-parallels",
        "printed": "169-195",
        "pdf": "184-210",
        "sections": "7.1-7.3",
        "focus": "Parallel lines, Saccheri quadrilaterals, and the critical function.",
        "question": "What can parallel behavior reveal before the course commits to Euclidean or hyperbolic geometry?",
        "translation": [
            "Parallelism is a nonintersection relation inside a chosen line model.",
            "Saccheri quadrilaterals are diagnostic shapes for testing summit-angle behavior.",
            "A critical function records how separation grows under a non-Euclidean hypothesis.",
            "Euclidean and hyperbolic pictures can be compared by plotting families rather than arguing from one sketch.",
        ],
        "visuals": [
            ("parallel", "parallel-families-compare.png", "Families through an exterior point", "Contrast unique Euclidean parallel with many hyperbolic nonintersecting geodesics."),
            ("saccheri", "saccheri-quadrilateral-diagnostics.png", "Saccheri diagnostics", "Inspect equal legs, base angles, and summit behavior."),
            ("function_plot", "critical-function-profile.png", "Critical function profile", "See monotone growth as a measurable signature."),
            ("proof_graph", "parallel-theory-dependencies.png", "Parallel theory dependencies", "Track what depends on neutral results and what needs a parallel hypothesis."),
        ],
        "lab": "Vary a Saccheri summit height in a model diagram and record base length, summit length, and angle trends.",
        "pitfalls": [
            "Nonintersecting in one model drawing must be checked as a geometric relation, not guessed from pixels.",
            "Euclidean uniqueness is a special behavior, not a default of neutral geometry.",
            "Saccheri diagrams are diagnostic only when their equal-leg and right-angle conditions are enforced.",
        ],
        "takeaways": [
            "Parallel theory is where models begin to separate visibly.",
            "Saccheri quadrilaterals convert a global axiom question into a measurable shape.",
            "Critical functions turn qualitative divergence into data.",
        ],
    },
    {
        "number": 8,
        "title": "Hyperbolic Geometry",
        "slug": "hyperbolic-geometry",
        "folder": "chapter-08-hyperbolic-geometry",
        "printed": "196-223",
        "pdf": "211-238",
        "sections": "8.1-8.3",
        "focus": "Asymptotic rays, triangle defect, and distance between parallel lines.",
        "question": "How does the hyperbolic model make many parallels, angle defect, and exponential separation visible?",
        "translation": [
            "Poincare disk geodesics are diameters or boundary-orthogonal arcs.",
            "Asymptotic rays share an ideal endpoint on the boundary.",
            "Triangle angle defect behaves like hyperbolic area in constant curvature.",
            "Parallel-line distance can vary along the pair rather than staying constant.",
        ],
        "visuals": [
            ("poincare", "poincare-geodesics-and-ideal-points.png", "Poincare geodesics and ideal points", "Identify diameters, orthogonal arcs, and shared boundary endpoints."),
            ("hyperbolic_triangle", "hyperbolic-triangle-defect.png", "Hyperbolic triangle defect", "Compare sampled angle sum with pi and read the defect."),
            ("parallel", "hyperbolic-parallel-distance.png", "Distance between parallel lines", "Observe separation changing along asymptotic and ultraparallel families."),
            ("function_plot", "hyperbolic-growth-curves.png", "Hyperbolic growth curves", "Inspect exponential-like separation against Euclidean linear comparison."),
        ],
        "lab": "Move one vertex of a disk triangle toward the boundary and measure how visual size, angle sum, and defect change.",
        "pitfalls": [
            "The disk boundary is infinitely far away in the hyperbolic metric.",
            "Euclidean arcs count as hyperbolic lines only when they meet the boundary orthogonally.",
            "Conformal angle drawing does not make Euclidean and hyperbolic lengths comparable.",
        ],
        "takeaways": [
            "Hyperbolic geometry is visible through geodesic families and angle defect.",
            "Ideal boundary behavior organizes parallel rays.",
            "The Poincare disk makes angle inspection convenient while changing distance dramatically.",
        ],
    },
    {
        "number": 9,
        "title": "Euclidean Geometry",
        "slug": "euclidean-geometry",
        "folder": "chapter-09-euclidean-geometry",
        "printed": "224-247",
        "pdf": "239-262",
        "sections": "9.1-9.3",
        "focus": "Equivalent forms of the Euclidean parallel postulate, similarity theory, and classical Euclidean theorems.",
        "question": "What extra structure returns when the Euclidean parallel postulate is adopted?",
        "translation": [
            "Equivalent parallel postulates are alternative interfaces to the same Euclidean behavior.",
            "Similarity is scale without shape change, checked by ratios and equal angles.",
            "Classical theorems become reusable invariants under rigid motion and scaling.",
            "Coordinate experiments can reveal why these results are Euclidean rather than neutral.",
        ],
        "visuals": [
            ("euclidean_parallel", "equivalent-parallel-postulates.png", "Equivalent parallel postulates", "Compare unique parallels, angle sums, and rectangle behavior."),
            ("similarity", "similar-triangle-ratios.png", "Similarity ratios", "Check side ratios and matching angles after scaling."),
            ("circle", "classical-euclidean-circle-theorems.png", "Classical circle theorem lab", "Inspect chord, radius, and perpendicular-bisector relationships."),
            ("proof_graph", "euclidean-theorem-dependencies.png", "Euclidean theorem dependencies", "See where the parallel postulate enters the dependency graph."),
        ],
        "lab": "Generate pairs of triangles by scaling and rotation, then verify angle equality and constant side ratios.",
        "pitfalls": [
            "A theorem familiar from school geometry may quietly use the Euclidean parallel postulate.",
            "Congruence and similarity are different equivalence relations.",
            "Coordinate evidence should be tied back to invariant statements.",
        ],
        "takeaways": [
            "Euclidean geometry is neutral geometry plus a strong parallel rule.",
            "Similarity unlocks scale-based arguments.",
            "Classical theorems are best remembered as invariant patterns.",
        ],
    },
    {
        "number": 10,
        "title": "Area",
        "slug": "area",
        "folder": "chapter-10-area",
        "printed": "248-284",
        "pdf": "263-299",
        "sections": "10.1-10.4",
        "focus": "Area functions, Euclidean area, hyperbolic area, and Bolyai's theorem.",
        "question": "How does area become a function with axioms, and why does hyperbolic area behave through defect?",
        "translation": [
            "Area is a function on regions constrained by invariance, nonnegativity, and additivity.",
            "Euclidean polygon area can be computed by triangulation or the shoelace formula.",
            "Hyperbolic triangle area is represented by angle defect in constant curvature.",
            "Bolyai-style cut-and-reassemble reasoning is an invariance experiment.",
        ],
        "visuals": [
            ("area", "area-function-additivity.png", "Area function additivity", "Decompose a polygon and compare summed pieces with the whole."),
            ("function_plot", "shoelace-orientation-check.png", "Shoelace orientation check", "Inspect signed area changing under vertex orientation."),
            ("hyperbolic_triangle", "hyperbolic-area-defect-table.png", "Hyperbolic area by defect", "Read defect as an area-like quantity across sample triangles."),
            ("scissors", "bolyai-scissors-invariance.png", "Cut and reassemble invariance", "Track pieces under a rearrangement without changing total area."),
        ],
        "lab": "Triangulate a polygon two different ways and verify that additive area gives the same total.",
        "pitfalls": [
            "Area is not just a formula; the formula must respect the chosen axioms.",
            "Signed area carries orientation information that ordinary area discards.",
            "Hyperbolic area and Euclidean area should not be compared by the same visual scale.",
        ],
        "takeaways": [
            "Area functions are axiomatic objects with computational realizations.",
            "Triangulation and shoelace formulas are consistency checks on Euclidean area.",
            "Hyperbolic defect turns angle data into area data.",
        ],
    },
    {
        "number": 11,
        "title": "The Theory of Isometries",
        "slug": "the-theory-of-isometries",
        "folder": "chapter-11-the-theory-of-isometries",
        "printed": "285-358",
        "pdf": "300-373",
        "sections": "11.1-11.9",
        "focus": "Collineations, Klein and Poincare disk models, reflections, pencils, cycles, double reflections, classification, and isometry groups.",
        "question": "How can transformations classify a geometry by what they preserve?",
        "translation": [
            "A collineation preserves incidence; an isometry preserves distance as well.",
            "Disk models expose transformations as maps of a bounded coordinate world.",
            "Reflections generate larger motion groups through composition.",
            "Pencils, cycles, and invariant sets organize transformation classification.",
        ],
        "visuals": [
            ("isometry", "isometry-classification-grid.png", "Isometry classification grid", "Compare translations, rotations, reflections, and glide-like compositions."),
            ("reflection", "double-reflection-composition.png", "Double reflections", "Observe when two reflections compose to a rotation or translation-like motion."),
            ("pencil", "pencils-and-cycles.png", "Pencils and cycles", "Inspect families of circles and lines sharing constraints."),
            ("proof_graph", "isometry-group-dependency-graph.png", "Isometry group dependencies", "Track how reflections, invariant sets, and classification fit together."),
        ],
        "lab": "Compose two reflection matrices at variable angle and measure the resulting rotation angle.",
        "pitfalls": [
            "Preserving lines is weaker than preserving distance.",
            "A transformation's visual effect depends on the model used to draw it.",
            "Composition order matters for transformations.",
        ],
        "takeaways": [
            "Transformations reveal geometry through invariants.",
            "Reflections are generators for rich isometry groups.",
            "Classification turns many motions into a small set of structural types.",
        ],
    },
]


AGENTS_MD = """# Agent Instructions: Geometry A Metric Approach with Models Notebook Course

This folder is a standalone visualization-first notebook edition of *Geometry: A Metric Approach with Models*, Second Edition, by Richard S. Millman and George D. Parker. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local skills under `D:\\Geometry\\.codex\\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or figures.
- The PDF is an image-only scan. Render pages only as temporary reading aids; do not store page crops in this course.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualizations are part of the explanation. Use diagrams, plots, widgets or HTML parameter labs, symbolic checks, computational experiments, and proof-state diagrams wherever they clarify the geometry.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.

## Course Structure

```text
Geometry-A-Metric-Approach-with-Models/
  00-book-index.ipynb
  AGENTS.md
  artifacts/
  scripts/
  utils/
  chapter-01-preliminary-notions/
  ...
  chapter-11-the-theory-of-isometries/
```

Each chapter folder contains:

```text
00-index.ipynb
<canonical notebook>.ipynb
```

There should be exactly one canonical teaching notebook in each chapter folder, excluding `00-index.ipynb`.

## Source Map

The book has 11 chapters, no formal part divisions, no appendices, then bibliography and index. Body printed pages map to physical PDF pages by `pdf_page = printed_page + 15`.

| Unit | Folder | Printed Pages | PDF Pages | Focus |
| --- | --- | ---: | ---: | --- |
| Chapter 1 | `chapter-01-preliminary-notions` | 1-16 | 16-31 | Axioms, models, equivalence relations, and functions. |
| Chapter 2 | `chapter-02-incidence-and-metric-geometry` | 17-41 | 32-56 | Incidence models, metric geometry, and special coordinate systems. |
| Chapter 3 | `chapter-03-betweenness-and-elementary-figures` | 42-62 | 57-77 | Alternative Cartesian descriptions, betweenness, segments, rays, angles, and triangles. |
| Chapter 4 | `chapter-04-plane-separation` | 63-89 | 78-104 | Plane separation, Pasch geometries, interiors, crossbar theorem, and convex quadrilaterals. |
| Chapter 5 | `chapter-05-angle-measure` | 90-123 | 105-138 | Angle measure, Molton plane, perpendicularity, angle congruence, and Poincare angle measure. |
| Chapter 6 | `chapter-06-neutral-geometry` | 124-168 | 139-183 | SAS, triangle congruence, exterior angle theorem, right triangles, circles and tangent lines, and synthetic proof flow. |
| Chapter 7 | `chapter-07-the-theory-of-parallels` | 169-195 | 184-210 | Parallel lines, Saccheri quadrilaterals, and the critical function. |
| Chapter 8 | `chapter-08-hyperbolic-geometry` | 196-223 | 211-238 | Asymptotic rays, triangle defect, and distance between parallel lines. |
| Chapter 9 | `chapter-09-euclidean-geometry` | 224-247 | 239-262 | Equivalent forms of the Euclidean parallel postulate, similarity theory, and classical Euclidean theorems. |
| Chapter 10 | `chapter-10-area` | 248-284 | 263-299 | Area functions, Euclidean area, hyperbolic area, and Bolyai's theorem. |
| Chapter 11 | `chapter-11-the-theory-of-isometries` | 285-358 | 300-373 | Collineations, disk models, reflections, pencils, cycles, double reflections, classification, and isometry groups. |

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Standalone chapter question and motivation.
3. Translation guide from book concepts into computational language.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Generated visual artifacts displayed inline.
8. Applied lab or design exercise.
9. Sanity checks asserting identities, artifact existence, and nonblank visuals.
10. Takeaways.

## Artifact Contract

Store generated outputs under:

```text
artifacts/chapter-XX/figures/
artifacts/chapter-XX/html/
artifacts/chapter-XX/checks/
artifacts/chapter-XX/tables/
```

Artifact filenames should name the concept, not the rendering technology. Repeated placeholder visuals are a QC failure. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `pandas`, `networkx`, `shapely`, `trimesh`, `pyvista`, and the rest of the root geometry stack. This course currently needs no dependency additions.

## Worker Boundaries

Assign one worker to one canonical notebook, one helper module, or one script task. Chapter workers may edit only their chapter folder, matching artifact subtree, and explicitly assigned helper module. Index workers own `00-book-index.ipynb` and `00-index.ipynb` files. QC workers run audits and validation and report findings.

## Commands

Run from `D:\\Geometry`:

```powershell
uv run python Geometry-A-Metric-Approach-with-Models/scripts/build_gmam_course_indexes.py
uv run python -m compileall -q Geometry-A-Metric-Approach-with-Models/utils Geometry-A-Metric-Approach-with-Models/scripts
uv run python Geometry-A-Metric-Approach-with-Models/scripts/audit_gmam_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Geometry-A-Metric-Approach-with-Models/scripts/audit_gmam_visuals.py
uv run python Geometry-A-Metric-Approach-with-Models/scripts/validate_gmam_course.py --limit 4 --timeout 300
git diff --check
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.
"""


UTILS_INIT = '''"""Utilities for the Geometry: A Metric Approach with Models course."""\n'''


ARTIFACTS_PY = '''"""Artifact helpers for the GMAM notebook course."""

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
    raise RuntimeError("Could not find GMAM book root")


def chapter_artifact_root(chapter_number: int, book_root: Path | None = None) -> Path:
    root = find_book_root() if book_root is None else Path(book_root)
    path = root / "artifacts" / f"chapter-{chapter_number:02d}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Any, path: Path) -> Path:
    path = ensure_parent(Path(path))
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
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


def assert_artifacts(paths: Iterable[Path], *, min_bytes: int = 64) -> None:
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


def display_artifact(path: Path, *, width: int = 760, height: int = 520) -> None:
    from IPython.display import HTML, Image, Markdown, display

    candidate = Path(path)
    suffix = candidate.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg"}:
        display(Image(filename=str(candidate), width=width))
    elif suffix in {".html", ".htm"}:
        display(HTML(f'<iframe src="{candidate.as_posix()}" width="{width}" height="{height}"></iframe>'))
    elif suffix == ".json":
        display(Markdown(f"`{candidate.name}`"))
    else:
        display(Markdown(f"[{candidate.name}]({candidate.as_posix()})"))
'''


PLOTTING_PY = '''"""Plotting helpers for metric-approach geometry notebooks."""

from __future__ import annotations

import math
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Polygon


PALETTE = ["#2f6fbb", "#d95f02", "#1b9e77", "#7570b3", "#e7298a", "#66a61e"]


def new_figure(title: str, *, figsize: tuple[float, float] = (8, 5)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(title, fontsize=13, pad=12)
    ax.grid(True, color="#e8e8e8", linewidth=0.8)
    ax.set_axisbelow(True)
    return fig, ax


def set_equal(ax, *, pad: float = 0.4) -> None:
    ax.set_aspect("equal", adjustable="box")
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    span = max(x1 - x0, y1 - y0) + pad
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    ax.set_xlim(cx - span / 2, cx + span / 2)
    ax.set_ylim(cy - span / 2, cy + span / 2)


def annotate_point(ax, point, label: str, *, color: str = "#222222", offset=(0.05, 0.05)) -> None:
    p = np.asarray(point, dtype=float)
    ax.scatter([p[0]], [p[1]], s=48, color=color, zorder=4)
    ax.text(p[0] + offset[0], p[1] + offset[1], label, fontsize=10, color=color)


def draw_segment(ax, p, q, *, color: str = "#2f6fbb", label: str | None = None, lw: float = 2.2) -> None:
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, label=label)


def draw_ray(ax, origin, direction, *, color: str = "#d95f02", label: str | None = None, length: float = 3.0) -> None:
    origin = np.asarray(origin, dtype=float)
    direction = np.asarray(direction, dtype=float)
    direction = direction / np.linalg.norm(direction)
    end = origin + length * direction
    ax.arrow(origin[0], origin[1], end[0] - origin[0], end[1] - origin[1],
             head_width=0.09, length_includes_head=True, color=color, lw=1.8)
    if label:
        ax.text(end[0], end[1], label, color=color, fontsize=10)


def draw_angle_arc(ax, center, radius: float, start_deg: float, end_deg: float, *, color: str = "#222222") -> None:
    arc = Arc(center, 2 * radius, 2 * radius, theta1=start_deg, theta2=end_deg, color=color, lw=2)
    ax.add_patch(arc)


def draw_circle(ax, center, radius: float, *, color: str = "#1b9e77", fill: bool = False, alpha: float = 0.15) -> None:
    ax.add_patch(Circle(center, radius, edgecolor=color, facecolor=color if fill else "none", lw=2, alpha=alpha if fill else 1.0))


def draw_polygon(ax, points: Iterable[tuple[float, float]], *, color: str = "#7570b3", alpha: float = 0.16) -> None:
    pts = np.asarray(list(points), dtype=float)
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor=color, alpha=alpha, lw=2))
    ax.plot([*pts[:, 0], pts[0, 0]], [*pts[:, 1], pts[0, 1]], color=color, lw=2)


def angle_degrees(u, v) -> float:
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    cosang = float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))
    return math.degrees(math.acos(max(-1.0, min(1.0, cosang))))
'''


GEOMETRY_PY = '''"""Geometry helpers and chapter visualization builders for GMAM."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objects as go
from PIL import Image, ImageStat

from .artifacts import save_matplotlib
from .plotting import (
    PALETTE,
    angle_degrees,
    annotate_point,
    draw_angle_arc,
    draw_circle,
    draw_polygon,
    draw_ray,
    draw_segment,
    new_figure,
    set_equal,
)


def orientation(a, b, c) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    c = np.asarray(c, dtype=float)
    return float(np.cross(b - a, c - a))


def triangle_area(a, b, c) -> float:
    return abs(orientation(a, b, c)) / 2


def shoelace_area(points) -> float:
    pts = np.asarray(points, dtype=float)
    x = pts[:, 0]
    y = pts[:, 1]
    return float(0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))))


def affine_parameter(a, b, p) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    p = np.asarray(p, dtype=float)
    v = b - a
    return float(np.dot(p - a, v) / np.dot(v, v))


def is_between(a, b, p, *, tol: float = 1e-9) -> bool:
    t = affine_parameter(a, b, p)
    return -tol <= t <= 1 + tol and abs(orientation(a, b, p)) <= tol


def angle_measure(a, o, b) -> float:
    return angle_degrees(np.asarray(a) - np.asarray(o), np.asarray(b) - np.asarray(o))


def hyperbolic_distance_disk(z, w) -> float:
    z = complex(z)
    w = complex(w)
    num = 2 * abs(z - w) ** 2
    den = (1 - abs(z) ** 2) * (1 - abs(w) ** 2)
    return float(math.acosh(1 + num / den))


def image_stats(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        width, height = image.size
        stat = ImageStat.Stat(image.convert("RGB"))
    return {
        "path": path.as_posix(),
        "width": width,
        "height": height,
        "bytes": path.stat().st_size,
        "max_channel_stddev": max(stat.stddev) if stat.stddev else 0.0,
    }


def render_visuals(artifact_root: Path, specs: list[dict[str, Any]]) -> tuple[list[Path], list[dict[str, Any]]]:
    paths: list[Path] = []
    stats: list[dict[str, Any]] = []
    for index, spec in enumerate(specs):
        fig = build_visual(spec, index)
        path = Path(artifact_root) / "figures" / spec["filename"]
        save_matplotlib(fig, path)
        plt.close(fig)
        paths.append(path)
        stats.append(image_stats(path))
    return paths, stats


def build_visual(spec: dict[str, Any], index: int):
    kind = spec.get("kind", "coordinate")
    if kind == "proof_graph":
        return proof_graph_visual(spec, index)
    if kind == "incidence":
        return incidence_visual(spec, index)
    if kind == "partition":
        return partition_visual(spec, index)
    if kind == "mapping":
        return mapping_visual(spec, index)
    if kind == "metric":
        return metric_visual(spec, index)
    if kind == "coordinate":
        return coordinate_visual(spec, index)
    if kind == "affine_line":
        return affine_line_visual(spec, index)
    if kind == "betweenness":
        return betweenness_visual(spec, index)
    if kind == "separation":
        return separation_visual(spec, index)
    if kind == "pasch":
        return pasch_visual(spec, index)
    if kind == "angle":
        return angle_visual(spec, index)
    if kind == "molton":
        return molton_visual(spec, index)
    if kind == "poincare":
        return poincare_visual(spec, index)
    if kind == "congruence":
        return congruence_visual(spec, index)
    if kind == "circle":
        return circle_visual(spec, index)
    if kind == "parallel":
        return parallel_visual(spec, index)
    if kind == "saccheri":
        return saccheri_visual(spec, index)
    if kind == "function_plot":
        return function_plot_visual(spec, index)
    if kind == "hyperbolic_triangle":
        return hyperbolic_triangle_visual(spec, index)
    if kind == "euclidean_parallel":
        return euclidean_parallel_visual(spec, index)
    if kind == "similarity":
        return similarity_visual(spec, index)
    if kind == "scissors":
        return scissors_visual(spec, index)
    if kind == "isometry":
        return isometry_visual(spec, index)
    if kind == "reflection":
        return reflection_visual(spec, index)
    if kind == "pencil":
        return pencil_visual(spec, index)
    if kind == "area":
        return area_visual(spec, index)
    return coordinate_visual(spec, index)


def proof_graph_visual(spec, index):
    fig, ax = new_figure(spec["title"], figsize=(8.2, 5.2))
    graph = nx.DiGraph()
    nodes = ["primitive terms", "axioms", "definitions", "lemmas", "theorems", "models", "checks"]
    graph.add_nodes_from(nodes)
    graph.add_edges_from([
        ("primitive terms", "axioms"),
        ("axioms", "definitions"),
        ("definitions", "lemmas"),
        ("lemmas", "theorems"),
        ("models", "checks"),
        ("axioms", "checks"),
        ("checks", "theorems"),
    ])
    pos = nx.spring_layout(graph, seed=37 + index)
    nx.draw_networkx_edges(graph, pos, ax=ax, arrows=True, arrowstyle="-|>", width=1.8, edge_color="#777777")
    node_colors = [PALETTE[i % len(PALETTE)] for i in range(len(nodes))]
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=node_colors, node_size=1450, alpha=0.95)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=9)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9, va="bottom")
    ax.axis("off")
    return fig


def incidence_visual(spec, index):
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.8))
    fig.suptitle(spec["title"], fontsize=13)
    pts = np.array([[0.1, 0.1], [1.0, 0.15], [0.35, 0.95], [1.2, 0.9]])
    lines = [(0, 1), (0, 2), (1, 3), (2, 3)]
    for ax, shift, title in zip(axes, [0.0, 0.18], ["candidate A", "candidate B"]):
        moved = pts + np.array([shift, 0.0])
        for i, j in lines:
            draw_segment(ax, moved[i], moved[j], color="#2f6fbb")
        for i, p in enumerate(moved):
            annotate_point(ax, p, f"P{i+1}", color=PALETTE[i % len(PALETTE)])
        ax.set_title(title)
        ax.set_xlim(-0.15, 1.65)
        ax.set_ylim(-0.1, 1.25)
        set_equal(ax)
    axes[0].text(0.0, -0.22, spec["inspection"], transform=axes[0].transAxes, fontsize=9)
    return fig


def partition_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    xs = np.arange(12)
    residues = xs % 4
    for r in range(4):
        mask = residues == r
        ax.scatter(xs[mask], np.zeros(mask.sum()) + r * 0.18, s=110, color=PALETTE[r], label=f"class {r}")
        for x in xs[mask]:
            ax.text(x, r * 0.18 + 0.08, str(x), ha="center", fontsize=9)
    for r in range(4):
        members = xs[residues == r]
        ax.plot(members, np.zeros_like(members) + r * 0.18, color=PALETTE[r], lw=3, alpha=0.35)
    ax.set_yticks([])
    ax.set_xlabel("integers sampled from one set")
    ax.legend(loc="upper right")
    ax.text(0.01, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def mapping_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    left = np.array([[0, 0], [0, 1], [0, 2], [0, 3]], dtype=float)
    right = np.array([[3, 0.3], [3, 1.3], [3, 2.3]], dtype=float)
    mapping = [0, 1, 1, 2]
    for i, p in enumerate(left):
        annotate_point(ax, p, f"x{i}", color="#2f6fbb")
    for j, p in enumerate(right):
        annotate_point(ax, p, f"y{j}", color="#d95f02")
    for i, j in enumerate(mapping):
        ax.annotate("", xy=right[j], xytext=left[i], arrowprops={"arrowstyle": "->", "lw": 1.7, "color": "#555555"})
    ax.text(1.45, 3.05, "fiber collision at y1", ha="center", fontsize=10)
    ax.set_xlim(-0.6, 3.7)
    ax.set_ylim(-0.4, 3.5)
    ax.axis("off")
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def metric_visual(spec, index):
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.6))
    fig.suptitle(spec["title"], fontsize=13)
    for ax, metric_name, scale in zip(axes, ["Euclidean radius", "Poincare visual radius"], [1.0, 0.55]):
        draw_circle(ax, (0, 0), 1.0, color="#bbbbbb")
        draw_circle(ax, (0.15, 0.05), 0.45 * scale, color="#2f6fbb", fill=True)
        annotate_point(ax, (0.15, 0.05), "center")
        ax.set_title(metric_name)
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        set_equal(ax)
    axes[0].text(0.0, -0.2, spec["inspection"], transform=axes[0].transAxes, fontsize=9)
    return fig


def coordinate_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    theta = np.linspace(0, 2 * np.pi, 240)
    ax.plot(np.cos(theta), np.sin(theta), color="#777777", lw=1.5, label="unit disk chart")
    point = np.array([0.58, 0.42])
    annotate_point(ax, point, "P")
    draw_segment(ax, (0, 0), point, color="#2f6fbb", label="polar radius")
    ax.axhline(0, color="#aaaaaa")
    ax.axvline(0, color="#aaaaaa")
    ax.text(point[0], 0.02, "x", color="#555555")
    ax.text(0.02, point[1], "y", color="#555555")
    ax.legend()
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def affine_line_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    x = np.linspace(-2, 3, 100)
    y = 0.55 * x + 0.5
    ax.plot(x, y, color="#2f6fbb", lw=2.5, label="implicit: ax + by + c = 0")
    ax.axvline(1.25, color="#d95f02", lw=2.2, label="vertical: x = constant")
    annotate_point(ax, (-1, -0.05), "A")
    annotate_point(ax, (2, 1.6), "B")
    ax.legend()
    ax.set_xlim(-2.2, 3.2)
    ax.set_ylim(-1.2, 2.8)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def betweenness_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    a = np.array([-1.5, -0.4])
    c = np.array([1.8, 0.8])
    ts = [-0.35, 0.0, 0.35, 0.7, 1.0, 1.25]
    draw_segment(ax, a, c, color="#2f6fbb", lw=3)
    for t in ts:
        p = (1 - t) * a + t * c
        color = "#1b9e77" if 0 <= t <= 1 else "#d95f02"
        annotate_point(ax, p, f"t={t:g}", color=color)
    ax.set_xlim(-2.2, 2.4)
    ax.set_ylim(-1.2, 1.7)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def separation_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    x = np.linspace(-2.5, 2.5, 100)
    y = 0.35 * x + 0.2
    ax.plot(x, y, color="#222222", lw=2.4, label="separating line")
    pts = np.array([[-1.8, 1.2], [-0.6, 0.8], [1.7, 1.5], [-1.5, -1.4], [0.4, -0.8], [1.9, -0.5]])
    side = pts[:, 1] - (0.35 * pts[:, 0] + 0.2)
    for p, s in zip(pts, side):
        color = "#2f6fbb" if s > 0 else "#d95f02"
        annotate_point(ax, p, "+" if s > 0 else "-", color=color)
    ax.legend()
    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-2.0, 2.0)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def pasch_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    tri = [(-1.8, -1.0), (1.8, -0.75), (-0.25, 1.35)]
    draw_polygon(ax, tri, color="#7570b3")
    for label, p in zip(["A", "B", "C"], tri):
        annotate_point(ax, p, label)
    draw_segment(ax, (-2.0, 0.6), (1.2, -1.25), color="#d95f02", label="transversal")
    annotate_point(ax, (-0.78, -0.1), "crosses AC", color="#d95f02")
    annotate_point(ax, (0.92, -0.82), "crosses AB", color="#d95f02")
    ax.legend()
    ax.set_xlim(-2.4, 2.2)
    ax.set_ylim(-1.6, 1.8)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def angle_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    o = np.array([0.0, 0.0])
    u = np.array([1.0, 0.15])
    v = np.array([0.25, 1.0])
    draw_ray(ax, o, u, color="#2f6fbb", label="ray 1")
    draw_ray(ax, o, v, color="#d95f02", label="ray 2")
    draw_angle_arc(ax, o, 0.75, math.degrees(math.atan2(u[1], u[0])), math.degrees(math.atan2(v[1], v[0])), color="#1b9e77")
    annotate_point(ax, o, "O")
    ax.text(0.5, 0.35, f"{angle_degrees(u, v):.1f} deg", color="#1b9e77", fontsize=11)
    ax.set_xlim(-0.4, 2.5)
    ax.set_ylim(-0.4, 2.5)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def molton_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    for slope in [-1.0, -0.35, 0.35, 1.0]:
        xs1 = np.linspace(-2.2, 0, 40)
        xs2 = np.linspace(0, 2.2, 40)
        ax.plot(xs1, slope * xs1, color="#2f6fbb", lw=1.8)
        ax.plot(xs2, (1.7 * slope if slope > 0 else slope) * xs2, color="#d95f02", lw=1.8)
    ax.axvline(0, color="#777777", lw=1)
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def poincare_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    theta = np.linspace(0, 2 * np.pi, 360)
    ax.plot(np.cos(theta), np.sin(theta), color="#222222", lw=2)
    ax.plot([-0.9, 0.9], [0.0, 0.0], color="#2f6fbb", lw=2.2, label="diameter geodesic")
    for center, radius, t0, t1, color in [((0.0, 1.55), 1.25, 220, 320, "#d95f02"), ((1.35, 0.0), 1.05, 135, 225, "#1b9e77")]:
        ang = np.radians(np.linspace(t0, t1, 120))
        ax.plot(center[0] + radius * np.cos(ang), center[1] + radius * np.sin(ang), color=color, lw=2.2)
    annotate_point(ax, (0.0, 0.0), "O")
    ax.legend(loc="upper right")
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def congruence_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    tri = np.array([[0, 0], [2.0, 0.1], [0.7, 1.4]])
    angle = np.radians(28)
    rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    tri2 = tri @ rot.T + np.array([0.2, -0.1])
    draw_polygon(ax, tri, color="#2f6fbb")
    draw_polygon(ax, tri2, color="#d95f02")
    for label, p in zip(["A", "B", "C"], tri):
        annotate_point(ax, p, label, color="#2f6fbb")
    for label, p in zip(["A'", "B'", "C'"], tri2):
        annotate_point(ax, p, label, color="#d95f02")
    ax.set_xlim(-0.8, 2.6)
    ax.set_ylim(-0.7, 2.3)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def circle_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    center = np.array([0.0, 0.0])
    p = np.array([0.72, 0.69])
    draw_circle(ax, center, 1.0, color="#1b9e77")
    annotate_point(ax, center, "C")
    annotate_point(ax, p, "T")
    draw_segment(ax, center, p, color="#2f6fbb", label="radius")
    tangent = np.array([-p[1], p[0]])
    tangent = tangent / np.linalg.norm(tangent)
    draw_segment(ax, p - 1.2 * tangent, p + 1.2 * tangent, color="#d95f02", label="tangent")
    ax.legend()
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def parallel_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    x = np.linspace(-2.5, 2.5, 160)
    ax.plot(x, 0.4 * x - 0.6, color="#2f6fbb", lw=2.2, label="reference")
    ax.plot(x, 0.4 * x + 0.7, color="#2f6fbb", lw=2.2, label="Euclidean parallel")
    for a in [-0.6, 0.0, 0.6]:
        ax.plot(x, np.tanh(x + a) + 0.2 * a, color="#d95f02", alpha=0.8, lw=1.8)
    annotate_point(ax, (0.0, 1.25), "exterior point", color="#1b9e77")
    ax.legend()
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-1.8, 2.0)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def saccheri_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    pts = np.array([[-1.2, -0.8], [1.2, -0.8], [0.9, 0.9], [-0.9, 0.9]])
    draw_polygon(ax, pts, color="#7570b3")
    for label, p in zip(["A", "B", "C", "D"], pts):
        annotate_point(ax, p, label)
    draw_segment(ax, pts[0], pts[3], color="#d95f02")
    draw_segment(ax, pts[1], pts[2], color="#d95f02")
    ax.text(0, -1.05, "base right angles and equal legs", ha="center", fontsize=10)
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.3, 1.4)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def function_plot_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    x = np.linspace(0, 3, 200)
    ax.plot(x, x, label="Euclidean linear comparison", color="#2f6fbb")
    ax.plot(x, np.sinh(x) / np.sinh(3) * 3, label="curved model growth", color="#d95f02")
    ax.plot(x, np.tanh(x), label="bounded critical profile", color="#1b9e77")
    ax.set_xlabel("parameter")
    ax.set_ylabel("measured response")
    ax.legend()
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def hyperbolic_triangle_visual(spec, index):
    fig = poincare_visual({**spec, "title": spec["title"]}, index)
    ax = fig.axes[0]
    pts = np.array([[0.0, 0.0], [0.65, 0.05], [0.15, 0.7]])
    draw_polygon(ax, pts, color="#e7298a")
    for label, p in zip(["A", "B", "C"], pts):
        annotate_point(ax, p, label, color="#e7298a")
    ax.text(-0.95, -0.95, "angle sum < pi gives defect", fontsize=10)
    return fig


def euclidean_parallel_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    x = np.linspace(-2, 2, 100)
    ax.plot(x, 0 * x, color="#222222", lw=2)
    ax.plot(x, 0 * x + 1.0, color="#2f6fbb", lw=2)
    draw_segment(ax, (-1.4, -0.25), (1.0, 1.35), color="#d95f02", label="transversal")
    ax.text(-1.8, 0.15, "alternate interior angles", fontsize=10)
    ax.text(0.7, 0.55, "sum = 180 deg", fontsize=10)
    ax.legend()
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-0.6, 1.7)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def similarity_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    tri = np.array([[0, 0], [1.2, 0], [0.35, 0.9]])
    draw_polygon(ax, tri, color="#2f6fbb")
    draw_polygon(ax, 1.7 * tri + np.array([1.7, 0.15]), color="#d95f02")
    ax.text(0.35, -0.25, "scale 1", ha="center")
    ax.text(2.5, -0.25, "scale 1.7", ha="center")
    ax.set_xlim(-0.4, 4.1)
    ax.set_ylim(-0.5, 2.1)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def area_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    poly = np.array([[-1.4, -0.9], [1.3, -0.7], [1.6, 0.7], [-0.3, 1.3], [-1.5, 0.2]])
    draw_polygon(ax, poly, color="#2f6fbb")
    anchor = poly[0]
    for i in range(1, len(poly) - 1):
        draw_segment(ax, anchor, poly[i + 1], color="#d95f02", lw=1.5)
    ax.text(-0.25, -1.25, f"shoelace area = {shoelace_area(poly):.2f}", fontsize=10)
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-1.6, 1.7)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def scissors_visual(spec, index):
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))
    fig.suptitle(spec["title"], fontsize=13)
    pieces = [
        np.array([[0, 0], [1.5, 0], [0.4, 0.8]]),
        np.array([[1.5, 0], [2.0, 1.0], [0.4, 0.8]]),
    ]
    for ax, title, offset in zip(axes, ["before cut", "after rearrangement"], [np.array([0, 0]), np.array([0.25, -0.15])]):
        for i, piece in enumerate(pieces):
            draw_polygon(ax, piece + offset + np.array([0.35 * i, 0.25 * i]), color=PALETTE[i])
        ax.set_title(title)
        ax.set_xlim(-0.4, 3.0)
        ax.set_ylim(-0.4, 1.8)
        set_equal(ax)
    axes[0].text(0.0, -0.2, spec["inspection"], transform=axes[0].transAxes, fontsize=9)
    return fig


def isometry_visual(spec, index):
    fig, axes = plt.subplots(2, 2, figsize=(8.8, 6.2))
    fig.suptitle(spec["title"], fontsize=13)
    pts = np.array([[0, 0], [1, 0], [0.3, 0.8]])
    transforms = [
        ("translate", pts + np.array([0.5, 0.3])),
        ("rotate", pts @ np.array([[0, -1], [1, 0]])),
        ("reflect", pts * np.array([-1, 1])),
        ("glide-like", pts * np.array([1, -1]) + np.array([0.6, 0.2])),
    ]
    for ax, (title, moved) in zip(axes.ravel(), transforms):
        draw_polygon(ax, pts, color="#bbbbbb")
        draw_polygon(ax, moved, color="#2f6fbb")
        ax.set_title(title)
        ax.set_xlim(-1.4, 2.1)
        ax.set_ylim(-1.2, 1.6)
        set_equal(ax)
    axes.ravel()[0].text(0.0, -0.22, spec["inspection"], transform=axes.ravel()[0].transAxes, fontsize=9)
    return fig


def reflection_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    theta = np.radians(35)
    line1 = np.array([np.cos(theta), np.sin(theta)])
    line2 = np.array([np.cos(-theta), np.sin(-theta)])
    draw_segment(ax, -2 * line1, 2 * line1, color="#2f6fbb", label="mirror 1")
    draw_segment(ax, -2 * line2, 2 * line2, color="#d95f02", label="mirror 2")
    p = np.array([1.0, 0.45])
    annotate_point(ax, p, "P")
    annotate_point(ax, np.array([0.25, 1.05]), "after two reflections", color="#1b9e77")
    draw_angle_arc(ax, (0, 0), 0.55, -35, 35, color="#222222")
    ax.legend()
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.6, 1.6)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def pencil_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    for r, color in zip([0.45, 0.75, 1.05, 1.35], PALETTE):
        draw_circle(ax, (0.2, 0.0), r, color=color)
    for angle in [-35, 0, 35]:
        d = np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle))])
        draw_segment(ax, -1.8 * d + np.array([0.2, 0]), 1.8 * d + np.array([0.2, 0]), color="#555555", lw=1.4)
    annotate_point(ax, (0.2, 0.0), "common center")
    ax.set_xlim(-1.7, 2.1)
    ax.set_ylim(-1.6, 1.6)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def build_parameter_lab(meta: dict[str, Any]):
    chapter = int(meta["number"])
    t = np.linspace(0.05, 2.5, 160)
    if chapter in {7, 8}:
        y1 = np.tanh(t)
        y2 = np.sinh(t) / np.sinh(2.5)
        title = "Parallel and hyperbolic growth parameter lab"
        ytitle = "normalized separation"
    elif chapter == 10:
        y1 = 0.5 * t * (2.5 - t)
        y2 = np.maximum(0, np.pi - (1.0 + 0.25 * t + 0.4))
        title = "Area and defect parameter lab"
        ytitle = "area-like response"
    elif chapter == 11:
        y1 = np.cos(t)
        y2 = np.sin(t)
        title = "Isometry composition parameter lab"
        ytitle = "matrix entry"
    else:
        y1 = t
        y2 = t**2 / t.max()
        title = f"Chapter {chapter} parameter lab"
        ytitle = "computed response"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y1, mode="lines", name="primary invariant"))
    fig.add_trace(go.Scatter(x=t, y=y2, mode="lines", name="comparison"))
    fig.update_layout(title=title, xaxis_title="parameter", yaxis_title=ytitle, template="plotly_white", height=420)
    return fig


def chapter_numeric_checks(meta: dict[str, Any], visual_stats: list[dict[str, Any]]) -> dict[str, Any]:
    a = np.array([0.0, 0.0])
    b = np.array([2.0, 0.0])
    c = np.array([0.5, 1.25])
    midpoint = (a + b) / 2
    checks = {
        "chapter": int(meta["number"]),
        "triangle_area": triangle_area(a, b, c),
        "midpoint_between": is_between(a, b, midpoint),
        "angle_A_degrees": angle_measure(b, a, c),
        "shoelace_area_square": shoelace_area(np.array([[0, 0], [1, 0], [1, 1], [0, 1]])),
        "visual_count": len(visual_stats),
        "minimum_visual_stddev": min(item["max_channel_stddev"] for item in visual_stats) if visual_stats else 0.0,
    }
    if int(meta["number"]) in {8, 10}:
        checks["sample_disk_distance"] = hyperbolic_distance_disk(0.1 + 0.0j, 0.45 + 0.2j)
        checks["sample_angle_defect"] = math.pi - (0.9 + 0.8 + 0.7)
    if int(meta["number"]) == 11:
        theta = math.radians(30)
        rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        checks["rotation_determinant"] = float(np.linalg.det(rot))
    return checks
'''


def course_map_literal() -> str:
    rows = []
    for chapter in CHAPTERS:
        rows.append(
            {
                "number": chapter["number"],
                "title": chapter["title"],
                "slug": chapter["slug"],
                "folder": chapter["folder"],
                "notebook": f"{chapter['number']:02d}-{chapter['slug']}.ipynb",
                "printed": chapter["printed"],
                "pdf": chapter["pdf"],
                "sections": chapter["sections"],
                "focus": chapter["focus"],
            }
        )
    return json.dumps(rows, indent=4)


VALIDATION_PY = '''"""Validation helpers for the GMAM notebook course."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat


BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-book-index.ipynb"}
COURSE_MAP = __COURSE_MAP__


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
'''.replace("__COURSE_MAP__", course_map_literal())


BUILD_INDEXES_PY = '''"""Build GMAM book and chapter index notebooks."""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat as nbf

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import COURSE_MAP  # noqa: E402


def write_notebook(path: Path, markdown: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = nbf.v4.new_notebook()
    nb["cells"] = [nbf.v4.new_markdown_cell(markdown.strip() + "\\n")]
    nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}
    nbf.write(nb, path)


def book_index() -> str:
    rows = [
        "| Chapter | Notebook | Printed Pages | PDF Pages | Focus |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for item in COURSE_MAP:
        rows.append(
            f"| {item['number']} | [{item['title']}]({item['folder']}/{item['notebook']}) | "
            f"{item['printed']} | {item['pdf']} | {item['focus']} |"
        )
    return f"""# Geometry: A Metric Approach with Models

This is a standalone visualization-first notebook course. The scanned PDF is used only for source orientation: title, chapter order, page spans, definitions, and exercises. The notebooks use original prose, original computational examples, and generated visual artifacts.

Body printed pages map to physical PDF pages by `pdf_page = printed_page + 15`.

The frontmatter note on computers and hyperbolic geometry is treated as motivation for the course design: the notebooks make the model calculations and graphical experiments executable with the modern shared geometry stack.

## Chapter Route

{chr(10).join(rows)}

## Course Contract

- One canonical notebook per chapter folder plus a local `00-index.ipynb`.
- Artifacts are saved under `artifacts/chapter-XX/`.
- Each chapter includes a storyboard, visual artifacts, computational checks, an applied lab, and takeaways.
- No textbook screenshots, crops, long exercise text, or copied prose are included.
"""


def chapter_index(item: dict) -> str:
    return f"""# Chapter {item['number']}: {item['title']}

- Source orientation: printed pages {item['printed']}; PDF pages {item['pdf']}; sections {item['sections']}.
- Focus: {item['focus']}
- Canonical notebook: [{item['notebook']}]({item['notebook']})
- Artifact root: `../artifacts/chapter-{item['number']:02d}/`

This chapter notebook is written to stand alone from the scanned textbook. Use the PDF only to confirm source orientation, not as a reading dependency.
"""


def main() -> None:
    write_notebook(BOOK_ROOT / "00-book-index.ipynb", book_index())
    for item in COURSE_MAP:
        write_notebook(BOOK_ROOT / item["folder"] / "00-index.ipynb", chapter_index(item))
    print(f"Built GMAM indexes for {len(COURSE_MAP)} chapters")


if __name__ == "__main__":
    main()
'''


AUDIT_NOTEBOOKS_PY = '''"""Audit GMAM notebooks for standalone depth and structure."""

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
    text = "\\n".join(markdown)
    return {
        "path": relative(path),
        "markdown_words": len(text.split()),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "has_setup": "BOOK_ROOT" in "\\n".join(code),
        "has_sanity": "final_sanity" in "\\n".join(code),
        "has_takeaways": "Takeaways" in text,
        "has_storyboard": "Visual Storyboard" in text and "visual-storyboard.json" in "\\n".join(code),
        "has_lab": "Applied Lab" in text,
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
        for marker in ["has_setup", "has_sanity", "has_takeaways", "has_storyboard", "has_lab"]:
            if not item[marker]:
                findings.append({**item, "finding": f"missing required marker: {marker}"})
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
            print("All GMAM notebooks meet the configured depth and shape checks.")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
'''


AUDIT_VISUALS_PY = '''"""Audit GMAM visual artifacts and notebook display calls."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import artifact_topics, canonical_notebooks, code_sources, image_stats, relative  # noqa: E402

VISUAL_SAVE_CALLS = {"render_visuals", "save_matplotlib", "save_plotly_html"}


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
            item["sha256"] = sha256(png)
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
            print("All GMAM visual audit checks passed.")
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
'''


VALIDATE_COURSE_PY = '''"""Execute GMAM notebooks with nbclient."""

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
    "01-preliminary-notions.ipynb",
    "02-incidence-and-metric-geometry.ipynb",
    "05-angle-measure.ipynb",
    "08-hyperbolic-geometry.ipynb",
    "10-area.ipynb",
    "11-the-theory-of-isometries.ipynb",
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


def md(text: str):
    return nbf.v4.new_markdown_cell(textwrap.dedent(text).strip() + "\n")


def code(text: str):
    cleaned = textwrap.dedent(text).strip()
    lines = [
        line[12:] if line.startswith("            ") else line
        for line in cleaned.splitlines()
    ]
    return nbf.v4.new_code_cell("\n".join(lines) + "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")


def write_notebook(path: Path, cells: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = nbf.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    }
    nbf.write(nb, path)


def visual_specs(chapter: dict) -> list[dict[str, str]]:
    return [
        {"kind": kind, "filename": filename, "title": title, "inspection": inspection}
        for kind, filename, title, inspection in chapter["visuals"]
    ]


def storyboard_dict(chapter: dict) -> dict:
    return {
        "chapter goal": chapter["question"],
        "source span read": f"printed pages {chapter['printed']}; PDF pages {chapter['pdf']}",
        "visual sequence": [
            {
                "concept": title,
                "representation": kind,
                "library": "numpy, matplotlib, networkx or plotly as appropriate",
                "artifact filename": filename,
                "learner inspection target": inspection,
            }
            for kind, filename, title, inspection in chapter["visuals"]
        ],
        "computational checks": [
            "artifact existence and nonzero image statistics",
            "orientation, area, angle, distance, or transformation invariants appropriate to the chapter",
            "a final JSON sanity record saved under the chapter artifact subtree",
        ],
        "implementation notes": "Use course-local utilities; keep generated paths under artifacts/chapter-XX.",
        "gaps": "Proof-heavy material is made inspectable through dependency graphs, parameter labs, and small computed examples.",
    }


def expanded_teaching_text(chapter: dict) -> str:
    visuals = "\n".join(
        f"- **{title}** (`{filename}`): {inspection}"
        for _, filename, title, inspection in chapter["visuals"]
    )
    translations = "\n".join(f"- {item}" for item in chapter["translation"])
    pitfalls = "\n".join(f"- {item}" for item in chapter["pitfalls"])
    takeaways = "\n".join(f"- {item}" for item in chapter["takeaways"])
    return f"""
    ## Chapter Question

    {chapter['question']}

    The notebook treats this chapter as a working laboratory rather than as a passive reading assignment. The source chapter fixes the mathematical territory: {chapter['focus']} The presentation here rebuilds that territory with original prose, generated diagrams, numerical checks, and small symbolic or computational experiments. The goal is for a reader to leave with operational tests: given a proposed object, can they decide whether it is a model, a segment, a tangent, a parallel family, an area function, or an isometry?

    A metric approach is especially friendly to computation because definitions can be translated into predicates. A line may be a set of points satisfying an equation, a ray may be a parameter restriction, and a triangle may be an inventory of side lengths, angle measures, signed area, and incidence data. The notebooks keep that translation visible. Every visual is paired with a question about what should remain invariant, what is allowed to vary, and which hidden assumptions are being tested.

    ## Translation Guide

    {translations}

    The point of the translation guide is not to replace proof with code. It is to make the proof objects inspectable. A proof about separation can become a sign table; a proof about congruence can become an alignment experiment; a proof about hyperbolic defect can become a parameter sweep whose output has to agree with a symbolic identity. When the computation is honest, it also shows where the computation is insufficient and where a theorem must do more than sample examples.

    ## Visual Storyboard

    {visuals}

    These artifacts are generated from fresh coordinate choices and helper functions. They are not textbook figures, crops, or traced reproductions. The names describe the concept because the file should still make sense when discovered outside the notebook.

    ## Concept Route

    The chapter route has three movements. First, it names the primitives and the predicates that make those primitives usable. Second, it draws one or more model scenes where the predicates can be inspected. Third, it records checks that a reader can rerun or modify. This rhythm is repeated across the whole course because the book's central habit is comparison between models: a statement is geometric only after we know which structure it preserves.

    For this chapter, the most important practical move is to resist the temptation to trust a picture too quickly. A figure is a proposal. The checks ask whether the proposal satisfies the rule that it is supposed to illustrate. If the rule is incidence, we ask which point lies on which line. If the rule is metric, we ask whether distances satisfy the metric axioms. If the rule is angle or area, we ask which numerical invariant survives a transformation.

    ## Worked Example Thread

    The worked example thread uses deliberately small data. Small examples are not childish; they are the easiest way to see every assumption. A finite incidence model can be checked line by line. A triangle with named coordinates can expose orientation, side length, and angle data without hiding behind a polished diagram. A disk-model geodesic can be sampled and measured before the theorem is stated in its mature form.

    The examples are also designed to be editable. Change a point, move a ray, swap a metric, or compose transformations in the other order. If a claim is robust, the final checks should still pass. If a claim depends on a hypothesis, the changed example should show exactly which assertion fails.

    ## Model-Checking Habit

    The central study habit in this course is to turn every geometric sentence into three companion objects: a picture, a predicate, and a failure case. The picture makes the claim memorable. The predicate makes it testable. The failure case keeps the theorem honest by showing which hypothesis cannot be removed. This is why many chapters include deliberately small coordinate examples even when the surrounding theorem is synthetic. Small examples let the reader see the whole state of the argument at once: the givens, the constructed objects, the invariant being measured, and the exact place where a wrong model would stop satisfying the rule.

    This habit also protects the course from overfitting to Euclidean intuition. When a later chapter moves from Cartesian lines to Poincare geodesics, from ordinary triangles to hyperbolic defect, or from rigid motions to isometry groups, the workflow stays stable: define the model, build an inspectable object, compute the invariant, and ask what would break if the model changed.

    ## Pitfalls

    {pitfalls}

    These pitfalls are not side comments. They are where many geometry errors begin. The notebook turns them into tests: a vertical line tests whether a coordinate formula is partial, a nonconvex quadrilateral tests whether all edge orientations agree, and a disk arc tests whether Euclidean appearance is being confused with hyperbolic meaning.

    ## Applied Lab

    {chapter['lab']}

    In the lab, the expected deliverable is a small record of observations rather than a copied exercise solution. The reader should change parameters, inspect the generated figure, and explain which invariant survived. When the lab produces a JSON or CSV artifact, it becomes a compact audit trail: not just a result, but the assumptions and measurements that produced the result.

    ## Takeaways

    {takeaways}
    """


def notebook_for_chapter(chapter: dict) -> list:
    specs = visual_specs(chapter)
    storyboard = storyboard_dict(chapter)
    return [
        md(
            f"""
            # Chapter {chapter['number']}: {chapter['title']}

            Source orientation: printed pages {chapter['printed']}; physical PDF pages {chapter['pdf']}; sections {chapter['sections']}.

            This notebook is a standalone computational lesson inspired by the source chapter's structure. It does not copy textbook prose, long exercise text, screenshots, page crops, or figures. The scanned PDF is only a source-orientation object; the teaching prose, diagrams, code, checks, and labs below are original.
            """
        ),
        md(expanded_teaching_text(chapter)),
        code(
            f"""
            from pathlib import Path
            import sys

            CHAPTER_META = {json.dumps({k: chapter[k] for k in ['number', 'title', 'slug', 'folder', 'printed', 'pdf', 'sections', 'focus']}, indent=4)}
            VISUAL_SPECS = {json.dumps(specs, indent=4)}
            STORYBOARD = {json.dumps(storyboard, indent=4)}

            BOOK_ROOT = Path.cwd()
            for candidate in [BOOK_ROOT, *BOOK_ROOT.parents]:
                if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
                    BOOK_ROOT = candidate
                    break
            else:
                raise RuntimeError("Could not find the GMAM book root")

            if str(BOOK_ROOT) not in sys.path:
                sys.path.insert(0, str(BOOK_ROOT))

            from utils.artifacts import assert_artifacts, chapter_artifact_root, display_artifact, save_csv, save_json, save_plotly_html
            from utils.geometry import build_parameter_lab, chapter_numeric_checks, render_visuals

            ARTIFACT_ROOT = chapter_artifact_root(CHAPTER_META["number"], BOOK_ROOT)
            for child in ["figures", "html", "checks", "tables"]:
                (ARTIFACT_ROOT / child).mkdir(parents=True, exist_ok=True)

            ARTIFACT_ROOT
            """
        ),
        md(
            """
            ## Storyboard Record

            The storyboard is saved as machine-readable JSON before any figures are generated. This makes the chapter auditable: the concept, representation, artifact filename, and learner inspection target are all visible as data.
            """
        ),
        code(
            """
            storyboard_path = save_json(STORYBOARD, ARTIFACT_ROOT / "checks" / "visual-storyboard.json")
            display_artifact(storyboard_path)
            storyboard_path
            """
        ),
        md(
            """
            ## Generated Visual Explanations

            The following cell creates the chapter's visual artifacts. Each figure is built from coordinates, predicates, or transformations in the local utilities, saved under the book-local artifact tree, and displayed inline for inspection.
            """
        ),
        code(
            """
            figure_paths, visual_stats = render_visuals(ARTIFACT_ROOT, VISUAL_SPECS)
            for path in figure_paths:
                display_artifact(path, width=820)
            visual_stats
            """
        ),
        md(
            """
            ## Numeric And Symbolic Checks

            A visualization-first notebook should still leave a trail of assertions. This chapter records reusable checks for area, betweenness, angle measurement, hyperbolic distance, or transformation invariants as appropriate.
            """
        ),
        code(
            """
            checks = chapter_numeric_checks(CHAPTER_META, visual_stats)
            checks_path = save_json(checks, ARTIFACT_ROOT / "checks" / "chapter-checks.json")
            display_artifact(checks_path)
            checks
            """
        ),
        md(
            """
            ## Parameter Lab

            The parameter lab is a compact interactive companion to the static diagrams. It is saved as HTML so it can be reopened without re-executing the notebook.
            """
        ),
        code(
            """
            lab_fig = build_parameter_lab(CHAPTER_META)
            html_path = save_plotly_html(lab_fig, ARTIFACT_ROOT / "html" / "parameter-lab.html")
            display_artifact(html_path, height=460)
            html_path
            """
        ),
        md(
            """
            ## Artifact Inventory

            The inventory table is intentionally plain. It helps QC confirm that the notebook produced visible artifacts and that those artifacts live in the chapter-local subtree.
            """
        ),
        code(
            """
            inventory_rows = [
                {
                    "artifact": path.name,
                    "category": path.parent.name,
                    "bytes": path.stat().st_size,
                    "chapter": CHAPTER_META["title"],
                }
                for path in [*figure_paths, html_path, checks_path, storyboard_path]
            ]
            table_path = save_csv(inventory_rows, ARTIFACT_ROOT / "tables" / "artifact-inventory.csv")
            display_artifact(table_path)
            inventory_rows
            """
        ),
        md(
            """
            ## Final Sanity Checks

            The final cell asserts that the visible artifacts exist, are nonempty, and contain enough pixel variation to rule out blank placeholder images. It also stores a final summary JSON for later course-level audits.
            """
        ),
        code(
            """
            assert_artifacts([*figure_paths, html_path, checks_path, storyboard_path, table_path], min_bytes=64)
            assert len(figure_paths) == len(VISUAL_SPECS)
            assert checks["minimum_visual_stddev"] > 1.0
            assert checks["midpoint_between"] is True
            final_sanity = {
                "chapter": CHAPTER_META["number"],
                "artifact_count": len(inventory_rows),
                "figure_count": len(figure_paths),
                "minimum_visual_stddev": checks["minimum_visual_stddev"],
                "passed": True,
            }
            final_path = save_json(final_sanity, ARTIFACT_ROOT / "checks" / "final-sanity.json")
            display_artifact(final_path)
            final_sanity
            """
        ),
    ]


def index_markdown(chapter: dict) -> str:
    return f"""# Chapter {chapter['number']}: {chapter['title']}

- Source orientation: printed pages {chapter['printed']}; PDF pages {chapter['pdf']}; sections {chapter['sections']}.
- Focus: {chapter['focus']}
- Canonical notebook: [{chapter['number']:02d}-{chapter['slug']}.ipynb]({chapter['number']:02d}-{chapter['slug']}.ipynb)
- Artifact root: `../artifacts/chapter-{chapter['number']:02d}/`

This index is intentionally small. The canonical notebook is the teaching object; this file is the local table of contents for the chapter folder.
"""


def book_index_markdown() -> str:
    rows = [
        "| Chapter | Notebook | Printed Pages | PDF Pages | Focus |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for chapter in CHAPTERS:
        rows.append(
            f"| {chapter['number']} | [{chapter['title']}]({chapter['folder']}/{chapter['number']:02d}-{chapter['slug']}.ipynb) | "
            f"{chapter['printed']} | {chapter['pdf']} | {chapter['focus']} |"
        )
    return f"""# Geometry: A Metric Approach with Models

This is a standalone visualization-first notebook course for Richard S. Millman and George D. Parker, *Geometry: A Metric Approach with Models*, Second Edition.

The PDF in this folder is an image-only scan. It is used only for source orientation: chapter structure, page spans, concept order, and exercise themes. The notebooks do not copy textbook prose, long exercise text, screenshots, page crops, or textbook figures.

Body printed pages map to physical PDF pages by `pdf_page = printed_page + 15`.

The frontmatter note on computers and hyperbolic geometry is treated as a design cue for the whole course: every chapter turns geometric concepts into diagrams, parameter labs, model checks, symbolic or numeric assertions, and reusable artifacts.

## Chapter Route

{chr(10).join(rows)}

## How To Use The Course

Open the chapter folder, run the canonical notebook, and inspect the generated artifacts under `artifacts/chapter-XX/`. Each notebook begins with a chapter question and translation guide, then builds original visual explanations, computational checks, an applied lab, and takeaways. The `00-index.ipynb` files are navigational; the canonical notebooks are the teaching units.
"""


def main() -> None:
    write_text(BOOK_ROOT / "AGENTS.md", AGENTS_MD)
    write_text(BOOK_ROOT / "utils" / "__init__.py", UTILS_INIT)
    write_text(BOOK_ROOT / "utils" / "artifacts.py", ARTIFACTS_PY)
    write_text(BOOK_ROOT / "utils" / "plotting.py", PLOTTING_PY)
    write_text(BOOK_ROOT / "utils" / "geometry.py", GEOMETRY_PY)
    write_text(BOOK_ROOT / "utils" / "validation.py", VALIDATION_PY)
    write_text(BOOK_ROOT / "scripts" / "build_gmam_course_indexes.py", BUILD_INDEXES_PY)
    write_text(BOOK_ROOT / "scripts" / "audit_gmam_notebooks.py", AUDIT_NOTEBOOKS_PY)
    write_text(BOOK_ROOT / "scripts" / "audit_gmam_visuals.py", AUDIT_VISUALS_PY)
    write_text(BOOK_ROOT / "scripts" / "validate_gmam_course.py", VALIDATE_COURSE_PY)

    write_notebook(BOOK_ROOT / "00-book-index.ipynb", [md(book_index_markdown())])
    for chapter in CHAPTERS:
        folder = BOOK_ROOT / chapter["folder"]
        write_notebook(folder / "00-index.ipynb", [md(index_markdown(chapter))])
        write_notebook(folder / f"{chapter['number']:02d}-{chapter['slug']}.ipynb", notebook_for_chapter(chapter))
        for child in ["figures", "html", "checks", "tables"]:
            (BOOK_ROOT / "artifacts" / f"chapter-{chapter['number']:02d}" / child).mkdir(parents=True, exist_ok=True)

    print(f"Bootstrapped {COURSE_TITLE} with {len(CHAPTERS)} chapter notebooks.")


if __name__ == "__main__":
    main()
