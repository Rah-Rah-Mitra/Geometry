# Agent Instructions: The Four Pillars of Geometry Notebook Course

This folder is a standalone visualization-first notebook edition of The Four Pillars of Geometry. Treat this folder as the project root for this course. The workspace root owns the shared uv environment, pyproject.toml, uv.lock, and .venv.

## Repo-Local Skills

Use the repo-local skills under D:\Geometry\.codex\skills: geometry-visualization-planner before storyboards, geometry-chapter-notebook-author when authoring canonical notebooks, and geometry-notebook-qc when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, or page crops.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualizations are part of the explanation.
- Keep helpers in utils, generated outputs in artifacts, and validation tools in scripts.
- Every canonical notebook must execute with nbclient.
- Generated paths in notebooks must be relative or book-local.

## Course Structure

The course has 00-book-index.ipynb, AGENTS.md, artifacts, scripts, utils, and four part folders. Each part folder has 00-part-index.ipynb. Each chapter folder has 00-index.ipynb plus exactly one canonical teaching notebook.

## Source Map

Main-body printed pages map to physical PDF pages by pdf_page = printed_page + 10.

| Unit | Folder | Printed Pages | PDF Pages | Focus |
| --- | --- | ---: | ---: | --- |
| Chapter 1 | part-01-euclidean-construction-and-axioms/chapter-01-straightedge-and-compass | 1-19 | 11-29 | Compass/straightedge primitives, equilateral construction, perpendiculars/parallels, constructible arithmetic, similar triangles, irrationality of sqrt(2). |
| Chapter 2 | part-01-euclidean-construction-and-axioms/chapter-02-euclids-approach-to-geometry | 20-45 | 30-55 | Parallel axiom, congruence, area dissection, Pythagorean theorem, Thales theorem, circle angles, regular pentagon construction. |
| Chapter 3 | part-02-linear-algebra/chapter-03-coordinates | 46-64 | 56-74 | Number line/plane, line equations, distances, circle-line intersections, angle/slope, isometry classifier, three-reflections theorem. |
| Chapter 4 | part-02-linear-algebra/chapter-04-vectors-and-euclidean-spaces | 65-87 | 75-97 | Vector operations, linear independence, centroids, inner products, Cauchy-Schwarz, triangle inequality, rotations via matrices and complex numbers. |
| Chapter 5 | part-03-projective-geometry/chapter-05-perspective | 88-116 | 98-126 | Vanishing points, straightedge-only drawing, projective plane models, homogeneous coordinates, projections, linear fractional maps, cross-ratio. |
| Chapter 6 | part-03-projective-geometry/chapter-06-projective-planes | 117-142 | 127-152 | Pappus/Desargues configurations, coincidence diagrams, Moulton-style failure modes, projective arithmetic, field-law dependency visuals. |
| Chapter 7 | part-04-transformation-groups/chapter-07-transformations | 143-173 | 153-183 | Isometry groups, affine/vector transformations, projective-line maps, spherical geometry, rotations, quaternions, finite rotation groups, S^3 and RP^3. |
| Chapter 8 | part-04-transformation-groups/chapter-08-non-euclidean-geometry | 174-212 | 184-222 | Upper-half-plane/disk models, Mobius transformations, reflections, hyperbolic geodesics, distance heatmaps, conformal grids, reflection factorizations. |

References and index pages remain source material only; this course does not create a separate appendix notebook.

## Artifact Contract

Store generated outputs under artifacts/chapter-XX-slug/figures, html, checks, and tables. Artifact filenames should name the concept, not the rendering technology. Repeated placeholder visuals are a QC failure.

## Commands

Run from D:\Geometry:

uv run python The-Four-Pillars-of-Geometry/scripts/build_fpog_course_indexes.py
uv run python -m compileall -q The-Four-Pillars-of-Geometry/utils The-Four-Pillars-of-Geometry/scripts
uv run python The-Four-Pillars-of-Geometry/scripts/audit_fpog_notebooks.py --min-words 1200 --min-code-cells 5
uv run python The-Four-Pillars-of-Geometry/scripts/audit_fpog_visuals.py
uv run python The-Four-Pillars-of-Geometry/scripts/validate_fpog_course.py --limit 4 --timeout 300
git diff --check

Run uv sync only if pyproject.toml or uv.lock changes.

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
