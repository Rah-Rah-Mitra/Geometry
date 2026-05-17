# Agent Instructions: Riemannian Geometry Notebook Course

This folder is a standalone visualization-first notebook edition of *Riemannian Geometry*. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or figures.
- Use the source only for title, chapter structure, page spans, terminology, definitions, theorem orientation, and concept coverage.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualizations are part of the explanation.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.

## Source Map

Source files: `Riemannian Geometry.pdf`.

Extraction method: rendered image-page TOC inspection; text extraction is image-only.

| Unit | Folder | Printed Pages | Focus |
| --- | --- | ---: | --- |
| Chapter 0 | `chapter-00-differentiable-manifolds` | 1-34 | Differentiable manifolds, tangent spaces, immersions, embeddings, examples, orientation, vector fields, brackets, and topology. |
| Chapter 1 | `chapter-01-riemannian-metrics` | 35-47 | Riemannian metrics, length, distance, and basic metric structures on manifolds. |
| Chapter 2 | `chapter-02-affine-connections-riemannian-connections` | 48-59 | Affine connections, Riemannian connections, covariant derivatives, torsion, and compatibility. |
| Chapter 3 | `chapter-03-geodesics-convex-neighborhoods` | 60-87 | Geodesic flow, minimizing properties, exponential map, and convex neighborhoods. |
| Chapter 4 | `chapter-04-curvature` | 88-109 | Curvature tensor, sectional curvature, Ricci curvature, scalar curvature, and tensors on Riemannian manifolds. |
| Chapter 5 | `chapter-05-jacobi-fields` | 110-123 | Jacobi equation, conjugate points, and variation fields. |
| Chapter 6 | `chapter-06-isometric-immersions` | 124-143 | Second fundamental form, fundamental equations, and immersion geometry. |
| Chapter 7 | `chapter-07-complete-manifolds-hopf-rinow-and-hadamard-theorems` | 144-154 | Completeness, Hopf-Rinow theorem, Hadamard theorem, and global consequences. |
| Chapter 8 | `chapter-08-spaces-of-constant-curvature` | 155-190 | Cartan metric determination, hyperbolic space, space forms, and hyperbolic isometries. |
| Chapter 9 | `chapter-09-variations-of-energy` | 191-209 | First and second variation of energy, Bonnet-Myers theorem, and Synge-Weinstein theorem. |
| Chapter 10 | `chapter-10-the-rauch-comparison-theorem` | 210-241 | Rauch theorem, index lemma applications, focal points, and comparison extensions. |
| Chapter 11 | `chapter-11-the-morse-index-theorem` | 242-252 | Index form, index theorem, and geodesic variation structure. |
| Chapter 12 | `chapter-12-the-fundamental-group-of-manifolds-of-negative` | 253-264 | Closed geodesics, Preissmann theorem, and topology of negative curvature. |
| Chapter 13 | `chapter-13-the-sphere-theorem` | 265-285 | Cut locus, injectivity radius estimates, sphere theorem, and further developments. |

Backmatter notes: references 292-296; index 297-315.

## Notebook Shape

Each canonical notebook should contain title and source span, standalone goal, translation guide, setup cell, chapter-specific library routing, original concept sections, generated visual artifacts displayed inline, proof/invariant/counterexample scaffolds, applied lab, final sanity checks, and takeaways.

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Riemannian-Geometry/scripts/build_rg_course_indexes.py
uv run python -m compileall -q Riemannian-Geometry/utils Riemannian-Geometry/scripts
uv run python Riemannian-Geometry/scripts/audit_rg_notebooks.py --min-words 900 --min-code-cells 5
uv run python Riemannian-Geometry/scripts/audit_rg_visuals.py
uv run python Riemannian-Geometry/scripts/validate_rg_course.py --limit 4 --timeout 300
git diff --check -- Riemannian-Geometry
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, and reproducible artifact checks, but they must not replace chapter-specific exposition and visible notebook computations.
