# Agent Instructions: Computational Geometry in C Notebook Course

This folder is a standalone visualization-first notebook edition of *Computational Geometry in C*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `Computational Geometry in C.pdf`.

Extraction method: pdftotext table-of-contents extraction.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 1 | `chapter-01-polygon-triangulation` | 1-43 | Art gallery theorems, polygon area, segment intersection, ears, and triangulation implementation. |
| Chapter 2 | `chapter-02-polygon-partitioning` | 44-62 | Monotone partitioning, trapezoidalization, mountains, linear triangulation, and convex partitioning. |
| Chapter 3 | `chapter-03-convex-hulls-in-two-dimensions` | 63-100 | Convexity, extreme points, gift wrapping, QuickHull, Graham scan, lower bounds, and divide-and-conquer. |
| Chapter 4 | `chapter-04-convex-hulls-in-three-dimensions` | 101-154 | Polyhedra, 3D hull algorithms, boundary representations, randomized incremental hulls, and higher dimensions. |
| Chapter 5 | `chapter-05-voronoi-diagrams` | 155-192 | Voronoi cells, Delaunay triangulations, algorithms, medial axis, hull lifting, and arrangements. |
| Chapter 6 | `chapter-06-arrangements` | 193-219 | Line arrangements, combinatorics, incremental construction, duality, higher-order Voronoi diagrams, and applications. |
| Chapter 7 | `chapter-07-search-and-intersection` | 220-293 | Segment, triangle, polygon, polyhedron, convex polygon intersection, point location, and extremal queries. |
| Chapter 8 | `chapter-08-motion-planning` | 294-346 | Shortest paths, disk and polygon translation, ladder motion, robot arms, configuration spaces, and separability. |
| Chapter 9 | `chapter-09-sources` | 347-367 | Bibliographies, FAQs, textbooks, monographs, journals, and conference resources mapped as a computational geometry reading graph. |

Backmatter notes: chapter 9 is a source-map and reading-graph unit.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Computational-Geometry-in-C/scripts/build_cgc_course_indexes.py
uv run python -m compileall -q Computational-Geometry-in-C/utils Computational-Geometry-in-C/scripts
uv run python Computational-Geometry-in-C/scripts/audit_cgc_notebooks.py --min-words 900 --min-code-cells 5
uv run python Computational-Geometry-in-C/scripts/audit_cgc_visuals.py
uv run python Computational-Geometry-in-C/scripts/validate_cgc_course.py --limit 4 --timeout 300
git diff --check -- Computational-Geometry-in-C
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
