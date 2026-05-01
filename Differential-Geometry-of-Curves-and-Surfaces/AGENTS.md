# Agent Instructions: Differential Geometry of Curves and Surfaces Notebook Course

This folder is a standalone visualization-first notebook edition of Manfredo P.
do Carmo's *Differential Geometry of Curves and Surfaces*, Revised & Updated
Second Edition. Treat this book folder as the course root. The workspace root
owns the shared `uv` environment, `pyproject.toml`, and `uv.lock`.

## Repo-Local Skills

Use the repo-local Codex skills under `D:\Geometry\.codex\skills` for chapter
work:

- `geometry-visualization-planner`: read an assigned source span and produce a
  concrete visual storyboard before authoring.
- `geometry-chapter-notebook-author`: author the standalone visual-first
  canonical notebook directly in its chapter folder.
- `geometry-notebook-qc`: review notebooks, artifacts, execution, visual
  relevance, stale paths, and dependency fit before handoff.

When using parallel workers, pass the relevant skill path and source span. Assign
one worker to one canonical notebook, one helper module, or one script task.
Chapter workers are not alone in the codebase; they must not revert other
workers' edits and should only touch their assigned chapter folder, matching
artifact subtree, and explicitly assigned helper.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or
  figures.
- The PDF is source orientation only. A reader should not need the PDF open.
- Visualization is part of delivery, not decoration or a quota. Use diagrams,
  plots, widgets, symbolic checks, 3D views, proof-state diagrams, and
  computational experiments wherever they clarify the geometry.
- Keep helpers in `utils/`, outputs in `artifacts/`, and validation tools in
  `scripts/`.
- Every canonical notebook should execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local. Avoid hardcoded
  workspace artifact/helper paths.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per content
  folder.

## Source Map

Body printed pages map to PDF pages by:

```text
pdf_page = printed_page + 16
```

| Unit | Printed Pages | PDF Pages | Handling |
| --- | ---: | ---: | --- |
| Front matter, prefaces, remarks | i-xvi | 1-16 | orientation only |
| Ch. 1 Curves | 1-52 | 17-68 | canonical notebook |
| Ch. 2 Regular Surfaces | 53-135 | 69-151 | canonical notebook; continuity/differentiability appendix integrated |
| Ch. 3 The Geometry of the Gauss Map | 136-219 | 152-235 | canonical notebook; self-adjoint maps appendix integrated |
| Ch. 4 The Intrinsic Geometry of Surfaces | 220-320 | 236-336 | canonical notebook; local theory proofs appendix integrated |
| Ch. 5 Global Differential Geometry | 321-474 | 337-490 | canonical notebook; point-set topology appendix integrated |
| Bibliography, hints, index | 475-513 | 491-529 | orientation only |

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Translation guide from book concepts into computational language.
3. Route through the chapter.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Visual explanations and executable artifacts: diagrams, plots, 3D scenes,
   widgets, symbolic derivations, tables, or computational experiments as needed.
8. Applied lab or design exercise.
9. Sanity checks asserting core identities and artifact existence.
10. Takeaways.

The setup cell should discover the book root by searching upward for both
`00-book-index.ipynb` and `utils`, then prepend that path to `sys.path`.

## Visualization-First Contract

The standard is not a fixed visual count; the standard is whether the notebook
can teach the chapter without the textbook open.

- Artifact filenames must name the concept, not the rendering technology.
- Prose near a visual must name what to inspect.
- Final sanity checks must assert artifact existence, nonzero size, and relevant
  numeric validation data.
- Repeated placeholder visuals are forbidden.
- Do not use textbook screenshots, PDF crops, or decorative images.
- For proof-heavy material, visualize proof state: assumptions, dependency
  graph, limiting process, deformation, orientation, or a small symbolic/numeric
  example.
- Use interactive Plotly, ipywidgets, PyVista, Trimesh, or other installed tools
  when changing a parameter, rotating a model, or inspecting a surface teaches
  the idea.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed
libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`,
`ipywidgets`, `pandas`, `sympy`, `networkx`, `pyvista`, `trimesh`, and the
book-local helpers in `utils/`.

Document optional or external tools rather than adding dependencies unless the
user explicitly asks for a dependency change.

## Artifacts

Store generated outputs under stable unit paths:

```text
artifacts/chapter-01/
artifacts/chapter-02/
...
```

Use subfolders such as `figures/`, `interactive/`, `checks/`, and `tables/`.
Write checks as JSON or CSV when they summarize reproducible invariants. Write
interactive visuals as HTML and static visuals as PNG/SVG.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Differential-Geometry-of-Curves-and-Surfaces/scripts/build_dgcs_course_indexes.py
uv run python -m compileall -q Differential-Geometry-of-Curves-and-Surfaces/utils Differential-Geometry-of-Curves-and-Surfaces/scripts
uv run pytest -q Differential-Geometry-of-Curves-and-Surfaces/scripts
uv run python Differential-Geometry-of-Curves-and-Surfaces/scripts/audit_dgcs_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Differential-Geometry-of-Curves-and-Surfaces/scripts/audit_dgcs_visuals.py
uv run python Differential-Geometry-of-Curves-and-Surfaces/scripts/validate_dgcs_course.py --limit 5 --timeout 300
uv run python Differential-Geometry-of-Curves-and-Surfaces/scripts/validate_dgcs_course.py --all --timeout 300
git diff --check
```

No dependency changes are expected for this course. Run `uv sync` only if
`pyproject.toml` or `uv.lock` changes intentionally.

## Static Checks Before Commit

Before handoff, verify:

- No root-level `utils/`, `artifacts/`, or book-specific `scripts/` directory has
  appeared outside the book folder.
- No notebook or script contains stale root artifact/helper paths.
- Every content folder has one canonical notebook plus `00-index.ipynb`.
- Markdown links resolve for local notebook, helper, JSON, CSV, PNG, HTML, and
  text references.
- The source PDF is preserved but not staged as a generated artifact.

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
