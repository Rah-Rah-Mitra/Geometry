# Agent Instructions: Geometric Deep Learning Notebook Course

This folder is a standalone visualization-first notebook edition of
*Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges* by
Michael M. Bronstein, Joan Bruna, Taco Cohen, and Petar Velickovic.

Treat this folder as the project root for this course. The workspace root owns
the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before planning a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring canonical notebooks.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and
  validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or
  textbook figures.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualization is part of the explanation. Use diagrams, plots, 3D scenes,
  interactive HTML, symbolic checks, mesh diagnostics, proof diagrams, and
  computational experiments wherever they clarify the chapter.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation
  tools in `scripts/`.
- Every canonical notebook must execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook per chapter folder plus a local
  `00-index.ipynb`.

## Source Map

The PDF has 160 physical pages. Body printed pages map to physical PDF pages by
`pdf_page = printed_page + 4`. The book has seven chapters, acknowledgements,
and a bibliography. It has no formal parts or appendices.

| Unit | Folder | Printed Pages | PDF Pages | Focus |
| --- | --- | ---: | ---: | --- |
| Front matter | `00-book-index.ipynb` | 1-3 | 5-7 | Preface, notation, course route |
| Chapter 01 | `chapter-01-introduction` | 4 | 8 | Representation learning, structured data, symmetry preview, GDL design loop |
| Chapter 02 | `chapter-02-learning-in-high-dimensions` | 5-8 | 9-12 | Interpolation, regularity, implicit bias, Lipschitz fill distance, covering growth |
| Chapter 03 | `chapter-03-geometric-priors` | 9-29 | 13-33 | Signals on domains, groups/actions, invariance/equivariance, stability, scale separation |
| Chapter 04 | `chapter-04-geometric-domains-the-5-gs` | 30-67 | 34-71 | Graphs/sets, grids, groups, manifolds/geodesics, gauges/bundles, meshes |
| Chapter 05 | `chapter-05-geometric-deep-learning-models` | 68-101 | 72-105 | CNNs, group CNNs, GNNs, sets/Transformers, E(3) message passing, mesh CNNs, RNN/LSTM |
| Chapter 06 | `chapter-06-problems-and-applications` | 102-113 | 106-117 | Chemistry, proteins, recommenders, traffic, vision, games, language/audio, healthcare, physics, VR/AR |
| Chapter 07 | `chapter-07-historic-perspective` | 114-127 | 118-130 | Symmetry history, architecture lineage, WL, harmonic analysis, geometry processing, algorithmic reasoning |

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Standalone chapter question and motivation.
3. Translation guide from book concepts into computational language.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Generated visual artifacts displayed inline.
8. Applied lab or design exercise.
9. Sanity checks asserting identities, artifact existence, and nonblank visuals.
10. Takeaways.

The setup cell should search upward for a folder containing both
`00-book-index.ipynb` and `utils`, then insert that folder into `sys.path`.

## Artifact Contract

Store generated outputs under:

```text
artifacts/chapter-XX/figures/
artifacts/chapter-XX/html/
artifacts/chapter-XX/checks/
artifacts/chapter-XX/tables/
artifacts/chapter-XX/data/
```

Artifact filenames should name the concept, not the rendering technology.
Repeated placeholder visuals are a QC failure. Every generated artifact should be
displayed inline or linked from the notebook, and final checks should assert that
files exist, are nonempty, and are nonblank when they are images.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed
libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`,
`ipywidgets`, `sympy`, `pandas`, `networkx`, `shapely`, `trimesh`, `pyvista`,
`skimage`, `opencv`, `torch`, `geomstats`, `ripser`, and the rest of the root
geometry stack. This course should not require root dependency changes.

## Worker Boundaries

Assign one worker to one canonical notebook, one helper module, or one script
task. Chapter workers read their assigned source span, design or consume a
visualization storyboard, and edit only their chapter folder, matching artifact
subtree, and explicitly assigned helper module. Index workers own
`00-book-index.ipynb` and chapter `00-index.ipynb` files. QC workers run audits
and validation and report findings.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Geometric-Deep-Learning/scripts/smoke_gdl_stack.py
uv run python -m compileall -q Geometric-Deep-Learning/utils Geometric-Deep-Learning/scripts
uv run python Geometric-Deep-Learning/scripts/build_gdl_course_indexes.py
uv run python Geometric-Deep-Learning/scripts/audit_gdl_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Geometric-Deep-Learning/scripts/audit_gdl_visuals.py
uv run python Geometric-Deep-Learning/scripts/validate_gdl_course.py --limit 4 --timeout 300
uv run python Geometric-Deep-Learning/scripts/validate_gdl_course.py --all --timeout 300
git diff --check
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.
