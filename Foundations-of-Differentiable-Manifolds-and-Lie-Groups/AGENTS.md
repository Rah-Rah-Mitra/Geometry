# Agent Instructions: Foundations of Differentiable Manifolds and Lie Groups Notebook Course

This folder is a standalone visualization-first notebook edition of *Foundations of Differentiable Manifolds and Lie Groups*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `Foundations of Differentiable Manifolds and Lie Groups.pdf`.

Extraction method: pdftotext table-of-contents extraction.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 1 | `chapter-01-manifolds` | 1-53 | Differentiable manifolds, tangent vectors, differentials, submanifolds, inverse and implicit functions, vector fields, distributions, and Frobenius theorem. |
| Chapter 2 | `chapter-02-tensors-and-differential-forms` | 54-81 | Tensor and exterior algebras, tensor fields, differential forms, Lie derivatives, and differential ideals. |
| Chapter 3 | `chapter-03-lie-groups` | 82-137 | Lie groups, Lie algebras, homomorphisms, subgroups, coverings, exponential map, adjoint representation, and homogeneous manifolds. |
| Chapter 4 | `chapter-04-integration-on-manifolds` | 138-162 | Orientation, integration on manifolds, de Rham cohomology, and Stokes-style constructions. |
| Chapter 5 | `chapter-05-sheaves-cohomology-and-the-de-rham-theorem` | 163-219 | Sheaves, cochain complexes, axiomatic sheaf cohomology, classical cohomology theories, de Rham theorem, products, and supports. |
| Chapter 6 | `chapter-06-the-hodge-theorem` | 220-259 | Laplace-Beltrami operator, Hodge theorem, calculus estimates, elliptic operators, periodic reduction, ellipticity, and exercises before the bibliography. |

Backmatter notes: bibliography 260-263; notation index 264-266; index 267-283.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Foundations-of-Differentiable-Manifolds-and-Lie-Groups/scripts/build_warner_course_indexes.py
uv run python -m compileall -q Foundations-of-Differentiable-Manifolds-and-Lie-Groups/utils Foundations-of-Differentiable-Manifolds-and-Lie-Groups/scripts
uv run python Foundations-of-Differentiable-Manifolds-and-Lie-Groups/scripts/audit_warner_notebooks.py --min-words 900 --min-code-cells 5
uv run python Foundations-of-Differentiable-Manifolds-and-Lie-Groups/scripts/audit_warner_visuals.py
uv run python Foundations-of-Differentiable-Manifolds-and-Lie-Groups/scripts/validate_warner_course.py --limit 4 --timeout 300
git diff --check -- Foundations-of-Differentiable-Manifolds-and-Lie-Groups
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
