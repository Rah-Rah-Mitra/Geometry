# Agent Instructions: Differential Geometry, Lie Groups, and Symmetric Spaces Notebook Course

This folder is a standalone visualization-first notebook edition of *Differential Geometry, Lie Groups, and Symmetric Spaces*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `Differential Geometry, Lie Groups, and Symmetric Spaces.pdf`.

Extraction method: pdftotext table-of-contents extraction.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 1 | `chapter-01-elementary-differential-geometry` | 2-97 | Manifolds, tensor fields, mappings, affine connections, parallelism, exponential maps, structural equations, and curvature. |
| Chapter 2 | `chapter-02-lie-groups-and-lie-algebras` | 98-154 | Exponential map, Lie subgroups, transformation groups, coset spaces, adjoint group, semisimple groups, and invariant forms. |
| Chapter 3 | `chapter-03-structure-of-semisimple-lie-algebras` | 155-197 | Lie and Engel theorems, Cartan subalgebras, roots, real forms, Cartan decompositions, and classical examples. |
| Chapter 4 | `chapter-04-symmetric-spaces` | 198-228 | Affine locally symmetric spaces, isometry groups, globally symmetric spaces, curvature, compact Lie groups, and Lie triple systems. |
| Chapter 5 | `chapter-05-decomposition-of-symmetric-spaces` | 229-251 | Orthogonal symmetric Lie algebras, duality, sectional curvature, semisimple isometry groups, and rank. |
| Chapter 6 | `chapter-06-symmetric-spaces-of-the-noncompact-type` | 252-280 | Semisimple group decompositions, maximal compact subgroups, Iwasawa decomposition, nilpotent groups, and global decompositions. |
| Chapter 7 | `chapter-07-symmetric-spaces-of-the-compact-type` | 281-351 | Weyl groups, conjugate points, singular sets, compact groups, affine Weyl groups, and rank-one geometry. |
| Chapter 8 | `chapter-08-hermitian-symmetric-spaces` | 352-400 | Almost complex manifolds, Ricci curvature, bounded domains, Hermitian symmetric spaces, and Cartan-Harish-Chandra representation. |
| Chapter 9 | `chapter-09-structure-of-semisimple-lie-groups` | 401-437 | Cartan, Iwasawa, Bruhat, rank-one, SU(2,1), Cartan subalgebras, automorphisms, multiplicities, and Jordan decompositions. |
| Chapter 10 | `chapter-10-classification-of-simple-lie-algebras-and-symmetric` | 438-458 | Classical groups, root systems, Dynkin diagrams, finite-order automorphisms, real forms, and symmetric-space classification. |

Backmatter notes: solutions 538-585; bibliography 605-634; index 641-675.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Differential-Geometry-Lie-Groups-and-Symmetric-Spaces/scripts/build_helgason_course_indexes.py
uv run python -m compileall -q Differential-Geometry-Lie-Groups-and-Symmetric-Spaces/utils Differential-Geometry-Lie-Groups-and-Symmetric-Spaces/scripts
uv run python Differential-Geometry-Lie-Groups-and-Symmetric-Spaces/scripts/audit_helgason_notebooks.py --min-words 900 --min-code-cells 5
uv run python Differential-Geometry-Lie-Groups-and-Symmetric-Spaces/scripts/audit_helgason_visuals.py
uv run python Differential-Geometry-Lie-Groups-and-Symmetric-Spaces/scripts/validate_helgason_course.py --limit 4 --timeout 300
git diff --check -- Differential-Geometry-Lie-Groups-and-Symmetric-Spaces
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
