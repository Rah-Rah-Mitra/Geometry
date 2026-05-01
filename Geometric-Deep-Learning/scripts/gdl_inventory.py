"""Course inventory for the Geometric Deep Learning notebooks."""

from __future__ import annotations

from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BOOK_ROOT.parent

ENTRIES = [
    {
        "chapter": 1,
        "title": "Introduction",
        "folder": "chapter-01-introduction",
        "notebook": "01-introduction.ipynb",
        "printed_pages": "4",
        "pdf_pages": "8",
        "sections": "1",
        "focus": "Representation learning, structured data, symmetry preview, and the GDL design loop.",
        "visual_spine": "ambient vs structured samples, symmetry action gallery, equivariance mini-lab, blueprint taxonomy",
    },
    {
        "chapter": 2,
        "title": "Learning in High Dimensions",
        "folder": "chapter-02-learning-in-high-dimensions",
        "notebook": "02-learning-in-high-dimensions.ipynb",
        "printed_pages": "5-8",
        "pdf_pages": "9-12",
        "sections": "2.1-2.2",
        "focus": "Interpolation, regularity, implicit bias, Lipschitz fill distance, and covering growth.",
        "visual_spine": "interpolants, regularity, implicit minimum norm, covering explosion, projection priors",
    },
    {
        "chapter": 3,
        "title": "Geometric Priors",
        "folder": "chapter-03-geometric-priors",
        "notebook": "03-geometric-priors.ipynb",
        "printed_pages": "9-29",
        "pdf_pages": "13-33",
        "sections": "3.1-3.5",
        "focus": "Signals on domains, groups/actions, invariance/equivariance, stability, and scale separation.",
        "visual_spine": "D3 actions, commuting squares, subgroup ladder, deformation stability, pooling hierarchy",
    },
    {
        "chapter": 4,
        "title": "Geometric Domains: the 5 Gs",
        "folder": "chapter-04-geometric-domains-the-5-gs",
        "notebook": "04-geometric-domains-the-5-gs.ipynb",
        "printed_pages": "30-67",
        "pdf_pages": "34-71",
        "sections": "4.1-4.6",
        "focus": "Graphs/sets, grids, groups, manifolds/geodesics, gauges/bundles, and meshes.",
        "visual_spine": "5G atlas, graph equivariance, circulant grids, finite groups, sphere transport, mesh Laplacians",
    },
    {
        "chapter": 5,
        "title": "Geometric Deep Learning Models",
        "folder": "chapter-05-geometric-deep-learning-models",
        "notebook": "05-geometric-deep-learning-models.ipynb",
        "printed_pages": "68-101",
        "pdf_pages": "72-105",
        "sections": "5.1-5.8",
        "focus": "CNNs, group CNNs, GNNs, sets/Transformers, E(3) message passing, mesh CNNs, and RNN/LSTM.",
        "visual_spine": "CNN filters, group convolutions, GNN flavors, Transformers, E(3) messages, mesh gauges, RNN gates",
    },
    {
        "chapter": 6,
        "title": "Problems and Applications",
        "folder": "chapter-06-problems-and-applications",
        "notebook": "06-problems-and-applications.ipynb",
        "printed_pages": "102-113",
        "pdf_pages": "106-117",
        "sections": "6",
        "focus": "Chemistry, proteins, recommenders, traffic, vision, games, language/audio, healthcare, physics, and VR/AR.",
        "visual_spine": "application atlas with invariant/equivariant checks for every domain",
    },
    {
        "chapter": 7,
        "title": "Historic Perspective",
        "folder": "chapter-07-historic-perspective",
        "notebook": "07-historic-perspective.ipynb",
        "printed_pages": "114-127",
        "pdf_pages": "118-130",
        "sections": "7",
        "focus": "Symmetry history, architecture lineage, WL, harmonic analysis, geometry processing, and algorithmic reasoning.",
        "visual_spine": "timeline, architecture lineage, WL demo, graph signal processing lineage, algorithmic invariant flow",
    },
]


def chapter_topic(chapter: int) -> str:
    return f"chapter-{chapter:02d}"


def canonical_path(entry: dict[str, object]) -> Path:
    return BOOK_ROOT / str(entry["folder"]) / str(entry["notebook"])


def index_path(entry: dict[str, object]) -> Path:
    return BOOK_ROOT / str(entry["folder"]) / "00-index.ipynb"

