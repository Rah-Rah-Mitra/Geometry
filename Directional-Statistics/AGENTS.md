# Agent Instructions: Directional Statistics Notebook Course

        This folder is a standalone visualization-first notebook edition of *Directional Statistics* by Kanti V. Mardia and Peter E. Jupp. Treat this folder as the course root. The workspace root `D:\Geometry` owns the shared `uv` Python environment.

        ## Repo-Local Skills

        Use the repo-local skills under `D:\Geometry\.codex\skills` for course work:

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

        - Chapter 01: `part-01-circular-statistics/chapter-01-circular-data/01-circular-data.ipynb`; printed pp. 1-12; PDF pp. 20-31; Circular and axial observations, faithful displays, and the distinction between wrapping clock data and projecting compass data.
- Chapter 02: `part-01-circular-statistics/chapter-02-summary-statistics/02-summary-statistics.ipynb`; printed pp. 13-24; PDF pp. 32-42; Coordinate-invariant summaries from unit-vector geometry: mean direction, resultant length, circular median, moments, and grouping corrections.
- Chapter 03: `part-01-circular-statistics/chapter-03-basic-concepts-and-models/03-basic-concepts-and-models.ipynb`; printed pp. 25-56; PDF pp. 43-73; Circular distribution functions, characteristic functions, Fourier reconstruction, and model families such as uniform, von Mises, cardioid, wrapped, and projected distributions.
- Chapter 04: `part-01-circular-statistics/chapter-04-fundamental-theorems-and-distribution-theory/04-fundamental-theorems-and-distribution-theory.ipynb`; printed pp. 57-82; PDF pp. 74-99; Characteristic-function properties, circular limit theorems, resultant distributions, and high-concentration approximations.
- Chapter 05: `part-01-circular-statistics/chapter-05-point-estimation/05-point-estimation.ipynb`; printed pp. 83-92; PDF pp. 100-109; Parameter estimation for circular models, especially von Mises concentration, wrapped Cauchy behavior, and mixtures.
- Chapter 06: `part-01-circular-statistics/chapter-06-tests-of-uniformity-and-goodness-of-fit/06-tests-of-uniformity-and-goodness-of-fit.ipynb`; printed pp. 93-118; PDF pp. 110-135; Graphical uniformity checks, Rayleigh, Kuiper, Watson, spacing, Ajne, Hermans-Rasson, Beran, and probability-integral-transform diagnostics.
- Chapter 07: `part-01-circular-statistics/chapter-07-tests-on-von-mises-distributions/07-tests-on-von-mises-distributions.ipynb`; printed pp. 119-144; PDF pp. 136-160; One-sample, two-sample, and multi-sample inference under von Mises assumptions.
- Chapter 08: `part-01-circular-statistics/chapter-08-non-parametric-methods/08-non-parametric-methods.ipynb`; printed pp. 145-158; PDF pp. 161-174; Distribution-free circular inference through symmetry, ranks, uniform scores, two-sample comparisons, runs, and q-sample tests.
- Chapter 09: `part-02-spherical-statistics/chapter-09-distributions-on-spheres/09-distributions-on-spheres.ipynb`; printed pp. 159-192; PDF pp. 175-208; Spherical data, descriptive measures, von Mises-Fisher and axial models, distribution theory, and asymptotics on spheres.
- Chapter 10: `part-02-spherical-statistics/chapter-10-inference-on-spheres/10-inference-on-spheres.ipynb`; printed pp. 193-244; PDF pp. 209-259; Exploratory spherical analysis, parameter estimation, uniformity tests, mean-direction confidence cones, and axial distribution tests.
- Chapter 11: `part-02-spherical-statistics/chapter-11-correlation-and-regression/11-correlation-and-regression.ipynb`; printed pp. 245-266; PDF pp. 260-281; Linear-circular, circular-circular, spherical-spherical dependence, directional regression, bivariate models, and directional time series.
- Chapter 12: `part-02-spherical-statistics/chapter-12-modern-methodology/12-modern-methodology.ipynb`; printed pp. 267-282; PDF pp. 282-297; Outliers, robust estimation, bootstrap methods, density estimation, Bayesian ideas, and smoothing for directional data.
- Chapter 13: `part-03-general-sample-spaces-and-shape/chapter-13-general-sample-spaces/13-general-sample-spaces.ipynb`; printed pp. 283-302; PDF pp. 298-316; Directional statistics on rotations, frames, Stiefel manifolds, Grassmann manifolds, hyperboloids, and general manifolds.
- Chapter 14: `part-03-general-sample-spaces-and-shape/chapter-14-shape-analysis/14-shape-analysis.ipynb`; printed pp. 303-348; PDF pp. 317-361; Landmark shape analysis as directional statistics on preshape and shape spaces, including Procrustes means, tangent approximations, and complex directional models.
- Appendix 01: `part-04-appendices/appendix-01-special-functions/appendix-01-special-functions.ipynb`; printed pp. 349-352; PDF pp. 362-365; Bessel, modified Bessel, Bessel-ratio, Kummer, and normalizing-constant calculations used throughout directional models.
- Appendix 02: `part-04-appendices/appendix-02-circular-tables-and-charts/appendix-02-circular-tables-and-charts.ipynb`; printed pp. 353-380; PDF pp. 366-393; Executable replacements for circular critical-value and estimation tables.
- Appendix 03: `part-04-appendices/appendix-03-spherical-tables/appendix-03-spherical-tables.ipynb`; printed pp. 381-390; PDF pp. 394-403; Executable spherical table replacements for Fisher, Watson, resultant, and concentration calculations.
- Appendix 04: `part-04-appendices/appendix-04-notation/appendix-04-notation.ipynb`; printed pp. 391-394; PDF pp. 404-406; Executable notation atlas for sample spaces, statistics, model families, special functions, and shape-analysis symbols.

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

        Use the shared `uv` environment at `D:\Geometry`. Prefer installed packages before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `networkx`, `pyvista`, `trimesh`, `PIL`, `geomstats`, `pyriemann`, and the other packages listed in the repo-local geometry library catalog. Document external-only tools rather than importing them.

        ## Worker Boundaries

        Assign one worker to one canonical notebook, one helper module, or one script task. Chapter workers should read their assigned source span, consume or create a visualization storyboard, and edit only the assigned chapter folder, its artifact subtree, and any explicitly assigned chapter helper. Shared utility changes belong to utility workers.

        ## Commands

        Run from `D:\Geometry`:

        ```powershell
        uv run python "Directional Statistics/scripts/build_dirstats_course_indexes.py"
        uv run python -m compileall -q "Directional Statistics/utils" "Directional Statistics/scripts"
        uv run python "Directional Statistics/scripts/audit_dirstats_notebooks.py" --min-words 1200 --min-code-cells 5
        uv run python "Directional Statistics/scripts/audit_dirstats_visuals.py"
        uv run python "Directional Statistics/scripts/audit_dirstats_artifacts.py"
        uv run python "Directional Statistics/scripts/validate_dirstats_course.py" --limit 8 --timeout 300
        git diff --check
        ```

