---
name: geometry-chapter-notebook-author
description: Author standalone visualization-first geometry notebooks. Use when Codex is assigned a geometry textbook chapter or page span and must directly create or revise the canonical notebook with original prose, diagrams, plots, code experiments, artifacts, and sanity checks.
---

# Geometry Chapter Notebook Author

## Purpose

Use this skill when writing the actual notebook, not just planning it. The notebook should teach the assigned chapter as a standalone computational lesson with visualizations and checks integrated into the explanation.

Read `references/geometry-library-catalog.md` before choosing plotting, symbolic, mesh, topology, computer vision, geometric algebra, optimal transport, GIS, or artifact tools.

## Chapter-First Rule

- Inspect the assigned source pages or chapter span before authoring. Use the source only for orientation, terminology, structure, and concept coverage.
- Author the canonical teaching notebook directly as a chapter-specific lesson.
- Scripts may support indexing, auditing, validation, artifact helpers, and small reproducible assets.
- Scripts must not mass-populate teaching notebooks with repeated generic markdown/code cells.
- Bootstrap scripts may create folder skeletons only unless the user explicitly asks for a rough bootstrap draft.
- Do not copy textbook prose, long exercise text, screenshots, page crops, figures, or page layouts.

## Authoring Workflow

1. Read the course `AGENTS.md`, assigned source span, chapter index, existing canonical notebook, generated artifacts, helper conventions, and any visualization storyboard.
2. During improvement passes, preserve useful existing prose, working code, artifacts, and checks. Replace only weak, stale, decorative, generic, or broken material.
3. Work directly in the assigned canonical notebook and matching artifact subtree. Keep one canonical teaching notebook per chapter unless the user requested a structural change.
4. Implement the approved storyboard. If no storyboard exists, create a brief source-specific visual plan before editing.
5. Write original teaching prose around chapter concepts:
   - title and source span
   - chapter goal or question
   - translation guide from book concepts to computational language
   - concept sections with visual explanations and code
   - proof or invariant scaffolds
   - applied lab or exploration
   - final checks and takeaways
6. Choose installed libraries by concept from the catalog. Do not default to Matplotlib when Plotly, PyVista, Trimesh, mesh tools, TDA, CV, manifold, transport, or GA tools better match the chapter.
7. Save outputs under the book-local `artifacts/` subtree and display them inline with the course helper such as `display_artifact(...)`.
8. End with sanity checks that assert core identities, artifact existence, nonzero artifact size, and relevant numeric/symbolic/geometric validation data.

## Visualization Expectations

- Every major visual must teach a concept, construction, invariant, proof move, or failure mode.
- Nearby prose must tell the learner what to inspect and why that representation was chosen.
- Use durable PNG/SVG for static diagrams, standalone HTML for Plotly or rich interactive views, and JSON/CSV for invariant summaries when useful.
- For proof-oriented material, expose proof state through dependency graphs, commutative diagrams, deformation/limit views, counterexample generators, invariant trackers, finite models, or symbolic identity checks.
- If a major concept has no appropriate visual or computational representation, document why in the notebook and provide the smallest useful textual, tabular, or symbolic scaffold.

## Helper Guidance

- Keep helper APIs small, readable, and course-local. Chapter-specific helpers belong in the course `utils/` namespace named for the chapter.
- Avoid opaque helpers that hide the pedagogy. If a helper is necessary, show the mathematical inputs/outputs in notebook cells.
- Keep generated paths relative or book-local. Avoid hardcoded workspace paths.
- Document optional/external tools in markdown rather than adding dependencies unless the user explicitly asks.

## Final Implementation Report

Report these fields at handoff:

- `notebook path`
- `source span used`
- `storyboard items implemented`
- `libraries used and why`
- `artifacts generated`
- `checks included`
- `known gaps`

Also report changed files, validation commands, and any residual execution or source-map risks.
