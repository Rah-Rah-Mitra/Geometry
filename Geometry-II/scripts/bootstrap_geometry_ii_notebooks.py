"""Bootstrap Geometry II canonical notebooks from chapter metadata.

This is intentionally course-local: it creates the first standalone notebook
edition for an empty book folder and can be rerun for selected chapters with
``--force`` when a chapter is deliberately regenerated.
"""

from __future__ import annotations

import argparse
import textwrap
from dataclasses import dataclass
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


BOOK_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Chapter:
    number: int
    title: str
    slug: str
    notebook: str
    printed_pages: str
    pdf_pages: str
    focus: str
    objects: str
    invariants: str
    misconceptions: str
    lab: str
    visuals: tuple[str, str, str]
    takeaways: tuple[str, str, str, str]

    @property
    def folder(self) -> Path:
        return BOOK_ROOT / self.slug


CHAPTERS = [
    Chapter(
        12,
        "Polytopes; Compact Convex Sets",
        "chapter-12-polytopes-compact-convex-sets",
        "12-polytopes-compact-convex-sets.ipynb",
        "1-85",
        "10-94",
        "convex hulls, volume and area, regular polytopes, Euler characteristic, Cauchy rigidity, approximation, and isoperimetry",
        "finite convex hulls, support lines, regular polygons and polyhedra, compact bodies, surface area, and approximating families",
        "convex hull containment, signed area, monotone improvement of polygonal approximations, and Euler characteristic checks",
        "The common trap is to treat a polytope as a picture of flat faces rather than as a finite system of inequalities, vertices, incidence data, and limiting comparisons with smooth bodies.",
        "Approximate the unit disk with regular n-gons, watch the area error shrink, and compare that stable numerical behavior with the purely combinatorial invariant V - E + F.",
        (
            "Convex hull and regular polygon approximation plotted as inspectable planar objects.",
            "A wireframe cube/octahedron incidence check for Euler characteristic.",
            "A JSON/CSV audit of area convergence and V - E + F.",
        ),
        (
            "Convexity is best learned by moving between hulls, half-planes, and support functions.",
            "Area and volume formulas become trustworthy when paired with convergence experiments.",
            "Euler characteristic is combinatorial but survives geometric deformation of convex polyhedra.",
            "Rigidity and isoperimetry are global statements, so the notebook treats examples as probes rather than proofs by picture.",
        ),
    ),
    Chapter(
        13,
        "Quadratic Forms",
        "chapter-13-quadratic-forms",
        "13-quadratic-forms.ipynb",
        "86-115",
        "95-124",
        "signatures, isotropic cones, radicals, orthogonalization, Witt decomposition, and reflection factorizations",
        "symmetric matrices, level sets, null cones, radicals, orthogonal complements, and reflection maps",
        "rank, signature, nullity, orthogonality with respect to a form, and invariance under congruence",
        "A positive definite mental model is too narrow: indefinite forms have visible null directions, and degenerate forms have whole directions that the form cannot detect.",
        "Classify several forms by their eigenvalue signs, then draw the level sets and null cone that make the signs geometrically visible.",
        (
            "Contour gallery for positive, indefinite, and degenerate quadratic forms.",
            "A three-dimensional isotropic cone for a form of signature (2,1).",
            "A JSON check of signatures and reflection preservation.",
        ),
        (
            "A quadratic form is a geometry once it decides which directions are positive, negative, or invisible.",
            "Orthogonality depends on the form, not only on the Euclidean dot product used to draw the page.",
            "Null cones turn algebraic sign data into a visible boundary between causal types of directions.",
            "Reflection and Witt-style decompositions are easier to inspect after the form is diagonalized.",
        ),
    ),
    Chapter(
        14,
        "Projective Quadrics",
        "chapter-14-projective-quadrics",
        "14-projective-quadrics.ipynb",
        "116-145",
        "125-154",
        "homogeneous quadrics, pencils, topology, polarity, tangent geometry, and projective group actions",
        "homogeneous coordinates, symmetric matrices up to scale, projective charts, polar hyperplanes, tangent lines, and pencils",
        "projective incidence, bilinear polarity symmetry, rank, degeneracy, and invariance under projective coordinate changes",
        "A quadric in projective space is not just an affine surface with an added horizon; the horizon can change the topology and the meaning of tangency.",
        "Move exterior points around a conic, draw their polar lines, and use a pencil of conics to see how rank and contact change inside one projective family.",
        (
            "Unit conic with exterior points, polars, and contact intuition.",
            "A pencil of conics shown through several affine chart contours.",
            "A JSON polarity check using p^T Q q = q^T Q p.",
        ),
        (
            "Homogeneous equations make scale irrelevant but preserve incidence.",
            "Polarity is a correspondence created by the quadric's bilinear form.",
            "Pencils organize many quadrics into a one-parameter experiment with visible degeneracies.",
            "The affine chart is a viewing window, not the projective object itself.",
        ),
    ),
    Chapter(
        15,
        "Affine Quadrics",
        "chapter-15-affine-quadrics",
        "15-affine-quadrics.ipynb",
        "146-169",
        "155-178",
        "affine classification, real and complex quadrics, topology, polarity, and Euclidean models",
        "quadratic and linear terms, centers, translations, Euclidean reductions, ellipsoids, paraboloids, hyperboloids, and tangent planes",
        "rank of the quadratic part, signature after translation, residual linear terms, and Euclidean normalization",
        "The affine terms are not cosmetic; translating to the center can change a messy equation into a recognizable normal form, while missing centers signal parabolic behavior.",
        "Reduce examples to normal form, draw representative surfaces, and connect the matrix signature to the visible topology of each real quadric.",
        (
            "A 3D gallery of ellipsoid, hyperboloid, and paraboloid models.",
            "A contour slice comparing centered and parabolic affine equations.",
            "A JSON classification record of signatures and centers.",
        ),
        (
            "Affine quadrics are projective quadrics seen through a chosen hyperplane at infinity.",
            "Translations remove linear terms only when the quadratic part sees the relevant direction.",
            "The signature of the quadratic part predicts whether a real surface closes, opens, or splits.",
            "Topology enters through the real locus, not through the equation alone.",
        ),
    ),
    Chapter(
        16,
        "Projective Conics",
        "chapter-16-projective-conics",
        "16-projective-conics.ipynb",
        "170-217",
        "179-226",
        "parametrized conics, cross-ratios, Pascal's theorem, homographies, intersections, Bezout, and conic pencils",
        "projective lines, rational parametrizations, six-point configurations, opposite-side intersections, homographies, and conic pencils",
        "cross-ratio preservation, collinearity of Pascal points, intersection multiplicity, and residuals in a homogeneous equation",
        "It is tempting to draw a conic as an ellipse and forget the projective line that parametrizes it. The parametrization is the engine behind the theorems.",
        "Sample six points on a conic, build the Pascal line computationally, then verify that a projective homography preserves cross-ratio.",
        (
            "A Pascal configuration with six points, opposite sides, and the Pascal line.",
            "A cross-ratio invariance experiment under a fractional linear map.",
            "A JSON residual check for conic incidence and collinearity.",
        ),
        (
            "A nondegenerate conic is projectively a line with a quadratic embedding.",
            "Cross-ratio is the portable coordinate on that line.",
            "Pascal's theorem turns six incidences into a collinearity condition that can be measured.",
            "Bezout-style counting becomes concrete when residuals and multiplicities are checked in examples.",
        ),
    ),
    Chapter(
        17,
        "Euclidean Conics",
        "chapter-17-euclidean-conics",
        "17-euclidean-conics.ipynb",
        "218-254",
        "227-263",
        "metric conics, focal and directrix views, cyclic points, tangential pencils, ellipses, and hyperbolas",
        "ellipses, hyperbolas, foci, directrices, eccentricity, tangents, normals, confocal families, and cyclic points",
        "constant sum or difference of focal distances, eccentricity ratios, tangent reflection laws, and metric invariants",
        "A projective conic becomes a Euclidean conic only after a metric is chosen; foci and distances are additional structure, not part of the bare projective curve.",
        "Measure focal sums and differences along sampled points, then compare ellipse and hyperbola behavior with the same code.",
        (
            "Ellipse and hyperbola drawn with foci and sample distance segments.",
            "A confocal family slice showing how metric parameters move while projective type remains organized.",
            "A JSON check of focal invariants and eccentricity.",
        ),
        (
            "Metric data enriches a projective conic with distance, angle, focus, and directrix structure.",
            "Ellipses and hyperbolas can be distinguished by a simple invariant along sampled points.",
            "Confocal families make tangent and normal behavior visible as a moving system.",
            "Cyclic points explain why some metric statements have a projective shadow.",
        ),
    ),
    Chapter(
        18,
        "The Sphere for Its Own Sake",
        "chapter-18-the-sphere-for-its-own-sake",
        "18-the-sphere-for-its-own-sake.ipynb",
        "255-317",
        "264-326",
        "charts, projections, topology, canonical measure, intrinsic metric, spherical triangles, Clifford parallelism, Villarceau circles, and the Mobius group",
        "sphere charts, stereographic projection, great circles, spherical triangles, surface measure, intrinsic distance, and Hopf-style circle families",
        "unit-length constraints, angular distance, chart distortion, area element behavior, and preservation of circles under stereographic projection",
        "The sphere is not a flat map with curved longitude lines. Its intrinsic geometry lives in angular distance and surface measure, while charts trade local convenience for distortion.",
        "Project great circles and latitude circles stereographically, then compare spherical side lengths in a triangle with the Euclidean drawing of its chart.",
        (
            "A sphere with great circles paired with a stereographic chart.",
            "A spherical triangle with angular side lengths.",
            "A JSON check of unit constraints and spherical distances.",
        ),
        (
            "A chart is a measurement device, not a replacement for the sphere.",
            "Great circles are geodesics because they are plane sections through the origin.",
            "Stereographic projection keeps circles visible but distorts lengths and areas.",
            "Spherical triangles expose the difference between intrinsic and planar angle intuition.",
        ),
    ),
    Chapter(
        19,
        "Elliptic and Hyperbolic Geometry",
        "chapter-19-elliptic-and-hyperbolic-geometry",
        "19-elliptic-and-hyperbolic-geometry.ipynb",
        "318-348",
        "327-357",
        "elliptic geometry, projective and ball models, distance formulas, isometries, measures, geodesics, and Poincare models",
        "antipodal sphere quotients, Klein disk, Poincare disk, geodesics, projective chords, circular arcs, and hyperbolic distance",
        "distance formula consistency, geodesic model changes, invariance under disk rotations, and boundary behavior",
        "The disk boundary is not an extra circle of ordinary points. It is the ideal boundary, and distances grow without bound as a point approaches it.",
        "Draw geodesics in the Poincare disk, compare straight Euclidean chords with circular hyperbolic geodesics, and verify distance invariance under a rotation.",
        (
            "Poincare disk geodesics as arcs orthogonal to the boundary.",
            "A distance experiment showing boundary blow-up and rotation invariance.",
            "A JSON check for Poincare distance preservation.",
        ),
        (
            "Elliptic geometry identifies antipodal directions; hyperbolic geometry uses a boundary as infinity.",
            "Different models can encode the same geometry with different-looking geodesics.",
            "The Poincare model preserves angles but not Euclidean lengths.",
            "Distance formulas turn model pictures into measurable geometry.",
        ),
    ),
    Chapter(
        20,
        "The Space of Spheres",
        "chapter-20-the-space-of-spheres",
        "20-the-space-of-spheres.ipynb",
        "349-362",
        "358-371",
        "generalized spheres, the fundamental quadratic form, orthogonality, sphere intersections, pencils, circular group, and polyspheric coordinates",
        "oriented circles and spheres, generalized planes, sphere pencils, orthogonality conditions, circular transformations, and coordinate models",
        "power of a point, orthogonality residuals, coaxal pencil structure, and preservation of circle incidence under circular transformations",
        "A sphere can be treated as a point in a larger quadratic space. That shift is abstract, but it becomes concrete when circle intersections and orthogonality are computed.",
        "Represent circles by centers and radii, draw orthogonal examples, and lift a coaxal pencil into a three-dimensional parameter plot.",
        (
            "A planar circle family with explicit orthogonality and intersection checks.",
            "A 3D plot of a coaxal pencil in center-radius coordinates.",
            "A JSON check of orthogonality residuals and pencil data.",
        ),
        (
            "Generalized spheres include ordinary spheres, planes, and oriented limiting cases.",
            "Orthogonality is a quadratic relation on sphere data.",
            "Pencils organize spheres through shared base conditions or limiting points.",
            "The circular group is natural once spheres are viewed as coordinates in a larger form.",
        ),
    ),
]


