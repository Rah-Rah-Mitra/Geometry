# Agent Instructions: Lectures on Discrete Geometry Notebook Course

This folder is a standalone visualization-first notebook edition of *Lectures on Discrete Geometry*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `Lectures on Discrete Geometry.pdf`.

Extraction method: pdftotext table-of-contents extraction.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 1 | `chapter-01-convexity` | 1-16 | Affine subspaces, convex sets, separation, Radon lemma, Helly theorem, centerpoint theorem, and ham sandwich theorem. |
| Chapter 2 | `chapter-02-lattices-and-minkowski-s-theorem` | 17-28 | Minkowski theorem, general lattices, and number-theoretic applications. |
| Chapter 3 | `chapter-03-convex-independent-subsets` | 29-40 | Erdos-Szekeres theorem, Horton sets, and geometric Ramsey examples. |
| Chapter 4 | `chapter-04-incidence-problems` | 41-76 | Incidence formulations, lower bounds, unit distances, crossing numbers, cuttings, and point-line incidences. |
| Chapter 5 | `chapter-05-convex-polytopes` | 77-124 | Geometric duality, H-polytopes, V-polytopes, faces, cyclic polytopes, upper bound theorem, Gale transform, and Voronoi diagrams. |
| Chapter 6 | `chapter-06-number-of-faces-in-arrangements` | 125-164 | Arrangements, complexity, levels, zones, cuttings, and probabilistic bounds. |
| Chapter 7 | `chapter-07-lower-envelopes` | 165-194 | Davenport-Schinzel sequences, lower envelope complexity, triangles in space, curves, and algebraic surface patches. |
| Chapter 8 | `chapter-08-intersection-patterns-of-convex-sets` | 195-206 | Fractional Helly theorem, colorful Caratheodory theorem, and Tverberg theorem. |
| Chapter 9 | `chapter-09-geometric-selection-theorems` | 207-230 | Selection lemmas, order types, same-type lemma, hypergraph regularity, and positive-fraction selection. |
| Chapter 10 | `chapter-10-transversals-and-epsilon-nets` | 231-264 | Transversals, matchings, epsilon nets, VC-dimension, weak epsilon nets, and Hadwiger-Debrunner problems. |
| Chapter 11 | `chapter-11-attempts-to-count-k-sets` | 265-288 | k-sets, halving edges, Lovasz lemma, upper bounds, and planar improvements. |
| Chapter 12 | `chapter-12-two-applications-of-high-dimensional-polytopes` | 289-310 | Weak perfect graph conjecture, Brunn-Minkowski inequality, and sorting partially ordered sets. |
| Chapter 13 | `chapter-13-volumes-in-high-dimension` | 311-328 | High-dimensional volume, nets, hardness of approximation, large-volume polytopes, and ellipsoid approximation. |
| Chapter 14 | `chapter-14-measure-concentration-and-almost-spherical-sections` | 329-354 | Measure concentration, isoperimetric inequalities, Lipschitz functions, symmetric polytopes, and Dvoretzky theorem. |
| Chapter 15 | `chapter-15-embedding-finite-metric-spaces-into-normed-spaces` | 355-375 | Approximate embeddings, Johnson-Lindenstrauss flattening, lower bounds, Hamming cube, expanders, and l_infinity and Euclidean embeddings. |

Backmatter notes: informal summary 401-408; hints 409-416; bibliography 417-458; index 459-496.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Lectures-on-Discrete-Geometry/scripts/build_ldg_course_indexes.py
uv run python -m compileall -q Lectures-on-Discrete-Geometry/utils Lectures-on-Discrete-Geometry/scripts
uv run python Lectures-on-Discrete-Geometry/scripts/audit_ldg_notebooks.py --min-words 900 --min-code-cells 5
uv run python Lectures-on-Discrete-Geometry/scripts/audit_ldg_visuals.py
uv run python Lectures-on-Discrete-Geometry/scripts/validate_ldg_course.py --limit 4 --timeout 300
git diff --check -- Lectures-on-Discrete-Geometry
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
