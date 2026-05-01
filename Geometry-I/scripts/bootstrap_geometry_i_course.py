"""Bootstrap the Geometry I standalone notebook course.

This is an initial course-generation helper. Future chapter improvement work
should edit canonical notebooks directly, using the visualization planner,
chapter author, and QC skills.
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path
from typing import Any

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

BOOK_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = Path(__file__).resolve().parent
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import geometry_i_inventory as inventory  # noqa: E402
from build_geometry_i_course_indexes import main as build_indexes  # noqa: E402
from utils.chapter_visuals import build_visual_suite  # noqa: E402


EXTRA_GUIDANCE: dict[str, dict[str, str]] = {
    "introduction": {
        "question": "How can a notebook make the book's visual promise operational rather than merely repeat it?",
        "lab": "Translate a definition into a diagram, perturb the diagram, and ask which quantity refuses to change.",
        "pitfall": "The main danger is treating a figure as an ornament. In this course a figure is a controlled experiment: it has inputs, labels, and an invariant to inspect.",
    },
    "chapter-00": {
        "question": "Which background conventions become computational objects in later geometry?",
        "lab": "Build metric balls, estimate distances between small sets, and test which statements are topological and which are metric.",
        "pitfall": "Notation can feel weightless until it is attached to a check. The notebook turns symbols like balls, isometries, and compact families into small numerical experiments.",
    },
    "chapter-01": {
        "question": "What does a group action preserve, and what does it sort into equivalent pieces?",
        "lab": "Generate an orbit of a tile, count the stabilizer, and compare the visual partition with the class formula.",
        "pitfall": "It is easy to confuse the group with the space it acts on. The diagrams keep the acting transformations separate from the points, tiles, or solids being moved.",
    },
    "chapter-02": {
        "question": "What remains when geometry has points and parallelism but no privileged origin?",
        "lab": "Move an affine frame, apply a shear, and verify that collinearity and parallel families survive.",
        "pitfall": "Coordinates are useful, but an affine statement should not depend on a chosen origin. The computational checks always compare before and after changing frames.",
    },
    "chapter-03": {
        "question": "Why do weighted point combinations encode affine structure more naturally than vector addition alone?",
        "lab": "Drag a point through a triangle conceptually by changing barycentric weights and check that the weights sum to one.",
        "pitfall": "Negative barycentric weights are not errors; they signal that the affine combination has moved outside the convex hull while remaining an affine statement.",
    },
    "chapter-04": {
        "question": "How does projective geometry turn rays, charts, and perspectives into one incidence language?",
        "lab": "Intersect rays with a chart, move the chart, and watch finite coordinates change while incidence remains stable.",
        "pitfall": "A projective point is not a coordinate tuple. It is an equivalence class of nonzero homogeneous vectors, so rescaling is invisible.",
    },
    "chapter-05": {
        "question": "How does adding ideal points convert parallel behavior into ordinary incidence?",
        "lab": "Follow a family of parallel lines until they meet the same ideal point, then change the affine chart.",
        "pitfall": "The point at infinity is not a far-away Euclidean point. It records a direction and becomes finite after a projective change of chart.",
    },
    "chapter-06": {
        "question": "Which numerical quantity survives every homography of a projective line?",
        "lab": "Move four points by a fractional linear map and verify that their cross-ratio stays fixed.",
        "pitfall": "The cross-ratio has several values under permutation. The invariant statement must name the ordering or track the induced permutation.",
    },
    "chapter-07": {
        "question": "What does a real geometric object gain when complex scalars are allowed?",
        "lab": "Compare real directions with complexified ones and inspect how polynomial roots become visible in the complex plane.",
        "pitfall": "Complexification is not the same as forgetting the real object. It is a controlled extension that keeps a memory of the original real structure.",
    },
    "chapter-08": {
        "question": "How do inner products turn linear algebra into metric geometry?",
        "lab": "Rotate vectors, inspect a quadratic cone, and verify that orthogonal motion preserves lengths and angles.",
        "pitfall": "An orthogonal matrix is not just any convenient change of coordinates. It is exactly a change that preserves the quadratic measurement.",
    },
    "chapter-09": {
        "question": "How does Euclidean affine geometry classify motions and distances without losing the point-based viewpoint?",
        "lab": "Apply translations, rotations, and reflections to a shape, then compare compact sets with the Hausdorff metric.",
        "pitfall": "A rigid motion can move every coordinate while preserving all pairwise distances. The check is metric, not visual similarity alone.",
    },
    "chapter-10": {
        "question": "How do classical configurations of triangles, spheres, and circles become transformations and invariants?",
        "lab": "Compute triangle centers, invert a circle, and watch which incidences and angle patterns survive.",
        "pitfall": "Classical diagrams often hide hypotheses. The notebook states the data used by each construction and separates measured facts from conjectural patterns.",
    },
    "chapter-11": {
        "question": "How does convexity turn geometry into separation, support, and optimization?",
        "lab": "Build a convex hull, draw supporting lines, and compare a convex function with its epigraph.",
        "pitfall": "Convexity is global: every segment between points must remain in the set. Checking only the boundary or a few directions is evidence, not a proof.",
    },
}

FIGURE_NAMES: dict[str, list[tuple[str, str]]] = {
    "introduction": [
        ("Visual study loop", "visual-study-loop.png"),
        ("Example-to-invariant measurement", "example-invariant-measurement.png"),
    ],
    "chapter-00": [
        ("Metric balls and set distance", "metric-balls-and-set-distance.png"),
        ("Background notation map", "background-notation-map.png"),
    ],
    "chapter-01": [
        ("Rotation orbit of a tile", "rotation-orbit-of-a-tile.png"),
        ("Orbit-stabilizer counts", "orbit-stabilizer-counts.png"),
    ],
    "chapter-02": [
        ("Affine frame transformed grid", "affine-frame-transformed-grid.png"),
        ("Parallel lines under affine map", "parallel-lines-under-affine-map.png"),
    ],
    "chapter-03": [
        ("Barycentric coordinate lattice", "barycentric-coordinate-lattice.png"),
        ("Barycenter balance lines", "barycenter-balance-lines.png"),
    ],
    "chapter-04": [
        ("Projective rays to chart points", "projective-rays-to-chart-points.png"),
        ("Perspective lines meet at a vanishing point", "perspective-lines-meet-at-vanishing-point.png"),
    ],
    "chapter-05": [
        ("Parallel family point at infinity", "parallel-family-point-at-infinity.png"),
        ("Affine chart with ideal boundary", "affine-chart-with-ideal-boundary.png"),
    ],
    "chapter-06": [
        ("Four points on a projective line", "four-points-on-projective-line.png"),
        ("Homography cross-ratio invariance", "homography-cross-ratio-invariance.png"),
    ],
    "chapter-07": [
        ("Complexified real directions", "complexified-real-directions.png"),
        ("Complex roots on unit circle", "complex-roots-on-unit-circle.png"),
    ],
    "chapter-08": [
        ("Isotropic cone quadratic condition", "isotropic-cone-quadratic-condition.png"),
        ("Orthogonal rotations preserve length", "orthogonal-rotations-preserve-length.png"),
    ],
    "chapter-09": [
        ("Plane isometry classification panel", "plane-isometry-classification-panel.png"),
        ("Hausdorff distance compact samples", "hausdorff-distance-compact-samples.png"),
    ],
    "chapter-10": [
        ("Triangle centers and cevians", "triangle-centers-and-cevians.png"),
        ("Circle inversion experiment", "circle-inversion-experiment.png"),
    ],
    "chapter-11": [
        ("Convex hull supporting lines", "convex-hull-supporting-lines.png"),
        ("Convex function epigraph", "convex-function-epigraph.png"),
    ],
}

DEEP_DIVES: dict[str, str] = {
    "introduction": """
