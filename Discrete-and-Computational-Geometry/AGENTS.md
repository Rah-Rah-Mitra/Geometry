# Agent Instructions: Discrete and Computational Geometry Notebook Course

This folder is a standalone visualization-first notebook edition of *Discrete and Computational Geometry*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `Discrete and Computational Geometry, 2nd Edition.pdf`.

Extraction method: pdftotext table-of-contents extraction.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 1 | `chapter-01-polygons` | 1-37 | Polygonal regions, triangulations, art galleries, area, and guards. |
| Chapter 2 | `chapter-02-convex-hulls` | 38-64 | Planar and spatial convex hulls, algorithms, support lines, and hull complexity. |
| Chapter 3 | `chapter-03-triangulations` | 65-106 | Triangulations, flips, Delaunay structures, and mesh quality. |
| Chapter 4 | `chapter-04-voronoi-diagrams` | 107-135 | Voronoi cells, Delaunay duality, nearest neighbors, and geometric partitions. |
| Chapter 5 | `chapter-05-shape-recovery` | 136-169 | Medial axes, alpha shapes, reconstruction, and sampling conditions. |
| Chapter 6 | `chapter-06-polygonal-chains` | 170-198 | Linkages, chains, configuration spaces, unfolding, and motion constraints. |
| Chapter 7 | `chapter-07-polyhedra` | 199-252 | Polyhedral surfaces, Euler characteristic, unfolding, rigidity, and three-dimensional constructions. |
| Appendix A | `appendix-a-computational-complexity` | 253-258 | Asymptotic analysis, reductions, algorithm classes, and geometric algorithm complexity. |

Backmatter notes: index 259-281.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Discrete-and-Computational-Geometry/scripts/build_dcg_course_indexes.py
uv run python -m compileall -q Discrete-and-Computational-Geometry/utils Discrete-and-Computational-Geometry/scripts
uv run python Discrete-and-Computational-Geometry/scripts/audit_dcg_notebooks.py --min-words 900 --min-code-cells 5
uv run python Discrete-and-Computational-Geometry/scripts/audit_dcg_visuals.py
uv run python Discrete-and-Computational-Geometry/scripts/validate_dcg_course.py --limit 4 --timeout 300
git diff --check -- Discrete-and-Computational-Geometry
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
