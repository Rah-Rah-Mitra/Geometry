# Agent Instructions: Knots, Links and Their Invariants Notebook Course

This folder is a standalone visualization-first notebook edition of *Knots, Links and Their Invariants*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

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

Source files: `Knots, Links and Their Invariants, An Elementary Course in Contemporary Knot Theory.pdf`.

Extraction method: pdftotext table-of-contents extraction.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Lecture 1 | `lecture-01-knots-and-links-reidemeister-moves` | 1-10 | Knot and link diagrams, Reidemeister moves, torus knots, invertibility, and chirality. |
| Lecture 2 | `lecture-02-the-conway-polynomial` | 11-20 | Axiomatic Conway polynomial, skein calculations, uniqueness, existence, chirality, orientation reversal, and multiplicativity. |
| Lecture 3 | `lecture-03-the-arithmetic-of-knots` | 21-28 | Boxed knots, connected sum, knot semigroup, prime decomposition, and unknotting remarks. |
| Lecture 4 | `lecture-04-some-simple-knot-invariants` | 29-38 | Stick number, crossing number, unknotting number, tricolorability, orientable surfaces, Seifert surfaces, and genus. |
| Lecture 5 | `lecture-05-the-kauffman-bracket` | 39-46 | States of knot diagrams, Kauffman bracket definition and properties, and invariance defects. |
| Lecture 6 | `lecture-06-the-jones-polynomial` | 47-56 | Jones polynomial via Kauffman bracket, axioms, multiplicativity, chirality, reversibility, and knot tables. |
| Lecture 7 | `lecture-07-braids` | 57-68 | Geometric braids, braid groups, group presentations, Artin presentation, closures, and undecidability digression. |
| Lecture 8 | `lecture-08-discriminants-and-finite-type-invariants` | 69-76 | Quadratic discriminants, degree of point relative to curve, inertia index, and Gauss linking number. |
| Lecture 9 | `lecture-09-vassiliev-invariants` | 77-86 | Singular knots, one-term and four-term relations, spaces of invariants, chord diagrams, and low-order examples. |
| Lecture 10 | `lecture-10-combinatorial-description-of-vassiliev-invariants` | 87-94 | Graded algebras, chord diagram algebra, Vassiliev-Kontsevich theorem, and comparison with other invariants. |
| Lecture 11 | `lecture-11-the-kontsevich-integrals` | 95-102 | Kontsevich integral for trefoil, configuration-space integral intuition, and finite type invariant encoding. |
| Lecture 12 | `lecture-12-other-important-topics` | 103-110 | Further knot-theoretic topics and relationships among invariants and constructions. |
| Lecture 13 | `lecture-13-a-brief-history-of-knot-theory` | 111-131 | Historical development, invariant milestones, and conceptual map of contemporary knot theory. |

Backmatter notes: bibliography 125-126; index 127-149.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Knots-Links-and-Their-Invariants-An-Elementary-Course-in-Contemporary-Knot-Theory/scripts/build_knots_course_indexes.py
uv run python -m compileall -q Knots-Links-and-Their-Invariants-An-Elementary-Course-in-Contemporary-Knot-Theory/utils Knots-Links-and-Their-Invariants-An-Elementary-Course-in-Contemporary-Knot-Theory/scripts
uv run python Knots-Links-and-Their-Invariants-An-Elementary-Course-in-Contemporary-Knot-Theory/scripts/audit_knots_notebooks.py --min-words 900 --min-code-cells 5
uv run python Knots-Links-and-Their-Invariants-An-Elementary-Course-in-Contemporary-Knot-Theory/scripts/audit_knots_visuals.py
uv run python Knots-Links-and-Their-Invariants-An-Elementary-Course-in-Contemporary-Knot-Theory/scripts/validate_knots_course.py --limit 4 --timeout 300
git diff --check -- Knots-Links-and-Their-Invariants-An-Elementary-Course-in-Contemporary-Knot-Theory
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