## Source-Specific Lens

The introduction argues for geometry as an active visual practice. In this
notebook course that becomes an engineering requirement: every chapter needs a
diagram or computation that does mathematical work. The first figure turns that
requirement into a loop. A definition is tested by a diagram; the diagram is
perturbed into examples; the examples suggest an invariant; the invariant is
checked. This is not a philosophy paragraph tucked before the mathematics. It
is the operating system for the course.

A useful way to read the introduction is to ask what makes a figure legitimate.
It is not enough that the figure looks like the intended object. The figure
must encode the data used by the claim, and it must make at least one possible
failure visible. The measurement panel models that idea. The plotted curve is
not a theorem, but it lets a reader see how repeated examples can point toward
an envelope or invariant worth proving.

The applied lab for the introduction is therefore a meta-lab. Pick a later
chapter term, such as cross-ratio, barycenter, supporting hyperplane, or
isometry. Before proving anything, build a minimal visual test for it. The
reader should be able to say which input changed, which relation survived, and
which check would fail if the definition were misunderstood.
""",
    "chapter-00": """
## Source-Specific Lens

Chapter 0 is short, but it is the control panel for the rest of the volume. Set
notation decides what counts as a restricted map. Algebra notation decides when
we are working with linear maps, groups, fields, or affine maps. Metric-space
notation decides what the words ball, diameter, distance between sets, and
isometry mean. The notebook visualizes those conventions because a convention
that cannot be tested tends to stay inert.

