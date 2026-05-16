# Agent Instructions: Hodge Theory and Complex Algebraic Geometry

This folder is a standalone visualization-first notebook course built from the
two local Voisin PDFs:

- `Hodge Theory and Complex Algebraic Geometry I.pdf`
- `Hodge Theory and Complex Algebraic Geometry II.pdf`

Treat this directory as the course root. The workspace root owns the shared
Python environment; do not edit sibling course folders while working here.

## Repo-Local Skills

Use the repo-local geometry skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before designing or extending chapter visuals.
- `geometry-chapter-notebook-author` when authoring a canonical chapter notebook.
- `geometry-notebook-qc` before handoff or after broad notebook changes.

## Non-Negotiables

- Write original teaching prose, diagrams, code, and explanations.
- Do not copy textbook passages, long exercise text, screenshots, PDF crops, or
  textbook figures.
- Every canonical notebook must be useful without opening the PDFs.
- Keep source references to page spans and terminology only.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, scripts in
  `scripts/`, and inventory/index files in `inventory/` or `indexes/`.
- Preserve one canonical notebook per chapter folder.
- Generated paths in notebooks must be relative or course-local.
- Every visual must have an inspection target and a computational or structural
  check where practical.

## Source Map

For both local PDFs, numbered body pages satisfy:

```text
pdf_page = printed_page + 12
```

The full chapter source map is stored in:

- `inventory/source-map.md`
- `inventory/source-map.csv`
- `inventory/source-map.json`
- `indexes/chapters.json`

## Course Structure

- `volume-01-foundations`: Volume I, compact Kahler foundations.
  - `part-00-orientation`
  - `part-01-preliminaries`
  - `part-02-hodge-decomposition`
  - `part-03-variations-of-hodge-structure`
  - `part-04-cycles-and-cycle-classes`
- `volume-02-applications`: Volume II, topology, variations, and algebraic cycles.
  - `part-00-orientation`
  - `part-01-topology-of-algebraic-varieties`
  - `part-02-variations-of-hodge-structure`
  - `part-03-algebraic-cycles`

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Copyright-safe source note.
3. Chapter goal and route.
4. Source inventory.
5. Translation guide from the chapter concepts into computational language.
6. Library routing.
7. Setup cell that discovers `BOOK_ROOT`.
8. Concept-specific generated artifacts displayed near explanatory prose.
9. Symbolic, numeric, or structural checks.
10. Applied lab.
11. Final artifact and invariant sanity checks.
12. Takeaways.

## Visualization Policy

Use the installed geometry stack intentionally. For this course, common routes
include:

- Matplotlib for Hodge diamonds, spectral sequence pages, operator boards,
  filtration ladders, cycle diagrams, and proof dependency views.
- NetworkX for source, proof, correspondence, and incidence graphs.
- NumPy and SymPy for finite linear algebra checks, filtrations, commutators,
  monodromy pairings, toy Laplacians, and Fourier transforms.
- Plotly or HTML artifacts only when parameter motion or inspection is central.

Do not add decorative visuals. A visual must teach a concept, construction,
invariant, proof move, or failure mode.

## Commands

Run from the workspace root:

```powershell
uv run python Hodge-Theory-and-Complex-Algebraic-Geometry/scripts/build_hodge_course.py
uv run python Hodge-Theory-and-Complex-Algebraic-Geometry/scripts/build_hodge_indexes.py
uv run python -m compileall -q Hodge-Theory-and-Complex-Algebraic-Geometry/utils Hodge-Theory-and-Complex-Algebraic-Geometry/scripts
uv run python Hodge-Theory-and-Complex-Algebraic-Geometry/scripts/audit_hodge_notebooks.py
uv run python Hodge-Theory-and-Complex-Algebraic-Geometry/scripts/audit_hodge_visuals.py
uv run python Hodge-Theory-and-Complex-Algebraic-Geometry/scripts/validate_hodge_course.py --limit 3 --timeout 240
uv run python Hodge-Theory-and-Complex-Algebraic-Geometry/scripts/validate_hodge_course.py --all --timeout 240
git diff --check -- Hodge-Theory-and-Complex-Algebraic-Geometry
```

## Worker Boundaries

Chapter workers should edit only their assigned chapter folder, the matching
`artifacts/volume-XX/<chapter-id>/` subtree, and explicitly assigned helpers.
Shared utility or validation changes should be made by a utility worker.

`scripts/build_hodge_course.py` is a bootstrap and regeneration tool. Do not use
it to overwrite an improved chapter notebook unless the task explicitly asks for
course-wide regeneration.

