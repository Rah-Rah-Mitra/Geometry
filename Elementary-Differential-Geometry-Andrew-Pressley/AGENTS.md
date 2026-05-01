# Agent Instructions: Pressley Elementary Differential Geometry Notebook Course

This folder is a standalone visualization-first notebook edition of Andrew
Pressley's *Elementary Differential Geometry, Second Edition*. Treat this book
folder as the course root:

```text
Elementary-Differential-Geometry-Andrew-Pressley/
  00-book-index.ipynb
  AGENTS.md
  artifacts/
  scripts/
  utils/
  chapter-01-curves-in-the-plane-and-in-space/
  ...
  appendix-a2-mobius-transformations/
```

The workspace root owns the shared `uv` environment, `pyproject.toml`, and
`uv.lock`. Run commands from `D:\Geometry` unless a script says otherwise.

## Repo-Local Skills

Use the repo-local Codex skills under `D:\Geometry\.codex\skills` for chapter
work:

- `geometry-visualization-planner`: read an assigned source span and produce a
  concrete visual storyboard before authoring.
- `geometry-chapter-notebook-author`: author the standalone visual-first
  canonical notebook directly in its chapter folder.
- `geometry-notebook-qc`: review notebooks, artifacts, execution, visual
  relevance, stale paths, and dependency fit before handoff.

When using parallel workers, assign one worker to one canonical notebook, one
helper module, or one script task. Chapter workers are not alone in the
codebase; they must not revert other workers' edits and should only touch their
assigned chapter folder, matching artifact subtree, and explicitly assigned
helper.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or
  figures.
- The PDF is source orientation only. A reader should not need the PDF open.
- Visualization is part of delivery, not decoration or a quota. Use diagrams,
  plots, 3D scenes, symbolic checks, mesh/surface views, proof-state diagrams,
  and computational experiments wherever they clarify the geometry.
- Keep helpers in `utils/`, outputs in `artifacts/`, and validation tools in
  `scripts/`.
- Every canonical notebook should execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local. Avoid hardcoded
  workspace artifact/helper paths.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per content
  folder.

## Source Map

Use the explicit physical PDF spans below. Back matter hints, solutions, and
index are inventoried only.

| Unit | Printed Pages | PDF Pages | Sections |
| --- | --- | --- | --- |
| Chapter 1: Curves in the plane and in space | 1-27 | 11-37 | 1.1-1.5 |
| Chapter 2: How much does a curve curve? | 29-54 | 38-63 | 2.1-2.3 |
| Chapter 3: Global properties of curves | 55-66 | 64-74 | 3.1-3.3 |
| Chapter 4: Surfaces in three dimensions | 67-94 | 75-101 | 4.1-4.5 |
| Chapter 5: Examples of surfaces | 95-120 | 102-126 | 5.1-5.6 |
| Chapter 6: The first fundamental form | 121-158 | 127-163 | 6.1-6.5 |
| Chapter 7: Curvature of surfaces | 159-178 | 164-182 | 7.1-7.4 |
| Chapter 8: Gaussian, mean and principal curvatures | 179-214 | 183-217 | 8.1-8.6 |
| Chapter 9: Geodesics | 215-246 | 218-248 | 9.1-9.5 |
| Chapter 10: Gauss' Theorema Egregium | 247-269 | 249-270 | 10.1-10.4 |
| Chapter 11: Hyperbolic geometry | 270-304 | 271-306 | 11.1-11.5 |
| Chapter 12: Minimal surfaces | 305-334 | 307-335 | 12.1-12.5 |
| Chapter 13: The Gauss-Bonnet theorem | 335-378 | 336-378 | 13.1-13.8 |
| Appendices A0-A2 | appendix labels | 379-398 | linear algebra, Euclidean isometries, Mobius maps |

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Translation guide from book concepts into computational language.
3. Route through the chapter.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Visual explanations and executable artifacts.
8. Applied lab or design exercise.
9. Sanity checks asserting core identities and artifact existence.
10. Takeaways.

The setup cell should discover the book root by searching upward for both
`00-book-index.ipynb` and `utils`, then prepend that path to `sys.path`.

## Visualization-First Contract

The standard is not a fixed visual count; the standard is whether the notebook
can teach the chapter without the textbook open.

- Artifact filenames must name the concept, not the rendering technology.
- Prose near a visual must name what to inspect.
- Final sanity checks must assert artifact existence, nonzero size, and relevant
  numeric validation data.
- Repeated placeholder visuals are forbidden.
- Do not use textbook screenshots, PDF crops, or decorative images.
- For proof-heavy material, visualize proof state: assumptions, dependency
  graph, limiting process, deformation, orientation, or a small symbolic/numeric
  example.
- Use interactive Plotly, ipywidgets, PyVista, Trimesh, or other installed tools
  when changing a parameter, rotating a model, or inspecting a surface teaches
  the idea.

## Artifacts

Store generated outputs under stable unit paths:

```text
artifacts/chapter-01/
...
artifacts/appendix-a2/
```

Use subfolders such as `figures/`, `interactive/`, `checks`, and `tables`.
Write checks as JSON or CSV when they summarize reproducible invariants.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Elementary-Differential-Geometry-Andrew-Pressley/scripts/build_pressley_course_indexes.py
uv run python -m compileall -q Elementary-Differential-Geometry-Andrew-Pressley/utils Elementary-Differential-Geometry-Andrew-Pressley/scripts
uv run pytest -q Elementary-Differential-Geometry-Andrew-Pressley/scripts
uv run python Elementary-Differential-Geometry-Andrew-Pressley/scripts/audit_pressley_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Elementary-Differential-Geometry-Andrew-Pressley/scripts/audit_pressley_visuals.py
uv run python Elementary-Differential-Geometry-Andrew-Pressley/scripts/validate_pressley_course.py --smoke --timeout 300
uv run python Elementary-Differential-Geometry-Andrew-Pressley/scripts/validate_pressley_course.py --all --timeout 300
git diff --check
```

No dependency changes are expected for this course. Run `uv sync` only if
`pyproject.toml` or `uv.lock` changes intentionally.

## Static Checks Before Commit

Before handoff, verify:

- No root-level `utils/`, `artifacts/`, or book-specific `scripts/` directory has
  appeared outside the book folder.
- No notebook or script contains stale root artifact/helper paths.
- Every content folder has one canonical notebook plus `00-index.ipynb`.
- Markdown links resolve for local notebook, helper, JSON, CSV, PNG, HTML, and
  text references.
- The source PDF is preserved but not staged as a newly generated artifact.
