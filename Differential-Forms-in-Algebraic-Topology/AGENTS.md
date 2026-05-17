# Agent Instructions: Differential Forms in Algebraic Topology Notebook Course

This folder is a standalone visualization-first notebook edition of *Differential Forms in Algebraic Topology*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `Differential Forms in Algebraic Topology.pdf`.

Extraction method: pdftotext table-of-contents extraction.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 1 | `chapter-01-de-rham-theory` | 13-88 | de Rham complexes, Mayer-Vietoris, orientation, integration, Poincare lemmas, Thom class, and duality. |
| Chapter 2 | `chapter-02-the-cech-de-rham-complex` | 89-153 | Good covers, double complexes, Cech cohomology, sphere bundles, Euler classes, and tic-tac-toe arguments. |
| Chapter 3 | `chapter-03-spectral-sequences-and-applications` | 154-265 | Filtered complexes, spectral sequence pages, transgression, Gysin sequences, and cohomological applications. |
| Chapter 4 | `chapter-04-characteristic-classes` | 266-286 | Chern-Weil intuition, Stiefel-Whitney, Chern, Pontrjagin, Euler classes, and classifying examples. |

Backmatter notes: index 319-342.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Differential-Forms-in-Algebraic-Topology/scripts/build_dfat_course_indexes.py
uv run python -m compileall -q Differential-Forms-in-Algebraic-Topology/utils Differential-Forms-in-Algebraic-Topology/scripts
uv run python Differential-Forms-in-Algebraic-Topology/scripts/audit_dfat_notebooks.py --min-words 900 --min-code-cells 5
uv run python Differential-Forms-in-Algebraic-Topology/scripts/audit_dfat_visuals.py
uv run python Differential-Forms-in-Algebraic-Topology/scripts/validate_dfat_course.py --limit 4 --timeout 300
git diff --check -- Differential-Forms-in-Algebraic-Topology
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