The metric-ball figure gives a concrete example of the distinction between a
point-to-point distance and a set-to-set distance. Two balls can be far apart,
tangent, or overlapping, and the formula changes its visible meaning in each
case. This becomes useful later when Euclidean affine spaces discuss distances
between sets and when convexity uses separating hyperplanes to certify
nonintersection.

The notation map is a study guide rather than a proof. It reminds the reader
that topology, measure, algebra, and metric language are not separate boxes.
They are reusable lenses. A later chapter may start with projective incidence
and suddenly need topology; another may begin with convex sets and need measure.
The lab asks the reader to attach a small object to each convention so the
symbol has a visual anchor.
""",
    "chapter-01": """
## Source-Specific Lens

Group actions become vivid when the acting group and the acted-on space are
drawn separately. The tile-orbit figure fixes one tile and applies rotations to
produce a visible orbit. The center is not itself the orbit; it is part of the
stabilizer story. That distinction matters in tilings, crystallographic groups,
and symmetric solids, where the same group element can move a tile, preserve a
vertex, or permute a whole configuration.

The bar chart records the simplest orbit-stabilizer certificate. It is small
on purpose: a group of size twelve, an orbit of six visible placements, and a
stabilizer of size two. The diagram invites a reader to predict what would
happen if the marked tile had less symmetry. The orbit would grow, the
stabilizer would shrink, and the product would stay fixed.

The worked habit is to replace the phrase "symmetry group" by a concrete
question: what is being moved, and which moves are invisible at the chosen
object? This same habit prepares the later chapters on Euclidean isometries,
projective homographies, and orthogonal groups. A transformation is understood
by the structure it preserves and the equivalence classes it creates.
""",
    "chapter-02": """
## Source-Specific Lens

Affine geometry removes the privileged origin but keeps the ability to compare
directions, parallelism, and ratios along a line. The transformed-grid figure
shows this visually. The gray grid is a coordinate convenience; the colored
grid is its affine image. Distances and angles may change, but straight lines
remain straight and parallel families remain parallel.

The second figure isolates that invariant. A family of parallel lines is sent
through an affine transformation, and the image is still a parallel family.
This is the geometric content behind affine frames and affine maps. Coordinates
are helpful, but the statement is not about the coordinate axes themselves. It
is about incidence and parallelism surviving a legal change.

