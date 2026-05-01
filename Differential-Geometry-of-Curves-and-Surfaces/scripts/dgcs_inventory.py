"""Course inventory for do Carmo's Differential Geometry of Curves and Surfaces."""

from __future__ import annotations

SOURCE_SPAN_NOTES = [
    "The local PDF is used only for source orientation.",
    "Body printed pages map to PDF pages by pdf_page = printed_page + 16.",
    "Back matter is inventoried but not converted into copied hints or exercise text.",
]

ENTRIES = [
    {
        "label": "Chapter 01",
        "title": "Curves",
        "folder": "chapter-01-curves",
        "notebook": "01-curves.ipynb",
        "artifact": "chapter-01",
        "printed_span": "1-52",
        "pdf_span": "17-68",
        "sections": "1-1 through 1-7",
        "focus": "parametrized curves, regularity, arc length, Frenet frames, curvature, torsion, and global plane-curve behavior",
        "topics": [
            "regular parametrizations and singular points",
            "arc length as a preferred parameter",
            "Frenet frame, curvature, torsion, and osculating geometry",
            "local canonical form and global plane-curve diagnostics",
        ],
    },
    {
        "label": "Chapter 02",
        "title": "Regular Surfaces",
        "folder": "chapter-02-regular-surfaces",
        "notebook": "02-regular-surfaces.ipynb",
        "artifact": "chapter-02",
        "printed_span": "53-135",
        "pdf_span": "69-151",
        "sections": "2-1 through 2-8 plus appendix",
        "focus": "surface patches, tangent planes, differentiable maps, first fundamental form, area, and orientation",
        "topics": [
            "regular surface definitions by patches and regular values",
            "coordinate changes and tangent planes",
            "first fundamental form and surface area",
            "orientation and compact orientable surface intuition",
        ],
    },
    {
        "label": "Chapter 03",
        "title": "The Geometry of the Gauss Map",
        "folder": "chapter-03-the-geometry-of-the-gauss-map",
        "notebook": "03-the-geometry-of-the-gauss-map.ipynb",
        "artifact": "chapter-03",
        "printed_span": "136-219",
        "pdf_span": "152-235",
        "sections": "3-1 through 3-5 plus appendix",
        "focus": "Gauss map, shape operator, curvatures, vector fields, ruled surfaces, and minimal surfaces",
        "topics": [
            "normal maps as curvature sensors",
            "shape operator and principal curvature directions",
            "Gaussian and mean curvature in coordinates",
            "ruled and minimal surface examples",
        ],
    },
    {
        "label": "Chapter 04",
        "title": "The Intrinsic Geometry of Surfaces",
        "folder": "chapter-04-the-intrinsic-geometry-of-surfaces",
        "notebook": "04-the-intrinsic-geometry-of-surfaces.ipynb",
        "artifact": "chapter-04",
        "printed_span": "220-320",
        "pdf_span": "236-336",
        "sections": "4-1 through 4-7 plus appendix",
        "focus": "isometries, conformal maps, compatibility equations, geodesics, parallel transport, Gauss-Bonnet, and exponential maps",
        "topics": [
            "intrinsic data versus extrinsic embeddings",
            "Christoffel symbols and compatibility",
            "geodesics and parallel transport",
            "Gauss-Bonnet and exponential coordinates",
        ],
    },
    {
        "label": "Chapter 05",
        "title": "Global Differential Geometry",
        "folder": "chapter-05-global-differential-geometry",
        "notebook": "05-global-differential-geometry.ipynb",
        "artifact": "chapter-05",
        "printed_span": "321-474",
        "pdf_span": "337-490",
        "sections": "5-1 through 5-11 plus appendix",
        "focus": "rigidity, completeness, variations, Jacobi fields, coverings, total curvature, flat surfaces, abstract surfaces, and Hilbert obstruction",
        "topics": [
            "local curvature versus global consequences",
            "completeness and Hopf-Rinow intuition",
            "variations, Jacobi fields, and conjugate points",
            "coverings, total curvature, developables, and global obstructions",
        ],
    },
]

BACK_MATTER = [
    {"title": "Bibliography and Comments", "printed_span": "475-477", "pdf_span": "491-493"},
    {"title": "Hints and Answers", "printed_span": "478-502", "pdf_span": "494-518"},
    {"title": "Index", "printed_span": "503-513", "pdf_span": "519-529"},
]
