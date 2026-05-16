# Agent Instructions: J-holomorphic Curves and Symplectic Topology

        This folder is a standalone visualization-first notebook edition of Dusa McDuff and Dietmar Salamon's *J-holomorphic Curves and Symplectic Topology*, second edition. Treat this folder as the course root. The workspace root owns the shared `uv` environment, `pyproject.toml`, and `uv.lock`.

        ## Repo-Local Skills

        Use the repo-local skills under `D:\Geometry\.codex\skills`:

        - `geometry-visualization-planner` before planning or revising a chapter storyboard.
        - `geometry-chapter-notebook-author` when authoring a canonical notebook.
        - `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

        ## Non-Negotiables

        - Write original teaching prose, examples, code, diagrams, and checks.
        - Do not copy textbook passages, long exercise text, screenshots, page crops, or solution text.
        - The PDF is source orientation only. A reader should not need the PDF open.
        - Visualization is part of delivery, not decoration or a quota.
        - Keep helpers in `utils/`, outputs in `artifacts/`, and validation tools in `scripts/`.
        - Every canonical notebook should execute with `nbclient`.
        - Generated paths in notebooks must be relative or book-local.
        - Preserve one canonical teaching notebook plus `00-index.ipynb` per content folder.

        ## Course Structure

        ```text
        J-Holomorphic-Curves-and-Symplectic-Topology/
          00-book-index.ipynb
          AGENTS.md
          SOURCE_MAP.md
          artifacts/
          scripts/
          utils/
          chapter-01-introduction/
          ...
          chapter-12-floer-homology/
          appendix-a-fredholm-theory/
          ...
          appendix-e-singularities-and-intersections/
        ```

        ## Source Map

        Printed page 1 starts at physical PDF page 16. For main matter, `PDF page = printed page + 15`.

        | Unit | Folder | Printed Pages | PDF Pages | Focus |
        | --- | --- | ---: | ---: | --- |
        | Chapter 1 | `chapter-01-introduction` | 1-16 | 16-31 | Symplectic manifolds, tame almost complex structures, moduli spaces, evaluation maps, and the Gromov-Witten counting pipeline. |
| Chapter 2 | `chapter-02-j-holomorphic-curves` | 17-38 | 32-53 | Almost complex structures, nonlinear Cauchy-Riemann equations, unique continuation, critical points, somewhere injective curves, and adjunction. |
| Chapter 3 | `chapter-03-moduli-spaces-and-transversality` | 39-74 | 54-89 | Moduli spaces of simple curves, transversality, regularity criteria, point constraints, and the implicit function theorem. |
| Chapter 4 | `chapter-04-compactness` | 75-114 | 90-129 | Energy, bubbling, mean value and isoperimetric inequalities, removal of singularities, convergence modulo bubbling, and connected bubble trees. |
| Chapter 5 | `chapter-05-stable-maps` | 115-152 | 130-167 | Stable maps, Gromov convergence, compactness for stable maps, uniqueness of limits, and the Gromov topology. |
| Chapter 6 | `chapter-06-moduli-spaces-of-stable-maps` | 153-200 | 168-215 | Simple stable maps, transversality, evaluation maps, semipositivity, pseudocycles, Gromov-Witten pseudocycles, and graph pseudocycles. |
| Chapter 7 | `chapter-07-gromov-witten-invariants` | 201-256 | 216-271 | Counting pseudoholomorphic spheres, variations on the definition, graph counts, rational curves in projective spaces, and Gromov-Witten axioms. |
| Chapter 8 | `chapter-08-hamiltonian-perturbations` | 257-294 | 272-309 | Trivial bundles, locally Hamiltonian fibrations, pseudoholomorphic sections, fiber spheres, section pseudocycles, and section counts. |
| Chapter 9 | `chapter-09-applications-in-symplectic-topology` | 295-368 | 310-383 | Hamiltonian periodic orbits, Lagrangian embeddings, nonsqueezing, symplectic four-manifolds, symplectomorphism groups, Hofer geometry, and distinguishing symplectic structures. |
| Chapter 10 | `chapter-10-gluing` | 369-416 | 384-431 | Gluing theorem, connected sums of curves, weighted norms, cutoff functions, construction and derivative of the gluing map, surjectivity, splitting axiom, and a revisited theorem. |
| Chapter 11 | `chapter-11-quantum-cohomology` | 417-486 | 432-501 | Small quantum cohomology, Gromov-Witten potential, examples, Seidel representation, and Frobenius manifolds. |
| Chapter 12 | `chapter-12-floer-homology` | 487-530 | 502-545 | Floer cochain complex, ring structure, Poincare duality, spectral invariants, Seidel representation, Donaldson's quantum category, and vortex equations. |
| Appendix A | `appendix-a-fredholm-theory` | 531-548 | 546-563 | Fredholm operators, determinant line bundles, implicit function theorem, finite-dimensional reduction, and Sard-Smale theorem. |
| Appendix B | `appendix-b-elliptic-regularity` | 549-578 | 564-593 | Sobolev spaces, Calderon-Zygmund inequality, regularity for the Laplace operator, and elliptic bootstrapping. |
| Appendix C | `appendix-c-riemann-roch-theorem` | 579-618 | 594-633 | Cauchy-Riemann operators, elliptic estimates, boundary Maslov index, proof of Riemann-Roch, Riemann mapping, nonsmooth bundles, and almost complex structures. |
| Appendix D | `appendix-d-stable-curves-of-genus-zero` | 619-652 | 634-667 | Mobius transformations, cross ratios, trees, labels, splittings, stable curves, Grothendieck-Knudsen space, Gromov topology, cohomology, and examples. |
| Appendix E | `appendix-e-singularities-and-intersections` | 653-694 | 668-709 | Main intersection results, positivity of intersections, integrability, Hartman-Wintner theorem, local behavior, contact between branches, and singularities of J-holomorphic curves. |

        ## Back Matter Inventory

        - Bibliography: printed pp. 695-710; PDF pp. 710-725.
- List of Symbols: printed pp. 711-714; PDF pp. 726-729.
- Index: printed pp. 715-729; PDF pp. 730-744.

        ## Notebook Shape

        Each canonical notebook should contain a title and source span, a standalone chapter question, a computational translation guide, setup cell, original concept sections, generated visual artifacts displayed inline, proof or invariant scaffolds, an applied lab, sanity checks, and takeaways.

        ## Artifact Contract

        Store generated outputs under:

        ```text
        artifacts/chapter-01/
        ...
        artifacts/chapter-12/
        artifacts/appendix-a/
        ...
        artifacts/appendix-e/
        ```

        Use subfolders such as `figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

        ## Geometry Stack

        Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `pandas`, `networkx`, `shapely`, `trimesh`, `pyvista`, `ripser`, `gudhi`, and the rest of the root geometry stack. This course currently needs no dependency additions.

        ## Worker Boundaries

        Other workers may edit other course folders. Do not touch anything outside this book folder unless explicitly assigned. Chapter workers may edit only their chapter folder, matching artifact subtree, and explicitly assigned helper module. Index workers own `00-book-index.ipynb` and `00-index.ipynb` files. QC workers run audits and validation and report findings.

        ## Commands

        Run from `D:\Geometry`:

        ```powershell
        uv run python J-Holomorphic-Curves-and-Symplectic-Topology/scripts/build_jhcst_course_indexes.py
        uv run python -m compileall -q J-Holomorphic-Curves-and-Symplectic-Topology/utils J-Holomorphic-Curves-and-Symplectic-Topology/scripts
        uv run python J-Holomorphic-Curves-and-Symplectic-Topology/scripts/audit_jhcst_notebooks.py --min-words 650 --min-code-cells 5
        uv run python J-Holomorphic-Curves-and-Symplectic-Topology/scripts/validate_jhcst_course.py --limit 4 --timeout 240
        uv run python J-Holomorphic-Curves-and-Symplectic-Topology/scripts/audit_jhcst_visuals.py
        git diff --check -- J-Holomorphic-Curves-and-Symplectic-Topology
        ```

        Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

        ## Visualization Library Policy

        Use the installed geometry stack intentionally. For this course, Matplotlib and NetworkX cover durable proof diagrams, local residual plots, dimension ledgers, and finite algebra checks. Use Plotly, PyVista, TDA, or other specialized libraries only when a chapter-specific visual genuinely needs them.

        Every major visualization must have the concept it teaches, the reason this representation was chosen, an inspection target for the learner, nearby prose explanation, and a check, invariant, or sanity test where practical.

        ## Notebook-First Rule

        A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not mass-populate chapter notebooks with generic teaching cells.