Classical results such as Thales, Pappus, and Desargues can be read in this
notebook style as robustness tests. If the theorem is affine, changing the
frame should not destroy it. A good lab extension is to draw the construction
in one coordinate frame, apply a shear, and verify that the intended incidences
remain while Euclidean measurements drift.
""",
    "chapter-03": """
## Source-Specific Lens

Barycentric coordinates are affine coordinates built from points rather than
from an origin and basis. The lattice inside the triangle shows the most
friendly case: nonnegative weights summing to one. Each point in the colored
lattice is a weighted average of the three vertices, and the color records how
much of one vertex participates in the blend.

The balance-line figure emphasizes that the same formula remains affine even
outside the triangle. The requirement is that the weights sum to one, not that
they all be positive. Positive weights give convex combinations; negative
weights give affine combinations outside the convex hull. This distinction is
essential when barycenters become a bridge from finite point configurations to
the universal affine space.

The computational check reconstructs a point from its barycentric weights and
records the error. That small check is the chapter's motto: affine information
is preserved by the right weighted sums. The lab extension is to move the
point, watch the weights change, and mark the exact moment when one weight
crosses zero.
""",
    "chapter-04": """
## Source-Specific Lens

Projective space begins with the decision to treat nonzero scalar multiples as
the same point. The ray-to-chart figure makes this visible: many rays leave the
origin, and a chart records where each ray cuts a chosen line. Moving the chart
would change the coordinate value, but not the ray itself. That is the core
lesson of homogeneous coordinates.

The perspective figure turns projective equivalence into an applied scene.
Lines that look parallel in an affine drawing can meet at a vanishing point
under projection. Aerial photography, central projection, and projective
charts all share this idea: apparent coordinates depend on the viewing plane,
while incidence remains the durable object.

The notebook's computational lab samples a Mobius-style transformation because
the one-dimensional projective case is easy to calculate and hard to fake. The
important habit is to ask whether a statement is phrased in chart coordinates
or in projective incidence. Only the latter deserves to be called projective.
""",
    "chapter-05": """
## Source-Specific Lens

The affine-projective relationship is the moment where parallelism becomes
ordinary incidence. The parallel-family figure shows several affine lines with
the same direction. In projective completion, they share an ideal point. That
point is not infinitely far away in a metric sense; it is a bookkeeping device
for direction.

The chart-with-boundary figure separates finite chart data from ideal data.
Changing the chart can make an ideal point finite or send a finite object to
the line at infinity. This is why projective completion is more than adding a
decorative boundary. It enlarges the language so exceptional affine cases can
be handled uniformly.

The applied lab asks the reader to send objects to infinity deliberately. If a
calculation becomes simpler after that move, the projective viewpoint has done
real work. The later chapters on cross-ratios, conics, circles, and inversions
all benefit from this same habit of removing special cases by changing the
ambient projective frame.
""",
    "chapter-06": """
## Source-Specific Lens

The projective line is a compact laboratory for invariants. Four ordered
points carry a cross-ratio. The first figure marks those points in one chart;
the second moves them by a homography and plots both a raw coordinate and the
cross-ratio. The raw coordinate moves. The cross-ratio remains flat.

This is the chapter's key visual lesson. Projective transformations can be very
active at the coordinate level while preserving a deeper relationship among
points. Harmonic division, involutions, and duality all exploit that gap
between coordinate motion and projective structure. A reader who watches only
the moving points misses the invariant; a reader who watches only the formula
misses why the invariant is geometric.

The lab is intentionally numerical but exact in spirit. It computes the
cross-ratio before and after a fractional linear transformation and records the
error. A useful extension is to permute the four labels. The invariant does not
disappear, but it changes by one of the standard six related values, which is
why ordering must be named.
""",
    "chapter-07": """
## Source-Specific Lens

Complexification extends the allowed scalars while keeping track of the real
object that was extended. The first figure shows a real line together with
imaginary variations. It is not meant as a literal drawing of a high-dimensional
complex vector space; it is a chart of the new degrees of freedom that appear
when real coordinates gain imaginary partners.

