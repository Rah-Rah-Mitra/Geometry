# Agent Instructions: Foundations of Differential Geometry Notebook Course

This folder is a standalone visualization-first notebook edition of *Foundations of Differential Geometry*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or figures.
- Use the source only for title, chapter structure, page spans, terminology, definitions, theorem orientation, and concept coverage.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualizations are part of the explanation.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.

## Source Map

Source files: `Foundations of Differential Geometry Volume I.pdf`, `Foundations of Differential Geometry Volume II.pdf`.

Extraction method: pdftotext table-of-contents extraction across two volumes.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 1 | `volume-01/chapter-01-differentiable-manifolds` | 1-62 | Pseudogroups, differentiable manifolds, tensor algebras, tensor fields, Lie groups, and fibre bundles. |
| Chapter 2 | `volume-01/chapter-02-theory-of-connections` | 63-112 | Principal fibre bundle connections, existence, parallelism, holonomy, curvature forms, reductions, invariant connections, and flatness. |
| Chapter 3 | `volume-01/chapter-03-linear-and-affine-connections` | 113-153 | Vector bundle connections, linear and affine connections, developments, curvature, torsion, geodesics, coordinates, normal coordinates, and holonomy. |
| Chapter 4 | `volume-01/chapter-04-riemannian-connections` | 154-197 | Riemannian metrics, Levi-Civita connections, normal coordinates, convex neighborhoods, completeness, holonomy, and de Rham decomposition. |
| Chapter 5 | `volume-01/chapter-05-curvature-and-space-forms` | 198-224 | Algebraic curvature, sectional curvature, spaces of constant curvature, flat affine and Riemannian connections. |
| Chapter 6 | `volume-01/chapter-06-transformations` | 225-266 | Affine transformations, infinitesimal affine transformations, isometries, Ricci tensor, extension of local isomorphisms, and equivalence problems. |
| Appendix 1 | `volume-01/appendix-1-ordinary-linear-differential-equations` | 267-268 | Linear ODE foundations for connections, parallel transport, and local existence arguments. |
| Appendix 2 | `volume-01/appendix-2-connected-locally-compact-metric-spaces-are-separable` | 269-271 | Separability lemma supporting manifold countability and local compactness arguments. |
| Appendix 3 | `volume-01/appendix-3-partition-of-unity` | 272-274 | Partition of unity construction and its role in globalizing local differential-geometric data. |
| Appendix 4 | `volume-01/appendix-4-arcwise-connected-subgroups-of-lie-groups` | 275-276 | Lie subgroup connectivity lemma used in holonomy and transformation theory. |
| Appendix 5 | `volume-01/appendix-5-irreducible-subgroups-of-o-n` | 277-280 | Irreducible orthogonal representations and holonomy decomposition examples. |
| Appendix 6 | `volume-01/appendix-6-green-s-theorem` | 281-283 | Green theorem scaffold for integration and curvature identities. |
| Appendix 7 | `volume-01/appendix-7-factorization-lemma` | 284-304 | Local factorization arguments for maps, bundles, and equivalence problems. |
| Chapter 7 | `volume-02/chapter-07-submanifolds` | 1-62 | Frame bundles, Gauss maps, second fundamental form, Gauss-Codazzi equations, hypersurfaces, rigidity, and totally geodesic submanifolds. |
| Chapter 8 | `volume-02/chapter-08-variations-of-the-length-integral` | 63-113 | Jacobi fields, conjugate points, comparison theorem, second variation, Morse index theorem, cut loci, nonpositive curvature, and fixed points. |
| Chapter 9 | `volume-02/chapter-09-complex-manifolds` | 114-185 | Almost complex manifolds, Hermitian and Kahler metrics, local coordinate formulas, examples, holomorphic curvature, and Hermitian connections. |
| Chapter 10 | `volume-02/chapter-10-homogeneous-spaces` | 186-221 | Invariant affine connections, reductive homogeneous spaces, invariant metrics, holonomy, de Rham decomposition, and invariant almost complex structures. |
| Chapter 11 | `volume-02/chapter-11-symmetric-spaces` | 222-292 | Affine and Riemannian symmetric spaces, canonical connections, totally geodesic submanifolds, symmetric Lie algebras, duality, examples, and classification outline. |
| Chapter 12 | `volume-02/chapter-12-characteristic-classes` | 293-320 | Weil homomorphism, invariant polynomials, Chern classes, Pontrjagin classes, Euler classes, and Chern-Weil formulas. |
| Appendix 8 | `volume-02/appendix-8-integrable-real-analytic-almost-complex-structures` | 321-324 | Real analytic integrability support for almost complex structures. |
| Appendix 9 | `volume-02/appendix-9-definitions-and-facts-on-lie-algebras` | 325-345 | Lie algebra background supporting homogeneous and symmetric space chapters. |

Backmatter notes: two-volume course; notes and combined index source-mapped only.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Foundations-of-Differential-Geometry/scripts/build_fdg_course_indexes.py
uv run python -m compileall -q Foundations-of-Differential-Geometry/utils Foundations-of-Differential-Geometry/scripts
uv run python Foundations-of-Differential-Geometry/scripts/audit_fdg_notebooks.py --min-words 900 --min-code-cells 5
uv run python Foundations-of-Differential-Geometry/scripts/audit_fdg_visuals.py
uv run python Foundations-of-Differential-Geometry/scripts/validate_fdg_course.py --limit 4 --timeout 300
git diff --check -- Foundations-of-Differential-Geometry
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
