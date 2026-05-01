---
name: geometry-visualization-planner
description: Plan visualization-first geometry notebook chapters. Use when Codex needs to turn a textbook chapter or page span into a storyboard of diagrams, 3D plots, interactive widgets, symbolic/numeric experiments, mesh views, proof visuals, and artifact/check choices before authoring a standalone geometry notebook.
---

# Geometry Visualization Planner

## Purpose

Use this skill before authoring or revising a geometry notebook chapter. The output is a chapter-specific implementation brief and visual storyboard that another chapter worker can implement directly.

Read `references/geometry-library-catalog.md` when choosing libraries, especially for 3D surfaces, meshes, topology, geometric algebra, projective/CV geometry, optimal transport, GIS, or symbolic geometry.

## Chapter-First Rule

- Inspect the assigned source pages or chapter span before planning. Use the PDF/source only for orientation, terminology, structure, and concept coverage.
- Plan a canonical teaching notebook as a direct chapter-specific lesson, not as the output of a generic notebook generator.
- Scripts may support indexing, auditing, validation, artifact helpers, and small reproducible assets.
- Scripts must not mass-populate teaching notebooks with repeated generic markdown/code cells.
- Bootstrap scripts may create folder skeletons only unless the user explicitly asks for a rough bootstrap draft.
- Do not plan copied textbook prose, long exercise text, screenshots, page crops, figures, or page layouts.

## Workflow

1. Read the course `AGENTS.md`, assigned source span, chapter index, existing canonical notebook, and relevant helper/artifact conventions.
2. Extract chapter-specific teaching claims: definitions, constructions, proof moves, invariants, examples, failure modes, and likely learner misconceptions.
3. Build a concept inventory and route each major concept to an inspectable representation:
   - diagram for incidence, orientation, area, angle, dependency, or proof structure
   - Matplotlib/Plotly plot for curves, fields, maps, level sets, transformations, or model comparisons
   - PyVista/Trimesh/mesh tools for surfaces, frames, curvature, polyhedra, geodesics, or mesh diagnostics
   - widget for parameter variation that teaches the concept
   - SymPy/Galgebra/GA package check for identities, metrics, forms, products, homogeneous coordinates, or limits
   - TDA/CV/OT/GIS library only when the chapter's geometry calls for that domain
4. Justify library choices from the catalog. Do not default to Matplotlib when 3D, mesh, topology, projective/CV, manifold, transport, or geometric algebra tools make the geometry more inspectable.
5. Plan artifact paths under the course-local `artifacts/` subtree. Artifact names must describe the concept, not the renderer.
6. Attach a learner inspection target and a validation/invariant to every planned visual. Reject decorative visuals.

## Proof Visualization

For proof-heavy chapters, choose at least one useful proof view when possible:

- proof dependency graph
- commutative diagram
- deformation or limiting process
- counterexample generator
- invariant tracker
- small finite model
- symbolic identity check

If a major proof concept has no useful visual or computational representation, say why and name the smallest textual or symbolic scaffold the author should provide.

## Storyboard Format

Return a compact Chapter Implementation Brief with these fields:

- `chapter goal`: standalone learning outcome.
- `source span read`: pages/files inspected and any source-map notes.
- `concept inventory`: chapter-specific definitions, constructions, theorem moves, examples, and misconceptions.
- `library routing table`: concept, representation, library, why this library, and fallback.
- `visual sequence`: ordered visuals with concept, representation, library, artifact filename, learner inspection target, and validation/invariant.
- `artifact plan`: book-local paths for PNG/SVG/HTML/JSON/CSV/table assets.
- `computational checks`: assertions, symbolic checks, numerical tolerances, or JSON/CSV invariant summaries.
- `proof-visualization strategy`: dependency/deformation/diagram/counterexample/invariant/finite-model/symbolic plan.
- `implementation notes`: helper boundaries, direct notebook authoring notes, artifact display notes, and dependency caveats.
- `risks`: copyright, execution, stale paths, weak visuals, missing source details, or library fit risks.
- `acceptance criteria`: concrete checks the author and QC worker should run.

## Standards

- The chapter is complete when the visual and computational treatment can carry the geometry without requiring the textbook open.
- Prefer direct, inspectable constructions over opaque helpers or animations.
- Keep the storyboard implementable by one chapter worker without global refactors unless the assignment explicitly includes shared utility work.
- Use the catalog examples as style references, but make every storyboard source-specific.
