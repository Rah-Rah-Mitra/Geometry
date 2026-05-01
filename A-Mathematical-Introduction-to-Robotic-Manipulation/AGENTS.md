# Agent Instructions: A Mathematical Introduction to Robotic Manipulation Notebook Course

This folder is a standalone visualization-first notebook edition of *A Mathematical Introduction to Robotic Manipulation* by Richard M. Murray, Zexiang Li, and S. Shankar Sastry. Treat this book folder as the project root for the course. The workspace root still owns the shared `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local Codex skills under `D:\Geometry\.codex\skills` for course work:

- `geometry-visualization-planner`: storyboard each chapter before authoring.
- `geometry-chapter-notebook-author`: author the canonical standalone notebook in its chapter folder.
- `geometry-notebook-qc`: review notebooks, artifacts, helpers, stale paths, and execution.

## Non-Negotiables

- Write original teaching prose, derivations, code, diagrams, and explanations.
- Do not copy textbook prose, long exercise text, screenshots, page crops, photos, or tables.
- A reader should not need the PDF open. Each notebook must include motivation, definitions, computational translations, worked examples, pitfalls, sanity checks, applied labs, and takeaways.
- Visualization is central, not decorative. Use diagrams, 2D and 3D plots, widgets, symbolic checks, proof diagrams, mesh or surface views, and computational experiments wherever they clarify the robotics geometry.
- Store course helpers in `utils/`, scripts in `scripts/`, and generated outputs in `artifacts/`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per chapter or appendix folder.
- Keep the PDF local to the source folder. Do not copy it into generated artifacts
  or treat it as a redistributable course output.

## Source Map

The local PDF is `A Mathematical Introduction to Robotic Manipulation.pdf`. Printed pages map to PDF pages by:

```text
pdf_page = printed_page + 18
```

The course follows four parts: foundations and single-robot manipulation, multifingered manipulation, nonholonomic systems, and outlook/appendices.

## Notebook Shape

Each canonical notebook should contain:

1. Title, source span, and chapter question.
2. Translation guide from textbook concepts into computational language.
3. Route through the notebook.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Visual explanations and generated artifacts.
8. Applied lab or design exercise.
9. Sanity checks for identities, artifact existence, and numeric margins.
10. Takeaways.

## Artifact Rules

Artifacts are part of the teaching product. Use stable book-local paths such as:

```text
artifacts/chapter-02/figures/screw-motion-explorer.png
artifacts/chapter-05/checks/final-sanity.json
artifacts/appendix-a/figures/se3-exponential-screw-reference.png
```

Artifact filenames must name the concept, not the rendering technology. Every generated artifact should be displayed inline and asserted in the final sanity cell. Repeated placeholder visuals, blank images, and copied PDF figures are QC failures.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `networkx`, `shapely`, `trimesh`, and `pyvista` are available. Do not add dependencies unless the user explicitly asks.

## Worker Boundaries

For parallel work, assign one worker to one canonical notebook or one clearly bounded helper/script task. Chapter workers may edit only their assigned chapter folder, its matching artifact subtree, and explicitly assigned helper modules. Index and QC workers own global navigation and validation reports.

## Validation Commands

Run from `D:\Geometry`:

```powershell
uv run python -m compileall -q "A Mathematical Introduction to Robotic Manipulation/utils" "A Mathematical Introduction to Robotic Manipulation/scripts"
uv run pytest -q "A Mathematical Introduction to Robotic Manipulation/scripts"
uv run python "A Mathematical Introduction to Robotic Manipulation/scripts/build_robotics_course_indexes.py"
uv run python "A Mathematical Introduction to Robotic Manipulation/scripts/audit_robotics_notebooks.py" --min-words 1200 --min-code-cells 5
uv run python "A Mathematical Introduction to Robotic Manipulation/scripts/audit_robotics_visuals.py"
uv run python "A Mathematical Introduction to Robotic Manipulation/scripts/validate_robotics_course.py" --limit 6 --timeout 300
uv run python "A Mathematical Introduction to Robotic Manipulation/scripts/validate_robotics_course.py" --all --timeout 300
git diff --check
```

Only run `uv sync` if dependencies change.

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
