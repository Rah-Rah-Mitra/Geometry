# Agent Instructions: Geometric Algebra For Computer Science Notebook Course

This folder is a standalone notebook edition of *Geometric Algebra for Computer Science*.
Agents working here should treat the book folder as the project root for this course:

```text
Geometric-Algebra-for-Computer-Science/
  00-book-index.ipynb
  AGENTS.md
  artifacts/
  scripts/
  utils/
  part-01-geometric-algebra/
  part-02-models-of-geometry/
  part-03-implementation/
  part-04-appendices/
```

The workspace root still owns shared environment files such as `pyproject.toml`,
`uv.lock`, and `.venv`. Run commands from the workspace root unless a script says
otherwise.

## Repo-Local Skills

This workspace includes repo-local Codex skills under `D:\Geometry\.codex\skills`.
Use them when assigning or doing chapter work:

- `geometry-visualization-planner`: create a visual storyboard and library choices
  before notebook authoring.
- `geometry-chapter-notebook-author`: author or revise a standalone visual-first
  chapter notebook directly in its chapter folder.
- `geometry-notebook-qc`: review notebooks, artifacts, execution, and visual
  relevance before handoff.

When using parallel agents, pass the relevant skill path and the assigned chapter or
page span to each worker. The skills contain the shared geometry library catalog.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations. Do not
  copy textbook passages, long exercise text, or page screenshots.
- A notebook should be useful without opening the textbook: explain the motivation,
  definitions, worked examples, pitfalls, checks, and takeaways.
- Visualization is part of delivery, not a decoration or quota. Use diagrams, 3D
  plots, widgets, symbolic checks, mesh/surface views, proof diagrams, and
  computational experiments wherever they clarify the chapter's geometry.
- Keep course-owned helpers in `utils/`, course-owned outputs in `artifacts/`, and
  course-owned build/validation tools in `scripts/`.
- Every canonical notebook must execute cleanly with `nbclient`.
- Generated paths in notebooks should be relative or book-local. Avoid hardcoded
  workspace paths such as `D:/Geometry/artifacts`.
- Preserve the existing folder hierarchy and notebook names unless the user asks for
  a structural migration.
- Chapter workers must read the assigned source pages before editing and should
  author the full canonical notebook directly rather than driving chapter work from a
  large course-generation script.

## Book Map

Use the table of contents as the authoritative structure:

| Part | Folder | Coverage |
| --- | --- | --- |
| I | `part-01-geometric-algebra` | Chapters 1-8: foundations of blades, products, transformations, and differentiation |
| II | `part-02-models-of-geometry` | Chapters 9-17: vector-space, homogeneous, Plucker, and conformal models |
| III | `part-03-implementation` | Chapters 18-23: implementation strategies, algorithms, specialization, and ray tracing |
| IV | `part-04-appendices` | Appendices A-D: metrics, contractions, retrieved products, and formula catalog |

Each chapter or appendix folder should contain:

```text
00-index.ipynb
<canonical chapter-or-appendix notebook>.ipynb
```

There should be exactly one canonical teaching notebook per chapter or appendix
folder, excluding `00-index.ipynb`. Keep generated notebooks under `artifacts/`, not
beside canonical notebooks.

## Notebook Shape

Follow the seed style used by Chapter 1:

1. Title and chapter idea.
2. Translation guide from textbook concepts into computational language.
3. Route through the chapter.
4. Imports and setup cell that discovers `BOOK_ROOT`.
5. Concept sections with original explanations and equations.
6. Executable examples using `utils/` helpers and local functions.
7. Visual explanations and executable artifacts: diagrams, plots, 3D scenes,
   widgets, symbolic derivations, tables, or computational experiments as the
   concepts require.
8. Applied lab or design exercise.
9. Sanity checks that assert important identities and artifact existence.
10. Chapter takeaways.

