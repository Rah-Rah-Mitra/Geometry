# Agent Instructions: Lectures on Symplectic Geometry Notebook Course

This folder is a standalone visualization-first notebook edition of Ana Cannas
da Silva's local PDF, `Lectures on Symplectic Geometry.pdf`. Treat this folder as
the project root for this course. The workspace root owns the shared Python
environment files.

## Repo-Local Skills

Use the repo-local geometry skills in `D:\Geometry\.codex\skills` for planning,
authoring, and quality control:

- `geometry-visualization-planner`
- `geometry-chapter-notebook-author`
- `geometry-notebook-qc`

The local PDF is used only for orientation, terminology, lecture order, and
source spans. Do not copy textbook prose, screenshots, page crops, figures, or
long exercise text.

## Source Map

The physical PDF has 223 pages. Arabic printed body pages map to physical PDF
pages by:

```text
physical_pdf_page = printed_page + 14
```

The table of contents places the course in eleven parts and thirty lecture
chapters:

- Part I: Lectures 1-2, introduction.
- Part II: Lectures 3-5, symplectomorphisms.
- Part III: Lectures 6-9, local forms.
- Part IV: Lectures 10-11, contact manifolds.
- Part V: Lectures 12-14, compatible almost complex structures.
- Part VI: Lectures 15-17, Kahler manifolds.
- Part VII: Lectures 18-20, Hamiltonian mechanics.
- Part VIII: Lectures 21-22, moment maps.
- Part IX: Lectures 23-24, symplectic reduction.
- Part X: Lectures 25-27, moment maps revisited.
- Part XI: Lectures 28-30, symplectic toric manifolds.

The canonical machine-readable inventory is
`scripts/lsg_inventory.py`; generated JSON copies live in `source-map.json` and
`artifacts/source-map.json`.

## Notebook Contract

Each lecture folder contains exactly one canonical lecture notebook plus a
`00-index.ipynb`:

1. Title and source span.
2. Original translation guide from the lecture's terms to computational objects.
3. Route through the lecture and proof/invariant scaffold.
4. Setup cell that discovers `BOOK_ROOT`.
5. Visual artifacts displayed near the prose that explains them.
6. Executable checks for the lecture's symplectic, contact, complex, Hamiltonian,
   moment-map, reduction, or toric invariant.
7. Final sanity checks for artifact existence and recorded validation values.
8. Takeaways and a small exploration prompt.

Generated paths must be book-local or relative. Keep helpers small and readable
in `utils/`; outputs under `artifacts/`; validation and audit tools under
`scripts/`.

## Visualization-First Requirements

Visuals are part of the mathematical argument, not decorative quota. Every
major artifact should state what to inspect and which invariant it checks:

- symplectic linear algebra: skew normal forms, Lagrangian planes, symplectic
  matrix residuals;
- cotangent and Lagrangian geometry: tautological/canonical forms, conormal
  models, graphs of closed one-forms;
- local normal forms: Darboux and Moser deformation fields;
- contact geometry: contact planes, Reeb dynamics, symplectization;
- compatible complex and Kahler structures: triples, type decompositions, Hodge
  restrictions, Fubini-Study examples;
- Hamiltonian mechanics: phase portraits, Poisson brackets, action checks,
  Legendre duality;
- moment maps, reduction, and toric geometry: group orbits, fibers, convex
  images, Delzant normals, and Duistermaat-Heckman volume variation.

For proof-heavy lectures, use dependency graphs, deformation diagrams,
symbolic/numeric identities, quotient sketches, or counterexample ledgers.

## Commands

Run from the workspace root:

```powershell
uv run python Lectures-on-Symplectic-Geometry/scripts/bootstrap_lsg_course.py
uv run python Lectures-on-Symplectic-Geometry/scripts/build_lsg_artifacts.py
uv run python Lectures-on-Symplectic-Geometry/scripts/build_lsg_course_indexes.py
uv run python -m compileall -q Lectures-on-Symplectic-Geometry/utils Lectures-on-Symplectic-Geometry/scripts
uv run pytest -q Lectures-on-Symplectic-Geometry/scripts
uv run python Lectures-on-Symplectic-Geometry/scripts/audit_lsg_notebooks.py --min-words 650 --min-code-cells 4
uv run python Lectures-on-Symplectic-Geometry/scripts/audit_lsg_visuals.py
uv run python Lectures-on-Symplectic-Geometry/scripts/validate_lsg_course.py --limit 6 --timeout 180
uv run python Lectures-on-Symplectic-Geometry/scripts/validate_lsg_course.py --all --timeout 240
git diff --check -- Lectures-on-Symplectic-Geometry
```

## Worker Boundaries

Other workers may edit other course folders. Stay inside
`Lectures-on-Symplectic-Geometry` unless the user explicitly broadens the task.
Never revert changes made by other workers. When improving one lecture, edit only
that lecture folder, its matching artifact subtree, and an explicitly assigned
helper or script.
