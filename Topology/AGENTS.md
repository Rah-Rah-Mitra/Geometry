# Agent Instructions: Topology Notebook Course

This folder is a standalone visualization-first notebook edition of *Topology*, Second Edition, by James Munkres.
Treat this folder as the project root for this course. The workspace root owns the shared `uv`
environment, `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, or page crops.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualizations are part of the explanation. Use diagrams, plots, graph views, widgets or HTML labs,
  symbolic checks, computational experiments, proof-state diagrams, and mesh/surface views wherever they clarify the topology.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.

## Course Structure

```text
Topology/
  00-book-index.ipynb
  AGENTS.md
  artifacts/
  scripts/
  utils/
  chapter-01-set-theory-and-logic/
  ...
  chapter-13-classification-of-covering-spaces/
```

Each chapter folder contains:

```text
00-index.ipynb
<canonical notebook>.ipynb
```

There should be exactly one canonical teaching notebook in each folder, excluding `00-index.ipynb`.

## Source Map

The source PDF is `Topology.pdf`, a Pearson custom-library PDF created with imposition. Do not assume
physical PDF pages match printed-page order. Use `scripts/topology_inventory.py` and the printed page
spans below for source orientation. The custom PDF table places Chapter 13 before Chapter 12, but this
course follows logical Munkres section order: Chapter 12 surfaces, then Chapter 13 covering spaces.

| Unit | Folder | Printed Pages | Sections | Focus |
| --- | --- | ---: | --- | --- |
| Chapter 1 | `chapter-01-set-theory-and-logic` | 1-72 | §§1-11 | sets, functions, relations, countability, choice, and well-ordering. |
| Chapter 2 | `chapter-02-topological-spaces-and-continuous-functions` | 73-144 | §§12-22 | bases, product topology, subspaces, quotient topology, and continuity. |
| Chapter 3 | `chapter-03-connectedness-and-compactness` | 145-186 | §§23-29 | connected spaces, compact spaces, limit-point compactness, local compactness, and nets. |
| Chapter 4 | `chapter-04-countability-and-separation-axioms` | 187-227 | §§30-36 | countability axioms, separation axioms, normal spaces, Urysohn's lemma, Tietze extension, and embeddings. |
| Chapter 5 | `chapter-05-the-tychonoff-theorem` | 228-240 | §§37-38 | products of compact spaces and Stone-Cech compactification. |
| Chapter 6 | `chapter-06-metrization-theorems-and-paracompactness` | 241-260 | §§39-42 | local finiteness, Nagata-Smirnov metrization, Smirnov metrization, and paracompactness. |
| Chapter 7 | `chapter-07-complete-metric-spaces-and-function-spaces` | 261-291 | §§43-47 | complete metric spaces, space-filling curves, compactness in metric spaces, compact convergence, and Ascoli's theorem. |
| Chapter 8 | `chapter-08-baire-spaces-and-dimension-theory` | 292-316 | §§48-50 | Baire spaces, nowhere-differentiable functions, and dimension theory. |
| Chapter 9 | `chapter-09-the-fundamental-group` | 317-371 | §§51-60 | path homotopy, the fundamental group, covering spaces, the circle, retractions, fixed points, and surface groups. |
| Chapter 10 | `chapter-10-separation-theorems-in-the-plane` | 372-402 | §§61-66 | Jordan separation, invariance of domain, plane graph embeddings, winding number, and Cauchy integral formula. |
| Chapter 11 | `chapter-11-the-seifert-van-kampen-theorem` | 403-442 | §§67-73 | direct sums, free products, free groups, Seifert-van Kampen, wedges of circles, adjoining two-cells, and group presentations. |
| Chapter 12 | `chapter-12-classification-of-surfaces` | 468-498 | §§74-78 | surface homology, cutting and pasting, polygon schemas, classification, and constructing compact surfaces. |
| Chapter 13 | `chapter-13-classification-of-covering-spaces` | 443-467 | §§79-82 | equivalence of covering spaces, universal covers, covering transformations, and existence/classification. |

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

## Artifact Contract

Store generated outputs under:

```text
artifacts/chapter-XX/figures/
artifacts/chapter-XX/html/
artifacts/chapter-XX/checks/
artifacts/chapter-XX/tables/
```

Artifact filenames should name the concept, not the rendering technology. Repeated placeholder visuals
are a QC failure. Every generated artifact should be displayed inline or linked from the notebook, and
final checks should assert that files exist and are nonempty.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding
dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `pandas`,
`networkx`, `shapely`, `trimesh`, `pyvista`, `ripser`, `gudhi`, and the rest of the root geometry stack.
This course currently needs no dependency additions.

## Worker Boundaries

Assign one worker to one canonical notebook, one helper module, or one script task.
Chapter workers may edit only their chapter folder, matching artifact subtree, and explicitly
assigned helper module. Index workers own `00-book-index.ipynb` and `00-index.ipynb` files.
QC workers run audits and validation and report findings.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Topology/scripts/build_topology_course_indexes.py
uv run python -m compileall -q Topology/utils Topology/scripts
uv run python Topology/scripts/audit_topology_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Topology/scripts/audit_topology_visuals.py
uv run python Topology/scripts/validate_topology_course.py --limit 4 --timeout 300
git diff --check
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Geometry visualization library policy

Use the installed geometry stack intentionally. Do not default to generic Matplotlib-only notebooks when the chapter’s geometry calls for richer representations.

### Library routing

- Use Matplotlib for durable 2D diagrams, proof sketches, constructions, incidence, orientation, area, angle, curves, and labeled static figures.
- Use Plotly for interactive 2D/3D parameter exploration, transformations, surfaces, and standalone HTML artifacts.
- Use ipywidgets/ipympl when parameter variation is central to understanding the concept.
- Use PyVista, VTK, Trimesh, and MeshIO for 3D surfaces, meshes, normals, curvature, polyhedra, frames, slicing, and spatial inspection.
- Use gpytoolbox, potpourri3d, robust_laplacian, manifold3d, and xatlas for mesh Laplacians, geodesics, parameterization, remeshing, and surface diagnostics.
- Use SymPy for exact symbolic checks, coordinate transformations, polynomial identities, and derivations.
- Use Galgebra, Clifford, Kingdon, and PyGanja for exterior algebra, geometric algebra, rotors, bivectors, conformal/projective models, and algebraic proof experiments.
- Use Gudhi, Ripser, and Persim for topology, filtrations, simplicial complexes, persistent homology, and persistence diagrams.
- Use Geomstats and PyRiemann for manifolds, geodesics, metrics, curvature intuition, SPD geometry, and statistical geometry.
- Use Shapely, scipy.spatial, and NetworkX for computational geometry, intersections, Voronoi/Delaunay, arrangements, graph structures, and proof dependency diagrams.
- Use OpenCV, Kornia, Torch, Torchvision, scikit-image, and Pillow for projective geometry, homographies, epipolar geometry, image geometry, camera models, and transformation experiments.
- Use POT and GeomLoss for optimal transport, Wasserstein geometry, barycenters, and metric geometry of distributions.
- Use GIS libraries only when geographic geometry clarifies the chapter.

### Visual justification rule

Every major visualization must have:

1. the concept it teaches,
2. the reason this representation was chosen,
3. an inspection target for the learner,
4. a nearby prose explanation,
5. a check, invariant, or sanity test where practical.

Decorative visuals are not acceptable.

### Notebook-first rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact creation, but they must not mass-populate chapter notebooks with generic teaching cells.
