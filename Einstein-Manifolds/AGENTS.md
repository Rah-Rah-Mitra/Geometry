# Agent Instructions: Einstein Manifolds Notebook Course

This folder is a standalone visualization-first notebook edition of *Einstein Manifolds*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `Einstein Manifolds.pdf`.

Extraction method: rendered image-page TOC inspection; text extraction is image-only.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 0 | `chapter-00-introduction` | 1-19 | Definitions, motivation, existence, examples, moduli, Ricci curvature feel, and current problems. |
| Chapter 1 | `chapter-01-basic-material` | 20-65 | Connections, pseudo-Riemannian manifolds, Killing fields, Einstein manifolds, curvature decompositions, Laplacians, conformal change, and variations. |
| Chapter 2 | `chapter-02-basic-material-continued-kahler-manifolds` | 66-93 | Complex manifolds, Hermitian and Kahler metrics, Ricci form, Chern classes, Hodge theory, and Calabi-Futaki theorem. |
| Chapter 3 | `chapter-03-relativity` | 94-115 | Einstein field equation, tidal stresses, curvature normal forms, Schwarzschild metric, orbits, light bending, Kruskal extension, and singularity theorems. |
| Chapter 4 | `chapter-04-riemannian-functionals` | 116-136 | Total scalar curvature, constant scalar curvature metrics, scalar curvature map, quadratic functionals, and variational properties. |
| Chapter 5 | `chapter-05-ricci-curvature-as-a-partial-differential-equation` | 137-153 | Pointwise solvability, local obstructions, local Einstein metric construction, regularity, analyticity, and uniqueness and nonexistence. |
| Chapter 6 | `chapter-06-einstein-manifolds-and-topology` | 154-176 | Dimension two, three and four cases, fundamental group, spinorial obstruction, and Cheeger-Gromoll theorem. |
| Chapter 7 | `chapter-07-homogeneous-riemannian-manifolds` | 177-207 | Homogeneous metrics, curvature, homogeneous Einstein examples, symmetric spaces, and standard homogeneous models. |
| Chapter 8 | `chapter-08-compact-homogeneous-kahler-manifolds` | 208-234 | Adjoint orbits, canonical complex structures, invariant Ricci forms, KKS symplectic forms, Kahler metrics, and examples. |
| Chapter 9 | `chapter-09-riemannian-submersions` | 235-277 | ONeill tensors, curvature formulas, canonical variation, homogeneous Einstein applications, warped products, and examples. |
| Chapter 10 | `chapter-10-holonomy-groups` | 278-317 | Definitions, parallel tensors, products, curvature, symmetric spaces, Berger-style structure, nonsimply connected cases, and Lorentzian manifolds. |
| Chapter 11 | `chapter-11-kahler-einstein-metrics-and-the-calabi-conjecture` | 318-339 | Kahler-Einstein metrics, Aubin-Calabi-Yau theorems, positive first Chern class, and extremal metrics. |
| Chapter 12 | `chapter-12-the-moduli-space-of-einstein-structures` | 340-368 | Surfaces, flat manifolds, infinitesimal deformations, formal integrability, premoduli spaces, Einstein constants, rigidity, and K3 examples. |
| Chapter 13 | `chapter-13-self-duality` | 369-395 | Self-dual four-manifolds, half-conformally flat manifolds, Penrose construction, reverse Penrose construction, and Einstein applications. |
| Chapter 14 | `chapter-14-quaternion-kahler-manifolds` | 396-421 | Hyperkahler manifolds, quaternion-Kahler structures, twistor spaces, symmetric examples, and applications. |
| Chapter 15 | `chapter-15-a-report-on-the-non-compact-case` | 422-431 | Nonhomogeneous Einstein metrics, bundle constructions, and bounded domains of holomorphy. |
| Chapter 16 | `chapter-16-generalizations-of-the-einstein-condition` | 432-455 | Natural linear conditions on covariant derivatives of Ricci tensors, Codazzi tensors, harmonic Weyl tensor, and harmonic curvature. |
| Appendix A | `appendix-a-sobolev-spaces-and-elliptic-operators` | 456-470 | Holder spaces, Sobolev spaces, embedding theorems, elliptic operators, adjoints, symbols, estimates, and regularity. |
| Addendum | `addendum-addendum` | 471-491 | Later examples: infinitely many Einstein constants, G2 and Spin(7) holonomy metrics, and inhomogeneous Kahler-Einstein metrics. |

Backmatter notes: index approx 477-528.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Einstein-Manifolds/scripts/build_em_course_indexes.py
uv run python -m compileall -q Einstein-Manifolds/utils Einstein-Manifolds/scripts
uv run python Einstein-Manifolds/scripts/audit_em_notebooks.py --min-words 900 --min-code-cells 5
uv run python Einstein-Manifolds/scripts/audit_em_visuals.py
uv run python Einstein-Manifolds/scripts/validate_em_course.py --limit 4 --timeout 300
git diff --check -- Einstein-Manifolds
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
