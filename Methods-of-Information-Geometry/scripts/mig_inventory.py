"""Source inventory for Methods of Information Geometry."""

from __future__ import annotations

ENTRIES = [
    {
        "number": 1,
        "topic": "chapter-01",
        "folder": "chapter-01-elementary-differential-geometry",
        "notebook": "01-elementary-differential-geometry.ipynb",
        "title": "Elementary differential geometry",
        "printed_pages": "1-24",
        "physical_pages": "10-33",
        "summary": "Differentiable manifolds, tangent spaces, vector and tensor fields, Riemannian metrics, affine connections, flatness, autoparallel submanifolds, projected connections, embedding curvature, and the Riemannian connection.",
        "terms": ["tangent space", "metric", "affine connection", "flatness", "autoparallel", "curvature"],
    },
    {
        "number": 2,
        "topic": "chapter-02",
        "folder": "chapter-02-geometric-structure-of-statistical-models",
        "notebook": "02-geometric-structure-of-statistical-models.ipynb",
        "title": "The geometric structure of statistical models",
        "printed_pages": "25-50",
        "physical_pages": "34-59",
        "summary": "Statistical models, Fisher metric, alpha-connection, Chentsov invariance, probability simplex geometry, alpha-affine manifolds, and alpha-families.",
        "terms": ["statistical model", "Fisher metric", "alpha-connection", "Chentsov", "simplex", "alpha-family"],
    },
    {
        "number": 3,
        "topic": "chapter-03",
        "folder": "chapter-03-dual-connections",
        "notebook": "03-dual-connections.ipynb",
        "title": "Dual connections",
        "printed_pages": "51-80",
        "physical_pages": "60-89",
        "summary": "Duality of connections, divergences as contrast functions, dually flat spaces, canonical divergence, exponential-family duality, alpha-affine duality, mutually dual foliations, and the triangular relation.",
        "terms": ["dual connection", "divergence", "dually flat", "canonical divergence", "exponential family", "triangular relation"],
    },
    {
        "number": 4,
        "topic": "chapter-04",
        "folder": "chapter-04-statistical-inference-and-differential-geometry",
        "notebook": "04-statistical-inference-and-differential-geometry.ipynb",
        "title": "Statistical inference and differential geometry",
        "printed_pages": "81-114",
        "physical_pages": "90-123",
        "summary": "Independent-observation inference, observed points, exponential and curved exponential families, consistency, first-order efficiency, higher-order asymptotics, tests, estimating functions, and fiber-bundle viewpoints.",
        "terms": ["estimation", "observed point", "curved exponential family", "efficiency", "asymptotics", "fiber bundle"],
    },
    {
        "number": 5,
        "topic": "chapter-05",
        "folder": "chapter-05-geometry-of-time-series-and-linear-systems",
        "notebook": "05-geometry-of-time-series-and-linear-systems.ipynb",
        "title": "The geometry of time series and linear systems",
        "printed_pages": "115-132",
        "physical_pages": "124-141",
        "summary": "System and time-series spaces, Fisher metric and alpha-connection on system space, finite-dimensional model geometry, stable systems, and stable feedback.",
        "terms": ["time series", "linear system", "spectrum", "Fisher metric", "alpha-connection", "stable feedback"],
    },
    {
        "number": 6,
        "topic": "chapter-06",
        "folder": "chapter-06-multiterminal-information-theory",
        "notebook": "06-multiterminal-information-theory.ipynb",
        "title": "Multiterminal information theory and statistical inference",
        "printed_pages": "133-144",
        "physical_pages": "142-153",
        "summary": "Multiterminal information, zero-rate testing, zero-rate estimation, and inference for general multiterminal information.",
        "terms": ["multiterminal information", "zero-rate testing", "zero-rate estimation", "mutual information", "projection"],
    },
    {
        "number": 7,
        "topic": "chapter-07",
        "folder": "chapter-07-information-geometry-for-quantum-systems",
        "notebook": "07-information-geometry-for-quantum-systems.ipynb",
        "title": "Information geometry for quantum systems",
        "printed_pages": "145-166",
        "physical_pages": "154-175",
        "summary": "Quantum state space, geometry induced by quantum divergences, geometry from generalized covariance, and applications to quantum estimation theory.",
        "terms": ["quantum state", "density matrix", "quantum divergence", "generalized covariance", "quantum estimation"],
    },
    {
        "number": 8,
        "topic": "chapter-08",
        "folder": "chapter-08-miscellaneous-topics",
        "notebook": "08-miscellaneous-topics.ipynb",
        "title": "Miscellaneous topics",
        "printed_pages": "167-180",
        "physical_pages": "176-189",
        "summary": "Convex analysis, linear programming, gradient flows, neuro-manifolds, nonlinear systems, Lie groups, transformation models, and mathematical problems posed by information geometry.",
        "terms": ["convex analysis", "gradient flow", "neuro-manifold", "Lie group", "transformation model", "open problems"],
    },
]

SUPPLEMENTS = [
    {"title": "Guide to the Bibliography", "printed_pages": "181-186", "physical_pages": "190-195"},
    {"title": "Bibliography", "printed_pages": "187-202", "physical_pages": "196-211"},
    {"title": "Index", "printed_pages": "203-206", "physical_pages": "212-215"},
]


def physical_page_files(span: str) -> list[str]:
    start, end = [int(part) for part in span.split("-")]
    return [f"source/djvu_text/page-{page:03}.txt" for page in range(start, end + 1)]


def notebook_path(entry: dict) -> str:
    return f"{entry['folder']}/{entry['notebook']}"

