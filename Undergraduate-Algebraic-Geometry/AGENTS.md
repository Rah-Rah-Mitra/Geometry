# Agent Instructions: Undergraduate Algebraic Geometry Notebook Course

    This folder is a standalone visualization-first notebook edition of Miles Reid's
    *Undergraduate Algebraic Geometry*. Treat this folder as the project root for
    the course. The workspace root owns the shared `uv` environment, `pyproject.toml`,
    `uv.lock`, and `.venv`.

    ## Repo-Local Skills

    Use the repo-local skills under `D:\Geometry\.codex\skills`:

    - `geometry-visualization-planner` before planning or revising a chapter storyboard.
    - `geometry-chapter-notebook-author` when authoring or revising a canonical notebook.
    - `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

    ## Non-Negotiables

    - Write original teaching prose, examples, equations, code, diagrams, and checks.
    - Do not copy textbook passages, long exercise text, screenshots, or page crops.
    - A reader must be able to learn from each notebook without opening the PDF.
    - Visualization is part of the explanation, not decoration or a quota.
    - Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
    - Every canonical notebook should execute with `nbclient`.
    - Generated paths in notebooks must be relative or book-local.
    - Preserve the one-canonical-notebook-per-chapter-folder structure.

    ## Course Structure

    ```text
    Undergraduate-Algebraic-Geometry/
      00-book-index.ipynb
      AGENTS.md
      artifacts/
      scripts/
      utils/
      prologue/
      part-i-playing-with-plane-curves/
      part-ii-the-category-of-affine-varieties/
      part-iii-applications/
    ```

    Each chapter folder contains exactly one canonical notebook plus `00-index.ipynb`.
    Part folders also contain a `00-index.ipynb`.

    ## Source Map

    Main-text printed pages map to physical PDF pages by:

    ```text
    physical PDF page = printed page - 2
    ```

    | Unit | Folder | Printed Pages | PDF Pages | Focus |
    | --- | --- | ---: | ---: | --- |
    | Chapter 0 | `prologue/chapter-00-woffle` | 11-18 | 9-16 | Why polynomial zero sets deserve their own geometry, why functions matter, and how algebra replaces local calculus. |
| Chapter 1 | `part-i-playing-with-plane-curves/chapter-01-plane-conics` | 19-34 | 17-32 | Conics as the first laboratory for projective coordinates, parametrization, intersection counting, and linear systems. |
| Chapter 2 | `part-i-playing-with-plane-curves/chapter-02-cubics-and-the-group-law` | 35-54 | 33-52 | Singular and smooth cubics, linear systems, the ninth point, chord-tangent addition, and the first appearance of genus. |
| Chapter 3 | `part-ii-the-category-of-affine-varieties/chapter-03-affine-varieties-and-the-nullstellensatz` | 57-72 | 55-70 | The affine algebra-geometry dictionary: ideals define loci, loci define radical ideals, and finite generation makes the dictionary computable. |
| Chapter 4 | `part-ii-the-category-of-affine-varieties/chapter-04-functions-on-varieties` | 73-84 | 71-82 | Coordinate rings, polynomial maps, pullbacks, function fields, rational maps, standard opens, and when maps are actually isomorphisms. |
| Chapter 5 | `part-iii-applications/chapter-05-projective-and-birational-geometry` | 87-100 | 85-98 | Projective varieties, homogeneous coordinate rings, affine charts, rational maps, birational equivalence, and rational examples. |
| Chapter 6 | `part-iii-applications/chapter-06-tangent-space-nonsingularity-dimension` | 101-108 | 99-106 | Algebraic tangent spaces, singular loci, dimension, intrinsic tangent definitions, and blowups as local resolution experiments. |
| Chapter 7 | `part-iii-applications/chapter-07-the-27-lines-on-a-cubic-surface` | 109-120 | 107-118 | A classical configuration theorem made visible through lines on a cubic surface, polar forms, rationality, and incidence. |
| Chapter 8 | `part-iii-applications/chapter-08-final-comments` | 121-132 | 119-130 | A bridge from classical varieties to sheaves, schemes, nilpotents, arithmetic fibers, and the incidence count behind cubic-surface lines. |

    ## Notebook Shape

    Each canonical notebook should contain:

    1. Title and source span.
    2. Standalone chapter question and motivation.
    3. Translation guide from book concepts into computational language.
    4. Setup cell that discovers `BOOK_ROOT`.
    5. Original concept sections with equations and diagrams.
    6. Executable examples using book-local utilities.
    7. Generated visual artifacts displayed inline.
    8. Applied lab or design exercise.
    9. Sanity checks asserting identities, artifact existence, and nonblank visuals.
    10. Takeaways.

    ## Artifact Contract

    Store generated outputs under:

    ```text
    artifacts/chapter-XX/figures/
    artifacts/chapter-XX/html/
    artifacts/chapter-XX/checks/
    artifacts/chapter-XX/tables/
    ```

    Artifact filenames should name the concept. Every generated artifact should be
    displayed inline or linked from the notebook, and final checks should assert that
    files exist and are nonempty.

    ## Worker Boundaries

    Assign one worker to one canonical notebook, one helper module, or one script task.
    Chapter workers should read their source span, refresh or consume a visualization
    storyboard, and edit only the assigned chapter folder, its artifact subtree, and
    explicitly assigned chapter helpers. Shared utility changes belong to utility
    workers.

    ## Geometry Stack

    Use the shared `uv` environment at the workspace root. Prefer installed libraries:
    `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `pandas`,
    `networkx`, `shapely`, `trimesh`, `pyvista`, `ripser`, and the rest of the root
    geometry stack. This course currently needs no dependency additions.

    Document SageMath, Singular, and other external computer algebra systems as
    optional external tools rather than importing them in canonical notebooks.

    ## Commands

    Run from `D:\Geometry`:

    ```powershell
    uv run python "Undergraduate-Algebraic-Geometry/scripts/build_uag_course_indexes.py"
    uv run python -m compileall -q "Undergraduate-Algebraic-Geometry/utils" "Undergraduate-Algebraic-Geometry/scripts"
    uv run python "Undergraduate-Algebraic-Geometry/scripts/audit_uag_notebooks.py" --min-words 1200 --min-code-cells 5
    uv run python "Undergraduate-Algebraic-Geometry/scripts/audit_uag_visuals.py"
    uv run python "Undergraduate-Algebraic-Geometry/scripts/validate_uag_course.py" --limit 3 --timeout 300
    git diff --check
    ```

    Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

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
