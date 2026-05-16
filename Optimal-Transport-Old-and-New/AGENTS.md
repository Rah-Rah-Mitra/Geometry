# Agent Instructions: Optimal Transport, Old and New Notebook Course

This folder is a standalone visualization-first notebook edition of Cedric Villani's *Optimal Transport: Old and New*. Treat this folder as the course root. The shared Python environment lives at the workspace root `D:\Geometry`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills` for course work:

- `geometry-visualization-planner` for storyboards and artifact choices.
- `geometry-chapter-notebook-author` for canonical notebook authoring.
- `geometry-notebook-qc` for notebook, artifact, and execution review.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, printed tables, screenshots, page crops, or figures.
- The notebooks must stand alone without the PDF open.
- Visualization is part of the argument, not decoration.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and maintenance scripts in `scripts/`.
- Keep generated paths relative or book-local.
- Preserve one canonical teaching notebook per introduction/chapter/conclusions unit plus a local `00-index.ipynb`.
- Course scripts may build indexes, audit notebooks, validate execution, and regenerate small reproducible artifacts. Do not use scripts to replace chapter-specific human revision with generic filler.

## Source Map

The local PDF is `Optimal Transport Old and New.pdf`. `pdfinfo` reports 997 physical PDF pages. The main text printed page number `p` corresponds to physical PDF page `p + 22`. The source map in `source-map.md` and `scripts/otonn_inventory.py` records the spans used for every canonical unit.

The canonical units are:

- Introduction: printed pp. 1-4; PDF pp. 23-26.
- Chapters 1-30: printed pp. 5-902; PDF pp. 27-924.
- Conclusions and open problems: printed pp. 903-914; PDF pp. 925-936.

References, lists, index, and the final cost-function table are indexed as back matter but are not separate teaching notebooks in this course build.

## Notebook Shape

Each canonical notebook should include:

1. Title and source span.
2. A chapter question and translation guide from the book's terms to computational language.
3. A route through the unit.
4. A setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with nearby visual explanations.
6. Executable examples using book-local utilities.
7. Visual artifacts saved under `artifacts/` and displayed inline.
8. A lab or design exercise.
9. Sanity checks asserting source-map consistency, mass conservation, artifact existence, and the unit's numeric/geometric invariant.
10. Takeaways.

## Geometry Stack

Use the installed geometry stack intentionally. For optimal transport and metric geometry, prefer:

- POT (`ot`) for exact discrete plans, Wasserstein costs, barycenters, and coupling checks.
- GeomLoss for CPU-safe Sinkhorn demonstrations when differentiable or entropic transport is the lesson.
- Matplotlib and Plotly for durable static figures and standalone interactive views.
- NetworkX for proof dependency graphs, chapter maps, and implication diagrams.
- SymPy for exact algebraic checks when a determinant, Hessian, Jacobian, or convexity identity is the point.
- NumPy, SciPy, pandas, and scikit-learn for small reproducible numerical experiments.

Document external-only tools rather than importing them silently.

## Worker Boundaries

Workers for this course should edit only this folder unless explicitly assigned shared repo work. If another worker has changed a file, preserve their work and revise around it.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python "Optimal-Transport-Old-and-New/scripts/build_otonn_course_indexes.py"
uv run python "Optimal-Transport-Old-and-New/scripts/generate_otonn_artifacts.py"
uv run python -m compileall -q "Optimal-Transport-Old-and-New/utils" "Optimal-Transport-Old-and-New/scripts"
uv run python "Optimal-Transport-Old-and-New/scripts/audit_otonn_notebooks.py" --min-words 650 --min-code-cells 5
uv run python "Optimal-Transport-Old-and-New/scripts/audit_otonn_visuals.py"
uv run python "Optimal-Transport-Old-and-New/scripts/audit_otonn_artifacts.py"
uv run python "Optimal-Transport-Old-and-New/scripts/validate_otonn_course.py" --limit 6 --timeout 240
git diff --check -- "Optimal-Transport-Old-and-New"
```

Use full validation with `--all` when shared utilities, setup cells, or many notebooks changed.

## Visual Justification Rule

Every major visualization must name:

1. the concept it teaches,
2. why the representation was chosen,
3. what the learner should inspect,
4. the artifact path,
5. a check or invariant where practical.

Decorative visuals are not acceptable.
