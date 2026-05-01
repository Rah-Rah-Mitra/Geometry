# Agent Instructions: Euclidean and Non-Euclidean Geometries Notebook Course

This folder is a standalone notebook edition of *Euclidean and Non-Euclidean
Geometries: Development and History*, Third Edition, by Marvin Jay Greenberg.
Treat this folder as the project root for this course. The workspace root still
owns the shared `uv` environment.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills` for course work:

- `geometry-visualization-planner` for chapter storyboards.
- `geometry-chapter-notebook-author` for authoring canonical notebooks.
- `geometry-notebook-qc` for standalone, artifact, and execution review.

When using parallel workers, assign one worker to one canonical notebook, one
helper module, or one script task. Chapter workers are not alone in the codebase;
they must not revert other workers' edits and should only touch their assigned
chapter folder, matching artifact subtree, and explicitly assigned helper.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or
  figures.
- The notebooks must stand alone without the PDF open.
- Visualization is part of the teaching argument, not decoration or a fixed quota.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools
  in `scripts/`.
- Every canonical notebook must execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per chapter or
  appendix folder.

## Source Map

The PDF is a 502-page scanned/image-only file. Use rendered page images only as
temporary source-orientation aids. Do not store those rendered pages as course
artifacts or display them in notebooks.

Body printed pages map to PDF pages by:

```text
pdf_page = printed_page + 18
```

The course follows the book's chapter structure:

- Introduction: printed pp. 1-5; PDF pp. 19-23; parallel problem and the
  Euclidean/non-Euclidean course map.
- Chapter 01: printed pp. 6-37; PDF pp. 24-55; Euclid's postulates, constructions,
  diagram danger, and parallel-postulate attempts.
- Chapter 02: printed pp. 38-69; PDF pp. 56-87; logic, proof, incidence geometry,
  models, isomorphism, projective and affine planes.
- Chapter 03: printed pp. 70-114; PDF pp. 88-132; Hilbert-style axiom families,
  betweenness, congruence, continuity, and parallelism.
- Chapter 04: printed pp. 115-147; PDF pp. 133-165; neutral geometry, angle sums,
  Saccheri-Legendre, and equivalent parallel postulates.
- Chapter 05: printed pp. 148-176; PDF pp. 166-194; historical attempts at the
  parallel postulate and the assumptions they expose.
- Chapter 06: printed pp. 177-222; PDF pp. 195-240; the discovery of hyperbolic
  geometry, limiting parallels, angle sums, and similar-triangle rigidity.
- Chapter 07: printed pp. 223-289; PDF pp. 241-307; consistency by models,
  Beltrami-Klein and Poincare models, inversion, and cross-ratio distance.
- Chapter 08: printed pp. 290-308; PDF pp. 308-326; philosophical implications,
  physical space, and the status of axioms.
- Chapter 09: printed pp. 309-385; PDF pp. 327-403; geometric transformations,
  groups, reflections, motions, automorphisms, and symmetry.
- Chapter 10: printed pp. 386-437; PDF pp. 404-455; further hyperbolic geometry,
  defect, angle of parallelism, cycles, trigonometry, and the pseudosphere.
- Appendix A: printed pp. 438-453; PDF pp. 456-471; elliptic and Riemannian
  geometries.
- Appendix B: printed pp. 454-460; PDF pp. 472-478; geometry without continuity.

Reference matter on printed pp. 461-484 is linked from the book index and folded
into `utils/axioms.py` rather than converted into separate teaching notebooks.

## Notebook Shape

Each canonical notebook should contain:

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

## Visualization-First Contract

The standard is not a fixed visual count; the standard is whether the notebook can
teach the chapter without the textbook open.

- Artifact filenames must name the concept, not the rendering technology.
- Prose near a visual must name what to inspect.
- Final sanity checks must assert artifact existence, nonzero size, and relevant
  numeric validation data.
- Repeated placeholder visuals are forbidden.
- Do not use textbook screenshots, PDF crops, or decorative images.
- For proof-heavy material, visualize proof state: assumptions, dependency graph,
  limiting process, deformation, orientation, or a small symbolic/numeric example.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed packages:
`numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `pandas`, `shapely`,
`networkx`, `sympy`, `pyvista`, `trimesh`, and the rest of the repo-local geometry
stack. Document optional tools rather than adding dependencies unless explicitly
requested.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Euclidean-and-Non-Euclidean-Geometries/scripts/build_eneg_course_indexes.py
uv run python -m compileall -q Euclidean-and-Non-Euclidean-Geometries/utils Euclidean-and-Non-Euclidean-Geometries/scripts
uv run pytest -q Euclidean-and-Non-Euclidean-Geometries/scripts
uv run python Euclidean-and-Non-Euclidean-Geometries/scripts/audit_eneg_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Euclidean-and-Non-Euclidean-Geometries/scripts/audit_eneg_visuals.py
uv run python Euclidean-and-Non-Euclidean-Geometries/scripts/validate_eneg_course.py --smoke --timeout 300
uv run python Euclidean-and-Non-Euclidean-Geometries/scripts/validate_eneg_course.py --all --timeout 300
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
