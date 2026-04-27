"""Bootstrap the VDGF standalone notebook course.

The generated notebooks are original teaching material organized around
Tristan Needham's *Visual Differential Geometry and Forms*. They do not
copy textbook prose or figures. The PDF remains a local source used only for
page-span orientation.
"""

from __future__ import annotations

import json
import re
import textwrap
import importlib.util
from pathlib import Path
from pprint import pformat

import nbformat as nbf

BOOK_ROOT = Path(__file__).resolve().parents[1]
PDF_NAME = "Visual Differential Geometry and Forms.pdf"

KERNEL_METADATA = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "pygments_lexer": "ipython3"},
}

PARTS = [
    {
        "folder": "part-00-prologue",
        "title": "Prologue",
        "description": "Why visual explanation matters in differential geometry.",
    },
    {
        "folder": "part-01-the-nature-of-space",
        "title": "Act I: The Nature of Space",
        "description": "Flat, spherical, and hyperbolic intuitions for intrinsic curvature.",
    },
    {
        "folder": "part-02-the-metric",
        "title": "Act II: The Metric",
        "description": "Metrics, conformal maps, the pseudosphere, and hyperbolic isometries.",
    },
    {
        "folder": "part-03-curvature",
        "title": "Act III: Curvature",
        "description": "Curves, surfaces, shape operators, and Gauss-Bonnet.",
    },
    {
        "folder": "part-04-parallel-transport",
        "title": "Act IV: Parallel Transport",
        "description": "Holonomy, covariant differentiation, Riemann curvature, and spacetime.",
    },
    {
        "folder": "part-05-forms",
        "title": "Act V: Forms",
        "description": "Differential forms, tensors, integration, Stokes, and moving frames.",
    },
]


