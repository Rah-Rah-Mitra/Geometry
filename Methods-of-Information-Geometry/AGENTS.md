# Agent Instructions: Methods of Information Geometry Notebook Course

This folder is a standalone visualization-first notebook edition of Shun-ichi Amari and Hiroshi Nagaoka's *Methods of Information Geometry*. Treat this folder as the course root. The workspace root `D:\Geometry` owns the shared `uv` Python environment.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills` for course work:

- `geometry-visualization-planner` for chapter storyboards and artifact choices.
- `geometry-chapter-notebook-author` for authoring canonical notebooks.
- `geometry-notebook-qc` for standalone, artifact, and execution review.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, printed tables, page screenshots, or page crops.
- Use the DjVu text layer only for orientation, source spans, terminology, and coverage checks.
- The notebooks must stand alone without the DjVu open.
- Visualization is part of the teaching argument, not decoration.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, source inventory under `source/`, and validation tools in `scripts/`.
- Every canonical chapter notebook should execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook per chapter folder plus a local `00-index.ipynb`.

## Extraction Path

The local source file is `Methods of Information Geometry.djvu`. No system DjVuLibre tools were available when this course was initialized, so this folder vendors a read-only extractor at `vendor/djvu_text_extractor`. It uses the pure-Rust `djvu-rs` DjVu/BZZ implementation to read bundled `DJVM` pages, decode `TXTz` text chunks, and emit page text plus a manifest under `source/djvu_text/`.

Re-run extraction from the course root:

```powershell
$env:CARGO_TARGET_DIR='D:\Geometry\Methods-of-Information-Geometry\.cargo-target'
cargo run --manifest-path vendor\djvu_text_extractor\Cargo.toml -- "Methods of Information Geometry.djvu" source\djvu_text
```

Or use the wrapper:

```powershell
uv run python "Methods-of-Information-Geometry/scripts/extract_djvu_text.py"
```

The source has 216 physical DjVu pages. The text layer has no NAVM bookmark table. Physical page 10 is printed page 1, so main-matter printed page `p` corresponds to physical DjVu page `p + 9`.

## Source Map

The extracted contents give 8 chapters and no appendices.

- Chapter 01: `chapter-01-elementary-differential-geometry/01-elementary-differential-geometry.ipynb`; printed pp. 1-24; physical pp. 10-33; differentiable manifolds, tangent vectors, tensor fields, submanifolds, Riemannian metrics, affine connections, flatness, autoparallel submanifolds, projected connections, embedding curvature, and the Riemannian connection.
- Chapter 02: `chapter-02-geometric-structure-of-statistical-models/02-geometric-structure-of-statistical-models.ipynb`; printed pp. 25-50; physical pp. 34-59; statistical models, Fisher metric, alpha-connection, Chentsov invariance, finite probability simplex geometry, alpha-affine manifolds, and alpha-families.
- Chapter 03: `chapter-03-dual-connections/03-dual-connections.ipynb`; printed pp. 51-80; physical pp. 60-89; dual affine connections, divergences as contrast functions, dually flat spaces, canonical divergence, exponential-family duality, alpha-affine duality, mutually dual foliations, and the triangular relation.
- Chapter 04: `chapter-04-statistical-inference-and-differential-geometry/04-statistical-inference-and-differential-geometry.ipynb`; printed pp. 81-114; physical pp. 90-123; independent-observation inference, exponential families and observed points, curved exponential families, consistency, first-order efficiency, higher-order estimation and testing, Fisher-information asymptotics, estimating functions, and fiber-bundle viewpoints.
- Chapter 05: `chapter-05-geometry-of-time-series-and-linear-systems/05-geometry-of-time-series-and-linear-systems.ipynb`; printed pp. 115-132; physical pp. 124-141; system and time-series spaces, Fisher metric and alpha-connection on system space, finite-dimensional model geometry, stable systems, and stable feedback.
- Chapter 06: `chapter-06-multiterminal-information-theory/06-multiterminal-information-theory.ipynb`; printed pp. 133-144; physical pp. 142-153; multiterminal information, zero-rate testing, zero-rate estimation, and inference for general multiterminal information.
- Chapter 07: `chapter-07-information-geometry-for-quantum-systems/07-information-geometry-for-quantum-systems.ipynb`; printed pp. 145-166; physical pp. 154-175; quantum state space, geometry from quantum divergences, geometry from generalized covariance, and quantum estimation.
- Chapter 08: `chapter-08-miscellaneous-topics/08-miscellaneous-topics.ipynb`; printed pp. 167-180; physical pp. 176-189; convex analysis, linear programming, gradient flows, neuro-manifolds, nonlinear systems, Lie groups, transformation models, and open problems in information geometry.

Supplementary source spans:

- Guide to the Bibliography: printed pp. 181-186; physical pp. 190-195.
- Bibliography: printed pp. 187-202; physical pp. 196-211.
- Index: printed pp. 203-206; physical pp. 212-215.

## Notebook Shape

Each canonical notebook should include:

1. Title and source span.
2. Translation guide from book concepts into computational language.
3. Route through the chapter.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Visual artifacts saved under `artifacts/` and displayed inline or linked.
8. Applied lab or design exercise.
9. Sanity checks asserting core identities and artifact existence.
10. Takeaways.

## Geometry Stack

Use the shared `uv` environment at `D:\Geometry`. Prefer installed packages before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `sympy`, `networkx`, `PIL`, and the other packages listed in the repo-local geometry library catalog. For this course, the core statistical-manifold visuals should prioritize Fisher metrics, alpha geometry, divergences, dually flat coordinates, exponential families, simplex geometry, time-series spectra, multiterminal information, and quantum state geometry.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python "Methods-of-Information-Geometry/scripts/build_mig_course_indexes.py"
uv run python -m compileall -q "Methods-of-Information-Geometry/utils" "Methods-of-Information-Geometry/scripts"
uv run python "Methods-of-Information-Geometry/scripts/audit_mig_notebooks.py" --min-words 800 --min-code-cells 4
uv run python "Methods-of-Information-Geometry/scripts/audit_mig_visuals.py"
uv run python "Methods-of-Information-Geometry/scripts/audit_mig_artifacts.py"
uv run python "Methods-of-Information-Geometry/scripts/validate_mig_course.py" --limit 3 --timeout 240 --include-indexes
git diff --check
```

## Worker Boundaries

Workers should edit only this folder unless explicitly assigned shared repository work. Do not revert or rewrite changes from other course workers. Shared utilities, extraction scripts, and audits in this folder are part of this course foundation.

