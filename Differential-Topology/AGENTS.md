# Agent Instructions: Differential Topology Notebook Course

This folder is a standalone visualization-first notebook edition of *Differential Topology*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `Differential Topology.pdf`.

Extraction method: pdftotext table-of-contents extraction.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 1 | `chapter-01-manifolds-and-smooth-maps` | 1-56 | Definitions, derivatives, inverse function theorem, immersions, submersions, transversality, homotopy, Sard theorem, and embeddings. |
| Chapter 2 | `chapter-02-transversality-and-intersection` | 57-93 | Manifolds with boundary, one-manifolds, mod 2 intersection, winding numbers, Jordan-Brouwer, and Borsuk-Ulam. |
| Chapter 3 | `chapter-03-oriented-intersection-theory` | 94-150 | Orientation, oriented intersection number, Lefschetz fixed point theorem, vector fields, Poincare-Hopf, Hopf degree, and Euler characteristic. |
| Chapter 4 | `chapter-04-integration-on-manifolds` | 151-201 | Exterior algebra, differential forms, integration, exterior derivative, form cohomology, Stokes theorem, mappings, and Gauss-Bonnet. |
| Appendix 1 | `appendix-1-measure-zero-and-sard-s-theorem` | 202-207 | Measure-zero sets, Sard theorem proof scaffolding, and critical value diagnostics. |
| Appendix 2 | `appendix-2-classification-of-compact-one-manifolds` | 208-211 | Compact one-manifold classification via interval and circle models. |

Backmatter notes: bibliography 212-216; index 217-236.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Differential-Topology/scripts/build_dt_course_indexes.py
uv run python -m compileall -q Differential-Topology/utils Differential-Topology/scripts
uv run python Differential-Topology/scripts/audit_dt_notebooks.py --min-words 900 --min-code-cells 5
uv run python Differential-Topology/scripts/audit_dt_visuals.py
uv run python Differential-Topology/scripts/validate_dt_course.py --limit 4 --timeout 300
git diff --check -- Differential-Topology
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
