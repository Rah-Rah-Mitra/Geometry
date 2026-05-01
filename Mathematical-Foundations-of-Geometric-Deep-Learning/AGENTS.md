        # Agent Instructions: Mathematical Foundations of Geometric Deep Learning Notebook Course

        This folder is a standalone visualization-first notebook edition of *Mathematical Foundations of Geometric Deep Learning* by Haitz Saez de Ocariz Borde and Michael Bronstein. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

        ## Repo-Local Skills

        Use the repo-local skills under `D:\Geometry\.codex\skills`:

        - `geometry-visualization-planner` before planning a chapter storyboard.
        - `geometry-chapter-notebook-author` when authoring canonical notebooks.
        - `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

        ## Non-Negotiables

        - Write original teaching prose, examples, code, diagrams, and checks.
        - Do not copy textbook passages, long exercise text, screenshots, page crops, or textbook figures.
        - A reader must be able to learn from each notebook without opening the PDF.
        - Visualization is part of the explanation. Use diagrams, plots, interactive HTML, symbolic checks, graph diagnostics, proof diagrams, and computational experiments wherever they clarify the chapter.
        - Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
        - Every canonical notebook must execute with `nbclient`.
        - Generated paths in notebooks must be relative or book-local.
        - Preserve one canonical teaching notebook per chapter folder plus a local `00-index.ipynb`.

        ## Source Map

        The PDF has 78 physical pages. The title/front matter and table of contents occupy pages 1-3. There are seven numbered chapters, references on page 78, no formal parts, and no appendices.

        | Chapter | Folder | Title | PDF Pages | Visual Spine |
        | --- | --- | --- | ---: | --- |
        | 01 | `chapter-01-algebraic-structures` | Algebraic Structures and Mathematics before Numbers | 4-19 | sets, maps, power sets, Cartesian products, finite groups, Cayley graphs, actions, invariance/equivariance, tensor notation, einsum checks |
| 02 | `chapter-02-geometric-analytical-structures` | Geometric and Analytical Structures | 20-25 | norm balls, induced metrics, pseudometric/quasi-metric examples, Hausdorff distance, proximity graphs, projections, Gram-Schmidt, attention scaling |
| 03 | `chapter-03-vector-calculus` | Vector Calculus | 26-36 | Lipschitz/smoothness gallery, scalar/vector fields, gradients, Jacobians, integrals, divergence/flux, Laplacian, loss landscapes, backprop graph |
| 04 | `chapter-04-topology-differential-geometry` | Topological Foundations and Differential Geometry | 37-50 | open sets, continuity via preimages, homeomorphism/homotopy, Euler characteristic, geodesics, charts, tangent spaces, exp/log maps, gauges, manifold hypothesis |
| 05 | `chapter-05-functional-analysis` | Functional Analysis | 51-54 | Cauchy sequences, completeness gaps, Banach/Hilbert geometry, function bases, orthonormal reconstruction, operators, adjoints, functionals |
| 06 | `chapter-06-spectral-theory` | Spectral Theory | 55-64 | eigen-directions, self-adjoint spectra, Laplacian eigenfunctions, Fourier Gram matrices, SVD, Parseval, heat flow, graph Laplacian bridge |
| 07 | `chapter-07-graph-theory` | Graph Theory | 65-77 | graph anatomy, adjacency/degree matrices, graph distances, graph families, geometric graphs, homophily, permutations, homomorphisms, Laplacians, graph Fourier modes, message passing |

        ## Notebook Shape

        Each canonical notebook should contain title and source span, a standalone chapter question, a translation guide, a visual storyboard, a setup cell that discovers `BOOK_ROOT`, original concept sections, executable examples, generated artifacts displayed inline, an applied lab, sanity checks, and takeaways.

        ## Artifact Contract

        Store generated outputs under `artifacts/chapter-XX/{figures,html,plots,tables,checks,data}/`. Artifact filenames should name the concept, not the rendering technology. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

        ## Geometry Stack

        Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `pandas`, `networkx`, `shapely`, `trimesh`, `pyvista`, `skimage`, `opencv`, `torch`, `geomstats`, `ripser`, and the rest of the root geometry stack. This course should not require root dependency changes.

        ## Worker Boundaries

        Assign one worker to one canonical notebook, one helper module, or one script task. Chapter workers read their assigned source span, design or consume a visualization storyboard, and edit only their chapter folder, matching artifact subtree, and explicitly assigned helper module. Index workers own `00-book-index.ipynb` and chapter `00-index.ipynb` files. QC workers run audits and validation and report findings.

        ## Commands

        Run from `D:\Geometry`:

        ```powershell
        uv run python Mathematical-Foundations-of-Geometric-Deep-Learning/scripts/build_mfgdl_course_indexes.py
        uv run python -m compileall -q Mathematical-Foundations-of-Geometric-Deep-Learning/utils Mathematical-Foundations-of-Geometric-Deep-Learning/scripts
        uv run python Mathematical-Foundations-of-Geometric-Deep-Learning/scripts/audit_mfgdl_notebooks.py --min-words 1000 --min-code-cells 5
        uv run python Mathematical-Foundations-of-Geometric-Deep-Learning/scripts/audit_mfgdl_visuals.py
        uv run python Mathematical-Foundations-of-Geometric-Deep-Learning/scripts/validate_mfgdl_course.py --limit 4 --timeout 300
        uv run python Mathematical-Foundations-of-Geometric-Deep-Learning/scripts/validate_mfgdl_course.py --all --timeout 300
        git diff --check
        ```

        Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.