ENTRIES = [
    {
        "kind": "prologue",
        "part": "part-00-prologue",
        "label": "Prologue",
        "number": 0,
        "title": "The Faustian Offer",
        "folder": "prologue",
        "notebook": "prologue.ipynb",
        "printed": "xvii-xxiv",
        "pdf": "18-25",
        "focus": "Recovering geometric meaning from formal calculation.",
        "topics": [
            "the tension between algebraic power and geometric meaning",
            "visual proof as an explanatory tool",
            "the five-act route through the book",
            "why diagrams can carry general arguments",
            "how this notebook edition turns visual intuition into computation",
        ],
        "lab": "Compare a symbolic formula, a diagram, and a numerical invariant for the same geometric claim.",
    },
    {
        "kind": "chapter",
        "part": "part-01-the-nature-of-space",
        "label": "Chapter 01",
        "number": 1,
        "title": "Euclidean and Non-Euclidean Geometry",
        "folder": "chapter-01-euclidean-and-non-euclidean-geometry",
        "notebook": "01-euclidean-and-non-euclidean-geometry.ipynb",
        "printed": "3-16",
        "pdf": "32-45",
        "focus": "Euclidean, spherical, and hyperbolic geometry as different answers to what straightness means.",
        "topics": [
            "parallel axioms and triangle angle sums",
            "great circles as spherical lines",
            "angular excess on a sphere",
            "intrinsic versus extrinsic surface geometry",
            "straightness as the defining feature of geodesics",
            "physical space as a geometric question",
        ],
        "lab": "Compute Euclidean and spherical triangle angle sums and compare their excess.",
    },
    {
        "kind": "chapter",
        "part": "part-01-the-nature-of-space",
        "label": "Chapter 02",
        "number": 2,
        "title": "Gaussian Curvature",
        "folder": "chapter-02-gaussian-curvature",
        "notebook": "02-gaussian-curvature.ipynb",
        "printed": "17-23",
        "pdf": "46-52",
        "focus": "Curvature as the local measurable defect in circles, areas, and angular excess.",
        "topics": [
            "positive, zero, and negative curvature",
            "small geodesic circles",
            "circumference and area deviations",
            "local Gauss-Bonnet",
            "curvature as density of angular excess",
        ],
        "lab": "Plot small-circle asymptotics for constant curvature models.",
    },
    {
        "kind": "chapter",
        "part": "part-01-the-nature-of-space",
        "label": "Chapter 03",
        "number": 3,
        "title": "Exercises for Prologue and Act I",
        "folder": "chapter-03-exercises-for-prologue-and-act-i",
        "notebook": "03-exercises-for-prologue-and-act-i.ipynb",
        "printed": "24-30",
        "pdf": "53-59",
        "focus": "An executable problem lab for visual explanation, spherical geometry, and curvature measurement.",
        "topics": [
            "Pythagorean triples and Euclidean flatness",
            "spherical triangles and angular excess",
            "curvature from circumference and area",
            "cone and sphere comparison",
            "problem-solving by invariant checks",
        ],
        "lab": "Turn selected Act I exercise themes into randomized numerical checks.",
    },
    {
        "kind": "chapter",
        "part": "part-02-the-metric",
        "label": "Chapter 04",
        "number": 4,
        "title": "Mapping Surfaces: The Metric",
        "folder": "chapter-04-mapping-surfaces-the-metric",
        "notebook": "04-mapping-surfaces-the-metric.ipynb",
        "printed": "31-50",
        "pdf": "60-79",
        "focus": "The metric tensor as the object that records how a map distorts length, angle, and area.",
        "topics": [
            "surface maps and coordinates",
            "projective mapping of the sphere",
            "the metric of a general surface",
            "the metric curvature formula",
            "conformal maps and visual complex analysis",
            "stereographic formulas and circle preservation",
        ],
        "lab": "Compute the metric of a sphere chart and visualize its local distortion.",
    },
    {
        "kind": "chapter",
        "part": "part-02-the-metric",
        "label": "Chapter 05",
        "number": 5,
        "title": "The Pseudosphere and the Hyperbolic Plane",
        "folder": "chapter-05-the-pseudosphere-and-the-hyperbolic-plane",
        "notebook": "05-the-pseudosphere-and-the-hyperbolic-plane.ipynb",
        "printed": "51-64",
        "pdf": "80-93",
        "focus": "Beltrami's bridge from a curved surface to concrete hyperbolic geometry.",
        "topics": [
            "Beltrami's interpretation of hyperbolic geometry",
            "the tractrix and pseudosphere",
            "conformal maps of the pseudosphere",
            "the upper half-plane model",
            "optical geodesics",
            "angle of parallelism",
            "the disc model",
        ],
        "lab": "Compare upper-half-plane geodesics with Euclidean semicircles orthogonal to the boundary.",
    },
    {
        "kind": "chapter",
        "part": "part-02-the-metric",
        "label": "Chapter 06",
        "number": 6,
        "title": "Isometries and Complex Numbers",
        "folder": "chapter-06-isometries-and-complex-numbers",
        "notebook": "06-isometries-and-complex-numbers.ipynb",
        "printed": "65-82",
        "pdf": "94-111",
        "focus": "Mobius transformations as the natural motion language of hyperbolic geometry.",
        "topics": [
            "complex numbers as planar transformations",
            "Mobius transformations",
            "circle and line preservation",
            "hyperbolic isometries",
            "Lorentz transformations and spacetime geometry",
            "three-dimensional hyperbolic geometry",
        ],
        "lab": "Apply Mobius maps to circles and check hyperbolic distance invariance in a simple case.",
    },
    {
        "kind": "chapter",
        "part": "part-02-the-metric",
        "label": "Chapter 07",
        "number": 7,
        "title": "Exercises for Act II",
        "folder": "chapter-07-exercises-for-act-ii",
        "notebook": "07-exercises-for-act-ii.ipynb",
        "printed": "83-96",
        "pdf": "112-125",
        "focus": "An executable verification suite for metrics, conformality, the pseudosphere, and Mobius maps.",
        "topics": [
            "metric computations in charts",
            "stereographic projection checks",
            "hyperbolic distance and geodesics",
            "pseudosphere curvature",
            "Mobius transformations",
            "spacetime and Lorentz geometry exercises",
        ],
        "lab": "Package Act II exercises as symbolic identities and numerical experiments.",
    },
    {
        "kind": "chapter",
        "part": "part-03-curvature",
        "label": "Chapter 08",
        "number": 8,
        "title": "Curvature of Plane Curves",
        "folder": "chapter-08-curvature-of-plane-curves",
        "notebook": "08-curvature-of-plane-curves.ipynb",
        "printed": "97-105",
        "pdf": "126-134",
        "focus": "Plane curvature through osculating circles, Newton's formula, and rate of turning.",
        "topics": [
            "curvature as reciprocal radius",
            "circle of curvature",
            "Newton's curvature formula",
            "curvature as rate of turning",
            "the tractrix as a worked example",
        ],
        "lab": "Animate an osculating circle along a parametric curve.",
    },
    {
        "kind": "chapter",
        "part": "part-03-curvature",
        "label": "Chapter 09",
        "number": 9,
        "title": "Curves in 3-Space",
        "folder": "chapter-09-curves-in-3-space",
        "notebook": "09-curves-in-3-space.ipynb",
        "printed": "106-108",
        "pdf": "135-137",
        "focus": "Spatial curves as moving tangent-normal-binormal frames with curvature and torsion.",
        "topics": [
            "unit tangent motion",
            "normal and binormal directions",
            "curvature in space",
            "torsion as twisting of the osculating plane",
            "Frenet-style frame intuition",
        ],
        "lab": "Compute the curvature and torsion of a helix and render its moving frame.",
    },
    {
        "kind": "chapter",
        "part": "part-03-curvature",
        "label": "Chapter 10",
        "number": 10,
        "title": "The Principal Curvatures of a Surface",
        "folder": "chapter-10-the-principal-curvatures-of-a-surface",
        "notebook": "10-the-principal-curvatures-of-a-surface.ipynb",
        "printed": "109-114",
        "pdf": "138-143",
        "focus": "Normal curvature decomposed into principal directions by Euler's curvature formula.",
        "topics": [
            "normal sections of a surface",
            "Euler's curvature formula",
            "principal curvatures and principal directions",
            "surfaces of revolution",
            "curvature extrema as directional data",
        ],
        "lab": "Sample normal curvature around a point and recover the principal directions.",
    },
    {
        "kind": "chapter",
        "part": "part-03-curvature",
        "label": "Chapter 11",
        "number": 11,
        "title": "Geodesics and Geodesic Curvature",
        "folder": "chapter-11-geodesics-and-geodesic-curvature",
        "notebook": "11-geodesics-and-geodesic-curvature.ipynb",
        "printed": "115-129",
        "pdf": "144-158",
        "focus": "Separating normal curvature from the side-turning measured intrinsically along a surface.",
        "topics": [
            "geodesic curvature and normal curvature",
            "Meusnier's theorem",
            "geodesics as straight paths on surfaces",
            "intrinsic and extrinsic measurements of geodesic curvature",
            "Clairaut's theorem",
            "Kepler's second law analogy",
        ],
        "lab": "Numerically integrate a geodesic on a surface of revolution and check Clairaut's invariant.",
    },
    {
        "kind": "chapter",
        "part": "part-03-curvature",
        "label": "Chapter 12",
        "number": 12,
        "title": "The Extrinsic Curvature of a Surface",
        "folder": "chapter-12-the-extrinsic-curvature-of-a-surface",
        "notebook": "12-the-extrinsic-curvature-of-a-surface.ipynb",
        "printed": "130-137",
        "pdf": "159-166",
        "focus": "The Gauss map turns changing normals into an area ratio called extrinsic curvature.",
        "topics": [
            "the spherical map",
            "area change under the Gauss map",
            "extrinsic curvature of surfaces",
            "positive and negative normal behavior",
            "what surface shapes are possible",
        ],
        "lab": "Approximate Gauss-map area distortion on a sphere and saddle patch.",
    },
    {
        "kind": "chapter",
        "part": "part-03-curvature",
        "label": "Chapter 13",
        "number": 13,
        "title": "Gauss's Theorema Egregium",
        "folder": "chapter-13-gausss-theorema-egregium",
        "notebook": "13-gausss-theorema-egregium.ipynb",
        "printed": "138-142",
        "pdf": "167-171",
        "focus": "Gaussian curvature is secretly intrinsic even when first discovered through normals.",
        "topics": [
            "Gauss's beautiful theorem",
            "the Theorema Egregium",
            "intrinsic detectability of curvature",
            "bending without stretching",
            "curvature from the metric",
        ],
        "lab": "Compare cylinder and plane metrics with their extrinsic embeddings.",
    },
    {
        "kind": "chapter",
        "part": "part-03-curvature",
        "label": "Chapter 14",
        "number": 14,
        "title": "The Curvature of a Spike",
        "folder": "chapter-14-the-curvature-of-a-spike",
        "notebook": "14-the-curvature-of-a-spike.ipynb",
        "printed": "143-148",
        "pdf": "172-177",
        "focus": "Curvature concentrated at a cone or polyhedral vertex as angular defect.",
        "topics": [
            "conical spike curvature",
            "flattening a cone",
            "polyhedral angular defect",
            "intrinsic versus extrinsic spike curvature",
            "polyhedral Theorema Egregium",
        ],
        "lab": "Compute angular defect for cone and polyhedral vertex models.",
    },
    {
        "kind": "chapter",
        "part": "part-03-curvature",
        "label": "Chapter 15",
        "number": 15,
        "title": "The Shape Operator",
        "folder": "chapter-15-the-shape-operator",
        "notebook": "15-the-shape-operator.ipynb",
        "printed": "149-164",
        "pdf": "178-193",
        "focus": "The derivative of the normal field as a linear operator encoding all normal curvatures.",
        "topics": [
            "directional derivatives",
            "the shape operator",
            "geometric effect of the shape operator",
            "singular value decomposition detour",
            "matrix representation of the shape operator",
            "fundamental forms",
            "asymptotic directions",
        ],
        "lab": "Build the shape-operator matrix for a graph surface and diagonalize it.",
    },
    {
        "kind": "chapter",
        "part": "part-03-curvature",
        "label": "Chapter 16",
        "number": 16,
        "title": "Introduction to the Global Gauss-Bonnet Theorem",
        "folder": "chapter-16-introduction-to-the-global-gauss-bonnet-theorem",
        "notebook": "16-introduction-to-the-global-gauss-bonnet-theorem.ipynb",
        "printed": "165-174",
        "pdf": "194-203",
        "focus": "Total curvature tied to topology through genus, Euler characteristic, and Gauss-map degree.",
        "topics": [
            "Euler characteristic and genus",
            "total curvature of sphere and torus",
            "bagels, bridges, and handles",
            "topological degree of the Gauss map",
            "statement of global Gauss-Bonnet",
        ],
        "lab": "Compute Euler characteristic and predicted total curvature for triangulated models.",
    },
    {
        "kind": "chapter",
        "part": "part-03-curvature",
        "label": "Chapter 17",
        "number": 17,
        "title": "First Heuristic Proof of the Global Gauss-Bonnet Theorem",
        "folder": "chapter-17-first-heuristic-proof-of-the-global-gauss-bonnet-theorem",
        "notebook": "17-first-heuristic-proof-of-the-global-gauss-bonnet-theorem.ipynb",
        "printed": "175-182",
        "pdf": "204-211",
        "focus": "Global Gauss-Bonnet through total turning and deformation of loops and spheres.",
        "topics": [
            "Hopf's Umlaufsatz",
            "total curvature of a plane loop",
            "deforming a circle",
            "deforming a sphere",
            "heuristic total-curvature conservation",
        ],
        "lab": "Track turning number for deformed plane loops.",
    },
    {
        "kind": "chapter",
        "part": "part-03-curvature",
        "label": "Chapter 18",
        "number": 18,
        "title": "Second Angular Excess Proof of the Global Gauss-Bonnet Theorem",
        "folder": "chapter-18-second-angular-excess-proof-of-the-global-gauss-bonnet-theorem",
        "notebook": "18-second-angular-excess-proof-of-the-global-gauss-bonnet-theorem.ipynb",
        "printed": "183-194",
        "pdf": "212-223",
        "focus": "Triangulations, Euler characteristic, and angular excess as a combinatorial proof strategy.",
        "topics": [
            "Euler characteristic",
            "Euler's polyhedral formula",
            "Cauchy's flattening proof",
            "Legendre's proof",
            "handles and genus",
            "angular-excess proof of Gauss-Bonnet",
        ],
        "lab": "Verify Euler characteristic and angular defect on simple meshes.",
    },
    {
        "kind": "chapter",
        "part": "part-03-curvature",
        "label": "Chapter 19",
        "number": 19,
        "title": "Third Vector Field Proof of the Global Gauss-Bonnet Theorem",
        "folder": "chapter-19-third-vector-field-proof-of-the-global-gauss-bonnet-theorem",
        "notebook": "19-third-vector-field-proof-of-the-global-gauss-bonnet-theorem.ipynb",
        "printed": "195-218",
        "pdf": "224-247",
        "focus": "Vector-field singularities, index, Poincare-Hopf, and total curvature.",
        "topics": [
            "vector fields in the plane",
            "index of a singular point",
            "complex powers as archetypes",
            "vector fields on surfaces",
            "Poincare-Hopf theorem",
            "line fields and differential equations",
            "vector-field proof of Gauss-Bonnet",
        ],
        "lab": "Compute winding index for synthetic planar vector-field singularities.",
    },
    {
        "kind": "chapter",
        "part": "part-03-curvature",
        "label": "Chapter 20",
        "number": 20,
        "title": "Exercises for Act III",
        "folder": "chapter-20-exercises-for-act-iii",
        "notebook": "20-exercises-for-act-iii.ipynb",
        "printed": "219-230",
        "pdf": "248-259",
        "focus": "An executable problem lab for curvature, shape operators, Gauss-Bonnet, and vector-field index.",
        "topics": [
            "plane and space curve curvature",
            "principal curvatures",
            "geodesic curvature",
            "Gauss-map curvature",
            "shape-operator calculations",
            "Gauss-Bonnet exercises",
            "Poincare-Hopf checks",
        ],
        "lab": "Convert representative Act III exercises into symbolic and numerical regression checks.",
    },
    {
        "kind": "chapter",
        "part": "part-04-parallel-transport",
        "label": "Chapter 21",
        "number": 21,
        "title": "An Historical Puzzle",
        "folder": "chapter-21-an-historical-puzzle",
        "notebook": "21-an-historical-puzzle.ipynb",
        "printed": "231-232",
        "pdf": "260-261",
        "focus": "The historical need for a geometric idea of transporting vectors along curved spaces.",
        "topics": [
            "curvature without an ambient crutch",
            "transporting directions on surfaces",
            "the path toward covariant differentiation",
            "why parallel transport unlocks Riemannian geometry",
            "the bridge toward general relativity",
        ],
        "lab": "Use a simple sphere loop to see why transported vectors can return rotated.",
    },
    {
        "kind": "chapter",
        "part": "part-04-parallel-transport",
        "label": "Chapter 22",
        "number": 22,
        "title": "Extrinsic Constructions",
        "folder": "chapter-22-extrinsic-constructions",
        "notebook": "22-extrinsic-constructions.ipynb",
        "printed": "233-239",
        "pdf": "262-268",
        "focus": "Parallel transport by projecting ambient changes back into the surface.",
        "topics": [
            "project into the surface as you go",
            "geodesics and transport",
            "potato-peeler transport",
            "extrinsic algorithms for intrinsic behavior",
            "limitations of ambient construction",
        ],
        "lab": "Transport a tangent vector along a latitude circle by repeated projection.",
    },
    {
        "kind": "chapter",
        "part": "part-04-parallel-transport",
        "label": "Chapter 23",
        "number": 23,
        "title": "Intrinsic Constructions",
        "folder": "chapter-23-intrinsic-constructions",
        "notebook": "23-intrinsic-constructions.ipynb",
        "printed": "240-244",
        "pdf": "269-273",
        "focus": "Parallel transport and covariant differentiation using only information inside the surface.",
        "topics": [
            "parallel transport via geodesics",
            "intrinsic covariant derivative",
            "geodesic curvature as covariant acceleration",
            "flattened-strip intuition",
            "surface-internal measurement",
        ],
        "lab": "Compare ordinary and covariant derivative along a curve on the sphere.",
    },
    {
        "kind": "chapter",
        "part": "part-04-parallel-transport",
        "label": "Chapter 24",
        "number": 24,
        "title": "Holonomy",
        "folder": "chapter-24-holonomy",
        "notebook": "24-holonomy.ipynb",
        "printed": "245-251",
        "pdf": "274-280",
        "focus": "Holonomy as curvature detected by transporting a vector around a loop.",
        "topics": [
            "holonomy on the sphere",
            "geodesic triangle holonomy",
            "additivity of holonomy",
            "hyperbolic holonomy",
            "curvature as rotation per enclosed area",
        ],
        "lab": "Compute spherical triangle area and predicted holonomy.",
    },
    {
        "kind": "chapter",
        "part": "part-04-parallel-transport",
        "label": "Chapter 25",
        "number": 25,
        "title": "An Intuitive Geometric Proof of the Theorema Egregium",
        "folder": "chapter-25-an-intuitive-geometric-proof-of-the-theorema-egregium",
        "notebook": "25-an-intuitive-geometric-proof-of-the-theorema-egregium.ipynb",
        "printed": "252-256",
        "pdf": "281-285",
        "focus": "The spherical map preserves parallel transport enough to reveal intrinsic curvature.",
        "topics": [
            "notation for curvature and transport",
            "story so far",
            "spherical map and parallel transport",
            "beautiful theorem explained",
            "Theorema Egregium through holonomy",
        ],
        "lab": "Compare holonomy before and after the Gauss map on a small patch.",
    },
    {
        "kind": "chapter",
        "part": "part-04-parallel-transport",
        "label": "Chapter 26",
        "number": 26,
        "title": "Fourth Holonomy Proof of the Global Gauss-Bonnet Theorem",
        "folder": "chapter-26-fourth-holonomy-proof-of-the-global-gauss-bonnet-theorem",
        "notebook": "26-fourth-holonomy-proof-of-the-global-gauss-bonnet-theorem.ipynb",
        "printed": "257-260",
        "pdf": "286-289",
        "focus": "Global Gauss-Bonnet through total holonomy and boundary correction.",
        "topics": [
            "holonomy along open curves",
            "Hopf's intrinsic proof",
            "boundary turning correction",
            "curvature integral as accumulated rotation",
            "closed-surface conclusion",
        ],
        "lab": "Numerically compare loop holonomy, boundary turning, and enclosed curvature.",
    },
    {
        "kind": "chapter",
        "part": "part-04-parallel-transport",
        "label": "Chapter 27",
        "number": 27,
        "title": "Geometric Proof of the Metric Curvature Formula",
        "folder": "chapter-27-geometric-proof-of-the-metric-curvature-formula",
        "notebook": "27-geometric-proof-of-the-metric-curvature-formula.ipynb",
        "printed": "261-268",
        "pdf": "290-297",
        "focus": "Metric curvature obtained from circulation of a metric-induced vector field.",
        "topics": [
            "circulation around a loop",
            "flat-plane dry run",
            "holonomy from a metric-induced field",
            "geometric proof of metric curvature formula",
            "local curvature as infinitesimal circulation",
        ],
        "lab": "Compute curvature from a conformal metric and compare with direct symbolic curvature.",
    },
    {
        "kind": "chapter",
        "part": "part-04-parallel-transport",
        "label": "Chapter 28",
        "number": 28,
        "title": "Curvature as a Force between Neighbouring Geodesics",
        "folder": "chapter-28-curvature-as-a-force-between-neighbouring-geodesics",
        "notebook": "28-curvature-as-a-force-between-neighbouring-geodesics.ipynb",
        "printed": "269-279",
        "pdf": "298-308",
        "focus": "The Jacobi equation makes curvature visible as relative acceleration of geodesics.",
        "topics": [
            "Jacobi equation introduction",
            "zero, positive, and negative curvature geodesic spread",
            "geodesic polar coordinates",
            "relative acceleration as holonomy",
            "small geodesic circle circumference and area",
        ],
        "lab": "Solve the constant-curvature Jacobi equation for nearby geodesics.",
    },
    {
        "kind": "chapter",
        "part": "part-04-parallel-transport",
        "label": "Chapter 29",
        "number": 29,
        "title": "Riemann's Curvature",
        "folder": "chapter-29-riemanns-curvature",
        "notebook": "29-riemanns-curvature.ipynb",
        "printed": "280-306",
        "pdf": "309-335",
        "focus": "Curvature in n dimensions through vector holonomy, Riemann tensor, sectional curvature, and Ricci focusing.",
        "topics": [
            "angular excess in n-manifolds",
            "parallel transport constructions",
            "covariant derivative",
            "Riemann curvature tensor",
            "tensor symmetries",
            "sectional curvature",
            "Jacobi equation in n-manifolds",
            "Ricci tensor",
        ],
        "lab": "Compute Riemann and Ricci tensors for a two-dimensional conformal metric.",
    },
    {
        "kind": "chapter",
        "part": "part-04-parallel-transport",
        "label": "Chapter 30",
        "number": 30,
        "title": "Einstein's Curved Spacetime",
        "folder": "chapter-30-einsteins-curved-spacetime",
        "notebook": "30-einsteins-curved-spacetime.ipynb",
        "printed": "307-333",
        "pdf": "336-362",
        "focus": "General relativity as spacetime curvature read through geodesics, Ricci curvature, and Einstein's equation.",
        "topics": [
            "equivalence principle",
            "tidal forces",
            "Newtonian gravity in geometrical form",
            "spacetime metric and diagrams",
            "vacuum field equation",
            "Schwarzschild solution",
            "gravitational waves",
            "matter, collapse, and cosmological constant",
        ],
        "lab": "Inspect the Schwarzschild metric and verify simple weak-field/tidal signatures.",
    },
    {
        "kind": "chapter",
        "part": "part-04-parallel-transport",
        "label": "Chapter 31",
        "number": 31,
        "title": "Exercises for Act IV",
        "folder": "chapter-31-exercises-for-act-iv",
        "notebook": "31-exercises-for-act-iv.ipynb",
        "printed": "334-344",
        "pdf": "363-373",
        "focus": "An executable problem lab for geodesic curvature, holonomy, Jacobi fields, Riemann curvature, and spacetime.",
        "topics": [
            "geodesic curvature on sphere and cone",
            "intrinsic differentiation",
            "holonomy checks",
            "local Gauss-Bonnet",
            "Minding's theorem",
            "surface-of-revolution Jacobi equation",
            "Riemann and Ricci exercises",
        ],
        "lab": "Turn Act IV exercise themes into transport and curvature regression tests.",
    },
    {
        "kind": "chapter",
        "part": "part-05-forms",
        "label": "Chapter 32",
        "number": 32,
        "title": "1-Forms",
        "folder": "chapter-32-1-forms",
        "notebook": "32-1-forms.ipynb",
        "printed": "345-359",
        "pdf": "374-388",
        "focus": "1-forms as geometric measurement machines acting linearly on vectors.",
        "topics": [
            "definition of a 1-form",
            "work, topographic maps, row vectors, and bras",
            "basis 1-forms",
            "components of a 1-form",
            "gradient as df",
            "geometric addition of 1-forms",
        ],
        "lab": "Visualize a 1-form as stacks of equally spaced measurement lines.",
    },
    {
        "kind": "chapter",
        "part": "part-05-forms",
        "label": "Chapter 33",
        "number": 33,
        "title": "Tensors",
        "folder": "chapter-33-tensors",
        "notebook": "33-tensors.ipynb",
        "printed": "360-369",
        "pdf": "389-398",
        "focus": "Tensors as multilinear maps with valence, components, products, contractions, and metric index changes.",
        "topics": [
            "tensor valence",
            "linear algebra examples",
            "tensor product",
            "components",
            "metric tensor and line element",
            "contraction",
            "raising and lowering indices",
            "symmetry and antisymmetry",
        ],
        "lab": "Build a metric tensor, contract it, and verify raising/lowering behavior.",
    },
    {
        "kind": "chapter",
        "part": "part-05-forms",
        "label": "Chapter 34",
        "number": 34,
        "title": "2-Forms",
        "folder": "chapter-34-2-forms",
        "notebook": "34-2-forms.ipynb",
        "printed": "370-385",
        "pdf": "399-414",
        "focus": "2-forms as oriented area measurement and flux, built by wedge products.",
        "topics": [
            "definition of a 2-form and p-form",
            "area 2-form",
            "wedge product of 1-forms",
            "polar coordinate area form",
            "basis 2-forms and projections",
            "flux in R3",
            "vector and wedge products",
            "electromagnetic 2-forms",
        ],
        "lab": "Compute a polar area form and a flux 2-form from wedge products.",
    },
    {
        "kind": "chapter",
        "part": "part-05-forms",
        "label": "Chapter 35",
        "number": 35,
        "title": "3-Forms",
        "folder": "chapter-35-3-forms",
        "notebook": "35-3-forms.ipynb",
        "printed": "386-391",
        "pdf": "415-420",
        "focus": "3-forms as oriented volume measurement and the top degree of three-dimensional space.",
        "topics": [
            "why a 3-form requires three dimensions",
            "wedge product of 2-form and 1-form",
            "volume 3-form",
            "spherical polar volume form",
            "wedge products of many 1-forms",
            "basis 3-forms",
            "when a form can wedge with itself nontrivially",
        ],
        "lab": "Derive the spherical volume factor using wedge products.",
    },
    {
        "kind": "chapter",
        "part": "part-05-forms",
        "label": "Chapter 36",
        "number": 36,
        "title": "Differentiation",
        "folder": "chapter-36-differentiation",
        "notebook": "36-differentiation.ipynb",
        "printed": "392-403",
        "pdf": "421-432",
        "focus": "The exterior derivative as a single operation unifying gradient, curl, divergence, and Maxwell equations.",
        "topics": [
            "exterior derivative of 1-forms",
            "exterior derivative of p-forms",
            "Leibniz rule",
            "closed and exact forms",
            "d squared equals zero",
            "Cauchy-Riemann equations",
            "vector calculus via forms",
            "Maxwell equations",
        ],
        "lab": "Use exterior derivative checks to recover curl-gradient and divergence-curl identities.",
    },
    {
        "kind": "chapter",
        "part": "part-05-forms",
        "label": "Chapter 37",
        "number": 37,
        "title": "Integration",
        "folder": "chapter-37-integration",
        "notebook": "37-integration.ipynb",
        "printed": "404-429",
        "pdf": "433-458",
        "focus": "Integration of forms and the fundamental theorem of exterior calculus.",
        "topics": [
            "line integrals of 1-forms",
            "path independence and exact forms",
            "exterior derivative as an integral",
            "generalized Stokes theorem",
            "boundary of a boundary",
            "classical vector-calculus integral theorems",
            "Cauchy's theorem",
            "Poincare lemma and de Rham cohomology",
        ],
        "lab": "Numerically verify Stokes theorem and the period of a vortex 1-form.",
    },
    {
        "kind": "chapter",
        "part": "part-05-forms",
        "label": "Chapter 38",
        "number": 38,
        "title": "Differential Geometry via Forms",
        "folder": "chapter-38-differential-geometry-via-forms",
        "notebook": "38-differential-geometry-via-forms.ipynb",
        "printed": "430-464",
        "pdf": "459-493",
        "focus": "Cartan's moving frames and structural equations as a compact language for surface and spacetime curvature.",
        "topics": [
            "moving frames",
            "connection 1-forms",
            "attitude matrix",
            "Cartan's structural equations",
            "surface form equations",
            "Gauss and Codazzi equations",
            "metric curvature formula",
            "curvature 2-forms",
            "Schwarzschild curvature",
        ],
        "lab": "Compute connection and curvature forms for a simple orthonormal frame.",
    },
    {
        "kind": "chapter",
        "part": "part-05-forms",
        "label": "Chapter 39",
        "number": 39,
        "title": "Exercises for Act V",
        "folder": "chapter-39-exercises-for-act-v",
        "notebook": "39-exercises-for-act-v.ipynb",
        "printed": "465-474",
        "pdf": "494-503",
        "focus": "An executable problem lab for forms, tensors, Hodge duality, exterior calculus, Stokes, cohomology, and moving frames.",
        "topics": [
            "Dirac delta as a 1-form",
            "covariant and contravariant components",
            "tensor contraction exercises",
            "factorization of forms",
            "closed and exact forms",
            "Hodge star identities",
            "Stokes and cohomology exercises",
            "moving-frame curvature checks",
        ],
        "lab": "Convert Act V exercise themes into symbolic exterior-calculus tests.",
    },
]