## Geometry visualization library policy

Use the installed geometry stack intentionally. Do not default to generic Matplotlib-only notebooks when the chapter’s geometry calls for richer representations.

### Library routing

- Use Matplotlib for durable 2D diagrams, proof sketches, constructions, incidence, orientation, area, angle, curves, and labeled static figures.
- Use Plotly for interactive 2D/3D parameter exploration, transformations, surfaces, and standalone HTML artifacts.
- Use ipywidgets/ipympl when parameter variation is central to understanding the concept.
- Use PyVista, VTK, Trimesh, and MeshIO for 3D surfaces, meshes, normals, curvature, polyhedra, frames, slicing, and spatial inspection.
- Use gpytoolbox, potpourri3d, robust_laplacian, manifold3d, and xatlas for mesh Laplacians, geodesics, parameterization, remeshing, and surface diagnostics.
- Use SymPy for exact symbolic checks, coordinate transformations, polynomial identities, and derivations.
- Use Galgebra, Clifford, Kingdon, and PyGanja for exterior algebra, geometric algebra, rotors, bivectors, conformal/projective models, and algebraic proof experiments.
- Use Gudhi, Ripser, and Persim for topology, filtrations, simplicial complexes, persistent homology, and persistence diagrams.
- Use Geomstats and PyRiemann for manifolds, geodesics, metrics, curvature intuition, SPD geometry, and statistical geometry.
- Use Shapely, scipy.spatial, and NetworkX for computational geometry, intersections, Voronoi/Delaunay, arrangements, graph structures, and proof dependency diagrams.
- Use OpenCV, Kornia, Torch, Torchvision, scikit-image, and Pillow for projective geometry, homographies, epipolar geometry, image geometry, camera models, and transformation experiments.
- Use POT and GeomLoss for optimal transport, Wasserstein geometry, barycenters, and metric geometry of distributions.
- Use GIS libraries only when geographic geometry clarifies the chapter.

### Visual justification rule

Every major visualization must have:

1. the concept it teaches,
2. the reason this representation was chosen,
3. an inspection target for the learner,
4. a nearby prose explanation,
5. a check, invariant, or sanity test where practical.

Decorative visuals are not acceptable.

### Notebook-first rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact creation, but they must not mass-populate chapter notebooks with generic teaching cells.
