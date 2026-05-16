# Agent Instructions: Convex Analysis Notebook Course

This folder is a standalone visualization-first notebook edition of Rockafellar's *Convex Analysis*. Treat `Convex-Analysis` as the course root. The workspace root still owns the shared Python environment.

## Repo-Local Skills

Use the repo-local geometry skills under `D:\Geometry\.codex\skills` for section work:

- `geometry-visualization-planner`: inspect an assigned section/page span and plan visual, computational, and proof-state treatment before authoring.
- `geometry-chapter-notebook-author`: author the standalone visual-first canonical notebook directly in the assigned section folder.
- `geometry-notebook-qc`: review notebooks, artifacts, helpers, execution, stale paths, and anti-generic risks before handoff.

When parallel workers are active, touch only the assigned section folder, matching `artifacts/` subtree, and explicitly assigned helper or script. Do not revert other workers' changes.

## Non-Negotiables

- Write original teaching prose, code, diagrams, derivations, and checks.
- Do not copy textbook passages, exercise text, screenshots, page crops, figures, or page layouts.
- Use the local PDF only for structure, terminology, and source-span orientation.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per numbered section.
- Keep sections grouped under their part folders.
- Store generated outputs under the course-local `artifacts/` subtree.
- Keep helpers in `utils/`, inventory and source maps in `inventory/`, and validation tools in `scripts/`.
- Generated paths in notebooks must be relative or book-local.
- Every canonical notebook should execute cleanly with `nbclient`.

## Source Map

The course follows the 39 numbered sections in the PDF contents. Body printed pages map to PDF pages by:

```text
pdf_page = printed_page + 18
```

The canonical source map is `inventory/source_map.json` with a readable companion in `inventory/source_map.md`.

## Notebook Shape

Each canonical section notebook should contain:

1. Title and source span.
2. Section goal and translation guide from Rockafellar's language to computational language.
3. Library routing and visual inspection targets.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original conceptual prose around convex geometry, epigraphs, subgradients, duality, saddle-functions, or convex algebra as appropriate.
6. Synthetic visual artifacts and proof/dependency maps generated from course-local helpers or visible section code.
7. A small learner lab or parameter experiment.
8. Final sanity checks asserting source-map alignment, artifact existence, nonzero artifact size, and the section invariant.
9. Takeaways.

## Visualization-First Contract

Visuals must teach a concept, construction, invariant, proof move, or failure mode. Decorative images are not acceptable.

- Prose near every visual must say what to inspect.
- Artifact filenames must name the concept rather than the renderer.
- Proof-heavy sections should expose assumptions, dependency graphs, limiting processes, certificates, or symbolic checks.
- Matplotlib is appropriate for durable 2D convex geometry; use richer libraries only when they add inspection value.
- Epigraph, subgradient, separation, conjugacy, duality, KKT, saddle, minimax, and convex-process visuals should include numerical or symbolic checks.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python "Convex-Analysis/scripts/build_convex_analysis_indexes.py"
uv run python -m compileall -q "Convex-Analysis/utils" "Convex-Analysis/scripts"
uv run pytest -q "Convex-Analysis/scripts/test_convex_analysis_core.py"
uv run python "Convex-Analysis/scripts/audit_convex_analysis_notebooks.py" --min-words 650 --min-code-cells 5
uv run python "Convex-Analysis/scripts/validate_convex_analysis_course.py" --smoke --timeout 300
uv run python "Convex-Analysis/scripts/validate_convex_analysis_course.py" --all --timeout 300
uv run python "Convex-Analysis/scripts/audit_convex_analysis_visuals.py"
git diff --check
```

For quick worker checks, run compileall, the core pytest file, the notebook audit, and a smoke validation over the assigned section before broader validation.