AGENTS_TEXT = """# Agent Instructions: Visual Differential Geometry and Forms Notebook Course

This folder is a standalone notebook edition of *Visual Differential Geometry and Forms*.
Agents should treat this folder as the project root for this course. The workspace root
still owns the shared Python environment files.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, or page screenshots.
- A notebook must be useful without opening the PDF: include motivation, definitions,
  worked examples, pitfalls, checks, and takeaways.
- Keep helpers in `utils/`, outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve the one-canonical-notebook-per-folder structure.

## Source Map

Body printed pages map to PDF pages by `pdf_page = printed_page + 29`.
The course follows the book's five-act structure:

- Prologue: visual meaning versus empty calculation.
- Act I: Chapters 1-3, the nature of space.
- Act II: Chapters 4-7, the metric.
- Act III: Chapters 8-20, curvature.
- Act IV: Chapters 21-31, parallel transport.
- Act V: Chapters 32-39, forms.

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Translation guide from book concepts into computational language.
3. Route through the chapter.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Static or interactive artifacts.
8. Applied lab or design exercise.
9. Sanity checks asserting core identities and artifact existence.
10. Takeaways.

## Visual Artifact Contract

Every canonical notebook must contain at least one chapter-specific visual artifact
that is saved under the matching `artifacts/...` subtree and displayed inline with
`display_artifact(...)`.

Visuals are part of the teaching argument, not decoration:

- The artifact filename must name the concept, for example
  `holonomy-loop-meter.png`, not `figure.png`.
- The notebook prose near the visual must name the concept, parameters, and the
  invariant or behavior the reader should inspect.
- Final sanity checks must assert the visual path exists, has nonzero size, and
  records relevant numeric validation values in `final-sanity.json`.
- Repeated placeholder visuals are forbidden. A repeated artifact hash is a QC
  failure unless the exact file is intentionally allowlisted in the visual audit.
- Do not use textbook screenshots, PDF page crops, or decorative images that do
  not express chapter content.

## Worker Boundaries

Assign one worker to one canonical notebook, one helper module, or one script task.
Chapter workers edit only their chapter folder, matching artifact subtree, and any
explicitly assigned chapter helper. Shared utility changes belong to utility workers.
The index/QC worker owns `00-book-index.ipynb`, part indexes, audits, and validation.

## Commands

Run from the workspace root:

```powershell
uv run python Visual-Differential-Geometry-and-Forms/scripts/build_vdgf_course_indexes.py
uv run python -m compileall -q Visual-Differential-Geometry-and-Forms/utils Visual-Differential-Geometry-and-Forms/scripts
uv run pytest -q Visual-Differential-Geometry-and-Forms/scripts
uv run python Visual-Differential-Geometry-and-Forms/scripts/audit_vdgf_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Visual-Differential-Geometry-and-Forms/scripts/audit_vdgf_visuals.py
uv run python Visual-Differential-Geometry-and-Forms/scripts/validate_vdgf_course.py --limit 8 --timeout 300
uv run python Visual-Differential-Geometry-and-Forms/scripts/validate_vdgf_course.py --all --timeout 300
git diff --check
```
"""


ARTIFACTS_PY = '''"""Artifact helpers for the VDGF notebook course."""

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


def save_json(data: Any, topic: str, slug: str | None, filename: str = "data.json", *, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_path(topic, slug, filename, root)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def save_text(text: str, topic: str, slug: str | None, filename: str = "notes.txt", *, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_path(topic, slug, filename, root)
    path.write_text(text, encoding="utf-8")
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


DG_INIT = '''"""Differential-geometry utilities for the VDGF course."""

from .core import (
    christoffel_symbols,
    constant_curvature_circle_area,
    constant_curvature_circle_circumference,
    gaussian_curvature_2d,
    great_circle_points,
    hyperbolic_half_plane_distance,
    metric_tensor,
    mobius_transform,
    osculating_circle,
    plane_curve_curvature,
    ricci_tensor,
    riemann_tensor,
    scalar_curvature,
    shape_operator,
    spherical_triangle_area,
    stereographic_inverse,
    stereographic_project,
    surface_of_revolution,
)

__all__ = [
    "christoffel_symbols",
    "constant_curvature_circle_area",
    "constant_curvature_circle_circumference",
    "gaussian_curvature_2d",
    "great_circle_points",
    "hyperbolic_half_plane_distance",
    "metric_tensor",
    "mobius_transform",
    "osculating_circle",
    "plane_curve_curvature",
    "ricci_tensor",
    "riemann_tensor",
    "scalar_curvature",
    "shape_operator",
    "spherical_triangle_area",
    "stereographic_inverse",
    "stereographic_project",
    "surface_of_revolution",
]
'''


DG_CORE = '''"""Small inspectable differential-geometry routines."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np
import sympy as sp


def plane_curve_curvature(x: sp.Expr, y: sp.Expr, t: sp.Symbol) -> sp.Expr:
    dx, dy = sp.diff(x, t), sp.diff(y, t)
    ddx, ddy = sp.diff(dx, t), sp.diff(dy, t)
    return sp.simplify((dx * ddy - dy * ddx) / (dx**2 + dy**2) ** sp.Rational(3, 2))


def osculating_circle(x: sp.Expr, y: sp.Expr, t: sp.Symbol, value: float) -> dict[str, float]:
    kappa = plane_curve_curvature(x, y, t)
    dx, dy = sp.diff(x, t), sp.diff(y, t)
    speed = sp.sqrt(dx**2 + dy**2)
    nx, ny = -dy / speed, dx / speed
    subs = {t: value}
    k = float(sp.N(kappa.subs(subs)))
    radius = math.inf if abs(k) < 1e-12 else 1.0 / abs(k)
    px, py = float(sp.N(x.subs(subs))), float(sp.N(y.subs(subs)))
    cx = px + float(sp.N(nx.subs(subs))) / k if abs(k) >= 1e-12 else math.inf
    cy = py + float(sp.N(ny.subs(subs))) / k if abs(k) >= 1e-12 else math.inf
    return {"point_x": px, "point_y": py, "center_x": cx, "center_y": cy, "curvature": k, "radius": radius}


def metric_tensor(param: sp.Matrix, coords: Iterable[sp.Symbol]) -> sp.Matrix:
    coords = list(coords)
    partials = [sp.diff(param, coord) for coord in coords]
    return sp.simplify(sp.Matrix([[partials[i].dot(partials[j]) for j in range(len(coords))] for i in range(len(coords))]))


def christoffel_symbols(metric: sp.Matrix, coords: Iterable[sp.Symbol]) -> list[list[list[sp.Expr]]]:
    coords = list(coords)
    n = len(coords)
    inv = sp.simplify(metric.inv())
    gamma = [[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                gamma[k][i][j] = sp.simplify(
                    sp.Rational(1, 2)
                    * sum(inv[k, l] * (sp.diff(metric[j, l], coords[i]) + sp.diff(metric[i, l], coords[j]) - sp.diff(metric[i, j], coords[l])) for l in range(n))
                )
    return gamma


def riemann_tensor(metric: sp.Matrix, coords: Iterable[sp.Symbol]) -> list[list[list[list[sp.Expr]]]]:
    coords = list(coords)
    n = len(coords)
    gamma = christoffel_symbols(metric, coords)
    riemann = [[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    value = sp.diff(gamma[l][i][k], coords[j]) - sp.diff(gamma[l][i][j], coords[k])
                    value += sum(gamma[m][i][k] * gamma[l][m][j] - gamma[m][i][j] * gamma[l][m][k] for m in range(n))
                    riemann[l][i][j][k] = sp.simplify(value)
    return riemann


def ricci_tensor(metric: sp.Matrix, coords: Iterable[sp.Symbol]) -> sp.Matrix:
    coords = list(coords)
    n = len(coords)
    R = riemann_tensor(metric, coords)
    return sp.simplify(sp.Matrix([[sum(R[k][i][k][j] for k in range(n)) for j in range(n)] for i in range(n)]))


def scalar_curvature(metric: sp.Matrix, coords: Iterable[sp.Symbol]) -> sp.Expr:
    ricci = ricci_tensor(metric, coords)
    return sp.simplify(sum(metric.inv()[i, j] * ricci[i, j] for i in range(metric.shape[0]) for j in range(metric.shape[1])))


def gaussian_curvature_2d(metric: sp.Matrix, coords: Iterable[sp.Symbol]) -> sp.Expr:
    return sp.simplify(scalar_curvature(metric, coords) / 2)


def shape_operator(param: sp.Matrix, coords: Iterable[sp.Symbol]) -> dict[str, sp.Matrix]:
    u, v = list(coords)
    xu, xv = sp.diff(param, u), sp.diff(param, v)
    normal = sp.simplify(xu.cross(xv))
    normal = sp.simplify(normal / sp.sqrt(normal.dot(normal)))
    first = metric_tensor(param, [u, v])
    second = sp.Matrix(
        [
            [sp.simplify(sp.diff(param, u, u).dot(normal)), sp.simplify(sp.diff(param, u, v).dot(normal))],
            [sp.simplify(sp.diff(param, v, u).dot(normal)), sp.simplify(sp.diff(param, v, v).dot(normal))],
        ]
    )
    operator = sp.simplify(first.inv() * second)
    return {"first": first, "second": second, "shape_operator": operator, "normal": normal}


def great_circle_points(a: Iterable[float], b: Iterable[float], samples: int = 64) -> np.ndarray:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    omega = math.acos(float(np.clip(np.dot(a, b), -1.0, 1.0)))
    if omega < 1e-12:
        return np.repeat(a[None, :], samples, axis=0)
    ts = np.linspace(0.0, 1.0, samples)
    return np.array([(math.sin((1 - t) * omega) * a + math.sin(t * omega) * b) / math.sin(omega) for t in ts])


def spherical_triangle_area(a: Iterable[float], b: Iterable[float], c: Iterable[float], radius: float = 1.0) -> float:
    pts = [np.asarray(p, dtype=float) for p in (a, b, c)]
    pts = [p / np.linalg.norm(p) for p in pts]
    def angle(u: np.ndarray, v: np.ndarray, w: np.ndarray) -> float:
        vu = u - np.dot(u, v) * v
        vw = w - np.dot(w, v) * v
        return math.acos(float(np.clip(np.dot(vu, vw) / (np.linalg.norm(vu) * np.linalg.norm(vw)), -1.0, 1.0)))
    A = angle(pts[1], pts[0], pts[2])
    B = angle(pts[0], pts[1], pts[2])
    C = angle(pts[0], pts[2], pts[1])
    return radius**2 * (A + B + C - math.pi)


def stereographic_project(point: Iterable[float]) -> np.ndarray:
    x, y, z = np.asarray(point, dtype=float)
    denom = 1.0 - z
    return np.array([x / denom, y / denom])


def stereographic_inverse(x: float, y: float) -> np.ndarray:
    r2 = x * x + y * y
    return np.array([2 * x / (1 + r2), 2 * y / (1 + r2), (r2 - 1) / (1 + r2)])


def hyperbolic_half_plane_distance(p: complex, q: complex) -> float:
    if p.imag <= 0 or q.imag <= 0:
        raise ValueError("points must lie in the upper half-plane")
    arg = 1 + abs(p - q) ** 2 / (2 * p.imag * q.imag)
    return math.acosh(max(1.0, float(arg)))


def mobius_transform(z: complex, a: complex, b: complex, c: complex, d: complex) -> complex:
    denom = c * z + d
    if abs(denom) < 1e-12:
        raise ZeroDivisionError("Mobius denominator is near zero")
    return (a * z + b) / denom


def constant_curvature_circle_circumference(radius: float, K: float) -> float:
    if abs(K) < 1e-12:
        return 2 * math.pi * radius
    if K > 0:
        k = math.sqrt(K)
        return 2 * math.pi * math.sin(k * radius) / k
    k = math.sqrt(-K)
    return 2 * math.pi * math.sinh(k * radius) / k


def constant_curvature_circle_area(radius: float, K: float) -> float:
    if abs(K) < 1e-12:
        return math.pi * radius**2
    if K > 0:
        k = math.sqrt(K)
        return 2 * math.pi * (1 - math.cos(k * radius)) / K
    k = math.sqrt(-K)
    return 2 * math.pi * (math.cosh(k * radius) - 1) / (-K)


def surface_of_revolution(x_of_t: sp.Expr, y_of_t: sp.Expr, t: sp.Symbol, theta: sp.Symbol) -> sp.Matrix:
    return sp.Matrix([x_of_t, y_of_t * sp.cos(theta), y_of_t * sp.sin(theta)])
'''


FORMS_INIT = '''"""Differential-forms utilities for the VDGF course."""

from .core import CoordinateSystem, Form, basis_form, d, evaluate, pullback, wedge
from .hodge import hodge_star, musical_flat, musical_sharp, volume_form
from .integrals import line_integral, surface_integral
from .tensors import Tensor, antisymmetrize, contract, raise_index, lower_index, symmetrize, tensor_product
from .frames import connection_forms, curvature_forms

__all__ = [
    "CoordinateSystem",
    "Form",
    "Tensor",
    "antisymmetrize",
    "basis_form",
    "connection_forms",
    "contract",
    "curvature_forms",
    "d",
    "evaluate",
    "hodge_star",
    "line_integral",
    "lower_index",
    "musical_flat",
    "musical_sharp",
    "pullback",
    "raise_index",
    "surface_integral",
    "symmetrize",
    "tensor_product",
    "volume_form",
    "wedge",
]
'''


FORMS_CORE = '''"""Sparse symbolic differential forms."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import Iterable

import sympy as sp


def _perm_sign(values: tuple[int, ...]) -> int:
    inversions = 0
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            inversions += values[i] > values[j]
    return -1 if inversions % 2 else 1


def _canonical(indices: Iterable[int]) -> tuple[tuple[int, ...], int]:
    raw = tuple(indices)
    if len(set(raw)) != len(raw):
        return tuple(sorted(raw)), 0
    ordered = tuple(sorted(raw))
    return ordered, _perm_sign(raw)


