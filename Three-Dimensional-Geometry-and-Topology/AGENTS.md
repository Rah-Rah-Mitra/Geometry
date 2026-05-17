# Agent Instructions: Three-Dimensional Geometry and Topology Notebook Course

This folder is a standalone visualization-first notebook edition of *Three-Dimensional Geometry and Topology*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `Three-Dimensional Geometry and Topology, Volume 1.pdf`.

Extraction method: pdftotext table-of-contents extraction.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 1 | `chapter-01-what-is-a-manifold` | 3-42 | Polygons and surfaces, hyperbolic surfaces, totality of surfaces, and examples of three-manifolds. |
| Chapter 2 | `chapter-02-hyperbolic-geometry-and-its-friends` | 43-108 | Negatively curved surfaces, inversive models, hyperboloid and Klein models, hyperbolic computations, isometries, complex coordinates, and three-sphere geometry. |
| Chapter 3 | `chapter-03-geometric-manifolds` | 109-208 | Geometric structures, triangulations, gluings, developing maps, completeness, discrete groups, bundles, connections, contact structures, model geometries, PL manifolds, and smoothings. |
| Chapter 4 | `chapter-04-the-structure-of-discrete-groups` | 209-229 | Small generators, Euclidean manifolds, crystallographic groups, elliptic three-manifolds, thick-thin decomposition, Teichmuller space, and fibered geometries. |

Backmatter notes: glossary 289-294; bibliography 295-300; index 301-322.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Three-Dimensional-Geometry-and-Topology/scripts/build_tdgt_course_indexes.py
uv run python -m compileall -q Three-Dimensional-Geometry-and-Topology/utils Three-Dimensional-Geometry-and-Topology/scripts
uv run python Three-Dimensional-Geometry-and-Topology/scripts/audit_tdgt_notebooks.py --min-words 900 --min-code-cells 5
uv run python Three-Dimensional-Geometry-and-Topology/scripts/audit_tdgt_visuals.py
uv run python Three-Dimensional-Geometry-and-Topology/scripts/validate_tdgt_course.py --limit 4 --timeout 300
git diff --check -- Three-Dimensional-Geometry-and-Topology
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