def markdown_for(chapter: Chapter) -> list[str]:
    visual_lines = "\n".join(f"- {item}" for item in chapter.visuals)
    takeaway_lines = "\n".join(f"- {item}" for item in chapter.takeaways)
    return [
        f"""# Chapter {chapter.number}: {chapter.title}

Source orientation: printed Volume II pages {chapter.printed_pages}; PDF pages {chapter.pdf_pages}. This notebook is an original visualization-first lesson based on the chapter structure and concepts, not a substitute scan or excerpt.

The chapter question is: how can we turn {chapter.focus} into objects that can be drawn, measured, transformed, and checked? The answer throughout this notebook is to treat definitions as computational contracts. A convex body becomes hull data and supporting inequalities; a form becomes a symmetric matrix with a visible signature; a conic, sphere, or hyperbolic model becomes an object whose invariants can be probed by code.

The notebook is meant to stand on its own. It introduces the working vocabulary, builds diagrams from scratch, runs small numerical checks, and ends with a lab that can be modified without reopening the book. The source pages are used for orientation: they tell us which ideas belong together, where the chapter puts emphasis, and which examples are worth turning into inspectable experiments.
""",
        f"""## Translation guide

- Objects: {chapter.objects}.
- Invariants: {chapter.invariants}.
- Main misconception to disarm: {chapter.misconceptions}
- Computational rule of thumb: start from the algebraic representation, draw the geometric locus, then assert the quantity that should not change.

This translation guide is deliberately practical. It does not try to reproduce every proof. Instead it asks which parts of a proof have a state that can be inspected: an incidence relation, a sign pattern, a limiting family, a deformation, a distance comparison, or a rank calculation. When the theorem is global, the notebook uses examples as probes and labels them as probes. When the claim is an identity, the notebook makes the identity executable.
""",
        f"""## Route through the chapter

1. Build a small dictionary of the chapter's objects and the numerical representation used in the notebook.
2. Draw the primary geometric situation with labels and stable axes.
3. Vary a parameter or compare related models so the invariant has something to resist.
4. Save artifacts under `artifacts/chapter-{chapter.number:02d}` and display them inline.
5. Run sanity checks that assert the relevant residuals, distances, signatures, or incidence relations.

The point of this route is not speed. It is to make the reader's eye and the computer agree about what the geometry says. If a diagram is attractive but no invariant is named near it, it is not yet doing mathematical work. If a formula is true but nothing in the notebook lets the reader inspect the objects it relates, the lesson is too thin.
""",
        f"""## Visualization storyboard

{visual_lines}

Each visual is paired with a check. The checks are intentionally small and readable: area ratios, matrix signatures, collinearity residuals, distance invariance, and orthogonality errors. This keeps the chapter honest. The plotted object is not a decoration; it is the front end for a reproducible computation.
""",
        f"""## Concept frame

The central objects of this chapter can be read at three levels. First there is a synthetic level: points, lines, planes, spheres, tangencies, and intersections. Second there is an algebraic level: coordinates, matrices, determinants, ranks, signatures, and residuals. Third there is a metric or topological level when the chapter asks for length, area, angle, orientation, compactness, or connectedness. A standalone notebook has to keep those levels visible at the same time.

The diagrams below are therefore built from data rather than imported as fixed pictures. That choice matters. If the reader changes a parameter, the artifact changes with it and the check either continues to pass or reveals exactly which assumption was broken. This is especially useful in Berger's style of geometry, where an object is often introduced synthetically and then compared with an affine, projective, Euclidean, spherical, or hyperbolic model.

The chapter also rewards paying attention to degeneracy. Degenerate cases are not annoyances pushed to the margin; they are boundary points of a classification. A vanishing determinant, a point at infinity, a null direction, a tangent contact, or an ideal boundary can all explain why a theorem needs the hypotheses it has. The code keeps those cases close enough to see, without pretending that a numerical experiment is a proof.
""",
        f"""## Worked example philosophy

The worked examples favor small complete constructions over large opaque demonstrations. Every object is named, every coordinate convention is stated, and every saved artifact has a filename that names the mathematical idea it illustrates. A reader should be able to rerun a cell, change one number, and predict which part of the visual will move.

The examples also separate representation from interpretation. A conic matrix is not itself a conic until we decide which projective chart we are viewing. A sphere drawn on a flat page is not intrinsically flat. A hyperbolic disk uses Euclidean pixels to represent non-Euclidean distance. These separations are the main source of both power and confusion, so they are made explicit before the applied lab.
""",
        f"""## How to read the artifacts

The artifacts in this notebook should be read as a small laboratory record. The PNG files are durable views of the construction, but the nearby code is part of the lesson: it states the coordinate convention, the parameter values, and the invariant being tested. The JSON and CSV files are intentionally plain so that a reader can open them outside the notebook and see the same evidence without rerunning every cell.

When a visual compares several objects, read it from the invariant outward. In this chapter the invariant is usually one of these: {chapter.invariants}. Ask first what should stay fixed, then inspect which part of the figure changes. If the figure shows a family, the interesting information is often in the limiting member: a degenerate conic, a tangent contact, a boundary point, a null direction, or an approximation that is nearly smooth but still finite.

The saved checks do not replace proof. They play a different role. They protect the notebook from misleading pictures, record the numerical scale of residuals, and give the reader a concrete experiment to modify. A good modification changes the parameters while preserving the hypotheses; a better one also breaks a hypothesis and watches the check fail for a geometric reason.
""",
        f"""## Applied lab

{chapter.lab}

For a stronger lab, change the parameters in two opposite directions: one that preserves the hypotheses and one that breaks them. The first change should keep the final checks small. The second should make a residual, signature, or visual feature fail in a meaningful way. That contrast is often where the real theorem becomes visible.
""",
        f"""## Takeaways

{takeaway_lines}
""",
    ]


