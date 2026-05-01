# Agent Instructions: Perspectives on Projective Geometry Notebook Course

This folder is a standalone visualization-first notebook edition of Jurgen
Richter-Gebert's *Perspectives on Projective Geometry: A Guided Tour Through
Real and Complex Geometry*. Treat this folder as the project root for this
course. The workspace root owns the shared uv environment, `pyproject.toml`,
`uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before chapter storyboards.
- `geometry-chapter-notebook-author` when authoring canonical notebooks.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and
  validation output.

When using parallel workers, assign one worker to one canonical notebook, one
helper module, or one script task. Chapter workers are not alone in the
codebase; they must not revert other workers' edits and should only touch their
assigned chapter folder, matching artifact subtree, and explicitly assigned
helper files.

## Non-Negotiables

- Write original teaching prose, examples, equations, code, diagrams, and
  checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or
  figures.
- The notebooks must stand alone without the PDF open.
- Visualization is part of the teaching argument, not decoration or a fixed
  quota.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation
  tools in `scripts/`.
- Every canonical notebook must execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per chapter
  folder.

## Source Map

The PDF has 593 physical pages. Main printed pages map to PDF pages by:

```text
pdf_page = printed_page + 22
```

The course follows the book's chapter structure. Chapter 1 is an overture
before the three named parts.

| Unit | Printed Pages | PDF Pages | Focus |
| --- | ---: | ---: | --- |
| Chapter 1 | 3-32 | 25-54 | Pappos configurations, projective completion, area and determinant proofs, conic variants, Miquel/cross-ratio lab. |
| Part I, Chapters 2-7 | 35-126 | 57-148 | Projective planes, homogeneous coordinates, cross-ratios, determinants, and bracket algebra. |
| Part II, Chapters 8-15 | 129-294 | 151-316 | Quadrilateral sets, conics, projective d-space, tensor diagrams, configurations, and theorem proving. |
| Part III, Chapters 16-27 | 297-556 | 319-578 | Complex projective line, Euclidean structures, Cayley-Klein geometry, hyperbolic models, and extensions. |

References are printed pp. 557-562 / PDF pp. 579-584. The index is printed
pp. 563-571 / PDF pp. 585-593. They are source material only and are not
converted into teaching notebooks.

## Notebook Shape

Each canonical notebook should contain:

1. Title, source span, and chapter question.
2. A translation guide from book concepts into computational language.
3. A route through the chapter.
4. A setup cell that discovers `BOOK_ROOT` without hardcoded workspace paths.
5. Original concept sections with equations and visual explanations.
6. Executable examples using book-local utilities.
7. Visual artifacts saved under `artifacts/` and displayed inline.
8. An applied lab or design exercise.
9. Sanity checks asserting core identities, artifact existence, nonzero sizes,
   and relevant numeric validation data.
10. Takeaways.

## Visualization-First Contract

The standard is not a fixed visual count; the standard is whether the notebook
can teach the chapter without the textbook open.

- Artifact filenames must name the concept, not the rendering technology.
- Prose near a visual must name what to inspect.
- Final sanity checks must assert artifact existence, nonzero size, and
  relevant numeric validation data.
- Repeated placeholder visuals are forbidden.
- Do not use textbook screenshots, PDF crops, or decorative images.
- For proof-heavy material, visualize proof state: assumptions, dependency
  graph, limiting process, deformation, orientation, or a small symbolic/numeric
  example.

## Artifact Contract

Store generated outputs under:

```text
artifacts/<chapter-slug>/figures
artifacts/<chapter-slug>/html
artifacts/<chapter-slug>/tables
artifacts/<chapter-slug>/checks
```

Storyboards live at `artifacts/<chapter-slug>/checks/storyboard.json`. Final
notebook checks live at `artifacts/<chapter-slug>/checks/final-sanity.json`.

## Geometry Stack

Use the shared uv environment at the workspace root. Prefer installed packages:
`numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `pandas`, `shapely`,
`networkx`, `sympy`, `pyvista`, `trimesh`, and the rest of the repo-local
geometry stack. Document optional tools rather than adding dependencies unless
explicitly requested.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Perspectives-on-Projective-Geometry/scripts/build_ppg_course_indexes.py
uv run python -m compileall -q Perspectives-on-Projective-Geometry/utils Perspectives-on-Projective-Geometry/scripts
uv run pytest -q Perspectives-on-Projective-Geometry/scripts
uv run python Perspectives-on-Projective-Geometry/scripts/audit_ppg_notebooks.py
uv run python Perspectives-on-Projective-Geometry/scripts/audit_ppg_visuals.py
uv run python Perspectives-on-Projective-Geometry/scripts/validate_ppg_course.py --smoke --timeout 300
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
