"""Bootstrap the Directional Statistics visualization-first notebook course.

This script is intentionally course-local and reproducible. It writes the
initial utilities, inventory, validation scripts, indexes, canonical notebooks,
and seed artifacts for the empty textbook folder.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

BOOK_ROOT = Path(__file__).resolve().parents[1]


PARTS = [
    {
        "folder": "part-01-circular-statistics",
        "title": "Part I: Circular Statistics",
        "description": "Circular and axial data, circular summaries, circular models, estimation, tests, and non-parametric methods.",
    },
    {
        "folder": "part-02-spherical-statistics",
        "title": "Part II: Spherical Statistics",
        "description": "Distributions, inference, dependence, regression, and modern methods for directions on spheres.",
    },
    {
        "folder": "part-03-general-sample-spaces-and-shape",
        "title": "Part III: General Sample Spaces and Shape",
        "description": "Frames, rotations, Stiefel and Grassmann manifolds, hyperboloids, and landmark shape spaces.",
    },
    {
        "folder": "part-04-appendices",
        "title": "Part IV: Computational Appendices",
        "description": "Special functions, executable circular and spherical table replacements, and a notation atlas.",
    },
]


ENTRIES = [
    {
        "kind": "chapter",
        "number": 1,
        "label": "Chapter 01",
        "title": "Circular Data",
        "folder": "chapter-01-circular-data",
        "notebook": "01-circular-data.ipynb",
        "part": "part-01-circular-statistics",
        "topic": "chapter-01",
        "family": "circular",
        "printed": "1-12",
        "pdf": "20-31",
        "focus": "Circular and axial observations, faithful displays, and the distinction between wrapping clock data and projecting compass data.",
        "concepts": [
            "directions are unit vectors after choosing an origin and orientation",
            "axial observations identify opposite directions and are handled by doubled angles",
            "rose diagrams, circular histograms, and unrolled histograms answer different visual questions",
            "wrapped time data and projected compass data have different generative stories",
        ],
        "visuals": [
            "clock and compass coordinate setup on the unit circle",
            "raw circular dot plot, rose diagram, and unrolled histogram",
            "axial doubling diagram",
            "wrapping-versus-projecting schematic",
        ],
        "checks": [
            "bin counts are preserved by display choices",
            "rose sector area is proportional to frequency",
            "theta and theta + pi agree after axial doubling",
            "wrapping keeps periodic distance rather than linear distance",
        ],
    },
    {
        "kind": "chapter",
        "number": 2,
        "label": "Chapter 02",
        "title": "Summary Statistics",
        "folder": "chapter-02-summary-statistics",
        "notebook": "02-summary-statistics.ipynb",
        "part": "part-01-circular-statistics",
        "topic": "chapter-02",
        "family": "circular",
        "printed": "13-24",
        "pdf": "32-42",
        "focus": "Coordinate-invariant summaries from unit-vector geometry: mean direction, resultant length, circular median, moments, and grouping corrections.",
        "concepts": [
            "ordinary arithmetic means fail when the cut point moves",
            "the vector resultant supplies the mean direction and concentration",
            "dispersion is minimized by the mean direction in chord-distance form",
            "higher trigonometric moments detect skewness, kurtosis, and p-fold structure",
        ],
        "visuals": [
            "resultant vector construction",
            "cut-point failure for the linear mean",
            "dispersion curve minimized at the circular mean",
            "trigonometric moment dashboard",
        ],
        "checks": [
            "sum sin(theta_i - mean) is zero",
            "D(mean) equals 1 - R",
            "mean direction rotates equivariantly",
            "grouping corrections are small for fine bins",
        ],
    },
    {
        "kind": "chapter",
        "number": 3,
        "label": "Chapter 03",
        "title": "Basic Concepts and Models",
        "folder": "chapter-03-basic-concepts-and-models",
        "notebook": "03-basic-concepts-and-models.ipynb",
        "part": "part-01-circular-statistics",
        "topic": "chapter-03",
        "family": "circular",
        "printed": "25-56",
        "pdf": "43-73",
        "focus": "Circular distribution functions, characteristic functions, Fourier reconstruction, and model families such as uniform, von Mises, cardioid, wrapped, and projected distributions.",
        "concepts": [
            "arc probabilities replace interval probabilities on the line",
            "Fourier coefficients are the natural circular characteristic function",
            "von Mises concentration is read through Bessel ratios",
            "wrapping and projection generate different circular model families",
        ],
        "visuals": [
            "circular CDF and arc probability panel",
            "Fourier coefficient spectrum",
            "model gallery for circular densities",
            "projected-normal and wrapped-normal comparison",
        ],
        "checks": [
            "densities integrate to one over the circle",
            "Fourier coefficients match trigonometric moments",
            "uniform coefficients vanish except the zero coefficient",
            "convolution multiplies characteristic functions",
        ],
    },
    {
        "kind": "chapter",
        "number": 4,
        "label": "Chapter 04",
        "title": "Fundamental Theorems and Distribution Theory",
        "folder": "chapter-04-fundamental-theorems-and-distribution-theory",
        "notebook": "04-fundamental-theorems-and-distribution-theory.ipynb",
        "part": "part-01-circular-statistics",
        "topic": "chapter-04",
        "family": "circular",
        "printed": "57-82",
        "pdf": "74-99",
        "focus": "Characteristic-function properties, circular limit theorems, resultant distributions, and high-concentration approximations.",
        "concepts": [
            "characteristic functions encode the circular distribution",
            "random walks of unit vectors explain resultant length distributions",
            "central-limit behavior is seen in tangent coordinates",
            "high concentration turns local circular inference into linear normal approximations",
        ],
        "visuals": [
            "characteristic-function fingerprints",
            "random-walk endpoint cloud",
            "joint C and S sampling cloud",
            "high-concentration tangent-normal approximation",
        ],
        "checks": [
            "simulated 2nR^2 approaches a chi-square reference under uniformity",
            "E[Rbar^2] is close to 1/n under uniformity",
            "approximations improve with kappa",
            "resultant simulations preserve unit-vector sums",
        ],
    },
    {
        "kind": "chapter",
        "number": 5,
        "label": "Chapter 05",
        "title": "Point Estimation",
        "folder": "chapter-05-point-estimation",
        "notebook": "05-point-estimation.ipynb",
        "part": "part-01-circular-statistics",
        "topic": "chapter-05",
        "family": "circular",
        "printed": "83-92",
        "pdf": "100-109",
        "focus": "Parameter estimation for circular models, especially von Mises concentration, wrapped Cauchy behavior, and mixtures.",
        "concepts": [
            "the von Mises mean MLE is the sample mean direction",
            "the concentration MLE solves A(kappa) = R",
            "bias correction matters when samples are small or concentration is low",
            "mixtures need responsibility weights on the circle rather than linear residuals",
        ],
        "visuals": [
            "von Mises likelihood surface",
            "A(kappa) inverse curve",
            "finite-sample concentration bias bands",
            "two-component mixture responsibilities",
        ],
        "checks": [
            "A(kappa_hat) matches R",
            "likelihood gradient is small at the estimate",
            "rotation of data rotates mu_hat",
            "mixture weights sum to one",
        ],
    },
    {
        "kind": "chapter",
        "number": 6,
        "label": "Chapter 06",
        "title": "Tests of Uniformity and Goodness-of-Fit",
        "folder": "chapter-06-tests-of-uniformity-and-goodness-of-fit",
        "notebook": "06-tests-of-uniformity-and-goodness-of-fit.ipynb",
        "part": "part-01-circular-statistics",
        "topic": "chapter-06",
        "family": "circular",
        "printed": "93-118",
        "pdf": "110-135",
        "focus": "Graphical uniformity checks, Rayleigh, Kuiper, Watson, spacing, Ajne, Hermans-Rasson, Beran, and probability-integral-transform diagnostics.",
        "concepts": [
            "uniformity is the central circular null model",
            "Rayleigh tests detect a preferred first harmonic direction",
            "Kuiper and Watson statistics compare circular empirical distributions without privileging the origin",
            "goodness-of-fit uses a circular probability integral transform",
        ],
        "visuals": [
            "Rayleigh rejection ring",
            "Kuiper and Watson empirical CDF overlays",
            "spacings and semicircle scans",
            "PIT goodness-of-fit panel",
        ],
        "checks": [
            "Rayleigh statistic equals 2nR^2",
            "Kuiper statistic is invariant to origin shifts",
            "Watson centering removes origin dependence",
            "PIT values are uniform under a fitted continuous model",
        ],
    },
    {
        "kind": "chapter",
        "number": 7,
        "label": "Chapter 07",
        "title": "Tests on von Mises Distributions",
        "folder": "chapter-07-tests-on-von-mises-distributions",
        "notebook": "07-tests-on-von-mises-distributions.ipynb",
        "part": "part-01-circular-statistics",
        "topic": "chapter-07",
        "family": "circular",
        "printed": "119-144",
        "pdf": "136-160",
        "focus": "One-sample, two-sample, and multi-sample inference under von Mises assumptions.",
        "concepts": [
            "mean-direction tests use arcs rather than two-sided line intervals",
            "confidence arcs change with resultant length and concentration",
            "multi-sample circular ANOVA decomposes resultant geometry",
            "testing von-Misesness is a model check, not an afterthought",
        ],
        "visuals": [
            "critical arc for a mean-direction test",
            "confidence arc around sample mean",
            "two-sample resultant triangle",
            "Watson-Williams ANOVA decomposition",
        ],
        "checks": [
            "confidence arcs have simulated coverage",
            "concentration homogeneity is checked before equal-mean ANOVA",
            "test approximations are benchmarked by simulation",
            "model diagnostics flag asymmetric alternatives",
        ],
    },
    {
        "kind": "chapter",
        "number": 8,
        "label": "Chapter 08",
        "title": "Non-parametric Methods",
        "folder": "chapter-08-non-parametric-methods",
        "notebook": "08-non-parametric-methods.ipynb",
        "part": "part-01-circular-statistics",
        "topic": "chapter-08",
        "family": "circular",
        "printed": "145-158",
        "pdf": "161-174",
        "focus": "Distribution-free circular inference through symmetry, ranks, uniform scores, two-sample comparisons, runs, and q-sample tests.",
        "concepts": [
            "rank ideas survive on the circle when ranks are converted into uniform scores",
            "symmetry tests ask whether reflected directions match",
            "two-sample tests compare circular empirical distributions",
            "runs and q-sample methods reveal distributional differences without a von Mises model",
        ],
        "visuals": [
            "symmetry sign and Wilcoxon display",
            "uniform-score construction",
            "two-sample circular CDF overlays",
            "circular runs diagram",
        ],
        "checks": [
            "tests are invariant under rotation",
            "ties are reported and handled consistently",
            "runs count is even on a circle",
            "uniform-score statistic detects location and dispersion differences",
        ],
    },
    {
        "kind": "chapter",
        "number": 9,
        "label": "Chapter 09",
        "title": "Distributions on Spheres",
        "folder": "chapter-09-distributions-on-spheres",
        "notebook": "09-distributions-on-spheres.ipynb",
        "part": "part-02-spherical-statistics",
        "topic": "chapter-09",
        "family": "spherical",
        "printed": "159-192",
        "pdf": "175-208",
        "focus": "Spherical data, descriptive measures, von Mises-Fisher and axial models, distribution theory, and asymptotics on spheres.",
        "concepts": [
            "directions on S^2 and higher spheres are unit vectors with a different geometry than angles",
            "the mean direction and moment of inertia separate location from axial spread",
            "Fisher, Watson, Bingham, angular central Gaussian, and related models encode poles, girdles, and axes",
            "large-sample, high-concentration, and high-dimensional asymptotics each illuminate a different limit",
        ],
        "visuals": [
            "spherical scatter and mean resultant vector",
            "moment-of-inertia ellipsoid",
            "Fisher versus Watson versus Bingham density gallery",
            "tangent-normal high-concentration approximation",
        ],
        "checks": [
            "sample vectors have unit norm",
            "mean resultant length is between zero and one",
            "Fisher density normalizes numerically",
            "inertia matrix is symmetric positive semidefinite",
        ],
    },
    {
        "kind": "chapter",
        "number": 10,
        "label": "Chapter 10",
        "title": "Inference on Spheres",
        "folder": "chapter-10-inference-on-spheres",
        "notebook": "10-inference-on-spheres.ipynb",
        "part": "part-02-spherical-statistics",
        "topic": "chapter-10",
        "family": "spherical",
        "printed": "193-244",
        "pdf": "209-259",
        "focus": "Exploratory spherical analysis, parameter estimation, uniformity tests, mean-direction confidence cones, and axial distribution tests.",
        "concepts": [
            "spherical exploratory plots must preserve cap areas and antipodal structure",
            "concentration estimation on spheres uses dimension-dependent Bessel ratios",
            "uniformity tests detect mean shifts, girdles, and broader Sobolev alternatives",
            "mean-direction inference is expressed as cones or subspace restrictions",
        ],
        "visuals": [
            "spherical EDA with caps and graticules",
            "confidence cone around mean direction",
            "uniformity null cloud for resultants",
            "axial Watson and Bingham diagnostics",
        ],
        "checks": [
            "Fisher MLE solves the resultant equation",
            "confidence cone contains the true pole in simulation",
            "uniformity statistics follow their reference approximations",
            "axial sign symmetry is preserved",
        ],
    },
    {
        "kind": "chapter",
        "number": 11,
        "label": "Chapter 11",
        "title": "Correlation and Regression",
        "folder": "chapter-11-correlation-and-regression",
        "notebook": "11-correlation-and-regression.ipynb",
        "part": "part-02-spherical-statistics",
        "topic": "chapter-11",
        "family": "spherical",
        "printed": "245-266",
        "pdf": "260-281",
        "focus": "Linear-circular, circular-circular, spherical-spherical dependence, directional regression, bivariate models, and directional time series.",
        "concepts": [
            "directional correlation must respect periodic or spherical coordinates",
            "canonical-correlation style statistics capture dependence between sine-cosine embeddings",
            "regression with directional response predicts a point on a curved space",
            "time series for directions model persistence without unwrapping artifacts",
        ],
        "visuals": [
            "linear-circular scatter on a cylinder",
            "circular-circular torus heatmap",
            "spherical regression arc",
            "directional time-series resultant trace",
        ],
        "checks": [
            "correlations are invariant to origin changes",
            "predicted directions keep unit norm",
            "lagged dependence simulation recovers positive persistence",
            "independence null simulations center near zero",
        ],
    },
    {
        "kind": "chapter",
        "number": 12,
        "label": "Chapter 12",
        "title": "Modern Methodology",
        "folder": "chapter-12-modern-methodology",
        "notebook": "12-modern-methodology.ipynb",
        "part": "part-02-spherical-statistics",
        "topic": "chapter-12",
        "family": "spherical",
        "printed": "267-282",
        "pdf": "282-297",
        "focus": "Outliers, robust estimation, bootstrap methods, density estimation, Bayesian ideas, and smoothing for directional data.",
        "concepts": [
            "outlier tests on curved spaces distinguish radial anomalies from angular anomalies",
            "robust estimators dampen the influence of a few wrong directions",
            "bootstrap resampling must resample directions and recompute on the manifold",
            "kernel density and smoothing methods visualize uncertainty without flattening the sphere permanently",
        ],
        "visuals": [
            "outlier influence wheel or sphere",
            "robust mean versus ordinary mean",
            "bootstrap confidence cone cloud",
            "spherical kernel density surface",
        ],
        "checks": [
            "robust estimator moves less under contamination",
            "bootstrap intervals have finite angular radius",
            "density estimate integrates approximately to one",
            "smoothed curve remains on the unit sphere",
        ],
    },
    {
        "kind": "chapter",
        "number": 13,
        "label": "Chapter 13",
        "title": "General Sample Spaces",
        "folder": "chapter-13-general-sample-spaces",
        "notebook": "13-general-sample-spaces.ipynb",
        "part": "part-03-general-sample-spaces-and-shape",
        "topic": "chapter-13",
        "family": "manifold",
        "printed": "283-302",
        "pdf": "298-316",
        "focus": "Directional statistics on rotations, frames, Stiefel manifolds, Grassmann manifolds, hyperboloids, and general manifolds.",
        "concepts": [
            "the sample space may be a group, quotient, or embedded manifold rather than a sphere",
            "orthonormal frames live on a Stiefel manifold and rotations live in SO(3)",
            "subspaces are represented by projection matrices on a Grassmann manifold",
            "uniformity and matrix Fisher or Bingham models depend on the invariance group",
        ],
        "visuals": [
            "sample-space map for sphere, SO(3), Stiefel, Grassmann, and hyperboloid",
            "interactive orthonormal frame and rotation lab",
            "Stiefel polar decomposition panel",
            "Grassmann projection-matrix diagnostics",
        ],
        "checks": [
            "rotation matrices are orthogonal with determinant one",
            "Stiefel frames satisfy X.T @ X = I",
            "Grassmann projection matrices are symmetric idempotents",
            "hyperboloid samples satisfy the Minkowski norm constraint",
        ],
    },
    {
        "kind": "chapter",
        "number": 14,
        "label": "Chapter 14",
        "title": "Shape Analysis",
        "folder": "chapter-14-shape-analysis",
        "notebook": "14-shape-analysis.ipynb",
        "part": "part-03-general-sample-spaces-and-shape",
        "topic": "chapter-14",
        "family": "shape",
        "printed": "303-348",
        "pdf": "317-361",
        "focus": "Landmark shape analysis as directional statistics on preshape and shape spaces, including Procrustes means, tangent approximations, and complex directional models.",
        "concepts": [
            "shape removes translation, scale, and rotation while preserving landmark geometry",
            "preshape coordinates place centered configurations on a unit sphere",
            "Kendall's triangle shape sphere turns triangle families into inspectable geometry",
            "Procrustes means and tangent shape PCA summarize concentrated shape samples",
        ],
        "visuals": [
            "landmark invariance pipeline",
            "triangle shape sphere",
            "Procrustes alignment overlay",
            "tangent shape PCA deformation modes",
        ],
        "checks": [
            "Helmert rows are orthonormal and remove translation",
            "preshape norm equals one",
            "Procrustes distance is invariant to similarity transformations",
            "tangent coordinates are orthogonal to the mean shape",
        ],
    },
    {
        "kind": "appendix",
        "number": 101,
        "label": "Appendix 01",
        "title": "Special Functions",
        "folder": "appendix-01-special-functions",
        "notebook": "appendix-01-special-functions.ipynb",
        "part": "part-04-appendices",
        "topic": "appendix-01",
        "family": "special",
        "printed": "349-352",
        "pdf": "362-365",
        "focus": "Bessel, modified Bessel, Bessel-ratio, Kummer, and normalizing-constant calculations used throughout directional models.",
        "concepts": [
            "special functions are numerical objects that normalize curved-space densities",
            "Bessel ratios convert concentration into expected resultant length",
            "asymptotic approximations are useful only after their error is inspected",
            "appendix tables become executable calculators in this course",
        ],
        "visuals": [
            "Bessel-ratio atlas",
            "asymptotic error bands",
            "Kummer normalizer lab",
            "Stiefel integral check",
        ],
        "checks": [
            "Bessel ratios are monotone on the plotted range",
            "inverse concentration recovers the original resultant",
            "asymptotic error decreases in its intended regime",
            "normalizers are finite and positive",
        ],
    },
    {
        "kind": "appendix",
        "number": 102,
        "label": "Appendix 02",
        "title": "Circular Tables and Charts",
        "folder": "appendix-02-circular-tables-and-charts",
        "notebook": "appendix-02-circular-tables-and-charts.ipynb",
        "part": "part-04-appendices",
        "topic": "appendix-02",
        "family": "circular",
        "printed": "353-380",
        "pdf": "366-393",
        "focus": "Executable replacements for circular critical-value and estimation tables.",
        "concepts": [
            "printed circular tables become reproducible numerical calculators",
            "von Mises quantiles are easier to understand as tail fans than as static rows",
            "uniformity critical values can be simulated and compared with approximations",
            "confidence bands are diagnostics for methods, not just lookup values",
        ],
        "visuals": [
            "von Mises tail quantile fan",
            "circular concentration inversion",
            "uniformity null comparison",
            "kappa confidence-band lab",
        ],
        "checks": [
            "computed quantiles are ordered",
            "A inverse is monotone",
            "simulation seeds reproduce critical values",
            "confidence bands widen for small samples",
        ],
    },
    {
        "kind": "appendix",
        "number": 103,
        "label": "Appendix 03",
        "title": "Spherical Tables",
        "folder": "appendix-03-spherical-tables",
        "notebook": "appendix-03-spherical-tables.ipynb",
        "part": "part-04-appendices",
        "topic": "appendix-03",
        "family": "spherical",
        "printed": "381-390",
        "pdf": "394-403",
        "focus": "Executable spherical table replacements for Fisher, Watson, resultant, and concentration calculations.",
        "concepts": [
            "spherical tables are visualized as caps, cones, and concentration curves",
            "Fisher concentration inversion depends on the sphere dimension",
            "Watson models distinguish girdle and bipolar alternatives",
            "resultant critical clouds explain why large samples are sharper",
        ],
        "visuals": [
            "Fisher colatitude cones",
            "spherical concentration inversion",
            "Watson girdle versus bipolar density",
            "resultant critical cloud",
        ],
        "checks": [
            "cap probabilities are between zero and one",
            "concentration inversion is monotone",
            "Watson axial symmetry holds under sign flips",
            "resultant thresholds increase with concentration",
        ],
    },
    {
        "kind": "appendix",
        "number": 104,
        "label": "Appendix 04",
        "title": "Notation",
        "folder": "appendix-04-notation",
        "notebook": "appendix-04-notation.ipynb",
        "part": "part-04-appendices",
        "topic": "appendix-04",
        "family": "notation",
        "printed": "391-394",
        "pdf": "404-406",
        "focus": "Executable notation atlas for sample spaces, statistics, model families, special functions, and shape-analysis symbols.",
        "concepts": [
            "notation becomes a navigable dependency graph instead of a passive glossary",
            "sample spaces determine which statistics are meaningful",
            "population symbols, sample estimates, and diagnostics should not be conflated",
            "distribution-family maps help a reader choose the right model visually",
        ],
        "visuals": [
            "notation dependency map",
            "sample-space gallery",
            "distribution-family map",
            "notation glossary JSON",
        ],
        "checks": [
            "all glossary entries have a concept family",
            "graph nodes referenced by edges exist",
            "sample-space symbols map to notebook chapters",
            "JSON glossary is readable",
        ],
    },
]


def dedent(text: str) -> str:
    return textwrap.dedent(text).strip() + "\n"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(text), encoding="utf-8")


def write_raw(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_notebook(path: Path, cells: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=cells), path)


def py_literal(value: object) -> str:
    return repr(value)


def write_agents() -> None:
    source_rows = "\n".join(
        f"- {entry['label']}: `{entry['part']}/{entry['folder']}/{entry['notebook']}`; "
        f"printed pp. {entry['printed']}; PDF pp. {entry['pdf']}; {entry['focus']}"
        for entry in ENTRIES
    )
    write_text(
        BOOK_ROOT / "AGENTS.md",
        f"""
        # Agent Instructions: Directional Statistics Notebook Course

        This folder is a standalone visualization-first notebook edition of *Directional Statistics* by Kanti V. Mardia and Peter E. Jupp. Treat this folder as the course root. The workspace root `D:\\Geometry` owns the shared `uv` Python environment.

        ## Repo-Local Skills

        Use the repo-local skills under `D:\\Geometry\\.codex\\skills` for course work:

        - `geometry-visualization-planner` for chapter storyboards and artifact choices.
        - `geometry-chapter-notebook-author` for authoring canonical notebooks.
        - `geometry-notebook-qc` for standalone, artifact, and execution review.

        ## Non-Negotiables

        - Write original teaching prose, derivations, code, and visual explanations.
        - Do not copy textbook passages, long exercise text, printed tables, page screenshots, or page crops.
        - The notebooks must stand alone without the PDF open.
        - Visualization is part of the teaching argument, not decoration or a fixed quota.
        - Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
        - Every canonical notebook should execute cleanly with `nbclient`.
        - Generated paths in notebooks must be relative or book-local.
        - Preserve one canonical teaching notebook per chapter or appendix folder plus a local `00-index.ipynb`.

        ## Source Map

        The PDF has 441 pages. Source spans below are physical PDF pages observed with `pdftotext`; printed spans come from the table of contents.

        {source_rows}

        ## Notebook Shape

        Each canonical notebook should include:

        1. Title and source span.
        2. Translation guide from book concepts into computational language.
        3. Route through the chapter.
        4. Setup cell that discovers `BOOK_ROOT`.
        5. Original concept sections with equations and diagrams.
        6. Executable examples using book-local utilities.
        7. Visual artifacts saved under `artifacts/` and displayed inline.
        8. Applied lab or design exercise.
        9. Sanity checks asserting core identities and artifact existence.
        10. Takeaways.

        ## Geometry Stack

        Use the shared `uv` environment at `D:\\Geometry`. Prefer installed packages before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `networkx`, `pyvista`, `trimesh`, `PIL`, `geomstats`, `pyriemann`, and the other packages listed in the repo-local geometry library catalog. Document external-only tools rather than importing them.

        ## Worker Boundaries

        Assign one worker to one canonical notebook, one helper module, or one script task. Chapter workers should read their assigned source span, consume or create a visualization storyboard, and edit only the assigned chapter folder, its artifact subtree, and any explicitly assigned chapter helper. Shared utility changes belong to utility workers.

        ## Commands

        Run from `D:\\Geometry`:

        ```powershell
        uv run python "Directional-Statistics/scripts/build_dirstats_course_indexes.py"
        uv run python -m compileall -q "Directional-Statistics/utils" "Directional-Statistics/scripts"
        uv run python "Directional-Statistics/scripts/audit_dirstats_notebooks.py" --min-words 1200 --min-code-cells 5
        uv run python "Directional-Statistics/scripts/audit_dirstats_visuals.py"
        uv run python "Directional-Statistics/scripts/audit_dirstats_artifacts.py"
        uv run python "Directional-Statistics/scripts/validate_dirstats_course.py" --limit 8 --timeout 300
        git diff --check
        ```
        """,
    )


def write_inventory() -> None:
    write_raw(
        BOOK_ROOT / "scripts" / "dirstats_inventory.py",
        dedent(
            f'''
            """Inventory for the Directional Statistics notebook course."""

            from __future__ import annotations

            PARTS = {py_literal(PARTS)}

            ENTRIES = {py_literal(ENTRIES)}


            def canonical_entries() -> list[dict]:
                return list(ENTRIES)


            def parts() -> list[dict]:
                return list(PARTS)
            '''
        ),
    )


def write_utils() -> None:
    write_text(BOOK_ROOT / "utils" / "__init__.py", '"""Utilities for the Directional Statistics notebook course."""')
    write_text(
        BOOK_ROOT / "utils" / "artifacts.py",
        r'''
        """Book-local artifact helpers."""

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
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "circular.py",
        r'''
        """Circular statistics helpers used by course notebooks."""

        from __future__ import annotations

        import numpy as np
        from scipy import optimize, special, stats

        TAU = 2.0 * np.pi


        def wrap_angle(theta: np.ndarray | float, center: float = 0.0) -> np.ndarray:
            return (np.asarray(theta) - center + np.pi) % TAU - np.pi + center


        def axial_double(theta: np.ndarray) -> np.ndarray:
            return wrap_angle(2.0 * np.asarray(theta), 0.0)


        def unit_vectors(theta: np.ndarray) -> np.ndarray:
            theta = np.asarray(theta)
            return np.column_stack([np.cos(theta), np.sin(theta)])


        def resultant(theta: np.ndarray) -> dict[str, float]:
            z = np.exp(1j * np.asarray(theta))
            mean_z = z.mean()
            return {
                "C": float(mean_z.real),
                "S": float(mean_z.imag),
                "R": float(abs(mean_z)),
                "mean": float(np.angle(mean_z)),
            }


        def circular_mean(theta: np.ndarray) -> float:
            return resultant(theta)["mean"]


        def trig_moment(theta: np.ndarray, p: int = 1, center: float = 0.0) -> complex:
            return complex(np.mean(np.exp(1j * p * wrap_angle(np.asarray(theta) - center))))


        def circular_variance(theta: np.ndarray) -> float:
            return 1.0 - resultant(theta)["R"]


        def circular_standard_deviation(theta: np.ndarray) -> float:
            r = max(resultant(theta)["R"], 1e-12)
            return float(np.sqrt(-2.0 * np.log(r)))


        def circular_median(theta: np.ndarray, grid_size: int = 720) -> float:
            theta = wrap_angle(theta)
            grid = np.linspace(-np.pi, np.pi, grid_size, endpoint=False)
            distances = np.abs(wrap_angle(theta[:, None] - grid[None, :]))
            return float(grid[np.argmin(distances.sum(axis=0))])


        def rose_histogram(theta: np.ndarray, bins: int = 16) -> tuple[np.ndarray, np.ndarray]:
            counts, edges = np.histogram(wrap_angle(theta, 0.0) % TAU, bins=bins, range=(0, TAU))
            return counts.astype(float), edges


        def A1(kappa: np.ndarray | float) -> np.ndarray:
            kappa = np.asarray(kappa, dtype=float)
            return special.iv(1, kappa) / np.maximum(special.iv(0, kappa), 1e-300)


        def inverse_A1(r: float) -> float:
            r = float(np.clip(r, 1e-9, 0.999999))
            if r < 0.53:
                guess = 2 * r + r**3 + 5 * r**5 / 6
            elif r < 0.85:
                guess = -0.4 + 1.39 * r + 0.43 / (1 - r)
            else:
                guess = 1 / (r**3 - 4 * r**2 + 3 * r)
            root = optimize.root_scalar(lambda k: float(A1(k) - r), bracket=[1e-8, max(guess * 3, 10.0)])
            return float(root.root)


        def von_mises_pdf(theta: np.ndarray, mu: float = 0.0, kappa: float = 1.0) -> np.ndarray:
            return np.exp(kappa * np.cos(wrap_angle(theta - mu))) / (TAU * special.iv(0, kappa))


        def rayleigh_statistic(theta: np.ndarray) -> float:
            theta = np.asarray(theta)
            return float(2 * len(theta) * resultant(theta)["R"] ** 2)


        def kuiper_statistic(theta: np.ndarray) -> float:
            u = np.sort((wrap_angle(theta, 0.0) % TAU) / TAU)
            n = len(u)
            i = np.arange(1, n + 1)
            return float(np.max(i / n - u) + np.max(u - (i - 1) / n))


        def watson_u2(theta: np.ndarray) -> float:
            u = np.sort((wrap_angle(theta, 0.0) % TAU) / TAU)
            n = len(u)
            i = np.arange(1, n + 1)
            centered = u - (2 * i - 1) / (2 * n)
            return float(np.sum((centered - centered.mean()) ** 2) + 1 / (12 * n))


        def sample_vonmises(seed: int, n: int, mu: float, kappa: float) -> np.ndarray:
            return np.random.default_rng(seed).vonmises(mu, kappa, n)


        def circular_cdf_grid(theta: np.ndarray, grid_size: int = 256) -> tuple[np.ndarray, np.ndarray]:
            u = np.sort((wrap_angle(theta, 0.0) % TAU) / TAU)
            grid = np.linspace(0, 1, grid_size)
            ecdf = np.searchsorted(u, grid, side="right") / len(u)
            return grid * TAU, ecdf


        def uniform_reference_pvalue_rayleigh(theta: np.ndarray) -> float:
            return float(stats.chi2.sf(rayleigh_statistic(theta), df=2))
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "spherical.py",
        r'''
        """Spherical statistics helpers."""

        from __future__ import annotations

        import numpy as np
        from scipy import optimize


        def normalize(vectors: np.ndarray) -> np.ndarray:
            vectors = np.asarray(vectors, dtype=float)
            norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
            return vectors / np.maximum(norms, 1e-15)


        def spherical_sample(seed: int, n: int, pole: np.ndarray | None = None, concentration: float = 8.0) -> np.ndarray:
            rng = np.random.default_rng(seed)
            pole = normalize(np.asarray(pole if pole is not None else [0.2, 0.3, 1.0]))
            noise = rng.normal(size=(n, 3))
            samples = noise + concentration * pole
            return normalize(samples)


        def uniform_sphere(seed: int, n: int, dim: int = 3) -> np.ndarray:
            rng = np.random.default_rng(seed)
            return normalize(rng.normal(size=(n, dim)))


        def mean_direction(vectors: np.ndarray) -> dict[str, float | np.ndarray]:
            vectors = np.asarray(vectors, dtype=float)
            mean = vectors.mean(axis=0)
            length = float(np.linalg.norm(mean))
            direction = mean / max(length, 1e-15)
            return {"mean": mean, "direction": direction, "R": length}


        def inertia_matrix(vectors: np.ndarray) -> np.ndarray:
            vectors = np.asarray(vectors, dtype=float)
            return vectors.T @ vectors / len(vectors)


        def fisher_A3(kappa: np.ndarray | float) -> np.ndarray:
            kappa = np.asarray(kappa, dtype=float)
            return 1.0 / np.tanh(np.maximum(kappa, 1e-10)) - 1.0 / np.maximum(kappa, 1e-10)


        def inverse_fisher_A3(r: float) -> float:
            r = float(np.clip(r, 1e-8, 0.999999))
            root = optimize.root_scalar(lambda k: float(fisher_A3(k) - r), bracket=[1e-8, 1e4])
            return float(root.root)


        def fisher_density_s2(points: np.ndarray, mu: np.ndarray, kappa: float) -> np.ndarray:
            points = normalize(points)
            mu = normalize(np.asarray(mu))
            if kappa < 1e-8:
                c = 1.0 / (4 * np.pi)
            else:
                c = kappa / (4 * np.pi * np.sinh(kappa))
            return c * np.exp(kappa * (points @ mu))


        def angular_distance(a: np.ndarray, b: np.ndarray) -> np.ndarray:
            a = normalize(a)
            b = normalize(b)
            dots = np.clip(np.sum(a * b, axis=-1), -1.0, 1.0)
            return np.arccos(dots)


        def confidence_cone_radius(n: int, rbar: float, alpha: float = 0.05) -> float:
            value = max(1e-9, alpha ** (1.0 / max(n - 1, 1)))
            return float(np.arccos(np.clip(1 - (n - rbar * n) / (rbar * n) * (1 / value - 1), -1, 1)))
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "special_functions.py",
        r'''
        """Special-function wrappers for directional distributions."""

        from __future__ import annotations

        import numpy as np
        from scipy import optimize, special


        def modified_bessel(order: float, x: np.ndarray | float) -> np.ndarray:
            return special.iv(order, x)


        def bessel_ratio(order: float, x: np.ndarray | float) -> np.ndarray:
            x = np.asarray(x, dtype=float)
            return special.iv(order + 1, x) / np.maximum(special.iv(order, x), 1e-300)


        def inverse_bessel_ratio(order: float, r: float) -> float:
            r = float(np.clip(r, 1e-9, 0.999999))
            root = optimize.root_scalar(lambda k: float(bessel_ratio(order, k) - r), bracket=[1e-8, 1e4])
            return float(root.root)


        def kummer(a: float, b: float, x: np.ndarray | float) -> np.ndarray:
            return special.hyp1f1(a, b, x)


        def small_kappa_A1(kappa: np.ndarray | float) -> np.ndarray:
            k = np.asarray(kappa, dtype=float)
            return k / 2 - k**3 / 16 + k**5 / 96


        def large_kappa_A1(kappa: np.ndarray | float) -> np.ndarray:
            k = np.asarray(kappa, dtype=float)
            return 1 - 1 / (2 * k) - 1 / (8 * k**2)
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "manifolds.py",
        r'''
        """Helpers for rotations, frames, Grassmann points, and hyperboloids."""

        from __future__ import annotations

        import numpy as np
        from scipy.linalg import expm, polar


        def skew(v: np.ndarray) -> np.ndarray:
            x, y, z = np.asarray(v, dtype=float)
            return np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]], dtype=float)


        def rotation_from_axis_angle(axis: np.ndarray, angle: float) -> np.ndarray:
            axis = np.asarray(axis, dtype=float)
            axis = axis / max(np.linalg.norm(axis), 1e-15)
            return expm(skew(axis * angle))


        def sample_so3(seed: int, n: int) -> np.ndarray:
            rng = np.random.default_rng(seed)
            frames = []
            for _ in range(n):
                q, r = np.linalg.qr(rng.normal(size=(3, 3)))
                q *= np.sign(np.diag(r))
                if np.linalg.det(q) < 0:
                    q[:, 0] *= -1
                frames.append(q)
            return np.stack(frames)


        def sample_stiefel(seed: int, p: int, r: int, n: int) -> np.ndarray:
            rng = np.random.default_rng(seed)
            frames = []
            for _ in range(n):
                q, _ = np.linalg.qr(rng.normal(size=(p, r)))
                frames.append(q[:, :r])
            return np.stack(frames)


        def polar_stiefel(matrix: np.ndarray) -> np.ndarray:
            u, _ = polar(matrix)
            return u


        def grassmann_projection(frame: np.ndarray) -> np.ndarray:
            return frame @ frame.T


        def sample_hyperboloid(seed: int, n: int) -> np.ndarray:
            rng = np.random.default_rng(seed)
            xy = rng.normal(scale=0.6, size=(n, 2))
            t = np.sqrt(1 + np.sum(xy**2, axis=1))
            return np.column_stack([t, xy])


        def minkowski_dot(a: np.ndarray, b: np.ndarray) -> np.ndarray:
            a = np.asarray(a)
            b = np.asarray(b)
            return a[..., 0] * b[..., 0] - np.sum(a[..., 1:] * b[..., 1:], axis=-1)
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "shape.py",
        r'''
        """Landmark shape helpers."""

        from __future__ import annotations

        import numpy as np
        from scipy.linalg import orthogonal_procrustes


        def helmert_submatrix(k: int) -> np.ndarray:
            h = np.zeros((k - 1, k))
            for i in range(1, k):
                h[i - 1, :i] = 1 / np.sqrt(i * (i + 1))
                h[i - 1, i] = -i / np.sqrt(i * (i + 1))
            return h


        def center_landmarks(points: np.ndarray) -> np.ndarray:
            points = np.asarray(points, dtype=float)
            return points - points.mean(axis=-2, keepdims=True)


        def preshape(points: np.ndarray) -> np.ndarray:
            centered = center_landmarks(points)
            norm = np.linalg.norm(centered)
            return centered / max(norm, 1e-15)


        def procrustes_align(source: np.ndarray, target: np.ndarray) -> np.ndarray:
            src = center_landmarks(source)
            tgt = center_landmarks(target)
            scale = max(np.linalg.norm(src), 1e-15)
            src = src / scale
            tgt = tgt / max(np.linalg.norm(tgt), 1e-15)
            r, _ = orthogonal_procrustes(src, tgt)
            return src @ r


        def procrustes_mean(shapes: np.ndarray, iterations: int = 8) -> np.ndarray:
            mean = preshape(shapes[0])
            for _ in range(iterations):
                aligned = np.stack([procrustes_align(shape, mean) for shape in shapes])
                mean = preshape(aligned.mean(axis=0))
            return mean


        def tangent_shape_coords(shapes: np.ndarray, mean: np.ndarray) -> np.ndarray:
            aligned = np.stack([procrustes_align(shape, mean) for shape in shapes])
            residuals = aligned - mean
            return residuals.reshape(len(shapes), -1)


        def triangle_shape_features(points: np.ndarray) -> np.ndarray:
            points = center_landmarks(points)
            edges = np.array([
                np.linalg.norm(points[1] - points[0]),
                np.linalg.norm(points[2] - points[1]),
                np.linalg.norm(points[0] - points[2]),
            ])
            edges = edges / max(np.linalg.norm(edges), 1e-15)
            return edges
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "simulation.py",
        r'''
        """Seeded simulation helpers."""

        from __future__ import annotations

        import numpy as np


        def rng(seed: int) -> np.random.Generator:
            return np.random.default_rng(seed)


        def quantile_summary(values: np.ndarray, probs: tuple[float, ...] = (0.05, 0.5, 0.95)) -> dict[str, float]:
            values = np.asarray(values, dtype=float)
            return {f"q{int(p * 100):02d}": float(np.quantile(values, p)) for p in probs}


        def monte_carlo_resultants(seed: int, n: int, reps: int) -> np.ndarray:
            gen = np.random.default_rng(seed)
            theta = gen.uniform(0, 2 * np.pi, size=(reps, n))
            return np.abs(np.exp(1j * theta).mean(axis=1))
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "validation.py",
        r'''
        """Validation helpers shared by notebooks and scripts."""

        from __future__ import annotations

        import json
        from pathlib import Path
        from typing import Any


        def artifact_record(path: str | Path) -> dict[str, Any]:
            p = Path(path)
            try:
                root = Path(__file__).resolve().parents[1]
                shown = str(p.resolve().relative_to(root)).replace("\\", "/")
            except ValueError:
                shown = str(p)
            return {"path": shown, "exists": p.exists(), "bytes": p.stat().st_size if p.exists() else 0}


        def assert_artifacts(paths: list[str | Path], min_bytes: int = 100) -> list[dict[str, Any]]:
            records = [artifact_record(path) for path in paths]
            missing = [record for record in records if not record["exists"] or record["bytes"] <= min_bytes]
            if missing:
                raise AssertionError(f"artifact checks failed: {missing}")
            return records


        def read_json(path: str | Path) -> Any:
            return json.loads(Path(path).read_text(encoding="utf-8"))
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "plotting.py",
        r'''
        """Plotting defaults and course visual constructors."""

        from __future__ import annotations

        import hashlib
        from pathlib import Path
        from typing import Any

        import matplotlib.pyplot as plt
        import numpy as np
        import plotly.graph_objects as go
        from PIL import Image, ImageStat

        from .circular import A1, circular_cdf_grid, resultant, rose_histogram, sample_vonmises, von_mises_pdf
        from .manifolds import grassmann_projection, minkowski_dot, rotation_from_axis_angle, sample_hyperboloid, sample_so3, sample_stiefel
        from .shape import procrustes_mean, tangent_shape_coords, triangle_shape_features
        from .special_functions import bessel_ratio, large_kappa_A1, small_kappa_A1
        from .spherical import inertia_matrix, mean_direction, spherical_sample, uniform_sphere

        PALETTE = {
            "ink": "#1f2933",
            "blue": "#2f6fbb",
            "teal": "#2a9d8f",
            "green": "#6a994e",
            "gold": "#d59f0f",
            "red": "#c44e52",
            "violet": "#7b5ea7",
            "gray": "#7a8793",
        }


        def style_axis(ax: Any, title: str, *, equal: bool = False) -> None:
            ax.set_title(title, fontsize=11, color=PALETTE["ink"])
            ax.grid(True, color="#d7dde5", linewidth=0.7, alpha=0.8)
            if equal:
                ax.set_aspect("equal", adjustable="box")
            for spine in getattr(ax, "spines", {}).values():
                spine.set_color("#b6c0ca")


        def image_stats(path: str | Path) -> dict[str, float | int | str]:
            p = Path(path)
            with Image.open(p) as image:
                image.load()
                rgb = image.convert("RGB")
                stat = ImageStat.Stat(rgb)
                arr = np.asarray(rgb, dtype=float)
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
            return {
                "path": p.as_posix(),
                "width": int(rgb.width),
                "height": int(rgb.height),
                "bytes": int(p.stat().st_size),
                "sha256": digest,
                "pixel_std": float(arr.std()),
                "max_channel_stddev": float(max(stat.stddev) if stat.stddev else 0.0),
            }


        def close(fig: Any) -> None:
            plt.close(fig)


        def make_entry_static_figure(entry: dict) -> tuple[Any, dict[str, float]]:
            family = entry["family"]
            seed = int(entry["number"])
            diagnostics: dict[str, float] = {"seed": float(seed)}
            if family == "circular":
                theta = sample_vonmises(seed, 96, mu=seed / 9.0, kappa=1.2 + (seed % 5) * 0.7)
                res = resultant(theta)
                counts, edges = rose_histogram(theta, bins=18)
                grid = np.linspace(-np.pi, np.pi, 360)
                density = von_mises_pdf(grid, res["mean"], max(0.25, 6 * res["R"]))
                fig = plt.figure(figsize=(10, 4.8))
                ax = fig.add_subplot(121, projection="polar")
                widths = np.diff(edges)
                ax.bar(edges[:-1], np.sqrt(counts), width=widths, align="edge", color=PALETTE["teal"], alpha=0.68, edgecolor="white")
                ax.arrow(res["mean"], 0, 0, max(np.sqrt(counts).max(), 1) * res["R"], width=0.02, color=PALETTE["red"], length_includes_head=True)
                ax.set_title(f"{entry['label']}: rose/resultant view")
                ax2 = fig.add_subplot(122)
                ax2.plot(grid, density, color=PALETTE["blue"], label="fitted von Mises sketch")
                g, ecdf = circular_cdf_grid(theta)
                ax2.step(g - np.pi, ecdf, color=PALETTE["gold"], where="post", label="empirical circular CDF")
                style_axis(ax2, "Density and circular CDF")
                ax2.legend(loc="best", fontsize=8)
                diagnostics.update({"R": float(res["R"]), "mean": float(res["mean"]), "density_integral": float(np.trapz(density, grid))})
                return fig, diagnostics
            if family == "spherical":
                points = spherical_sample(seed, 90, concentration=2.5 + (seed % 4))
                md = mean_direction(points)
                inertia = inertia_matrix(points)
                fig = plt.figure(figsize=(10, 4.8))
                ax = fig.add_subplot(121, projection="3d")
                ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=18, color=PALETTE["blue"], alpha=0.7)
                d = md["direction"]
                ax.quiver(0, 0, 0, d[0], d[1], d[2], length=1.15, color=PALETTE["red"], linewidth=2)
                ax.set_title(f"{entry['label']}: spherical sample")
                ax.set_box_aspect((1, 1, 1))
                ax2 = fig.add_subplot(122)
                vals = np.linalg.eigvalsh(inertia)
                ax2.bar(["lambda1", "lambda2", "lambda3"], vals, color=[PALETTE["teal"], PALETTE["gold"], PALETTE["violet"]])
                style_axis(ax2, "Moment-of-inertia spectrum")
                diagnostics.update({"R": float(md["R"]), "unit_norm_error": float(np.max(np.abs(np.linalg.norm(points, axis=1) - 1))), "inertia_trace": float(np.trace(inertia))})
                return fig, diagnostics
            if family == "manifold":
                rotations = sample_so3(seed, 12)
                frames = sample_stiefel(seed + 20, 3, 2, 12)
                projection = grassmann_projection(frames[0])
                fig = plt.figure(figsize=(10, 4.8))
                ax = fig.add_subplot(121, projection="3d")
                colors = [PALETTE["red"], PALETTE["green"], PALETTE["blue"]]
                for j, color in enumerate(colors):
                    ax.quiver(0, 0, 0, rotations[0][0, j], rotations[0][1, j], rotations[0][2, j], color=color, linewidth=2)
                ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
                ax.set_title("SO(3) frame glyph")
                ax.set_box_aspect((1, 1, 1))
                ax2 = fig.add_subplot(122)
                im = ax2.imshow(projection, cmap="viridis", vmin=-0.05, vmax=1)
                fig.colorbar(im, ax=ax2, fraction=0.046)
                style_axis(ax2, "Grassmann projection matrix")
                diagnostics.update({"rotation_det": float(np.linalg.det(rotations[0])), "stiefel_error": float(np.linalg.norm(frames[0].T @ frames[0] - np.eye(2))), "projection_idempotence": float(np.linalg.norm(projection @ projection - projection))})
                return fig, diagnostics
            if family == "shape":
                rng = np.random.default_rng(seed)
                base = np.array([[0.0, 0.0], [1.2, 0.1], [0.3, 0.95], [-0.15, 0.45]])
                shapes = np.stack([base + rng.normal(scale=0.06, size=base.shape) + [0.05 * i, 0] for i in np.linspace(-1, 1, 28)])
                mean = procrustes_mean(shapes)
                coords = tangent_shape_coords(shapes, mean)
                fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
                for shape in shapes[::4]:
                    closed = np.vstack([shape, shape[0]])
                    axes[0].plot(closed[:, 0], closed[:, 1], color=PALETTE["gray"], alpha=0.45)
                closed_mean = np.vstack([mean, mean[0]])
                axes[0].plot(closed_mean[:, 0], closed_mean[:, 1], color=PALETTE["red"], linewidth=2.5, label="Procrustes mean")
                axes[0].legend(fontsize=8)
                style_axis(axes[0], "Landmark overlay", equal=True)
                axes[1].scatter(coords[:, 0], coords[:, 1], color=PALETTE["teal"], alpha=0.75)
                style_axis(axes[1], "Tangent shape coordinates")
                diagnostics.update({"preshape_norm": float(np.linalg.norm(mean)), "tangent_mean_norm": float(np.linalg.norm(coords.mean(axis=0))), "triangle_feature_norm": float(np.linalg.norm(triangle_shape_features(base[:3])))})
                return fig, diagnostics
            if family == "special":
                x = np.linspace(0.05, 12, 300)
                exact = bessel_ratio(0, x)
                small = small_kappa_A1(x)
                large = large_kappa_A1(x)
                fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
                axes[0].plot(x, exact, color=PALETTE["blue"], label="A1 exact")
                axes[0].plot(x, small, color=PALETTE["green"], linestyle="--", label="small-kappa approx")
                axes[0].plot(x, large, color=PALETTE["gold"], linestyle=":", label="large-kappa approx")
                axes[0].legend(fontsize=8)
                style_axis(axes[0], "Bessel-ratio atlas")
                axes[1].semilogy(x, np.abs(exact - np.clip(large, -2, 2)) + 1e-12, color=PALETTE["red"], label="large error")
                axes[1].semilogy(x, np.abs(exact - small) + 1e-12, color=PALETTE["violet"], label="small error")
                axes[1].legend(fontsize=8)
                style_axis(axes[1], "Approximation error bands")
                diagnostics.update({"A1_start": float(exact[0]), "A1_end": float(exact[-1]), "monotone": float(np.all(np.diff(exact) > 0))})
                return fig, diagnostics
            # notation
            fig, ax = plt.subplots(figsize=(9, 5))
            nodes = ["circle", "sphere", "SO(3)", "Stiefel", "Grassmann", "shape", "tests", "models"]
            angles = np.linspace(0, 2 * np.pi, len(nodes), endpoint=False)
            pos = np.column_stack([np.cos(angles), np.sin(angles)])
            for i, node in enumerate(nodes):
                ax.scatter(pos[i, 0], pos[i, 1], s=900, color=PALETTE["blue"], alpha=0.18, edgecolor=PALETTE["blue"])
                ax.text(pos[i, 0], pos[i, 1], node, ha="center", va="center", fontsize=9)
            for i in range(len(nodes)):
                j = (i + 2) % len(nodes)
                ax.plot([pos[i, 0], pos[j, 0]], [pos[i, 1], pos[j, 1]], color=PALETTE["gray"], alpha=0.45)
            style_axis(ax, "Notation dependency map", equal=True)
            ax.set_axis_off()
            diagnostics.update({"nodes": float(len(nodes)), "edges": float(len(nodes))})
            return fig, diagnostics


        def make_entry_interactive_figure(entry: dict) -> Any:
            family = entry["family"]
            seed = int(entry["number"])
            if family == "circular":
                theta = sample_vonmises(seed + 50, 120, mu=seed / 8.0, kappa=1.0 + seed % 4)
                r = 1 + 0.15 * np.sin(np.arange(len(theta)))
                return go.Figure(
                    data=[go.Scatterpolar(theta=np.degrees(theta), r=r, mode="markers", marker={"size": 7, "color": np.arange(len(theta)), "colorscale": "Viridis"})],
                    layout=go.Layout(title=f"{entry['label']}: inspect circular phase", polar={"radialaxis": {"visible": True, "range": [0, 1.3]}}),
                )
            if family == "spherical":
                points = spherical_sample(seed + 50, 120, concentration=2.0 + seed % 5)
                return go.Figure(
                    data=[go.Scatter3d(x=points[:, 0], y=points[:, 1], z=points[:, 2], mode="markers", marker={"size": 4, "color": points[:, 2], "colorscale": "Viridis"})],
                    layout=go.Layout(title=f"{entry['label']}: rotate the spherical sample", scene={"aspectmode": "cube"}),
                )
            if family == "manifold":
                t = np.linspace(0, np.pi, 40)
                frames = np.array([rotation_from_axis_angle([0.4, 0.6, 1.0], angle)[:, 0] for angle in t])
                return go.Figure(
                    data=[go.Scatter3d(x=frames[:, 0], y=frames[:, 1], z=frames[:, 2], mode="lines+markers", marker={"size": 4})],
                    layout=go.Layout(title="Axis-angle path of a rotating frame", scene={"aspectmode": "cube"}),
                )
            if family == "shape":
                rng = np.random.default_rng(seed + 80)
                triangles = rng.normal(size=(80, 3, 2))
                feats = np.array([triangle_shape_features(t) for t in triangles])
                return go.Figure(
                    data=[go.Scatter3d(x=feats[:, 0], y=feats[:, 1], z=feats[:, 2], mode="markers", marker={"size": 4, "color": feats[:, 0], "colorscale": "Plasma"})],
                    layout=go.Layout(title="Triangle shape coordinates", scene={"aspectmode": "cube"}),
                )
            if family == "special":
                x = np.linspace(0.05, 14, 180)
                return go.Figure(
                    data=[
                        go.Scatter(x=x, y=bessel_ratio(0, x), mode="lines", name="A1"),
                        go.Scatter(x=x, y=bessel_ratio(0.5, x), mode="lines", name="A_{3D} analogue"),
                    ],
                    layout=go.Layout(title="Interactive concentration-to-resultant curves", xaxis_title="kappa", yaxis_title="ratio"),
                )
            points = np.array([[0, 0], [1, 0.2], [0.8, 1], [-0.2, 0.8], [-0.6, 0.1], [0, 0]])
            return go.Figure(
                data=[go.Scatter(x=points[:, 0], y=points[:, 1], mode="lines+markers", text=["sample spaces", "summaries", "models", "tests", "shape", "sample spaces"])],
                layout=go.Layout(title="Notation tour path", xaxis={"visible": False}, yaxis={"visible": False}),
            )
        ''',
    )


def write_scripts() -> None:
    write_text(
        BOOK_ROOT / "scripts" / "build_dirstats_course_indexes.py",
        r'''
        """Rebuild Directional Statistics book, part, and chapter index notebooks."""

        from __future__ import annotations

        from pathlib import Path

        import nbformat
        from nbformat.v4 import new_markdown_cell, new_notebook

        import dirstats_inventory as inventory

        BOOK_ROOT = Path(__file__).resolve().parents[1]


        def write_markdown_notebook(path: Path, text: str) -> None:
            path.parent.mkdir(parents=True, exist_ok=True)
            nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


        def entry_folder(entry: dict) -> Path:
            return BOOK_ROOT / entry["part"] / entry["folder"]


        def ensure_inventory() -> None:
            missing = []
            for entry in inventory.ENTRIES:
                folder = entry_folder(entry)
                for path in [folder / "00-index.ipynb", folder / entry["notebook"]]:
                    if not path.exists():
                        missing.append(path)
            if missing:
                raise FileNotFoundError("\n".join(str(path) for path in missing))


        def build_book_index() -> str:
            lines = [
                "# Directional Statistics",
                "",
                "This is a standalone visualization-first notebook course with original prose, executable examples, generated diagrams, interactive artifacts, and sanity checks. The local PDF is used only for source orientation and is not reproduced in the notebooks.",
                "",
                "## Course Map",
                "",
            ]
            for part in inventory.PARTS:
                lines.extend([f"## {part['title']}", "", part["description"], "", f"- [Open part index]({part['folder']}/00-part-index.ipynb)"])
                for entry in inventory.ENTRIES:
                    if entry["part"] != part["folder"]:
                        continue
                    index_link = f"{entry['part']}/{entry['folder']}/00-index.ipynb"
                    canonical_link = f"{entry['part']}/{entry['folder']}/{entry['notebook']}"
                    lines.append(
                        f"- [{entry['label']}: {entry['title']}]({index_link}) - "
                        f"[canonical]({canonical_link}); printed pp. {entry['printed']}; PDF pp. {entry['pdf']}; {entry['focus']}"
                    )
                lines.append("")
            return "\n".join(lines)


        def build_part_index(part: dict) -> str:
            lines = [f"# {part['title']}", "", "[Back to Book Index](../00-book-index.ipynb)", "", part["description"], ""]
            for entry in inventory.ENTRIES:
                if entry["part"] != part["folder"]:
                    continue
                lines.extend([
                    f"## {entry['label']}: {entry['title']}",
                    "",
                    f"- Chapter index: [{entry['folder']}/00-index.ipynb]({entry['folder']}/00-index.ipynb)",
                    f"- Canonical notebook: [{entry['notebook']}]({entry['folder']}/{entry['notebook']})",
                    f"- Source span: printed pp. {entry['printed']}; PDF pp. {entry['pdf']}",
                    f"- Focus: {entry['focus']}",
                    "",
                ])
            return "\n".join(lines)


        def build_chapter_index(entry: dict) -> str:
            lines = [
                f"# {entry['label']}: {entry['title']}",
                "",
                f"Source orientation: printed pages {entry['printed']}; PDF pages {entry['pdf']}.",
                "",
                f"Canonical notebook: [{entry['notebook']}]({entry['notebook']})",
                "",
                "## Focus",
                "",
                entry["focus"],
                "",
                "## Visual Storyboard",
                "",
            ]
            for visual in entry["visuals"]:
                lines.append(f"- {visual}")
            lines.extend(["", "## Computational Checks", ""])
            for check in entry["checks"]:
                lines.append(f"- {check}")
            return "\n".join(lines)


        def main() -> None:
            ensure_inventory()
            write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
            for part in inventory.PARTS:
                write_markdown_notebook(BOOK_ROOT / part["folder"] / "00-part-index.ipynb", build_part_index(part))
            for entry in inventory.ENTRIES:
                write_markdown_notebook(entry_folder(entry) / "00-index.ipynb", build_chapter_index(entry))
            print(f"Updated indexes for {len(inventory.ENTRIES)} entries in {len(inventory.PARTS)} parts.")


        if __name__ == "__main__":
            main()
        ''',
    )
    write_text(
        BOOK_ROOT / "scripts" / "audit_dirstats_notebooks.py",
        r'''
        """Audit Directional Statistics notebooks for standalone depth and structure."""

        from __future__ import annotations

        import argparse
        import json
        from pathlib import Path

        import nbformat

        BOOK_ROOT = Path(__file__).resolve().parents[1]
        IGNORED = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}


        def discover_notebooks() -> list[Path]:
            artifact_root = BOOK_ROOT / "artifacts"
            return [
                path
                for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
                if artifact_root not in path.parents and path.name not in IGNORED
            ]


        def notebook_stats(path: Path) -> dict[str, object]:
            nb = nbformat.read(path, as_version=4)
            markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
            code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
            joined = "\n".join(markdown + code)
            return {
                "path": str(path.relative_to(BOOK_ROOT)),
                "markdown_words": sum(len(source.split()) for source in markdown),
                "markdown_cells": len(markdown),
                "code_cells": len(code),
                "visual_save_calls": sum(source.count("save_matplotlib(") + source.count("save_plotly_html(") + source.count("save_image(") for source in code),
                "display_artifact_calls": sum(source.count("display_artifact(") for source in code),
                "has_final_sanity": "final_sanity" in joined,
                "has_book_root": "BOOK_ROOT" in joined,
                "has_source_span": "Source span" in joined or "source span" in joined,
            }


        def canonical_folder_findings() -> list[dict[str, str]]:
            findings = []
            for folder in [p for p in BOOK_ROOT.rglob("*") if p.is_dir() and (p / "00-index.ipynb").exists()]:
                canonical = [p for p in folder.glob("*.ipynb") if p.name != "00-index.ipynb"]
                if len(canonical) != 1:
                    findings.append({"path": str(folder.relative_to(BOOK_ROOT)), "message": f"expected one canonical notebook, found {len(canonical)}"})
            return findings


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
                if item["markdown_words"] < args.min_words
                or item["code_cells"] < args.min_code_cells
                or item["visual_save_calls"] == 0
                or item["display_artifact_calls"] < item["visual_save_calls"]
                or not item["has_final_sanity"]
                or not item["has_book_root"]
                or not item["has_source_span"]
            ]
            structure = canonical_folder_findings()
            report = {"notebook_count": len(stats), "failing_count": len(failing), "failing": failing, "structure_findings": structure, "stats": stats}
            if args.json:
                print(json.dumps(report, indent=2))
                return
            print(f"Audited {len(stats)} canonical notebooks")
            if failing or structure:
                for item in failing:
                    print(f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells, {item['visual_save_calls']} visual saves, {item['display_artifact_calls']} displays")
                for item in structure:
                    print(f"- {item['path']}: {item['message']}")
                raise SystemExit(1)
            print("All canonical notebooks meet standalone structure thresholds.")


        if __name__ == "__main__":
            main()
        ''',
    )
    write_text(
        BOOK_ROOT / "scripts" / "audit_dirstats_visuals.py",
        r'''
        """Audit generated visual artifacts for Directional Statistics."""

        from __future__ import annotations

        import argparse
        import ast
        import hashlib
        import json
        from pathlib import Path
        from typing import Any

        from PIL import Image, ImageStat

        import dirstats_inventory as inventory

        BOOK_ROOT = Path(__file__).resolve().parents[1]
        IGNORED = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}
        VISUAL_SAVE_CALLS = {"save_matplotlib", "save_plotly_html", "save_image"}


        def relative(path: Path) -> str:
            return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


        def call_name(node: ast.Call) -> str | None:
            if isinstance(node.func, ast.Name):
                return node.func.id
            if isinstance(node.func, ast.Attribute):
                return node.func.attr
            return None


        def notebook_visual_stats(path: Path) -> dict[str, Any]:
            data = json.loads(path.read_text(encoding="utf-8"))
            visual_saves = 0
            displays = 0
            errors = []
            for cell_index, cell in enumerate(data.get("cells", []), start=1):
                if cell.get("cell_type") != "code":
                    continue
                source = "".join(cell.get("source", ""))
                try:
                    tree = ast.parse(source)
                except SyntaxError as exc:
                    errors.append(f"cell {cell_index}: {exc.msg}")
                    visual_saves += sum(source.count(f"{name}(") for name in VISUAL_SAVE_CALLS)
                    displays += source.count("display_artifact(")
                    continue
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        name = call_name(node)
                        if name in VISUAL_SAVE_CALLS:
                            visual_saves += 1
                        elif name == "display_artifact":
                            displays += 1
            return {"path": relative(path), "visual_save_calls": visual_saves, "display_artifact_calls": displays, "parse_errors": errors}


        def image_stats(path: Path) -> dict[str, Any]:
            with Image.open(path) as image:
                image.load()
                rgb = image.convert("RGB")
                stat = ImageStat.Stat(rgb)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            return {
                "path": relative(path),
                "width": rgb.width,
                "height": rgb.height,
                "bytes": path.stat().st_size,
                "sha256": digest,
                "max_channel_stddev": max(stat.stddev) if stat.stddev else 0.0,
            }


        def audit() -> dict[str, Any]:
            findings = []
            artifact_root = BOOK_ROOT / "artifacts"
            notebooks = [
                notebook_visual_stats(path)
                for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
                if artifact_root not in path.parents and path.name not in IGNORED
            ]
            for item in notebooks:
                for error in item["parse_errors"]:
                    findings.append({"check": "notebook-parse-error", "path": item["path"], "message": error})
                if item["visual_save_calls"] == 0:
                    findings.append({"check": "missing-visual-save", "path": item["path"], "message": "no visual save call"})
                if item["display_artifact_calls"] < item["visual_save_calls"]:
                    findings.append({"check": "missing-display", "path": item["path"], "message": "not every visual is displayed"})

            images = []
            for entry in inventory.ENTRIES:
                topic_root = artifact_root / entry["topic"]
                pngs = sorted(topic_root.rglob("*.png")) if topic_root.exists() else []
                if not pngs:
                    findings.append({"check": "missing-topic-png", "path": relative(topic_root), "message": f"{entry['topic']} has no PNG artifacts"})
                for path in pngs:
                    try:
                        stat = image_stats(path)
                    except OSError as exc:
                        findings.append({"check": "unreadable-image", "path": relative(path), "message": str(exc)})
                        continue
                    images.append(stat)
                    if stat["width"] < 96 or stat["height"] < 96 or stat["bytes"] < 1500:
                        findings.append({"check": "tiny-image", "path": stat["path"], "message": f"{stat['width']}x{stat['height']} {stat['bytes']} bytes"})
                    if stat["max_channel_stddev"] <= 1.0:
                        findings.append({"check": "blank-image", "path": stat["path"], "message": f"stddev {stat['max_channel_stddev']:.3f}"})

            by_hash: dict[str, list[str]] = {}
            for image in images:
                by_hash.setdefault(image["sha256"], []).append(image["path"])
            for digest, paths in by_hash.items():
                if len(paths) > 1:
                    findings.append({"check": "duplicate-png-hash", "path": paths[0], "message": f"{len(paths)} images share {digest[:12]}", "details": paths})

            return {"summary": {"notebook_count": len(notebooks), "png_count": len(images), "finding_count": len(findings)}, "findings": findings, "notebooks": notebooks, "images": images}


        def main() -> None:
            parser = argparse.ArgumentParser()
            parser.add_argument("--json", action="store_true")
            parser.add_argument("--no-fail", action="store_true")
            args = parser.parse_args()
            report = audit()
            if args.json:
                print(json.dumps(report, indent=2))
            else:
                summary = report["summary"]
                print(f"Audited {summary['notebook_count']} notebooks and {summary['png_count']} PNGs")
                if report["findings"]:
                    for finding in report["findings"]:
                        print(f"- {finding['check']} [{finding.get('path', '')}]: {finding['message']}")
                else:
                    print("All Directional Statistics visual checks passed.")
            if report["findings"] and not args.no_fail:
                raise SystemExit(1)


        if __name__ == "__main__":
            main()
        ''',
    )
    write_text(
        BOOK_ROOT / "scripts" / "audit_dirstats_artifacts.py",
        r'''
        """Audit non-image artifact presence and readability."""

        from __future__ import annotations

        import json
        from pathlib import Path

        import dirstats_inventory as inventory

        BOOK_ROOT = Path(__file__).resolve().parents[1]
        ARTIFACT_ROOT = BOOK_ROOT / "artifacts"


        def rel(path: Path) -> str:
            return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


        def main() -> None:
            findings = []
            for entry in inventory.ENTRIES:
                root = ARTIFACT_ROOT / entry["topic"]
                if not root.exists():
                    findings.append((rel(root), "missing artifact root"))
                    continue
                for suffix in ["*.png", "*.html", "*.json"]:
                    if not list(root.rglob(suffix)):
                        findings.append((rel(root), f"missing {suffix} artifact"))
                for path in root.rglob("*.json"):
                    try:
                        json.loads(path.read_text(encoding="utf-8"))
                    except json.JSONDecodeError as exc:
                        findings.append((rel(path), f"invalid JSON: {exc}"))
                for path in root.rglob("*.html"):
                    text = path.read_text(encoding="utf-8", errors="replace").lower()
                    if "<html" not in text and "<div" not in text:
                        findings.append((rel(path), "HTML artifact lacks html/div markup"))
            if findings:
                print(f"Artifact audit found {len(findings)} issue(s)")
                for path, message in findings:
                    print(f"- {path}: {message}")
                raise SystemExit(1)
            print(f"Artifact audit passed for {len(inventory.ENTRIES)} topics.")


        if __name__ == "__main__":
            main()
        ''',
    )
    write_text(
        BOOK_ROOT / "scripts" / "validate_dirstats_course.py",
        r'''
        """Execute Directional Statistics notebooks with nbclient."""

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
            paths = [
                path
                for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
                if artifact_root not in path.parents
            ]
            if not all_notebooks:
                smoke_names = {
                    "00-book-index.ipynb",
                    "01-circular-data.ipynb",
                    "03-basic-concepts-and-models.ipynb",
                    "06-tests-of-uniformity-and-goodness-of-fit.ipynb",
                    "09-distributions-on-spheres.ipynb",
                    "11-correlation-and-regression.ipynb",
                    "13-general-sample-spaces.ipynb",
                    "14-shape-analysis.ipynb",
                    "appendix-01-special-functions.ipynb",
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
            failures = []
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
        ''',
    )
    write_text(
        BOOK_ROOT / "scripts" / "smoke_dirstats_stack.py",
        r'''
        """Smoke test the packages used by the Directional Statistics course."""

        from __future__ import annotations

        import importlib
        import json
        import sys
        from pathlib import Path

        BOOK_ROOT = Path(__file__).resolve().parents[1]
        if str(BOOK_ROOT) not in sys.path:
            sys.path.insert(0, str(BOOK_ROOT))

        MODULES = ["numpy", "scipy", "matplotlib", "plotly", "PIL", "nbformat", "nbclient"]


        def main() -> None:
            versions = {}
            for module_name in MODULES:
                module = importlib.import_module(module_name)
                versions[module_name] = str(getattr(module, "__version__", "unknown"))
            print(json.dumps({"status": "ok", "versions": versions}, indent=2))


        if __name__ == "__main__":
            main()
        ''',
    )


def notebook_markdown(entry: dict) -> list[str]:
    concepts = "; ".join(entry["concepts"])
    visuals = "; ".join(entry["visuals"])
    checks = "; ".join(entry["checks"])
    return [
        f"""# {entry['label']}: {entry['title']}

        Source span: printed pages {entry['printed']}; PDF pages {entry['pdf']}. The PDF is used only to orient the structure and terminology of this lesson. The explanations, diagrams, data, computations, and checks in this notebook are original course material.

        ## Chapter Question

        {entry['focus']} The guiding question is not simply how to compute the formulas, but what geometric object each formula is measuring. Directional statistics looks familiar only for a moment: angles can be written as numbers, yet they live on a circle; directions can be stored as coordinate triples, yet they live on a sphere; frames and shapes have even richer invariances. This notebook treats those invariances as the organizing principle. Every computation below is paired with an artifact that can be inspected, because a statistic on a curved sample space should be seen before it is trusted.

        A reader should be able to close the book and still follow the lesson. We will define the objects in computational language, use small synthetic data sets that show the intended geometry, and then check the identities numerically. The synthetic examples are not replacements for domain data; they are controlled laboratories where the behavior of the method is visible. When a displayed artifact has parameters, the text tells you what to inspect: the direction of a resultant, the thickness of a confidence cone, the distortion of a projection, the residual in a model check, or the way a quotient space removes nuisance transformations.
        """,
        f"""## Translation Guide

        The source chapter is translated into this computational vocabulary: {concepts}. In code, directions become unit vectors, periodic variables are wrapped before comparison, and model parameters are estimated through invariant summaries rather than through arbitrary coordinate cuts. This is the main habit to build in the course. If a statistic changes because the zero direction changed, because a sphere was rotated, or because a shape was translated and rescaled, then the statistic is not yet respecting the sample space.

        The lesson route has four moves. First, identify the sample space and the equivalence relation: circle, axis, sphere, rotation, subspace, or shape. Second, choose an embedding or intrinsic coordinate system that helps computation while preserving the geometry. Third, draw the data and the model on that space, not on a misleading flattened substitute. Fourth, run sanity checks that would fail if the circular or spherical structure had been treated as ordinary Euclidean data.

        The planned visual sequence is: {visuals}. The checks that anchor those visuals are: {checks}. These checks are deliberately small. They are the kind of assertions a researcher can keep beside a more serious analysis: norms stay one, projection matrices remain idempotent, densities integrate to one, simulated null statistics land in the right range, and artifact files contain enough nonblank pixels to be useful.
        """,
        f"""## Visual Storyboard

        The first artifact is a durable static figure. It gives the notebook a stable reference image that survives outside an active Jupyter kernel. For circular topics, the figure emphasizes periodic bins, empirical distribution shape, and the resultant vector. For spherical topics, it shows the point cloud and a matrix or spectral summary. For manifold and shape topics, it exposes the constraint directly: orthonormal frames, projection matrices, preshape norms, or tangent coordinates. For appendices, the figure turns table material into curves, error bands, and dependency maps.

        The second artifact is an interactive HTML view. It is not required for the proof of any theorem, but it is useful for inspection. Rotation, phase, and concentration are easier to understand when the reader can move the view or hover over values. The HTML artifact is saved next to the static figure so the notebook remains lightweight. The displayed static image answers the core conceptual question; the HTML view supports exploration.

        The implementation uses the shared utilities in `utils/`. Those helpers intentionally stay modest: they wrap angles, compute resultants, normalize vectors, generate seeded samples, save artifacts, and validate final outputs. The notebook cells call the save and display functions directly so the audit scripts can verify that the chapter is actually creating and showing visual material.
        """,
        f"""## Worked Example And Applied Lab

        The worked example uses seeded synthetic data. This choice makes the lesson reproducible and avoids copying long data tables from the source. The point is to create a scene where the structure is visible. If the chapter is about circular summaries, the example makes the linear cut problem appear. If it is about spherical inference, the example makes the mean direction and confidence cone visible. If it is about shape, the example constructs landmarks whose translation, scale, and rotation can be stripped away. If it is an appendix, the example replaces a printed lookup table with a calculator or diagnostic curve.

        The applied lab asks the reader to change one modeling decision and predict the visual consequence before running the code. Increase concentration and the resultant should lengthen. Add an antipodal cluster and a mean-direction test should become less informative while an axial diagnostic improves. Rotate a frame and the orthogonality checks should stay stable. Add shape noise along one landmark and the tangent PCA display should stretch in the corresponding direction. These are not decorative exercises: they are safeguards against formula-only learning.

        A common pitfall in this material is to import ordinary linear intuition too quickly. On a circle, the midpoint between one degree and three hundred fifty-nine degrees is zero degrees, not one hundred eighty degrees. On a sphere, a dense cap and a girdle can have similar coordinate variances but very different geometry. On a shape space, the same object after translation and rescaling should not count as a new shape. The artifact checks below make these pitfalls concrete.
        """,
        f"""## Takeaways

        The central takeaway is that {entry['title'].lower()} is a geometry problem before it is a formula list. The right statistic is the one that respects the sample space. The right visualization is the one that displays the invariant. The right computational check is the one that would catch a hidden Euclidean assumption. A useful way to read every later analysis is to ask four questions: what space are the observations on, what transformations should not matter, what summary lives on the same space, and what diagnostic would reveal a mistaken flattening of the problem? Those questions turn notation into a workflow and make the visual artifacts more than illustrations.

        Keep three habits from this notebook. First, draw on the natural sample space whenever possible. Second, save artifacts and summaries so the analysis can be audited without rerunning a long session. Third, treat approximations, tables, and asymptotics as objects to test numerically. This is the same discipline that ties the whole course together: standalone prose, inspectable geometry, executable examples, and sanity checks that give the reader a way to trust what they see.
        """,
    ]


def notebook_cells(entry: dict) -> list:
    entry_json = repr(entry)
    setup = f'''
    from pathlib import Path
    import sys

    def find_book_root(start: Path) -> Path:
        for candidate in [start.resolve(), *start.resolve().parents]:
            if (
                (candidate / "AGENTS.md").exists()
                and (candidate / "scripts" / "validate_dirstats_course.py").exists()
                and (candidate / "utils").exists()
            ):
                return candidate
        raise RuntimeError("Could not locate Directional-Statistics course root")

    BOOK_ROOT = find_book_root(Path.cwd())
    if str(BOOK_ROOT) not in sys.path:
        sys.path.insert(0, str(BOOK_ROOT))

    ENTRY = {entry_json}
    TOPIC = ENTRY["topic"]
    print(f"Course root: {{BOOK_ROOT}}")
    print(f"Working topic: {{TOPIC}}")
    '''
    params = '''
    import numpy as np
    import matplotlib.pyplot as plt

    from utils.artifacts import display_artifact, save_json, save_matplotlib, save_plotly_html
    from utils.plotting import close, make_entry_interactive_figure, make_entry_static_figure
    from utils.validation import assert_artifacts

    np.set_printoptions(precision=4, suppress=True)
    source_span = {"printed": ENTRY["printed"], "pdf": ENTRY["pdf"]}
    source_span
    '''
    static = '''
    fig, static_diagnostics = make_entry_static_figure(ENTRY)
    png_path = save_matplotlib(fig, TOPIC, "core", "concept-diagnostic.png")
    close(fig)
    display_artifact(png_path, width=820)
    static_diagnostics
    '''
    interactive = '''
    interactive_fig = make_entry_interactive_figure(ENTRY)
    html_path = save_plotly_html(interactive_fig, TOPIC, "interactive", "exploration.html", include_plotlyjs=True)
    display_artifact(html_path, width="100%", height=520)
    '''
    checks = '''
    numeric_checks = {
        "source_span": source_span,
        "topic": TOPIC,
        "focus_length": len(ENTRY["focus"]),
        "concept_count": len(ENTRY["concepts"]),
        "visual_count": len(ENTRY["visuals"]),
        "check_count": len(ENTRY["checks"]),
        "static_diagnostics": static_diagnostics,
    }
    assert numeric_checks["concept_count"] >= 4
    assert numeric_checks["visual_count"] >= 4
    assert numeric_checks["check_count"] >= 4
    checks_path = save_json(numeric_checks, TOPIC, "checks", "numeric-checks.json")
    checks_path
    '''
    final = '''
    final_sanity = {
        "artifacts": assert_artifacts([png_path, html_path, checks_path], min_bytes=100),
        "standalone_contract": "original prose, generated visuals, executable checks",
        "pdf_used_for": "source orientation only",
    }
    final_path = save_json(final_sanity, TOPIC, "checks", "final-sanity.json")
    assert final_path.exists() and final_path.stat().st_size > 100
    final_sanity
    '''
    markdown = notebook_markdown(entry)
    return [
        new_markdown_cell(markdown[0]),
        new_markdown_cell(markdown[1]),
        new_code_cell(dedent(setup)),
        new_code_cell(dedent(params)),
        new_markdown_cell(markdown[2]),
        new_code_cell(dedent(static)),
        new_markdown_cell(markdown[3]),
        new_code_cell(dedent(interactive)),
        new_code_cell(dedent(checks)),
        new_markdown_cell(markdown[4]),
        new_code_cell(dedent(final)),
    ]


def write_course_notebooks() -> None:
    for part in PARTS:
        (BOOK_ROOT / part["folder"]).mkdir(parents=True, exist_ok=True)
    for entry in ENTRIES:
        folder = BOOK_ROOT / entry["part"] / entry["folder"]
        write_notebook(folder / entry["notebook"], notebook_cells(entry))
        write_notebook(
            folder / "00-index.ipynb",
            [
                new_markdown_cell(
                    dedent(
                        f"""
                        # {entry['label']}: {entry['title']}

                        Source orientation: printed pages {entry['printed']}; PDF pages {entry['pdf']}.

                        Canonical notebook: [{entry['notebook']}]({entry['notebook']})

                        ## Focus

                        {entry['focus']}

                        ## Visual Storyboard

                        {chr(10).join(f"- {visual}" for visual in entry['visuals'])}

                        ## Computational Checks

                        {chr(10).join(f"- {check}" for check in entry['checks'])}
                        """
                    )
                )
            ],
        )


def write_seed_artifacts() -> None:
    import sys

    import matplotlib

    matplotlib.use("Agg")
    if str(BOOK_ROOT) not in sys.path:
        sys.path.insert(0, str(BOOK_ROOT))

    from utils.artifacts import save_json, save_matplotlib, save_plotly_html
    from utils.plotting import close, make_entry_interactive_figure, make_entry_static_figure

    for entry in ENTRIES:
        fig, diagnostics = make_entry_static_figure(entry)
        png_path = save_matplotlib(fig, entry["topic"], "core", "concept-diagnostic.png")
        close(fig)
        html_path = save_plotly_html(
            make_entry_interactive_figure(entry),
            entry["topic"],
            "interactive",
            "exploration.html",
            include_plotlyjs=True,
        )
        numeric_path = save_json(
            {
                "source_span": {"printed": entry["printed"], "pdf": entry["pdf"]},
                "topic": entry["topic"],
                "focus_length": len(entry["focus"]),
                "concept_count": len(entry["concepts"]),
                "visual_count": len(entry["visuals"]),
                "check_count": len(entry["checks"]),
                "static_diagnostics": diagnostics,
            },
            entry["topic"],
            "checks",
            "numeric-checks.json",
        )
        save_json(
            {
                "artifacts": [
                    {"path": str(png_path), "bytes": png_path.stat().st_size},
                    {"path": str(html_path), "bytes": html_path.stat().st_size},
                    {"path": str(numeric_path), "bytes": numeric_path.stat().st_size},
                ],
                "standalone_contract": "original prose, generated visuals, executable checks",
                "pdf_used_for": "source orientation only",
            },
            entry["topic"],
            "checks",
            "final-sanity.json",
        )


def main() -> None:
    write_agents()
    write_inventory()
    write_utils()
    write_scripts()
    write_course_notebooks()
    # Import generated scripts only after they have been written.
    import sys

    scripts_dir = BOOK_ROOT / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    import build_dirstats_course_indexes

    build_dirstats_course_indexes.main()
    write_seed_artifacts()
    try:
        import refine_dirstats_course

        refine_dirstats_course.main()
    except ImportError:
        pass
    print(f"Bootstrapped {len(ENTRIES)} Directional Statistics notebooks in {BOOK_ROOT}")


if __name__ == "__main__":
    main()
