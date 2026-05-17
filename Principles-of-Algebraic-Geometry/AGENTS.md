# Agent Instructions: Principles of Algebraic Geometry Notebook Course

Standalone visualization-first course for Griffiths and Harris, Principles of
Algebraic Geometry.

Use the repo-local geometry skills in D:/Geometry/.codex/skills:

- geometry-visualization-planner before chapter authoring
- geometry-chapter-notebook-author for direct notebook edits
- geometry-notebook-qc after edits

Course rules:

- Read the verified chapter span from scripts/pag_inventory.py and inspect the
  matching PDF pages before revising a notebook. The source is for structure,
  terminology, theorem orientation, and coverage only.
- Do not copy textbook prose, long exercise text, screenshots, page crops, or
  source figures.
- Preserve useful existing work, but replace bootstrap prose, generic sliders,
  generic images, stale paths, and decorative visuals.
- Each chapter notebook must stand alone: source span, chapter goal, translation
  guide, section-level coverage ledger, visual storyboard, library routing,
  concept explanations, proof/invariant scaffolds, computational experiments,
  local artifacts, and final sanity checks.
- Save chapter outputs under artifacts/chapter-XX/. Artifact filenames should
  describe the concept, not the renderer.
- Do not use a monolithic generator to author teaching notebooks. Scripts may
  support inventory, indexing, audits, validation, helpers, and small assets.

Useful checks:

```
..\.venv\Scripts\python.exe -m compileall -q utils scripts
..\.venv\Scripts\python.exe scripts\audit_pag_notebooks.py
..\.venv\Scripts\python.exe scripts\audit_pag_visuals.py
..\.venv\Scripts\python.exe scripts\audit_pag_artifacts.py
..\.venv\Scripts\python.exe scripts\validate_pag_course.py --limit 3 --timeout 180
..\.venv\Scripts\python.exe scripts\validate_pag_course.py --all --timeout 300
git diff --check -- Principles-of-Algebraic-Geometry
```
