# Agent Instructions: Geometric Tools For Computer Graphics Notebook Course

This folder is a standalone notebook edition of *Geometric Tools for Computer Graphics* by Philip J. Schneider and David H. Eberly. Treat this folder as the project root for this course. The workspace root still owns the shared `uv` environment.

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
- Preserve one canonical teaching notebook per chapter or appendix folder plus a local `00-index.ipynb`.

## Source Map

The PDF has 1056 physical pages. Printed body page 1 starts on PDF page 48, so body spans use `pdf_page = printed_page + 47`. The course uses inferred parts because the book table of contents does not define formal parts.

- Chapter 01: `part-01-foundations/chapter-01-introduction/01-introduction.ipynb`; printed pp. 1-8; PDF pp. 48-55; Floating-point failure modes, parameter-domain search, robust predicates, and the shared pattern behind geometric queries.
- Chapter 02: `part-01-foundations/chapter-02-matrices-and-linear-systems/02-matrices-and-linear-systems.ipynb`; printed pp. 9-62; PDF pp. 56-109; Linear maps, row reduction, rank, determinants, eigenspaces, Euclidean inner products, and least-squares fitting.
- Chapter 03: `part-01-foundations/chapter-03-vector-algebra/03-vector-algebra.ipynb`; printed pp. 63-108; PDF pp. 110-155; Affine and vector-space distinction, frames, orientation, barycentric coordinates, simplexes, and geometric operations.
- Chapter 04: `part-01-foundations/chapter-04-matrices-vector-algebra-and-transformations/04-matrices-vector-algebra-and-transformations.ipynb`; printed pp. 109-170; PDF pp. 156-217; Homogeneous point/vector representation, affine transformations, projections, change of basis, and normal-vector transforms.
- Chapter 05: `part-02-2d-geometric-tools/chapter-05-geometric-primitives-in-2d/05-geometric-primitives-in-2d.ipynb`; printed pp. 171-188; PDF pp. 218-235; Line, ray, segment, triangle, rectangle, polygon, conic, Bezier, B-spline, and NURBS representations.
- Chapter 06: `part-02-2d-geometric-tools/chapter-06-distance-in-2d/06-distance-in-2d.ipynb`; printed pp. 189-240; PDF pp. 236-287; Closest-point regions for points, linear components, polygons, quadratic curves, polynomial curves, and GJK distance.
- Chapter 07: `part-02-2d-geometric-tools/chapter-07-intersection-in-2d/07-intersection-in-2d.ipynb`; printed pp. 241-284; PDF pp. 288-331; Intersections among linear components, curves, convex polygons, moving objects, and the method of separating axes.
- Chapter 08: `part-02-2d-geometric-tools/chapter-08-miscellaneous-2d-problems/08-miscellaneous-2d-problems.ipynb`; printed pp. 285-324; PDF pp. 332-371; Circle and line constructions with tangency, prescribed radius, offsets, perpendicularity, and solution multiplicity.
- Chapter 09: `part-03-3d-geometric-tools/chapter-09-geometric-primitives-in-3d/09-geometric-primitives-in-3d.ipynb`; printed pp. 325-364; PDF pp. 372-411; Lines, rays, segments, planes, planar components, meshes, polyhedra, quadrics, torus, curves, and surfaces.
- Chapter 10: `part-03-3d-geometric-tools/chapter-10-distance-in-3d/10-distance-in-3d.ipynb`; printed pp. 365-480; PDF pp. 412-527; Point, line, ray, segment, triangle, rectangle, box, polyhedron, quadric, curve, surface, and geodesic distances.
- Chapter 11: `part-03-3d-geometric-tools/chapter-11-intersection-in-3d/11-intersection-in-3d.ipynb`; printed pp. 481-662; PDF pp. 528-709; Intersection tests for linear components, planes, triangles, polyhedra, quadrics, polynomial surfaces, bounding boxes, cylinders, and torus.
- Chapter 12: `part-03-3d-geometric-tools/chapter-12-miscellaneous-3d-problems/12-miscellaneous-3d-problems.ipynb`; printed pp. 663-672; PDF pp. 710-719; Projection of points and vectors onto planes, line-plane angles, plane-plane angles, and planes through geometric constraints.
- Chapter 13: `part-04-computational-geometry/chapter-13-computational-geometry-topics/13-computational-geometry-topics.ipynb`; printed pp. 673-826; PDF pp. 720-873; BSP trees, point containment, Boolean operations, convex hulls, Delaunay triangulation, polygon partitioning, minimum bounds, area, and volume.
- Appendix A: `part-05-appendices/appendix-a-numerical-methods/appendix-a-numerical-methods.ipynb`; printed pp. 827-922; PDF pp. 874-969; Linear solvers, polynomial systems, decompositions, rotations, root finding, minimization, least-squares fitting, subdivision, and calculus tools.
- Appendix B: `part-05-appendices/appendix-b-trigonometry/appendix-b-trigonometry.ipynb`; printed pp. 923-948; PDF pp. 970-995; Angles, trigonometric functions, identities, laws, inverse branches, derivatives, integrals, and conversion examples.
- Appendix C: `part-05-appendices/appendix-c-basic-formulas-for-geometric-primitives/appendix-c-basic-formulas-for-geometric-primitives.ipynb`; printed pp. 949-959; PDF pp. 996-1006; Formula atlas for triangles, quadrilaterals, circles, polyhedra, cylinders, cones, spheres, and torus primitives.

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

## Geometry Stack

Use the shared `uv` environment at `D:\Geometry`. Prefer installed packages before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `networkx`, `shapely`, `pyvista`, `trimesh`, `PIL`, and the other packages listed in the repo-local geometry library catalog. Document external-only tools rather than importing them.

## Worker Boundaries

Assign one worker to one canonical notebook or one shared helper/script task. Chapter workers should read their assigned source span, consume or create a visualization storyboard, and edit only the assigned chapter folder, its artifact subtree, and any explicitly assigned helper.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python "Geometric Tools for Computer Graphics/scripts/build_gtcg_course_indexes.py"
uv run python -m compileall -q "Geometric Tools for Computer Graphics/utils" "Geometric Tools for Computer Graphics/scripts"
uv run python "Geometric Tools for Computer Graphics/scripts/audit_gtcg_notebooks.py" --min-words 1200 --min-code-cells 5
uv run python "Geometric Tools for Computer Graphics/scripts/audit_gtcg_visuals.py"
uv run python "Geometric Tools for Computer Graphics/scripts/validate_gtcg_course.py" --limit 8 --timeout 300
uv run python "Geometric Tools for Computer Graphics/scripts/validate_gtcg_course.py" --all --timeout 300
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
