# Agent Instructions: Geometry II Visualization-First Notebook Course

This folder is a standalone notebook edition of Marcel Berger's *Geometry II*,
Volume II. Treat this folder as the project root for this course. The workspace
root still owns the shared `uv` environment.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills` for course work:

- `geometry-visualization-planner` for chapter storyboards.
- `geometry-chapter-notebook-author` for authoring canonical notebooks.
- `geometry-notebook-qc` for standalone, artifact, and execution review.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, page screenshots, or page crops.
- The notebooks must stand alone without the PDF open.
- Visualization is part of the teaching argument, not decoration or a fixed quota.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook per chapter folder plus a local `00-index.ipynb`.
- Keep the original PDF out of generated artifacts and never stage extracted page images.

## Source Map

The PDF has 415 pages. The visible body in this file is Volume II of Berger's
work and covers Chapters 12-20. The table of contents, bibliography, notation
index, and general index are reference material, not teaching notebooks.

Use `pdf_page = printed_volume_ii_page + 9`.

- Chapter 12: `chapter-12-polytopes-compact-convex-sets/12-polytopes-compact-convex-sets.ipynb`; printed pp. 1-85; PDF pp. 10-94; Polytopes, compact convex sets, volume, area, regular polytopes, Euler's formula, Cauchy's theorem, approximation, and isoperimetry.
- Chapter 13: `chapter-13-quadratic-forms/13-quadratic-forms.ipynb`; printed pp. 86-115; PDF pp. 95-124; Quadratic forms, signatures, isotropic cones, radicals, orthogonalization, Witt decomposition, and reflection factorizations.
- Chapter 14: `chapter-14-projective-quadrics/14-projective-quadrics.ipynb`; printed pp. 116-145; PDF pp. 125-154; Projective quadrics, pencils, topology, polarity, tangent geometry, and projective group actions.
- Chapter 15: `chapter-15-affine-quadrics/15-affine-quadrics.ipynb`; printed pp. 146-169; PDF pp. 155-178; Affine quadrics, reductions of quadratic forms, classification, topology, polarity, and Euclidean models.
- Chapter 16: `chapter-16-projective-conics/16-projective-conics.ipynb`; printed pp. 170-217; PDF pp. 179-226; Projective conics, parametrizations, cross-ratios, Pascal's theorem, homographies, intersections, Bezout, and pencils.
- Chapter 17: `chapter-17-euclidean-conics/17-euclidean-conics.ipynb`; printed pp. 218-254; PDF pp. 227-263; Euclidean conics, metric properties, cyclic points, tangential pencils, ellipses, and hyperbolas.
- Chapter 18: `chapter-18-the-sphere-for-its-own-sake/18-the-sphere-for-its-own-sake.ipynb`; printed pp. 255-317; PDF pp. 264-326; Spheres, charts, projections, topology, canonical measure, intrinsic metric, spherical triangles, Clifford parallelism, Villarceau circles, and the Mobius group.
- Chapter 19: `chapter-19-elliptic-and-hyperbolic-geometry/19-elliptic-and-hyperbolic-geometry.ipynb`; printed pp. 318-348; PDF pp. 327-357; Elliptic geometry, hyperbolic projective and ball models, distance formulas, isometries, measure, and Poincare models.
- Chapter 20: `chapter-20-the-space-of-spheres/20-the-space-of-spheres.ipynb`; printed pp. 349-362; PDF pp. 358-371; Generalized spheres, the fundamental quadratic form, orthogonality, sphere intersections, pencils, the circular group, and polyspheric coordinates.

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

## Artifact Contract

Artifacts are part of the learning product. Store them under stable chapter paths:

```text
artifacts/chapter-12/checks/
artifacts/chapter-12/figures/
artifacts/chapter-12/plots/
artifacts/chapter-12/tables/
...
artifacts/chapter-20/checks/
```

Rules:

- Write checks as JSON or CSV when they summarize reproducible invariants.
- Write interactive visuals as HTML and static visuals as PNG/SVG.
- Reference artifacts in prose using paths such as `artifacts/chapter-18/...`.
- Do not store scans, page crops, or copyrighted page images.
- If a notebook generates an artifact, include a final assertion that the file exists.
- Repeated placeholder visuals are a QC failure unless explicitly justified.

## Geometry Stack

Use the shared `uv` environment at `D:\Geometry`. Prefer installed packages before
adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`,
`sympy`, `networkx`, `pyvista`, `trimesh`, `PIL`, `shapely`, and the other
packages listed in the repo-local geometry library catalog. Document external-only
tools rather than importing them.

## Worker Boundaries

Assign one worker to one canonical notebook or one shared helper/script task.
Chapter workers should read their assigned source span, consume or create a
visualization storyboard, and edit only the assigned chapter folder, its artifact
subtree, and any explicitly assigned helper.

Suggested roles:

- Visualization planner: reads the source span and proposes the visual storyboard.
- Chapter worker: authors one canonical notebook and local artifacts.
- Utility worker: implements shared geometry helpers and tests.
- Index worker: regenerates `00-book-index.ipynb` and chapter indexes.
- QC worker: runs audits, validates links, executes notebooks, and checks stale paths.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Geometry-II/scripts/build_geometry_ii_course_indexes.py
uv run python -m compileall -q Geometry-II/utils Geometry-II/scripts
uv run python Geometry-II/scripts/audit_geometry_ii_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Geometry-II/scripts/audit_geometry_ii_visuals.py
uv run python Geometry-II/scripts/validate_geometry_ii_course.py --limit 4 --timeout 300
uv run python Geometry-II/scripts/validate_geometry_ii_course.py --all --timeout 300
git diff --check
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Static Checks Before Commit

Before committing, verify:

- No root-level `utils/`, `artifacts/`, or book-specific `scripts/` directory has reappeared.
- No notebook or script contains stale root artifact/helper paths.
- Every chapter folder has one canonical notebook plus `00-index.ipynb`.
- Markdown links resolve for local notebook, helper, JSON, CSV, PNG, HTML, and text references.
- No PDF files are staged.

Useful stale-path patterns:

```text
D:/Geometry/artifacts
D:\Geometry\artifacts
/mnt/d/Geometry/artifacts
D:/Geometry/utils
D:\Geometry\utils
/mnt/d/Geometry/utils
D:/Geometry/scripts
D:\Geometry\scripts
/mnt/d/Geometry/scripts
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
