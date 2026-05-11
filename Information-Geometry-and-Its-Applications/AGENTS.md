# Agent Instructions: Information Geometry and Its Applications Notebook Course

This folder is a standalone visualization-first notebook edition of Shun-ichi Amari's *Information Geometry and Its Applications*. Treat this folder as the course root. The workspace root `D:\Geometry` owns the shared `uv` Python environment.

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
- Every canonical chapter notebook should execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook per chapter folder plus a local `00-index.ipynb`.

## Source Map

The PDF has 376 pages. Source spans below are physical PDF pages observed from the local PDF table of contents; printed spans come from the book contents. There are 4 parts, 13 chapters, and no appendices.

- Chapter 01: `part-01-geometry-of-divergence-functions/chapter-01-manifold-divergence-dually-flat-structure/01-manifold-divergence-dually-flat-structure.ipynb`; printed pp. 3-30; PDF pp. 20-47; Manifolds, divergences, Bregman geometry, Legendre duality, affine coordinates, and the generalized Pythagorean theorem.
- Chapter 02: `part-01-geometry-of-divergence-functions/chapter-02-exponential-and-mixture-families/02-exponential-and-mixture-families.ipynb`; printed pp. 31-50; PDF pp. 48-67; Exponential and mixture families, e-flat and m-flat structures, kernel exponential families, maximum entropy, mutual information, and maximum likelihood.
- Chapter 03: `part-01-geometry-of-divergence-functions/chapter-03-invariant-geometry-of-probability-distributions/03-invariant-geometry-of-probability-distributions.ipynb`; printed pp. 51-70; PDF pp. 68-87; Invariance, coarse graining, sufficient statistics, f-divergences, KL properties, Fisher information, and positive measures.
- Chapter 04: `part-01-geometry-of-divergence-functions/chapter-04-alpha-geometry-tsallis-entropy-positive-definite-matrices/04-alpha-geometry-tsallis-entropy-positive-definite-matrices.ipynb`; printed pp. 71-106; PDF pp. 88-123; Alpha geometry, alpha geodesics and projections, Tsallis q-entropy, escort geometry, positive measures, positive-definite matrices, and miscellaneous divergences.
- Chapter 05: `part-02-dual-differential-geometry/chapter-05-elements-of-differential-geometry/05-elements-of-differential-geometry.ipynb`; printed pp. 109-130; PDF pp. 126-147; Manifolds, tangent spaces, metrics, affine connections, tensors, covariant derivatives, geodesics, curvature, Levi-Civita connection, and submanifolds.
- Chapter 06: `part-02-dual-differential-geometry/chapter-06-dual-affine-connections-dually-flat-manifold/06-dual-affine-connections-dually-flat-manifold.ipynb`; printed pp. 131-161; PDF pp. 141-171; Dual connections, metric and cubic tensors from divergences, alpha geometry, dually flat manifolds, canonical divergence, mixed coordinates, neural firing, integrated information, and input-output economics.
- Chapter 07: `part-03-statistical-inference/chapter-07-asymptotic-theory-of-statistical-inference/07-asymptotic-theory-of-statistical-inference.ipynb`; printed pp. 165-177; PDF pp. 173-185; Estimation, exponential and curved exponential families, first- and higher-order asymptotics, and hypothesis testing.
- Chapter 08: `part-03-statistical-inference/chapter-08-hidden-variables-and-em/08-hidden-variables-and-em.ipynb`; printed pp. 179-189; PDF pp. 186-196; EM as alternating divergence minimization, hidden-variable models, Gaussian mixtures, information loss under data reduction, and misspecification.
- Chapter 09: `part-03-statistical-inference/chapter-09-neyman-scott-estimating-functions-semiparametrics/09-neyman-scott-estimating-functions-semiparametrics.ipynb`; printed pp. 191-213; PDF pp. 197-219; Nuisance parameters, Neyman-Scott behavior, semiparametric models, estimating functions, exponential-case solutions, scale problems, and neural firing examples.
- Chapter 10: `part-03-statistical-inference/chapter-10-linear-systems-and-time-series/10-linear-systems-and-time-series.ipynb`; printed pp. 215-227; PDF pp. 220-232; Stationary time series, linear systems, finite-dimensional system manifolds, dual system geometry, and AR, MA, and ARMA models.
- Chapter 11: `part-04-applications-of-information-geometry/chapter-11-machine-learning/11-machine-learning.ipynb`; printed pp. 231-278; PDF pp. 234-281; Clustering, Voronoi diagrams, robust centers, SVM geometry, kernels, graphical models, mean-field approximation, belief propagation, CCCP, boosting, Bayesian duality, RBMs, and contrastive divergence.
- Chapter 12: `part-04-applications-of-information-geometry/chapter-12-natural-gradient-and-singular-learning/12-natural-gradient-and-singular-learning.ipynb`; printed pp. 279-314; PDF pp. 282-317; Natural gradient descent, stochastic learning, Hessian geometry, reinforcement learning, mirror descent, multilayer perceptron singularities, plateau dynamics, and singular statistical models.
- Chapter 13: `part-04-applications-of-information-geometry/chapter-13-signal-processing-and-optimization/13-signal-processing-and-optimization.ipynb`; printed pp. 315-358; PDF pp. 318-361; PCA, ICA, non-negative matrix factorization, sparse signal processing, convex programming, barrier-induced dual geometry, game-score geometry, and Hyvarinen score.

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

Chapter workers should edit only their assigned chapter folder, its artifact subtree, and any explicitly assigned chapter helper. Shared utility and script changes belong to foundation workers. Avoid rewriting another worker's notebook content or generated artifacts.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python "Information-Geometry-and-Its-Applications/scripts/build_igapp_course_indexes.py"
uv run python -m compileall -q "Information-Geometry-and-Its-Applications/utils" "Information-Geometry-and-Its-Applications/scripts"
uv run python "Information-Geometry-and-Its-Applications/scripts/audit_igapp_notebooks.py" --min-words 1200 --min-code-cells 5
uv run python "Information-Geometry-and-Its-Applications/scripts/audit_igapp_visuals.py"
uv run python "Information-Geometry-and-Its-Applications/scripts/audit_igapp_artifacts.py"
uv run python "Information-Geometry-and-Its-Applications/scripts/validate_igapp_course.py" --limit 8 --timeout 300
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
