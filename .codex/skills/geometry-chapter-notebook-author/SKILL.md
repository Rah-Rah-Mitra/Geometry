---
name: geometry-chapter-notebook-author
description: Author standalone visualization-first geometry notebooks. Use when Codex is assigned a geometry textbook chapter or page span and must directly create or revise the canonical notebook with original prose, diagrams, plots, code experiments, artifacts, and sanity checks.
---

# Geometry Chapter Notebook Author

## Purpose

Use this skill when writing the actual notebook, not just planning it. The notebook should teach the chapter as a standalone computational lesson with visualizations as part of the explanation.

Read `references/geometry-library-catalog.md` when deciding which plotting, symbolic, mesh, computer vision, geometric algebra, optimal transport, or topological data analysis tools to use.

## Authoring Workflow

1. Read the course `AGENTS.md`, the assigned source pages, the local chapter index, any existing canonical notebook, and any visualization storyboard.
2. Work directly in the assigned chapter notebook and its matching artifact subtree. Do not replace chapter work with a monolithic course-generation script unless the assignment is explicitly a bootstrap or inventory task.
3. Write original teaching prose. Do not copy textbook passages, long exercise text, figures, screenshots, or page crops.
4. Build the notebook around concept sections:
   - motivation and chapter question
   - definitions and computational translations
   - visual explanations and diagrams
   - executable examples
   - interactive or parameterized explorations when useful
   - symbolic or numeric checks
   - pitfalls, applied lab, and takeaways
5. Save reusable outputs under the book-local `artifacts/` subtree and display them inline with the course helper such as `display_artifact(...)`.
6. End with sanity checks that assert core identities, artifact existence, nonzero artifact size, and relevant numeric validation data.

## Visualization Expectations

- Use as many visual forms as the chapter needs: diagrams, Matplotlib, Plotly, PyVista, Trimesh, widgets, SymPy derivations, mesh diagnostics, image/CV transforms, TDA diagrams, or geometric algebra views.
- Make the visual explain a concept, construction, invariant, or failure mode. Avoid decorative output.
- Label geometry, choose meaningful scales/aspect ratios, and include legends or annotations when objects overlap.
- For proof-oriented material, create visual or code scaffolds that expose the proof idea: limiting processes, dependency graphs, examples, deformation, obstruction, orientation, or invariant preservation.
- Prefer static PNG/SVG for durable diagrams and standalone HTML for interactive Plotly views.

## Implementation Notes

- Keep helper APIs small and readable; chapter-specific helpers belong in the course `utils/` namespace named for the chapter.
- Use installed libraries from the catalog first. Document optional/external tools in markdown if they would be ideal but are not installed.
- Keep paths relative or book-local. Avoid hardcoded workspace paths inside notebooks.
- Preserve the one-canonical-notebook-per-chapter structure unless the user asks for a structural migration.
- Report changed files, generated artifacts, checks run, and any residual gaps.
