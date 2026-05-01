# Agent Instructions: Geometry I Notebook Course

This folder is a standalone notebook edition of Marcel Berger's *Geometry I*.
Agents should treat this folder as the project root for this course. The
workspace root, `D:\Geometry`, owns the shared Python environment files.

## Repo-Local Skills

Use the repo-local Codex skills under `D:\Geometry\.codex\skills` for chapter
work:

- `geometry-visualization-planner`: read an assigned chapter or page span and
  produce a visual storyboard before authoring.
- `geometry-chapter-notebook-author`: author the standalone visual-first
  canonical notebook directly in its chapter folder.
- `geometry-notebook-qc`: review notebooks, artifacts, execution, visual
  relevance, stale paths, and dependency fit before handoff.

When using parallel workers, pass the relevant skill path and source span.
Assign one worker to one canonical notebook, one helper module, or one script
task. Chapter workers are not alone in the codebase; they must not revert other
workers' edits and should only touch their assigned chapter folder, matching
artifact subtree, and explicitly assigned helper.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, screenshots, page crops,
  or figures.
- A notebook must stand alone from the PDF: include motivation, definitions,
  worked examples, pitfalls, checks, and takeaways.
- Visualization is part of delivery, not decoration or a quota. Use diagrams,
  plots, widgets, symbolic checks, 3D views, proof-state diagrams, and
  computational experiments wherever they clarify the chapter.
- Keep helpers in `utils/`, outputs in `artifacts/`, and validation tools in
  `scripts/`.
- Every canonical notebook must execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per source
  folder.

## Source Map

The local PDF is `Geometry-I.pdf`. It is scanned/image-based, so the notebooks
use it only for orientation: title, chapter structure, page spans, definitions,
and exercise themes. They do not include extracted page images or copied prose.

The contained course material is Volume I only: Introduction, Chapter 0, and
Chapters 1-11. The table of contents lists Volume II as a cross-volume preview,
but those chapters are not part of this PDF-backed course folder.

Arabic printed pages map to physical PDF pages by:

```text
pdf_page = printed_page + 12
```

Front matter uses explicit spans in `scripts/geometry_i_inventory.py`.

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Translation guide from book concepts into computational language.
3. Route through the chapter.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Visual explanations and executable artifacts: diagrams, plots, 3D scenes,
   widgets, symbolic derivations, tables, or computational experiments as
   needed.
8. Applied lab or design exercise.
9. Sanity checks asserting core identities and artifact existence.
10. Takeaways.

## Visualization-First Contract

The standard is whether the notebook can teach the chapter without the textbook
open.

- Artifact filenames must name the concept, not the rendering technology.
- Prose near a visual must name what to inspect.
- Final sanity checks must assert artifact existence, nonzero size, and relevant
  numeric validation data.
- Repeated placeholder visuals are forbidden.
- Do not use textbook screenshots, PDF crops, or decorative images.
- For proof-heavy material, visualize proof state: assumptions, dependency
  graph, limiting process, deformation, orientation, or a small symbolic or
  numeric example.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed
libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`,
`ipywidgets`, `pandas`, `shapely`, `networkx`, `sympy`, `pyvista`, `trimesh`,
and the rest of the repo-local geometry stack. Document optional tools rather
than adding dependencies unless explicitly requested.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Geometry-I/scripts/build_geometry_i_course_indexes.py
uv run python -m compileall -q Geometry-I/utils Geometry-I/scripts
uv run pytest -q Geometry-I/scripts
uv run python Geometry-I/scripts/audit_geometry_i_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Geometry-I/scripts/audit_geometry_i_visuals.py
uv run python Geometry-I/scripts/validate_geometry_i_course.py --smoke --timeout 300
uv run python Geometry-I/scripts/validate_geometry_i_course.py --limit 6 --timeout 300
uv run python Geometry-I/scripts/validate_geometry_i_course.py --all --timeout 300
git diff --check
```

