# Agent Instructions: Elementary Differential Geometry (Barrett O'Neill)

This folder is a standalone visualization-first notebook edition of *Elementary Differential Geometry, Revised Second Edition* by Barrett O'Neill. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills` for course work:

- `geometry-visualization-planner` for chapter storyboards.
- `geometry-chapter-notebook-author` for authoring or revising canonical notebooks.
- `geometry-notebook-qc` for standalone, artifact, and execution review.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, screenshots, page crops, answer-key content, or PDF images.
- The notebooks must stand alone without the PDF open.
- Visualization is part of the teaching argument, not decoration or a fixed quota.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook per chapter or appendix folder plus a local `00-index.ipynb`.

## Source Map

The PDF has 518 pages. Body and appendix printed pages map to PDF pages by `pdf_page = printed_page + 15`.

- Introduction: printed pp. 1-2; PDF pp. 16-17.
- Chapter 1: printed pp. 3-42; PDF pp. 18-57.
- Chapter 2: printed pp. 43-99; PDF pp. 58-114.
- Chapter 3: printed pp. 100-129; PDF pp. 115-144.
- Chapter 4: printed pp. 130-201; PDF pp. 145-216.
- Chapter 5: printed pp. 202-262; PDF pp. 217-277.
- Chapter 6: printed pp. 263-320; PDF pp. 278-335.
- Chapter 7: printed pp. 321-387; PDF pp. 336-402.
- Chapter 8: printed pp. 388-450; PDF pp. 403-465.
- Appendix A: printed pp. 451-466; PDF pp. 466-481.

Bibliography, answers, and index are not canonical notebook units.

## Notebook Shape

Each canonical notebook should include title and source span, translation guide, setup cell discovering `BOOK_ROOT`, original concept sections, executable examples, generated artifacts displayed inline, applied lab, final sanity checks, and takeaways.

## Visualization-First Contract

Visuals are part of the proof and explanation. Artifact filenames must name the concept. Notebook prose near each visual must state what invariant, behavior, or failure mode the reader should inspect. Final sanity checks must assert generated visual paths exist, have nonzero size, and record validation values in `final-sanity.json`.

Repeated placeholder visuals, blank images, and decorative figures are QC failures. For proof-heavy sections, visualize proof state with dependency diagrams, limiting processes, small examples, symbolic residuals, or deformation panels.

## Geometry Stack

Use the shared `uv` environment at `D:\Geometry`. Prefer installed libraries: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `networkx`, `pyvista`, `trimesh`, `PIL`, and the wider stack in the repo-local library catalog.

## Worker Boundaries

Assign one worker to one canonical notebook or one shared helper/script task. Chapter workers should read their assigned source span, consume or create a visualization storyboard, and edit only the assigned chapter folder, its artifact subtree, and any explicitly assigned helper.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Geometric-Algebra-for-Computer-Science/scripts/smoke_geometry_stack.py
uv run python -m compileall -q Elementary-Differential-Geometry-Barrett-ONeill/utils Elementary-Differential-Geometry-Barrett-ONeill/scripts
uv run pytest -q Elementary-Differential-Geometry-Barrett-ONeill/scripts
uv run python Elementary-Differential-Geometry-Barrett-ONeill/scripts/build_oneill_course_indexes.py
uv run python Elementary-Differential-Geometry-Barrett-ONeill/scripts/audit_oneill_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Elementary-Differential-Geometry-Barrett-ONeill/scripts/audit_oneill_visuals.py
uv run python Elementary-Differential-Geometry-Barrett-ONeill/scripts/validate_oneill_course.py --limit 11 --timeout 300
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
