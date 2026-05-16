# Agent Instructions: A Course in Metric Geometry Notebook Course

This folder is a standalone visualization-first notebook edition of *A Course in Metric Geometry* by Dmitri Burago, Yuri Burago, and Sergei Ivanov. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or figures.
- Use the PDF only for source orientation: title, authors, chapter order, page spans, terminology, and concept coverage.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualizations are part of the explanation. Use diagrams, plots, HTML parameter labs, symbolic checks, finite metric experiments, proof-state diagrams, and model comparisons wherever they clarify the geometry.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.

## Course Structure

```text
A-Course-in-Metric-Geometry/
  00-book-index.ipynb
  AGENTS.md
  source_map.json
  artifacts/
  scripts/
  utils/
  chapter-01-metric-spaces/
  ...
  chapter-10-spaces-of-curvature-bounded-below/
```

Each chapter folder contains:

```text
00-index.ipynb
<canonical notebook>.ipynb
```

There should be exactly one canonical teaching notebook in each chapter folder, excluding `00-index.ipynb`.

## Source Map

The book has 10 chapters, no formal part divisions, then bibliography and index. Body printed pages map to physical PDF pages by `pdf_page = printed_page + 15`.

| Unit | Folder | Printed Pages | PDF Pages | Focus |
| --- | --- | ---: | ---: | --- |
| Chapter 1 | `chapter-01-metric-spaces` | 1-24 | 16-39 | Metric axioms, examples, topology, Lipschitz maps, completeness, compactness, and Hausdorff dimension. |
| Chapter 2 | `chapter-02-length-spaces` | 25-58 | 40-73 | Length structures, induced intrinsic metrics, shortest paths, length measure, and speed. |
| Chapter 3 | `chapter-03-constructions` | 59-100 | 74-115 | Gluing, maximal metrics, polyhedral spaces, quotients, coverings, arcwise isometries, products, and cones. |
| Chapter 4 | `chapter-04-spaces-of-bounded-curvature` | 101-134 | 116-149 | Alexandrov-style bounded curvature definitions, examples, angles, distance functions, first variation, globalization, and cones. |
| Chapter 5 | `chapter-05-smooth-length-structures` | 135-208 | 150-223 | Riemannian length, exponential maps, the hyperbolic plane, sub-Riemannian structures, volumes, and Besikovitch inequality. |
| Chapter 6 | `chapter-06-curvature-of-riemannian-metrics` | 209-240 | 224-255 | Coordinate curvature computations, covariant derivative, geodesic and Gaussian curvature, geometric meaning, and comparison theorems. |
| Chapter 7 | `chapter-07-space-of-metric-spaces` | 241-270 | 256-285 | Lipschitz distance, Gromov-Hausdorff distance, convergence, and compact length-space limits. |
| Chapter 8 | `chapter-08-large-scale-geometry` | 271-306 | 286-321 | Noncompact limits, tangent and asymptotic cones, quasi-isometries, Gromov hyperbolicity, and periodic metrics. |
| Chapter 9 | `chapter-09-spaces-of-curvature-bounded-above` | 307-350 | 322-365 | CAT spaces, local properties, Hadamard spaces, fundamental groups, and semi-dispersing billiards. |
| Chapter 10 | `chapter-10-spaces-of-curvature-bounded-below` | 351-404 | 366-419 | CBB definitions, examples, Toponogov, diameter, splitting, dimension, volume, limits, local properties, directions, and tangent cones. |

Bibliography is printed pages 405-408 (PDF pages 420-423). Index is printed pages 409-419 (PDF pages 424-434).

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Standalone chapter question and motivation.
3. Translation guide from book concepts into computational language.
4. Setup cell that discovers `BOOK_ROOT`.
5. Chapter-specific library routing.
6. Original concept sections with equations and diagrams.
7. Generated visual artifacts displayed inline.
8. Proof, invariant, counterexample, finite-model, or deformation scaffold where useful.
9. Applied lab or design exercise.
10. Final sanity checks asserting identities, artifact existence, and nonblank visuals.
11. Takeaways.

## Artifact Contract

Store generated outputs under:

```text
artifacts/chapter-XX/figures/
artifacts/chapter-XX/html/
artifacts/chapter-XX/checks/
artifacts/chapter-XX/tables/
```

Artifact filenames should name the concept, not the rendering technology. Repeated placeholder visuals are a QC failure. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `pandas`, `networkx`, `shapely`, `trimesh`, `pyvista`, `gudhi`, `ripser`, `geomstats`, `POT`, and the rest of the root geometry stack. This course currently needs no dependency additions.

## Worker Boundaries

Other workers may edit other course folders. Do not touch anything outside `A-Course-in-Metric-Geometry` unless explicitly required. Chapter workers may edit only their chapter folder, matching artifact subtree, and explicitly assigned helper module. Index workers own `00-book-index.ipynb`, chapter `00-index.ipynb` files, and `source_map.json`. QC workers run audits and validation and report findings.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python A-Course-in-Metric-Geometry/scripts/build_acmg_course_indexes.py
uv run python -m compileall -q A-Course-in-Metric-Geometry/utils A-Course-in-Metric-Geometry/scripts
uv run python A-Course-in-Metric-Geometry/scripts/audit_acmg_notebooks.py --min-words 900 --min-code-cells 5
uv run python A-Course-in-Metric-Geometry/scripts/audit_acmg_visuals.py
uv run python A-Course-in-Metric-Geometry/scripts/validate_acmg_course.py --limit 4 --timeout 300
git diff --check -- A-Course-in-Metric-Geometry
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Geometry Visualization Library Policy

Use the installed geometry stack intentionally. Do not default to generic Matplotlib-only notebooks when the chapter's geometry calls for richer representations.

- Use Matplotlib for durable 2D metric diagrams, proof sketches, constructions, comparison triangles, model overlays, and labeled static figures.
- Use Plotly for interactive 2D/3D parameter exploration, surfaces, distance landscapes, and standalone HTML artifacts.
- Use NetworkX for proof dependency graphs, finite metric models, quotient/covering graphs, tree boundaries, and group-action diagrams.
- Use SymPy for exact symbolic checks, metric identities, curvature formulas, comparison identities, and small algebraic derivations.
- Use scipy, Shapely, and NumPy for distance matrices, correspondences, geodesic approximations, convexity diagnostics, and computational geometry.
- Use PyVista/Trimesh or Plotly 3D when surfaces, cones, curvature, tangent cones, or volume models need spatial inspection.
- Use topology, manifold, transport, or GIS libraries only when the chapter's geometry calls for them.

Every major visualization must have the concept it teaches, the reason this representation was chosen, an inspection target for the learner, nearby prose explanation, and a check or invariant where practical.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