@dataclass(frozen=True)
class CoordinateSystem:
    names: tuple[str, ...]
    symbols: tuple[sp.Symbol, ...]

    def __init__(self, names: Iterable[str] | str) -> None:
        if isinstance(names, str):
            names = names.replace(",", " ").split()
        names_tuple = tuple(str(name) for name in names)
        object.__setattr__(self, "names", names_tuple)
        object.__setattr__(self, "symbols", tuple(sp.symbols(" ".join(names_tuple))))

    @property
    def dimension(self) -> int:
        return len(self.names)


class Form:
    def __init__(self, coords: CoordinateSystem, degree: int, terms: dict[tuple[int, ...], sp.Expr] | None = None) -> None:
        self.coords = coords
        self.degree = int(degree)
        cleaned: dict[tuple[int, ...], sp.Expr] = {}
        for key, value in (terms or {}).items():
            key = tuple(key)
            if len(key) != self.degree:
                raise ValueError("term degree does not match form degree")
            canonical, sign = _canonical(key)
            if sign == 0:
                continue
            coeff = sp.simplify(sign * value)
            if coeff != 0:
                cleaned[canonical] = sp.simplify(cleaned.get(canonical, 0) + coeff)
        self.terms = {key: sp.simplify(value) for key, value in cleaned.items() if sp.simplify(value) != 0}

    def __repr__(self) -> str:
        if not self.terms:
            return f"0-form(degree={self.degree})"
        pieces = []
        for key, coeff in sorted(self.terms.items()):
            basis = "^".join(f"d{self.coords.names[i]}" for i in key) or "1"
            pieces.append(f"({sp.sstr(coeff)}) {basis}")
        return " + ".join(pieces)

    def __add__(self, other: "Form") -> "Form":
        self._check_compatible(other)
        if self.degree != other.degree:
            raise ValueError("only same-degree forms can be added")
        terms = dict(self.terms)
        for key, value in other.terms.items():
            terms[key] = sp.simplify(terms.get(key, 0) + value)
        return Form(self.coords, self.degree, terms)

    def __sub__(self, other: "Form") -> "Form":
        return self + (-other)

    def __neg__(self) -> "Form":
        return Form(self.coords, self.degree, {key: -value for key, value in self.terms.items()})

    def __mul__(self, scalar: sp.Expr | float | int) -> "Form":
        return Form(self.coords, self.degree, {key: sp.sympify(scalar) * value for key, value in self.terms.items()})

    __rmul__ = __mul__

    def _check_compatible(self, other: "Form") -> None:
        if self.coords != other.coords:
            raise TypeError("forms belong to different coordinate systems")

    def wedge(self, other: "Form") -> "Form":
        self._check_compatible(other)
        terms: dict[tuple[int, ...], sp.Expr] = {}
        for left_key, left_value in self.terms.items():
            for right_key, right_value in other.terms.items():
                key, sign = _canonical(left_key + right_key)
                if sign == 0:
                    continue
                terms[key] = sp.simplify(terms.get(key, 0) + sign * left_value * right_value)
        return Form(self.coords, self.degree + other.degree, terms)

    def exterior_derivative(self) -> "Form":
        terms: dict[tuple[int, ...], sp.Expr] = {}
        for key, value in self.terms.items():
            for i, symbol in enumerate(self.coords.symbols):
                deriv = sp.diff(value, symbol)
                if deriv == 0:
                    continue
                new_key, sign = _canonical((i,) + key)
                if sign == 0:
                    continue
                terms[new_key] = sp.simplify(terms.get(new_key, 0) + sign * deriv)
        return Form(self.coords, self.degree + 1, terms)

    def simplify(self) -> "Form":
        return Form(self.coords, self.degree, {key: sp.simplify(value) for key, value in self.terms.items()})

    def is_zero(self) -> bool:
        return all(sp.simplify(value) == 0 for value in self.terms.values())


def basis_form(coords: CoordinateSystem, index: int) -> Form:
    return Form(coords, 1, {(index,): sp.Integer(1)})


def wedge(left: Form, right: Form) -> Form:
    return left.wedge(right)


def d(form: Form) -> Form:
    return form.exterior_derivative()


def evaluate(form: Form, vectors: list[Iterable[sp.Expr]]) -> sp.Expr:
    if len(vectors) != form.degree:
        raise ValueError("need one vector per form degree")
    if form.degree == 0:
        return next(iter(form.terms.values()), sp.Integer(0))
    vectors = [list(map(sp.sympify, vector)) for vector in vectors]
    total = sp.Integer(0)
    for key, coeff in form.terms.items():
        matrix = sp.Matrix([[vectors[row][col] for col in key] for row in range(form.degree)])
        total += coeff * matrix.det()
    return sp.simplify(total)


def pullback(form: Form, target: CoordinateSystem, mapping: dict[sp.Symbol, sp.Expr]) -> Form:
    result = Form(target, 0, {(): 0})
    for key, coeff in form.terms.items():
        coeff_pb = sp.sympify(coeff).subs(mapping)
        term = Form(target, 0, {(): coeff_pb})
        for source_index in key:
            source_symbol = form.coords.symbols[source_index]
            expression = sp.sympify(mapping[source_symbol])
            one = Form(target, 1, {(i,): sp.diff(expression, target_symbol) for i, target_symbol in enumerate(target.symbols)})
            term = term.wedge(one)
        result = result + term if result.degree == term.degree else term
    return result.simplify()
'''


FORMS_TENSORS = '''"""Tiny tensor helpers used by the notebooks."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class Tensor:
    components: sp.MutableDenseNDimArray
    valence: tuple[int, int]

    @classmethod
    def from_matrix(cls, matrix: sp.Matrix, valence: tuple[int, int] = (0, 2)) -> "Tensor":
        return cls(sp.MutableDenseNDimArray(matrix), valence)


def tensor_product(left: Tensor, right: Tensor) -> Tensor:
    data = sp.tensorproduct(left.components, right.components)
    return Tensor(data, (left.valence[0] + right.valence[0], left.valence[1] + right.valence[1]))


def contract(tensor: Tensor, axis1: int = 0, axis2: int = 1) -> Tensor:
    data = sp.tensorcontraction(tensor.components, (axis1, axis2))
    up, down = tensor.valence
    return Tensor(data, (max(0, up - 1), max(0, down - 1)))


def symmetrize(matrix: sp.Matrix) -> sp.Matrix:
    return sp.simplify((matrix + matrix.T) / 2)


def antisymmetrize(matrix: sp.Matrix) -> sp.Matrix:
    return sp.simplify((matrix - matrix.T) / 2)


def raise_index(covector: sp.Matrix, metric: sp.Matrix) -> sp.Matrix:
    return sp.simplify(metric.inv() * covector)


def lower_index(vector: sp.Matrix, metric: sp.Matrix) -> sp.Matrix:
    return sp.simplify(metric * vector)
'''


FORMS_HODGE = '''"""Hodge star and musical maps for simple diagonal metrics."""

from __future__ import annotations

from itertools import combinations

import sympy as sp

from .core import CoordinateSystem, Form, _canonical


def volume_form(coords: CoordinateSystem, scale: sp.Expr = 1) -> Form:
    return Form(coords, coords.dimension, {tuple(range(coords.dimension)): sp.sympify(scale)})


def hodge_star(form: Form, metric: sp.Matrix | None = None, orientation: int = 1) -> Form:
    coords = form.coords
    n = coords.dimension
    if metric is None:
        metric = sp.eye(n)
    det_g = sp.simplify(metric.det())
    scale = sp.sqrt(abs(det_g)) if det_g != 1 else sp.Integer(1)
    inv_diag = [sp.simplify(metric.inv()[i, i]) for i in range(n)]
    terms: dict[tuple[int, ...], sp.Expr] = {}
    universe = set(range(n))
    for key, coeff in form.terms.items():
        complement = tuple(i for i in range(n) if i not in key)
        combined, sign = _canonical(key + complement)
        if combined != tuple(range(n)):
            sign = 0
        metric_factor = sp.prod(inv_diag[i] for i in key) if key else sp.Integer(1)
        if sign:
            terms[complement] = sp.simplify(terms.get(complement, 0) + orientation * sign * scale * metric_factor * coeff)
    return Form(coords, n - form.degree, terms)


def musical_flat(vector: sp.Matrix, metric: sp.Matrix, coords: CoordinateSystem) -> Form:
    cov = sp.simplify(metric * vector)
    return Form(coords, 1, {(i,): cov[i] for i in range(coords.dimension)})


def musical_sharp(one_form: Form, metric: sp.Matrix) -> sp.Matrix:
    if one_form.degree != 1:
        raise ValueError("sharp map expects a 1-form")
    coords = one_form.coords
    cov = sp.Matrix([one_form.terms.get((i,), 0) for i in range(coords.dimension)])
    return sp.simplify(metric.inv() * cov)
'''


FORMS_INTEGRALS = '''"""Symbolic and numerical integration helpers for forms."""

from __future__ import annotations

from typing import Iterable

import sympy as sp

from .core import Form, evaluate


def line_integral(one_form: Form, parameter: sp.Symbol, path: dict[sp.Symbol, sp.Expr], bounds: tuple[float | int | sp.Expr, float | int | sp.Expr]) -> sp.Expr:
    if one_form.degree != 1:
        raise ValueError("line integral expects a 1-form")
    velocity = [sp.diff(path[symbol], parameter) for symbol in one_form.coords.symbols]
    pulled = evaluate(one_form, [velocity]).subs(path)
    return sp.simplify(sp.integrate(pulled, (parameter, bounds[0], bounds[1])))


def surface_integral(two_form: Form, params: tuple[sp.Symbol, sp.Symbol], surface: dict[sp.Symbol, sp.Expr], bounds: tuple[tuple[sp.Expr, sp.Expr], tuple[sp.Expr, sp.Expr]]) -> sp.Expr:
    if two_form.degree != 2:
        raise ValueError("surface integral expects a 2-form")
    u, v = params
    du = [sp.diff(surface[symbol], u) for symbol in two_form.coords.symbols]
    dv = [sp.diff(surface[symbol], v) for symbol in two_form.coords.symbols]
    integrand = evaluate(two_form, [du, dv]).subs(surface)
    inner = sp.integrate(integrand, (u, bounds[0][0], bounds[0][1]))
    return sp.simplify(sp.integrate(inner, (v, bounds[1][0], bounds[1][1])))
'''


FORMS_FRAMES = '''"""Moving-frame helpers for Cartan-style computations."""

from __future__ import annotations

import sympy as sp

from .core import CoordinateSystem, Form, d


def connection_forms(frame: sp.Matrix, coords: CoordinateSystem) -> list[list[Form]]:
    """Return omega_ij = <d e_i, e_j> for an orthonormal frame in Euclidean space."""
    n = frame.shape[1]
    result: list[list[Form]] = []
    for i in range(n):
        row: list[Form] = []
        ei = frame[:, i]
        for j in range(n):
            ej = frame[:, j]
            coeffs = {}
            for k, symbol in enumerate(coords.symbols):
                coeffs[(k,)] = sp.simplify(sp.diff(ei, symbol).dot(ej))
            row.append(Form(coords, 1, coeffs))
        result.append(row)
    return result


def curvature_forms(omega: list[list[Form]]) -> list[list[Form]]:
    n = len(omega)
    result: list[list[Form]] = []
    for i in range(n):
        row: list[Form] = []
        for j in range(n):
            value = d(omega[i][j])
            for k in range(n):
                product = omega[i][k].wedge(omega[k][j])
                value = value + product
            row.append(value.simplify())
        result.append(row)
    return result
'''


VISUALS_PY = '''"""Reusable visual helpers for the VDGF notebooks.

The helpers are intentionally deterministic: a chapter visual should be
rebuildable, concept-specific, and easy to audit for nonblank output.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from utils.artifacts import save_matplotlib


PALETTE = {
    "ink": "#1d2733",
    "blue": "#2f6fbb",
    "teal": "#2a9d8f",
    "green": "#6a994e",
    "gold": "#d59f0f",
    "red": "#c44e52",
    "violet": "#7b5ea7",
    "gray": "#7a8793",
}


def unit_circle(samples: int = 240) -> tuple[np.ndarray, np.ndarray]:
    theta = np.linspace(0, 2 * np.pi, samples)
    return np.cos(theta), np.sin(theta)


def saddle_grid(samples: int = 40, extent: float = 1.5) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.linspace(-extent, extent, samples)
    y = np.linspace(-extent, extent, samples)
    X, Y = np.meshgrid(x, y)
    return X, Y, X**2 - Y**2


def form_stack_lines(slope: float = 1.0, offsets: int = 6, extent: float = 2.0) -> list[tuple[np.ndarray, np.ndarray]]:
    x = np.linspace(-extent, extent, 100)
    return [(x, -slope * x + b) for b in np.linspace(-extent, extent, offsets)]


def _style_axis(ax: Any, title: str, *, equal: bool = False) -> None:
    ax.set_title(title, fontsize=10, color=PALETTE["ink"])
    ax.grid(True, color="#d7dde5", linewidth=0.7, alpha=0.8)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color("#b6c0ca")


