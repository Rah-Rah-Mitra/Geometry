# Agent Instructions: Introduction to Smooth Manifolds Notebook Course

This folder is a standalone visualization-first notebook edition of *Introduction to Smooth Manifolds*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `Introduction to Smooth Manifolds.pdf`.

Extraction method: pdftotext table-of-contents extraction.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 1 | `chapter-01-smooth-manifolds` | 1-31 | Topological manifolds, smooth structures, examples, and manifolds with boundary. |
| Chapter 2 | `chapter-02-smooth-maps` | 32-49 | Smooth functions, smooth maps, partitions of unity, and local-to-global construction. |
| Chapter 3 | `chapter-03-tangent-vectors` | 50-76 | Tangent vectors, differentials, coordinates, tangent bundle, curve velocities, and functorial views. |
| Chapter 4 | `chapter-04-submersions-immersions-and-embeddings` | 77-97 | Constant rank maps, embeddings, submersions, smooth covering maps, and local normal forms. |
| Chapter 5 | `chapter-05-submanifolds` | 98-124 | Embedded and immersed submanifolds, map restriction, tangent spaces, and boundary submanifolds. |
| Chapter 6 | `chapter-06-sard-s-theorem` | 125-149 | Measure zero, Sard theorem, Whitney embedding and approximation, and transversality. |
| Chapter 7 | `chapter-07-lie-groups` | 150-173 | Basic Lie groups, homomorphisms, subgroups, actions, equivariant maps, and examples. |
| Chapter 8 | `chapter-08-vector-fields` | 174-204 | Vector fields, smooth maps, Lie brackets, and Lie algebra of a Lie group. |
| Chapter 9 | `chapter-09-integral-curves-and-flows` | 205-248 | Integral curves, flows, flowouts, manifolds with boundary, Lie derivatives, commuting fields, time-dependent fields, and first-order PDEs. |
| Chapter 10 | `chapter-10-vector-bundles` | 249-271 | Vector bundles, sections, bundle homomorphisms, subbundles, and fiber bundles. |
| Chapter 11 | `chapter-11-the-cotangent-bundle` | 272-303 | Covectors, differential of a function, pullbacks, line integrals, and conservative covector fields. |
| Chapter 12 | `chapter-12-tensors` | 304-326 | Multilinear algebra, symmetric and alternating tensors, and tensor fields on manifolds. |
| Chapter 13 | `chapter-13-riemannian-metrics` | 327-348 | Riemannian manifolds, distance function, tangent-cotangent isomorphism, and pseudo-Riemannian metrics. |
| Chapter 14 | `chapter-14-differential-forms` | 349-376 | Alternating tensors, forms on manifolds, exterior derivatives, and examples. |
| Chapter 15 | `chapter-15-orientations` | 377-399 | Orientations of vector spaces and manifolds, Riemannian volume form, and covering maps. |
| Chapter 16 | `chapter-16-integration-on-manifolds` | 400-439 | Volume measurement, integration of forms, Stokes theorem, corners, Riemannian integration, and densities. |
| Chapter 17 | `chapter-17-de-rham-cohomology` | 440-466 | de Rham groups, homotopy invariance, Mayer-Vietoris, degree theory, and proof scaffolding. |
| Chapter 18 | `chapter-18-the-de-rham-theorem` | 467-489 | Singular homology and cohomology, smooth singular homology, and de Rham theorem. |
| Chapter 19 | `chapter-19-distributions-and-foliations` | 490-514 | Distributions, involutivity, Frobenius theorem, foliations, Lie subgroups, and overdetermined PDEs. |
| Chapter 20 | `chapter-20-the-exponential-map` | 515-539 | One-parameter subgroups, exponential map, closed subgroup theorem, infinitesimal generators, Lie correspondence, and normal subgroups. |
| Chapter 21 | `chapter-21-quotient-manifolds` | 540-563 | Group action quotients, covering manifolds, homogeneous spaces, and Lie-theory applications. |
| Chapter 22 | `chapter-22-symplectic-manifolds` | 564-595 | Symplectic tensors, symplectic structures, Darboux theorem, Hamiltonian vector fields, contact structures, and nonlinear first-order PDEs. |
| Appendix A | `appendix-a-review-of-topology` | 596-616 | Topological spaces, subspaces, products, quotients, connectedness, compactness, homotopy, fundamental group, and coverings. |
| Appendix B | `appendix-b-review-of-linear-algebra` | 617-641 | Vector spaces, linear maps, determinant, inner products, norms, products, and direct sums. |
| Appendix C | `appendix-c-review-of-calculus` | 642-662 | Multivariable calculus, derivatives, inverse function theorem, and local analytic tools. |
| Appendix D | `appendix-d-review-of-differential-equations` | 663-683 | ODE existence, uniqueness, flows, and differential equation background for smooth manifolds. |

Backmatter notes: references 675-680; index 681-726.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Introduction-to-Smooth-Manifolds/scripts/build_ism_course_indexes.py
uv run python -m compileall -q Introduction-to-Smooth-Manifolds/utils Introduction-to-Smooth-Manifolds/scripts
uv run python Introduction-to-Smooth-Manifolds/scripts/audit_ism_notebooks.py --min-words 900 --min-code-cells 5
uv run python Introduction-to-Smooth-Manifolds/scripts/audit_ism_visuals.py
uv run python Introduction-to-Smooth-Manifolds/scripts/validate_ism_course.py --limit 4 --timeout 300
git diff --check -- Introduction-to-Smooth-Manifolds
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
