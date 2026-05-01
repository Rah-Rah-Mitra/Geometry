# Agent Instructions: Basic Topology Notebook Course

This folder is a standalone visualization-first notebook edition of M. A.
Armstrong's *Basic Topology*. Treat this book folder as the course root. The
workspace root owns the shared `uv` environment, `pyproject.toml`, and
`uv.lock`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or solution text.
- The PDFs are source orientation only. A reader should not need the PDF open.
- Visualization is part of delivery, not decoration or a quota.
- Keep helpers in `utils/`, outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook should execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per content folder.

## Course Structure

```text
Basic-Topology/
  00-book-index.ipynb
  AGENTS.md
  artifacts/
  scripts/
  utils/
  chapter-01-introduction/
  ...
  chapter-10-knots-and-covering-spaces/
  appendix-generators-and-relations/
```

## Source Map

Printed page 1 starts at physical PDF page 12.

| Unit | Folder | Printed Pages | PDF Pages | Focus |
| --- | --- | ---: | ---: | --- |
| Chapter 1 | `chapter-01-introduction` | 1-26 | 12-37 | Euler characteristic, equivalence, surfaces, classification, invariants. |
| Chapter 2 | `chapter-02-continuity` | 27-42 | 38-53 | Open/closed sets, continuous maps, space-filling curves, extension. |
| Chapter 3 | `chapter-03-compactness-and-connectedness` | 43-64 | 54-75 | Compactness, products, connectedness, path connectedness. |
| Chapter 4 | `chapter-04-identification-spaces` | 65-86 | 76-97 | Quotients, Mobius strip, topological groups, orbit spaces. |
| Chapter 5 | `chapter-05-the-fundamental-group` | 87-118 | 98-128 | Homotopy, pi_1, calculations, Brouwer, separation, boundaries. |
| Chapter 6 | `chapter-06-triangulations` | 119-148 | 129-158 | Simplicial complexes, subdivision, approximation, edge groups. |
| Chapter 7 | `chapter-07-surfaces` | 149-172 | 159-181 | Surface classification, orientation, surgery, symbols. |
| Chapter 8 | `chapter-08-simplicial-homology` | 173-194 | 182-202 | Chains, cycles, boundaries, homology, invariance. |
| Chapter 9 | `chapter-09-degree-and-lefschetz-number` | 195-212 | 203-220 | Degree, Euler-Poincare, Borsuk-Ulam, Lefschetz, dimension. |
| Chapter 10 | `chapter-10-knots-and-covering-spaces` | 213-240 | 221-247 | Knots, knot groups, Seifert surfaces, coverings, Alexander polynomial. |
| Appendix | `appendix-generators-and-relations` | 241-243 | 248-250 | Free groups, presentations, free products. |

## Notebook Shape

Each canonical notebook should contain a title and source span, a standalone
chapter question, a translation guide, setup cell, original concept sections,
generated visual artifacts displayed inline, worked examples, an applied lab,
sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under:

```text
artifacts/chapter-01/
...
artifacts/chapter-10/
artifacts/appendix-generators-and-relations/
```

Use subfolders such as `figures/`, `html/`, `checks/`, and `tables/`. Artifact
filenames should name the concept, not the rendering technology. Every
generated artifact should be displayed inline or linked from the notebook, and
final checks should assert that files exist and are nonempty.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed
libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`,
`plotly`, `ipywidgets`, `sympy`, `pandas`, `networkx`, `shapely`, `trimesh`,
`pyvista`, `ripser`, `gudhi`, and the rest of the root geometry stack.
This course currently needs no dependency additions.

## Worker Boundaries

Assign one worker to one canonical notebook, one helper module, or one script
task. Chapter workers may edit only their chapter folder, matching artifact
subtree, and explicitly assigned helper module. Index workers own
`00-book-index.ipynb` and `00-index.ipynb` files. QC workers run audits and
validation and report findings.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Basic-Topology/scripts/build_bt_course_indexes.py
uv run python -m compileall -q Basic-Topology/utils Basic-Topology/scripts
uv run python Basic-Topology/scripts/audit_bt_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Basic-Topology/scripts/audit_bt_visuals.py
uv run python Basic-Topology/scripts/validate_bt_course.py --limit 4 --timeout 300
git diff --check
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

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
