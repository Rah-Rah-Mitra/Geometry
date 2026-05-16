"""Course manifest for the manifold inference notebook edition."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]
PDF_NAME = "Nonparametric Inference on Manifolds with Applications to Shape Spaces.pdf"


@dataclass(frozen=True)
class Chapter:
    key: str
    number: str
    title: str
    part: str
    folder: str
    notebook: str
    printed_pages: str
    pdf_pages: str
    focus: str
    concepts: tuple[str, ...]
    libraries: tuple[str, ...]
    visuals: tuple[str, ...]

    @property
    def path(self) -> Path:
        return BOOK_ROOT / self.part / self.folder / self.notebook

    @property
    def index_path(self) -> Path:
        return BOOK_ROOT / self.part / self.folder / "00-index.ipynb"

    @property
    def artifact_dir(self) -> Path:
        return BOOK_ROOT / "artifacts" / self.key


PARTS: dict[str, str] = {
    "part-01-foundations-and-examples": "Foundations, examples, and Frechet inference",
    "part-02-shape-spaces": "Landmark, Kendall, Stiefel, affine, and projective shape spaces",
    "part-03-bayes-on-manifolds": "Nonparametric Bayes methods on manifolds",
    "part-04-appendices": "Differentiable, Riemannian, Dirichlet, and parametric background",
}


CHAPTERS: tuple[Chapter, ...] = (
    Chapter(
        "chapter-01",
        "01",
        "Introduction",
        "part-01-foundations-and-examples",
        "chapter-01-introduction",
        "01-introduction.ipynb",
        "1-7",
        "16-22",
        "Why landmark data lead to quotient manifolds and why Frechet means are the main statistical object.",
        ("landmarks", "transformation groups", "extrinsic versus intrinsic distance", "two-sample mean testing"),
        ("matplotlib", "networkx"),
        ("shape-inference-roadmap.png", "quotient-ladder.png"),
    ),
    Chapter(
        "chapter-02",
        "02",
        "Examples",
        "part-01-foundations-and-examples",
        "chapter-02-examples",
        "02-examples.ipynb",
        "8-20",
        "23-35",
        "A visual gallery of directional and shape-data examples that will reappear as computational laboratories.",
        ("circle data", "sphere data", "planar shapes", "affine shapes", "reflection shapes"),
        ("matplotlib", "plotly"),
        ("application-gallery.png", "sphere-observations.html"),
    ),
    Chapter(
        "chapter-03",
        "03",
        "Location and spread on metric spaces",
        "part-01-foundations-and-examples",
        "chapter-03-location-and-spread",
        "03-location-and-spread.ipynb",
        "21-35",
        "36-50",
        "Frechet functions, metric variation, sample means, and asymptotic behavior before smooth structure is assumed.",
        ("Frechet function", "metric variation", "sample mean set", "circle example", "bootstrap"),
        ("numpy", "scipy", "matplotlib"),
        ("metric-frechet-landscape.png", "circle-bootstrap-bands.png"),
    ),
    Chapter(
        "chapter-04",
        "04",
        "Extrinsic analysis on manifolds",
        "part-01-foundations-and-examples",
        "chapter-04-extrinsic-analysis",
        "04-extrinsic-analysis.ipynb",
        "36-56",
        "51-71",
        "Embedding a manifold, averaging in the ambient space, and projecting back with tangent covariance diagnostics.",
        ("embedding", "projection", "extrinsic mean", "extrinsic covariance", "equivariance"),
        ("geomstats", "matplotlib", "numpy"),
        ("sphere-extrinsic-projection.png", "extrinsic-covariance-ellipse.png"),
    ),
    Chapter(
        "chapter-05",
        "05",
        "Intrinsic analysis on manifolds",
        "part-01-foundations-and-examples",
        "chapter-05-intrinsic-analysis",
        "05-intrinsic-analysis.ipynb",
        "57-76",
        "72-91",
        "Geodesic-distance Frechet means, log-map coordinates, cut-locus caveats, and bootstrap inference on spheres.",
        ("geodesic distance", "intrinsic mean", "log map", "cut locus", "two-sample tests"),
        ("geomstats", "matplotlib", "scipy"),
        ("intrinsic-mean-iteration.png", "log-map-bootstrap-cloud.png"),
    ),
    Chapter(
        "chapter-06",
        "06",
        "Landmark-based shape spaces",
        "part-02-shape-spaces",
        "chapter-06-landmark-shape-spaces",
        "06-landmark-shape-spaces.ipynb",
        "77-81",
        "92-96",
        "The landmark pipeline from labeled configurations to quotient spaces under increasingly large transformation groups.",
        ("k-ads", "centering", "scale", "group orbit", "shape manifold"),
        ("matplotlib", "numpy"),
        ("landmark-normalization-pipeline.png", "group-orbit-comparison.png"),
    ),
    Chapter(
        "chapter-07",
        "07",
        "Kendall similarity shape spaces",
        "part-02-shape-spaces",
        "chapter-07-kendall-similarity-shapes",
        "07-kendall-similarity-shapes.ipynb",
        "82-86",
        "97-101",
        "Preshape spheres, rotation quotients, horizontal directions, and geodesic distance on similarity shapes.",
        ("preshape sphere", "rotation quotient", "horizontal tangent", "Procrustes distance"),
        ("numpy", "matplotlib", "plotly"),
        ("preshape-sphere-orbits.png", "kendall-geodesic.html"),
    ),
    Chapter(
        "chapter-08",
        "08",
        "The planar shape space Sigma_k2",
        "part-02-shape-spaces",
        "chapter-08-planar-shape-space",
        "08-planar-shape-space.ipynb",
        "87-109",
        "102-124",
        "Complex projective planar shape space, intrinsic and extrinsic means, size-and-shape, and two-sample inference.",
        ("complex preshape", "CP space", "Veronese embedding", "Procrustes mean", "bootstrap"),
        ("geomstats", "matplotlib", "plotly"),
        ("planar-shape-sphere.png", "procrustes-bootstrap.png"),
    ),
    Chapter(
        "chapter-09",
        "09",
        "Reflection similarity shape spaces",
        "part-02-shape-spaces",
        "chapter-09-reflection-shape-spaces",
        "09-reflection-shape-spaces.ipynb",
        "110-129",
        "125-144",
        "Reflection invariance as an unoriented quotient and extrinsic analysis through Gram-style representations.",
        ("reflection quotient", "Gram matrix", "unoriented shape", "matched pairs", "two-sample tests"),
        ("matplotlib", "numpy", "scipy"),
        ("reflection-quotient-diagnostic.png", "gram-embedding-spectrum.png"),
    ),
    Chapter(
        "chapter-10",
        "10",
        "Stiefel manifolds V_k,m",
        "part-02-shape-spaces",
        "chapter-10-stiefel-manifolds",
        "10-stiefel-manifolds.ipynb",
        "130-134",
        "145-149",
        "Orthogonal frames as manifold data, projection onto Stiefel constraints, and extrinsic mean diagnostics.",
        ("orthonormal frame", "polar projection", "tangent residual", "extrinsic mean"),
        ("numpy", "matplotlib", "scipy"),
        ("stiefel-frame-projection.png", "orthogonality-residuals.png"),
    ),
    Chapter(
        "chapter-11",
        "11",
        "Affine shape spaces A Sigma_km",
        "part-02-shape-spaces",
        "chapter-11-affine-shape-spaces",
        "11-affine-shape-spaces.ipynb",
        "135-146",
        "150-161",
        "Affine normalization, rank conditions, and digit-like landmark examples where similarity information is intentionally discarded.",
        ("affine orbit", "rank", "normalization", "classification", "landmark covariance"),
        ("numpy", "matplotlib", "scikit-learn"),
        ("affine-normalization-grid.png", "digit-shape-affine-features.png"),
    ),
    Chapter(
        "chapter-12",
        "12",
        "Real projective spaces and projective shape spaces",
        "part-02-shape-spaces",
        "chapter-12-projective-shape-spaces",
        "12-projective-shape-spaces.ipynb",
        "147-155",
        "162-170",
        "Projective points as lines through the origin, antipodal quotients, and extrinsic analysis on real projective space.",
        ("real projective space", "antipodal quotient", "projective distance", "projective shape"),
        ("geomstats", "matplotlib", "plotly"),
        ("projective-antipodal-quotient.png", "projective-distance-field.html"),
    ),
    Chapter(
        "chapter-13",
        "13",
        "Nonparametric Bayes inference on manifolds",
        "part-03-bayes-on-manifolds",
        "chapter-13-bayes-inference",
        "13-bayes-inference.ipynb",
        "156-181",
        "171-196",
        "Density estimation, posterior consistency intuition, and manifold mixture computation with spherical and SPD examples.",
        ("metric support", "kernel mixture", "Dirichlet process", "posterior computation", "classification"),
        ("pyriemann", "matplotlib", "scipy", "numpy"),
        ("manifold-density-mixture.png", "spd-riemannian-mean.png"),
    ),
    Chapter(
        "chapter-14",
        "14",
        "Nonparametric Bayes regression, classification, and testing",
        "part-03-bayes-on-manifolds",
        "chapter-14-bayes-regression-classification-testing",
        "14-bayes-regression-classification-testing.ipynb",
        "182-208",
        "197-223",
        "Mixture-of-kernels regression, classification probabilities, and posterior testing as geometry-aware predictive workflows.",
        ("product kernels", "regression", "classification", "Bayes testing", "posterior predictive checks"),
        ("matplotlib", "scipy", "numpy"),
        ("manifold-kernel-classifier.png", "posterior-test-calibration.png"),
    ),
    Chapter(
        "appendix-a",
        "A",
        "Differentiable manifolds",
        "part-04-appendices",
        "appendix-a-differentiable-manifolds",
        "appendix-a-differentiable-manifolds.ipynb",
        "209-213",
        "224-228",
        "An executable atlas for charts, tangent vectors, immersions, submersions, and quotient-map intuition.",
        ("chart", "tangent vector", "immersion", "submersion", "quotient"),
        ("matplotlib", "sympy"),
        ("atlas-transition-map.png", "tangent-pushforward.png"),
    ),
    Chapter(
        "appendix-b",
        "B",
        "Riemannian manifolds",
        "part-04-appendices",
        "appendix-b-riemannian-manifolds",
        "appendix-b-riemannian-manifolds.ipynb",
        "214-217",
        "229-232",
        "Metrics, geodesics, exponential and logarithm maps, curvature intuition, and SPD comparison checks.",
        ("metric tensor", "geodesic", "exponential map", "logarithm map", "curvature"),
        ("geomstats", "pyriemann", "matplotlib"),
        ("riemannian-exp-log-map.png", "spd-geodesic-comparison.png"),
    ),
    Chapter(
        "appendix-c",
        "C",
        "Dirichlet processes",
        "part-04-appendices",
        "appendix-c-dirichlet-processes",
        "appendix-c-dirichlet-processes.ipynb",
        "218-224",
        "233-239",
        "Stick-breaking, Polya urns, random discrete measures, and why DP mixtures adapt to manifold support.",
        ("stick breaking", "Polya urn", "base measure", "random measure", "posterior update"),
        ("numpy", "matplotlib", "scipy"),
        ("stick-breaking-measure.png", "polya-urn-clusters.png"),
    ),
    Chapter(
        "appendix-d",
        "D",
        "Parametric models on S_d and Sigma_k2",
        "part-04-appendices",
        "appendix-d-parametric-models",
        "appendix-d-parametric-models.ipynb",
        "225-228",
        "240-243",
        "Parametric sphere and planar-shape models used as baselines for the nonparametric methods.",
        ("von Mises-Fisher", "axial models", "planar shape model", "normalizing constant"),
        ("geomstats", "matplotlib", "scipy"),
        ("sphere-parametric-family.png", "shape-space-parametric-baseline.png"),
    ),
)


def chapter_by_key(key: str) -> Chapter:
    for chapter in CHAPTERS:
        if chapter.key == key:
            return chapter
    raise KeyError(key)


def canonical_notebooks() -> list[Path]:
    return [chapter.path for chapter in CHAPTERS]


def index_notebooks() -> list[Path]:
    paths = [BOOK_ROOT / "00-book-index.ipynb"]
    paths.extend(BOOK_ROOT / part / "00-part-index.ipynb" for part in PARTS)
    paths.extend(chapter.index_path for chapter in CHAPTERS)
    return paths