def setup_cell(chapter: Chapter) -> str:
    return f"""
from pathlib import Path
import sys

BOOK_ROOT = Path.cwd()
for candidate in [BOOK_ROOT, *BOOK_ROOT.parents]:
    if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
        BOOK_ROOT = candidate
        break
else:
    raise RuntimeError("Could not find the Geometry II book root")

if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

CHAPTER = {chapter.number}
ARTIFACT_ROOT = BOOK_ROOT / "artifacts" / f"chapter-{{CHAPTER:02d}}"
FIGURE_ROOT = ARTIFACT_ROOT / "figures"
PLOT_ROOT = ARTIFACT_ROOT / "plots"
TABLE_ROOT = ARTIFACT_ROOT / "tables"
CHECK_ROOT = ARTIFACT_ROOT / "checks"
for root in [FIGURE_ROOT, PLOT_ROOT, TABLE_ROOT, CHECK_ROOT]:
    root.mkdir(parents=True, exist_ok=True)

print(f"Geometry II root: {{BOOK_ROOT}}")
"""


IMPORTS = """
import math
import numpy as np
import matplotlib.pyplot as plt

from utils.artifacts import assert_artifacts, display_artifact, save_csv, save_json
from utils.geometry import (
    circle_orthogonality,
    conic_matrix,
    conic_residual,
    convex_hull_2d,
    cross_ratio,
    disk_rotation,
    euler_characteristic,
    ellipse_points,
    hyperbola_points,
    polar_line,
    poincare_distance,
    polygon_area,
    quadratic_signature,
    regular_polygon,
    sphere_grid,
    spherical_distance,
    stereographic_project,
)
from utils.plotting import COLORS, finish_axes, new_3d_axes, new_axes, plot_line, plot_points, plot_polyline, plot_unit_circle, save_figure, set_equal_3d

generated_artifacts = []
"""