The setup cell should search upward for a folder containing both
`00-book-index.ipynb` and `utils`, then insert that folder into `sys.path`:

```python
from pathlib import Path
import sys

BOOK_ROOT = Path.cwd()
for candidate in [BOOK_ROOT, *BOOK_ROOT.parents]:
    if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
        BOOK_ROOT = candidate
        break
else:
    raise RuntimeError("Could not find the GA book root")

if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

ARTIFACT_ROOT = BOOK_ROOT / "artifacts" / "chapter-XX"
ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
```

## Artifacts

Artifacts are part of the learning product. Store them under stable chapter or
appendix paths:

```text
artifacts/chapter-XX/checks/
artifacts/chapter-XX/figures/
artifacts/chapter-XX/plots/
artifacts/chapter-XX/tables/
artifacts/appendices/appendix-a/
```

Rules:

- Write checks as JSON or CSV when they summarize reproducible invariants.
- Write interactive visuals as HTML and static visuals as PNG/SVG.
- Reference artifacts in prose using paths such as `artifacts/chapter-13/...`.
- Do not store large scans or copyrighted page images.
- If a notebook generates an artifact, include a final assertion that the file exists.

## Visualization-First Contract

Canonical notebooks should use visual and computational forms wherever they improve
the delivery of the geometry. The standard is not a fixed count; the standard is
whether the notebook can stand alone as a clearer learning product than a passive
textbook reading.

Visuals are part of the teaching argument:

- The artifact filename must name the concept, for example
  `outer-product-orientation.png`, not `figure.png`.
- The notebook prose near the visual must name the concept, parameters, and the
  invariant or behavior the reader should inspect.
- Final sanity checks must assert the visual path exists, has nonzero size, and
  records relevant numeric validation values when the notebook has a final check
  artifact.
- Repeated placeholder visuals are forbidden. A repeated artifact hash is a QC
  failure unless the exact file is intentionally allowlisted in an audit.
- Make the geometry inspectable with labels, meaningful scale/aspect ratio, and
  legends when multiple objects overlap.
- Use color and styling to clarify structure; do not rely on hue alone for meaning.
- Do not use textbook screenshots, PDF page crops, or decorative images that do
  not express chapter content.
- For proof-heavy material, visualize the proof state where possible: assumptions,
  dependencies, limiting processes, deformations, counterexamples, orientation
  changes, or small symbolic/numeric examples that make the invariant visible.
- Use interactive Plotly, ipywidgets, PyVista, Trimesh, or other installed tools when
  changing a parameter, rotating a model, or inspecting a surface teaches the idea.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed libraries
before adding dependencies:

