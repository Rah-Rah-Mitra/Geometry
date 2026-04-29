---
name: geometry-visualization-planner
description: Plan visualization-first geometry notebook chapters. Use when Codex needs to turn a textbook chapter or page span into a storyboard of diagrams, 3D plots, interactive widgets, symbolic/numeric experiments, mesh views, proof visuals, and artifact/check choices before authoring a standalone geometry notebook.
---

# Geometry Visualization Planner

## Purpose

Use this skill before authoring or revising a geometry notebook chapter. The output is a concrete visual storyboard that another chapter worker can implement directly.

Read `references/geometry-library-catalog.md` when choosing libraries, especially if the chapter needs 3D surfaces, geometric algebra, topological data analysis, optimal transport, computer vision, or symbolic geometry.

## Workflow

1. Read the course `AGENTS.md`, the assigned chapter or page span, the chapter index, and any existing canonical notebook.
2. Extract the chapter's teaching claims: definitions, constructions, proof moves, invariants, examples, and likely learner misconceptions.
3. Convert each geometric claim into an inspectable representation when possible:
   - diagram for incidence, orientation, area, angle, or proof structure
   - 2D plot for curves, fields, maps, level sets, or model comparisons
   - 3D plot or mesh for surfaces, frames, curvature, conformal objects, or ray geometry
   - interactive widget for parameters whose variation teaches the concept
   - symbolic check for identities, metrics, forms, products, or limiting arguments
   - numerical experiment for invariants, convergence, stability, or counterexamples
4. Select libraries from the catalog by concept and reliability. Prefer already-installed tools and course-local helpers; use optional/external tools only as documented alternatives.
5. Define artifact names that describe the concept, not the rendering technology.
6. Pair each planned visualization with the invariant or observation the learner should inspect.

## Storyboard Format

Return a compact plan with these fields:

- `chapter goal`: the standalone learning outcome.
- `source span read`: pages or files inspected.
- `visual sequence`: ordered visuals with concept, representation, library, artifact filename, and learner inspection target.
- `computational checks`: assertions or JSON summaries that validate the visuals and identities.
- `implementation notes`: helper functions, artifact paths, and any dependency caveats.
- `gaps`: concepts that are proof-heavy or text-heavy and how to visualize them with diagrams, code snippets, or small symbolic experiments.

## Standards

- Do not impose a fixed number of visuals. The chapter is complete when the visual and computational treatment can carry the geometry without requiring the textbook.
- Do not plan decorative images, textbook screenshots, PDF crops, or repeated placeholder visuals.
- Prefer direct, inspectable constructions over opaque animations.
- For proof-heavy chapters, visualize proof state: assumptions, deformation, limiting process, commutative diagram, dependency graph, or a small example that makes the theorem's invariant visible.
- Keep the storyboard implementable by one chapter worker without global refactors unless the assignment explicitly includes shared utility work.