def chapter_code(number: int) -> list[str]:
    return {
        12: [
            """
rng = np.random.default_rng(12)
cloud = rng.normal(size=(28, 2))
cloud[:, 0] *= 1.2
cloud[:, 1] *= 0.75
hull = convex_hull_2d(cloud)

fig, ax = new_axes(title="Convex hull as a finite certificate")
plot_points(ax, cloud, color=COLORS["blue"], size=32)
plot_polyline(ax, hull, closed=True, color=COLORS["orange"], linewidth=2.5, label="convex hull")
ax.legend(loc="upper right")
ax.set_xlabel("x")
ax.set_ylabel("y")
finish_axes(ax)
hull_path = FIGURE_ROOT / "convex-hull-finite-certificate.png"
save_figure(fig, hull_path)
generated_artifacts.append(hull_path)
display_artifact(hull_path)
""",
            """
rows = []
fig, ax = new_axes(title="Regular polygons approximate the disk")
t = np.linspace(0, 2 * np.pi, 500)
ax.plot(np.cos(t), np.sin(t), color=COLORS["ink"], linewidth=2.0, label="unit circle")
for n, color in [(6, COLORS["red"]), (12, COLORS["orange"]), (24, COLORS["teal"]), (48, COLORS["purple"])]:
    poly = regular_polygon(n, phase=np.pi / n)
    area = abs(polygon_area(poly))
    rows.append({"n": n, "area": area, "area_error": math.pi - area, "relative_error": (math.pi - area) / math.pi})
    plot_polyline(ax, poly, closed=True, color=color, linewidth=1.5, label=f"{n}-gon")
ax.legend(loc="lower right", fontsize=8)
finish_axes(ax, margin=0.15)
approx_path = FIGURE_ROOT / "regular-polygons-approach-disk.png"
save_figure(fig, approx_path)
table_path = TABLE_ROOT / "regular-polygon-area-convergence.csv"
save_csv(rows, table_path)
generated_artifacts.extend([approx_path, table_path])
display_artifact(approx_path)
""",
            """
euler_checks = {
    "cube": {"V": 8, "E": 12, "F": 6, "chi": euler_characteristic(8, 12, 6)},
    "octahedron": {"V": 6, "E": 12, "F": 8, "chi": euler_characteristic(6, 12, 8)},
    "tetrahedron": {"V": 4, "E": 6, "F": 4, "chi": euler_characteristic(4, 6, 4)},
    "area_convergence_last_error": rows[-1]["area_error"],
}
check_path = CHECK_ROOT / "polytope-area-euler-checks.json"
save_json(euler_checks, check_path)
generated_artifacts.append(check_path)
display_artifact(check_path)
""",
        ],
        13: [
            """
x = np.linspace(-2.2, 2.2, 300)
y = np.linspace(-2.2, 2.2, 300)
xx, yy = np.meshgrid(x, y)
forms = [
    ("positive definite", xx**2 + yy**2, COLORS["blue"]),
    ("indefinite", xx**2 - yy**2, COLORS["orange"]),
    ("degenerate", xx**2, COLORS["purple"]),
]
fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), constrained_layout=True)
for ax, (title, values, color) in zip(axes, forms):
    ax.contour(xx, yy, values, levels=[-2, -1, -0.25, 0, 0.25, 1, 2], colors=color, linewidths=1.1)
    ax.axhline(0, color="#d1d5db", linewidth=0.8)
    ax.axvline(0, color="#d1d5db", linewidth=0.8)
    ax.set_aspect("equal")
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
contour_path = FIGURE_ROOT / "quadratic-form-signature-contours.png"
save_figure(fig, contour_path)
generated_artifacts.append(contour_path)
display_artifact(contour_path)
""",
            """
u = np.linspace(0, 2 * np.pi, 72)
r = np.linspace(0.0, 1.6, 32)
uu, rr = np.meshgrid(u, r)
xx = rr * np.cos(uu)
yy = rr * np.sin(uu)
zz = rr
fig, ax = new_3d_axes(title="Isotropic cone for x^2 + y^2 - z^2 = 0")
ax.plot_surface(xx, yy, zz, color=COLORS["teal"], alpha=0.65, linewidth=0)
ax.plot_surface(xx, yy, -zz, color=COLORS["teal"], alpha=0.35, linewidth=0)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
set_equal_3d(ax, np.column_stack([xx.ravel(), yy.ravel(), zz.ravel()]))
cone_path = FIGURE_ROOT / "isotropic-cone-signature-2-1.png"
save_figure(fig, cone_path)
generated_artifacts.append(cone_path)
display_artifact(cone_path)
""",
            """
matrices = {
    "positive_definite": np.diag([3.0, 1.0]),
    "indefinite": np.diag([2.0, -1.0]),
    "degenerate": np.diag([1.0, 0.0]),
    "lorentz_3d": np.diag([1.0, 1.0, -1.0]),
}
signature_checks = {name: quadratic_signature(matrix) for name, matrix in matrices.items()}
v = np.array([1.0, 2.0])
q = matrices["indefinite"]
reflection = np.diag([1.0, -1.0])
signature_checks["reflection_preserves_q_v"] = float(v @ q @ v - (reflection @ v) @ q @ (reflection @ v))
check_path = CHECK_ROOT / "quadratic-form-signatures.json"
save_json(signature_checks, check_path)
generated_artifacts.append(check_path)
display_artifact(check_path)
""",
        ],
        14: [
            """
q = conic_matrix("unit_circle")
points_h = [np.array([1.45, 0.45, 1.0]), np.array([0.55, 1.55, 1.0]), np.array([-1.35, 0.75, 1.0])]
fig, ax = new_axes(title="Polarity of exterior points with respect to a conic")
plot_unit_circle(ax, color=COLORS["ink"], label="x^2 + y^2 = 1")
for index, point_h in enumerate(points_h, start=1):
    point = point_h[:2] / point_h[2]
    line = polar_line(q, point_h)
    plot_points(ax, point.reshape(1, 2), labels=[f"P{index}"], color=COLORS["orange"])
    plot_line(ax, line, xlim=(-2.0, 2.0), color=[COLORS["blue"], COLORS["teal"], COLORS["purple"]][index - 1], label=f"polar(P{index})")
ax.legend(loc="upper right", fontsize=8)
finish_axes(ax, margin=0.2)
polar_path = FIGURE_ROOT / "projective-conic-polar-lines.png"
save_figure(fig, polar_path)
generated_artifacts.append(polar_path)
display_artifact(polar_path)
""",
            """
x = np.linspace(-2.0, 2.0, 320)
y = np.linspace(-2.0, 2.0, 320)
xx, yy = np.meshgrid(x, y)
fig, axes = plt.subplots(1, 4, figsize=(12.5, 3.2), constrained_layout=True)
for ax, lam in zip(axes, [-1.0, -0.25, 0.25, 1.0]):
    values = (1 + lam) * xx**2 + (1 - lam) * yy**2 - 1
    ax.contour(xx, yy, values, levels=[0], colors=COLORS["red"], linewidths=2)
    ax.axhline(0, color="#e5e7eb", linewidth=0.8)
    ax.axvline(0, color="#e5e7eb", linewidth=0.8)
    ax.set_aspect("equal")
    ax.set_title(f"lambda={lam:g}")
pencil_path = FIGURE_ROOT / "projective-quadric-pencil-chart.png"
save_figure(fig, pencil_path)
generated_artifacts.append(pencil_path)
display_artifact(pencil_path)
""",
            """
p = np.array([1.4, 0.2, 1.0])
r = np.array([-0.3, 1.7, 1.0])
left = float(p @ q @ r)
right = float(r @ q @ p)
checks = {
    "polarity_symmetry_residual": left - right,
    "sample_conic_residual_max": float(np.max(np.abs(conic_residual(q, regular_polygon(16))))),
    "pencil_parameter_count": 4,
}
check_path = CHECK_ROOT / "projective-quadric-polarity-checks.json"
save_json(checks, check_path)
generated_artifacts.append(check_path)
display_artifact(check_path)
""",
        ],
        15: [
            """
u = np.linspace(0, 2 * np.pi, 60)
v = np.linspace(-1.2, 1.2, 40)
uu, vv = np.meshgrid(u, v)
fig = plt.figure(figsize=(13, 4.2), constrained_layout=True)
axes = [fig.add_subplot(1, 3, i, projection="3d") for i in range(1, 4)]

x = 1.4 * np.cos(uu) * np.cos(vv)
y = 0.9 * np.sin(uu) * np.cos(vv)
z = 0.75 * np.sin(vv)
axes[0].plot_surface(x, y, z, color=COLORS["blue"], alpha=0.75, linewidth=0)
axes[0].set_title("ellipsoid")

x = np.cosh(vv) * np.cos(uu)
y = np.cosh(vv) * np.sin(uu)
z = np.sinh(vv)
axes[1].plot_surface(x, y, z, color=COLORS["orange"], alpha=0.68, linewidth=0)
axes[1].set_title("one-sheet hyperboloid")

r = np.linspace(0, 1.6, 50)
uu2, rr = np.meshgrid(u, r)
x = rr * np.cos(uu2)
y = rr * np.sin(uu2)
z = 0.65 * rr**2
axes[2].plot_surface(x, y, z, color=COLORS["teal"], alpha=0.74, linewidth=0)
axes[2].set_title("elliptic paraboloid")
for ax in axes:
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    set_equal_3d(ax)
gallery_path = FIGURE_ROOT / "affine-quadric-surface-gallery.png"
save_figure(fig, gallery_path)
generated_artifacts.append(gallery_path)
display_artifact(gallery_path)
""",
            """
x = np.linspace(-2.2, 2.2, 260)
y = np.linspace(-2.2, 2.2, 260)
xx, yy = np.meshgrid(x, y)
examples = [
    ("centered ellipse", xx**2 / 2.25 + yy**2 - 1),
    ("centered hyperbola", xx**2 - yy**2 - 1),
    ("parabolic", yy - xx**2),
]
fig, axes = plt.subplots(1, 3, figsize=(12, 3.4), constrained_layout=True)
for ax, (title, values) in zip(axes, examples):
    ax.contour(xx, yy, values, levels=[0], colors=COLORS["purple"], linewidths=2.2)
    ax.set_aspect("equal")
    ax.set_title(title)
    ax.axhline(0, color="#e5e7eb", linewidth=0.8)
    ax.axvline(0, color="#e5e7eb", linewidth=0.8)
slice_path = FIGURE_ROOT / "affine-quadric-normal-form-slices.png"
save_figure(fig, slice_path)
generated_artifacts.append(slice_path)
display_artifact(slice_path)
""",
            """
checks = {
    "ellipsoid_signature": quadratic_signature(np.diag([1.0, 1.0, 1.0])),
    "one_sheet_hyperboloid_signature": quadratic_signature(np.diag([1.0, 1.0, -1.0])),
    "paraboloid_quadratic_part_signature": quadratic_signature(np.diag([1.0, 1.0, 0.0])),
    "parabolic_linear_term_present": True,
}
check_path = CHECK_ROOT / "affine-quadric-classification-checks.json"
save_json(checks, check_path)
generated_artifacts.append(check_path)
display_artifact(check_path)
""",
        ],
        16: [
            """
def line_from_points(a, b):
    return np.cross(np.array([a[0], a[1], 1.0]), np.array([b[0], b[1], 1.0]))

def intersect_lines(l1, l2):
    p = np.cross(l1, l2)
    return p[:2] / p[2]

angles = np.array([0.25, 1.1, 2.2, 3.35, 4.35, 5.35])
pts = np.column_stack([np.cos(angles), np.sin(angles)])
A, B, C, D, E, F = pts
L_ab, L_bc, L_cd = line_from_points(A, B), line_from_points(B, C), line_from_points(C, D)
L_de, L_ef, L_fa = line_from_points(D, E), line_from_points(E, F), line_from_points(F, A)
X = intersect_lines(L_ab, L_de)
Y = intersect_lines(L_bc, L_ef)
Z = intersect_lines(L_cd, L_fa)
pascal_line = line_from_points(X, Y)

fig, ax = new_axes(title="Pascal line from six points on a conic")
plot_unit_circle(ax, color=COLORS["ink"], label="conic")
plot_points(ax, pts, labels=list("ABCDEF"), color=COLORS["blue"])
for p, qpt in [(A, B), (B, C), (C, D), (D, E), (E, F), (F, A)]:
    ax.plot([p[0], qpt[0]], [p[1], qpt[1]], color=COLORS["gray"], linewidth=1.2)
plot_points(ax, np.vstack([X, Y, Z]), labels=["X", "Y", "Z"], color=COLORS["red"], size=54)
plot_line(ax, pascal_line, xlim=(-4.0, 4.0), color=COLORS["orange"], label="Pascal line")
ax.legend(loc="upper right", fontsize=8)
finish_axes(ax, margin=0.7)
pascal_path = FIGURE_ROOT / "projective-conic-pascal-line.png"
save_figure(fig, pascal_path)
generated_artifacts.append(pascal_path)
display_artifact(pascal_path)
""",
            """
t_values = np.array([-1.2, -0.2, 0.7, 1.8])
def homography(t):
    return (2.0 * t + 1.0) / (0.35 * t + 1.0)
cr_before = cross_ratio(*t_values)
cr_after = cross_ratio(*homography(t_values))
fig, ax = new_axes(title="Cross-ratio survives a projective coordinate change")
ax.scatter(t_values, np.zeros_like(t_values), s=60, color=COLORS["blue"], label="original line")
ax.scatter(homography(t_values), np.ones_like(t_values), s=60, color=COLORS["orange"], label="after homography")
for i, (a, b) in enumerate(zip(t_values, homography(t_values)), start=1):
    ax.plot([a, b], [0, 1], color="#d1d5db", linewidth=1.0)
    ax.text(a, -0.08, f"t{i}", ha="center", fontsize=8)
    ax.text(b, 1.08, f"h(t{i})", ha="center", fontsize=8)
ax.set_yticks([0, 1], ["source", "image"])
ax.legend(loc="upper left", fontsize=8)
finish_axes(ax, margin=0.3)
cr_path = FIGURE_ROOT / "cross-ratio-homography-invariance.png"
save_figure(fig, cr_path)
generated_artifacts.append(cr_path)
display_artifact(cr_path)
""",
            """
checks = {
    "pascal_collinearity_residual": float(abs(np.dot(pascal_line, np.array([Z[0], Z[1], 1.0])))),
    "cross_ratio_before": float(cr_before),
    "cross_ratio_after": float(cr_after),
    "cross_ratio_residual": float(cr_before - cr_after),
    "conic_residual_max": float(np.max(np.abs(conic_residual(conic_matrix("unit_circle"), pts)))),
}
check_path = CHECK_ROOT / "projective-conic-pascal-crossratio-checks.json"
save_json(checks, check_path)
generated_artifacts.append(check_path)
display_artifact(check_path)
""",
        ],
        17: [
            """
ellipse = ellipse_points(2.0, 1.2, 420)
c = math.sqrt(2.0**2 - 1.2**2)
foci = np.array([[-c, 0.0], [c, 0.0]])
samples = ellipse[::60]
fig, ax = new_axes(title="Ellipse as a constant focal-sum curve")
ax.plot(ellipse[:, 0], ellipse[:, 1], color=COLORS["blue"], linewidth=2.2, label="ellipse")
plot_points(ax, foci, labels=["F1", "F2"], color=COLORS["red"], size=64)
for point in samples:
    ax.plot([foci[0, 0], point[0]], [0, point[1]], color=COLORS["orange"], linewidth=1.0, alpha=0.65)
    ax.plot([foci[1, 0], point[0]], [0, point[1]], color=COLORS["teal"], linewidth=1.0, alpha=0.65)
ax.legend(loc="upper right", fontsize=8)
finish_axes(ax, margin=0.25)
ellipse_path = FIGURE_ROOT / "ellipse-focal-sum-invariant.png"
save_figure(fig, ellipse_path)
generated_artifacts.append(ellipse_path)
display_artifact(ellipse_path)
""",
            """
left, right = hyperbola_points(1.0, 0.75, span=1.8)
c_h = math.sqrt(1.0**2 + 0.75**2)
hfoci = np.array([[-c_h, 0.0], [c_h, 0.0]])
fig, ax = new_axes(title="Hyperbola as a constant focal-difference curve")
ax.plot(left[:, 0], left[:, 1], color=COLORS["purple"], linewidth=2.1, label="left branch")
ax.plot(right[:, 0], right[:, 1], color=COLORS["purple"], linewidth=2.1, label="right branch")
plot_points(ax, hfoci, labels=["F1", "F2"], color=COLORS["red"], size=64)
for point in right[::55]:
    ax.plot([hfoci[0, 0], point[0]], [0, point[1]], color=COLORS["orange"], linewidth=0.9, alpha=0.6)
    ax.plot([hfoci[1, 0], point[0]], [0, point[1]], color=COLORS["teal"], linewidth=0.9, alpha=0.6)
ax.legend(loc="upper right", fontsize=8)
finish_axes(ax, margin=0.25)
hyperbola_path = FIGURE_ROOT / "hyperbola-focal-difference-invariant.png"
save_figure(fig, hyperbola_path)
generated_artifacts.append(hyperbola_path)
display_artifact(hyperbola_path)
""",
            """
ellipse_sums = [float(np.linalg.norm(p - foci[0]) + np.linalg.norm(p - foci[1])) for p in samples]
hyperbola_diffs = [float(abs(np.linalg.norm(p - hfoci[0]) - np.linalg.norm(p - hfoci[1]))) for p in right[::40]]
checks = {
    "ellipse_expected_sum": 4.0,
    "ellipse_sum_max_error": float(max(abs(value - 4.0) for value in ellipse_sums)),
    "hyperbola_expected_difference": 2.0,
    "hyperbola_difference_max_error": float(max(abs(value - 2.0) for value in hyperbola_diffs)),
    "ellipse_eccentricity": c / 2.0,
}
check_path = CHECK_ROOT / "euclidean-conic-focal-checks.json"
save_json(checks, check_path)
generated_artifacts.append(check_path)
display_artifact(check_path)
""",
        ],
        18: [
            """
x, y, z = sphere_grid(72, 36)
equator = np.column_stack([np.cos(np.linspace(0, 2 * np.pi, 240)), np.sin(np.linspace(0, 2 * np.pi, 240)), np.zeros(240)])
meridian = np.column_stack([np.cos(np.linspace(0, 2 * np.pi, 240)), np.zeros(240), np.sin(np.linspace(0, 2 * np.pi, 240))])
latitude = np.column_stack([0.75 * np.cos(np.linspace(0, 2 * np.pi, 240)), 0.75 * np.sin(np.linspace(0, 2 * np.pi, 240)), np.full(240, math.sqrt(1 - 0.75**2))])

fig = plt.figure(figsize=(12, 5), constrained_layout=True)
ax3 = fig.add_subplot(1, 2, 1, projection="3d")
ax3.plot_surface(x, y, z, color="#dbeafe", alpha=0.55, linewidth=0)
ax3.plot(equator[:, 0], equator[:, 1], equator[:, 2], color=COLORS["blue"], linewidth=2, label="great circle")
ax3.plot(meridian[:, 0], meridian[:, 1], meridian[:, 2], color=COLORS["teal"], linewidth=2, label="great circle")
ax3.plot(latitude[:, 0], latitude[:, 1], latitude[:, 2], color=COLORS["orange"], linewidth=2, label="small circle")
ax3.set_title("sphere with great and small circles")
set_equal_3d(ax3)
ax3.legend(fontsize=8)

ax2 = fig.add_subplot(1, 2, 2)
for curve, color, label in [(equator, COLORS["blue"], "equator"), (meridian[meridian[:, 2] < 0.98], COLORS["teal"], "meridian"), (latitude, COLORS["orange"], "latitude")]:
    projected = stereographic_project(curve)
    ax2.plot(projected[:, 0], projected[:, 1], color=color, linewidth=2, label=label)
ax2.set_aspect("equal")
ax2.grid(True, color="#e5e7eb")
ax2.set_title("stereographic chart")
ax2.legend(fontsize=8)
sphere_path = FIGURE_ROOT / "sphere-stereographic-circles.png"
save_figure(fig, sphere_path)
generated_artifacts.append(sphere_path)
display_artifact(sphere_path)
""",
            """
triangle = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
])
fig, ax = new_3d_axes(title="Spherical triangle with right angular sides")
ax.plot_surface(x, y, z, color="#eef2ff", alpha=0.30, linewidth=0)
for i, j, color in [(0, 1, COLORS["blue"]), (1, 2, COLORS["orange"]), (2, 0, COLORS["teal"])]:
    a = triangle[i]
    b = triangle[j]
    ts = np.linspace(0, 1, 80)
    arc = np.array([(math.sin((1 - t) * math.pi / 2) * a + math.sin(t * math.pi / 2) * b) for t in ts])
    arc = arc / np.linalg.norm(arc, axis=1)[:, None]
    ax.plot(arc[:, 0], arc[:, 1], arc[:, 2], color=color, linewidth=3)
ax.scatter(triangle[:, 0], triangle[:, 1], triangle[:, 2], color=COLORS["red"], s=45)
set_equal_3d(ax)
triangle_path = FIGURE_ROOT / "spherical-triangle-angular-sides.png"
save_figure(fig, triangle_path)
generated_artifacts.append(triangle_path)
display_artifact(triangle_path)
""",
            """
side_lengths = {
    "AB": spherical_distance(triangle[0], triangle[1]),
    "BC": spherical_distance(triangle[1], triangle[2]),
    "CA": spherical_distance(triangle[2], triangle[0]),
}
checks = {
    "side_lengths": side_lengths,
    "all_sides_pi_over_2": all(abs(value - math.pi / 2) < 1e-12 for value in side_lengths.values()),
    "latitude_unit_residual_max": float(np.max(np.abs(np.linalg.norm(latitude, axis=1) - 1.0))),
}
check_path = CHECK_ROOT / "sphere-distance-chart-checks.json"
save_json(checks, check_path)
generated_artifacts.append(check_path)
display_artifact(check_path)
""",
        ],
        19: [
            """
def poincare_geodesic_arc(u, v, count=160):
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    mat = 2 * np.vstack([u, v])
    rhs = np.array([np.dot(u, u) + 1, np.dot(v, v) + 1])
    center = np.linalg.solve(mat, rhs)
    radius = math.sqrt(np.dot(center, center) - 1)
    a0 = math.atan2(u[1] - center[1], u[0] - center[0])
    a1 = math.atan2(v[1] - center[1], v[0] - center[0])
    if abs(a1 - a0) > math.pi:
        if a1 > a0:
            a0 += 2 * math.pi
        else:
            a1 += 2 * math.pi
    angles = np.linspace(a0, a1, count)
    return center + radius * np.column_stack([np.cos(angles), np.sin(angles)])

fig, ax = new_axes(title="Poincare disk geodesics meet the boundary orthogonally")
plot_unit_circle(ax, color=COLORS["ink"], label="ideal boundary")
pairs = [
    (np.array([-0.65, -0.2]), np.array([0.35, 0.55])),
    (np.array([-0.15, 0.7]), np.array([0.7, -0.25])),
    (np.array([-0.55, 0.0]), np.array([0.55, 0.0])),
]
for a, b in pairs:
    if abs(np.cross(a, b)) < 1e-10:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["blue"], linewidth=2.5)
    else:
        arc = poincare_geodesic_arc(a, b)
        ax.plot(arc[:, 0], arc[:, 1], color=COLORS["blue"], linewidth=2.5)
    plot_points(ax, np.vstack([a, b]), color=COLORS["orange"], size=38)
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.legend(loc="upper right", fontsize=8)
disk_path = FIGURE_ROOT / "poincare-disk-geodesics.png"
save_figure(fig, disk_path)
generated_artifacts.append(disk_path)
display_artifact(disk_path)
""",
            """
radii = np.linspace(0.0, 0.92, 80)
distances = [poincare_distance(np.array([0.0, 0.0]), np.array([r, 0.0])) for r in radii[1:]]
fig, ax = new_axes(title="Hyperbolic distance grows toward the ideal boundary")
ax.set_aspect("auto")
ax.plot(radii[1:], distances, color=COLORS["red"], linewidth=2.4)
ax.set_xlabel("Euclidean radius in disk")
ax.set_ylabel("Poincare distance from origin")
ax.grid(True, color="#e5e7eb")
distance_path = FIGURE_ROOT / "poincare-distance-boundary-growth.png"
save_figure(fig, distance_path)
generated_artifacts.append(distance_path)
display_artifact(distance_path)
""",
            """
u = np.array([0.18, 0.31])
v = np.array([0.62, -0.12])
rot = disk_rotation(0.73)
d0 = poincare_distance(u, v)
d1 = poincare_distance(rot @ u, rot @ v)
checks = {
    "distance_before_rotation": d0,
    "distance_after_rotation": d1,
    "rotation_invariance_residual": d0 - d1,
    "distance_near_boundary_sample": distances[-1],
}
check_path = CHECK_ROOT / "hyperbolic-distance-model-checks.json"
save_json(checks, check_path)
generated_artifacts.append(check_path)
display_artifact(check_path)
""",
        ],
        20: [
            """
def draw_circle(ax, center, radius, color, label=None, linewidth=2.0):
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(center[0] + radius * np.cos(t), center[1] + radius * np.sin(t), color=color, linewidth=linewidth, label=label)

c1, r1 = (0.0, 0.0), 1.0
c2, r2 = (1.25, 0.0), 0.75
c3, r3 = (0.45, 0.95), 0.62
fig, ax = new_axes(title="Orthogonality is a quadratic relation on circles")
draw_circle(ax, c1, r1, COLORS["blue"], "circle A")
draw_circle(ax, c2, r2, COLORS["orange"], "circle B, orthogonal to A")
draw_circle(ax, c3, r3, COLORS["purple"], "comparison circle")
plot_points(ax, np.array([c1, c2, c3]), labels=["A", "B", "C"], color=COLORS["red"])
ax.legend(loc="upper right", fontsize=8)
finish_axes(ax, margin=0.25)
circle_path = FIGURE_ROOT / "sphere-space-circle-orthogonality.png"
save_figure(fig, circle_path)
generated_artifacts.append(circle_path)
display_artifact(circle_path)
""",
            """
centers = np.column_stack([np.linspace(-1.2, 1.2, 80), np.zeros(80)])
radii = np.sqrt((centers[:, 0] - 1.6) ** 2 + 0.35)
fig, ax = new_3d_axes(title="A coaxal pencil lifted to center-radius coordinates")
ax.plot(centers[:, 0], centers[:, 1], radii, color=COLORS["teal"], linewidth=2.5)
ax.scatter([c1[0], c2[0], c3[0]], [c1[1], c2[1], c3[1]], [r1, r2, r3], color=COLORS["red"], s=45)
ax.set_xlabel("center x")
ax.set_ylabel("center y")
ax.set_zlabel("radius")
set_equal_3d(ax)
pencil_path = FIGURE_ROOT / "sphere-pencil-center-radius-lift.png"
save_figure(fig, pencil_path)
generated_artifacts.append(pencil_path)
display_artifact(pencil_path)
""",
            """
checks = {
    "A_B_orthogonality_residual": circle_orthogonality(c1, r1, c2, r2),
    "A_C_orthogonality_residual": circle_orthogonality(c1, r1, c3, r3),
    "pencil_sample_count": int(len(radii)),
    "min_pencil_radius": float(np.min(radii)),
}
check_path = CHECK_ROOT / "sphere-space-orthogonality-checks.json"
save_json(checks, check_path)
generated_artifacts.append(check_path)
display_artifact(check_path)
""",
        ],
    }[number]


