---
name: geometry-notebook-qc
description: Quality-check visualization-first geometry notebooks. Use when Codex needs to review geometry notebooks, artifacts, and helper changes for standalone teaching quality, visual relevance, executable correctness, artifact integrity, stale paths, and dependency fit.
---

# Geometry Notebook QC

## Purpose

Use this skill after authoring or revising a geometry notebook chapter. The goal is to catch weak standalone explanations, missing or decorative visualizations, broken artifacts, execution failures, stale paths, and dependency mistakes.

Read `references/geometry-library-catalog.md` when evaluating whether a notebook uses the available stack appropriately.

## Review Workflow

1. Read the course `AGENTS.md`, the changed notebook, local helper changes, and generated artifacts.
2. Check standalone delivery:
   - the reader can learn the chapter without opening the textbook
   - definitions, motivation, examples, pitfalls, checks, and takeaways are present
   - textbook text and images are not copied
3. Check visualization quality:
   - visuals are concept-specific and integrated into the teaching argument
   - proof-heavy sections have diagrams, symbolic experiments, dependency views, or runnable examples where useful
   - labels, scale, aspect ratio, colors, and legends make the geometry inspectable
   - repeated placeholders, blank images, and decorative visuals are rejected
4. Check artifacts:
   - outputs live under the matching book-local `artifacts/` subtree
   - filenames name the concept
   - generated artifacts are displayed inline and asserted in final checks
   - JSON/CSV checks record key invariants when relevant
5. Run the narrowest useful validation commands first, then broaden when shared helpers or global indexes changed.

## Command Guidance

Use the commands listed in each course `AGENTS.md`. For quick checks, prefer:

- `uv run python -m compileall -q <course>/utils <course>/scripts`
- course notebook audit script
- course visual audit script when present
- limited `validate_*_course.py` execution before full validation
- `git diff --check`

Run full notebook validation when shared utilities, setup cells, artifact helpers, or many notebooks changed.

## Reporting

Lead with actionable findings. For each issue, include the file path, tight location when possible, why it weakens the notebook, and the concrete fix. If there are no findings, state that and list any checks not run.
