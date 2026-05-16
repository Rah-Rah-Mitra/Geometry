# Agent Instructions: Introduction to Symplectic Topology Notebook Course

This folder is a standalone notebook edition of McDuff and Salamon's *Introduction
to Symplectic Topology*, third edition. Treat this folder as the project root for
this course. The workspace root still owns the shared Python environment files.

## Repo-Local Skills

Use the repo-local geometry skills in `D:\Geometry\.codex\skills` for all course
work:

- `geometry-visualization-planner`: plan chapter-specific visual storyboards.
- `geometry-chapter-notebook-author`: author canonical teaching notebooks.
- `geometry-notebook-qc`: audit standalone teaching quality, artifacts, execution,
  and source-map coverage.

Workers should read this file, the relevant source-map entry, and the assigned
notebook before editing. Use the PDF only for orientation, terminology, structure,
and concept coverage.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or
  figure crops.
- Keep edits inside this course folder unless the user explicitly assigns shared
  workspace work.
- A canonical notebook must be useful without the PDF open: include motivation,
  definitions, examples, pitfalls, computational checks, and takeaways.
- Visuals must teach a symplectic concept, construction, invariant, proof move, or
  failure mode. Decorative images are not acceptable.
- Keep helpers in `utils/`, validation and audit tools in `scripts/`, generated
  outputs in `artifacts/`, and source inventory in `inventory/`.
- Generated notebook paths must be relative or book-local.
- Preserve one canonical teaching notebook per chapter or appendix folder.

## Source Map

The local source is:

`Introduction to Symplectic Topology Third Edition.pdf`

For the body matter, printed pages map to PDF pages by:

`pdf_page = printed_page + 13`

The course follows the book structure:

- Introduction: printed pages 1-8.
- Part I, Foundations: Chapters 1-4.
- Part II, Symplectic Manifolds: Chapters 5-7.
- Part III, Symplectomorphisms: Chapters 8-10.
- Part IV, Symplectic Invariants: Chapters 11-14.
- Appendix A: Smooth maps.

The canonical machine-readable source map lives in `inventory/source-map.json`,
with a readable companion in `inventory/source-map.md`.

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Standalone goal and translation guide from book concepts to computational
   language.
3. Chapter route with the relevant definitions, constructions, and proof moves.
4. A setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations, examples, and caveats.
6. Visual explanations linked to generated artifacts.
7. Executable checks for the symplectic form, Hamiltonian flow, moment map,
   fibration, capacity, variational, or smooth-extension invariants as appropriate.
8. A short lab or reader-facing experiment.
9. Final sanity checks asserting artifact existence and invariant truth.
10. Takeaways.

## Visualization-First Contract

Every major artifact must have:

- the concept it teaches,
- why the representation was chosen,
- a learner inspection target,
- a nearby prose explanation,
- a numerical, symbolic, or structural invariant when practical.

Priority visual/check families for this course:

- symplectic form and standard matrix checks,
- Hamiltonian vector fields and energy-preserving flow,
- moment maps, convexity, and reduced spaces,
- symplectic fibration connection/holonomy pictures,
- blow-up and construction diagrams,
- area-preserving twist maps and fixed-point diagnostics,
- generating-function and variational action landscapes,
- capacity/nonsqueezing and Hofer-distance comparisons,
- existence/uniqueness and open-problem dependency graphs,
- appendix smoothing/extension checks.

## Geometry Stack

Prefer installed libraries before adding dependencies:

- `numpy`, `scipy`, `matplotlib`, `plotly`, `pandas`, `networkx`
- `sympy` for exact matrix/form checks
- `nbformat`, `nbclient` for notebook generation and validation
- `Pillow` for artifact pixel checks

Use heavier 3D, mesh, TDA, or optimal-transport tools only when a chapter needs
them. Document optional tools instead of silently importing them.

## Commands

Run from the workspace root:

```powershell
uv run python Introduction-to-Symplectic-Topology/scripts/inventory_symplectic_source.py --write
uv run python Introduction-to-Symplectic-Topology/scripts/generate_symplectic_artifacts.py --all
uv run python Introduction-to-Symplectic-Topology/scripts/build_symplectic_course_indexes.py
uv run python -m compileall -q Introduction-to-Symplectic-Topology/utils Introduction-to-Symplectic-Topology/scripts
uv run pytest -q Introduction-to-Symplectic-Topology/scripts
uv run python Introduction-to-Symplectic-Topology/scripts/audit_symplectic_notebooks.py --min-words 650 --min-code-cells 5
uv run python Introduction-to-Symplectic-Topology/scripts/audit_symplectic_visuals.py
uv run python Introduction-to-Symplectic-Topology/scripts/validate_symplectic_course.py --limit 6 --timeout 180
uv run python Introduction-to-Symplectic-Topology/scripts/validate_symplectic_course.py --all --timeout 240
git diff --check -- Introduction-to-Symplectic-Topology
```

Full notebook validation is intentionally separate from the smoke command because
the complete course has many notebooks.
