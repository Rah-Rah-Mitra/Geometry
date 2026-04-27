"""Chapter metadata inventory for Visual Differential Geometry and Forms.

The PDF spans are 1-based physical PDF pages. Printed spans use the page
labels in the book. Content-only spans omit blank pages and act-divider pages.
"""

from __future__ import annotations

import argparse
import json
from typing import Any


PDF_SOURCE = "Visual Differential Geometry and Forms.pdf"

SOURCE_SPAN_NOTES = [
    "Front matter uses roman printed pages; Prologue is printed xvii-xxiii on PDF pages 18-24.",
    "Arabic printed pages map to physical PDF pages by adding 29.",
    "Blank pages and act-divider pages are excluded from chapter spans.",
    "Corrected exercise-chapter spans: ch. 3 is 24-28, ch. 7 is 83-93, ch. 20 is 219-227, ch. 31 is 334-341.",
    "Ch. 39 ends at printed page 474 / PDF page 503; Further Reading starts at printed page 475 / PDF page 504.",
]

INVENTORY: list[dict[str, Any]] = [
    {
        "id": "prologue",
        "part": "Front Matter",
        "title": "Prologue",
        "printed_span": "xvii-xxiii",
        "pdf_span": "18-24",
        "focus": "Frames the book as a geometric alternative to unilluminating symbolic calculation and explains the five-act structure.",
        "topics": [
            "Newtonian ultimate equality and geometric limiting arguments",
            "The author's notation and stance on rigor",
            "A critique of opaque algebraic calculation",
            "The five-act dramatic organization of the book",
            "Why Global Gauss-Bonnet, Riemann curvature, relativity, and Forms are central",
            "Housekeeping conventions for equations, figures, framed results, and exercises",
        ],
    },
    {
        "id": 1,
        "part": "Act I: The Nature of Space",
        "title": "Euclidean and Non-Euclidean Geometry",
        "printed_span": "3-16",
        "pdf_span": "32-45",
        "focus": "Introduces intrinsic geometry by contrasting Euclidean, spherical, and hyperbolic behavior through geodesics and angular excess.",
        "topics": [
            "Euclid's parallel axiom and its geometric consequences",
            "Hyperbolic geometry as a coherent alternative to Euclidean geometry",
            "Spherical great circles as straightest paths",
            "Angular excess of spherical triangles",
            "Intrinsic versus extrinsic viewpoints on curved surfaces",
            "Geodesics as shortest and locally straight paths",
            "Sticky-tape and string constructions for physical intuition",
        ],
    },
    {
        "id": 2,
        "part": "Act I: The Nature of Space",
        "title": "Gaussian Curvature",
        "printed_span": "17-23",
        "pdf_span": "46-52",
        "focus": "Motivates Gaussian curvature as the local quantity detected by circles, triangles, and the local Gauss-Bonnet theorem.",
        "topics": [
            "Curvature as an intrinsic measurement",
            "Circle circumference and area deviations from Euclidean formulas",
            "Positive, zero, and negative local curvature signatures",
            "Angular excess as total curvature in small regions",
            "Local Gauss-Bonnet for geodesic triangles",
            "Curvature density as a bridge from local geometry to integral formulas",
        ],
    },
    {
        "id": 3,
        "part": "Act I: The Nature of Space",
        "title": "Exercises for Prologue and Act I",
        "printed_span": "24-28",
        "pdf_span": "53-57",
        "focus": "Practice set reinforcing ultimate equality, non-Euclidean geometry, and first curvature measurements.",
        "topics": [
            "Newtonian ultimate-equality calculations",
            "Pythagorean triples and Euclidean geometry",
            "Spherical triangle and tessellation exercises",
            "Geodesic construction experiments on surfaces",
            "Estimating Gaussian curvature from intrinsic data",
            "Comparisons of angular excess across surfaces",
        ],
    },
    {
        "id": 4,
        "part": "Act II: The Metric",
        "title": "Mapping Surfaces: The Metric",
        "printed_span": "31-50",
        "pdf_span": "60-79",
        "focus": "Develops the metric as the intrinsic data preserved or distorted by maps, with stereographic projection as the main example.",
        "topics": [
            "Projective maps from the sphere",
            "Metrics for general parametrized surfaces",
            "Metric curvature formula as a preview of intrinsic computation",
            "Conformal maps and angle preservation",
            "Visual complex-analysis intuition",
            "Stereographic projection of the sphere",
            "Circle preservation and explicit stereographic formulas",
        ],
    },
    {
        "id": 5,
        "part": "Act II: The Metric",
        "title": "The Pseudosphere and the Hyperbolic Plane",
        "printed_span": "51-64",
        "pdf_span": "80-93",
        "focus": "Uses the pseudosphere to connect tractrix geometry, constant negative curvature, and the Poincare models of hyperbolic geometry.",
        "topics": [
            "Beltrami's realization of hyperbolic geometry",
            "The tractrix and construction of the pseudosphere",
            "Conformal coordinates on the pseudosphere",
            "The Beltrami-Poincare half-plane",
            "Optical interpretation of hyperbolic geodesics",
            "Angle of parallelism in hyperbolic geometry",
            "The Beltrami-Poincare disc model",
        ],
    },
    {
        "id": 6,
        "part": "Act II: The Metric",
        "title": "Isometries and Complex Numbers",
        "printed_span": "65-82",
        "pdf_span": "94-111",
        "focus": "Describes isometries of hyperbolic geometry using Mobius transformations and links the metric story to spacetime geometry.",
        "topics": [
            "Metric-preserving transformations",
            "Mobius transformations as complex maps",
            "Classification and action of hyperbolic isometries",
            "The main isometry result for the Poincare models",
            "Special relativity and spacetime metric geometry",
            "Three-dimensional hyperbolic geometry",
            "Complex-number methods as geometric notation",
        ],
    },
    {
        "id": 7,
        "part": "Act II: The Metric",
        "title": "Exercises for Act II",
        "printed_span": "83-93",
        "pdf_span": "112-122",
        "focus": "Practice set on metrics, conformal maps, pseudospherical models, Mobius maps, and spacetime geometry.",
        "topics": [
            "Metric derivations for mapped surfaces",
            "Stereographic and conformal-map calculations",
            "Pseudosphere and hyperbolic-plane constructions",
            "Geodesics in half-plane and disc models",
            "Mobius transformation algebra",
            "Lorentz and spacetime metric exercises",
            "Three-dimensional hyperbolic examples",
        ],
    },
    {
        "id": 8,
        "part": "Act III: Curvature",
        "title": "Curvature of Plane Curves",
        "printed_span": "97-105",
        "pdf_span": "126-134",
        "focus": "Builds plane-curve curvature from physical, geometric, and infinitesimal viewpoints.",
        "topics": [
            "Curvature as force needed to bend motion",
            "The circle of curvature",
            "Newton's curvature formula",
            "Curvature as rate of tangent turning",
            "Arc-length parametrization and unit tangent motion",
            "The tractrix as a worked example",
        ],
    },
    {
        "id": 9,
        "part": "Act III: Curvature",
        "title": "Curves in 3-Space",
        "printed_span": "106-108",
        "pdf_span": "135-137",
        "focus": "Extends curve curvature to space curves through osculating planes, torsion, and the Frenet-Serret frame.",
        "topics": [
            "Osculating plane of a twisting curve",
            "Torsion as rotation of the osculating plane",
            "Tangent, normal, and binormal vectors",
            "Curvature vector for unit-speed motion",
            "Physical straw-and-wire model of the Frenet frame",
            "Frenet-Serret equations as frame rotation",
        ],
    },
    {
        "id": 10,
        "part": "Act III: Curvature",
        "title": "The Principal Curvatures of a Surface",
        "printed_span": "109-114",
        "pdf_span": "138-143",
        "focus": "Introduces normal curvature of surfaces and the principal curvatures that organize all directional curvatures.",
        "topics": [
            "Normal sections through a surface point",
            "Euler's curvature formula",
            "Principal directions and extremal curvatures",
            "Proof strategy for Euler's formula",
            "Curvature behavior on surfaces of revolution",
            "Mean and Gaussian curvature as products and averages",
        ],
    },
    {
        "id": 11,
        "part": "Act III: Curvature",
        "title": "Geodesics and Geodesic Curvature",
        "printed_span": "115-129",
        "pdf_span": "144-158",
        "focus": "Separates normal and geodesic curvature and develops geodesics on surfaces of revolution through Clairaut and Kepler analogies.",
        "topics": [
            "Geodesic curvature versus normal curvature",
            "Meusnier's theorem",
            "Geodesics as intrinsically straight curves",
            "Intrinsic and extrinsic measurements of geodesic curvature",
            "Sticky-tape construction revisited",
            "Clairaut's theorem on surfaces of revolution",
            "Kepler's second law and hyperbolic geodesics",
        ],
    },
    {
        "id": 12,
        "part": "Act III: Curvature",
        "title": "The Extrinsic Curvature of a Surface",
        "printed_span": "130-137",
        "pdf_span": "159-166",
        "focus": "Defines extrinsic curvature through the spherical map and explores the local shapes permitted by principal curvature signs.",
        "topics": [
            "The Gauss or spherical map",
            "Area distortion under the spherical map",
            "Extrinsic curvature as product of principal curvatures",
            "Elliptic, hyperbolic, parabolic, and planar points",
            "Possible local surface shapes",
            "Relation between sign of curvature and surface bending",
        ],
    },
    {
        "id": 13,
        "part": "Act III: Curvature",
        "title": "Gauss's Theorema Egregium",
        "printed_span": "138-142",
        "pdf_span": "167-171",
        "focus": "States and motivates Gauss's discovery that Gaussian curvature is intrinsic despite being defined extrinsically.",
        "topics": [
            "Gauss's 1816 beautiful theorem",
            "Gauss's 1827 Theorema Egregium",
            "Intrinsic invariance of Gaussian curvature",
            "Curvature preserved by bending without stretching",
            "Consequences for maps and surface deformation",
            "Historical importance of the theorem",
        ],
    },
    {
        "id": 14,
        "part": "Act III: Curvature",
        "title": "The Curvature of a Spike",
        "printed_span": "143-148",
        "pdf_span": "172-177",
        "focus": "Uses conical and polyhedral spikes to make curvature concentration and intrinsic/extrinsic agreement visible.",
        "topics": [
            "Curvature concentrated at a conical tip",
            "Angular defect and excess for spikes",
            "Intrinsic measurement of polyhedral curvature",
            "Extrinsic curvature through spherical images",
            "Polyhedral version of the Theorema Egregium",
            "Discrete models for smooth curvature ideas",
        ],
    },
    {
        "id": 15,
        "part": "Act III: Curvature",
        "title": "The Shape Operator",
        "printed_span": "149-164",
        "pdf_span": "178-193",
        "focus": "Packages surface bending into the shape operator and connects its matrix, eigenstructure, and classical fundamental forms.",
        "topics": [
            "Directional derivatives of vector fields",
            "Definition of the shape operator",
            "Geometric action of the operator on tangent vectors",
            "Singular value decomposition and transpose detour",
            "Matrix representation of the shape operator",
            "Principal curvatures and asymptotic directions",
            "First, second, and third fundamental forms",
        ],
    },
    {
        "id": 16,
        "part": "Act III: Curvature",
        "title": "Introduction to the Global Gauss-Bonnet Theorem",
        "printed_span": "165-174",
        "pdf_span": "194-203",
        "focus": "Introduces the global Gauss-Bonnet theorem by linking total curvature to topology and Euler characteristic.",
        "topics": [
            "Basic topology and statement of the theorem",
            "Total curvature of spheres and tori",
            "Genus and surface classification intuition",
            "Pancake, bagel, and bridge visualizations",
            "Topological degree of the spherical map",
            "Historical framing of the theorem",
        ],
    },
    {
        "id": 17,
        "part": "Act III: Curvature",
        "title": "First (Heuristic) Proof of the Global Gauss-Bonnet Theorem",
        "printed_span": "175-182",
        "pdf_span": "204-211",
        "focus": "Gives a first visual proof through total curvature of loops and deformed surfaces.",
        "topics": [
            "Hopf's Umlaufsatz for plane loops",
            "Total curvature of deformed circles",
            "Heuristic proof of the turning theorem",
            "Total curvature of a deformed sphere",
            "Heuristic global Gauss-Bonnet argument",
            "How local turning data becomes global topology",
        ],
    },
    {
        "id": 18,
        "part": "Act III: Curvature",
        "title": "Second (Angular Excess) Proof of the Global Gauss-Bonnet Theorem",
        "printed_span": "183-194",
        "pdf_span": "212-223",
        "focus": "Proves global Gauss-Bonnet through triangulations, Euler characteristic, and angular excess bookkeeping.",
        "topics": [
            "Euler characteristic as V - E + F",
            "Euler's polyhedral formula",
            "Cauchy's proof by flattening polyhedra",
            "Polygonal nets and their Euler characteristic",
            "Legendre's proof of the polyhedral formula",
            "Adding handles and changing genus",
            "Angular-excess proof of global Gauss-Bonnet",
        ],
    },
    {
        "id": 19,
        "part": "Act III: Curvature",
        "title": "Third (Vector Field) Proof of the Global Gauss-Bonnet Theorem",
        "printed_span": "195-218",
        "pdf_span": "224-247",
        "focus": "Derives global Gauss-Bonnet from vector-field indices, Poincare-Hopf, and the geometry of singularities.",
        "topics": [
            "Vector fields in the plane",
            "Index of an isolated singular point",
            "Complex powers as archetypal singularities",
            "Vector fields on surfaces and honey-flow intuition",
            "Topographic maps and surface index",
            "Poincare-Hopf theorem and applications",
            "Vector-field proof of global Gauss-Bonnet",
            "Transition toward parallel transport",
        ],
    },
    {
        "id": 20,
        "part": "Act III: Curvature",
        "title": "Exercises for Act III",
        "printed_span": "219-227",
        "pdf_span": "248-256",
        "focus": "Practice set on curve curvature, surface curvature, shape operators, Gauss-Bonnet, and vector-field topology.",
        "topics": [
            "Plane-curve curvature computations",
            "Frenet-frame and torsion exercises",
            "Principal, normal, and geodesic curvature problems",
            "Shape-operator and fundamental-form calculations",
            "Theorema Egregium and spike-curvature examples",
            "Global Gauss-Bonnet and Euler characteristic",
            "Vector-field index and Poincare-Hopf exercises",
        ],
    },
    {
        "id": 21,
        "part": "Act IV: Parallel Transport",
        "title": "An Historical Puzzle",
        "printed_span": "231-232",
        "pdf_span": "260-261",
        "focus": "Motivates parallel transport through the historical gap between Einstein's 1915 field equation and Levi-Civita's 1917 concept.",
        "topics": [
            "Parallel transport as a late foundational concept",
            "Einstein's reconciliation of gravity and relativity",
            "Tensor calculus as the available 1915 tool",
            "Gravity as curvature of spacetime",
            "Experimental confirmation of general relativity",
            "Why a geometric interpretation needs parallel transport",
        ],
    },
    {
        "id": 22,
        "part": "Act IV: Parallel Transport",
        "title": "Extrinsic Constructions",
        "printed_span": "233-239",
        "pdf_span": "262-268",
        "focus": "Builds parallel transport extrinsically by projecting motion into the surface and by physical transport analogies.",
        "topics": [
            "Projecting vectors back into the tangent surface",
            "Transport along curves embedded in space",
            "Geodesics as curves with self-parallel tangents",
            "Parallel transport along geodesics",
            "Potato-peeler transport model",
            "Extrinsic intuition for a later intrinsic definition",
        ],
    },
    {
        "id": 23,
        "part": "Act IV: Parallel Transport",
        "title": "Intrinsic Constructions",
        "printed_span": "240-244",
        "pdf_span": "269-273",
        "focus": "Recasts parallel transport intrinsically using geodesic constructions and the covariant derivative.",
        "topics": [
            "Parallel transport via infinitesimal geodesic moves",
            "Intrinsic construction without ambient space",
            "The covariant derivative as intrinsic change",
            "Comparison with ordinary derivatives",
            "How transported vectors remain tangent",
            "Preparation for holonomy and curvature",
        ],
    },
    {
        "id": 24,
        "part": "Act IV: Parallel Transport",
        "title": "Holonomy",
        "printed_span": "245-251",
        "pdf_span": "274-280",
        "focus": "Shows that curvature can be detected by the angle picked up when vectors are parallel transported around loops.",
        "topics": [
            "Holonomy on the sphere",
            "Geodesic triangles and angular excess",
            "Holonomy of general geodesic triangles",
            "Additivity of holonomy over regions",
            "Hyperbolic-plane examples",
            "Curvature as infinitesimal rotational failure",
        ],
    },
    {
        "id": 25,
        "part": "Act IV: Parallel Transport",
        "title": "An Intuitive Geometric Proof of the Theorema Egregium",
        "printed_span": "252-256",
        "pdf_span": "281-285",
        "focus": "Explains the Theorema Egregium through the way the spherical map preserves parallel transport and holonomy.",
        "topics": [
            "Recap of curvature and spherical-map notation",
            "Story of the preceding curvature constructions",
            "Parallel transport under the spherical map",
            "Gauss's beautiful theorem revisited",
            "Intrinsic explanation of the Theorema Egregium",
            "Holonomy as the bridge between extrinsic and intrinsic curvature",
        ],
    },
    {
        "id": 26,
        "part": "Act IV: Parallel Transport",
        "title": "Fourth (Holonomy) Proof of the Global Gauss-Bonnet Theorem",
        "printed_span": "257-260",
        "pdf_span": "286-289",
        "focus": "Uses holonomy to give an intrinsic proof of global Gauss-Bonnet.",
        "topics": [
            "Holonomy as accumulated curvature",
            "The issue of open-curve holonomy",
            "Closing curves by comparing endpoints",
            "Hopf's intrinsic proof strategy",
            "Global Gauss-Bonnet without extrinsic spherical maps",
            "Parallel transport as the organizing mechanism",
        ],
    },
    {
        "id": 27,
        "part": "Act IV: Parallel Transport",
        "title": "Geometric Proof of the Metric Curvature Formula",
        "printed_span": "261-268",
        "pdf_span": "290-297",
        "focus": "Proves the metric curvature formula geometrically by interpreting holonomy as circulation in a map.",
        "topics": [
            "Circulation of vector fields around loops",
            "Flat-plane holonomy as a dry run",
            "Metric-induced vector fields in coordinate maps",
            "Holonomy as circulation",
            "Geometric derivation of the curvature formula",
            "Why the metric alone determines curvature",
        ],
    },
    {
        "id": 28,
        "part": "Act IV: Parallel Transport",
        "title": "Curvature as a Force between Neighbouring Geodesics",
        "printed_span": "269-279",
        "pdf_span": "298-308",
        "focus": "Interprets curvature dynamically through geodesic deviation and the Jacobi equation.",
        "topics": [
            "Jacobi equation for nearby geodesics",
            "Zero curvature and parallel behavior in the plane",
            "Positive curvature and convergence on the sphere",
            "Negative curvature and divergence on the pseudosphere",
            "Geodesic polar coordinate proof",
            "Relative acceleration as velocity holonomy",
            "Small geodesic-circle circumference and area",
        ],
    },
    {
        "id": 29,
        "part": "Act IV: Parallel Transport",
        "title": "Riemann's Curvature",
        "printed_span": "280-306",
        "pdf_span": "309-335",
        "focus": "Generalizes surface curvature to n-manifolds through parallel transport, the Riemann tensor, sectional curvature, Jacobi fields, and Ricci curvature.",
        "topics": [
            "Angular excess in higher-dimensional manifolds",
            "Three constructions of parallel transport",
            "Covariant derivative in n-manifolds",
            "Riemann curvature tensor from small-loop holonomy",
            "Components, symmetries, and sectional curvatures",
            "Jacobi equation in n-manifolds",
            "Ricci tensor and volume/area acceleration",
            "Historical notes and geometric interpretation",
        ],
    },
    {
        "id": 30,
        "part": "Act IV: Parallel Transport",
        "title": "Einstein's Curved Spacetime",
        "printed_span": "307-333",
        "pdf_span": "336-362",
        "focus": "Gives a geometric introduction to general relativity as curvature of spacetime caused by matter and energy.",
        "topics": [
            "Equivalence-principle motivation",
            "Gravitational tidal forces",
            "Newtonian gravity in geometric form",
            "Spacetime metric and diagrams",
            "Einstein vacuum field equation",
            "Schwarzschild solution and early tests",
            "Gravitational waves",
            "Matter field equation, black holes, and cosmology",
        ],
    },
    {
        "id": 31,
        "part": "Act IV: Parallel Transport",
        "title": "Exercises for Act IV",
        "printed_span": "334-341",
        "pdf_span": "363-370",
        "focus": "Practice set on parallel transport, holonomy, curvature formulas, Jacobi fields, Riemann curvature, and relativity.",
        "topics": [
            "Extrinsic and intrinsic parallel-transport constructions",
            "General local Gauss-Bonnet exercises",
            "Holonomy and curvature computations",
            "Metric curvature formula derivations",
            "Jacobi equation and geodesic deviation",
            "Riemann tensor identities and symmetries",
            "Einstein tensor and relativity applications",
        ],
    },
    {
        "id": 32,
        "part": "Act V: Forms",
        "title": "1-Forms",
        "printed_span": "345-359",
        "pdf_span": "374-388",
        "focus": "Introduces 1-forms as covectors that measure vectors, with geometric examples from work, gradients, and basis forms.",
        "topics": [
            "Definition and visualization of a 1-form",
            "Gravitational work as a 1-form",
            "Topographic maps and gradient 1-forms",
            "Row vectors and Dirac bras",
            "Basis 1-forms and components",
            "The differential df as a 1-form",
            "Geometric addition of 1-forms",
        ],
    },
    {
        "id": 33,
        "part": "Act V: Forms",
        "title": "Tensors",
        "printed_span": "360-369",
        "pdf_span": "389-398",
        "focus": "Develops tensors by valence, components, tensor products, contractions, metric duality, and symmetry.",
        "topics": [
            "Tensor definition by input valence",
            "Linear algebra as tensor examples",
            "Addition and tensor products",
            "Component notation",
            "Metric tensor and line element",
            "Contraction operations",
            "Raising/lowering valence with the metric",
            "Symmetric and antisymmetric tensors",
        ],
    },
    {
        "id": 34,
        "part": "Act V: Forms",
        "title": "2-Forms",
        "printed_span": "370-385",
        "pdf_span": "399-414",
        "focus": "Builds 2-forms as oriented area-measuring objects and relates them to wedge products, flux, and electromagnetic forms.",
        "topics": [
            "Definition of 2-forms and p-forms",
            "Area 2-form as core example",
            "Wedge product of 1-forms",
            "Polar-coordinate area form",
            "Basis 2-forms and projection areas",
            "Flux forms in three dimensions",
            "Vector product versus wedge product",
            "Faraday and Maxwell electromagnetic 2-forms",
        ],
    },
    {
        "id": 35,
        "part": "Act V: Forms",
        "title": "3-Forms",
        "printed_span": "386-391",
        "pdf_span": "415-420",
        "focus": "Extends wedge products to volume-measuring 3-forms and clarifies dimension-dependent behavior.",
        "topics": [
            "Why 3-forms require three dimensions",
            "Wedge product of 2-forms and 1-forms",
            "Volume 3-form",
            "Spherical polar coordinate volume form",
            "Wedge products of multiple 1-forms",
            "Basis 3-forms",
            "Whether a form can wedge nontrivially with itself",
        ],
    },
    {
        "id": 36,
        "part": "Act V: Forms",
        "title": "Differentiation",
        "printed_span": "392-403",
        "pdf_span": "421-432",
        "focus": "Introduces the exterior derivative and shows how it unifies differential operations in vector calculus and physics.",
        "topics": [
            "Exterior derivative of 1-forms",
            "Exterior derivative of 2-forms and p-forms",
            "Leibniz rule for forms",
            "Closed and exact forms",
            "The fundamental identity d squared equals zero",
            "Cauchy-Riemann equations via forms",
            "Gradient, curl, and divergence in form language",
            "Maxwell's equations",
        ],
    },
    {
        "id": 37,
        "part": "Act V: Forms",
        "title": "Integration",
        "printed_span": "404-429",
        "pdf_span": "433-458",
        "focus": "Develops integration of forms and the generalized Stokes theorem, then connects it to vector calculus, complex analysis, and de Rham cohomology.",
        "topics": [
            "Line integrals of 1-forms",
            "Work, circulation, and path independence",
            "Exact forms and potentials",
            "Exterior derivative as infinitesimal integral",
            "Fundamental theorem of exterior calculus",
            "Classical Green, Gauss, and Stokes theorems",
            "Cauchy's theorem and Poincare lemma",
            "Primer on de Rham cohomology",
        ],
    },
    {
        "id": 38,
        "part": "Act V: Forms",
        "title": "Differential Geometry via Forms",
        "printed_span": "430-464",
        "pdf_span": "459-493",
        "focus": "Applies Cartan's exterior calculus to differential geometry, recovering curvature formulas and extending them to n-manifolds and Schwarzschild spacetime.",
        "topics": [
            "Cartan's method of moving frames",
            "Connection 1-forms and attitude matrices",
            "Cartan's two structural equations",
            "Six fundamental form equations of a surface",
            "Geometric meanings of symmetry and Gauss equations",
            "Metric curvature formula and Theorema Egregium via forms",
            "Hilbert and Liebmann rigidity results",
            "Curvature 2-forms, Bianchi identities, and Schwarzschild curvature",
        ],
    },
    {
        "id": 39,
        "part": "Act V: Forms",
        "title": "Exercises for Act V",
        "printed_span": "465-474",
        "pdf_span": "494-503",
        "focus": "Practice set on forms, tensors, exterior calculus, integration theorems, cohomology, and Cartan's geometric machinery.",
        "topics": [
            "1-form and basis-form exercises",
            "Tensor product, contraction, and metric-duality problems",
            "2-form, 3-form, wedge, and Hodge-style computations",
            "Exterior derivative and vector-calculus identities",
            "Maxwell and conservation-law applications",
            "Integration, closed/exact forms, and cohomology",
            "Moving frames, curvature forms, and Schwarzschild exercises",
        ],
    },
]


