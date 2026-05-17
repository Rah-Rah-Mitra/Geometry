# Agent Instructions: Introduction to Riemannian Manifolds Notebook Course

This folder is a standalone visualization-first notebook edition of *Introduction to Riemannian Manifolds*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `Introduction to Riemannian Manifolds, Second Edition.pdf`.

Extraction method: pdftotext table-of-contents extraction.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 1 | `chapter-01-what-is-curvature` | 1-8 | Informal curvature motivation, classification theorems, local-to-global theorems, surfaces, and higher-dimensional curvature intuition. |
| Chapter 2 | `chapter-02-riemannian-metrics` | 9-54 | Metric definitions, constructions, distances, pseudo-Riemannian metrics, and generalizations. |
| Chapter 3 | `chapter-03-model-riemannian-manifolds` | 55-84 | Symmetries, Euclidean spaces, spheres, hyperbolic spaces, invariant Lie group metrics, homogeneous spaces, and pseudo-Riemannian models. |
| Chapter 4 | `chapter-04-connections` | 85-114 | Differentiating vector fields, vector bundle connections, covariant derivatives, geodesics, parallel transport, and pullback connections. |
| Chapter 5 | `chapter-05-the-levi-civita-connection` | 115-150 | Tangential connection, abstract Levi-Civita connection, exponential map, normal neighborhoods, Fermi coordinates, model-space geodesics, and geometries. |
| Chapter 6 | `chapter-06-geodesics-and-distance` | 151-192 | Minimizing curves, normal neighborhoods, completeness, distance functions, and semigeodesic coordinates. |
| Chapter 7 | `chapter-07-curvature` | 193-224 | Curvature tensor, flat manifolds, symmetries, Ricci identities, Ricci and scalar curvature, Weyl tensor, and conformal change. |
| Chapter 8 | `chapter-08-riemannian-submanifolds` | 225-262 | Second fundamental form, hypersurfaces, Euclidean hypersurfaces, sectional curvature, and submanifold calculations. |
| Chapter 9 | `chapter-09-the-gauss-bonnet-theorem` | 263-282 | Plane geometry, Gauss-Bonnet formula, compact surface theorem, and curvature-topology relation. |
| Chapter 10 | `chapter-10-jacobi-fields` | 283-318 | Jacobi equation, computations, conjugate points, second variation, cut points, and local symmetric spaces. |
| Chapter 11 | `chapter-11-comparison-theory` | 319-344 | Jacobi fields, Hessians, Riccati equations, sectional and Ricci curvature comparisons, and volume and diameter bounds. |
| Chapter 12 | `chapter-12-curvature-and-topology` | 345-370 | Constant curvature, nonpositive curvature, positive curvature, Killing-Hopf, Cartan-Hadamard, Myers, Synge, and topology consequences. |
| Appendix A | `appendix-a-review-of-smooth-manifolds` | 371-390 | Topological preliminaries, smooth maps, tangent vectors, submanifolds, vector bundles, vector fields, and covering maps. |
| Appendix B | `appendix-b-review-of-tensors` | 391-406 | Tensors, tensor bundles, differential forms, integration, and densities. |
| Appendix C | `appendix-c-review-of-lie-groups` | 407-427 | Definitions, Lie algebras, and group actions on manifolds. |

Backmatter notes: references 415-418; notation index 419-422; subject index 423-447.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Introduction-to-Riemannian-Manifolds/scripts/build_irm_course_indexes.py
uv run python -m compileall -q Introduction-to-Riemannian-Manifolds/utils Introduction-to-Riemannian-Manifolds/scripts
uv run python Introduction-to-Riemannian-Manifolds/scripts/audit_irm_notebooks.py --min-words 900 --min-code-cells 5
uv run python Introduction-to-Riemannian-Manifolds/scripts/audit_irm_visuals.py
uv run python Introduction-to-Riemannian-Manifolds/scripts/validate_irm_course.py --limit 4 --timeout 300
git diff --check -- Introduction-to-Riemannian-Manifolds
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