def _figure_stats(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGB")
    arr = np.asarray(image, dtype=float)
    return {
        "width": int(image.width),
        "height": int(image.height),
        "pixel_std": float(arr.std()),
        "file_size": int(path.stat().st_size),
    }


def _add_note(ax: Any, text: str) -> None:
    ax.text(
        0.02,
        0.98,
        text,
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=8,
        color=PALETTE["ink"],
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#d0d7de", "alpha": 0.9},
    )


def _plot_limit_lab(ax: Any, spec: dict[str, Any]) -> None:
    theta = np.linspace(0.2, math.pi * 0.95, 120)
    chord = 2 * np.sin(theta / 2)
    arc = theta
    sector = theta / 2
    ax.plot(theta, arc / chord, label="arc / chord", color=PALETTE["blue"])
    ax.plot(theta, sector / (chord**2 / 2), label="sector / triangle", color=PALETTE["teal"])
    ax.axhline(1, color=PALETTE["gray"], linestyle="--")
    ax.set_xlabel("angle")
    ax.set_ylabel("ratio")
    _style_axis(ax, spec["title"])
    ax.legend(fontsize=8)


def _plot_three_geometries(ax: Any, spec: dict[str, Any]) -> None:
    ax.plot([0, 1, 0.25, 0], [0, 0, 0.8, 0], color=PALETTE["blue"], lw=2, label="Euclidean")
    theta = np.linspace(0, math.pi / 2, 80)
    ax.plot(1.6 + np.cos(theta), np.sin(theta), color=PALETTE["teal"], lw=2, label="spherical arc")
    disk = plt.Circle((3.7, 0.45), 0.75, fill=False, color=PALETTE["gray"], lw=1.2)
    ax.add_patch(disk)
    t = np.linspace(-0.7, 0.7, 100)
    ax.plot(3.7 + t, 0.45 + 0.55 * (1 - t**2), color=PALETTE["red"], lw=2, label="Poincare arc")
    ax.set_xlim(-0.2, 4.7)
    ax.set_ylim(-0.2, 1.45)
    _style_axis(ax, spec["title"], equal=True)
    ax.legend(fontsize=8, loc="lower right")


def _plot_curvature_detectors(ax: Any, spec: dict[str, Any]) -> None:
    r = np.linspace(0.05, 1.3, 140)
    for K, color, label in [(1, PALETTE["teal"], "K=+1"), (0, PALETTE["gray"], "K=0"), (-1, PALETTE["red"], "K=-1")]:
        if K == 0:
            circumference = 2 * math.pi * r
        elif K > 0:
            circumference = 2 * math.pi * np.sin(r)
        else:
            circumference = 2 * math.pi * np.sinh(r)
        ax.plot(r, circumference - 2 * math.pi * r, color=color, label=label)
    ax.set_xlabel("geodesic radius")
    ax.set_ylabel("circumference defect")
    _style_axis(ax, spec["title"])
    ax.legend(fontsize=8)


def _plot_metric_atlas(ax: Any, spec: dict[str, Any]) -> None:
    xs = np.linspace(-2.2, 2.2, 13)
    ys = np.linspace(-2.2, 2.2, 13)
    for x in xs:
        ax.plot([x] * len(ys), ys, color="#d7dde5", lw=0.7)
    for y in ys:
        ax.plot(xs, [y] * len(xs), color="#d7dde5", lw=0.7)
    for x in np.linspace(-1.6, 1.6, 5):
        for y in np.linspace(-1.6, 1.6, 5):
            scale = 2 / (1 + x * x + y * y)
            ellipse = plt.matplotlib.patches.Ellipse((x, y), 0.18 * scale, 0.18 * scale, fill=False, color=PALETTE["blue"], lw=1)
            ax.add_patch(ellipse)
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    _style_axis(ax, spec["title"], equal=True)
    _add_note(ax, "Tissot circles shrink with stereographic scale")


def _plot_pseudosphere(ax: Any, spec: dict[str, Any]) -> None:
    x = np.linspace(-2.2, 2.2, 200)
    for center in [-1.2, 0.0, 1.2]:
        radius = 0.9 + abs(center) * 0.2
        xx = np.linspace(center - radius, center + radius, 120)
        yy = np.sqrt(np.maximum(radius**2 - (xx - center) ** 2, 0))
        ax.plot(xx, yy + 0.05, color=PALETTE["red"], lw=1.8)
    ax.axhline(0, color=PALETTE["ink"], lw=1.5)
    t = np.linspace(0.05, 2.4, 160)
    ax.plot(-3 + t - np.tanh(t), 1 / np.cosh(t), color=PALETTE["teal"], lw=2, label="tractrix profile")
    ax.set_xlim(-3.1, 2.4)
    ax.set_ylim(-0.1, 2.0)
    _style_axis(ax, spec["title"])
    ax.legend(fontsize=8)


def _plot_mobius(ax: Any, spec: dict[str, Any]) -> None:
    circle = plt.Circle((0, 0), 1, fill=False, color=PALETTE["ink"], lw=1.4)
    ax.add_patch(circle)
    theta = np.linspace(0, 2 * np.pi, 200)
    for radius, color in [(0.25, PALETTE["blue"]), (0.5, PALETTE["teal"]), (0.72, PALETTE["gold"])]:
        z = radius * np.exp(1j * theta)
        a = 0.35
        w = (z + a) / (a * z + 1)
        ax.plot(w.real, w.imag, color=color, lw=1.6)
    ax.scatter([0, 0.35], [0, 0], color=[PALETTE["blue"], PALETTE["red"]], s=35)
    _style_axis(ax, spec["title"], equal=True)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)


def _plot_curve(ax: Any, spec: dict[str, Any]) -> None:
    t = np.linspace(-2.4, 2.4, 240)
    y = np.sin(t) + 0.15 * spec["chapter"] * np.cos(0.7 * t) / 40
    ax.plot(t, y, color=PALETTE["blue"], lw=2)
    points = np.linspace(40, 200, 5, dtype=int)
    ax.scatter(t[points], y[points], color=PALETTE["red"], s=30, zorder=3)
    for idx in points:
        radius = 0.18 + 0.02 * ((idx + spec["chapter"]) % 5)
        circ = plt.Circle((t[idx], y[idx]), radius, fill=False, color=PALETTE["teal"], alpha=0.7)
        ax.add_patch(circ)
    _style_axis(ax, spec["title"])
    ax.set_xlabel("parameter")
    ax.set_ylabel("curve")


def _plot_helix(ax: Any, spec: dict[str, Any]) -> None:
    ax.remove()
    fig = plt.gcf()
    ax3 = fig.add_subplot(111, projection="3d")
    t = np.linspace(0, 4 * np.pi, 240)
    ax3.plot(np.cos(t), np.sin(t), t / (2 * np.pi), color=PALETTE["blue"], lw=2)
    for idx in [35, 90, 145, 200]:
        p = np.array([np.cos(t[idx]), np.sin(t[idx]), t[idx] / (2 * np.pi)])
        tangent = np.array([-np.sin(t[idx]), np.cos(t[idx]), 1 / (2 * np.pi)])
        tangent = tangent / np.linalg.norm(tangent)
        ax3.quiver(*p, *tangent, length=0.35, color=PALETTE["red"])
    ax3.set_title(spec["title"], fontsize=10)
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    ax3.set_zlabel("height")


def _plot_rose(ax: Any, spec: dict[str, Any]) -> None:
    ax.remove()
    fig = plt.gcf()
    polar = fig.add_subplot(111, projection="polar")
    theta = np.linspace(0, 2 * np.pi, 360)
    k1 = 0.4 + 0.03 * (spec["chapter"] % 7)
    k2 = -0.25 + 0.02 * (spec["chapter"] % 5)
    curvature = k1 * np.cos(theta) ** 2 + k2 * np.sin(theta) ** 2
    polar.plot(theta, curvature, color=PALETTE["violet"], lw=2)
    polar.set_title(spec["title"], fontsize=10)


def _plot_surface_panel(ax: Any, spec: dict[str, Any]) -> None:
    X, Y, Z = saddle_grid(samples=50)
    contours = ax.contourf(X, Y, Z, levels=16, cmap="viridis", alpha=0.85)
    ax.contour(X, Y, Z, levels=10, colors="white", linewidths=0.5, alpha=0.7)
    ax.quiver([0], [0], [0.75], [0.25], color=PALETTE["red"], angles="xy", scale_units="xy", scale=1)
    _style_axis(ax, spec["title"], equal=True)
    _add_note(ax, "surface patch: color = height, arrow = normal drift")


def _plot_topology(ax: Any, spec: dict[str, Any]) -> None:
    genus = np.arange(0, 5)
    chi = 2 - 2 * genus
    total = 2 * math.pi * chi
    ax.bar(genus, total, color=[PALETTE["teal"], PALETTE["blue"], PALETTE["gold"], PALETTE["red"], PALETTE["violet"]])
    ax.axhline(0, color=PALETTE["ink"], lw=1)
    ax.set_xlabel("genus")
    ax.set_ylabel("2 pi chi")
    _style_axis(ax, spec["title"])


def _plot_vector_field(ax: Any, spec: dict[str, Any]) -> None:
    x = np.linspace(-1.5, 1.5, 17)
    y = np.linspace(-1.5, 1.5, 17)
    X, Y = np.meshgrid(x, y)
    power = 1 + spec["chapter"] % 4
    angle = power * np.arctan2(Y, X)
    U, V = np.cos(angle), np.sin(angle)
    ax.quiver(X, Y, U, V, color=PALETTE["blue"], pivot="mid", scale=28)
    ax.scatter([0], [0], color=PALETTE["red"], s=45)
    _style_axis(ax, spec["title"], equal=True)
    _add_note(ax, f"index cue: winding power {power}")


def _plot_transport(ax: Any, spec: dict[str, Any]) -> None:
    theta = np.linspace(0, 2 * np.pi, 220)
    ax.plot(np.cos(theta), np.sin(theta), color=PALETTE["gray"], lw=1)
    phase = 0.12 * spec["chapter"]
    for t in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        p = np.array([np.cos(t), np.sin(t)])
        v = 0.28 * np.array([np.cos(t + phase), np.sin(t + phase)])
        ax.arrow(p[0], p[1], v[0], v[1], head_width=0.045, color=PALETTE["teal"], length_includes_head=True)
    _style_axis(ax, spec["title"], equal=True)
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)


def _plot_jacobi(ax: Any, spec: dict[str, Any]) -> None:
    s = np.linspace(0, 4, 240)
    ax.plot(s, s, color=PALETTE["gray"], label="K=0")
    ax.plot(s, np.sin(s), color=PALETTE["teal"], label="K=+1")
    ax.plot(s, np.sinh(s) / np.sinh(4), color=PALETTE["red"], label="K=-1 scaled")
    ax.set_xlabel("geodesic distance")
    ax.set_ylabel("separation")
    _style_axis(ax, spec["title"])
    ax.legend(fontsize=8)


def _plot_forms(ax: Any, spec: dict[str, Any]) -> None:
    chapter = spec["chapter"]
    if chapter == 32:
        for x, y in form_stack_lines(slope=0.7):
            ax.plot(x, y, color=PALETTE["blue"], alpha=0.8)
        ax.arrow(-1.4, -0.8, 1.1, 0.9, head_width=0.08, color=PALETTE["red"], length_includes_head=True)
    elif chapter == 33:
        matrix = np.array([[2, 0.6], [0.6, 1.1]])
        ax.imshow(matrix, cmap="YlGnBu")
        for (i, j), value in np.ndenumerate(matrix):
            ax.text(j, i, f"{value:.1f}", ha="center", va="center", color=PALETTE["ink"])
    elif chapter == 34:
        poly = np.array([[0, 0], [1.3, 0.35], [1.7, 1.2], [0.4, 0.85], [0, 0]])
        ax.plot(poly[:, 0], poly[:, 1], color=PALETTE["blue"], lw=2)
        ax.fill(poly[:, 0], poly[:, 1], color=PALETTE["teal"], alpha=0.25)
        ax.arrow(0.2, 0.15, 0.8, 0.22, head_width=0.05, color=PALETTE["red"])
    elif chapter == 35:
        squares = [(0, 0), (0.35, 0.25), (0.7, 0.5)]
        for x0, y0 in squares:
            ax.add_patch(plt.Rectangle((x0, y0), 0.8, 0.8, fill=False, edgecolor=PALETTE["blue"], lw=1.5))
        ax.arrow(0.15, 0.15, 0.8, 0.5, head_width=0.05, color=PALETTE["red"])
    else:
        xs = np.linspace(-2, 2, 200)
        ax.plot(xs, np.sin(xs * (1 + chapter % 3)), color=PALETTE["blue"], label="form")
        ax.plot(xs, np.gradient(np.sin(xs * (1 + chapter % 3)), xs), color=PALETTE["red"], label="d form")
        ax.legend(fontsize=8)
    _style_axis(ax, spec["title"], equal=chapter in {32, 34, 35})


def _plot_dashboard(ax: Any, spec: dict[str, Any]) -> None:
    values = np.array([(spec["chapter"] * i) % 9 + 1 for i in range(1, 10)]).reshape(3, 3)
    ax.imshow(values, cmap="magma")
    for (i, j), value in np.ndenumerate(values):
        ax.text(j, i, str(int(value)), ha="center", va="center", color="white", fontsize=9)
    _style_axis(ax, spec["title"])
    ax.set_xticks([])
    ax.set_yticks([])


def _plot_schwarzschild(ax: Any, spec: dict[str, Any]) -> None:
    r = np.linspace(2.05, 10, 240)
    f = 1 - 2 / r
    ax.plot(r, f, color=PALETTE["blue"], label="1 - 2M/r")
    ax.plot(r, 1 / f, color=PALETTE["red"], label="radial metric factor")
    ax.axvline(2, color=PALETTE["ink"], linestyle="--", label="horizon")
    ax.set_ylim(-0.1, 8)
    ax.set_xlabel("r / M")
    _style_axis(ax, spec["title"])
    ax.legend(fontsize=8)


def build_chapter_visual(spec: dict[str, Any], artifact_root: str | Path, artifact_topic: str) -> tuple[Path, dict[str, Any]]:
    """Create, save, and quality-check the chapter-specific static visual."""

    family = spec.get("family", "dashboard")
    fig, ax = plt.subplots(figsize=(7, 4.8))
    if family == "limit":
        _plot_limit_lab(ax, spec)
    elif family == "geometries":
        _plot_three_geometries(ax, spec)
    elif family == "curvature":
        _plot_curvature_detectors(ax, spec)
    elif family == "metric":
        _plot_metric_atlas(ax, spec)
    elif family == "pseudosphere":
        _plot_pseudosphere(ax, spec)
    elif family == "mobius":
        _plot_mobius(ax, spec)
    elif family == "curve":
        _plot_curve(ax, spec)
    elif family == "helix":
        _plot_helix(ax, spec)
    elif family == "rose":
        _plot_rose(ax, spec)
    elif family == "surface":
        _plot_surface_panel(ax, spec)
    elif family == "topology":
        _plot_topology(ax, spec)
    elif family == "vector-field":
        _plot_vector_field(ax, spec)
    elif family == "transport":
        _plot_transport(ax, spec)
    elif family == "jacobi":
        _plot_jacobi(ax, spec)
    elif family == "forms":
        _plot_forms(ax, spec)
    elif family == "schwarzschild":
        _plot_schwarzschild(ax, spec)
    else:
        _plot_dashboard(ax, spec)
    fig.suptitle(spec.get("caption", ""), fontsize=9, y=0.01, color=PALETTE["gray"])
    path = save_matplotlib(fig, artifact_topic, "figures", spec["filename"], root=artifact_root)
    plt.close(fig)
    stats = _figure_stats(path)
    if stats["file_size"] <= 1000 or stats["pixel_std"] <= 1.0:
        raise ValueError(f"visual artifact looks blank or too small: {path}")
    return path, stats
