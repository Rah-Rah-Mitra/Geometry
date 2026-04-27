# Agent Instructions: Visual Differential Geometry and Forms Notebook Course

This folder is a standalone notebook edition of *Visual Differential Geometry and Forms*.
Agents should treat this folder as the project root for this course. The workspace root
still owns the shared Python environment files.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, or page screenshots.
- A notebook must be useful without opening the PDF: include motivation, definitions,
  worked examples, pitfalls, checks, and takeaways.
- Keep helpers in `utils/`, outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve the one-canonical-notebook-per-folder structure.

## Source Map

Body printed pages map to PDF pages by `pdf_page = printed_page + 29`.
The course follows the book's five-act structure:

- Prologue: visual meaning versus empty calculation.
- Act I: Chapters 1-3, the nature of space.
- Act II: Chapters 4-7, the metric.
- Act III: Chapters 8-20, curvature.
- Act IV: Chapters 21-31, parallel transport.
- Act V: Chapters 32-39, forms.

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Translation guide from book concepts into computational language.
3. Route through the chapter.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Static or interactive artifacts.
8. Applied lab or design exercise.
9. Sanity checks asserting core identities and artifact existence.
10. Takeaways.

## Worker Boundaries

Assign one worker to one canonical notebook, one helper module, or one script task.
Chapter workers edit only their chapter folder, matching artifact subtree, and any
explicitly assigned chapter helper. Shared utility changes belong to utility workers.
The index/QC worker owns `00-book-index.ipynb`, part indexes, audits, and validation.

## Commands

Run from the workspace root:

```powershell
uv run python Visual-Differential-Geometry-and-Forms/scripts/build_vdgf_course_indexes.py
uv run python -m compileall -q Visual-Differential-Geometry-and-Forms/utils Visual-Differential-Geometry-and-Forms/scripts
uv run pytest -q Visual-Differential-Geometry-and-Forms/scripts
uv run python Visual-Differential-Geometry-and-Forms/scripts/audit_vdgf_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Visual-Differential-Geometry-and-Forms/scripts/validate_vdgf_course.py --limit 8 --timeout 300
uv run python Visual-Differential-Geometry-and-Forms/scripts/validate_vdgf_course.py --all --timeout 300
git diff --check
```