def final_sanity_cell() -> str:
    return """
assert generated_artifacts, "the notebook should generate artifacts"
assert_artifacts(generated_artifacts, min_bytes=32)
final_sanity = {
    "artifact_count": len(generated_artifacts),
    "all_artifacts_exist": all(path.exists() for path in generated_artifacts),
    "artifact_root": ARTIFACT_ROOT.relative_to(BOOK_ROOT).as_posix(),
}
final_sanity
"""


def write_notebook(chapter: Chapter, *, force: bool = False) -> Path:
    path = chapter.folder / chapter.notebook
    if path.exists() and not force:
        return path
    chapter.folder.mkdir(parents=True, exist_ok=True)
    cells = []
    cells.append(new_markdown_cell(markdown_for(chapter)[0]))
    cells.append(new_markdown_cell(markdown_for(chapter)[1]))
    cells.append(new_markdown_cell(markdown_for(chapter)[2]))
    cells.append(new_code_cell(textwrap.dedent(setup_cell(chapter)).strip() + "\n"))
    cells.append(new_code_cell(textwrap.dedent(IMPORTS).strip() + "\n"))
    cells.append(new_markdown_cell(markdown_for(chapter)[3]))
    for code in chapter_code(chapter.number):
        cells.append(new_code_cell(textwrap.dedent(code).strip() + "\n"))
    for text in markdown_for(chapter)[4:]:
        cells.append(new_markdown_cell(text))
    cells.append(new_code_cell(textwrap.dedent(final_sanity_cell()).strip() + "\n"))
    nb = new_notebook(cells=cells, metadata={"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}})
    nbformat.write(nb, path)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapters", nargs="*", type=int, default=[chapter.number for chapter in CHAPTERS])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    selected = [chapter for chapter in CHAPTERS if chapter.number in set(args.chapters)]
    if not selected:
        raise SystemExit("No matching chapters selected")
    for chapter in selected:
        path = write_notebook(chapter, force=args.force)
        print(path.relative_to(BOOK_ROOT))


if __name__ == "__main__":
    main()