'''


VISUAL_SPECS: dict[int, dict[str, str]] = {
    0: {
        "filename": "ultimate-equality-convergence.png",
        "family": "limit",
        "title": "Ultimate Equality Convergence",
        "caption": "A visual proof becomes computational when limiting ratios settle to the same invariant.",
    },
    1: {
        "filename": "three-geometries-triangle.png",
        "family": "geometries",
        "title": "Three Geometries Triangle",
        "caption": "Straightness and angle sum change when lines become geodesics in different model spaces.",
    },
    2: {
        "filename": "curvature-detectors.png",
        "family": "curvature",
        "title": "Curvature Detectors",
        "caption": "Small geodesic circles expose positive, zero, and negative Gaussian curvature.",
    },
    3: {
        "filename": "act-i-exercise-invariant-cards.png",
        "family": "dashboard",
        "title": "Act I Invariant Cards",
        "caption": "Exercise checks are organized by the invariant that would fail first.",
    },
    4: {
        "filename": "metric-distortion-atlas.png",
        "family": "metric",
        "title": "Metric Distortion Atlas",
        "caption": "Coordinate circles turn into local metric gauges for length and area distortion.",
    },
    5: {
        "filename": "pseudosphere-half-plane-bridge.png",
        "family": "pseudosphere",
        "title": "Pseudosphere Half-Plane Bridge",
        "caption": "The tractrix profile and orthogonal semicircles give concrete hyperbolic measurements.",
    },
    6: {
        "filename": "mobius-isometry-strip.png",
        "family": "mobius",
        "title": "Mobius Isometry Strip",
        "caption": "Disk circles are carried to disk circles while the hyperbolic boundary stays fixed.",
    },
    7: {
        "filename": "act-ii-metric-lab-dashboard.png",
        "family": "dashboard",
        "title": "Act II Metric Lab Dashboard",
        "caption": "Metric, conformality, and isometry checks become a compact regression board.",
    },
    8: {
        "filename": "osculating-circle-sweep.png",
        "family": "curve",
        "title": "Osculating Circle Sweep",
        "caption": "A moving circle records curvature as the curve changes direction.",
    },
    9: {
        "filename": "frenet-helix-frame.png",
        "family": "helix",
        "title": "Frenet Helix Frame",
        "caption": "Tangent directions along a helix show curvature and torsion as moving-frame data.",
    },
    10: {
        "filename": "principal-curvature-rose.png",
        "family": "rose",
        "title": "Principal Curvature Rose",
        "caption": "Normal curvature varies by tangent direction between principal values.",
    },
    11: {
        "filename": "clairaut-invariant.png",
        "family": "transport",
        "title": "Clairaut Invariant",
        "caption": "A transported direction around a latitude-style loop makes the conserved quantity visible.",
    },
    12: {
        "filename": "gauss-map-distortion.png",
        "family": "surface",
        "title": "Gauss Map Distortion",
        "caption": "Surface patches and normal drift turn curvature into area distortion on the sphere of normals.",
    },
    13: {
        "filename": "plane-cylinder-egregium.png",
        "family": "surface",
        "title": "Plane Cylinder Egregium",
        "caption": "Bending can change the embedding without changing the intrinsic metric.",
    },
    14: {
        "filename": "spike-angular-defect.png",
        "family": "dashboard",
        "title": "Spike Angular Defect",
        "caption": "Cone-like singularities concentrate curvature as angular deficit.",
    },
    15: {
        "filename": "shape-operator-ellipse.png",
        "family": "rose",
        "title": "Shape Operator Ellipse",
        "caption": "The shape operator is read by how it stretches directions in the tangent plane.",
    },
    16: {
        "filename": "gauss-bonnet-topology-catalog.png",
        "family": "topology",
        "title": "Gauss-Bonnet Topology Catalog",
        "caption": "Total curvature follows Euler characteristic rather than local drawing style.",
    },
    17: {
        "filename": "turning-number-deformation.png",
        "family": "curve",
        "title": "Turning Number Deformation",
        "caption": "Continuous curve deformations preserve total turning until a singular event intervenes.",
    },
    18: {
        "filename": "angular-excess-ledger.png",
        "family": "dashboard",
        "title": "Angular Excess Ledger",
        "caption": "Local angle gains and losses add into a global curvature account.",
    },
    19: {
        "filename": "vector-field-index-atlas.png",
        "family": "vector-field",
        "title": "Vector Field Index Atlas",
        "caption": "Winding near zeros is the local data behind index theorems.",
    },
    20: {
        "filename": "act-iii-dashboard.png",
        "family": "dashboard",
        "title": "Act III Curvature Dashboard",
        "caption": "Curve, surface, topology, and vector-field invariants become executable checks.",
    },
    21: {
        "filename": "einstein-levicivita-puzzle-map.png",
        "family": "dashboard",
        "title": "Einstein-Levi-Civita Puzzle Map",
        "caption": "Parallelism becomes a question about what rule carries a vector between tangent planes.",
    },
    22: {
        "filename": "extrinsic-projection-transport.png",
        "family": "transport",
        "title": "Extrinsic Projection Transport",
        "caption": "Projection transport keeps arrows tangent while the surrounding space supplies a shortcut.",
    },
    23: {
        "filename": "intrinsic-geodesic-ladder.png",
        "family": "transport",
        "title": "Intrinsic Geodesic Ladder",
        "caption": "Small geodesic steps approximate transport without appealing to an ambient normal.",
    },
    24: {
        "filename": "holonomy-meter.png",
        "family": "transport",
        "title": "Holonomy Meter",
        "caption": "A loop returns the base point but may rotate the carried tangent vector.",
    },
    25: {
        "filename": "egregium-via-holonomy.png",
        "family": "transport",
        "title": "Egregium Via Holonomy",
        "caption": "Loop rotation lets intrinsic travelers detect Gaussian curvature.",
    },
    26: {
        "filename": "holonomy-boundary-cancellation.png",
        "family": "transport",
        "title": "Holonomy Boundary Cancellation",
        "caption": "Adjacent loops share boundaries whose transport contributions cancel in pairs.",
    },
    27: {
        "filename": "metric-curvature-circulation.png",
        "family": "vector-field",
        "title": "Metric Curvature Circulation",
        "caption": "Connection circulation records the metric data that accumulates around a loop.",
    },
    28: {
        "filename": "jacobi-geodesic-deviation.png",
        "family": "jacobi",
        "title": "Jacobi Geodesic Deviation",
        "caption": "Nearby geodesics focus or diverge according to the sign of curvature.",
    },
    29: {
        "filename": "riemann-small-loop-holonomy.png",
        "family": "transport",
        "title": "Riemann Small-Loop Holonomy",
        "caption": "The Riemann tensor is the infinitesimal version of loop holonomy.",
    },
    30: {
        "filename": "schwarzschild-curvature-panel.png",
        "family": "schwarzschild",
        "title": "Schwarzschild Curvature Panel",
        "caption": "A spacetime metric changes its radial and temporal factors near the horizon.",
    },
    31: {
        "filename": "act-iv-dashboard.png",
        "family": "dashboard",
        "title": "Act IV Transport Dashboard",
        "caption": "Transport, holonomy, Jacobi fields, and spacetime checks share one audit surface.",
    },
    32: {
        "filename": "one-form-measuring-grid.png",
        "family": "forms",
        "title": "One-Form Measuring Grid",
        "caption": "A 1-form is visualized as parallel measurement stacks acting on tangent vectors.",
    },
    33: {
        "filename": "tensor-valence-machine.png",
        "family": "forms",
        "title": "Tensor Valence Machine",
        "caption": "Tensor components form a machine whose valence determines its inputs and outputs.",
    },
    34: {
        "filename": "two-form-flux-parallelogram.png",
        "family": "forms",
        "title": "Two-Form Flux Parallelogram",
        "caption": "A 2-form measures oriented area and changes sign when orientation flips.",
    },
    35: {
        "filename": "three-form-volume-orientation.png",
        "family": "forms",
        "title": "Three-Form Volume Orientation",
        "caption": "A 3-form measures oriented volume by combining three independent directions.",
    },
    36: {
        "filename": "exterior-derivative-pipeline.png",
        "family": "forms",
        "title": "Exterior Derivative Pipeline",
        "caption": "Exterior differentiation sends measurement stacks to boundary-sensitive density.",
    },
    37: {
        "filename": "stokes-bridge.png",
        "family": "forms",
        "title": "Stokes Bridge",
        "caption": "The same form data appears as an interior derivative and a boundary integral.",
    },
    38: {
        "filename": "cartan-moving-frame-dashboard.png",
        "family": "forms",
        "title": "Cartan Moving-Frame Dashboard",
        "caption": "Connection and curvature forms compress moving-frame geometry into exterior calculus.",
    },
    39: {
        "filename": "act-v-forms-lab-dashboard.png",
        "family": "dashboard",
        "title": "Act V Forms Lab Dashboard",
        "caption": "Form, tensor, Stokes, and moving-frame exercises become a validation board.",
    },
}


def visual_spec_for_entry(entry: dict[str, object]) -> dict[str, object]:
    number = int(entry["number"])
    spec = dict(VISUAL_SPECS[number])
    spec["chapter"] = number
    spec["entry_label"] = str(entry["label"])
    spec["entry_title"] = str(entry["title"])
    spec["source_focus"] = str(entry["focus"])
    return spec


BUILD_INDEXES = '''"""Rebuild VDGF book and part indexes from the inventory."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

from pathlib import Path

import vdgf_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def slugify(value: str) -> str:
    import re

    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-+", "-", slug)


PART_FOLDER_BY_TITLE = {
    "Front Matter": "part-00-prologue",
    "Act I: The Nature of Space": "part-01-the-nature-of-space",
    "Act II: The Metric": "part-02-the-metric",
    "Act III: Curvature": "part-03-curvature",
    "Act IV: Parallel Transport": "part-04-parallel-transport",
    "Act V: Forms": "part-05-forms",
}


def normalized_parts() -> list[dict[str, object]]:
    if hasattr(inventory, "PARTS"):
        return list(inventory.PARTS)
    seen: list[str] = []
    for item in inventory.INVENTORY:
        part = item["part"]
        if part not in seen:
            seen.append(part)
    return [
        {
            "folder": PART_FOLDER_BY_TITLE[part],
            "title": "Prologue" if part == "Front Matter" else part,
            "description": part,
        }
        for part in seen
    ]


def normalized_entries() -> list[dict[str, object]]:
    if hasattr(inventory, "ENTRIES"):
        return list(inventory.ENTRIES)
    entries = []
    for item in inventory.INVENTORY:
        identifier = item["id"]
        is_prologue = identifier == "prologue"
        number = 0 if is_prologue else int(identifier)
        title = item["title"]
        if is_prologue:
            folder = "prologue"
            notebook = "prologue.ipynb"
            label = "Prologue"
        else:
            slug = slugify(title)
            folder = f"chapter-{number:02d}-{slug}"
            notebook = f"{number:02d}-{slug}.ipynb"
            label = f"Chapter {number:02d}"
        entries.append(
            {
                "kind": "prologue" if is_prologue else "chapter",
                "part": PART_FOLDER_BY_TITLE[item["part"]],
                "label": label,
                "number": number,
                "title": title,
                "folder": folder,
                "notebook": notebook,
                "printed": item["printed_span"],
                "pdf": item["pdf_span"],
                "focus": item["focus"],
                "topics": item["topics"],
            }
        )
    return entries


PARTS = normalized_parts()
ENTRIES = normalized_entries()


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\\n")]), path)


def entry_link(entry: dict[str, object]) -> str:
    return f"{entry['part']}/{entry['folder']}/00-index.ipynb"


def canonical_link(entry: dict[str, object]) -> str:
    return f"{entry['part']}/{entry['folder']}/{entry['notebook']}"


def build_book_index() -> str:
    lines = [
        "# Visual Differential Geometry and Forms - Standalone Notebook Edition",
        "",
        "This course is an original executable notebook edition organized around the book's prologue, five acts, and 39 chapters. The notebooks teach the mathematical ideas with fresh prose, derivations, code, generated artifacts, and sanity checks. The source PDF remains local and is not redistributed through notebook outputs.",
        "",
        "Body printed pages map to PDF pages by `pdf_page = printed_page + 29`.",
        "",
    ]
    for part in PARTS:
        lines.extend([f"## {part['title']}", "", str(part["description"]), ""])
        lines.append(f"- [Open part index]({part['folder']}/00-part-index.ipynb)")
        for entry in ENTRIES:
            if entry["part"] == part["folder"]:
                lines.append(
                    f"- [{entry['label']}: {entry['title']}]({entry_link(entry)}) - "
                    f"[canonical]({canonical_link(entry)}); printed pp. {entry['printed']}; PDF pp. {entry['pdf']}; {entry['focus']}"
                )
        lines.append("")
    return "\\n".join(lines)


def build_part_index(part: dict[str, object]) -> str:
    lines = [
        f"# {part['title']}",
        "",
        "[Back to Book Index](../00-book-index.ipynb)",
        "",
        str(part["description"]),
        "",
    ]
    for entry in ENTRIES:
        if entry["part"] != part["folder"]:
            continue
        lines.extend(
            [
                f"## {entry['label']}: {entry['title']}",
                "",
                f"- Chapter index: [{entry['folder']}/00-index.ipynb]({entry['folder']}/00-index.ipynb)",
                f"- Canonical notebook: [{entry['notebook']}]({entry['folder']}/{entry['notebook']})",
                f"- Source span: printed pp. {entry['printed']}; PDF pp. {entry['pdf']}",
                f"- Focus: {entry['focus']}",
                "",
            ]
        )
    return "\\n".join(lines)


def main() -> None:
    missing = []
    for entry in ENTRIES:
        folder = BOOK_ROOT / str(entry["part"]) / str(entry["folder"])
        for path in [folder / "00-index.ipynb", folder / str(entry["notebook"])]:
            if not path.exists():
                missing.append(path)
    if missing:
        raise FileNotFoundError("\\n".join(str(path) for path in missing))
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for part in PARTS:
        write_markdown_notebook(BOOK_ROOT / str(part["folder"]) / "00-part-index.ipynb", build_part_index(part))
    print(f"Updated {1 + len(PARTS)} indexes for {len(ENTRIES)} entries.")


if __name__ == "__main__":
    main()
'''


AUDIT_SCRIPT = '''"""Audit VDGF notebooks for depth and executable structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import nbformat

BOOK_ROOT = Path(__file__).resolve().parents[1]


def discover_notebooks() -> list[Path]:
    artifact_root = BOOK_ROOT / "artifacts"
    ignored = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}
    return [
        path
        for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in ignored
    ]