The roots-on-a-circle figure gives a familiar reason to complexify. A
polynomial can hide its full structure over the real numbers and reveal it over
the complex numbers. The same principle affects vector spaces, affine spaces,
projective spaces, and morphisms: extending scalars can make structure more
regular while still remembering the real source.

The chapter's lab checks root moduli on the unit circle. The check is small,
but the habit is large. Whenever a real construction is complexified, ask what
becomes simpler, what new points appear, and how the original real locus sits
inside the complexified space.
""",
    "chapter-08": """
## Source-Specific Lens

Euclidean vector spaces are vector spaces with a measurement device. The
orthogonal-action figure rotates vectors on the unit circle and checks that
length is preserved. That one picture contains the seed of the orthogonal
group: the legal transformations are exactly those that leave the inner
product, and therefore lengths and angles, unchanged.

The isotropic-cone figure shifts attention to a quadratic condition. In
positive-definite Euclidean geometry the equation of zero length has only the
zero vector, but related quadratic geometries make cones of null directions
visible. This prepares the reader for later quadratic forms without leaving the
visual language of level sets and preserved quantities.

The lab records the norm before and after rotation. It is deliberately simple
because the same check scales upward: matrices in the orthogonal group preserve
the Gram matrix, quaternions encode rotations, and conical volume forms track
how angular data interacts with metric structure.
""",
    "chapter-09": """
## Source-Specific Lens

Euclidean affine geometry combines point-based affine language with Euclidean
measurement. The isometry panel shows a shape under translation, rotation, and
reflection. Coordinates change everywhere, but pairwise distances remain. This
is the practical test for a rigid motion and the gateway to classifying plane
isometries by generators.

The Hausdorff-distance figure moves from point-to-point distances to distances
between compact samples. This matters because the chapter discusses not only
individual points and rigid motions but also subsets, curves, measure, and
symmetrization. Geometry becomes a way to compare whole shapes.

The lab asks the reader to trust the metric check over visual resemblance.
Two shapes may look similar because of plotting scale, and two coordinate
tables may look unrelated even when an isometry connects them. The invariant is
distance, so the computation records distance preservation explicitly.
""",
    "chapter-10": """
## Source-Specific Lens

The chapter on triangles, spheres, and circles is a gallery of classical
objects, but the notebook treats the gallery as a set of transformations and
invariants. The triangle-centers figure marks a centroid and its cevians so the
reader can inspect how a center summarizes a configuration rather than merely
decorate it.

The inversion figure gives the chapter a dynamic test. A circle is transformed
through inversion, and distances from the inversion center trade near and far.
This single transformation connects circle geometry, angle behavior, and
projective-looking exceptional cases. It also warns the reader that a familiar
Euclidean picture can become simpler after a non-Euclidean-looking move.

The lab records the radius product under inversion. The check is a compact way
to remember the transformation: a point and its inverse lie on the same ray and
their distances from the center multiply to the square of the inversion radius.
That fact is the computational handle for many circle configurations.
""",
    "chapter-11": """
## Source-Specific Lens

Convexity is the geometry of segments, support, and separation. The convex-hull
figure starts with scattered points, draws the hull, and overlays supporting
directions. A support line is a certificate: it says the set lies on one side
while the line touches the boundary in the measured direction.

The epigraph figure translates a function into a set. A function is convex
when the region above its graph is convex. This visual shift is powerful
because it turns inequalities into geometry. Separation theorems, supporting
hyperplanes, and optimization arguments can then be read as statements about
sets rather than only formulas.

