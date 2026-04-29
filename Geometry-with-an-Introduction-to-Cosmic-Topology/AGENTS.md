# Agent Instructions: Geometry with an Introduction to Cosmic Topology Notebook Course

    This folder is a standalone visualization-first notebook edition of *Geometry with an Introduction to Cosmic Topology*.
    Treat this folder as the project root for this course. The workspace root owns the shared `uv`
    environment, `pyproject.toml`, `uv.lock`, and `.venv`.

    ## Repo-Local Skills

    Use the repo-local skills under `D:\Geometry\.codex\skills`:

    - `geometry-visualization-planner` before planning or revising a chapter storyboard.
    - `geometry-chapter-notebook-author` when authoring a canonical notebook.
    - `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

    ## Non-Negotiables

    - Write original teaching prose, examples, code, diagrams, and checks.
    - Do not copy textbook passages, long exercise text, screenshots, or page crops.
    - A reader must be able to learn from each notebook without opening the PDF.
    - Visualizations are part of the explanation. Use diagrams, plots, 3D-style views,
      widgets or HTML parameter labs, symbolic checks, computational experiments, and
      proof-state diagrams wherever they clarify the geometry.
    - Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
    - Every canonical notebook must execute with `nbclient`.
    - Generated paths in notebooks must be relative or book-local.

    ## Course Structure

    ```text
    Geometry-with-an-Introduction-to-Cosmic-Topology/
      00-book-index.ipynb
      AGENTS.md
      artifacts/
      scripts/
      utils/
      chapter-01-an-invitation-to-geometry/
      ...
      chapter-08-cosmic-topology/
      appendix-a-list-of-symbols/
    ```

    Each chapter or appendix folder contains:

    ```text
    00-index.ipynb
    <canonical notebook>.ipynb
    ```

    There should be exactly one canonical teaching notebook in each folder, excluding `00-index.ipynb`.

    ## Source Map

    Main-body printed pages map to physical PDF pages by `pdf_page = printed_page + 10`.

    | Unit | Folder | Printed Pages | PDF Pages | Focus |
    | --- | --- | ---: | ---: | --- |
    | Chapter 1 | `chapter-01-an-invitation-to-geometry` | 1-14 | 11-24 | Local measurement, global shape, finite boundaryless surfaces, and the first split between Euclidean, hyperbolic, and elliptic behavior. |
| Chapter 2 | `chapter-02-the-complex-plane` | 15-28 | 25-38 | Complex numbers as the computational coordinate system for the geometries that follow. |
| Chapter 3 | `chapter-03-transformations` | 29-70 | 39-80 | Inversions, clines, the extended plane, and Mobius transformations as the machinery for non-Euclidean geometry. |
| Chapter 4 | `chapter-04-geometry` | 71-80 | 81-90 | The Erlangen program: a geometry is a space together with a transformation group and its invariants. |
| Chapter 5 | `chapter-05-hyperbolic-geometry` | 81-120 | 91-130 | The Poincare disk and upper half-plane models, hyperbolic geodesics, measurement, area, and triangle defect. |
| Chapter 6 | `chapter-06-elliptic-geometry` | 121-144 | 131-154 | Elliptic geometry from the sphere, stereographic projection, antipodal identification, and projective disk measurement. |
| Chapter 7 | `chapter-07-geometry-on-surfaces` | 145-194 | 155-204 | Curvature scales, the unified family (X_k, G_k), surface topology, Gauss-Bonnet, quotient spaces, and Dirichlet domains. |
| Chapter 8 | `chapter-08-cosmic-topology` | 195-220 | 205-230 | Three-dimensional candidate universes, cosmic crystallography, circles in the sky, and density-parameter evidence. |
| Appendix A | `appendix-a-list-of-symbols` | 221-222 | 231-232 | A compact computational glossary for the symbols used across the course. |

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
    artifacts/appendix-a/
    ```

    Artifact filenames should name the concept, not the rendering technology.
    Repeated placeholder visuals are a QC failure. Every generated artifact should be displayed inline
    or linked from the notebook, and final checks should assert that files exist and are nonempty.

    ## Geometry Stack

    Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding
    dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `pandas`,
    `networkx`, `shapely`, `trimesh`, `pyvista`, `ripser`, and the rest of the root geometry stack.
    This course currently needs no dependency additions.

    ## Worker Boundaries

    Assign one worker to one canonical notebook, one helper module, or one script task.
    Chapter workers may edit only their chapter folder, matching artifact subtree, and explicitly
    assigned helper module. Index workers own `00-book-index.ipynb` and `00-index.ipynb` files.
    QC workers run audits and validation and report findings.

    ## Commands

    Run from `D:\Geometry`:

    ```powershell
    uv run python Geometry-with-an-Introduction-to-Cosmic-Topology/scripts/build_gict_course_indexes.py
    uv run python -m compileall -q Geometry-with-an-Introduction-to-Cosmic-Topology/utils Geometry-with-an-Introduction-to-Cosmic-Topology/scripts
    uv run python Geometry-with-an-Introduction-to-Cosmic-Topology/scripts/audit_gict_notebooks.py --min-words 1200 --min-code-cells 5
    uv run python Geometry-with-an-Introduction-to-Cosmic-Topology/scripts/audit_gict_visuals.py
    uv run python Geometry-with-an-Introduction-to-Cosmic-Topology/scripts/validate_gict_course.py --limit 4 --timeout 300
    git diff --check
    ```

    Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.
