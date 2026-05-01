# Agent Instructions: Differential Geometry From Elastic Curves to Willmore Surfaces

        This folder is a standalone notebook edition of *Differential Geometry: From Elastic Curves to Willmore Surfaces* by Ulrich Pinkall and Oliver Gross. Treat this folder as the project root for this course. The workspace root still owns the shared `uv` environment.

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

        The PDF has 204 pages. The body has two parts, 13 chapters, two appendices, references, and index.

        - Chapter 01: `part-01-curves/chapter-01-curves-in-rn/01-curves-in-rn.ipynb`; printed pp. 3-11; PDF pp. 13-21; Regular parametrized curves, reparametrization, length, arclength, unit tangent, and bending energy.
- Chapter 02: `part-01-curves/chapter-02-variations-of-curves/02-variations-of-curves.ipynb`; printed pp. 13-27; PDF pp. 22-37; One-parameter curve families, variational vector fields, first variation, constrained criticality, and elastica.
- Chapter 03: `part-01-curves/chapter-03-curves-in-r2/03-curves-in-r2.ipynb`; printed pp. 29-45; PDF pp. 38-55; Signed curvature, sector area, planar elastica, tangent winding, and regular homotopy.
- Chapter 04: `part-01-curves/chapter-04-parallel-normal-fields/04-parallel-normal-fields.ipynb`; printed pp. 47-57; PDF pp. 56-66; Parallel normal transport, curvature functions, and reconstruction of curves from normal-plane data.
- Chapter 05: `part-01-curves/chapter-05-curves-in-r3/05-curves-in-r3.ipynb`; printed pp. 59-85; PDF pp. 67-92; Total torsion, elastic space curves, vortex filament flow, framed curves, twist energy, and Frenet-normal limitations.
- Chapter 06: `part-02-surfaces/chapter-06-surfaces-and-riemannian-geometry/06-surfaces-and-riemannian-geometry.ipynb`; printed pp. 87-103; PDF pp. 94-110; Parametrized surfaces, tangent spaces, induced metrics, area forms, metric rotation, and isometry.
- Chapter 07: `part-02-surfaces/chapter-07-integration-and-stokes-theorem/07-integration-and-stokes-theorem.ipynb`; printed pp. 105-115; PDF pp. 111-121; Integration on surfaces and curves, one-forms, two-forms, pullback, boundary orientation, and Stokes' theorem.
- Chapter 08: `part-02-surfaces/chapter-08-curvature/08-curvature.ipynb`; printed pp. 117-129; PDF pp. 122-134; Unit normal, shape operator, principal curvature, mean curvature, Gaussian curvature, umbilics, and Gauss-map area.
- Chapter 09: `part-02-surfaces/chapter-09-levi-civita-connection/09-levi-civita-connection.ipynb`; printed pp. 131-137; PDF pp. 135-142; Tangential differentiation, Levi-Civita connection, Gauss and Codazzi equations, and Theorema Egregium.
- Chapter 10: `part-02-surfaces/chapter-10-total-gaussian-curvature/10-total-gaussian-curvature.ipynb`; printed pp. 139-149; PDF pp. 143-153; Curves on surfaces, total Gaussian curvature, Gauss-Bonnet, and parallel transport holonomy.
- Chapter 11: `part-02-surfaces/chapter-11-closed-surfaces/11-closed-surfaces.ipynb`; printed pp. 151-160; PDF pp. 154-163; Boundary gluing, oriented and non-oriented closed surfaces, orientation covers, genus, and total curvature.
- Chapter 12: `part-02-surfaces/chapter-12-variations-of-surfaces/12-variations-of-surfaces.ipynb`; printed pp. 161-179; PDF pp. 164-182; Surface vector calculus, one-parameter surface families, curvature variation, area variation, volume variation, minimal and CMC surfaces.
- Chapter 13: `part-02-surfaces/chapter-13-willmore-surfaces/13-willmore-surfaces.ipynb`; printed pp. 181-191; PDF pp. 183-193; Willmore functional, Willmore equation, energy offsets, cylinder examples, and inversion invariance.
- Appendix A: `part-03-appendices/appendix-a-some-technicalities/appendix-a-some-technicalities.ipynb`; printed pp. 193-196; PDF pp. 194-197; Smooth maps on closed domains, support, bump functions, and smooth cutoffs.
- Appendix B: `part-03-appendices/appendix-b-timeline/appendix-b-timeline.ipynb`; printed pp. 197-198; PDF pp. 198-199; A navigable timeline connecting elastic curves, surface theory, topology, variational calculus, and Willmore surfaces.

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

        Use the shared `uv` environment at `D:\Geometry`. Prefer installed packages before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `networkx`, `pyvista`, `trimesh`, `PIL`, and the other packages listed in the repo-local geometry library catalog. Document external-only tools rather than importing them.

        ## Worker Boundaries

        Assign one worker to one canonical notebook or one shared helper/script task. Chapter workers should read their assigned source span, consume or create a visualization storyboard, and edit only the assigned chapter folder, its artifact subtree, and any explicitly assigned helper.

        ## Commands

        Run from `D:\Geometry`:

        ```powershell
        uv run python Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/scripts/build_dgecws_course_indexes.py
        uv run python -m compileall -q Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/utils Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/scripts
        uv run python Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/scripts/audit_dgecws_notebooks.py --min-words 1200 --min-code-cells 5
        uv run python Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/scripts/audit_dgecws_visuals.py
        uv run python Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/scripts/validate_dgecws_course.py --limit 8 --timeout 300
        uv run python Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/scripts/validate_dgecws_course.py --all --timeout 300
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
