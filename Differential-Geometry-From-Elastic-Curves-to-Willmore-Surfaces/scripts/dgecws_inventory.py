"""Inventory for the DGE-CWS notebook course."""

from __future__ import annotations

PARTS = [
    {
        "folder": "part-01-curves",
        "title": "Part I: Curves",
        "description": "Parametrized curves, arclength, variation, elastic curves, normal transport, torsion, and filament flow."
    },
    {
        "folder": "part-02-surfaces",
        "title": "Part II: Surfaces",
        "description": "Parametrized surfaces, forms and integration, curvature, connections, global curvature, closed surfaces, variations, and Willmore energy."
    },
    {
        "folder": "part-03-appendices",
        "title": "Part III: Appendices",
        "description": "Technical smoothness tools and a historical concept map used as navigation aids."
    }
]

ENTRIES = [
    {
        "kind": "chapter",
        "number": 1,
        "label": "Chapter 01",
        "title": "Curves in Rn",
        "folder": "chapter-01-curves-in-rn",
        "notebook": "01-curves-in-rn.ipynb",
        "part": "part-01-curves",
        "topic": "chapter-01",
        "printed": "3-11",
        "pdf": "13-21",
        "family": "curve",
        "focus": "Regular parametrized curves, reparametrization, length, arclength, unit tangent, and bending energy.",
        "concepts": [
            "regular curves are maps with nonzero velocity",
            "length survives reparametrization and rigid motion",
            "arclength converts arbitrary speed into intrinsic differentiation",
            "bending energy measures how fast the unit tangent turns"
        ],
        "visuals": [
            "regularity and velocity arrows",
            "two parametrizations of one quarter circle",
            "arclength cumulative map and unit-speed reconstruction",
            "bending density along line, circle, and helix"
        ],
        "checks": [
            "speed stays positive on regular examples",
            "length agrees after reparametrization",
            "arclength reconstruction has unit speed",
            "circle bending energy is L/(2 r^2)"
        ]
    },
    {
        "kind": "chapter",
        "number": 2,
        "label": "Chapter 02",
        "title": "Variations of Curves",
        "folder": "chapter-02-variations-of-curves",
        "notebook": "02-variations-of-curves.ipynb",
        "part": "part-01-curves",
        "topic": "chapter-02",
        "printed": "13-27",
        "pdf": "22-37",
        "family": "variation",
        "focus": "One-parameter curve families, variational vector fields, first variation, constrained criticality, and elastica.",
        "concepts": [
            "a variation is a path through curve space",
            "arclength differentiation does not commute with time variation",
            "compactly supported variations remove boundary terms",
            "elastic curves turn variational calculus into ODE diagnostics"
        ],
        "visuals": [
            "ribbon of nearby curves",
            "speed variation residual",
            "commutator panel for d/dt and d/ds",
            "pendulum tangent path and integrated elastica"
        ],
        "checks": [
            "mixed partials commute for smooth tests",
            "finite differences match variation integrals",
            "boundary terms vanish for bump support",
            "elastic ODE residual stays small"
        ]
    },
    {
        "kind": "chapter",
        "number": 3,
        "label": "Chapter 03",
        "title": "Curves in R2",
        "folder": "chapter-03-curves-in-r2",
        "notebook": "03-curves-in-r2.ipynb",
        "part": "part-01-curves",
        "topic": "chapter-03",
        "printed": "29-45",
        "pdf": "38-55",
        "family": "plane",
        "focus": "Signed curvature, sector area, planar elastica, tangent winding, and regular homotopy.",
        "concepts": [
            "a plane curve has scalar signed curvature",
            "signed area is an integral, not just a filled picture",
            "curvature functions reconstruct unit-speed curves",
            "tangent winding is the global integer kept by regular homotopy"
        ],
        "visuals": [
            "T, JT, and curvature sign along a curve",
            "sector-area sweep with positive and negative pieces",
            "elastica potential and curvature bands",
            "tangent-winding gallery"
        ],
        "checks": [
            "determinant curvature agrees with angle derivative",
            "reconstructed curve has the target curvature",
            "closed curve total curvature is near 2*pi*n",
            "homotopy samples keep nonzero velocity"
        ]
    },
    {
        "kind": "chapter",
        "number": 4,
        "label": "Chapter 04",
        "title": "Parallel Normal Fields",
        "folder": "chapter-04-parallel-normal-fields",
        "notebook": "04-parallel-normal-fields.ipynb",
        "part": "part-01-curves",
        "topic": "chapter-04",
        "printed": "47-57",
        "pdf": "56-66",
        "family": "spacecurve",
        "focus": "Parallel normal transport, curvature functions, and reconstruction of curves from normal-plane data.",
        "concepts": [
            "parallel normal fields avoid unnecessary twisting",
            "transport preserves normal inner products",
            "the Hasimoto curvature function records acceleration in a fixed normal plane",
            "curvature data reconstructs the curve up to rigid motion"
        ],
        "visuals": [
            "transported normal frames on a helix",
            "Gram determinant and orthogonality traces",
            "normal-plane curvature trace",
            "reconstruction dictionary for curvature data"
        ],
        "checks": [
            "frame remains orthonormal",
            "transported normal is perpendicular to tangent",
            "determinant stays positive",
            "rigid alignment residual is small"
        ]
    },
    {
        "kind": "chapter",
        "number": 5,
        "label": "Chapter 05",
        "title": "Curves in R3",
        "folder": "chapter-05-curves-in-r3",
        "notebook": "05-curves-in-r3.ipynb",
        "part": "part-01-curves",
        "topic": "chapter-05",
        "printed": "59-85",
        "pdf": "67-92",
        "family": "torsion",
        "focus": "Total torsion, elastic space curves, vortex filament flow, framed curves, twist energy, and Frenet-normal limitations.",
        "concepts": [
            "torsion measures normal-plane rotation along a space curve",
            "elastic space curves can be read through tangent dynamics",
            "binormal flow moves a curve using its own curvature frame",
            "a framed curve stores twist independently of its centerline"
        ],
        "visuals": [
            "torsion holonomy meter",
            "tangent path on the sphere",
            "short binormal-flow diagnostic",
            "framed tube with twist stripe"
        ],
        "checks": [
            "torsion angle is computed by atan2 and unwrapped",
            "frame identities hold numerically",
            "binormal update keeps small arclength drift",
            "twist energy is nonnegative"
        ]
    },
    {
        "kind": "chapter",
        "number": 6,
        "label": "Chapter 06",
        "title": "Surfaces and Riemannian Geometry",
        "folder": "chapter-06-surfaces-and-riemannian-geometry",
        "notebook": "06-surfaces-and-riemannian-geometry.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-06",
        "printed": "87-103",
        "pdf": "94-110",
        "family": "surface",
        "focus": "Parametrized surfaces, tangent spaces, induced metrics, area forms, metric rotation, and isometry.",
        "concepts": [
            "a surface is inspected through a parametrization with rank two derivative",
            "the first fundamental form turns tangent vectors into lengths and angles",
            "the area form is sqrt(det G) in coordinates",
            "isometry means the metric data agrees even when embeddings differ"
        ],
        "visuals": [
            "pushforward grid and tangent arrows",
            "metric ellipses across a patch",
            "area/J parallelogram",
            "isometry lab for flat/developable examples"
        ],
        "checks": [
            "metric matrices are positive definite",
            "area equals sqrt(EG-F^2)",
            "J squared is minus identity",
            "matched examples preserve metric coefficients"
        ]
    },
    {
        "kind": "chapter",
        "number": 7,
        "label": "Chapter 07",
        "title": "Integration and Stokes' Theorem",
        "folder": "chapter-07-integration-and-stokes-theorem",
        "notebook": "07-integration-and-stokes-theorem.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-07",
        "printed": "105-115",
        "pdf": "111-121",
        "family": "forms",
        "focus": "Integration on surfaces and curves, one-forms, two-forms, pullback, boundary orientation, and Stokes' theorem.",
        "concepts": [
            "forms carry the Jacobian and orientation information that raw functions miss",
            "a one-form measures tangent vectors along a curve",
            "boundary orientation is part of the theorem, not a drawing convention",
            "Stokes' theorem equates accumulated boundary measurement with interior exterior derivative"
        ],
        "visuals": [
            "density pullback grid",
            "two-form orientation tiles",
            "one-form curve measurement field",
            "Stokes balance panel"
        ],
        "checks": [
            "pullback integral agrees after change of variables",
            "curve integral is reparametrization invariant",
            "outer and hole boundary orientations have opposite signs",
            "numeric Stokes residual is small"
        ]
    },
    {
        "kind": "chapter",
        "number": 8,
        "label": "Chapter 08",
        "title": "Curvature",
        "folder": "chapter-08-curvature",
        "notebook": "08-curvature.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-08",
        "printed": "117-129",
        "pdf": "122-134",
        "family": "curvature",
        "focus": "Unit normal, shape operator, principal curvature, mean curvature, Gaussian curvature, umbilics, and Gauss-map area.",
        "concepts": [
            "the surface normal converts bending into a derivative",
            "the shape operator is the tangent map hidden inside dN",
            "principal curvatures are directional extrema",
            "Gaussian curvature is the signed area distortion of the normal map"
        ],
        "visuals": [
            "normal orientation on a surface patch",
            "shape-operator gallery",
            "directional curvature polar plot",
            "Gauss-map area panel"
        ],
        "checks": [
            "normal is unit and perpendicular to partials",
            "shape operator is self-adjoint for the metric",
            "H and K match trace and determinant",
            "sphere has constant positive curvature"
        ]
    },
    {
        "kind": "chapter",
        "number": 9,
        "label": "Chapter 09",
        "title": "Levi-Civita Connection",
        "folder": "chapter-09-levi-civita-connection",
        "notebook": "09-levi-civita-connection.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-09",
        "printed": "131-137",
        "pdf": "135-142",
        "family": "connection",
        "focus": "Tangential differentiation, Levi-Civita connection, Gauss and Codazzi equations, and Theorema Egregium.",
        "concepts": [
            "differentiate in space and project back to the tangent plane",
            "the metric determines the same connection coefficients",
            "Codazzi compares derivatives of the shape operator",
            "Theorema Egregium says Gaussian curvature is intrinsic"
        ],
        "visuals": [
            "tangent-normal derivative split",
            "Christoffel coefficient comparison",
            "moving frame rotation form",
            "Gauss/Codazzi residual heatmaps"
        ],
        "checks": [
            "projected derivative is tangent",
            "metric compatibility residual is small",
            "torsion-free coordinate check passes",
            "plane and cylinder both give K=0"
        ]
    },
    {
        "kind": "chapter",
        "number": 10,
        "label": "Chapter 10",
        "title": "Total Gaussian Curvature",
        "folder": "chapter-10-total-gaussian-curvature",
        "notebook": "10-total-gaussian-curvature.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-10",
        "printed": "139-149",
        "pdf": "143-153",
        "family": "gaussbonnet",
        "focus": "Curves on surfaces, total Gaussian curvature, Gauss-Bonnet, and parallel transport holonomy.",
        "concepts": [
            "surface curves split curvature into geodesic and normal pieces",
            "Gauss-Bonnet balances interior curvature and boundary turning",
            "parallel transport around a loop returns with a measurable angle",
            "holonomy is a local detector for enclosed curvature"
        ],
        "visuals": [
            "curve classifiers on a surface",
            "Gauss-Bonnet accounting bars",
            "parallel transport ODE loop",
            "holonomy-curvature comparison"
        ],
        "checks": [
            "test frames remain orthonormal",
            "hemisphere integral approaches 2*pi",
            "annulus boundary terms cancel in flat case",
            "transport preserves tangent vector length"
        ]
    },
    {
        "kind": "chapter",
        "number": 11,
        "label": "Chapter 11",
        "title": "Closed Surfaces",
        "folder": "chapter-11-closed-surfaces",
        "notebook": "11-closed-surfaces.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-11",
        "printed": "151-160",
        "pdf": "154-163",
        "family": "topology",
        "focus": "Boundary gluing, oriented and non-oriented closed surfaces, orientation covers, genus, and total curvature.",
        "concepts": [
            "closed surfaces can be represented by pairing boundary curves",
            "orientation data decides whether the glued surface is orientable",
            "genus can be computed from the boundary-pairing ledger",
            "total Gaussian curvature only sees Euler characteristic"
        ],
        "visuals": [
            "boundary pairing graph",
            "torus and Klein gluing contrast",
            "orientation-cover diagram",
            "genus calculator panel"
        ],
        "checks": [
            "pairing map is an involution",
            "orientation signs match the selected model",
            "genus formula matches examples",
            "Euler characteristic predicts total curvature target"
        ]
    },
    {
        "kind": "chapter",
        "number": 12,
        "label": "Chapter 12",
        "title": "Variations of Surfaces",
        "folder": "chapter-12-variations-of-surfaces",
        "notebook": "12-variations-of-surfaces.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-12",
        "printed": "161-179",
        "pdf": "164-182",
        "family": "surfacevariation",
        "focus": "Surface vector calculus, one-parameter surface families, curvature variation, area variation, volume variation, minimal and CMC surfaces.",
        "concepts": [
            "grad, div, and Laplacian become intrinsic surface operators",
            "a variation decomposes into normal motion and tangential relabeling",
            "mean curvature is the gradient of area",
            "constant mean curvature is the area critical condition under fixed volume"
        ],
        "visuals": [
            "surface vector-calculus dashboard",
            "variation decomposition panel",
            "first area variation plot",
            "cone volume and CMC comparison"
        ],
        "checks": [
            "divergence theorem residual is small",
            "normal bump finite difference matches area variation",
            "minimal examples have small H",
            "sphere has constant H for volume constraint"
        ]
    },
    {
        "kind": "chapter",
        "number": 13,
        "label": "Chapter 13",
        "title": "Willmore Surfaces",
        "folder": "chapter-13-willmore-surfaces",
        "notebook": "13-willmore-surfaces.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-13",
        "printed": "181-191",
        "pdf": "183-193",
        "family": "willmore",
        "focus": "Willmore functional, Willmore equation, energy offsets, cylinder examples, and inversion invariance.",
        "concepts": [
            "Willmore energy measures bending after subtracting the topological Gaussian term",
            "the sphere is the baseline compact example",
            "the first variation produces a fourth-order surface equation",
            "inversion preserves the conformal Willmore density away from singularities"
        ],
        "visuals": [
            "Willmore energy zoo",
            "functional offset bars",
            "finite-difference Willmore residual",
            "inversion lab"
        ],
        "checks": [
            "Willmore energy is scale invariant for the sphere",
            "integrated K records the expected offset",
            "sphere residual is small",
            "inversion comparison avoids the center singularity"
        ]
    },
    {
        "kind": "appendix",
        "number": 101,
        "label": "Appendix A",
        "title": "Some Technicalities",
        "folder": "appendix-a-some-technicalities",
        "notebook": "appendix-a-some-technicalities.ipynb",
        "part": "part-03-appendices",
        "topic": "appendix-a",
        "printed": "193-196",
        "pdf": "194-197",
        "family": "appendix",
        "focus": "Smooth maps on closed domains, support, bump functions, and smooth cutoffs.",
        "concepts": [
            "smoothness on a closed domain is inherited from an open extension",
            "support records where a function is allowed to act",
            "flat bump functions localize variations without boundary traces",
            "diffeomorphism checks require a smooth inverse and nonzero Jacobian"
        ],
        "visuals": [
            "extension collar diagram",
            "boundary derivative experiment",
            "diffeomorphism grid",
            "bump function toolbox"
        ],
        "checks": [
            "sampled bump support is compact",
            "boundary derivatives are numerically flat",
            "composition error for inverse maps is small",
            "Jacobian samples stay nonzero"
        ]
    },
    {
        "kind": "appendix",
        "number": 102,
        "label": "Appendix B",
        "title": "Timeline",
        "folder": "appendix-b-timeline",
        "notebook": "appendix-b-timeline.ipynb",
        "part": "part-03-appendices",
        "topic": "appendix-b",
        "printed": "197-198",
        "pdf": "198-199",
        "family": "timeline",
        "focus": "A navigable timeline connecting elastic curves, surface theory, topology, variational calculus, and Willmore surfaces.",
        "concepts": [
            "historical milestones can be used as a concept dependency map",
            "curve theory and surface theory repeatedly exchange methods",
            "topological invariants constrain curvature integrals",
            "Willmore surfaces inherit both variational and conformal ideas"
        ],
        "visuals": [
            "chronological milestone timeline",
            "concept dependency graph",
            "elastic-to-Willmore lineage",
            "chapter-link navigation table"
        ],
        "checks": [
            "years are sorted",
            "each node has a theme",
            "duplicate years are intentionally grouped",
            "chapter links resolve to local notebooks"
        ]
    }
]


def canonical_entries() -> list[dict]:
    return list(ENTRIES)


def parts() -> list[dict]:
    return list(PARTS)