| Use case | Installed libraries |
| --- | --- |
| General plotting | `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `ipympl`, `pandas`, `polars`, `seaborn` |
| 3D surfaces and meshes | `pyvista`, `trimesh`, `meshio`, `gpytoolbox`, `manifold3d`, `potpourri3d`, `robust_laplacian`, `mapbox_earcut`, `xatlas`, `trame` |
| Computational geometry | `scipy.spatial`, `shapely`, `networkx` |
| Symbolic geometry | `sympy`, `galgebra` |
| Geometric algebra | `kingdon`, `clifford`, `galgebra`, `pyganja`, course-local `utils.ga` |
| Computer vision | `cv2` from `opencv-contrib-python`, `skimage`, `kornia`, `torch`, `torchvision` |
| Riemannian/statistical geometry | `geomstats`, `pyriemann` |
| Optimal transport | `ot` from POT, `geomloss` |
| Topological data analysis | `ripser`, `gudhi`, `persim` |
| GIS/geometric maps | `geopandas`, `rasterio`, `fiona`, `pyproj`, `pyogrio`, `osmnx`, `contextily`, `folium`, `pydeck` |

Document these as optional/external rather than importing them in canonical
notebooks: `open3d` is not available for the current CPython 3.13 environment,
`meshplot` and `singular` do not resolve from the package registry here, and
SageMath/Singular require an external Sage/Singular installation.

## Utilities

Shared code belongs in `utils/`.

- Core algebra primitives live in `utils/ga/`.
- Chapter-specific helpers use names such as `utils/chapter13_conformal.py`.
- Keep helper APIs inspectable and small enough for learners to read.
- Prefer local helpers over new dependencies unless the user explicitly approves a
  dependency change.
- If a helper changes a contract used by multiple notebooks, run the full validation
  suite.

## Worker Boundaries

For parallel work, assign one worker to one canonical notebook or one clearly bounded
script/helper task.

Workers must:

- Read the relevant chapter/page span before editing.
- If assigned chapter work, design or consume a visualization storyboard and then
  author the full canonical notebook directly in the chapter folder.
- Write only inside their assigned chapter folder, its matching `artifacts/` subtree,
  and any explicitly assigned helper module.
- Avoid editing global indexes unless assigned to the index/QC worker.
- Avoid editing shared `utils/ga/` unless assigned to the core utility worker.
- Avoid using `generate_ga_course.py` for chapter-level improvement work unless the
  assignment is explicitly a bootstrap or regeneration task.
- Report changed files, generated artifacts, checks run, and any residual gaps.

Suggested worker roles:

- Visualization planner: reads the source span and proposes the visual storyboard.
- Chapter worker: authors one canonical notebook and local artifacts.
- Utility worker: implements shared algebra/model helpers and tests.
- Dependency/library worker: checks installed packages and recommends compatible
  tools for chapter visuals.
- Index worker: regenerates `00-book-index.ipynb` and part indexes.
- QC worker: runs audits, validates links, executes notebooks, and checks stale paths.

## Script Commands

Run these from `D:\Geometry`:

```powershell
uv run python Geometric-Algebra-for-Computer-Science/scripts/build_ga_course_indexes.py
uv run python Geometric-Algebra-for-Computer-Science/scripts/smoke_geometry_stack.py
uv run python -m compileall -q Geometric-Algebra-for-Computer-Science/utils Geometric-Algebra-for-Computer-Science/scripts
uv run pytest -q
uv run python Geometric-Algebra-for-Computer-Science/scripts/audit_ga_notebooks.py --min-words 1000 --min-code-cells 5
uv run python Geometric-Algebra-for-Computer-Science/scripts/validate_ga_course.py --limit 8 --timeout 300
uv run python Geometric-Algebra-for-Computer-Science/scripts/validate_ga_course.py --all --timeout 300
git diff --check
```

`validate_ga_course.py` may print Windows ZMQ shutdown warnings after a successful
run. Treat the command exit code and the final `Executed ... notebooks successfully`
line as the source of truth.

## Static Checks Before Commit

Before committing, verify:

- No root-level `utils/`, `artifacts/`, or book-specific `scripts/` directory has
  reappeared.
- No notebook or script contains stale root artifact/helper paths.
- Every chapter and appendix folder has one canonical notebook plus `00-index.ipynb`.
- Markdown links resolve for local notebook, helper, JSON, CSV, PNG, HTML, and text
  references.
- No PDF files are staged.

Useful stale-path patterns:

```text
D:/Geometry/artifacts
D:\Geometry\artifacts
/mnt/d/Geometry/artifacts
D:/Geometry/utils
D:\Geometry\utils
/mnt/d/Geometry/utils
D:/Geometry/scripts
D:\Geometry\scripts
/mnt/d/Geometry/scripts
```

## Reusing This Pattern For Other Books

For a new book, create a sibling folder with the same ownership model:

```text
Book-Slug/
  00-book-index.ipynb
  AGENTS.md
  artifacts/
  scripts/
  utils/
  part-or-chapter-folders/
```

Then copy this file, replace the contents map, update script names, and keep that
book's helpers and artifacts inside the book folder. The root environment can remain
shared across books.