The lab compares hull vertices, support values, and epigraph behavior. A good
extension is to perturb a point cloud and ask which supports change. That
experiment captures the chapter's broader theme: convex objects are stable
enough to be measured globally, but their boundary certificates can change in
very local ways.
""",
}


def _topic_bullets(entry: dict[str, Any]) -> str:
    return "\n".join(f"- {topic}" for topic in entry["topics"])


def _relative_artifact_link(entry: dict[str, Any], filename: str) -> str:
    notebook_dir = BOOK_ROOT / entry["folder"]
    artifact = BOOK_ROOT / "artifacts" / entry["artifact_topic"] / "figures" / filename
    return Path("../" * len(notebook_dir.relative_to(BOOK_ROOT).parts)).joinpath(
        artifact.relative_to(BOOK_ROOT)
    ).as_posix()


def _static_visual_markdown(entry: dict[str, Any]) -> str:
    lines = [
        "## Static Visual Preview",
        "",
        "These generated images are embedded directly so the notebook still reads as a visual lesson before code execution. Running the notebook rebuilds the same artifacts and verifies them.",
        "",
    ]
    for caption, filename in FIGURE_NAMES[str(entry["id"])]:
        lines.extend([f"**{caption}.**", "", f"![{caption}]({_relative_artifact_link(entry, filename)})", ""])
    return "\n".join(lines)


def _storyboard(entry: dict[str, Any]) -> str:
    topic_list = "; ".join(entry["topics"])
    return f"""
## Visualization Storyboard

The storyboard for this source unit is compact but explicit. The source span is
printed `{entry['printed_span']}` and PDF `{entry['pdf_span']}`. The notebook
uses that span to orient the concepts, then builds original diagrams and checks
around the following teaching target:

**Chapter goal.** {entry['focus']}

**Visual sequence.** First, a structural diagram names the objects that will be
manipulated. Second, a computational figure varies a parameter or changes a
coordinate system so the reader can see what moves and what stays fixed. Third,
the applied lab records a small numerical or symbolic check in the artifact
tree. The visual sequence is intentionally not a copy of the book's pictures;
it is a fresh computational model of the same geometry.

**Concept inventory.** {topic_list}.

**Inspection target.** The reader should ask three questions of every figure:
what object is being acted on, what operation is being applied, and what
relationship remains invariant after the operation. This is the habit that lets
the notebook stand alone from the scanned PDF.
"""


def _long_teaching_markdown(entry: dict[str, Any]) -> str:
    guide = EXTRA_GUIDANCE[str(entry["id"])]
    topics = _topic_bullets(entry)
    return f"""
# {entry['label']}: {entry['title']}

Source span: printed `{entry['printed_span']}`, PDF `{entry['pdf_span']}`.

## Chapter Question

{guide['question']}

This notebook is a standalone computational lesson inspired by the source span,
not a transcription of it. The purpose is to turn the chapter's geometric
language into things a reader can inspect: labeled points, transformed grids,
orbits, ratios, cones, hulls, curves, and small numerical certificates. The
scanned PDF remains useful as a historical and structural source, but the
reader should be able to learn the mathematical route here without opening it.

## Translation Guide

The chapter's ideas are translated into a small computational vocabulary:

{topics}

The translation is deliberately concrete. A point becomes an array only after
we decide which coordinate chart is being used. A transformation becomes a
matrix, a fractional linear expression, or a callable map only after we state
the object it acts on. An invariant becomes an assertion, a repeated
measurement, or a JSON record in the artifact directory. The notebook keeps
these layers separate because many mistakes in geometry come from mixing them:
coordinates are not points, drawings are not proofs, and numerical evidence is
not the same as a theorem. They are still valuable when they are labeled and
checked.

The central visual habit is to pair each construction with an inspection
target. When a grid is sheared, inspect which lines remain parallel. When rays
hit a projective chart, inspect which incidences survive after coordinates
change. When four points on a line move under a homography, inspect the
cross-ratio rather than the raw coordinates. When a convex hull is drawn,
inspect the supporting directions rather than only the polygon outline. This
habit is the thread connecting the whole course.

## Route Through The Notebook

