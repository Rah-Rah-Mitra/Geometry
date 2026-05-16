"""Source map for the A Course in Metric Geometry notebook course."""

from __future__ import annotations

from typing import Any

BOOK_TITLE = "A Course in Metric Geometry"
BOOK_AUTHORS = ["Dmitri Burago", "Yuri Burago", "Sergei Ivanov"]
PDF_FILENAME = "A Course in Metric Geometry.pdf"
PRINTED_TO_PDF_OFFSET = 15


COURSE_MAP: list[dict[str, Any]] = [
    {
        "number": 1,
        "title": "Metric Spaces",
        "slug": "metric-spaces",
        "folder": "chapter-01-metric-spaces",
        "notebook": "01-metric-spaces.ipynb",
        "printed": "1-24",
        "pdf": "16-39",
        "focus": "Metric axioms, examples, topology, Lipschitz maps, completeness, compactness, and Hausdorff dimension.",
        "sections": [
            {"number": "1.1", "title": "Definitions", "printed_start": 1, "pdf_start": 16},
            {"number": "1.2", "title": "Examples", "printed_start": 3, "pdf_start": 18},
            {"number": "1.3", "title": "Metrics and Topology", "printed_start": 7, "pdf_start": 22},
            {"number": "1.4", "title": "Lipschitz Maps", "printed_start": 9, "pdf_start": 24},
            {"number": "1.5", "title": "Complete Spaces", "printed_start": 10, "pdf_start": 25},
            {"number": "1.6", "title": "Compact Spaces", "printed_start": 13, "pdf_start": 28},
            {"number": "1.7", "title": "Hausdorff Measure and Dimension", "printed_start": 17, "pdf_start": 32},
        ],
    },
    {
        "number": 2,
        "title": "Length Spaces",
        "slug": "length-spaces",
        "folder": "chapter-02-length-spaces",
        "notebook": "02-length-spaces.ipynb",
        "printed": "25-58",
        "pdf": "40-73",
        "focus": "Length structures, induced intrinsic metrics, shortest paths, length measure, and speed.",
        "sections": [
            {"number": "2.1", "title": "Length Structures", "printed_start": 25, "pdf_start": 40},
            {"number": "2.2", "title": "First Examples of Length Structures", "printed_start": 30, "pdf_start": 45},
            {"number": "2.3", "title": "Length Structures Induced by Metrics", "printed_start": 33, "pdf_start": 48},
            {"number": "2.4", "title": "Characterization of Intrinsic Metrics", "printed_start": 38, "pdf_start": 53},
            {"number": "2.5", "title": "Shortest Paths", "printed_start": 43, "pdf_start": 58},
            {"number": "2.6", "title": "Length and Hausdorff Measure", "printed_start": 53, "pdf_start": 68},
            {"number": "2.7", "title": "Length and Lipschitz Speed", "printed_start": 54, "pdf_start": 69},
        ],
    },
    {
        "number": 3,
        "title": "Constructions",
        "slug": "constructions",
        "folder": "chapter-03-constructions",
        "notebook": "03-constructions.ipynb",
        "printed": "59-100",
        "pdf": "74-115",
        "focus": "Gluing, maximal metrics, polyhedral spaces, quotients, coverings, arcwise isometries, products, and cones.",
        "sections": [
            {"number": "3.1", "title": "Locality, Gluing and Maximal Metrics", "printed_start": 59, "pdf_start": 74},
            {"number": "3.2", "title": "Polyhedral Spaces", "printed_start": 67, "pdf_start": 82},
            {"number": "3.3", "title": "Isometries and Quotients", "printed_start": 75, "pdf_start": 90},
            {"number": "3.4", "title": "Local Isometries and Coverings", "printed_start": 78, "pdf_start": 93},
            {"number": "3.5", "title": "Arcwise Isometries", "printed_start": 86, "pdf_start": 101},
            {"number": "3.6", "title": "Products and Cones", "printed_start": 88, "pdf_start": 103},
        ],
    },
    {
        "number": 4,
        "title": "Spaces of Bounded Curvature",
        "slug": "spaces-of-bounded-curvature",
        "folder": "chapter-04-spaces-of-bounded-curvature",
        "notebook": "04-spaces-of-bounded-curvature.ipynb",
        "printed": "101-134",
        "pdf": "116-149",
        "focus": "Alexandrov-style bounded curvature definitions, examples, angles, distance functions, first variation, globalization, and cones.",
        "sections": [
            {"number": "4.1", "title": "Definitions", "printed_start": 101, "pdf_start": 116},
            {"number": "4.2", "title": "Examples", "printed_start": 109, "pdf_start": 124},
            {"number": "4.3", "title": "Angles in Alexandrov Spaces and Equivalence of Definitions", "printed_start": 114, "pdf_start": 129},
            {"number": "4.4", "title": "Analysis of Distance Functions", "printed_start": 119, "pdf_start": 134},
            {"number": "4.5", "title": "The First Variation Formula", "printed_start": 121, "pdf_start": 136},
            {"number": "4.6", "title": "Nonzero Curvature Bounds and Globalization", "printed_start": 126, "pdf_start": 141},
            {"number": "4.7", "title": "Curvature of Cones", "printed_start": 131, "pdf_start": 146},
        ],
    },
    {
        "number": 5,
        "title": "Smooth Length Structures",
        "slug": "smooth-length-structures",
        "folder": "chapter-05-smooth-length-structures",
        "notebook": "05-smooth-length-structures.ipynb",
        "printed": "135-208",
        "pdf": "150-223",
        "focus": "Riemannian length, exponential maps, the hyperbolic plane, sub-Riemannian structures, volumes, and Besikovitch inequality.",
        "sections": [
            {"number": "5.1", "title": "Riemannian Length Structures", "printed_start": 136, "pdf_start": 151},
            {"number": "5.2", "title": "Exponential Map", "printed_start": 150, "pdf_start": 165},
            {"number": "5.3", "title": "Hyperbolic Plane", "printed_start": 154, "pdf_start": 169},
            {"number": "5.4", "title": "Sub-Riemannian Metric Structures", "printed_start": 178, "pdf_start": 193},
            {"number": "5.5", "title": "Riemannian and Finsler Volumes", "printed_start": 192, "pdf_start": 207},
            {"number": "5.6", "title": "Besikovitch Inequality", "printed_start": 201, "pdf_start": 216},
        ],
    },
    {
        "number": 6,
        "title": "Curvature of Riemannian Metrics",
        "slug": "curvature-of-riemannian-metrics",
        "folder": "chapter-06-curvature-of-riemannian-metrics",
        "notebook": "06-curvature-of-riemannian-metrics.ipynb",
        "printed": "209-240",
        "pdf": "224-255",
        "focus": "Coordinate curvature computations, covariant derivative, geodesic and Gaussian curvature, geometric meaning, and comparison theorems.",
        "sections": [
            {"number": "6.1", "title": "Motivation: Coordinate Computations", "printed_start": 211, "pdf_start": 226},
            {"number": "6.2", "title": "Covariant Derivative", "printed_start": 214, "pdf_start": 229},
            {"number": "6.3", "title": "Geodesic and Gaussian Curvatures", "printed_start": 221, "pdf_start": 236},
            {"number": "6.4", "title": "Geometric Meaning of Gaussian Curvature", "printed_start": 226, "pdf_start": 241},
            {"number": "6.5", "title": "Comparison Theorems", "printed_start": 237, "pdf_start": 252},
        ],
    },
    {
        "number": 7,
        "title": "Space of Metric Spaces",
        "slug": "space-of-metric-spaces",
        "folder": "chapter-07-space-of-metric-spaces",
        "notebook": "07-space-of-metric-spaces.ipynb",
        "printed": "241-270",
        "pdf": "256-285",
        "focus": "Lipschitz distance, Gromov-Hausdorff distance, convergence, and compact length-space limits.",
        "sections": [
            {"number": "7.1", "title": "Examples", "printed_start": 242, "pdf_start": 257},
            {"number": "7.2", "title": "Lipschitz Distance", "printed_start": 249, "pdf_start": 264},
            {"number": "7.3", "title": "Gromov-Hausdorff Distance", "printed_start": 251, "pdf_start": 266},
            {"number": "7.4", "title": "Gromov-Hausdorff Convergence", "printed_start": 260, "pdf_start": 275},
            {"number": "7.5", "title": "Convergence of Length Spaces", "printed_start": 265, "pdf_start": 280},
        ],
    },
    {
        "number": 8,
        "title": "Large-scale Geometry",
        "slug": "large-scale-geometry",
        "folder": "chapter-08-large-scale-geometry",
        "notebook": "08-large-scale-geometry.ipynb",
        "printed": "271-306",
        "pdf": "286-321",
        "focus": "Noncompact limits, tangent and asymptotic cones, quasi-isometries, Gromov hyperbolicity, and periodic metrics.",
        "sections": [
            {"number": "8.1", "title": "Noncompact Gromov-Hausdorff Limits", "printed_start": 271, "pdf_start": 286},
            {"number": "8.2", "title": "Tangent and Asymptotic Cones", "printed_start": 275, "pdf_start": 290},
            {"number": "8.3", "title": "Quasi-isometries", "printed_start": 277, "pdf_start": 292},
            {"number": "8.4", "title": "Gromov Hyperbolic Spaces", "printed_start": 284, "pdf_start": 299},
            {"number": "8.5", "title": "Periodic Metrics", "printed_start": 298, "pdf_start": 313},
        ],
    },
    {
        "number": 9,
        "title": "Spaces of Curvature Bounded Above",
        "slug": "spaces-of-curvature-bounded-above",
        "folder": "chapter-09-spaces-of-curvature-bounded-above",
        "notebook": "09-spaces-of-curvature-bounded-above.ipynb",
        "printed": "307-350",
        "pdf": "322-365",
        "focus": "CAT spaces, local properties, Hadamard spaces, fundamental groups, and semi-dispersing billiards.",
        "sections": [
            {"number": "9.1", "title": "Definitions and Local Properties", "printed_start": 308, "pdf_start": 323},
            {"number": "9.2", "title": "Hadamard Spaces", "printed_start": 324, "pdf_start": 339},
            {"number": "9.3", "title": "Fundamental Group of a Nonpositively Curved Space", "printed_start": 338, "pdf_start": 353},
            {"number": "9.4", "title": "Example: Semi-dispersing Billiards", "printed_start": 341, "pdf_start": 356},
        ],
    },
    {
        "number": 10,
        "title": "Spaces of Curvature Bounded Below",
        "slug": "spaces-of-curvature-bounded-below",
        "folder": "chapter-10-spaces-of-curvature-bounded-below",
        "notebook": "10-spaces-of-curvature-bounded-below.ipynb",
        "printed": "351-404",
        "pdf": "366-419",
        "focus": "CBB definitions, examples, Toponogov, diameter, splitting, dimension, volume, limits, local properties, directions, and tangent cones.",
        "sections": [
            {"number": "10.1", "title": "One More Definition", "printed_start": 352, "pdf_start": 367},
            {"number": "10.2", "title": "Constructions and Examples", "printed_start": 354, "pdf_start": 369},
            {"number": "10.3", "title": "Toponogov's Theorem", "printed_start": 360, "pdf_start": 375},
            {"number": "10.4", "title": "Curvature and Diameter", "printed_start": 364, "pdf_start": 379},
            {"number": "10.5", "title": "Splitting Theorem", "printed_start": 366, "pdf_start": 381},
            {"number": "10.6", "title": "Dimension and Volume", "printed_start": 369, "pdf_start": 384},
            {"number": "10.7", "title": "Gromov-Hausdorff Limits", "printed_start": 376, "pdf_start": 391},
            {"number": "10.8", "title": "Local Properties", "printed_start": 378, "pdf_start": 393},
            {"number": "10.9", "title": "Spaces of Directions and Tangent Cones", "printed_start": 390, "pdf_start": 405},
            {"number": "10.10", "title": "Further Information", "printed_start": 398, "pdf_start": 413},
        ],
    },
]

BIBLIOGRAPHY = {"printed": "405-408", "pdf": "420-423"}
INDEX = {"printed": "409-419", "pdf": "424-434"}


def source_map_payload() -> dict[str, Any]:
    return {
        "title": BOOK_TITLE,
        "authors": BOOK_AUTHORS,
        "pdf_filename": PDF_FILENAME,
        "printed_to_pdf_offset": PRINTED_TO_PDF_OFFSET,
        "chapters": COURSE_MAP,
        "bibliography": BIBLIOGRAPHY,
        "index": INDEX,
    }

