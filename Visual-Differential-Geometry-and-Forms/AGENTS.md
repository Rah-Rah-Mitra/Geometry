# Agent Instructions: Visual Differential Geometry and Forms Notebook Course

This folder is a standalone notebook edition of *Visual Differential Geometry and Forms*.
Agents should treat this folder as the project root for this course. The workspace root
still owns the shared Python environment files.

## Repo-Local Skills

This workspace includes repo-local Codex skills under `D:\Geometry\.codex\skills`.
Use them when assigning or doing chapter work:

- `geometry-visualization-planner`: create a visual storyboard and library choices
  before notebook authoring.
- `geometry-chapter-notebook-author`: author or revise a standalone visual-first
  chapter notebook directly in its chapter folder.
- `geometry-notebook-qc`: review notebooks, artifacts, execution, and visual
  relevance before handoff.

When using parallel agents, pass the relevant skill path and the assigned source span
to each worker. The skills contain the shared geometry library catalog.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, or page screenshots.
- A notebook must be useful without opening the PDF: include motivation, definitions,
  worked examples, pitfalls, checks, and takeaways.
- Visualization is part of delivery, not a decoration or quota. Use diagrams, 3D
  plots, widgets, symbolic checks, mesh/surface views, proof diagrams, and
  computational experiments wherever they clarify the chapter's geometry.
- Keep helpers in `utils/`, outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve the one-canonical-notebook-per-folder structure.
- Chapter workers must read the assigned source span before editing and should author
  the full canonical notebook directly rather than driving chapter work from a large
  bootstrap script.

## Source Map

Body printed pages map to PDF pages by `pdf_page = printed_page + 29`.
The course follows the book's five-act structure:

- Prologue: visual meaning versus empty calculation.
- Act I: Chapters 1-3, the nature of space.
- Act II: Chapters 4-7, the metric.
- Act III: Chapters 8-20, curvature.
- Act IV: Chapters 21-31, parallel transport.
- Act V: Chapters 32-39, forms.

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Translation guide from book concepts into computational language.
3. Route through the chapter.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Visual explanations and executable artifacts: diagrams, plots, 3D scenes,
   widgets, symbolic derivations, tables, or computational experiments as the
   concepts require.
8. Applied lab or design exercise.
9. Sanity checks asserting core identities and artifact existence.
10. Takeaways.

## Visualization-First Contract

Canonical notebooks should use visual and computational forms wherever they improve
the delivery of the geometry. The standard is not a fixed count; the standard is
whether the notebook can stand alone as a clearer learning product than a passive
textbook reading.

Visuals are part of the teaching argument:

- The artifact filename must name the concept, for example
  `holonomy-loop-meter.png`, not `figure.png`.
- The notebook prose near the visual must name the concept, parameters, and the
  invariant or behavior the reader should inspect.
- Final sanity checks must assert the visual path exists, has nonzero size, and
  records relevant numeric validation values in `final-sanity.json`.
- Repeated placeholder visuals are forbidden. A repeated artifact hash is a QC
  failure unless the exact file is intentionally allowlisted in the visual audit.
- Do not use textbook screenshots, PDF page crops, or decorative images that do
  not express chapter content.
- For proof-heavy material, visualize the proof state where possible: assumptions,
  dependencies, limiting processes, deformations, counterexamples, orientation
  changes, or small symbolic/numeric examples that make the invariant visible.
- Use interactive Plotly, ipywidgets, PyVista, Trimesh, or other installed tools when
  changing a parameter, rotating a model, or inspecting a surface teaches the idea.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed libraries
before adding dependencies:

| Use case | Installed libraries |
| --- | --- |
| General plotting | `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `ipympl`, `pandas`, `polars`, `seaborn` |
| 3D surfaces and meshes | `pyvista`, `trimesh`, `meshio`, `gpytoolbox`, `manifold3d`, `potpourri3d`, `robust_laplacian`, `mapbox_earcut`, `xatlas`, `trame` |
| Computational geometry | `scipy.spatial`, `shapely`, `networkx` |
| Symbolic geometry | `sympy`, `galgebra` |
| Geometric algebra | `kingdon`, `clifford`, `galgebra`, `pyganja`, course-local helpers |
| Computer vision | `cv2` from `opencv-contrib-python`, `skimage`, `kornia`, `torch`, `torchvision` |
| Riemannian/statistical geometry | `geomstats`, `pyriemann` |
| Optimal transport | `ot` from POT, `geomloss` |
| Topological data analysis | `ripser`, `gudhi`, `persim` |
| GIS/geometric maps | `geopandas`, `rasterio`, `fiona`, `pyproj`, `pyogrio`, `osmnx`, `contextily`, `folium`, `pydeck` |

Document these as optional/external rather than importing them in canonical
notebooks: `open3d` is not available for the current CPython 3.13 environment,
`meshplot` and `singular` do not resolve from the package registry here, and
SageMath/Singular require an external Sage/Singular installation.

## Worker Boundaries

Assign one worker to one canonical notebook, one helper module, or one script task.
Chapter workers read their assigned source span, design or consume a visualization
storyboard, and edit only their chapter folder, matching artifact subtree, and any
explicitly assigned chapter helper. Shared utility changes belong to utility workers.
Avoid using `bootstrap_vdgf_course.py` for chapter-level improvement work unless the
assignment is explicitly a bootstrap or regeneration task.

Suggested worker roles:

- Visualization planner: reads the source span and proposes the visual storyboard.
- Chapter worker: authors one canonical notebook and local artifacts.
- Utility worker: implements shared differential-geometry/forms helpers and tests.
- Dependency/library worker: checks installed packages and recommends compatible
  tools for chapter visuals.
- Index worker: regenerates `00-book-index.ipynb` and part indexes.
- QC worker: runs audits, validates links, executes notebooks, and checks stale paths.

## Commands

Run from the workspace root:

```powershell
uv run python Visual-Differential-Geometry-and-Forms/scripts/build_vdgf_course_indexes.py
uv run python Geometric-Algebra-for-Computer-Science/scripts/smoke_geometry_stack.py
uv run python -m compileall -q Visual-Differential-Geometry-and-Forms/utils Visual-Differential-Geometry-and-Forms/scripts
uv run pytest -q Visual-Differential-Geometry-and-Forms/scripts
uv run python Visual-Differential-Geometry-and-Forms/scripts/audit_vdgf_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Visual-Differential-Geometry-and-Forms/scripts/audit_vdgf_visuals.py
uv run python Visual-Differential-Geometry-and-Forms/scripts/validate_vdgf_course.py --limit 8 --timeout 300
uv run python Visual-Differential-Geometry-and-Forms/scripts/validate_vdgf_course.py --all --timeout 300
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
