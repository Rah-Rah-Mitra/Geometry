# Agent Instructions: Metric Spaces of Non-Positive Curvature Notebook Course

This folder is a standalone visualization-first notebook edition of Martin R. Bridson and Andre Haefliger's *Metric Spaces of Non-Positive Curvature*. Treat this book folder as the course root. The workspace root owns the shared `uv` environment, `pyproject.toml`, and `uv.lock`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or figures.
- The PDF is source orientation only. A reader should not need the PDF open.
- Visualization is part of delivery, not decoration or a quota.
- Keep helpers in `utils/`, outputs in `artifacts/`, inventories in `inventory/`, and validation tools in `scripts/`.
- Every canonical notebook should execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per content folder.

## Source Map

The local PDF has 664 physical pages. For the main printed book body, printed page 1 aligns with physical PDF page 20, so the working conversion is `pdf_page = printed_page + 19`. The source map in `inventory/source-map.md` and `inventory/source-map.json` records the chapter and local appendix spans used by this course.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/msnpc_inventory.py
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/build_msnpc_course_indexes.py
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/build_msnpc_artifacts.py
uv run python -m compileall -q Metric-Spaces-of-Non-Positive-Curvature/utils Metric-Spaces-of-Non-Positive-Curvature/scripts
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/audit_msnpc_notebooks.py --min-words 550 --min-code-cells 3
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/audit_msnpc_visuals.py
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/validate_msnpc_course.py --smoke --timeout 240
git diff --check -- Metric-Spaces-of-Non-Positive-Curvature
```

Run full validation with:

```powershell
uv run python Metric-Spaces-of-Non-Positive-Curvature/scripts/validate_msnpc_course.py --all --timeout 240
```

## Visualization Library Policy

Every major visualization must name the concept it teaches, the representation, the library route, an inspection target, and a check or invariant. Use Matplotlib for durable metric diagrams, NetworkX for Cayley graphs, scwols, groupoids, and dependency graphs, standalone HTML for small interactive inspection cards, and SymPy or numeric helpers for reproducible checks.
