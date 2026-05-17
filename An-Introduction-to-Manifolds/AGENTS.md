# Agent Instructions: An Introduction to Manifolds Notebook Course

This folder is a standalone visualization-first notebook edition of *An Introduction to Manifolds*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `An Introduction to Manifolds.pdf`.

Extraction method: pdftotext table-of-contents extraction.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 1 | `chapter-01-euclidean-spaces` | 3-47 | Smooth functions, derivations, tangent vectors, exterior algebra, and differential forms on Euclidean space. |
| Chapter 2 | `chapter-02-manifolds` | 48-85 | Topological and smooth manifolds, atlases, smooth maps, quotients, and projective examples. |
| Chapter 3 | `chapter-03-the-tangent-space` | 86-163 | Tangent spaces, differentials, submanifolds, rank theorems, tangent bundles, partitions of unity, vector fields, flows, Lie brackets, and pushforwards. |
| Chapter 4 | `chapter-04-lie-groups-and-lie-algebras` | 164-189 | Matrix Lie groups, Lie subgroups, matrix exponential, determinant differential, left-invariant vector fields, Lie algebras, brackets, and Lie algebra homomorphisms. |
| Chapter 5 | `chapter-05-differential-forms` | 190-235 | Forms on manifolds, cotangent bundle, pullbacks, wedge products, invariant forms, exterior derivative, restriction, Lie derivative, and interior multiplication. |
| Chapter 6 | `chapter-06-integration` | 236-273 | Orientations, manifolds with boundary, boundary orientation, integration of forms, Stokes theorem, line integrals, and Green's theorem. |
| Chapter 7 | `chapter-07-de-rham-theory` | 274-316 | De Rham cohomology, exact and Mayer-Vietoris sequences, homotopy invariance, cohomology computations, degree-style invariants, and cochain homotopies. |

Backmatter notes: brief introduction 1-2; appendices A-E 317-359; selected solutions 361-385; list of notations 387-393; references 395-396; index 397-430. Canonical notebooks cover the seven main chapters.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python An-Introduction-to-Manifolds/scripts/build_aim_course_indexes.py
uv run python -m compileall -q An-Introduction-to-Manifolds/utils An-Introduction-to-Manifolds/scripts
uv run python An-Introduction-to-Manifolds/scripts/audit_aim_notebooks.py --min-words 900 --min-code-cells 5
uv run python An-Introduction-to-Manifolds/scripts/audit_aim_visuals.py
uv run python An-Introduction-to-Manifolds/scripts/validate_aim_course.py --limit 4 --timeout 300
git diff --check -- An-Introduction-to-Manifolds
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
