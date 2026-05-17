# Agent Instructions: Algebraic Topology Notebook Course

This folder is a standalone visualization-first notebook edition of *Algebraic Topology*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `Algebraic Topology.pdf`.

Extraction method: pdftotext table-of-contents extraction.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 0 | `chapter-00-some-underlying-geometric-notions` | 1-20 | CW complexes, quotient spaces, deformation, homotopy, and geometric models for algebraic topology. |
| Chapter 1 | `chapter-01-the-fundamental-group` | 21-96 | Paths, homotopy, covering spaces, van Kampen, graphs, surfaces, and group presentations. |
| Chapter 2 | `chapter-02-homology` | 97-184 | Simplicial and singular homology, exact sequences, excision, cellular homology, and Euler characteristic. |
| Chapter 3 | `chapter-03-cohomology` | 185-336 | Cup products, Poincare duality, universal coefficients, Kunneth ideas, and characteristic computations. |
| Chapter 4 | `chapter-04-homotopy-theory` | 337-518 | Homotopy groups, fibrations, obstruction ideas, spectral sequence orientation, and stable phenomena. |
| Appendix A | `appendix-a-appendix` | 519-539 | Auxiliary algebraic and point-set tools used throughout the topology chapters. |

Backmatter notes: bibliography 533-538; index 539-553.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Algebraic-Topology/scripts/build_at_course_indexes.py
uv run python -m compileall -q Algebraic-Topology/utils Algebraic-Topology/scripts
uv run python Algebraic-Topology/scripts/audit_at_notebooks.py --min-words 900 --min-code-cells 5
uv run python Algebraic-Topology/scripts/audit_at_visuals.py
uv run python Algebraic-Topology/scripts/validate_at_course.py --limit 4 --timeout 300
git diff --check -- Algebraic-Topology
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
