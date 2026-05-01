# Agent Instructions: Geometry A Metric Approach with Models Notebook Course

This folder is a standalone visualization-first notebook edition of *Geometry: A Metric Approach with Models*, Second Edition, by Richard S. Millman and George D. Parker. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or figures.
- The PDF is an image-only scan. Render pages only as temporary reading aids; do not store page crops in this course.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualizations are part of the explanation. Use diagrams, plots, widgets or HTML parameter labs, symbolic checks, computational experiments, and proof-state diagrams wherever they clarify the geometry.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.

## Course Structure

```text
Geometry-A-Metric-Approach-with-Models/
  00-book-index.ipynb
  AGENTS.md
  artifacts/
  scripts/
  utils/
  chapter-01-preliminary-notions/
  ...
  chapter-11-the-theory-of-isometries/
```

Each chapter folder contains:

```text
00-index.ipynb
<canonical notebook>.ipynb
```

There should be exactly one canonical teaching notebook in each chapter folder, excluding `00-index.ipynb`.

## Source Map

The book has 11 chapters, no formal part divisions, no appendices, then bibliography and index. Body printed pages map to physical PDF pages by `pdf_page = printed_page + 15`.

| Unit | Folder | Printed Pages | PDF Pages | Focus |
| --- | --- | ---: | ---: | --- |
| Chapter 1 | `chapter-01-preliminary-notions` | 1-16 | 16-31 | Axioms, models, equivalence relations, and functions. |
| Chapter 2 | `chapter-02-incidence-and-metric-geometry` | 17-41 | 32-56 | Incidence models, metric geometry, and special coordinate systems. |
| Chapter 3 | `chapter-03-betweenness-and-elementary-figures` | 42-62 | 57-77 | Alternative Cartesian descriptions, betweenness, segments, rays, angles, and triangles. |
| Chapter 4 | `chapter-04-plane-separation` | 63-89 | 78-104 | Plane separation, Pasch geometries, interiors, crossbar theorem, and convex quadrilaterals. |
| Chapter 5 | `chapter-05-angle-measure` | 90-123 | 105-138 | Angle measure, Molton plane, perpendicularity, angle congruence, and Poincare angle measure. |
| Chapter 6 | `chapter-06-neutral-geometry` | 124-168 | 139-183 | SAS, triangle congruence, exterior angle theorem, right triangles, circles and tangent lines, and synthetic proof flow. |
| Chapter 7 | `chapter-07-the-theory-of-parallels` | 169-195 | 184-210 | Parallel lines, Saccheri quadrilaterals, and the critical function. |
| Chapter 8 | `chapter-08-hyperbolic-geometry` | 196-223 | 211-238 | Asymptotic rays, triangle defect, and distance between parallel lines. |
| Chapter 9 | `chapter-09-euclidean-geometry` | 224-247 | 239-262 | Equivalent forms of the Euclidean parallel postulate, similarity theory, and classical Euclidean theorems. |
| Chapter 10 | `chapter-10-area` | 248-284 | 263-299 | Area functions, Euclidean area, hyperbolic area, and Bolyai's theorem. |
| Chapter 11 | `chapter-11-the-theory-of-isometries` | 285-358 | 300-373 | Collineations, disk models, reflections, pencils, cycles, double reflections, classification, and isometry groups. |

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Standalone chapter question and motivation.
3. Translation guide from book concepts into computational language.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Generated visual artifacts displayed inline.
8. Applied lab or design exercise.
9. Sanity checks asserting identities, artifact existence, and nonblank visuals.
10. Takeaways.

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

Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `pandas`, `networkx`, `shapely`, `trimesh`, `pyvista`, and the rest of the root geometry stack. This course currently needs no dependency additions.

## Worker Boundaries

Assign one worker to one canonical notebook, one helper module, or one script task. Chapter workers may edit only their chapter folder, matching artifact subtree, and explicitly assigned helper module. Index workers own `00-book-index.ipynb` and `00-index.ipynb` files. QC workers run audits and validation and report findings.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Geometry-A-Metric-Approach-with-Models/scripts/build_gmam_course_indexes.py
uv run python -m compileall -q Geometry-A-Metric-Approach-with-Models/utils Geometry-A-Metric-Approach-with-Models/scripts
uv run python Geometry-A-Metric-Approach-with-Models/scripts/audit_gmam_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Geometry-A-Metric-Approach-with-Models/scripts/audit_gmam_visuals.py
uv run python Geometry-A-Metric-Approach-with-Models/scripts/validate_gmam_course.py --limit 4 --timeout 300
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
