# Agent Instructions: Ideals, Varieties, and Algorithms Notebook Course

This folder is a standalone visualization-first notebook edition of *Ideals, Varieties, and Algorithms: An Introduction to Computational Algebraic Geometry and Commutative Algebra*, Fifth Edition.
Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, or page crops.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualizations are part of the explanation. Use diagrams, plots, interactive HTML, symbolic checks, computational experiments, proof-state diagrams, and algorithm traces wherever they clarify the algebraic geometry.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Use exact arithmetic for algebra checks when possible. Numeric samples may support visualization but should not replace exact validation.

## Course Structure

```text
00-book-index.ipynb
AGENTS.md
artifacts/
scripts/
utils/
chapter-01-geometry-algebra-and-algorithms/
...
chapter-10-additional-grobner-basis-algorithms/
appendix-a-some-concepts-from-algebra/
...
appendix-d-independent-projects/
```

Each chapter or appendix folder contains exactly one canonical teaching notebook plus `00-index.ipynb`.

## Source Map

Use explicit spans from `scripts/iva_inventory.py`. The PDF omits some printed blank pages, so do not use one global offset rule. Source spans are for orientation only; notebooks must not reproduce textbook prose, exercises, screenshots, or page crops. The local PDF is a user-provided source file and is not redistributed by generated notebooks or artifacts.

## Notebook Shape

Each canonical notebook should contain title/source span, standalone motivation, a translation guide, setup, concept sections, executable examples, generated visual artifacts, an applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/chapter-XX/` or `artifacts/appendix-x/`, using `figures/`, `html/`, and `checks/` subfolders. Artifact filenames should name the concept, not the rendering technology. Repeated placeholder visuals are a QC failure. Every generated visual artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding dependencies: `sympy`, `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `networkx`, `pandas`, `shapely`, and the rest of the root geometry stack.

SageMath, Singular, and Macaulay2 are not installed locally. Use SymPy and small readable helpers for in-notebook exact demonstrations; mark Sage/Singular/Macaulay2 workflows as optional external CAS workflows.

## Worker Boundaries

Assign one worker to one canonical notebook, one helper module, or one script task. Chapter workers may edit only their chapter folder, matching artifact subtree, and explicitly assigned helper module. Index workers own `00-book-index.ipynb` and `00-index.ipynb` files. QC workers run audits and validation and report findings.

## Commands

Run from `D:\Geometry`:

```powershell
$book = Get-ChildItem -LiteralPath 'D:\Geometry' -Directory | Where-Object { $_.Name -like 'Ideals*' } | Select-Object -First 1
uv run python ([System.IO.Path]::Combine($book.FullName, 'scripts', 'build_iva_course_indexes.py'))
uv run python -m compileall -q ([System.IO.Path]::Combine($book.FullName, 'utils')) ([System.IO.Path]::Combine($book.FullName, 'scripts'))
uv run python ([System.IO.Path]::Combine($book.FullName, 'scripts', 'smoke_iva_stack.py'))
uv run python ([System.IO.Path]::Combine($book.FullName, 'scripts', 'audit_iva_notebooks.py')) --min-words 1200 --min-code-cells 5
uv run python ([System.IO.Path]::Combine($book.FullName, 'scripts', 'audit_iva_visuals.py'))
uv run python ([System.IO.Path]::Combine($book.FullName, 'scripts', 'validate_iva_course.py')) --limit 8 --timeout 300
git diff --check
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.
