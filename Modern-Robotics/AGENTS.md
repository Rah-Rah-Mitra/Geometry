# Agent Instructions: Modern Robotics Notebook Course

This folder is a standalone visualization-first notebook edition of *Modern Robotics: Mechanics, Planning, and Control* by Kevin M. Lynch and Frank C. Park. Treat this book folder as the project root for the course. The workspace root still owns the shared `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local Codex skills under `D:\Geometry\.codex\skills` for course work:

- `geometry-visualization-planner`: storyboard each chapter before authoring.
- `geometry-chapter-notebook-author`: author the canonical standalone notebook in its chapter folder.
- `geometry-notebook-qc`: review notebooks, artifacts, helpers, stale paths, and execution.

## Non-Negotiables

- Write original teaching prose, derivations, code, diagrams, and explanations.
- Do not copy textbook prose, long exercise text, screenshots, page crops, photos, or tables.
- A reader should not need the PDF open. Each notebook must include motivation, definitions, computational translations, worked examples, pitfalls, sanity checks, applied labs, and takeaways.
- Visualization is central, not decorative. Use diagrams, 2D and 3D plots, widgets, symbolic checks, proof diagrams, mesh or surface views, and computational experiments wherever they clarify the robotics geometry.
- Store course helpers in `utils/`, scripts in `scripts/`, and generated outputs in `artifacts/`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per chapter or appendix folder.
- Keep the PDF local to the source folder. Do not copy it into generated artifacts or treat it as a redistributable course output.

## Source Map

The local PDF is `Mordern Robotics.pdf`. The filename is intentionally recorded as found in the folder. Printed pages map to PDF pages by:

```text
pdf_page = printed_page + 18
```

The course follows five parts: geometric foundations, manipulator kinematics, dynamics/trajectories/planning, control/contact/mobile robots, and reference appendices.

## Notebook Shape

Each canonical notebook should contain:

1. Title, source span, and chapter question.
2. Translation guide from textbook concepts into computational language.
3. Route through the notebook.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Visual explanations and generated artifacts.
8. Applied lab or design exercise.
9. Sanity checks for identities, artifact existence, and numeric margins.
10. Takeaways.

## Artifact Rules

Artifacts are part of the teaching product. Use stable book-local paths such as:

```text
artifacts/chapter-03-rigid-body-motions/figures/screw-axis-lab.png
artifacts/chapter-10-motion-planning/checks/final-sanity.json
artifacts/appendix-b-other-representations-of-rotations/figures/rotation-parameter-comparison.png
```

Artifact filenames must name the concept, not the rendering technology. Every generated artifact should be displayed inline and asserted in the final sanity cell. Repeated placeholder visuals, blank images, and copied PDF figures are QC failures.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `networkx`, `shapely`, `trimesh`, and `pyvista` are available. Do not add dependencies unless the user explicitly asks.

## Worker Boundaries

For parallel work, assign one worker to one canonical notebook or one clearly bounded helper/script task. Chapter workers may edit only their assigned chapter folder, its matching artifact subtree, and explicitly assigned helper modules. Index and QC workers own global navigation and validation reports.

## Validation Commands

Run from `D:\Geometry`:

```powershell
uv run python -m compileall -q "Modern-Robotics/utils" "Modern-Robotics/scripts"
uv run pytest -q "Modern-Robotics/scripts"
uv run python "Modern-Robotics/scripts/build_modern_robotics_course_indexes.py"
uv run python "Modern-Robotics/scripts/audit_modern_robotics_notebooks.py" --min-words 1200 --min-code-cells 5
uv run python "Modern-Robotics/scripts/audit_modern_robotics_visuals.py"
uv run python "Modern-Robotics/scripts/validate_modern_robotics_course.py" --limit 6 --timeout 300
uv run python "Modern-Robotics/scripts/validate_modern_robotics_course.py" --all --timeout 300
git diff --check
```

Only run `uv sync` if dependencies change.