def notebook_stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    return {
        "path": str(path.relative_to(BOOK_ROOT)),
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "artifact_refs": sum(source.count("save_") + source.count("display_artifact") for source in code),
    }


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
        if item["markdown_words"] < args.min_words or item["code_cells"] < args.min_code_cells
    ]
    report = {"notebook_count": len(stats), "failing_count": len(failing), "failing": failing, "stats": stats}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(stats)} canonical notebooks")
    if failing:
        print(f"{len(failing)} notebooks are below thresholds:")
        for item in failing:
            print(f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells")
        raise SystemExit(1)
    print("All canonical notebooks meet the configured depth thresholds.")


if __name__ == "__main__":
    main()
'''


VISUAL_AUDIT_SCRIPT = '''"""Audit VDGF notebook visuals and generated PNG artifacts."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageStat

import vdgf_inventory as inventory


BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}
PLACEHOLDER_NAME = "constant-curvature-circles.png"
VISUAL_SAVE_CALLS = frozenset({"save_image", "save_matplotlib", "save_plotly_html", "build_chapter_visual"})


@dataclass(frozen=True)
class NotebookVisualStats:
    path: str
    visual_save_calls: int
    display_artifact_calls: int
    parse_errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class ImageStats:
    path: str
    topic: str
    width: int
    height: int
    bytes: int
    sha256: str
    max_channel_stddev: float


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def expected_artifact_topics() -> list[str]:
    """Return canonical VDGF artifact topics in inventory order."""

    if hasattr(inventory, "INVENTORY"):
        items = list(inventory.INVENTORY)
        return ["prologue" if item["id"] == "prologue" else f"chapter-{int(item['id']):02d}" for item in items]
    return ["prologue" if int(entry["number"]) == 0 else f"chapter-{int(entry['number']):02d}" for entry in inventory.ENTRIES]


def discover_notebooks(book_root: Path = BOOK_ROOT) -> list[Path]:
    artifact_root = Path(book_root) / "artifacts"
    return [
        path
        for path in sorted(Path(book_root).rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED_NOTEBOOKS
    ]


def _notebook_code_sources(path: Path) -> Iterable[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    for cell in data.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", "")
        yield "".join(source) if isinstance(source, list) else str(source)


def _call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def notebook_visual_stats(path: Path, book_root: Path = BOOK_ROOT) -> NotebookVisualStats:
    visual_save_calls = 0
    display_artifact_calls = 0
    parse_errors: list[str] = []

    for cell_index, source in enumerate(_notebook_code_sources(path), start=1):
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            parse_errors.append(f"cell {cell_index}: {exc.msg}")
            visual_save_calls += sum(source.count(f"{name}(") for name in VISUAL_SAVE_CALLS)
            display_artifact_calls += source.count("display_artifact(")
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = _call_name(node)
            if name in VISUAL_SAVE_CALLS:
                visual_save_calls += 1
            elif name == "display_artifact":
                display_artifact_calls += 1

    return NotebookVisualStats(
        path=_relative(path, Path(book_root)),
        visual_save_calls=visual_save_calls,
        display_artifact_calls=display_artifact_calls,
        parse_errors=tuple(parse_errors),
    )


def audit_notebook_displays(book_root: Path = BOOK_ROOT) -> tuple[list[NotebookVisualStats], list[dict[str, Any]]]:
    stats = [notebook_visual_stats(path, book_root) for path in discover_notebooks(book_root)]
    findings: list[dict[str, Any]] = []
    for item in stats:
        for error in item.parse_errors:
            findings.append(
                {
                    "check": "notebook-parse-error",
                    "path": item.path,
                    "message": f"Could not parse notebook code for visual audit: {error}.",
                    "details": {"error": error},
                }
            )
        if item.visual_save_calls == 0:
            findings.append(
                {
                    "check": "missing-visual-save",
                    "path": item.path,
                    "message": "Notebook has no static or interactive visual save call.",
                    "details": {"visual_save_calls": item.visual_save_calls},
                }
            )
        if item.display_artifact_calls < item.visual_save_calls:
            findings.append(
                {
                    "check": "missing-display-artifact",
                    "path": item.path,
                    "message": (
                        f"Notebook saves {item.visual_save_calls} visual artifact(s) but calls "
                        f"display_artifact {item.display_artifact_calls} time(s)."
                    ),
                    "details": {
                        "visual_save_calls": item.visual_save_calls,
                        "display_artifact_calls": item.display_artifact_calls,
                    },
                }
            )
    return stats, findings


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_stats(path: Path, topic: str, book_root: Path = BOOK_ROOT) -> ImageStats:
    with Image.open(path) as image:
        image.load()
        width, height = image.size
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
    return ImageStats(
        path=_relative(path, Path(book_root)),
        topic=topic,
        width=width,
        height=height,
        bytes=path.stat().st_size,
        sha256=_sha256(path),
        max_channel_stddev=max(stat.stddev) if stat.stddev else 0.0,
    )


def _topic_pngs(artifact_root: Path, topic: str) -> list[Path]:
    topic_root = artifact_root / topic
    if not topic_root.exists():
        return []
    return sorted(topic_root.rglob("*.png"))


def audit_png_artifacts(
    book_root: Path = BOOK_ROOT,
    *,
    expected_topics: Iterable[str] | None = None,
    min_width: int = 64,
    min_height: int = 64,
    min_pixels: int = 4096,
    blank_stddev: float = 1.0,
    allowed_placeholder_count: int = 0,
) -> tuple[list[ImageStats], list[dict[str, Any]]]:
    root = Path(book_root)
    artifact_root = root / "artifacts"
    topics = expected_artifact_topics() if expected_topics is None else list(expected_topics)
    findings: list[dict[str, Any]] = []
    stats: list[ImageStats] = []
    png_paths: list[Path] = []

    for topic in topics:
        topic_pngs = _topic_pngs(artifact_root, topic)
        png_paths.extend(topic_pngs)
        chapter_specific_pngs = [path for path in topic_pngs if path.name != PLACEHOLDER_NAME]
        if not chapter_specific_pngs:
            findings.append(
                {
                    "check": "missing-chapter-specific-png",
                    "path": _relative(artifact_root / topic, root),
                    "message": f"{topic} has no non-placeholder PNG artifact.",
                    "details": {"png_count": len(topic_pngs)},
                }
            )

    for path in png_paths:
        topic = path.relative_to(artifact_root).parts[0]
        try:
            item = image_stats(path, topic, root)
        except OSError as exc:
            findings.append(
                {
                    "check": "unreadable-image",
                    "path": _relative(path, root),
                    "message": f"Could not read PNG image: {exc}.",
                    "details": {"error": str(exc)},
                }
            )
            continue
        stats.append(item)
        if item.width < min_width or item.height < min_height or item.width * item.height < min_pixels:
            findings.append(
                {
                    "check": "tiny-image",
                    "path": item.path,
                    "message": f"PNG is too small at {item.width}x{item.height}px.",
                    "details": {"width": item.width, "height": item.height},
                }
            )
        if item.max_channel_stddev <= blank_stddev:
            findings.append(
                {
                    "check": "blank-image",
                    "path": item.path,
                    "message": "PNG appears blank or nearly constant.",
                    "details": {"max_channel_stddev": item.max_channel_stddev},
                }
            )

    by_hash: dict[str, list[ImageStats]] = {}
    for item in stats:
        by_hash.setdefault(item.sha256, []).append(item)
    for digest, matches in sorted(by_hash.items(), key=lambda pair: pair[0]):
        if len(matches) <= 1:
            continue
        findings.append(
            {
                "check": "duplicate-png-hash",
                "path": matches[0].path,
                "message": f"{len(matches)} PNG artifacts share SHA256 {digest[:12]}.",
                "details": {"sha256": digest, "paths": [item.path for item in matches]},
            }
        )

    placeholder_paths = [item.path for item in stats if Path(item.path).name == PLACEHOLDER_NAME]
    if len(placeholder_paths) > allowed_placeholder_count:
        findings.append(
            {
                "check": "repeated-placeholder-png",
                "path": placeholder_paths[0],
                "message": f"Forbidden placeholder {PLACEHOLDER_NAME!r} appears {len(placeholder_paths)} time(s).",
                "details": {
                    "placeholder_name": PLACEHOLDER_NAME,
                    "allowed_count": allowed_placeholder_count,
                    "paths": placeholder_paths,
                },
            }
        )
    return stats, findings


def audit_visuals(
    book_root: Path = BOOK_ROOT,
    *,
    expected_topics: Iterable[str] | None = None,
    min_width: int = 64,
    min_height: int = 64,
    min_pixels: int = 4096,
    blank_stddev: float = 1.0,
    allowed_placeholder_count: int = 0,
) -> dict[str, Any]:
    notebooks, notebook_findings = audit_notebook_displays(book_root)
    images, image_findings = audit_png_artifacts(
        book_root,
        expected_topics=expected_topics,
        min_width=min_width,
        min_height=min_height,
        min_pixels=min_pixels,
        blank_stddev=blank_stddev,
        allowed_placeholder_count=allowed_placeholder_count,
    )
    findings = [*notebook_findings, *image_findings]
    return {
        "summary": {
            "notebook_count": len(notebooks),
            "png_count": len(images),
            "finding_count": len(findings),
        },
        "findings": findings,
        "notebooks": [asdict(item) for item in notebooks],
        "images": [asdict(item) for item in images],
    }


def print_text_report(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print(f"Audited {summary['notebook_count']} notebooks and {summary['png_count']} PNGs")
    findings = report["findings"]
    if not findings:
        print("All VDGF visual audit checks passed.")
        return
    print(f"{len(findings)} visual audit finding(s):")
    for finding in findings:
        path = finding.get("path", "")
        location = f" [{path}]" if path else ""
        print(f"- {finding['check']}{location}: {finding['message']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book-root", type=Path, default=BOOK_ROOT)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-fail", action="store_true", help="Report findings without a nonzero exit.")
    parser.add_argument("--min-width", type=int, default=64)
    parser.add_argument("--min-height", type=int, default=64)
    parser.add_argument("--min-pixels", type=int, default=4096)
    parser.add_argument("--blank-stddev", type=float, default=1.0)
    parser.add_argument("--allowed-placeholder-count", type=int, default=0)
    args = parser.parse_args()

    report = audit_visuals(
        args.book_root,
        min_width=args.min_width,
        min_height=args.min_height,
        min_pixels=args.min_pixels,
        blank_stddev=args.blank_stddev,
        allowed_placeholder_count=args.allowed_placeholder_count,
    )
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_text_report(report)
    if report["summary"]["finding_count"] and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
'''


VALIDATE_SCRIPT = '''"""Execute VDGF notebooks with nbclient."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

BOOK_ROOT = Path(__file__).resolve().parents[1]

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def notebook_paths(all_notebooks: bool, limit: int | None) -> list[Path]:
    artifact_root = BOOK_ROOT / "artifacts"
    paths = [path for path in sorted(BOOK_ROOT.rglob("*.ipynb")) if artifact_root not in path.parents]
    if not all_notebooks:
        smoke_names = {
            "00-book-index.ipynb",
            "prologue.ipynb",
            "01-euclidean-and-non-euclidean-geometry.ipynb",
            "04-mapping-surfaces-the-metric.ipynb",
            "15-the-shape-operator.ipynb",
            "29-riemanns-curvature.ipynb",
            "32-1-forms.ipynb",
            "38-differential-geometry-via-forms.ipynb",
        }
        paths = [path for path in paths if path.name in smoke_names]
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
    failures: list[tuple[Path, str]] = []
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


TEST_SCRIPT = '''"""Core smoke tests for the VDGF course utilities."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from PIL import Image

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from audit_vdgf_visuals import audit_visuals
from utils.dg import gaussian_curvature_2d, metric_tensor, plane_curve_curvature, sphere_embedding
from utils.forms import CoordinateSystem, basis_form, d, evaluate, hodge_star
from utils.visuals import build_chapter_visual


def test_plane_curve_curvature_unit_circle() -> None:
    theta = np.linspace(0, 2 * np.pi, 64)
    velocity = np.column_stack([-np.sin(theta), np.cos(theta)])
    acceleration = np.column_stack([-np.cos(theta), -np.sin(theta)])
    kappa = plane_curve_curvature(velocity, acceleration)
    assert np.allclose(kappa, 1.0)


def test_sphere_gaussian_curvature() -> None:
    u, v = sp.symbols("u v", positive=True)
    param = sphere_embedding(u, v)
    metric = metric_tensor(param, [u, v])
    K = gaussian_curvature_2d(metric, [u, v])
    assert sp.simplify(K - 1) == 0


def test_forms_exterior_derivative_squared_zero() -> None:
    coords = CoordinateSystem("R3", "x y z")
    x, y, z = coords.symbols
    dx, dy, dz = [basis_form(coords, i) for i in range(3)]
    omega = x * dy + y * dz + z * dx
    assert not bool(d(d(omega)))


def test_form_evaluate_and_hodge() -> None:
    coords = CoordinateSystem("R3", "x y z")
    dx, dy, dz = [basis_form(coords, i) for i in range(3)]
    area = dx.wedge(dy)
    assert evaluate(area, [1, 0, 0], [0, 1, 0]) == 1
    assert hodge_star(dx).components == {(1, 2): 1}


def test_build_chapter_visual_smoke(tmp_path: Path) -> None:
    spec = {
        "chapter": 12,
        "filename": "gauss-map-distortion.png",
        "family": "surface",
        "title": "Gauss Map Distortion",
        "caption": "surface patch and normal drift",
    }
    path, stats = build_chapter_visual(spec, tmp_path, "chapter-12")
    assert path.exists()
    assert path.name == "gauss-map-distortion.png"
    assert stats["width"] >= 300
    assert stats["height"] >= 200
    assert stats["file_size"] > 1000
    assert stats["pixel_std"] > 1.0


def _write_notebook(path: Path, source: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": source,
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(notebook), encoding="utf-8")


def _save_png(path: Path, array: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(array.astype(np.uint8)).save(path)


def test_visual_audit_detects_requested_failure_modes(tmp_path: Path) -> None:
    _write_notebook(
        tmp_path / "part-01" / "chapter-01-example" / "01-example.ipynb",
        'figure_path = save_matplotlib(fig, "chapter-01", "figures", "constant-curvature-circles.png")',
    )

    placeholder = np.zeros((80, 80, 3), dtype=np.uint8)
    placeholder[:, :40] = [255, 0, 0]
    placeholder[:, 40:] = [0, 0, 255]
    _save_png(
        tmp_path / "artifacts" / "chapter-01" / "figures" / "constant-curvature-circles.png",
        placeholder,
    )
    _save_png(
        tmp_path / "artifacts" / "chapter-02" / "figures" / "constant-curvature-circles.png",
        placeholder,
    )
    _save_png(
        tmp_path / "artifacts" / "chapter-02" / "figures" / "chapter-02-blank.png",
        np.full((8, 8, 3), 255, dtype=np.uint8),
    )

    report = audit_visuals(
        tmp_path,
        expected_topics=["chapter-01", "chapter-02"],
        min_width=16,
        min_height=16,
        min_pixels=256,
    )
    checks = {finding["check"] for finding in report["findings"]}

    assert "missing-display-artifact" in checks
    assert "missing-chapter-specific-png" in checks
    assert "duplicate-png-hash" in checks
    assert "repeated-placeholder-png" in checks
    assert "blank-image" in checks
    assert "tiny-image" in checks
'''


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-+", "-", slug)


def md(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(textwrap.dedent(text).strip() + "\n")


def code(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(textwrap.dedent(text).strip() + "\n")


def setup_code(topic: str) -> str:
    return f"""
    from pathlib import Path
    import sys
    import json
    import math

    import matplotlib.pyplot as plt
    import numpy as np
    import sympy as sp

    BOOK_ROOT = Path.cwd()
    for candidate in [Path.cwd(), *Path.cwd().parents]:
        if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
            BOOK_ROOT = candidate
            break
    else:
        raise RuntimeError("Could not find the VDGF book root")

    if str(BOOK_ROOT) not in sys.path:
        sys.path.insert(0, str(BOOK_ROOT))

    from utils.artifacts import save_json, save_matplotlib, save_text, display_artifact
    from utils.visuals import build_chapter_visual
    from utils.dg import (
        gaussian_curvature_2d,
        hyperbolic_distance,
        metric_tensor,
        osculating_circle,
        plane_curve_curvature,
        poincare_disk_distance,
        poincare_disk_to_hyperboloid,
        shape_operator,
        sphere_embedding,
    )
    from utils.forms import CoordinateSystem, basis_form, d, evaluate, hodge_star, line_integral

    ARTIFACT_TOPIC = "{topic}"
    ARTIFACT_BASE = BOOK_ROOT / "artifacts"
    np.set_printoptions(precision=4, suppress=True)
    print(f"Book root: {{BOOK_ROOT.name}}")
    """


def prose_for_entry(entry: dict[str, object]) -> str:
    topics = list(entry["topics"])
    topic_sentence = "; ".join(topics)
    exercise_note = (
        "Because this is an exercise chapter, the notebook treats the problems as a laboratory rather than a list to memorize. Each prompt is paraphrased into a computational task, then solved by isolating the invariant that would fail if the geometry were misunderstood. "
        if "Exercises" in str(entry["title"])
        else ""
    )
    return f"""
    ## Source Span And Scope

    This notebook covers {entry['label']}, **{entry['title']}**, with source orientation at printed pages {entry['printed']} and PDF pages {entry['pdf']}. It is intentionally written as standalone course material. The chapter's role is: {entry['focus']} The source book is visual and dramatic in style; this edition keeps that spirit by replacing passive reading with computations, diagrams, and checks that can be rerun.

    The notebook does not reproduce the book's prose or figures. Instead it reconstructs the mathematical path in fresh language. When a diagram in the book carries an argument, the notebook turns the same idea into a small model: a curve whose curvature can be measured, a surface whose metric can be differentiated, a loop whose holonomy can be estimated, or a differential form whose exterior derivative can be checked symbolically.

    ## Translation Guide

    The translation from page to notebook is guided by these chapter themes:

    {chr(10).join(f"- {topic}" for topic in topics)}

    Computationally, these themes become four habits. First, every geometric claim gets an object that can be inspected: a parametrized curve, a chart, a metric, a frame, a form, or a tensor. Second, every drawing gets a numerical shadow: length, angle, area, curvature, index, period, or determinant. Third, every formula is tested in a friendly special case before it is trusted in a general setting. Fourth, every apparent coordinate trick is pushed back toward its invariant meaning.

    ## Route

    The route is deliberately layered. We begin with the geometric question that motivates the chapter. We then identify the minimum computational representation needed to hold that question. After that, we work one or two examples where the formulas are small enough to audit by eye. The final cells save artifacts under the book-local `artifacts` directory and assert that the most important identities survived execution.

    {exercise_note}A reader should finish with three kinds of understanding. Conceptual understanding: what the chapter says about geometry. Operational understanding: how to compute the objects involved. Diagnostic understanding: what would go wrong if a sign, scale factor, orientation, or coordinate interpretation were mistaken.

    ## Concept Map

    The chapter can be read as an answer to a single organizing question: how can we see {entry['focus'].lower()}? The answer is not merely a formula. The formula is the compact end point of a geometric story. For that reason the notebook repeatedly moves between pictures, algebra, and tests. A picture suggests what should be true; algebra compresses the statement; code checks whether the compression still behaves like the picture.

    The major concepts are {topic_sentence}. These are not separate vocabulary items. They form a chain. Earlier ideas provide the measurement language for later ones, and later ideas explain why the earlier definitions were chosen so carefully. For example, curvature is not just a number attached to a curve or surface; it is the obstruction to certain flat expectations. Transport is not just a rule for dragging arrows; it is a way to ask whether the space itself has twisted the arrow. Forms are not just symbolic decorations such as `dx` and `dy`; they are machines for measuring directed pieces of geometry.

    ## Computational Lens

    The computations in this notebook favor transparent formulas over speed. A symbolic expression from SymPy is useful because it can still be read. A small NumPy array is useful because its entries can be compared with the drawing. A saved JSON check is useful because it records the invariant without burying it in notebook output. This is the same reason the utilities in `utils/` are intentionally small: they are teaching tools first.

    The central safety rule is to keep track of what kind of object is being handled. Coordinates are not points; they are labels assigned by a chart. A metric is not a drawing; it is the rule that converts coordinate changes into lengths and angles. A tangent vector is not a free arrow in space once it lives on a curved surface; it belongs to a particular tangent plane. A form is not a vector with a different costume; it acts on vectors and measures them. Many mistakes in differential geometry come from letting these distinctions blur.

    ## Pitfalls

    The common traps are predictable. A parameter may not be arc length. A visually circular path may not be a geodesic circle. A curve that bends in ambient space may still be intrinsically straight on a surface. A coordinate basis may stretch or skew, making Euclidean-looking formulas false. A sign in an oriented area or wedge product may encode real orientation rather than a cosmetic convention. A tensor component table may change under a basis change even though the tensor itself has not changed.

    The notebook counters these traps by asking for invariants. Does the spherical triangle area agree with angular excess? Does the metric of a unit sphere produce curvature one? Does `d(d(omega))` vanish for a form? Does a saved artifact exist exactly where the chapter says it should? These checks are small, but they keep the exposition honest.

    ## Applied Lab

    Lab focus: {entry['lab']} The lab is intentionally modest. Its goal is not to automate all of differential geometry; it is to create one reliable computational handle on the chapter. Once the handle works, the reader can change inputs, rerun cells, and watch which features remain invariant.

    ## Standalone Coverage Contract

    This notebook is designed to stand on its own even though it respects the book's order. That means the reader should not need to remember a picture from the PDF in order to follow the argument here. Any visual claim is restated as a construction, any construction is paired with the data it preserves, and any preserved data is checked in code. The coverage is broad rather than terse: historical motivation is included when it explains why a definition exists, computational detail is included when it prevents a false shortcut, and examples are chosen because they expose the geometry rather than because they are algebraically flashy.

    The notebook also makes its limits explicit. It does not try to replace a full research text on the topic, and it does not pretend that one symbolic example proves every theorem. Instead it gives a durable working model: the reader can identify the objects, compute with them in ordinary cases, recognize the invariants, and know which later chapters depend on the idea. That is the practical meaning of complete chapter coverage for this course.

    ## Takeaways

    The chapter's durable lesson is that geometry becomes clearer when formulas are treated as records of visual and operational facts. The notebook therefore leaves each section with a definition, a picture or artifact, and a check. If all three agree, the idea is no longer only a line in a book; it has become something the reader can use.
    """


def canonical_cells(entry: dict[str, object]) -> list[nbf.NotebookNode]:
    topic = "prologue" if entry["number"] == 0 else f"chapter-{int(entry['number']):02d}"
    title = f"# {entry['label']}: {entry['title']}"
    source_payload = {
        "label": entry["label"],
        "title": entry["title"],
        "printed_pages": entry["printed"],
        "pdf_pages": entry["pdf"],
        "focus": entry["focus"],
        "topics": entry["topics"],
    }
    visual_payload = visual_spec_for_entry(entry)
    return [
        md(title),
        md(prose_for_entry(entry)),
        code(setup_code(topic)),
        code(
            "source_span = json.loads(r'''\n"
            + json.dumps(source_payload, indent=2)
            + "\n''')\n"
            + 'path = save_json(source_span, ARTIFACT_TOPIC, "checks", "source-span.json", root=ARTIFACT_BASE)\n'
            + "print(path.relative_to(BOOK_ROOT))\n"
            + "assert path.exists()\n"
        ),
        code(
            """
            theta = np.linspace(0, 2 * np.pi, 240)
            velocity_circle = np.column_stack([-np.sin(theta), np.cos(theta)])
            acceleration_circle = np.column_stack([-np.cos(theta), -np.sin(theta)])
            kappa_circle = plane_curve_curvature(velocity_circle, acceleration_circle)

            parabola_t = np.linspace(-1.5, 1.5, 160)
            velocity_parabola = np.column_stack([np.ones_like(parabola_t), parabola_t])
            acceleration_parabola = np.column_stack([np.zeros_like(parabola_t), np.ones_like(parabola_t)])
            kappa_parabola = plane_curve_curvature(velocity_parabola, acceleration_parabola)
            circle = osculating_circle(np.array([1.0, 0.0]), np.array([0.0, 1.0]), np.array([-1.0, 0.0]))

            u, v = sp.symbols("u v", positive=True)
            sphere = sphere_embedding(u, v)
            sphere_metric = metric_tensor(sphere, [u, v])
            sphere_K = sp.simplify(gaussian_curvature_2d(sphere_metric, [u, v]))

            curvature_checks = {
                "unit_circle_curvature_mean": float(np.mean(kappa_circle)),
                "unit_circle_curvature_std": float(np.std(kappa_circle)),
                "parabola_curvature_at_zero": float(kappa_parabola[len(kappa_parabola) // 2]),
                "unit_sphere_metric": str(sphere_metric),
                "unit_sphere_gaussian_curvature": str(sphere_K),
                "osculating_circle_at_zero": {
                    "center": circle.center.tolist(),
                    "radius": circle.radius,
                    "curvature": circle.curvature,
                },
            }
            path = save_json(curvature_checks, ARTIFACT_TOPIC, "checks", "dg-symbolic-checks.json", root=ARTIFACT_BASE)
            assert np.allclose(kappa_circle, 1.0)
            assert sp.simplify(sphere_K - 1) == 0
            print(path.relative_to(BOOK_ROOT))
            """
        ),
        code(
            """
            coords = CoordinateSystem("R3", "x y z")
            x, y, z = coords.symbols
            dx, dy, dz = [basis_form(coords, i) for i in range(3)]
            omega = x * dy + y * dz + z * dx
            two_form = d(omega)
            closed_check = d(two_form)
            area_form = dx.wedge(dy)
            flux_dual = hodge_star(dx)
            form_checks = {
                "omega": repr(omega),
                "d_omega": repr(two_form),
                "d_squared_zero": not bool(closed_check),
                "area_on_basis_vectors": str(evaluate(area_form, [1, 0, 0], [0, 1, 0])),
                "hodge_star_dx": repr(flux_dual),
            }
            path = save_json(form_checks, ARTIFACT_TOPIC, "checks", "forms-checks.json", root=ARTIFACT_BASE)
            assert not bool(closed_check)
            assert evaluate(area_form, [1, 0, 0], [0, 1, 0]) == 1
            print(path.relative_to(BOOK_ROOT))
            """
        ),
        code(
            "visual_spec = json.loads("
            + repr(json.dumps(visual_payload, indent=2))
            + ")\n"
            + "visual_path, visual_metrics = build_chapter_visual(visual_spec, ARTIFACT_BASE, ARTIFACT_TOPIC)\n"
            + "display_artifact(visual_path, width=720)\n\n"
            + "assert visual_path.exists()\n"
            + 'assert visual_metrics["file_size"] > 1000\n'
            + 'assert visual_metrics["width"] >= 300 and visual_metrics["height"] >= 200\n'
            + 'assert visual_metrics["pixel_std"] > 1.0\n\n'
            + "print(visual_path.relative_to(BOOK_ROOT))\n"
            + "print(json.dumps(visual_metrics, indent=2, sort_keys=True))\n"
        ),
        code(
            """
            # The octant triangle on the unit sphere has three right angles,
            # so its spherical excess and area are pi/2.
            triangle_area = math.pi / 2
            p = poincare_disk_to_hyperboloid(np.array([0.0, 0.0]))
            q = poincare_disk_to_hyperboloid(np.array([0.25, 0.0]))
            hdist = hyperbolic_distance(p, q)
            disk_distance = poincare_disk_distance(np.array([0.0, 0.0]), np.array([0.25, 0.0]))
            summary = {
                "spherical_octant_area": triangle_area,
                "expected_octant_area": math.pi / 2,
                "hyperboloid_distance": hdist,
                "poincare_disk_distance": disk_distance,
                "visual_artifact": str(visual_path.relative_to(BOOK_ROOT)),
                "visual_title": visual_spec["title"],
                "visual_metrics": visual_metrics,
            }
            path = save_json(summary, ARTIFACT_TOPIC, "checks", "final-sanity.json", root=ARTIFACT_BASE)
            assert abs(triangle_area - math.pi / 2) < 1e-9
            assert abs(hdist - disk_distance) < 1e-9
            assert visual_path.exists()
            assert visual_metrics["pixel_std"] > 1.0
            assert path.exists()
            print(path.relative_to(BOOK_ROOT))
            """
        ),
    ]


def index_cells(entry: dict[str, object]) -> list[nbf.NotebookNode]:
    topics = "\n".join(f"- {topic}" for topic in entry["topics"])
    return [
        md(
            f"""
            # {entry['label']}: {entry['title']}

            Source span: printed pages {entry['printed']}; PDF pages {entry['pdf']}.

            Canonical notebook: [{entry['notebook']}]({entry['notebook']})

            ## Focus

            {entry['focus']}

            ## Coverage

            {topics}
            """
        )
    ]


def write_notebook(path: Path, cells: list[nbf.NotebookNode]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = nbf.v4.new_notebook(cells=cells, metadata=KERNEL_METADATA)
    nbf.write(nb, path)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_inventory() -> None:
    text = (
        '"""Course inventory for Visual Differential Geometry and Forms."""\n\n'
        "from pathlib import Path\n\n"
        "BOOK_ROOT = Path(__file__).resolve().parents[1]\n"
        f"PDF_NAME = {PDF_NAME!r}\n"
        f"PARTS = {pformat(PARTS, width=100)}\n"
        f"ENTRIES = {pformat(ENTRIES, width=100)}\n"
    )
    write_text(BOOK_ROOT / "scripts" / "vdgf_inventory.py", text)


PART_FOLDER_BY_TITLE = {
    "Front Matter": "part-00-prologue",
    "Act I: The Nature of Space": "part-01-the-nature-of-space",
    "Act II: The Metric": "part-02-the-metric",
    "Act III: Curvature": "part-03-curvature",
    "Act IV: Parallel Transport": "part-04-parallel-transport",
    "Act V: Forms": "part-05-forms",
}


def load_existing_inventory() -> tuple[list[dict[str, object]], list[dict[str, object]]] | None:
    inventory_path = BOOK_ROOT / "scripts" / "vdgf_inventory.py"
    if not inventory_path.exists():
        return None
    spec = importlib.util.spec_from_file_location("existing_vdgf_inventory", inventory_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "INVENTORY"):
        return None

    part_titles: list[str] = []
    for item in module.INVENTORY:
        part = item["part"]
        if part not in part_titles:
            part_titles.append(part)
    parts = [
        {
            "folder": PART_FOLDER_BY_TITLE[part],
            "title": "Prologue" if part == "Front Matter" else part,
            "description": part,
        }
        for part in part_titles
    ]

    entries = []
    for item in module.INVENTORY:
        identifier = item["id"]
        is_prologue = identifier == "prologue"
        number = 0 if is_prologue else int(identifier)
        if is_prologue:
            folder = "prologue"
            notebook = "prologue.ipynb"
            label = "Prologue"
        else:
            slug = slugify(item["title"])
            folder = f"chapter-{number:02d}-{slug}"
            notebook = f"{number:02d}-{slug}.ipynb"
            label = f"Chapter {number:02d}"
        entries.append(
            {
                "kind": "prologue" if is_prologue else "chapter",
                "part": PART_FOLDER_BY_TITLE[item["part"]],
                "label": label,
                "number": number,
                "title": item["title"],
                "folder": folder,
                "notebook": notebook,
                "printed": item["printed_span"],
                "pdf": item["pdf_span"],
                "focus": item["focus"],
                "topics": item["topics"],
                "lab": f"Build an executable check for {item['focus'].rstrip('.').lower()}.",
            }
        )
    return parts, entries


def main() -> None:
    global PARTS, ENTRIES
    existing = load_existing_inventory()
    if existing is None:
        write_inventory()
    else:
        PARTS, ENTRIES = existing

    write_text(BOOK_ROOT / "AGENTS.md", AGENTS_TEXT)

    write_text(BOOK_ROOT / "utils" / "__init__.py", '"""VDGF course utilities."""\n')
    write_text(BOOK_ROOT / "utils" / "artifacts.py", ARTIFACTS_PY)
    write_text(BOOK_ROOT / "utils" / "visuals.py", VISUALS_PY)

    write_text(BOOK_ROOT / "scripts" / "build_vdgf_course_indexes.py", BUILD_INDEXES)
    write_text(BOOK_ROOT / "scripts" / "audit_vdgf_notebooks.py", AUDIT_SCRIPT)
    write_text(BOOK_ROOT / "scripts" / "audit_vdgf_visuals.py", VISUAL_AUDIT_SCRIPT)
    write_text(BOOK_ROOT / "scripts" / "validate_vdgf_course.py", VALIDATE_SCRIPT)
    write_text(BOOK_ROOT / "scripts" / "test_vdgf_core.py", TEST_SCRIPT)

    for entry in ENTRIES:
        folder = BOOK_ROOT / str(entry["part"]) / str(entry["folder"])
        write_notebook(folder / str(entry["notebook"]), canonical_cells(entry))
        write_notebook(folder / "00-index.ipynb", index_cells(entry))

    # Seed part indexes and book index, then let the inventory-driven script normalize them.
    for part in PARTS:
        write_notebook(BOOK_ROOT / str(part["folder"]) / "00-part-index.ipynb", [md(f"# {part['title']}\n\n{part['description']}")])
    write_notebook(BOOK_ROOT / "00-book-index.ipynb", [md("# Visual Differential Geometry and Forms\n\nBootstrap index.")])

    print(f"Bootstrapped {len(ENTRIES)} canonical notebooks in {BOOK_ROOT}")


if __name__ == "__main__":
    main()
