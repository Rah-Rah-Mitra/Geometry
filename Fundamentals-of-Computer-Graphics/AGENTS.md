# Agent Instructions: Fundamentals of Computer Graphics Notebook Course

This folder is a standalone visualization-first notebook edition of *Fundamentals
of Computer Graphics*, Fifth Edition, by Steve Marschner and Peter Shirley.
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
- Visualization is part of the explanation. Use diagrams, plots, image
  experiments, interactive HTML, symbolic checks, mesh diagnostics, and
  computational experiments wherever they clarify the chapter.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation
  tools in `scripts/`.
- Every canonical notebook must execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook per chapter folder plus a local
  `00-index.ipynb`.

## Source Map

The PDF has 717 physical pages. Body printed pages map to physical PDF pages by
`pdf_page = printed_page + 17`. The book has 23 chapters, references, and an
index; it does not have formal parts or appendices.

| Unit | Folder | Printed Pages | PDF Pages | Focus |
| --- | --- | ---: | ---: | --- |
| Chapter 01 | `chapter-01-introduction` | 1-12 | 18-29 | Graphics areas, applications, APIs, pipeline thinking, numerical issues, efficiency, and visual debugging. |
| Chapter 02 | `chapter-02-miscellaneous-math` | 13-62 | 30-79 | Sets, mappings, quadratics, vectors, curves, surfaces, interpolation, triangles, probability, and Monte Carlo integration. |
| Chapter 03 | `chapter-03-raster-images` | 63-78 | 80-95 | Raster devices, pixels, RGB color, gamma, quantization, and alpha compositing. |
| Chapter 04 | `chapter-04-ray-tracing` | 79-96 | 96-113 | Ray generation, perspective, ray-object intersections, closest hits, shading inputs, shadows, and reflections. |
| Chapter 05 | `chapter-05-surface-shading` | 97-106 | 114-123 | Point lights, Lambertian diffuse reflection, Blinn-Phong highlights, attenuation, and ambient terms. |
| Chapter 06 | `chapter-06-linear-algebra` | 107-126 | 124-143 | Determinants, matrices, inverses, linear systems, eigenvectors, and matrix diagonalization. |
| Chapter 07 | `chapter-07-transformation-matrices` | 127-156 | 144-173 | 2D and 3D transformations, homogeneous coordinates, inverse transforms, and coordinate frames. |
| Chapter 08 | `chapter-08-viewing` | 157-176 | 174-193 | Viewing transforms, projective transforms, perspective projection, frusta, and field of view. |
| Chapter 09 | `chapter-09-graphics-pipeline` | 177-204 | 194-221 | Rasterization, interpolation, depth buffering, antialiasing, clipping, and culling. |
| Chapter 10 | `chapter-10-signal-processing` | 205-254 | 222-271 | Sampling, convolution, reconstruction filters, image processing, frequency response, and aliasing. |
| Chapter 11 | `chapter-11-texture-mapping` | 255-290 | 272-307 | Texture coordinates, filtering, mipmaps, bump and displacement mapping, shadows, environment maps, and procedural textures. |
| Chapter 12 | `chapter-12-data-structures-for-graphics` | 291-334 | 308-351 | Meshes, scene graphs, spatial structures, BSP trees, and tiled array layouts. |
| Chapter 13 | `chapter-13-sampling` | 335-356 | 352-373 | Probability measures, inverse CDFs, rejection, stratification, lines, disks, spheres, and hemisphere sampling. |
| Chapter 14 | `chapter-14-physics-based-rendering` | 357-382 | 374-399 | Photons, radiometry, Fresnel, refraction, attenuation, BRDFs, the rendering equation, and Monte Carlo path tracing. |
| Chapter 15 | `chapter-15-curves` | 383-428 | 400-445 | Parametric curves, continuity, polynomial pieces, cubics, Bezier curves, B-splines, and NURBS. |
| Chapter 16 | `chapter-16-computer-animation` | 429-460 | 446-477 | Principles of animation, keyframing, deformation, character animation, physics, procedural techniques, and groups. |
| Chapter 17 | `chapter-17-using-graphics-hardware` | 461-502 | 478-519 | GPU pipeline, buffers, state, shaders, vertex arrays, transformations, attributes, textures, meshes, and instancing. |
| Chapter 18 | `chapter-18-color` | 503-524 | 520-541 | Colorimetry, color spaces, chromatic adaptation, color appearance, and perceptual distances. |
| Chapter 19 | `chapter-19-visual-perception` | 525-568 | 542-585 | Sensitivity, spatial vision, depth cues, motion, object perception, and picture perception. |
| Chapter 20 | `chapter-20-tone-reproduction` | 569-594 | 586-611 | Dynamic range, tone curves, image formation, frequency, gradient, spatial, sigmoid, and night tone mapping operators. |
| Chapter 21 | `chapter-21-implicit-modeling` | 595-622 | 612-639 | Implicit fields, skeletal primitives, blending, rendering, partitioning, CSG, warping, and BlobTrees. |
| Chapter 22 | `chapter-22-computer-graphics-in-games` | 623-644 | 640-661 | Platform constraints, limited resources, optimization, game types, and production workflows. |
| Chapter 23 | `chapter-23-visualization` | 645-680 | 662-697 | Data and task abstraction, visual encoding, interaction, composition, reduction, and visualization examples. |

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
files exist and are nonempty.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed
libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`,
`ipywidgets`, `sympy`, `pandas`, `networkx`, `shapely`, `trimesh`, `pyvista`,
`skimage`, `opencv`, and the rest of the root geometry stack. This course should
not require root dependency changes.

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
uv run python "Fundamentals of Computer Graphics/scripts/build_fcg_course_indexes.py"
uv run python -m compileall -q "Fundamentals of Computer Graphics/utils" "Fundamentals of Computer Graphics/scripts"
uv run python "Fundamentals of Computer Graphics/scripts/audit_fcg_notebooks.py" --min-words 1200 --min-code-cells 5
uv run python "Fundamentals of Computer Graphics/scripts/audit_fcg_visuals.py"
uv run python "Fundamentals of Computer Graphics/scripts/validate_fcg_course.py" --limit 8 --timeout 300
git diff --check
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes. If shared utilities
or setup cells change late, also run:

```powershell
uv run python "Fundamentals of Computer Graphics/scripts/validate_fcg_course.py" --all --timeout 300
```

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
