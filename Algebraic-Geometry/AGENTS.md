# Agent Instructions: Hartshorne Algebraic Geometry Notebook Course

This folder is a standalone visualization-first notebook edition of Robin Hartshorne's *Algebraic Geometry* (Graduate Texts in Mathematics 52). Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, figures, or page layouts.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualizations are part of the explanation. Use algebraic diagrams, chart atlases, dependency graphs, symbolic checks, finite models, interactive HTML, and invariant dashboards wherever they clarify the algebraic geometry.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook should execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Use exact arithmetic for algebra checks when possible. Numeric samples may support visualization but should not replace exact validation.

## Course Structure

```text
00-book-index.ipynb
AGENTS.md
artifacts/
scripts/
utils/
chapter-01-varieties/
chapter-02-schemes/
chapter-03-cohomology/
chapter-04-curves/
chapter-05-surfaces/
appendix-a-intersection-theory/
appendix-b-transcendental-methods/
appendix-c-weil-conjectures/
```

Each chapter or appendix folder contains exactly one canonical teaching notebook plus `00-index.ipynb`.

## Source Map

Use explicit spans from `scripts/ag_inventory.py`. The local PDF has 511 physical pages. Main-matter printed page 1 is PDF page 16, so the chapter and appendix spans below use a stable `printed page + 15 = PDF page` rule for the main matter. The source is used only for orientation; notebooks must not reproduce textbook prose, exercises, screenshots, or page crops. The local PDF is user-provided and is not redistributed by generated notebooks or artifacts.

## Notebook Shape

Each canonical notebook should contain title/source span, standalone motivation, a translation guide, setup, concept sections, executable examples, generated visual artifacts, a small lab or exploration, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/chapter-XX/` or `artifacts/appendix-x/`, using `figures/`, `html/`, `checks/`, and `tables/` subfolders. Artifact filenames should name the concept, not the rendering technology. Repeated placeholder visuals are a QC failure. Every generated visual artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding dependencies: `sympy`, `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `networkx`, `pandas`, `shapely`, and the rest of the root geometry stack.

SageMath, Singular, and Macaulay2 are not installed locally. Use SymPy and small readable helpers for in-notebook exact demonstrations; mark Sage/Singular/Macaulay2 workflows as optional external CAS workflows.

## Worker Boundaries

Other workers may edit other course folders. Do not write outside `Algebraic-Geometry` unless the user explicitly assigns shared work. Chapter workers may edit only their chapter folder, matching artifact subtree, and explicitly assigned helper module. Index workers own `00-book-index.ipynb` and `00-index.ipynb` files. QC workers run audits and validation and report findings.

## Commands

Run from `D:\Geometry`:

```powershell
$book = 'D:\Geometry\Algebraic-Geometry'
uv run python ([System.IO.Path]::Combine($book, 'scripts', 'build_ag_course_indexes.py'))
uv run python -m compileall -q ([System.IO.Path]::Combine($book, 'utils')) ([System.IO.Path]::Combine($book, 'scripts'))
uv run python ([System.IO.Path]::Combine($book, 'scripts', 'audit_ag_notebooks.py')) --min-words 900 --min-code-cells 4
uv run python ([System.IO.Path]::Combine($book, 'scripts', 'audit_ag_visuals.py'))
uv run python ([System.IO.Path]::Combine($book, 'scripts', 'validate_ag_course.py')) --limit 3 --timeout 300
git diff --check -- Algebraic-Geometry
```

Run full validation with:

```powershell
uv run python ([System.IO.Path]::Combine($book, 'scripts', 'validate_ag_course.py')) --all --timeout 300
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Visualization Library Policy

- Use Matplotlib for durable 2D diagrams, chart atlases, incidence pictures, divisor sketches, Newton polygons, and labeled static figures.
- Use Plotly for interactive parameter labs, surfaces, filtrations, families, and point-count dashboards.
- Use NetworkX for dependency graphs, gluing diagrams, exact-sequence scaffolds, spectral-sequence page transitions, and incidence graphs.
- Use SymPy for exact polynomial, homogeneous-coordinate, divisor-degree, Cech-coboundary, and finite-field point-count checks.
- Use NumPy and pandas for small numerical tables, sample clouds, and reproducible summaries.

Every major visualization must have a nearby explanation naming the concept it teaches, the reason this representation was chosen, the learner inspection target, and a check or invariant where practical.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact creation, but they must not replace chapter-specific pedagogy with repeated template prose.
