# Agent Instructions: Computational Geometry Algorithms and Applications Notebook Course

This folder is a standalone notebook edition of *Computational Geometry: Algorithms and Applications*, Third Edition. Agents should treat this folder as the project root for this course. The workspace root still owns the shared Python environment files.

## Repo-Local Skills

Use the repo-local Codex skills under `D:\Geometry\.codex\skills` for chapter work:

- `geometry-visualization-planner`: read an assigned chapter/page span and produce the visual storyboard before authoring.
- `geometry-chapter-notebook-author`: author the standalone visual-first canonical notebook directly in its chapter folder.
- `geometry-notebook-qc`: review notebooks, artifacts, execution, visual relevance, stale paths, and dependency fit before handoff.

When using parallel workers, pass the relevant skill path and source span. Assign one worker to one canonical notebook, one helper module, or one script task. Chapter workers are not alone in the codebase; they must not revert other workers' edits and should only touch their assigned chapter folder, matching artifact subtree, and explicitly assigned helper.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or figures.
- A notebook must stand alone from the PDF: include motivation, definitions, worked examples, pitfalls, checks, and takeaways.
- Visualization is part of delivery, not decoration or a quota. Use diagrams, plots, widgets, symbolic checks, 3D views, proof-state diagrams, and computational experiments wherever they clarify the chapter.
- Keep helpers in `utils/`, outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per chapter folder.

## Source Map

The PDF contains 16 chapters, followed by bibliography and index. There are no appendices or formal part divisions in the PDF. Body printed pages map to PDF pages by:

```text
pdf_page = printed_page + 11
```

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Translation guide from book concepts into computational language.
3. Route through the chapter.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Visual explanations and executable artifacts: diagrams, plots, 3D scenes, widgets, symbolic derivations, tables, or computational experiments as needed.
8. Applied lab or design exercise.
9. Sanity checks asserting core identities and artifact existence.
10. Takeaways.

## Visualization-First Contract

The standard is not a fixed visual count; the standard is whether the notebook can teach the chapter without the textbook open.

- Artifact filenames must name the concept, not the rendering technology.
- Prose near a visual must name what to inspect.
- Final sanity checks must assert artifact existence, nonzero size, and relevant numeric validation data.
- Repeated placeholder visuals are forbidden.
- Do not use textbook screenshots, PDF crops, or decorative images.
- For proof-heavy material, visualize proof state: assumptions, dependency graph, limiting process, deformation, orientation, or a small symbolic/numeric example.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed libraries: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `pandas`, `shapely`, `networkx`, `sympy`, `pyvista`, `trimesh`, and the rest of the repo-local geometry stack. Document optional tools rather than adding dependencies unless explicitly requested.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python "Computational Geometry Algorithms and Applications/scripts/build_cgaa_course_indexes.py"
uv run python -m compileall -q "Computational Geometry Algorithms and Applications/utils" "Computational Geometry Algorithms and Applications/scripts"
uv run pytest -q "Computational Geometry Algorithms and Applications/scripts"
uv run python "Computational Geometry Algorithms and Applications/scripts/audit_cgaa_notebooks.py" --min-words 1200 --min-code-cells 5
uv run python "Computational Geometry Algorithms and Applications/scripts/audit_cgaa_visuals.py"
uv run python "Computational Geometry Algorithms and Applications/scripts/validate_cgaa_course.py" --smoke --timeout 300
uv run python "Computational Geometry Algorithms and Applications/scripts/validate_cgaa_course.py" --all --timeout 300
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