1. Set up the course-local import path and artifact helpers.
2. Build the chapter's visual suite under `artifacts/{entry['artifact_topic']}`.
3. Display the generated figures inline and identify what each one is meant to
   reveal.
4. Run a short computational lab that records a check tied to the chapter's
   invariant.
5. Save a final sanity report so later audits can verify that the notebook
   generated nonempty, nonblank artifacts.

## Conceptual Development

The source unit is organized around a movement from definitions to usable
geometric tests. Definitions fix the legal moves: which transformations count,
which objects are equivalent, which coordinates are only auxiliary, and which
measurements are meaningful. Examples then supply stress tests. A good example
should do at least one of three things: make the definition visible, expose a
failure mode, or reveal a quantity that deserves to be invariant. The notebook
therefore treats every figure as an experiment with a mathematical purpose.

For this chapter the most important working claim is: {entry['focus']} The
claim is too large to absorb as text alone, so the notebook splits it into a
diagram, a parameterized computation, and a final check. The diagram establishes
the objects. The computation changes something visible. The check records the
quantity that should not change, or records the diagnostic that tells us how a
construction behaves.

## Worked Example Strategy

The worked examples are intentionally small. They use only enough coordinates
to make the geometry inspectable. Small examples are easier to falsify, easier
to redraw, and easier to connect to a theorem. A triangle can demonstrate
affine weights; four points can demonstrate a projective invariant; a handful
of sample points can demonstrate a convex hull and its supports. Once the
reader sees the invariant in a small case, the general statement has something
to attach to.

The examples also distinguish exact structure from sampled evidence. If a
calculation is exact or algebraic, the notebook says so. If it is a numerical
sample, the notebook treats it as an exploratory lens. This distinction matters
because the visual-first standard is not a license to replace proof with
pictures. It is a way to make proof goals visible before the formal argument
arrives.

{DEEP_DIVES[str(entry["id"])]}

## Pitfalls

{guide['pitfall']}

Another recurring pitfall is over-trusting the coordinate system. Coordinates
are a chosen language, not the geometry itself. The notebook repeatedly changes
frames, charts, or parameters to force this issue. If the statement is truly
geometric, the right relationship survives the change. If it does not survive,
the visual failure is not a nuisance; it is useful information about the
hypotheses.

## Applied Lab

{guide['lab']}

The lab is lightweight by design. It leaves behind a table and a JSON summary
in the artifact subtree. Those files make the notebook auditable: a later QC
pass can check that figures exist, images are nonblank, and the relevant
numeric identity has been recorded. The lab also gives the reader a pattern for
extending the chapter: change the input, rerun the suite, and compare the
reported invariant.

## Takeaways

- A standalone geometry notebook should define the objects, show them, change
  them, and check the invariant.
- The source PDF orients the chapter, but the learning product here is original
  prose, code, figures, and computational evidence.
- Every artifact should answer a visible mathematical question rather than
  merely decorate the page.
- The final sanity checks are part of the teaching contract: they make the
  visual work reproducible and inspectable.
"""


def _setup_cell(entry: dict[str, Any]) -> str:
    return f"""
from pathlib import Path
import json
import sys


def discover_book_root(start=Path.cwd()):
    start = Path(start).resolve()
    for candidate in [start, *start.parents]:
        if (candidate / "Geometry-I.pdf").exists():
            return candidate
    raise RuntimeError("Could not locate Geometry-I.pdf")


BOOK_ROOT = discover_book_root()
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.artifacts import assert_artifacts_nonempty, display_artifact, image_nonblank, save_json
from utils.chapter_visuals import build_visual_suite, run_geometry_checks

ENTRY_ID = {entry['id']!r}
ARTIFACT_TOPIC = {entry['artifact_topic']!r}
VISUAL_KEY = {entry['visual_key']!r}
TITLE = {entry['title']!r}

BOOK_ROOT
"""


def _build_visual_cell() -> str:
    return """