def _span_start(span: str) -> int:
    """Return the numeric start of an Arabic or PDF span."""
    return int(span.split("-", 1)[0])


def validate_inventory() -> None:
    """Validate the hand-curated metadata for shape and simple span consistency."""
    expected_ids = ["prologue", *range(1, 40)]
    actual_ids = [entry["id"] for entry in INVENTORY]
    if actual_ids != expected_ids:
        raise ValueError(f"Unexpected chapter ids: {actual_ids!r}")

    for entry in INVENTORY:
        topic_count = len(entry["topics"])
        if not 5 <= topic_count <= 8:
            raise ValueError(f"{entry['id']} has {topic_count} topic bullets")
        if not entry["focus"].endswith("."):
            raise ValueError(f"{entry['id']} focus should be a sentence")

    for entry in INVENTORY[1:]:
        printed_start = _span_start(entry["printed_span"])
        pdf_start = _span_start(entry["pdf_span"])
        if pdf_start - printed_start != 29:
            raise ValueError(f"{entry['id']} violates Arabic printed-to-PDF offset")


def to_markdown() -> str:
    """Render the inventory as concise Markdown."""
    lines = [
        "# VDGF Chapter Metadata Inventory",
        "",
        f"Source: `{PDF_SOURCE}`",
        "",
        "## Source Span Notes",
        "",
    ]
    lines.extend(f"- {note}" for note in SOURCE_SPAN_NOTES)
    lines.extend(["", "## Chapters", ""])

    for entry in INVENTORY:
        lines.append(f"### {entry['id']}. {entry['title']}")
        lines.append(f"- Part: {entry['part']}")
        lines.append(f"- Printed span: {entry['printed_span']}")
        lines.append(f"- PDF span: {entry['pdf_span']}")
        lines.append(f"- Focus: {entry['focus']}")
        lines.append("- Topics:")
        lines.extend(f"  - {topic}" for topic in entry["topics"])
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    parser.add_argument("--check", action="store_true", help="Validate inventory metadata and exit.")
    args = parser.parse_args()

    validate_inventory()

    if args.check:
        print(f"ok: {len(INVENTORY)} entries")
        return

    if args.json:
        print(json.dumps({"source": PDF_SOURCE, "source_span_notes": SOURCE_SPAN_NOTES, "chapters": INVENTORY}, indent=2))
        return

    print(to_markdown(), end="")


if __name__ == "__main__":
    main()
