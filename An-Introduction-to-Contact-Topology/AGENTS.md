# Agent Instructions: An Introduction to Contact Topology Notebook Course

This folder is a standalone visualization-first notebook edition of Hansjorg
Geiges's *An Introduction to Contact Topology*. Treat this book folder as the
course root. The workspace root owns the shared `uv` environment,
`pyproject.toml`, and `uv.lock`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or solution text.
- The PDF is source orientation only. A reader should not need the PDF open.
- Visualization is part of delivery, not decoration or a quota.
- Keep helpers in `utils/`, outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook should execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per content folder.

## Course Structure

```text
An-Introduction-to-Contact-Topology/
  00-book-index.ipynb
  AGENTS.md
  source-map.json
  artifacts/
  scripts/
  utils/
  chapter-01-facets-of-contact-geometry/
  ...
  chapter-08-contact-structures-on-5-manifolds/
  appendix-a-generalised-poincare-lemma/
  appendix-b-time-dependent-vector-fields/
```

## Source Map

Printed page 1 starts at physical PDF page 19. For main-matter printed pages,
the physical PDF page is printed page plus 18.

| Unit | Folder | Printed Pages | PDF Pages | Focus |
| --- | --- | ---: | ---: | --- |
| Chapter 1 | `chapter-01-facets-of-contact-geometry` | 1-50 | 19-68 | Contact forms, Reeb fields, contact elements, mechanics, geodesic flow, order of contact, applications. |
| Chapter 2 | `chapter-02-contact-manifolds` | 51-92 | 69-110 | Examples, Gray stability, Moser trick, Hamiltonians, Darboux and neighborhood theorems, isotopy extension. |
| Chapter 3 | `chapter-03-knots-in-contact-3-manifolds` | 93-129 | 111-147 | Legendrian and transverse knots, projections, approximation, linking, classical invariants. |
| Chapter 4 | `chapter-04-contact-structures-on-3-manifolds` | 130-267 | 148-285 | Martinet, Lutz twist, tight/overtwisted, characteristic foliations, convex surfaces, tomography, classification. |
| Chapter 5 | `chapter-05-symplectic-fillings-and-convexity` | 268-285 | 286-303 | Weak/strong fillings, cobordisms, Levi pseudoconvexity, omega-convexity. |
| Chapter 6 | `chapter-06-contact-surgery` | 286-331 | 304-349 | Topological and contact surgery, framings, contact Dehn surgery, symplectic fillings. |
| Chapter 7 | `chapter-07-further-constructions-of-contact-manifolds` | 332-365 | 350-383 | Brieskorn manifolds, Boothby-Wang, open books, connected sums, branched covers, plumbing, reduction. |
| Chapter 8 | `chapter-08-contact-structures-on-5-manifolds` | 366-400 | 384-418 | Almost contact structures, 5-manifold structure, existence of contact structures. |
| Appendix A | `appendix-a-generalised-poincare-lemma` | 401-403 | 419-421 | Homotopy operator behind a relative Poincare lemma. |
| Appendix B | `appendix-b-time-dependent-vector-fields` | 404-407 | 422-425 | Time-dependent vector fields, flows, pullback and Lie derivative identities. |

Back matter is inventoried in `scripts/ict_inventory.py` and `source-map.json`
but is not a canonical teaching notebook.

## Notebook Shape

Each canonical notebook should contain a title and source span, a standalone
chapter question, a translation guide, setup cell, original concept sections,
generated visual artifacts displayed inline, worked examples, an applied lab,
sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under:

```text
artifacts/chapter-01/
...
artifacts/chapter-08/
artifacts/appendix-a/
artifacts/appendix-b/
```

Use subfolders such as `figures/`, `html/`, `checks/`, and `tables/`. Artifact
filenames should name the concept, not the rendering technology. Every
generated artifact should be displayed inline or linked from the notebook, and
final checks should assert that files exist and are nonempty.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed
libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`,
`plotly`, `ipywidgets`, `sympy`, `pandas`, `networkx`, `shapely`, `trimesh`,
`pyvista`, `ripser`, `gudhi`, and the rest of the root geometry stack.
This course currently needs no dependency additions.

## Worker Boundaries

Assign one worker to one canonical notebook, one helper module, or one script
task. Chapter workers may edit only their chapter folder, matching artifact
subtree, and explicitly assigned helper module. Index workers own
`00-book-index.ipynb` and `00-index.ipynb` files. QC workers run audits and
validation and report findings.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python An-Introduction-to-Contact-Topology/scripts/export_ict_source_map.py
uv run python An-Introduction-to-Contact-Topology/scripts/build_ict_course_indexes.py
uv run python -m compileall -q An-Introduction-to-Contact-Topology/utils An-Introduction-to-Contact-Topology/scripts
uv run python An-Introduction-to-Contact-Topology/scripts/audit_ict_notebooks.py --min-words 900 --min-code-cells 4
uv run python An-Introduction-to-Contact-Topology/scripts/audit_ict_visuals.py
uv run python An-Introduction-to-Contact-Topology/scripts/validate_ict_course.py --smoke --timeout 240
git diff --check
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Geometry Visualization Library Policy

Use the installed geometry stack intentionally. Do not default to generic
Matplotlib-only notebooks when the chapter's geometry calls for richer
representations.

### Library Routing

- Use Matplotlib for durable 2D diagrams, front projections, characteristic foliations, surgery sketches, and labeled static figures.
- Use Plotly for interactive 2D/3D parameter exploration, open books, wavefronts, contact planes, and standalone HTML artifacts.
- Use SymPy for exact checks with forms, contact volume coefficients, Reeb equations, homotopy operators, and flow identities.
- Use NetworkX for proof dependency graphs, surgery/plumbing graphs, and obstruction diagrams.
- Use NumPy/SciPy for sampled flows, rotation numbers, fronts, and lightweight numerical checks.
- Use PyVista/Trimesh only when a chapter needs inspectable 3D surfaces or meshes beyond simple Plotly scenes.

### Visual Justification Rule

Every major visualization must have:

1. the concept it teaches,
2. the reason this representation was chosen,
3. an inspection target for the learner,
4. a nearby prose explanation,
5. a check, invariant, or sanity test where practical.

Decorative visuals are not acceptable.

### Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course
generator. Scripts may support indexing, auditing, validation, and reproducible
artifact creation, but they must not replace direct chapter-specific pedagogy.