suite = build_visual_suite(ARTIFACT_TOPIC, VISUAL_KEY, TITLE)
suite
"""


def _display_cell() -> str:
    return """
for visual_path in suite["visuals"]:
    display_artifact(visual_path, width=760)
"""


def _inspect_cell() -> str:
    return """
summary_path = Path(suite["summary"])
summary = json.loads(summary_path.read_text(encoding="utf-8"))
summary["geometry_checks"]
"""


def _lab_cell() -> str:
    return """
lab_checks = run_geometry_checks(VISUAL_KEY)
lab_checks
"""


def _sanity_cell() -> str:
    return """
artifact_sizes = assert_artifacts_nonempty([*suite["visuals"], suite["summary"], suite["table"]])
image_reports = {Path(path).name: image_nonblank(path) for path in suite["visuals"]}
final_sanity = {
    "entry_id": ENTRY_ID,
    "artifact_topic": ARTIFACT_TOPIC,
    "artifact_sizes": artifact_sizes,
    "image_reports": image_reports,
    "geometry_checks": lab_checks,
}
final_path = save_json(final_sanity, ARTIFACT_TOPIC, "final-sanity.json")
assert final_path.exists()
final_sanity
"""


def make_notebook(entry: dict[str, Any]) -> nbformat.NotebookNode:
    cells = [
        new_markdown_cell(_long_teaching_markdown(entry)),
        new_markdown_cell(_storyboard(entry)),
        new_markdown_cell(_static_visual_markdown(entry)),
        new_code_cell(textwrap.dedent(_setup_cell(entry)).strip() + "\n"),
        new_markdown_cell(
            "## Build the visual suite\n\n"
            "This cell creates the chapter-specific artifacts. The filenames name the concept they represent, and the builder records image and geometry checks in JSON."
        ),
        new_code_cell(textwrap.dedent(_build_visual_cell()).strip() + "\n"),
        new_markdown_cell(
            "## Inspect the figures\n\n"
            "The figures are displayed inline so the reader can connect the prose to the generated artifacts. Rerunning the notebook regenerates the same visual evidence."
        ),
        new_code_cell(textwrap.dedent(_display_cell()).strip() + "\n"),
        new_markdown_cell(
            "## Read the computational certificate\n\n"
            "The summary file is small but important: it turns the visual output into an auditable object."
        ),
        new_code_cell(textwrap.dedent(_inspect_cell()).strip() + "\n"),
        new_markdown_cell(
            "## Applied Lab\n\n"
            "The lab repeats the chapter's core check without relying on the figure output. It is intentionally small enough to modify."
        ),
        new_code_cell(textwrap.dedent(_lab_cell()).strip() + "\n"),
        new_markdown_cell(
            "## Final Sanity Checks\n\n"
            "The notebook finishes by asserting that artifacts exist, are nonempty, and have nonblank image statistics. These checks are part of the course contract."
        ),
        new_code_cell(textwrap.dedent(_sanity_cell()).strip() + "\n"),
    ]
    return new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
    )


def write_notebooks() -> None:
    for entry in inventory.ENTRIES:
        folder = BOOK_ROOT / entry["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        nbformat.write(make_notebook(entry), folder / entry["notebook"])


def make_artifact_dirs() -> None:
    for entry in inventory.ENTRIES:
        for kind in ["figures", "html", "checks", "tables"]:
            (BOOK_ROOT / "artifacts" / entry["artifact_topic"] / kind).mkdir(parents=True, exist_ok=True)


def materialize_artifacts() -> None:
    for entry in inventory.ENTRIES:
        build_visual_suite(entry["artifact_topic"], entry["visual_key"], entry["title"])


def main() -> None:
    make_artifact_dirs()
    write_notebooks()
    build_indexes()
    materialize_artifacts()
    print(f"Bootstrapped {len(inventory.ENTRIES)} Geometry I notebooks")


if __name__ == "__main__":
    main()
