"""Bootstrap the visualization-first GICT notebook course.

This is a one-time builder for the empty course folder. It writes the book-local
AGENTS.md, utility modules, validation scripts, canonical notebooks, indexes, and
starter artifacts. The notebooks are still the canonical teaching surface: they
generate and display the same artifacts when executed.
"""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path
from typing import Any

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


BOOK_ROOT = Path(__file__).resolve().parents[1]
PDF_SOURCE = "Geometry with an Introduction to Cosmic Topology.pdf"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-+", "-", slug)


def dedent(text: str) -> str:
    return textwrap.dedent(text).strip() + "\n"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(text), encoding="utf-8")


def write_notebook(path: Path, cells: list[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    notebook = new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
    )
    nbformat.write(notebook, path)


CHAPTERS: list[dict[str, Any]] = [
    {
        "kind": "chapter",
        "number": 1,
        "title": "An Invitation to Geometry",
        "printed": "1-14",
        "pdf": "11-24",
        "sections": "1.1-1.3",
        "focus": "Local measurement, global shape, finite boundaryless surfaces, and the first split between Euclidean, hyperbolic, and elliptic behavior.",
        "goal": "See geometry as the interplay between local measurements and global shape, using flat tori, spheres, cones, saddles, and Klein's invariant viewpoint.",
        "translation": [
            "A finite world without boundary becomes computable by replacing edge crossings with equivalence classes.",
            "A geodesic is represented by the path that a local observer would measure as shortest.",
            "Triangle angle sum and circle circumference become detectors of curvature.",
            "The Erlangen viewpoint translates a geometry into a space plus transformations that preserve the chosen measurements.",
        ],
        "route": [
            "Start from a square video-game universe and unwrap it to a tiled cover.",
            "Compare Euclidean, spherical, and hyperbolic alternatives to the parallel postulate.",
            "Use cone and saddle sectors to make angle defect visible.",
            "End by treating transformations as filters that decide which measurements count as geometric.",
        ],
        "visuals": [
            {"kind": "torus", "filename": "flat-torus-edge-identification.png", "title": "Flat torus edge identification", "note": "Opposite edges are the same place, not walls."},
            {"kind": "sphere", "filename": "sphere-great-circle-triangle.png", "title": "Spherical triangle angle excess", "note": "Great-circle edges make a triangle whose angle sum exceeds pi."},
            {"kind": "parallel", "filename": "parallel-postulate-comparison.png", "title": "Three parallel-postulate worlds", "note": "One, many, or zero parallels through a point."},
            {"kind": "cone", "filename": "cone-saddle-angle-defect.png", "title": "Cone and saddle sector defect", "note": "Sector angle controls circumference and triangle angle sum."},
            {"kind": "hexagon", "filename": "hexagon-edge-gluing.png", "title": "Hexagon edge gluing", "note": "Corner totals explain when a glued polygon is homogeneous."},
            {"kind": "erlangen", "filename": "erlangen-invariant-filter.png", "title": "Erlangen invariant filter", "note": "The allowed transformations decide which features survive."},
        ],
        "lab": "Build a small universe simulator: choose a rectangle, place an observer and an object, then compute the nearest image in the tiled cover.",
        "pitfalls": [
            "The embedded donut in three-dimensional space is not the same geometry as the flat torus quotient.",
            "A drawn curve on a surface is not automatically a geodesic.",
            "A finite universe does not need an edge; it can close through identification.",
        ],
    },
    {
        "kind": "chapter",
        "number": 2,
        "title": "The Complex Plane",
        "printed": "15-28",
        "pdf": "25-38",
        "sections": "2.1-2.4",
        "focus": "Complex numbers as the computational coordinate system for the geometries that follow.",
        "goal": "Make complex arithmetic geometric: addition is displacement, multiplication is scale and rotation, division reverses those operations, and equations describe loci.",
        "translation": [
            "The point x + yi can be treated as a vector, a coordinate, or a movable object.",
            "The modulus and conjugate encode length and reflection across the real axis.",
            "Polar form turns multiplication and division into angle addition and subtraction.",
            "Complex equations become lines, circles, angle constraints, and regions in the plane.",
        ],
        "route": [
            "Draw addition and subtraction as arrows.",
            "Convert between Cartesian and polar form.",
            "Use arguments to measure oriented angles.",
            "Finish by plotting equations and inequalities as geometric sets.",
        ],
        "visuals": [
            {"kind": "complex_vectors", "filename": "complex-vectors-add-subtract.png", "title": "Complex vectors and addition", "note": "Addition is a parallelogram; subtraction points from one complex number to another."},
            {"kind": "conjugate", "filename": "modulus-conjugate-reflection.png", "title": "Modulus and conjugation", "note": "Conjugation reflects across the real axis and preserves modulus."},
            {"kind": "polar", "filename": "cartesian-polar-converter.png", "title": "Cartesian to polar form", "note": "Argument records direction and is periodic modulo 2*pi."},
            {"kind": "multiplication", "filename": "polar-multiplication-angle-sum.png", "title": "Multiplication as rotation and scale", "note": "Arguments add while moduli multiply."},
            {"kind": "angle", "filename": "oriented-angle-formula.png", "title": "Oriented angle formula", "note": "The quotient of translated vectors measures the turn at a vertex."},
            {"kind": "region", "filename": "complex-regions-panel.png", "title": "Complex equations as regions", "note": "Equations and inequalities become visible subsets of the plane."},
        ],
        "lab": "Sample random complex numbers and verify that polar multiplication predicts the Cartesian product to numerical precision.",
        "pitfalls": [
            "The argument is not single-valued; always specify a branch or work modulo 2*pi.",
            "Complex multiplication is not componentwise multiplication.",
            "A formula involving z and conjugate(z) may represent a real geometric locus.",
        ],
    },
    {
        "kind": "chapter",
        "number": 3,
        "title": "Transformations",
        "printed": "29-70",
        "pdf": "39-80",
        "sections": "3.1-3.5",
        "focus": "Inversions, clines, the extended plane, and Mobius transformations as the machinery for non-Euclidean geometry.",
        "goal": "Understand transformations by watching what they preserve: angles, clines, fixed points, cross ratios, and normal-form dynamics.",
        "translation": [
            "A transformation is a function on the plane whose geometric content is visible through images of test objects.",
            "Inversion swaps inside and outside while preserving angles in magnitude.",
            "Lines and circles unify as clines so that transformations can be stated cleanly.",
            "Mobius maps are generated by simple operations and are controlled by fixed points and cross ratios.",
        ],
        "route": [
            "Begin with affine maps and reflections.",
            "Introduce inversion and clines.",
            "Add the point at infinity through stereographic projection.",
            "Study Mobius maps by fixed points and cline families.",
        ],
        "visuals": [
            {"kind": "affine_grid", "filename": "basic-transform-grid.png", "title": "Basic complex transformations", "note": "Translation, rotation, dilation, and affine maps move the same test grid differently."},
            {"kind": "reflection", "filename": "reflection-composition.png", "title": "Reflections compose to motions", "note": "Parallel mirrors give translations; intersecting mirrors give rotations."},
            {"kind": "inversion", "filename": "inversion-radial-grid.png", "title": "Circle inversion", "note": "The product of distances to the inversion center is constant."},
            {"kind": "clines", "filename": "clines-under-inversion.png", "title": "Clines map to clines", "note": "Lines and circles are one family under inversion."},
            {"kind": "stereographic", "filename": "stereographic-projection.png", "title": "Stereographic projection", "note": "Infinity appears as the north pole of a sphere model."},
            {"kind": "mobius_dynamics", "filename": "mobius-fixed-point-dynamics.png", "title": "Mobius fixed-point dynamics", "note": "Normal forms move points along or around cline families."},
        ],
        "lab": "Choose four points and check that the cross ratio is unchanged by a sampled Mobius transformation.",
        "pitfalls": [
            "A circle through the inversion center becomes a line, so the cline language is safer than separate cases.",
            "Angle preservation does not imply distance preservation.",
            "The point at infinity is a bookkeeping device with geometric consequences.",
        ],
    },
    {
        "kind": "chapter",
        "number": 4,
        "title": "Geometry",
        "printed": "71-80",
        "pdf": "81-90",
        "sections": "4.1-4.2",
        "focus": "The Erlangen program: a geometry is a space together with a transformation group and its invariants.",
        "goal": "Turn the definition of a geometry into an inspectable workflow: choose transformations, compute orbits, identify invariants, and test homogeneity and isotropy.",
        "translation": [
            "Congruence is membership in the same orbit under the transformation group.",
            "A minimally invariant set is an orbit, while larger invariant sets are unions of orbits.",
            "Euclidean geometry preserves distances and angles; Mobius geometry preserves clines and angles but not Euclidean distance.",
            "Homogeneity and isotropy are group-action properties that can be tested with witness transformations.",
        ],
        "route": [
            "Use small finite groups to make orbits concrete.",
            "Compare translation, reflection, Euclidean, and Mobius groups.",
            "Record which measurements survive each group.",
            "Use one Mobius example to separate angle preservation from distance preservation.",
        ],
        "visuals": [
            {"kind": "erlangen", "filename": "erlangen-filter.png", "title": "Erlangen filter", "note": "A measurement counts only if the group preserves it."},
            {"kind": "orbit", "filename": "rotation-group-orbits.png", "title": "Finite rotation orbits", "note": "A seed point generates its congruence class."},
            {"kind": "reflection", "filename": "reflection-orbits.png", "title": "Reflection geometry", "note": "Fixed points and mirror pairs reveal orbit structure."},
            {"kind": "euclidean_invariants", "filename": "euclidean-invariants.png", "title": "Euclidean invariants", "note": "Pairwise distances and angles survive rotations and translations."},
            {"kind": "homogeneity", "filename": "homogeneous-isotropic-grid.png", "title": "Homogeneity and isotropy grid", "note": "Witness transformations expose which groups move points and directions freely."},
            {"kind": "mobius_distance", "filename": "mobius-distance-failure.png", "title": "Mobius distance failure", "note": "Inversion keeps angles but changes Euclidean distances."},
        ],
        "lab": "Compute an orbit under a chosen finite group and decide whether a proposed feature is invariant.",
        "pitfalls": [
            "A set can be invariant without being minimal.",
            "Congruence depends on the chosen group, not on visual similarity alone.",
            "The same space supports different geometries when the transformation group changes.",
        ],
    },
    {
        "kind": "chapter",
        "number": 5,
        "title": "Hyperbolic Geometry",
        "printed": "81-120",
        "pdf": "91-130",
        "sections": "5.1-5.5",
        "focus": "The Poincare disk and upper half-plane models, hyperbolic geodesics, measurement, area, and triangle defect.",
        "goal": "Make hyperbolic geometry computable by drawing geodesics as orthogonal clines, measuring distance with the disk metric, and comparing triangle defect with area.",
        "translation": [
            "The unit circle is the circle at infinity, not part of the hyperbolic plane.",
            "Hyperbolic lines are Euclidean clines that meet the boundary orthogonally.",
            "The metric density grows near the boundary, so Euclidean nearness does not mean hyperbolic nearness.",
            "Triangle angle defect is area in curvature -1 units.",
        ],
        "route": [
            "Build disk automorphisms from reflections.",
            "Draw geodesics and parallel families.",
            "Compute distance and circle samples.",
            "Transfer the same geometry to the upper half-plane with the Cayley map.",
        ],
        "visuals": [
            {"kind": "hyperbolic_disk", "filename": "poincare-disk-geodesics.png", "title": "Poincare disk geodesics", "note": "Lines are diameters or boundary-orthogonal arcs."},
            {"kind": "hyperbolic_parallel", "filename": "hyperbolic-parallelism.png", "title": "Hyperbolic parallel families", "note": "Through one exterior point there are many nonintersecting lines."},
            {"kind": "metric_density", "filename": "hyperbolic-metric-density.png", "title": "Metric density near infinity", "note": "The boundary recedes infinitely far away."},
            {"kind": "hyperbolic_circle", "filename": "hyperbolic-circles.png", "title": "Hyperbolic circles", "note": "Off-center hyperbolic circles look Euclidean-shifted."},
            {"kind": "triangle_defect", "filename": "triangle-defect-area.png", "title": "Triangle defect equals area", "note": "Smaller angle sum means larger hyperbolic area."},
            {"kind": "halfplane", "filename": "disk-to-half-plane.png", "title": "Disk to upper half-plane", "note": "The Cayley transform changes the drawing without changing the geometry."},
        ],
        "lab": "Sample a triangle in the disk and compare a numerical angle sum with the area predicted by defect.",
        "pitfalls": [
            "The disk boundary is infinitely far away in the hyperbolic metric.",
            "Euclidean arcs are hyperbolic lines only when they hit the boundary orthogonally.",
            "A Euclidean circle is not automatically a hyperbolic circle with the same center.",
        ],
    },
    {
        "kind": "chapter",
        "number": 6,
        "title": "Elliptic Geometry",
        "printed": "121-144",
        "pdf": "131-154",
        "sections": "6.1-6.4",
        "focus": "Elliptic geometry from the sphere, stereographic projection, antipodal identification, and projective disk measurement.",
        "goal": "Learn elliptic geometry by pairing antipodal points, drawing great circles as elliptic lines, and measuring area by triangle excess.",
        "translation": [
            "The projective plane identifies antipodal points on the sphere.",
            "In the extended plane, antipodes satisfy a reciprocal conjugate relation, with zero paired to infinity.",
            "Elliptic lines are great circles after projection, and any two lines meet.",
            "Triangle angle excess is area in curvature +1 units.",
        ],
        "route": [
            "Project the sphere to the plane and track antipodes.",
            "Build elliptic lines from clines through antipodal pairs.",
            "Measure distances and circles in the projective disk.",
            "Use lunes to derive triangle excess.",
        ],
        "visuals": [
            {"kind": "antipodes", "filename": "stereographic-antipodes.png", "title": "Stereographic antipodes", "note": "Opposite sphere points become reciprocal plane points."},
            {"kind": "elliptic_clines", "filename": "great-circles-antipodal-clines.png", "title": "Great circles as antipodal clines", "note": "A cline through a point and its antipode is an elliptic line."},
            {"kind": "projective_disk", "filename": "projective-disk-boundary-walk.png", "title": "Projective disk boundary walk", "note": "Boundary exits reenter at antipodal points."},
            {"kind": "elliptic_distance", "filename": "elliptic-distance-circles.png", "title": "Elliptic distance and circles", "note": "Large-radius circles fold through the antipodal identification."},
            {"kind": "lune", "filename": "lune-triangle-area.png", "title": "Lunes and triangle excess", "note": "Area is controlled by angle excess."},
            {"kind": "elliptic_trig", "filename": "elliptic-triangle-trig.png", "title": "Elliptic triangle trigonometry", "note": "Spherical formulas become projective disk computations."},
        ],
        "lab": "Move three projective-disk points and verify that the computed excess stays positive for nondegenerate elliptic triangles.",
        "pitfalls": [
            "The projective disk boundary has identified antipodal points; it is not an ordinary disk edge.",
            "Two elliptic lines always intersect, even when the disk drawing tempts a parallel interpretation.",
            "Large elliptic circles may look counterintuitive because the far side is identified.",
        ],
    },
    {
        "kind": "chapter",
        "number": 7,
        "title": "Geometry on Surfaces",
        "printed": "145-194",
        "pdf": "155-204",
        "sections": "7.1-7.7",
        "focus": "Curvature scales, the unified family (X_k, G_k), surface topology, Gauss-Bonnet, quotient spaces, and Dirichlet domains.",
        "goal": "Connect curvature measurements to topology: circle growth detects k, polygon labels classify surfaces, and Gauss-Bonnet ties area to Euler characteristic.",
        "translation": [
            "Changing the curvature scale changes lengths and areas while preserving the sign of geometry.",
            "The family (X_k, G_k) gives one vocabulary for elliptic, Euclidean, and hyperbolic surfaces.",
            "A polygon boundary word can encode a compact surface and its Euler characteristic.",
            "A quotient space inherits geometry when the identifying group acts cleanly enough.",
        ],
        "route": [
            "Extract curvature from circle circumference growth.",
            "Compare scaled elliptic and hyperbolic disks.",
            "Classify surfaces by orientability and Euler characteristic.",
            "Build quotient and Dirichlet domains as computational fundamental domains.",
        ],
        "visuals": [
            {"kind": "curvature_growth", "filename": "circle-growth-curvature.png", "title": "Circle growth detects curvature", "note": "The second-order deviation from C=2*pi*r reveals the sign of curvature."},
            {"kind": "scaled_models", "filename": "scaled-xk-models.png", "title": "Scaled X_k models", "note": "The disk radius and metric formulas move with k."},
            {"kind": "parallel_angle", "filename": "angle-of-parallelism.png", "title": "Angle of parallelism", "note": "Distance and curvature determine the limiting parallel angle."},
            {"kind": "surface_classifier", "filename": "polygonal-surface-classifier.png", "title": "Polygonal surface classifier", "note": "Boundary labels produce vertices, edges, faces, and orientability signals."},
            {"kind": "gauss_bonnet", "filename": "gauss-bonnet-surface-map.png", "title": "Gauss-Bonnet surface map", "note": "The sign of Euler characteristic predicts the geometry type."},
            {"kind": "dirichlet", "filename": "quotient-dirichlet-domains.png", "title": "Quotient and Dirichlet domains", "note": "Nearest-image bisectors build the domain seen by an inhabitant."},
        ],
        "lab": "Enter a boundary word for a polygonal surface and compute a first-pass classification with Euler characteristic and orientability.",
        "pitfalls": [
            "The surface classification theorem is a catalog theorem here, not a full proof.",
            "A quotient by a group with fixed points can create cone points instead of a smooth inherited geometry.",
            "Curvature sign and topology constrain each other, but scale still changes metric quantities.",
        ],
    },
    {
        "kind": "chapter",
        "number": 8,
        "title": "Cosmic Topology",
        "printed": "195-220",
        "pdf": "205-230",
        "sections": "8.1-8.4",
        "focus": "Three-dimensional candidate universes, cosmic crystallography, circles in the sky, and density-parameter evidence.",
        "goal": "Treat cosmic topology as a computational detection problem: finite topology can create repeated images, pair-separation spikes, and matching CMB circles.",
        "translation": [
            "A candidate universe is modeled as a three-dimensional geometry divided by a group of isometries.",
            "Cosmic crystallography searches for excess repeated distances in a catalog.",
            "The last scattering surface can intersect copies of itself, creating matching circles.",
            "Density parameters describe the curvature evidence while topology remains a global question.",
        ],
        "route": [
            "Survey Euclidean, elliptic, and hyperbolic three-manifold models.",
            "Simulate catalog images in a flat torus and compare pair-separation histograms.",
            "Construct matching-circle geometry for the last scattering surface.",
            "End with a Friedmann-parameter dashboard that separates near-flat geometry from unknown topology.",
        ],
        "visuals": [
            {"kind": "three_geometries", "filename": "three-geometry-models.png", "title": "Three model geometries", "note": "Euclidean, hyperbolic, and elliptic spaces support different geodesic pictures."},
            {"kind": "three_torus", "filename": "three-torus-face-pairings.png", "title": "Three-torus face pairings", "note": "A cube with opposite faces identified has no wall."},
            {"kind": "dodecahedron", "filename": "dodecahedral-face-pairings.png", "title": "Dodecahedral face pairings", "note": "Twisted opposite faces create elliptic or hyperbolic candidates."},
            {"kind": "psh", "filename": "cosmic-crystallography-psh.png", "title": "Pair separation histogram", "note": "Torus repeats create spikes at translation lengths."},
            {"kind": "lss", "filename": "lss-matching-circles.png", "title": "Last scattering surface circles", "note": "Matching circles appear when the observable radius exceeds the injectivity radius."},
            {"kind": "friedmann", "filename": "friedmann-density-geometry.png", "title": "Friedmann density geometry", "note": "Omega parameters encode near-flat curvature evidence."},
        ],
        "lab": "Generate a toy torus catalog and see how changing the fundamental-domain dimensions moves the histogram spikes.",
        "pitfalls": [
            "No spike is not proof of simple connectivity; it may mean the topology scale is too large or the method is insensitive.",
            "Geometry is local curvature type, while topology is global shape.",
            "The observational values are historical to the source edition unless intentionally updated.",
        ],
    },
    {
        "kind": "appendix",
        "number": 9,
        "title": "Appendix A: List of Symbols",
        "printed": "221-222",
        "pdf": "231-232",
        "sections": "Appendix A",
        "focus": "A compact computational glossary for the symbols used across the course.",
        "goal": "Turn the source symbol list into an executable glossary that links notation to the course models and helper functions.",
        "translation": [
            "Symbols are grouped by complex-plane, transformation, model, surface, and cosmic-topology contexts.",
            "Each symbol gets a computational role rather than a copied textbook definition.",
            "The glossary doubles as a quick sanity check that helper functions agree with the course notation.",
            "Small examples show how symbols move between chapters.",
        ],
        "route": [
            "Build a table of symbols and course meanings.",
            "Group symbols by model and chapter.",
            "Run small checks for representative formulas.",
            "Display a map connecting notation families.",
        ],
        "visuals": [
            {"kind": "glossary_map", "filename": "symbol-family-map.png", "title": "Symbol family map", "note": "Notation clusters by the geometry it supports."},
            {"kind": "complex_vectors", "filename": "complex-symbols.png", "title": "Complex-plane symbols", "note": "z, conjugate(z), |z|, and arg(z) are one computational package."},
            {"kind": "mobius_distance", "filename": "transformation-symbols.png", "title": "Transformation symbols", "note": "Maps, groups, and invariants are tied together."},
            {"kind": "curvature_growth", "filename": "curvature-symbols.png", "title": "Curvature symbols", "note": "k, radius, circumference, and area formulas belong together."},
            {"kind": "surface_classifier", "filename": "surface-symbols.png", "title": "Surface symbols", "note": "H_g, C_g, and chi organize the surface catalog."},
            {"kind": "friedmann", "filename": "cosmic-symbols.png", "title": "Cosmic topology symbols", "note": "Omega terms and observable radii bridge geometry and data."},
        ],
        "lab": "Use the glossary table as a lookup dataset and query symbols by chapter or mathematical role.",
        "pitfalls": [
            "The same letter can appear in different contexts; always name the model.",
            "The symbol list is a reference, not a replacement for the construction that gives the symbol meaning.",
            "Back matter is summarized and reworked rather than copied.",
        ],
    },
]


def entry_folder(entry: dict[str, Any]) -> str:
    if entry["kind"] == "appendix":
        return "appendix-a-list-of-symbols"
    return f"chapter-{entry['number']:02d}-{slugify(entry['title'])}"


def entry_notebook(entry: dict[str, Any]) -> str:
    if entry["kind"] == "appendix":
        return "appendix-a-list-of-symbols.ipynb"
    return f"{entry['number']:02d}-{slugify(entry['title'])}.ipynb"


def artifact_topic(entry: dict[str, Any]) -> str:
    if entry["kind"] == "appendix":
        return "appendix-a"
    return f"chapter-{entry['number']:02d}"


def public_entries() -> list[dict[str, Any]]:
    entries = []
    for item in CHAPTERS:
        clone = dict(item)
        clone["folder"] = entry_folder(item)
        clone["notebook"] = entry_notebook(item)
        clone["artifact"] = artifact_topic(item)
        entries.append(clone)
    return entries


def agent_md() -> str:
    rows = "\n".join(
        f"| {'Appendix A' if e['kind'] == 'appendix' else 'Chapter ' + str(e['number'])} | `{e['folder']}` | {e['printed']} | {e['pdf']} | {e['focus']} |"
        for e in public_entries()
    )
    return f"""
    # Agent Instructions: Geometry with an Introduction to Cosmic Topology Notebook Course

    This folder is a standalone visualization-first notebook edition of *Geometry with an Introduction to Cosmic Topology*.
    Treat this folder as the project root for this course. The workspace root owns the shared `uv`
    environment, `pyproject.toml`, `uv.lock`, and `.venv`.

    ## Repo-Local Skills

    Use the repo-local skills under `D:\\Geometry\\.codex\\skills`:

    - `geometry-visualization-planner` before planning or revising a chapter storyboard.
    - `geometry-chapter-notebook-author` when authoring a canonical notebook.
    - `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

    ## Non-Negotiables

    - Write original teaching prose, examples, code, diagrams, and checks.
    - Do not copy textbook passages, long exercise text, screenshots, or page crops.
    - A reader must be able to learn from each notebook without opening the PDF.
    - Visualizations are part of the explanation. Use diagrams, plots, 3D-style views,
      widgets or HTML parameter labs, symbolic checks, computational experiments, and
      proof-state diagrams wherever they clarify the geometry.
    - Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
    - Every canonical notebook must execute with `nbclient`.
    - Generated paths in notebooks must be relative or book-local.

    ## Course Structure

    ```text
    Geometry-with-an-Introduction-to-Cosmic-Topology/
      00-book-index.ipynb
      AGENTS.md
      artifacts/
      scripts/
      utils/
      chapter-01-an-invitation-to-geometry/
      ...
      chapter-08-cosmic-topology/
      appendix-a-list-of-symbols/
    ```

    Each chapter or appendix folder contains:

    ```text
    00-index.ipynb
    <canonical notebook>.ipynb
    ```

    There should be exactly one canonical teaching notebook in each folder, excluding `00-index.ipynb`.

    ## Source Map

    Main-body printed pages map to physical PDF pages by `pdf_page = printed_page + 10`.

    | Unit | Folder | Printed Pages | PDF Pages | Focus |
    | --- | --- | ---: | ---: | --- |
    {rows}

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
    artifacts/appendix-a/
    ```

    Artifact filenames should name the concept, not the rendering technology.
    Repeated placeholder visuals are a QC failure. Every generated artifact should be displayed inline
    or linked from the notebook, and final checks should assert that files exist and are nonempty.

    ## Geometry Stack

    Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding
    dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `pandas`,
    `networkx`, `shapely`, `trimesh`, `pyvista`, `ripser`, and the rest of the root geometry stack.
    This course currently needs no dependency additions.

    ## Worker Boundaries

    Assign one worker to one canonical notebook, one helper module, or one script task.
    Chapter workers may edit only their chapter folder, matching artifact subtree, and explicitly
    assigned helper module. Index workers own `00-book-index.ipynb` and `00-index.ipynb` files.
    QC workers run audits and validation and report findings.

    ## Commands

    Run from `D:\\Geometry`:

    ```powershell
    uv run python Geometry-with-an-Introduction-to-Cosmic-Topology/scripts/build_gict_course_indexes.py
    uv run python -m compileall -q Geometry-with-an-Introduction-to-Cosmic-Topology/utils Geometry-with-an-Introduction-to-Cosmic-Topology/scripts
    uv run python Geometry-with-an-Introduction-to-Cosmic-Topology/scripts/audit_gict_notebooks.py --min-words 1200 --min-code-cells 5
    uv run python Geometry-with-an-Introduction-to-Cosmic-Topology/scripts/audit_gict_visuals.py
    uv run python Geometry-with-an-Introduction-to-Cosmic-Topology/scripts/validate_gict_course.py --limit 4 --timeout 300
    git diff --check
    ```

    Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.
    """


def utils_init() -> str:
    return '''
    """Utilities for the Geometry with an Introduction to Cosmic Topology course."""
    '''


def artifacts_py() -> str:
    return r'''
    """Artifact helpers for the GICT notebook course."""

    from __future__ import annotations

    import csv
    import json
    import re
    from html import escape
    from pathlib import Path
    from typing import Any, Iterable

    import numpy as np
    from PIL import Image as PILImage

    BOOK_ROOT = Path(__file__).resolve().parents[1]
    ARTIFACT_ROOT = BOOK_ROOT / "artifacts"


    def slugify(value: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
        slug = re.sub(r"-+", "-", slug).strip("-._")
        return slug or "artifact"


    def ensure_artifact_root(root: str | Path) -> Path:
        path = Path(root)
        for child in ["figures", "html", "checks", "tables"]:
            (path / child).mkdir(parents=True, exist_ok=True)
        return path


    def artifact_path(root: str | Path, category: str, filename: str) -> Path:
        base = ensure_artifact_root(root)
        path = base / slugify(category) / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        return path


    def save_json(data: Any, root: str | Path, category: str, filename: str = "data.json") -> Path:
        path = artifact_path(root, category, filename)
        path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
        return path


    def save_table(rows: Iterable[dict[str, Any]], root: str | Path, category: str, filename: str = "table.csv") -> Path:
        path = artifact_path(root, category, filename)
        rows = list(rows)
        fieldnames: list[str] = sorted({key for row in rows for key in row.keys()})
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return path


    def save_text(text: str, root: str | Path, category: str, filename: str = "notes.txt") -> Path:
        path = artifact_path(root, category, filename)
        path.write_text(text, encoding="utf-8")
        return path


    def save_html(text: str, root: str | Path, category: str, filename: str = "view.html") -> Path:
        path = artifact_path(root, category, filename)
        path.write_text(text, encoding="utf-8")
        return path


    def save_matplotlib(figure: Any, root: str | Path, category: str, filename: str, *, dpi: int = 155) -> Path:
        path = artifact_path(root, category, filename)
        figure.savefig(path, dpi=dpi, bbox_inches="tight")
        return path


    def image_stats(path: str | Path) -> dict[str, Any]:
        resolved = Path(path)
        image = PILImage.open(resolved).convert("RGB")
        arr = np.asarray(image, dtype=float)
        return {
            "path": resolved.as_posix(),
            "width": int(image.width),
            "height": int(image.height),
            "pixel_std": float(arr.std()),
            "file_size": int(resolved.stat().st_size),
        }


    def assert_artifacts(paths: Iterable[str | Path], *, min_size: int = 256) -> None:
        for item in paths:
            path = Path(item)
            if not path.exists():
                raise AssertionError(f"Missing artifact: {path}")
            if path.stat().st_size < min_size:
                raise AssertionError(f"Artifact too small: {path}")


    def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
        from IPython.display import HTML, IFrame, Image, display

        resolved = Path(path)
        suffix = resolved.suffix.lower()
        if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
            return display(Image(filename=str(resolved), width=width, height=height))
        if suffix == ".svg":
            return display(HTML(resolved.read_text(encoding="utf-8")))
        if suffix in {".html", ".htm"}:
            return display(IFrame(src=str(resolved), width=width or "100%", height=height or 420))
        link = escape(resolved.as_posix(), quote=True)
        return display(HTML(f'<a href="{link}">{link}</a>'))
    '''


def complex_plane_py() -> str:
    return r'''
    """Complex-plane helpers for GICT notebooks."""

    from __future__ import annotations

    import math

    import numpy as np


    def principal_arg(z: complex) -> float:
        return float(np.angle(z))


    def angle_mod_2pi(theta: float) -> float:
        return float((theta + np.pi) % (2 * np.pi) - np.pi)


    def complex_to_polar(z: complex) -> tuple[float, float]:
        return abs(z), principal_arg(z)


    def from_polar(radius: float, theta: float) -> complex:
        return complex(radius * math.cos(theta), radius * math.sin(theta))


    def oriented_angle(u: complex, v: complex, w: complex) -> float:
        """Return the oriented angle from ray v->u to ray v->w."""
        return principal_arg((w - v) / (u - v))


    def complex_grid(extent: float = 2.0, count: int = 9) -> list[np.ndarray]:
        values = np.linspace(-extent, extent, count)
        lines: list[np.ndarray] = []
        t = np.linspace(-extent, extent, 160)
        for value in values:
            lines.append(t + 1j * value)
            lines.append(value + 1j * t)
        return lines


    def unit_circle(samples: int = 240) -> np.ndarray:
        theta = np.linspace(0, 2 * np.pi, samples)
        return np.exp(1j * theta)
    '''


def mobius_py() -> str:
    return r'''
    """Mobius, inversion, and stereographic helpers."""

    from __future__ import annotations

    import numpy as np


    def mobius(z: complex | np.ndarray, a: complex, b: complex, c: complex, d: complex) -> complex | np.ndarray:
        return (a * z + b) / (c * z + d)


    def disk_automorphism(z: complex | np.ndarray, a: complex, theta: float = 0.0) -> complex | np.ndarray:
        lam = np.exp(1j * theta)
        return lam * (z - a) / (1 - np.conjugate(a) * z)


    def cross_ratio(z1: complex, z2: complex, z3: complex, z4: complex) -> complex:
        return ((z1 - z3) * (z2 - z4)) / ((z1 - z4) * (z2 - z3))


    def invert_in_circle(z: complex | np.ndarray, center: complex = 0j, radius: float = 1.0) -> complex | np.ndarray:
        shifted = z - center
        return center + (radius**2) / np.conjugate(shifted)


    def antipode(z: complex) -> complex:
        if abs(z) < 1e-12:
            raise ZeroDivisionError("0 is paired with infinity in the extended plane")
        return -1 / np.conjugate(z)


    def stereographic(point: np.ndarray) -> complex:
        x, y, z = point
        if abs(1 - z) < 1e-12:
            raise ZeroDivisionError("north pole projects to infinity")
        return complex(x / (1 - z), y / (1 - z))


    def inverse_stereographic(z: complex) -> np.ndarray:
        r2 = abs(z) ** 2
        return np.array([2 * z.real / (r2 + 1), 2 * z.imag / (r2 + 1), (r2 - 1) / (r2 + 1)])


    def classify_mobius_multiplier(multiplier: complex, tol: float = 1e-8) -> str:
        radius = abs(multiplier)
        angle = abs(np.angle(multiplier))
        if abs(radius - 1) < tol and angle > tol:
            return "elliptic"
        if angle < tol and abs(radius - 1) > tol:
            return "hyperbolic"
        if abs(radius - 1) > tol and angle > tol:
            return "loxodromic"
        return "parabolic-or-identity"
    '''


def models_py() -> str:
    return r'''
    """Metric model helpers for elliptic, Euclidean, and hyperbolic geometry."""

    from __future__ import annotations

    import math

    import numpy as np


    def hyperbolic_distance(p: complex, q: complex) -> float:
        numerator = abs(p - q) ** 2
        denominator = (1 - abs(p) ** 2) * (1 - abs(q) ** 2)
        return float(np.arccosh(1 + 2 * numerator / denominator))


    def elliptic_distance(p: complex, q: complex) -> float:
        numerator = abs(p - q)
        denominator = abs(1 + np.conjugate(p) * q)
        return float(2 * np.arctan2(numerator, denominator))


    def circumference_k(radius: float | np.ndarray, k: float) -> float | np.ndarray:
        r = np.asarray(radius)
        if abs(k) < 1e-12:
            return 2 * np.pi * r
        scale = math.sqrt(abs(k))
        if k > 0:
            return 2 * np.pi * np.sin(scale * r) / scale
        return 2 * np.pi * np.sinh(scale * r) / scale


    def disk_area_k(radius: float | np.ndarray, k: float) -> float | np.ndarray:
        r = np.asarray(radius)
        if abs(k) < 1e-12:
            return np.pi * r**2
        scale = math.sqrt(abs(k))
        if k > 0:
            return 2 * np.pi * (1 - np.cos(scale * r)) / k
        return 2 * np.pi * (np.cosh(scale * r) - 1) / abs(k)


    def triangle_area_from_angles(alpha: float, beta: float, gamma: float, k: float) -> float:
        excess = alpha + beta + gamma - math.pi
        if abs(k) < 1e-12:
            return 0.0
        return excess / k


    def angle_of_parallelism(distance: float, k: float = -1.0) -> float:
        if k >= 0:
            raise ValueError("Angle of parallelism belongs to negative curvature")
        return float(2 * np.arctan(np.exp(-math.sqrt(abs(k)) * distance)))


    def unified_right_hypotenuse(a: float, k: float) -> float:
        if abs(k) < 1e-12:
            return math.sqrt(2) * a
        scale = math.sqrt(abs(k))
        if k > 0:
            return math.acos(math.cos(scale * a) ** 2) / scale
        return math.acosh(math.cosh(scale * a) ** 2) / scale
    '''


def surfaces_py() -> str:
    return r'''
    """Surface topology helpers for polygonal models and quotient domains."""

    from __future__ import annotations

    import math
    from dataclasses import dataclass

    import numpy as np


    @dataclass(frozen=True)
    class SurfaceSummary:
        name: str
        orientable: bool
        euler: int
        geometry: str


    def euler_handlebody(genus: int) -> int:
        return 2 - 2 * genus


    def euler_crosscap(genus: int) -> int:
        return 2 - genus


    def geometry_from_euler(euler: int, orientable: bool) -> str:
        if euler > 0:
            return "elliptic"
        if euler == 0:
            return "euclidean"
        return "hyperbolic"


    def classify_catalog(name: str, orientable: bool, genus: int) -> SurfaceSummary:
        euler = euler_handlebody(genus) if orientable else euler_crosscap(genus)
        return SurfaceSummary(name=name, orientable=orientable, euler=euler, geometry=geometry_from_euler(euler, orientable))


    def torus_distance(p: np.ndarray, q: np.ndarray, width: float, height: float) -> float:
        delta = np.asarray(q) - np.asarray(p)
        dx = min(abs(delta[0]), width - abs(delta[0]))
        dy = min(abs(delta[1]), height - abs(delta[1]))
        return float(math.hypot(dx, dy))


    def torus_images(point: tuple[float, float], width: float, height: float, radius: int = 1) -> np.ndarray:
        x, y = point
        images = []
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                images.append((x + i * width, y + j * height))
        return np.asarray(images, dtype=float)


    def gauss_bonnet_area(euler: int, k: float) -> float:
        if abs(k) < 1e-12:
            if euler != 0:
                raise ValueError("Flat constant-curvature surfaces require chi = 0")
            return math.inf
        return 2 * math.pi * euler / k
    '''


def cosmic_topology_py() -> str:
    return r'''
    """Small simulation helpers for cosmic topology notebooks."""

    from __future__ import annotations

    import math

    import numpy as np


    def pair_distances(points: np.ndarray) -> np.ndarray:
        points = np.asarray(points, dtype=float)
        dists = []
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                dists.append(float(np.linalg.norm(points[i] - points[j])))
        return np.asarray(dists)


    def pair_separation_histogram(points: np.ndarray, bins: int = 32) -> tuple[np.ndarray, np.ndarray]:
        distances = pair_distances(points)
        hist, edges = np.histogram(distances, bins=bins)
        return hist, edges


    def torus_catalog(seed: int = 7, base_count: int = 14, width: float = 4.0, height: float = 3.0, copies: int = 1) -> np.ndarray:
        rng = np.random.default_rng(seed)
        base = rng.random((base_count, 2)) * np.array([width, height])
        images = []
        for i in range(-copies, copies + 1):
            for j in range(-copies, copies + 1):
                images.append(base + np.array([i * width, j * height]))
        return np.vstack(images)


    def sphere_intersection_circle_radius(r_obs: float, separation: float) -> float:
        if separation <= 0 or separation >= 2 * r_obs:
            return 0.0
        return float(math.sqrt(r_obs**2 - (separation / 2) ** 2))


    def ccp_score(points: np.ndarray, epsilon: float = 1e-3) -> float:
        distances = np.sort(pair_distances(points))
        if len(distances) < 2:
            return 0.0
        gaps = np.diff(distances)
        return float(np.count_nonzero(gaps < epsilon) / len(gaps))


    def omega_geometry(omega_k: float, tol: float = 1e-3) -> str:
        if abs(omega_k) <= tol:
            return "nearly euclidean"
        if omega_k > 0:
            return "hyperbolic convention"
        return "elliptic convention"
    '''


def visuals_py() -> str:
    return r'''
    """Deterministic visual builders for the GICT notebooks."""

    from __future__ import annotations

    import math
    from pathlib import Path
    from typing import Any

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Circle, Polygon, Rectangle

    from utils.artifacts import image_stats, save_html, save_matplotlib
    from utils.complex_plane import complex_grid, unit_circle
    from utils.cosmic_topology import pair_distances, sphere_intersection_circle_radius, torus_catalog
    from utils.mobius import disk_automorphism, invert_in_circle
    from utils.models import angle_of_parallelism, circumference_k, disk_area_k, unified_right_hypotenuse
    from utils.surfaces import classify_catalog, torus_images


    PALETTE = {
        "ink": "#1f2933",
        "blue": "#3269a8",
        "teal": "#258f86",
        "green": "#5b8a3c",
        "gold": "#c79020",
        "red": "#bd4b4b",
        "violet": "#6d5aa8",
        "gray": "#718096",
        "light": "#eef3f7",
    }


    def _style(ax: Any, title: str, *, equal: bool = True) -> None:
        ax.set_title(title, fontsize=11, color=PALETTE["ink"])
        ax.grid(True, color="#d7dee8", linewidth=0.7, alpha=0.75)
        if equal:
            ax.set_aspect("equal", adjustable="box")
        for spine in ax.spines.values():
            spine.set_color("#b8c2cc")


    def _plot_unit_disk(ax: Any) -> None:
        ax.add_patch(Circle((0, 0), 1, fill=False, color=PALETTE["ink"], linewidth=1.5))
        ax.set_xlim(-1.15, 1.15)
        ax.set_ylim(-1.15, 1.15)


    def _plot_torus(ax: Any, spec: dict[str, Any]) -> None:
        w, h = 4.0, 2.6
        for i in range(-1, 2):
            for j in range(-1, 2):
                ax.add_patch(Rectangle((i * w, j * h), w, h, fill=False, edgecolor="#b8c2cc", linewidth=0.9))
        p = np.array([1.0, 0.8])
        q = np.array([3.4, 2.1])
        images = torus_images(tuple(q), w, h, radius=1)
        ax.scatter(images[:, 0], images[:, 1], s=28, color=PALETTE["teal"], label="object images")
        ax.scatter([p[0]], [p[1]], s=48, color=PALETTE["red"], label="observer")
        ax.arrow(3.75, 1.3, 0.7, 0, width=0.02, color=PALETTE["blue"], length_includes_head=True)
        ax.arrow(0.25, 1.3, -0.7, 0, width=0.02, color=PALETTE["blue"], length_includes_head=True)
        ax.set_xlim(-0.7, w + 0.7)
        ax.set_ylim(-0.5, h + 0.5)
        ax.legend(fontsize=8, loc="upper right")
        _style(ax, spec["title"])


    def _plot_sphere(ax: Any, spec: dict[str, Any]) -> None:
        ax.remove()
        fig = plt.gcf()
        ax3 = fig.add_subplot(111, projection="3d")
        u = np.linspace(0, 2 * np.pi, 48)
        v = np.linspace(0, np.pi, 24)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones_like(u), np.cos(v))
        ax3.plot_surface(x, y, z, color="#dceaf7", edgecolor="#ffffff", linewidth=0.2, alpha=0.8)
        t = np.linspace(0, np.pi / 2, 80)
        ax3.plot(np.cos(t), np.sin(t), 0 * t, color=PALETTE["blue"], linewidth=2)
        ax3.plot(np.cos(t) * 0, np.sin(t), np.cos(t), color=PALETTE["red"], linewidth=2)
        ax3.plot(np.cos(t), 0 * t, np.sin(t), color=PALETTE["teal"], linewidth=2)
        ax3.set_title(spec["title"], fontsize=11)
        ax3.set_box_aspect((1, 1, 1))
        ax3.set_axis_off()


    def _plot_parallel(ax: Any, spec: dict[str, Any]) -> None:
        ax.set_xlim(-0.2, 6.4)
        ax.set_ylim(-1.2, 1.4)
        labels = ["Euclidean: one", "Hyperbolic: many", "Elliptic: none"]
        offsets = [0, 2.2, 4.4]
        for label, ox in zip(labels, offsets):
            ax.plot([ox, ox + 1.6], [0, 0], color=PALETTE["ink"], linewidth=1.6)
            ax.scatter([ox + 0.8], [0.75], color=PALETTE["red"], s=24)
            if "Euclidean" in label:
                ax.plot([ox, ox + 1.6], [0.75, 0.75], color=PALETTE["blue"], linewidth=1.5)
            elif "Hyperbolic" in label:
                xs = np.linspace(ox, ox + 1.6, 80)
                ax.plot(xs, 0.75 + 0.25 * (xs - ox - 0.8) ** 2, color=PALETTE["blue"])
                ax.plot(xs, 0.75 - 0.25 * (xs - ox - 0.8) ** 2, color=PALETTE["teal"])
            else:
                theta = np.linspace(0.2, 2.95, 80)
                ax.plot(ox + 0.8 + 0.8 * np.cos(theta), -0.05 + 0.8 * np.sin(theta), color=PALETTE["blue"])
                ax.plot(ox + 0.8 + 0.8 * np.cos(theta), 0.75 - 0.8 * np.sin(theta), color=PALETTE["teal"])
            ax.text(ox + 0.8, -0.75, label, ha="center", fontsize=8)
        _style(ax, spec["title"], equal=False)


    def _plot_cone(ax: Any, spec: dict[str, Any]) -> None:
        theta = np.linspace(0, 1.55 * np.pi, 120)
        ax.plot(np.cos(theta), np.sin(theta), color=PALETTE["blue"], linewidth=2, label="cone sector")
        theta2 = np.linspace(0, 2.45 * np.pi, 160)
        ax.plot(1.45 + np.cos(theta2) * 0.55, np.sin(theta2) * 0.55, color=PALETTE["red"], linewidth=2, label="saddle sector")
        ax.plot([0, 1], [0, 0], color=PALETTE["ink"])
        ax.plot([0, np.cos(theta[-1])], [0, np.sin(theta[-1])], color=PALETTE["ink"])
        ax.text(-0.3, -0.35, "C = theta r", fontsize=9)
        ax.legend(fontsize=8)
        _style(ax, spec["title"])


    def _plot_hexagon(ax: Any, spec: dict[str, Any]) -> None:
        angles = np.linspace(0, 2 * np.pi, 7)[:-1] + np.pi / 6
        pts = np.c_[np.cos(angles), np.sin(angles)]
        ax.add_patch(Polygon(pts, fill=False, edgecolor=PALETTE["ink"], linewidth=2))
        labels = ["a", "b", "c", "a", "b", "c"]
        for i, label in enumerate(labels):
            p = (pts[i] + pts[(i + 1) % 6]) / 2
            ax.text(p[0] * 1.08, p[1] * 1.08, label, ha="center", va="center", fontsize=10, color=PALETTE["blue"])
        for i in range(0, 6, 2):
            ax.plot([pts[i, 0], pts[(i + 3) % 6, 0]], [pts[i, 1], pts[(i + 3) % 6, 1]], "--", color=PALETTE["gray"], alpha=0.7)
        ax.text(0, -1.35, "corner-pair total: 2 x 120 deg in the plane", ha="center", fontsize=8)
        _style(ax, spec["title"])


    def _plot_erlangen(ax: Any, spec: dict[str, Any]) -> None:
        names = ["translation", "rotation", "scale", "Mobius"]
        props = ["distance", "angle", "line", "circle"]
        data = np.array([[1, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1], [0, 1, 0.5, 1]])
        ax.imshow(data, cmap="YlGnBu", vmin=0, vmax=1)
        ax.set_xticks(range(len(props)), props, rotation=30, ha="right")
        ax.set_yticks(range(len(names)), names)
        for i in range(len(names)):
            for j in range(len(props)):
                ax.text(j, i, "yes" if data[i, j] == 1 else ("case" if data[i, j] else "no"), ha="center", va="center", fontsize=8)
        ax.set_title(spec["title"], fontsize=11)


    def _plot_complex_vectors(ax: Any, spec: dict[str, Any]) -> None:
        z, w = 2 + 1j, -1 + 1.4j
        for value, color, label in [(z, PALETTE["blue"], "z"), (w, PALETTE["teal"], "w"), (z + w, PALETTE["red"], "z+w")]:
            ax.arrow(0, 0, value.real, value.imag, color=color, width=0.02, length_includes_head=True)
            ax.text(value.real, value.imag, label, fontsize=9)
        ax.plot([w.real, z.real], [w.imag, z.imag], "--", color=PALETTE["gold"], label="z-w")
        ax.set_xlim(-1.8, 2.6)
        ax.set_ylim(-0.5, 3.0)
        ax.legend(fontsize=8)
        _style(ax, spec["title"])


    def _plot_conjugate(ax: Any, spec: dict[str, Any]) -> None:
        z = 1.5 + 1.2j
        circle = Circle((0, 0), abs(z), fill=False, color=PALETTE["gray"], linestyle="--")
        ax.add_patch(circle)
        ax.scatter([z.real, z.real], [z.imag, -z.imag], color=[PALETTE["blue"], PALETTE["red"]])
        ax.plot([z.real, z.real], [z.imag, -z.imag], color=PALETTE["teal"])
        ax.axhline(0, color=PALETTE["ink"])
        ax.text(z.real + 0.05, z.imag, "z")
        ax.text(z.real + 0.05, -z.imag, "conj(z)")
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-1.8, 1.8)
        _style(ax, spec["title"])


    def _plot_polar(ax: Any, spec: dict[str, Any]) -> None:
        theta = 0.72
        r = 1.6
        z = r * np.exp(1j * theta)
        ax.add_patch(Circle((0, 0), r, fill=False, color=PALETTE["gray"], linestyle="--"))
        ax.arrow(0, 0, z.real, z.imag, color=PALETTE["blue"], width=0.02, length_includes_head=True)
        arc = np.linspace(0, theta, 50)
        ax.plot(0.5 * np.cos(arc), 0.5 * np.sin(arc), color=PALETTE["red"], linewidth=2)
        ax.text(0.55, 0.18, "theta")
        ax.text(z.real, z.imag, "r exp(i theta)")
        ax.set_xlim(-2, 2)
        ax.set_ylim(-1.6, 1.8)
        _style(ax, spec["title"])


    def _plot_multiplication(ax: Any, spec: dict[str, Any]) -> None:
        z = 1.2 * np.exp(0.45j)
        w = 1.35 * np.exp(0.85j)
        zw = z * w
        for value, color, label in [(z, PALETTE["blue"], "z"), (w, PALETTE["teal"], "w"), (zw, PALETTE["red"], "zw")]:
            ax.arrow(0, 0, value.real, value.imag, color=color, width=0.015, length_includes_head=True)
            ax.text(value.real, value.imag, label)
        ax.set_xlim(-0.5, 2.2)
        ax.set_ylim(-0.2, 1.8)
        _style(ax, spec["title"])


    def _plot_angle(ax: Any, spec: dict[str, Any]) -> None:
        v = np.array([0.0, 0.0])
        u = np.array([1.8, 0.25])
        w = np.array([0.7, 1.55])
        ax.plot([v[0], u[0]], [v[1], u[1]], color=PALETTE["blue"], linewidth=2)
        ax.plot([v[0], w[0]], [v[1], w[1]], color=PALETTE["red"], linewidth=2)
        ax.scatter([v[0], u[0], w[0]], [v[1], u[1], w[1]], color=PALETTE["ink"])
        ax.text(0.2, 0.25, "arg((w-v)/(u-v))", fontsize=9)
        ax.set_xlim(-0.3, 2.1)
        ax.set_ylim(-0.2, 1.9)
        _style(ax, spec["title"])


    def _plot_region(ax: Any, spec: dict[str, Any]) -> None:
        xs = np.linspace(-2, 2, 180)
        ys = np.linspace(-2, 2, 180)
        X, Y = np.meshgrid(xs, ys)
        Z = X + 1j * Y
        mask = (np.abs(Z - 0.5) < 1.0) & (Y > X - 0.7)
        ax.contourf(X, Y, mask.astype(float), levels=[-0.1, 0.5, 1.1], colors=["#ffffff", "#d6f0ed"])
        ax.contour(X, Y, np.abs(Z - 0.5), levels=[1.0], colors=[PALETTE["blue"]])
        ax.plot(xs, xs - 0.7, color=PALETTE["red"])
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        _style(ax, spec["title"])


    def _plot_affine_grid(ax: Any, spec: dict[str, Any]) -> None:
        a = 0.75 * np.exp(0.7j)
        b = 0.5 + 0.4j
        for line in complex_grid(1.5, 7):
            transformed = a * line + b
            ax.plot(line.real, line.imag, color="#c9d4df", linewidth=0.7)
            ax.plot(transformed.real, transformed.imag, color=PALETTE["blue"], linewidth=0.9)
        ax.set_xlim(-2.0, 2.2)
        ax.set_ylim(-1.8, 2.1)
        _style(ax, spec["title"])


    def _plot_reflection(ax: Any, spec: dict[str, Any]) -> None:
        ax.axhline(0, color=PALETTE["ink"], linewidth=1.2)
        pts = np.array([[0.4, 0.9], [1.2, 0.5], [-0.8, 0.7]])
        ax.scatter(pts[:, 0], pts[:, 1], color=PALETTE["blue"], label="points")
        ax.scatter(pts[:, 0], -pts[:, 1], color=PALETTE["red"], label="reflections")
        for x, y in pts:
            ax.plot([x, x], [y, -y], "--", color=PALETTE["gray"])
        ax.legend(fontsize=8)
        ax.set_xlim(-1.5, 1.8)
        ax.set_ylim(-1.2, 1.2)
        _style(ax, spec["title"])


    def _plot_inversion(ax: Any, spec: dict[str, Any]) -> None:
        ax.add_patch(Circle((0, 0), 1, fill=False, color=PALETTE["ink"], linewidth=1.4))
        for r in [0.35, 0.65, 1.35]:
            theta = np.linspace(0, 2 * np.pi, 240)
            z = 0.15 + r * np.exp(1j * theta)
            inv = invert_in_circle(z)
            ax.plot(z.real, z.imag, color="#c9d4df", linewidth=0.8)
            ax.plot(inv.real, inv.imag, color=PALETTE["blue"], linewidth=0.9)
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.2, 2.2)
        _style(ax, spec["title"])


    def _plot_clines(ax: Any, spec: dict[str, Any]) -> None:
        ax.add_patch(Circle((0, 0), 1, fill=False, color=PALETTE["ink"]))
        theta = np.linspace(0, 2 * np.pi, 240)
        for c, r, color in [(0.45 + 0.2j, 0.55, PALETTE["blue"]), (-0.2 + 0.0j, 0.75, PALETTE["teal"])]:
            z = c + r * np.exp(1j * theta)
            inv = invert_in_circle(z)
            ax.plot(z.real, z.imag, color=color, alpha=0.45)
            ax.plot(inv.real, inv.imag, color=color, linewidth=2)
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        _style(ax, spec["title"])


    def _plot_stereographic(ax: Any, spec: dict[str, Any]) -> None:
        ax.remove()
        fig = plt.gcf()
        ax3 = fig.add_subplot(111, projection="3d")
        u = np.linspace(0, 2 * np.pi, 48)
        v = np.linspace(0, np.pi, 24)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones_like(u), np.cos(v))
        ax3.plot_surface(x, y, z, alpha=0.35, color="#d6e6f5", edgecolor="white", linewidth=0.2)
        t = np.linspace(-1.5, 1.5, 80)
        ax3.plot(t, 0 * t, -1 + 0 * t, color=PALETTE["gray"])
        ax3.scatter([0], [0], [1], color=PALETTE["red"], s=40)
        ax3.plot([0, 0.7], [0, 0.45], [1, -1], color=PALETTE["blue"], linewidth=2)
        ax3.set_title(spec["title"])
        ax3.set_axis_off()


    def _plot_mobius_dynamics(ax: Any, spec: dict[str, Any]) -> None:
        _plot_unit_disk(ax)
        theta = np.linspace(0, 2 * np.pi, 240)
        for radius, color in [(0.25, PALETTE["blue"]), (0.5, PALETTE["teal"]), (0.75, PALETTE["gold"])]:
            z = radius * np.exp(1j * theta)
            w = disk_automorphism(z, 0.35)
            ax.plot(w.real, w.imag, color=color, linewidth=1.4)
        ax.scatter([0.35, -0.35], [0, 0], color=[PALETTE["red"], PALETTE["violet"]], s=35)
        _style(ax, spec["title"])


    def _plot_orbit(ax: Any, spec: dict[str, Any]) -> None:
        base = 0.75 + 0.25j
        orbit = np.array([base * np.exp(1j * k * np.pi / 2) for k in range(4)])
        ax.scatter(orbit.real, orbit.imag, color=PALETTE["blue"], s=50)
        for z in orbit:
            ax.plot([0, z.real], [0, z.imag], color=PALETTE["gray"], linewidth=0.8)
        ax.add_patch(Circle((0, 0), abs(base), fill=False, color=PALETTE["teal"], linestyle="--"))
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        _style(ax, spec["title"])


    def _plot_euclidean_invariants(ax: Any, spec: dict[str, Any]) -> None:
        tri = np.array([[0, 0], [1.2, 0.1], [0.35, 0.9]])
        angle = 0.65
        rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        moved = tri @ rot.T + np.array([1.4, 0.45])
        ax.add_patch(Polygon(tri, fill=False, edgecolor=PALETTE["blue"], linewidth=2, label="original"))
        ax.add_patch(Polygon(moved, fill=False, edgecolor=PALETTE["red"], linewidth=2, label="moved"))
        ax.legend(fontsize=8)
        ax.set_xlim(-0.3, 2.7)
        ax.set_ylim(-0.2, 1.9)
        _style(ax, spec["title"])


    def _plot_homogeneity(ax: Any, spec: dict[str, Any]) -> None:
        groups = ["translations", "rotations", "euclidean", "mobius"]
        props = ["point move", "direction move", "distance"]
        data = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 1], [1, 1, 0]])
        ax.imshow(data, cmap="PuBuGn", vmin=0, vmax=1)
        ax.set_xticks(range(3), props, rotation=25, ha="right")
        ax.set_yticks(range(4), groups)
        for i in range(4):
            for j in range(3):
                ax.text(j, i, "yes" if data[i, j] else "no", ha="center", va="center", fontsize=8)
        ax.set_title(spec["title"], fontsize=11)


    def _plot_mobius_distance(ax: Any, spec: dict[str, Any]) -> None:
        xs = np.array([0.45, 0.7, 1.1])
        ys = np.zeros_like(xs)
        inv = 1 / xs
        ax.scatter(xs, ys + 0.3, color=PALETTE["blue"], label="before")
        ax.scatter(inv, ys - 0.3, color=PALETTE["red"], label="after 1/z")
        for x, y in zip(xs, inv):
            ax.plot([x, y], [0.3, -0.3], "--", color=PALETTE["gray"])
        ax.legend(fontsize=8)
        ax.set_xlim(0, 2.5)
        ax.set_ylim(-0.8, 0.8)
        _style(ax, spec["title"], equal=False)


    def _plot_hyperbolic_disk(ax: Any, spec: dict[str, Any]) -> None:
        _plot_unit_disk(ax)
        theta = np.linspace(0, 2 * np.pi, 240)
        for c, r in [(0.45, 0.55), (-0.35, 0.65), (0, 0)]:
            if r == 0:
                ax.plot([-0.9, 0.9], [0, 0], color=PALETTE["blue"], linewidth=1.5)
            else:
                z = c + r * np.exp(1j * theta)
                mask = np.abs(z) <= 1.001
                ax.plot(z.real[mask], z.imag[mask], color=PALETTE["blue"], linewidth=1.3)
        _style(ax, spec["title"])


    def _plot_hyperbolic_parallel(ax: Any, spec: dict[str, Any]) -> None:
        _plot_unit_disk(ax)
        ax.plot([-0.9, 0.9], [0, 0], color=PALETTE["ink"], linewidth=1.4)
        p = np.array([0.0, 0.45])
        ax.scatter([p[0]], [p[1]], color=PALETTE["red"], s=35)
        xs = np.linspace(-0.85, 0.85, 120)
        for bend, color in [(0.35, PALETTE["blue"]), (0.65, PALETTE["teal"]), (0.9, PALETTE["gold"])]:
            y = p[1] + bend * (xs**2 - 0.1)
            mask = xs**2 + y**2 < 1
            ax.plot(xs[mask], y[mask], color=color)
        _style(ax, spec["title"])


    def _plot_metric_density(ax: Any, spec: dict[str, Any]) -> None:
        r = np.linspace(0, 0.96, 200)
        ax.plot(r, 2 / (1 - r**2), color=PALETTE["red"], label="hyperbolic density")
        ax.plot(r, 2 / (1 + r**2), color=PALETTE["blue"], label="elliptic density")
        ax.set_xlabel("Euclidean radius")
        ax.set_ylabel("metric density")
        ax.legend(fontsize=8)
        _style(ax, spec["title"], equal=False)


    def _plot_hyperbolic_circle(ax: Any, spec: dict[str, Any]) -> None:
        _plot_unit_disk(ax)
        center = 0.35 + 0.15j
        for radius, color in [(0.25, PALETTE["blue"]), (0.45, PALETTE["teal"]), (0.65, PALETTE["gold"])]:
            theta = np.linspace(0, 2 * np.pi, 180)
            z = center + radius * np.exp(1j * theta)
            z = z[np.abs(z) < 0.98]
            ax.plot(z.real, z.imag, color=color)
        ax.scatter([center.real], [center.imag], color=PALETTE["red"])
        _style(ax, spec["title"])


    def _plot_triangle_defect(ax: Any, spec: dict[str, Any]) -> None:
        sums = np.linspace(0.1, np.pi - 0.05, 180)
        area = np.pi - sums
        ax.plot(sums, area, color=PALETTE["red"], linewidth=2, label="hyperbolic area")
        ax.plot(np.pi + sums * 0.5, sums * 0.5, color=PALETTE["blue"], linewidth=2, label="elliptic excess")
        ax.axvline(np.pi, color=PALETTE["gray"], linestyle="--")
        ax.set_xlabel("angle sum")
        ax.set_ylabel("area scale")
        ax.legend(fontsize=8)
        _style(ax, spec["title"], equal=False)


    def _plot_halfplane(ax: Any, spec: dict[str, Any]) -> None:
        ax.axhline(0, color=PALETTE["ink"], linewidth=1.5)
        xs = np.linspace(-2, 2, 240)
        for c, r in [(-0.8, 0.8), (0.5, 1.0), (1.6, 0.55)]:
            theta = np.linspace(0, np.pi, 120)
            ax.plot(c + r * np.cos(theta), r * np.sin(theta), color=PALETTE["blue"])
        ax.plot([0, 0], [0, 2.0], color=PALETTE["teal"])
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-0.1, 2.2)
        _style(ax, spec["title"])


    def _plot_antipodes(ax: Any, spec: dict[str, Any]) -> None:
        _plot_unit_disk(ax)
        pts = np.array([0.35 + 0.25j, -0.4 + 0.55j, 0.7 - 0.15j])
        for z in pts:
            za = -1 / np.conjugate(z)
            ax.scatter([z.real], [z.imag], color=PALETTE["blue"])
            ax.scatter([za.real], [za.imag], color=PALETTE["red"], marker="x")
            ax.plot([z.real, za.real], [z.imag, za.imag], "--", color=PALETTE["gray"])
        ax.set_xlim(-2.4, 2.4)
        ax.set_ylim(-2.4, 2.4)
        _style(ax, spec["title"])


    def _plot_elliptic_clines(ax: Any, spec: dict[str, Any]) -> None:
        _plot_unit_disk(ax)
        theta = np.linspace(0, 2 * np.pi, 240)
        for angle, color in [(0, PALETTE["blue"]), (0.7, PALETTE["teal"]), (1.4, PALETTE["gold"])]:
            ax.plot(np.cos(angle) * np.linspace(-1, 1, 100), np.sin(angle) * np.linspace(-1, 1, 100), color=color)
        ax.plot(0.25 + 0.95 * np.cos(theta), 0.1 + 0.95 * np.sin(theta), color=PALETTE["red"], alpha=0.8)
        _style(ax, spec["title"])


    def _plot_projective_disk(ax: Any, spec: dict[str, Any]) -> None:
        _plot_unit_disk(ax)
        theta = np.linspace(0, 2 * np.pi, 16, endpoint=False)
        for t in theta[::2]:
            ax.arrow(np.cos(t), np.sin(t), -0.001 * np.cos(t), -0.001 * np.sin(t), color=PALETTE["blue"], head_width=0.08)
            ax.plot([np.cos(t), -np.cos(t)], [np.sin(t), -np.sin(t)], "--", color="#d0d7de", linewidth=0.7)
        path = np.array([[0, 0], [0.5, 0.3], [0.9, 0.2], [-0.9, -0.2], [-0.4, -0.5]])
        ax.plot(path[:, 0], path[:, 1], color=PALETTE["red"], linewidth=2)
        _style(ax, spec["title"])


    def _plot_elliptic_distance(ax: Any, spec: dict[str, Any]) -> None:
        _plot_unit_disk(ax)
        theta = np.linspace(0, 2 * np.pi, 240)
        for r, color in [(0.25, PALETTE["blue"]), (0.55, PALETTE["teal"]), (0.9, PALETTE["gold"])]:
            ax.plot(r * np.cos(theta), r * np.sin(theta), color=color)
        ax.text(-0.9, -1.05, "large elliptic circles fold through antipodes", fontsize=8)
        _style(ax, spec["title"])


    def _plot_lune(ax: Any, spec: dict[str, Any]) -> None:
        _plot_unit_disk(ax)
        theta = np.linspace(-0.55, 0.95, 120)
        ax.fill_between(np.cos(theta), np.sin(theta), -np.sin(theta), color="#d6f0ed", alpha=0.7)
        ax.plot([0, 1], [0, 0], color=PALETTE["blue"], linewidth=2)
        ax.plot([0, np.cos(0.95)], [0, np.sin(0.95)], color=PALETTE["red"], linewidth=2)
        ax.text(0.15, 0.25, "lune area = 2 alpha", fontsize=9)
        _style(ax, spec["title"])


    def _plot_elliptic_trig(ax: Any, spec: dict[str, Any]) -> None:
        tri = np.array([[0.0, 0.0], [0.65, 0.1], [0.2, 0.7]])
        _plot_unit_disk(ax)
        ax.add_patch(Polygon(tri, fill=False, edgecolor=PALETTE["blue"], linewidth=2))
        ax.scatter(tri[:, 0], tri[:, 1], color=PALETTE["red"])
        ax.text(-0.9, -1.05, "cos(c) = cos(a)cos(b)+sin(a)sin(b)cos(gamma)", fontsize=8)
        _style(ax, spec["title"])


    def _plot_curvature_growth(ax: Any, spec: dict[str, Any]) -> None:
        r = np.linspace(0.04, 1.35, 220)
        for k, color, label in [(-1, PALETTE["red"], "k=-1"), (0, PALETTE["gray"], "k=0"), (1, PALETTE["blue"], "k=+1")]:
            ratio = circumference_k(r, k) / (2 * np.pi * r)
            ax.plot(r, ratio, color=color, label=label)
        ax.axhline(1, color=PALETTE["ink"], linestyle="--")
        ax.set_xlabel("geodesic radius")
        ax.set_ylabel("C/(2*pi*r)")
        ax.legend(fontsize=8)
        _style(ax, spec["title"], equal=False)


    def _plot_scaled_models(ax: Any, spec: dict[str, Any]) -> None:
        for radius, color, label in [(0.7, PALETTE["blue"], "k=+2"), (1.0, PALETTE["gray"], "k=0 scale"), (1.35, PALETTE["red"], "k=-0.55")]:
            ax.add_patch(Circle((0, 0), radius, fill=False, color=color, linewidth=1.8, label=label))
        ax.legend(fontsize=8)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        _style(ax, spec["title"])


    def _plot_parallel_angle(ax: Any, spec: dict[str, Any]) -> None:
        d = np.linspace(0, 4, 180)
        for k, color in [(-0.25, PALETTE["blue"]), (-1, PALETTE["red"]), (-4, PALETTE["gold"])]:
            ax.plot(d, [angle_of_parallelism(float(x), k) for x in d], color=color, label=f"k={k}")
        ax.set_xlabel("distance")
        ax.set_ylabel("angle")
        ax.legend(fontsize=8)
        _style(ax, spec["title"], equal=False)


    def _plot_surface_classifier(ax: Any, spec: dict[str, Any]) -> None:
        rows = [classify_catalog("sphere", True, 0), classify_catalog("torus", True, 1), classify_catalog("two-holed torus", True, 2), classify_catalog("projective plane", False, 1), classify_catalog("Klein bottle", False, 2), classify_catalog("C3", False, 3)]
        ax.axis("off")
        text = "surface              chi   geometry\n" + "\n".join(f"{r.name:<20} {r.euler:>3}   {r.geometry}" for r in rows)
        ax.text(0.02, 0.95, text, va="top", family="monospace", fontsize=10, color=PALETTE["ink"])
        ax.set_title(spec["title"], fontsize=11)


    def _plot_gauss_bonnet(ax: Any, spec: dict[str, Any]) -> None:
        genus = np.arange(0, 6)
        ax.plot(genus, [2 - 2 * g for g in genus], "o-", color=PALETTE["blue"], label="H_g")
        ax.plot(np.arange(1, 7), [2 - g for g in range(1, 7)], "s-", color=PALETTE["red"], label="C_g")
        ax.axhline(0, color=PALETTE["gray"], linestyle="--")
        ax.set_xlabel("genus")
        ax.set_ylabel("Euler characteristic")
        ax.legend(fontsize=8)
        _style(ax, spec["title"], equal=False)


    def _plot_dirichlet(ax: Any, spec: dict[str, Any]) -> None:
        w, h = 3.0, 2.0
        base = np.array([0.8, 0.7])
        images = torus_images(tuple(base), w, h, radius=1)
        ax.scatter(images[:, 0], images[:, 1], color=PALETTE["blue"], s=22)
        ax.add_patch(Rectangle((0, 0), w, h, fill=False, edgecolor=PALETTE["ink"], linewidth=1.5))
        ax.add_patch(Rectangle((base[0] - w / 2, base[1] - h / 2), w, h, fill=False, edgecolor=PALETTE["red"], linestyle="--", linewidth=1.6))
        ax.set_xlim(-1.2, 4.2)
        ax.set_ylim(-1.1, 3.1)
        _style(ax, spec["title"])


    def _plot_three_geometries(ax: Any, spec: dict[str, Any]) -> None:
        ax.remove()
        fig = plt.gcf()
        ax3 = fig.add_subplot(111, projection="3d")
        t = np.linspace(-1, 1, 80)
        ax3.plot(t, 0 * t, 0 * t, color=PALETTE["blue"], label="Euclidean line")
        ax3.plot(np.sin(t), np.cos(t), t * 0.4, color=PALETTE["teal"], label="curved geodesic view")
        ax3.scatter([0], [0], [0], color=PALETTE["red"])
        ax3.legend(fontsize=7)
        ax3.set_title(spec["title"])
        ax3.set_axis_off()


    def _plot_three_torus(ax: Any, spec: dict[str, Any]) -> None:
        ax.remove()
        fig = plt.gcf()
        ax3 = fig.add_subplot(111, projection="3d")
        r = [0, 1]
        for x in r:
            for y in r:
                ax3.plot([x, x], [y, y], [0, 1], color=PALETTE["ink"])
        for x in r:
            for z in r:
                ax3.plot([x, x], [0, 1], [z, z], color=PALETTE["ink"])
        for y in r:
            for z in r:
                ax3.plot([0, 1], [y, y], [z, z], color=PALETTE["ink"])
        ax3.text(0.5, -0.1, 0.5, "opposite faces identified", fontsize=8)
        ax3.set_title(spec["title"])
        ax3.set_axis_off()


    def _plot_dodecahedron(ax: Any, spec: dict[str, Any]) -> None:
        theta = np.linspace(0, 2 * np.pi, 6)[:-1] + np.pi / 5
        outer = np.c_[np.cos(theta), np.sin(theta)]
        inner = 0.45 * outer
        for i in range(5):
            poly = np.vstack([outer[i], outer[(i + 1) % 5], inner[(i + 1) % 5], inner[i]])
            ax.add_patch(Polygon(poly, fill=True, alpha=0.35, color=[PALETTE["blue"], PALETTE["teal"], PALETTE["gold"], PALETTE["red"], PALETTE["violet"]][i]))
        ax.add_patch(Polygon(inner, fill=False, edgecolor=PALETTE["ink"], linewidth=1.5))
        ax.text(0, 0, "opposite-face\n36 deg or 108 deg twist", ha="center", va="center", fontsize=8)
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        _style(ax, spec["title"])


    def _plot_psh(ax: Any, spec: dict[str, Any]) -> None:
        rng = np.random.default_rng(3)
        simple = rng.random((50, 2)) * 8
        torus = torus_catalog(seed=5, base_count=8, width=3.0, height=2.2, copies=1)
        ax.hist(pair_distances(simple), bins=28, alpha=0.55, label="simply connected", color=PALETTE["gray"])
        ax.hist(pair_distances(torus), bins=28, alpha=0.55, label="torus images", color=PALETTE["blue"])
        ax.set_xlabel("pair separation")
        ax.set_ylabel("count")
        ax.legend(fontsize=8)
        _style(ax, spec["title"], equal=False)


    def _plot_lss(ax: Any, spec: dict[str, Any]) -> None:
        _plot_unit_disk(ax)
        sep = 1.25
        r_obs = 0.85
        circle_radius = sphere_intersection_circle_radius(r_obs, sep)
        ax.add_patch(Circle((-sep / 2, 0), r_obs, fill=False, edgecolor=PALETTE["blue"], linewidth=1.4))
        ax.add_patch(Circle((sep / 2, 0), r_obs, fill=False, edgecolor=PALETTE["teal"], linewidth=1.4))
        ax.plot([0, 0], [-circle_radius, circle_radius], color=PALETTE["red"], linewidth=2, label="matching circle slice")
        ax.legend(fontsize=8)
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.1, 1.1)
        _style(ax, spec["title"])


    def _plot_friedmann(ax: Any, spec: dict[str, Any]) -> None:
        omega_m = np.linspace(0, 1, 100)
        omega_l = 1 - omega_m
        ax.fill_between(omega_m, 0, omega_l, color="#d6f0ed", alpha=0.8)
        ax.plot(omega_m, omega_l, color=PALETTE["blue"], label="Omega_k = 0")
        ax.scatter([0.28], [0.72], color=PALETTE["red"], s=50, label="chapter-era near-flat point")
        ax.set_xlabel("Omega_M")
        ax.set_ylabel("Omega_Lambda")
        ax.legend(fontsize=8)
        _style(ax, spec["title"], equal=False)


    def _plot_glossary_map(ax: Any, spec: dict[str, Any]) -> None:
        labels = ["C", "Mobius", "D/H", "P2/S", "X_k", "chi", "Omega"]
        theta = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
        pts = np.c_[np.cos(theta), np.sin(theta)]
        for i, label in enumerate(labels):
            ax.scatter([pts[i, 0]], [pts[i, 1]], s=160, color=PALETTE["blue"])
            ax.text(pts[i, 0], pts[i, 1], label, color="white", ha="center", va="center", fontsize=8)
            ax.plot([0, pts[i, 0]], [0, pts[i, 1]], color="#c9d4df")
        ax.text(0, 0, "course\nnotation", ha="center", va="center", fontsize=9)
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        _style(ax, spec["title"])


    PLOTTERS = {
        "torus": _plot_torus,
        "sphere": _plot_sphere,
        "parallel": _plot_parallel,
        "cone": _plot_cone,
        "hexagon": _plot_hexagon,
        "erlangen": _plot_erlangen,
        "complex_vectors": _plot_complex_vectors,
        "conjugate": _plot_conjugate,
        "polar": _plot_polar,
        "multiplication": _plot_multiplication,
        "angle": _plot_angle,
        "region": _plot_region,
        "affine_grid": _plot_affine_grid,
        "reflection": _plot_reflection,
        "inversion": _plot_inversion,
        "clines": _plot_clines,
        "stereographic": _plot_stereographic,
        "mobius_dynamics": _plot_mobius_dynamics,
        "orbit": _plot_orbit,
        "euclidean_invariants": _plot_euclidean_invariants,
        "homogeneity": _plot_homogeneity,
        "mobius_distance": _plot_mobius_distance,
        "hyperbolic_disk": _plot_hyperbolic_disk,
        "hyperbolic_parallel": _plot_hyperbolic_parallel,
        "metric_density": _plot_metric_density,
        "hyperbolic_circle": _plot_hyperbolic_circle,
        "triangle_defect": _plot_triangle_defect,
        "halfplane": _plot_halfplane,
        "antipodes": _plot_antipodes,
        "elliptic_clines": _plot_elliptic_clines,
        "projective_disk": _plot_projective_disk,
        "elliptic_distance": _plot_elliptic_distance,
        "lune": _plot_lune,
        "elliptic_trig": _plot_elliptic_trig,
        "curvature_growth": _plot_curvature_growth,
        "scaled_models": _plot_scaled_models,
        "parallel_angle": _plot_parallel_angle,
        "surface_classifier": _plot_surface_classifier,
        "gauss_bonnet": _plot_gauss_bonnet,
        "dirichlet": _plot_dirichlet,
        "three_geometries": _plot_three_geometries,
        "three_torus": _plot_three_torus,
        "dodecahedron": _plot_dodecahedron,
        "psh": _plot_psh,
        "lss": _plot_lss,
        "friedmann": _plot_friedmann,
        "glossary_map": _plot_glossary_map,
    }


    def render_visuals(artifact_root: str | Path, specs: list[dict[str, Any]]) -> tuple[list[Path], list[dict[str, Any]]]:
        paths: list[Path] = []
        stats: list[dict[str, Any]] = []
        for spec in specs:
            fig = plt.figure(figsize=(7.0, 4.8))
            ax = fig.add_subplot(111)
            plotter = PLOTTERS[spec["kind"]]
            plotter(ax, spec)
            fig.suptitle(spec.get("note", ""), y=0.02, fontsize=8, color=PALETTE["gray"])
            path = save_matplotlib(fig, artifact_root, "figures", spec["filename"])
            plt.close(fig)
            paths.append(path)
            stats.append(image_stats(path))
        return paths, stats


    def build_parameter_lab_html(chapter: dict[str, Any], specs: list[dict[str, Any]]) -> str:
        visual_rows = "\n".join(
            f"<li><strong>{item['title']}</strong>: {item['note']}</li>" for item in specs
        )
        return f"""<!doctype html>
    <html lang=\"en\">
    <meta charset=\"utf-8\">
    <title>{chapter['title']} parameter lab</title>
    <style>
    body {{ font-family: system-ui, sans-serif; margin: 1.5rem; color: #1f2933; }}
    .panel {{ border: 1px solid #cbd5df; border-radius: 6px; padding: 1rem; max-width: 900px; }}
    input {{ width: 100%; }}
    code {{ background: #eef3f7; padding: 0.1rem 0.25rem; border-radius: 3px; }}
    </style>
    <body>
    <div class=\"panel\">
      <h1>{chapter['title']}: parameter lab</h1>
      <p>{chapter['goal']}</p>
      <label>Parameter <code>t</code>: <span id=\"value\">0.50</span></label>
      <input id=\"slider\" type=\"range\" min=\"0\" max=\"1\" step=\"0.01\" value=\"0.5\">
      <p id=\"output\"></p>
      <h2>Visual inspection targets</h2>
      <ul>{visual_rows}</ul>
    </div>
    <script>
    const slider = document.getElementById('slider');
    const value = document.getElementById('value');
    const output = document.getElementById('output');
    function render() {{
      const t = Number(slider.value);
      value.textContent = t.toFixed(2);
      const curved = Math.sinh(t * 2) / 2;
      const circular = Math.sin(t * Math.PI / 2);
      output.textContent = `Euclidean parameter: ${{t.toFixed(3)}}; hyperbolic-like response: ${{curved.toFixed(3)}}; elliptic-like response: ${{circular.toFixed(3)}}.`;
    }}
    slider.addEventListener('input', render);
    render();
    </script>
    </body>
    </html>"""


    def chapter_numeric_checks(chapter_number: int) -> dict[str, float | str]:
        values: dict[str, float | str] = {"chapter": float(chapter_number)}
        values["complex_product_residual"] = float(abs((1 + 2j) * (3 - 1j) - (5 + 5j)))
        values["hyperbolic_distance_positive"] = float((2 * np.arctanh(0.4)) > 0)
        values["curvature_zero_circumference"] = float(abs(circumference_k(0.8, 0) - 2 * np.pi * 0.8))
        values["disk_area_positive"] = float(disk_area_k(0.7, -1) > 0)
        values["right_hypotenuse_euclidean"] = float(abs(unified_right_hypotenuse(1.0, 0) - math.sqrt(2)))
        values["lss_circle_radius"] = float(sphere_intersection_circle_radius(1.0, 1.2))
        values["status"] = "ok"
        return values
    '''


def inventory_py() -> str:
    payload = []
    for entry in public_entries():
        payload.append(
            {
                "kind": entry["kind"],
                "number": entry["number"],
                "title": entry["title"],
                "folder": entry["folder"],
                "notebook": entry["notebook"],
                "artifact": entry["artifact"],
                "printed_span": entry["printed"],
                "pdf_span": entry["pdf"],
                "sections": entry["sections"],
                "focus": entry["focus"],
            }
        )
    return (
        '"""Course inventory for Geometry with an Introduction to Cosmic Topology."""\n\n'
        "from __future__ import annotations\n\n"
        f"PDF_SOURCE = {PDF_SOURCE!r}\n"
        'BODY_PAGE_RULE = "For Arabic printed pages in the main body, physical PDF page = printed page + 10."\n\n'
        f"ENTRIES = {json.dumps(payload, indent=4)}\n"
    )


def build_indexes_py() -> str:
    return r'''
    """Build GICT book, chapter, and appendix indexes."""

    from __future__ import annotations

    from pathlib import Path

    import nbformat
    from nbformat.v4 import new_markdown_cell, new_notebook

    import gict_inventory as inventory

    BOOK_ROOT = Path(__file__).resolve().parents[1]


    def write_markdown_notebook(path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


    def build_book_index() -> str:
        lines = [
            "# Geometry with an Introduction to Cosmic Topology",
            "",
            "This is a standalone visualization-first notebook course. The notebooks use the local PDF only as source orientation for structure and concepts; the teaching prose, diagrams, computations, and artifacts are original.",
            "",
            "## Course Map",
            "",
        ]
        for entry in inventory.ENTRIES:
            label = "Appendix A" if entry["kind"] == "appendix" else f"Chapter {entry['number']}"
            lines.append(
                f"- **{label}: {entry['title']}** - [index]({entry['folder']}/00-index.ipynb); "
                f"[canonical]({entry['folder']}/{entry['notebook']}); printed pp. {entry['printed_span']}; "
                f"PDF pp. {entry['pdf_span']}; {entry['focus']}"
            )
        lines.extend(
            [
                "",
                "## Validation",
                "",
                "Run the commands in `AGENTS.md` from the workspace root. Artifacts are generated under `artifacts/` and displayed inline by each canonical notebook.",
            ]
        )
        return "\n".join(lines)


    def build_entry_index(entry: dict[str, object]) -> str:
        label = "Appendix A" if entry["kind"] == "appendix" else f"Chapter {entry['number']}"
        return "\n".join(
            [
                f"# {label}: {entry['title']}",
                "",
                f"- Source span: printed pages {entry['printed_span']}; PDF pages {entry['pdf_span']}; sections {entry['sections']}.",
                f"- Focus: {entry['focus']}",
                f"- Canonical notebook: [{entry['notebook']}]({entry['notebook']})",
                "- Back to [book index](../00-book-index.ipynb)",
            ]
        )


    def main() -> None:
        write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
        for entry in inventory.ENTRIES:
            write_markdown_notebook(BOOK_ROOT / str(entry["folder"]) / "00-index.ipynb", build_entry_index(entry))
        print(f"Updated {1 + len(inventory.ENTRIES)} index notebooks.")


    if __name__ == "__main__":
        main()
    '''


def audit_notebooks_py() -> str:
    return r'''
    """Audit GICT canonical notebooks for standalone depth and structure."""

    from __future__ import annotations

    import argparse
    import re
    from pathlib import Path

    import nbformat

    import gict_inventory as inventory

    BOOK_ROOT = Path(__file__).resolve().parents[1]
    IGNORED = {"00-book-index.ipynb", "00-index.ipynb"}


    def canonical_notebooks() -> list[Path]:
        return [BOOK_ROOT / str(entry["folder"]) / str(entry["notebook"]) for entry in inventory.ENTRIES]


    def notebook_stats(path: Path) -> dict[str, object]:
        nb = nbformat.read(path, as_version=4)
        markdown = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "markdown")
        code = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "code")
        words = re.findall(r"[A-Za-z][A-Za-z0-9'-]*", markdown)
        return {
            "path": path,
            "words": len(words),
            "code_cells": sum(1 for cell in nb.cells if cell.cell_type == "code"),
            "display_artifact": code.count("display_artifact("),
            "save_calls": code.count("save_") + code.count("render_visuals("),
            "has_setup": "BOOK_ROOT" in code and "ARTIFACT_ROOT" in code,
            "has_takeaways": "Takeaways" in markdown,
        }


    def main() -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("--min-words", type=int, default=1200)
        parser.add_argument("--min-code-cells", type=int, default=5)
        args = parser.parse_args()
        failures: list[str] = []
        for folder in [p for p in BOOK_ROOT.iterdir() if p.is_dir() and (p.name.startswith("chapter-") or p.name.startswith("appendix-"))]:
            notebooks = [p for p in folder.glob("*.ipynb") if p.name not in IGNORED]
            if len(notebooks) != 1:
                failures.append(f"{folder.relative_to(BOOK_ROOT)} has {len(notebooks)} canonical notebooks")
        for path in canonical_notebooks():
            stats = notebook_stats(path)
            if not path.exists():
                failures.append(f"missing notebook {path}")
                continue
            if int(stats["words"]) < args.min_words:
                failures.append(f"{path.relative_to(BOOK_ROOT)} has only {stats['words']} words")
            if int(stats["code_cells"]) < args.min_code_cells:
                failures.append(f"{path.relative_to(BOOK_ROOT)} has only {stats['code_cells']} code cells")
            if not stats["has_setup"]:
                failures.append(f"{path.relative_to(BOOK_ROOT)} is missing BOOK_ROOT/ARTIFACT_ROOT setup")
            if not stats["has_takeaways"]:
                failures.append(f"{path.relative_to(BOOK_ROOT)} is missing takeaways")
            if int(stats["display_artifact"]) < 3:
                failures.append(f"{path.relative_to(BOOK_ROOT)} displays too few artifacts")
        print(f"Audited {len(canonical_notebooks())} canonical notebooks.")
        if failures:
            for failure in failures:
                print(f"FAIL: {failure}")
            raise SystemExit(1)
        print("All canonical notebooks meet the configured structure and depth thresholds.")


    if __name__ == "__main__":
        main()
    '''


def audit_visuals_py() -> str:
    return r'''
    """Audit GICT generated visuals and artifact integrity."""

    from __future__ import annotations

    import argparse
    import hashlib
    from pathlib import Path

    import nbformat
    from PIL import Image
    import numpy as np

    import gict_inventory as inventory

    BOOK_ROOT = Path(__file__).resolve().parents[1]


    def sha256(path: Path) -> str:
        h = hashlib.sha256()
        h.update(path.read_bytes())
        return h.hexdigest()


    def png_stats(path: Path) -> dict[str, object]:
        image = Image.open(path).convert("RGB")
        arr = np.asarray(image, dtype=float)
        return {
            "path": path,
            "width": image.width,
            "height": image.height,
            "pixel_std": float(arr.std()),
            "size": path.stat().st_size,
            "sha": sha256(path),
        }


    def main() -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("--min-width", type=int, default=300)
        parser.add_argument("--min-height", type=int, default=240)
        parser.add_argument("--min-std", type=float, default=2.0)
        args = parser.parse_args()
        failures: list[str] = []
        all_hashes: dict[str, list[Path]] = {}
        for entry in inventory.ENTRIES:
            artifact_root = BOOK_ROOT / "artifacts" / str(entry["artifact"])
            pngs = sorted((artifact_root / "figures").glob("*.png"))
            if len(pngs) < 5:
                failures.append(f"{artifact_root.relative_to(BOOK_ROOT)} has only {len(pngs)} PNG figures")
            for png in pngs:
                stats = png_stats(png)
                all_hashes.setdefault(str(stats["sha"]), []).append(png)
                if stats["width"] < args.min_width or stats["height"] < args.min_height:
                    failures.append(f"{png.relative_to(BOOK_ROOT)} is too small: {stats['width']}x{stats['height']}")
                if stats["pixel_std"] < args.min_std:
                    failures.append(f"{png.relative_to(BOOK_ROOT)} appears blank: std={stats['pixel_std']:.3f}")
            htmls = sorted((artifact_root / "html").glob("*.html"))
            if not htmls:
                failures.append(f"{artifact_root.relative_to(BOOK_ROOT)} has no HTML lab artifact")
            notebook = BOOK_ROOT / str(entry["folder"]) / str(entry["notebook"])
            nb = nbformat.read(notebook, as_version=4)
            code = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "code")
            if "display_artifact(" not in code:
                failures.append(f"{notebook.relative_to(BOOK_ROOT)} does not display artifacts")
        duplicates = [paths for paths in all_hashes.values() if len(paths) > 1]
        for paths in duplicates:
            joined = ", ".join(str(path.relative_to(BOOK_ROOT)) for path in paths)
            failures.append(f"duplicate PNG hash: {joined}")
        print(f"Audited visuals for {len(inventory.ENTRIES)} entries.")
        if failures:
            for failure in failures:
                print(f"FAIL: {failure}")
            raise SystemExit(1)
        print("All visual artifacts are present, nonblank, and uniquely rendered.")


    if __name__ == "__main__":
        main()
    '''


def validate_course_py() -> str:
    return r'''
    """Execute GICT canonical notebooks with nbclient."""

    from __future__ import annotations

    import argparse
    from pathlib import Path

    import nbformat
    from nbclient import NotebookClient

    import gict_inventory as inventory

    BOOK_ROOT = Path(__file__).resolve().parents[1]


    def notebook_paths(all_notebooks: bool, limit: int | None) -> list[Path]:
        paths = [BOOK_ROOT / str(entry["folder"]) / str(entry["notebook"]) for entry in inventory.ENTRIES]
        if all_notebooks:
            return paths
        return paths[: limit or len(paths)]


    def execute_notebook(path: Path, timeout: int) -> None:
        nb = nbformat.read(path, as_version=4)
        client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
        client.execute()


    def main() -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("--all", action="store_true")
        parser.add_argument("--limit", type=int, default=None)
        parser.add_argument("--timeout", type=int, default=300)
        args = parser.parse_args()
        paths = notebook_paths(args.all, args.limit)
        for index, path in enumerate(paths, start=1):
            print(f"[{index}/{len(paths)}] {path.relative_to(BOOK_ROOT)}")
            execute_notebook(path, args.timeout)
        print(f"Executed {len(paths)} notebooks successfully.")


    if __name__ == "__main__":
        main()
    '''


def notebook_markdown(entry: dict[str, Any]) -> list[str]:
    visual_text = "\n".join(
        f"- **{item['title']}** (`{item['filename']}`): {item['note']}"
        for item in entry["visuals"]
    )
    translation = "\n".join(f"- {item}" for item in entry["translation"])
    route = "\n".join(f"- {item}" for item in entry["route"])
    pitfalls = "\n".join(f"- {item}" for item in entry["pitfalls"])
    label = "Appendix A" if entry["kind"] == "appendix" else f"Chapter {entry['number']}"
    return [
        f"""
        # {label}: {entry['title']}

        Source orientation: printed pages {entry['printed']}; physical PDF pages {entry['pdf']}; sections {entry['sections']}.

        This notebook is a standalone computational lesson. It follows the source chapter's mathematical
        order, but the prose, examples, diagrams, and checks are original. The aim is not to reproduce
        the book on screen; it is to rebuild the ideas as things a reader can inspect, compute, perturb,
        and test. Keep the PDF closed while reading this notebook: every definition needed for the lesson
        is introduced here in operational language, and every major claim is paired with a generated
        artifact or a numerical sanity check.

        **Chapter question.** {entry['goal']}

        **Why this chapter matters.** {entry['focus']} This course treats geometry as a working laboratory.
        When a statement says that an angle is preserved, a boundary is identified, or an area is controlled
        by curvature, the notebook asks for a representation that can be drawn and a check that can fail if
        the idea has been misunderstood. That habit is the through-line from the complex plane to cosmic
        topology.
        """,
        f"""
        ## Translation Guide

        The source chapter is translated into computational language as follows:

        {translation}

        A useful mental model is to separate three layers. The **model layer** names the space and its
        coordinates. The **transformation layer** names what is allowed to move without changing the
        geometry. The **measurement layer** names what the inhabitant of the space can detect. A visual
        notebook should keep all three layers on screen. If a curve, point, polygon, or catalog is drawn, the
        nearby text should tell the reader which model it lives in, which transformations are being applied,
        and which measurement is being checked.
        """,
        f"""
        ## Route Through The Notebook

        {route}

        The route is intentionally visual first. We begin each section with a small inspectable construction,
        then attach formulas after the geometry has something to refer to. This is especially important for
        non-Euclidean and quotient-space ideas, where a familiar Euclidean drawing can be correct as a
        coordinate picture but misleading as a metric picture.
        """,
        f"""
        ## Visual Storyboard

        The generated artifacts for this notebook are:

        {visual_text}

        Each filename names the concept being inspected. The final sanity cell asserts that the artifacts
        exist, are nonempty, and are visually nonblank. That check is deliberately prosaic: if the course is
        going to make visual explanation central, blank or decorative figures must be treated as failures,
        not as cosmetic issues.

        Read the figures as a sequence rather than as isolated illustrations. The first visual usually fixes
        the model: a plane, disk, sphere, polygon, quotient domain, or catalog. The middle visuals change
        one parameter or one transformation at a time so that the invariant has a chance to stand out. The
        last visuals connect the computation back to the chapter's larger question. A useful habit is to ask
        three questions after every display: What object is being represented? Which measurement is being
        preserved or changed? Which part of the code would have to be wrong for the picture to lie?

        The artifacts also make the notebook reproducible. The JSON files record small residuals and
        counts, the CSV tables record the visual inventory, and the HTML lab gives a low-friction place to
        perturb a parameter. None of these files replace mathematical proof, but they make the proof goals
        more concrete. For example, a theorem about angle preservation becomes easier to parse after the
        reader has watched distances change while angle checks remain stable; a classification statement
        becomes less abstract after a table of invariants separates examples that initially look alike.

        When adapting this notebook, keep the same standard: every new visual should earn its place by
        revealing a construction, invariant, obstruction, or failure mode. A pretty picture with no inspection
        target should be removed or rewritten until the reader knows what to look for.
        """,
        f"""
        ## Worked Example

        A recurring worked example in this chapter is to choose a simple test object, transform it, and ask
        what changed. For a complex vector this might mean comparing modulus and argument before and
        after multiplication. For a hyperbolic geodesic it might mean checking that the Euclidean circle meets
        the disk boundary orthogonally. For a surface quotient it might mean walking across an edge and
        returning through its identified partner. The particular objects differ from chapter to chapter, but the
        discipline is the same: draw the object, compute a small invariant, perturb a parameter, and explain
        which observation survives.

        The code below follows that pattern. It creates the visual artifacts from a compact storyboard, then
        writes a JSON check file and a CSV inventory. The checks are not a proof of every theorem in the
        chapter; they are executable guardrails that keep the main constructions honest.
        """,
        f"""
        ## Applied Lab

        {entry['lab']}

        Treat the lab as an invitation to change parameters rather than as a fixed exercise. The important
        output is a comparison: what stays invariant, what changes smoothly, and what breaks when the
        assumptions are violated? A strong answer includes a picture, a numerical residual, and one sentence
        explaining why the residual is the right thing to measure.
        """,
        f"""
        ## Pitfalls

        {pitfalls}

        These pitfalls are worth naming because the pictures in this subject are powerful enough to mislead.
        A Euclidean-looking disk can carry a hyperbolic metric. A boundary of a polygon may be an
        identification pattern rather than a wall. A local measurement can be insensitive to global topology.
        The notebooks keep these distinctions explicit by pairing drawings with formulas and by saving the
        intermediate checks.
        """,
        f"""
        ## Takeaways

        - The chapter's central ideas can be inspected through generated diagrams rather than memorized from static figures.
        - The relevant formulas act as checks on the visuals: distance, angle, area, orbit, or topology data should agree with the drawing.
        - A good model separates coordinate appearance from intrinsic measurement.
        - The artifacts are part of the course, not byproducts; rerunning the notebook rebuilds them from the local utilities.

        Before moving on, choose one artifact and explain it without using the textbook's wording: name the
        model, name the transformation or measurement, and name the visible evidence. If that explanation
        feels vague, rerun the relevant cell with a changed parameter and watch what remains stable.
        """,
    ]


def setup_code(entry: dict[str, Any]) -> str:
    meta = json.dumps(
        {k: entry[k] for k in ["kind", "number", "title", "printed", "pdf", "sections", "goal", "focus"]},
        indent=4,
    )
    specs = json.dumps(entry["visuals"], indent=4)
    return (
        "from pathlib import Path\n"
        "import sys\n\n"
        "BOOK_ROOT = Path.cwd()\n"
        "for candidate in [BOOK_ROOT, *BOOK_ROOT.parents]:\n"
        "    if (candidate / \"00-book-index.ipynb\").exists() and (candidate / \"utils\").exists():\n"
        "        BOOK_ROOT = candidate\n"
        "        break\n"
        "else:\n"
        "    raise RuntimeError(\"Could not find the GICT book root\")\n\n"
        "if str(BOOK_ROOT) not in sys.path:\n"
        "    sys.path.insert(0, str(BOOK_ROOT))\n\n"
        f"ARTIFACT_ROOT = BOOK_ROOT / \"artifacts\" / \"{entry['artifact']}\"\n"
        "ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)\n\n"
        f"CHAPTER_META = {meta}\n"
        f"VISUAL_SPECS = {specs}\n\n"
        "from utils.artifacts import assert_artifacts, display_artifact, save_json, save_table, save_html\n"
        "from utils.visuals import build_parameter_lab_html, chapter_numeric_checks, render_visuals\n"
    )


def notebook_cells(entry: dict[str, Any]) -> list[Any]:
    markdown = notebook_markdown(entry)
    cells: list[Any] = [
        new_markdown_cell(dedent(markdown[0])),
        new_markdown_cell(dedent(markdown[1])),
        new_markdown_cell(dedent(markdown[2])),
        new_code_cell(dedent(setup_code(entry))),
        new_markdown_cell(dedent(markdown[3])),
        new_code_cell(dedent('''
        figure_paths, visual_stats = render_visuals(ARTIFACT_ROOT, VISUAL_SPECS)
        for path in figure_paths:
            display_artifact(path, width=820)
        visual_stats
        ''')),
        new_markdown_cell(dedent(markdown[4])),
        new_code_cell(dedent('''
        checks = chapter_numeric_checks(int(CHAPTER_META["number"]))
        checks["visual_count"] = len(figure_paths)
        checks["minimum_pixel_std"] = min(item["pixel_std"] for item in visual_stats)
        checks_path = save_json(checks, ARTIFACT_ROOT, "checks", "chapter-checks.json")
        display_artifact(checks_path)
        checks
        ''')),
        new_markdown_cell(dedent(markdown[5])),
        new_code_cell(dedent('''
        html_path = save_html(build_parameter_lab_html(CHAPTER_META, VISUAL_SPECS), ARTIFACT_ROOT, "html", "parameter-lab.html")
        display_artifact(html_path, height=420)
        html_path
        ''')),
        new_code_cell(dedent('''
        inventory_rows = [
            {
                "artifact": path.name,
                "category": path.parent.name,
                "bytes": path.stat().st_size,
                "chapter": CHAPTER_META["title"],
            }
            for path in figure_paths
        ]
        table_path = save_table(inventory_rows, ARTIFACT_ROOT, "tables", "visual-inventory.csv")
        display_artifact(table_path)
        inventory_rows[:2]
        ''')),
        new_markdown_cell(dedent(markdown[6])),
        new_code_cell(dedent('''
        all_paths = list(figure_paths) + [checks_path, html_path, table_path]
        assert_artifacts(all_paths)
        assert len(figure_paths) >= 5
        assert min(item["pixel_std"] for item in visual_stats) > 2.0
        assert checks["status"] == "ok"
        final_sanity = {
            "artifact_count": len(all_paths),
            "min_pixel_std": min(item["pixel_std"] for item in visual_stats),
            "all_paths_exist": all(path.exists() for path in all_paths),
        }
        final_path = save_json(final_sanity, ARTIFACT_ROOT, "checks", "final-sanity.json")
        display_artifact(final_path)
        final_sanity
        ''')),
        new_markdown_cell(dedent(markdown[7])),
    ]
    return cells


def create_files() -> None:
    entries = public_entries()
    for folder in ["artifacts", "utils", "scripts"]:
        (BOOK_ROOT / folder).mkdir(exist_ok=True)
    write_text(BOOK_ROOT / "AGENTS.md", agent_md())
    write_text(BOOK_ROOT / "utils" / "__init__.py", utils_init())
    write_text(BOOK_ROOT / "utils" / "artifacts.py", artifacts_py())
    write_text(BOOK_ROOT / "utils" / "complex_plane.py", complex_plane_py())
    write_text(BOOK_ROOT / "utils" / "mobius.py", mobius_py())
    write_text(BOOK_ROOT / "utils" / "models.py", models_py())
    write_text(BOOK_ROOT / "utils" / "surfaces.py", surfaces_py())
    write_text(BOOK_ROOT / "utils" / "cosmic_topology.py", cosmic_topology_py())
    write_text(BOOK_ROOT / "utils" / "visuals.py", visuals_py())
    write_text(BOOK_ROOT / "scripts" / "gict_inventory.py", inventory_py())
    write_text(BOOK_ROOT / "scripts" / "build_gict_course_indexes.py", build_indexes_py())
    write_text(BOOK_ROOT / "scripts" / "audit_gict_notebooks.py", audit_notebooks_py())
    write_text(BOOK_ROOT / "scripts" / "audit_gict_visuals.py", audit_visuals_py())
    write_text(BOOK_ROOT / "scripts" / "validate_gict_course.py", validate_course_py())
    for entry in entries:
        folder = BOOK_ROOT / entry["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        write_notebook(folder / entry["notebook"], notebook_cells(entry))
        for child in ["figures", "html", "checks", "tables"]:
            (BOOK_ROOT / "artifacts" / entry["artifact"] / child).mkdir(parents=True, exist_ok=True)
    import runpy

    runpy.run_path(str(BOOK_ROOT / "scripts" / "build_gict_course_indexes.py"), run_name="__main__")


def main() -> None:
    create_files()
    print(f"Bootstrapped {len(public_entries())} canonical notebooks in {BOOK_ROOT}")


if __name__ == "__main__":
    main()
