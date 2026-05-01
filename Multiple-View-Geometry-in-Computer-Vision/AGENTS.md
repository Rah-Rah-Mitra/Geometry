# Agent Instructions: Multiple View Geometry in Computer Vision Notebook Course

This folder is a standalone visualization-first notebook edition of *Multiple View Geometry in Computer Vision, Second Edition* by Richard Hartley and Andrew Zisserman. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills` for course work:

- `geometry-visualization-planner` for chapter storyboards.
- `geometry-chapter-notebook-author` for authoring canonical notebooks.
- `geometry-notebook-qc` for standalone, artifact, and execution review.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or figures.
- The notebooks must stand alone without the PDF open.
- Visualization is part of the teaching argument, not decoration or a fixed quota.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook per chapter or appendix folder plus a local `00-index.ipynb`.

## Source Map

The PDF has 673 physical pages. Printed page 1 starts on PDF page 19, so body and appendix spans use:

```text
pdf_page = printed_page + 18
```

The course follows the book structure: a root introductory chapter, Part 0 background, Part I single-view geometry, Part II two-view geometry, Part III three-view geometry, Part IV N-view geometry, and Part V appendices. Bibliography and printed index pages are not authored as canonical notebooks.

## Notebook Shape

Each canonical notebook should include:

1. Title and source span.
2. Translation guide from book concepts into computational language.
3. Route through the chapter.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Visual artifacts saved under `artifacts/` and displayed inline.
8. Applied lab or design exercise.
9. Sanity checks asserting core identities and artifact existence.
10. Takeaways.

## Geometry Stack

Use the shared `uv` environment at `D:\Geometry`. Prefer installed packages before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `networkx`, `opencv-contrib-python` as `cv2`, `scikit-image`, `pandas`, `pyvista`, `trimesh`, and `PIL`.

## Worker Boundaries

Assign one worker to one canonical notebook or one shared helper/script task. Chapter workers should read their assigned source span, consume or create a visualization storyboard, and edit only the assigned chapter folder, its artifact subtree, and any explicitly assigned helper. Workers are not alone in the codebase; do not revert other workers' edits.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python "Multiple-View-Geometry-in-Computer-Vision/scripts/build_mvg_course_indexes.py"
uv run python -m compileall -q "Multiple-View-Geometry-in-Computer-Vision/utils" "Multiple-View-Geometry-in-Computer-Vision/scripts"
uv run pytest -q "Multiple-View-Geometry-in-Computer-Vision/scripts"
uv run python "Multiple-View-Geometry-in-Computer-Vision/scripts/audit_mvg_notebooks.py" --min-words 1200 --min-code-cells 5
uv run python "Multiple-View-Geometry-in-Computer-Vision/scripts/audit_mvg_visuals.py"
uv run python "Multiple-View-Geometry-in-Computer-Vision/scripts/validate_mvg_course.py" --smoke --timeout 300
uv run python "Multiple-View-Geometry-in-Computer-Vision/scripts/validate_mvg_course.py" --limit 8 --timeout 300
git diff --check
```
