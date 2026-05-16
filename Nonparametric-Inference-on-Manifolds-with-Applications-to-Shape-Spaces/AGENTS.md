# Agent Instructions: Nonparametric Inference on Manifolds Course

This folder is a standalone visualization-first notebook edition of *Nonparametric Inference on Manifolds with Applications to Shape Spaces* by Abhishek Bhattacharya and Rabi Bhattacharya. Treat this folder as the course root. The workspace root `D:\Geometry` owns the shared `uv` Python environment.

## Repo-Local Skills

Use the repo-local geometry skills under `D:\Geometry\.codex\skills` for course work:

- `geometry-visualization-planner` for source-specific storyboards and artifact choices.
- `geometry-chapter-notebook-author` for canonical chapter or appendix notebooks.
- `geometry-notebook-qc` for standalone, artifact, and execution review.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, exercise text, page screenshots, page crops, or printed figures.
- The notebooks must stand alone without the PDF open.
- Visualization is part of the mathematical argument, not decoration.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, source maps in `inventory/`, and validation tools in `scripts/`.
- Preserve one canonical teaching notebook per chapter or appendix folder plus a local `00-index.ipynb`.
- Generated paths in notebooks must be relative or book-local.
- Prefer the installed geometry stack before adding dependencies.

## Source Map

The PDF has 252 physical pages. Printed page 1 begins on physical PDF page 16, so printed spans below are shifted by +15 for body matter.

- Chapter 01: `part-01-foundations-and-examples/chapter-01-introduction/01-introduction.ipynb`; printed pp. 1-7; PDF pp. 16-22.
- Chapter 02: `part-01-foundations-and-examples/chapter-02-examples/02-examples.ipynb`; printed pp. 8-20; PDF pp. 23-35.
- Chapter 03: `part-01-foundations-and-examples/chapter-03-location-and-spread/03-location-and-spread.ipynb`; printed pp. 21-35; PDF pp. 36-50.
- Chapter 04: `part-01-foundations-and-examples/chapter-04-extrinsic-analysis/04-extrinsic-analysis.ipynb`; printed pp. 36-56; PDF pp. 51-71.
- Chapter 05: `part-01-foundations-and-examples/chapter-05-intrinsic-analysis/05-intrinsic-analysis.ipynb`; printed pp. 57-76; PDF pp. 72-91.
- Chapter 06: `part-02-shape-spaces/chapter-06-landmark-shape-spaces/06-landmark-shape-spaces.ipynb`; printed pp. 77-81; PDF pp. 92-96.
- Chapter 07: `part-02-shape-spaces/chapter-07-kendall-similarity-shapes/07-kendall-similarity-shapes.ipynb`; printed pp. 82-86; PDF pp. 97-101.
- Chapter 08: `part-02-shape-spaces/chapter-08-planar-shape-space/08-planar-shape-space.ipynb`; printed pp. 87-109; PDF pp. 102-124.
- Chapter 09: `part-02-shape-spaces/chapter-09-reflection-shape-spaces/09-reflection-shape-spaces.ipynb`; printed pp. 110-129; PDF pp. 125-144.
- Chapter 10: `part-02-shape-spaces/chapter-10-stiefel-manifolds/10-stiefel-manifolds.ipynb`; printed pp. 130-134; PDF pp. 145-149.
- Chapter 11: `part-02-shape-spaces/chapter-11-affine-shape-spaces/11-affine-shape-spaces.ipynb`; printed pp. 135-146; PDF pp. 150-161.
- Chapter 12: `part-02-shape-spaces/chapter-12-projective-shape-spaces/12-projective-shape-spaces.ipynb`; printed pp. 147-155; PDF pp. 162-170.
- Chapter 13: `part-03-bayes-on-manifolds/chapter-13-bayes-inference/13-bayes-inference.ipynb`; printed pp. 156-181; PDF pp. 171-196.
- Chapter 14: `part-03-bayes-on-manifolds/chapter-14-bayes-regression-classification-testing/14-bayes-regression-classification-testing.ipynb`; printed pp. 182-208; PDF pp. 197-223.
- Appendix A: `part-04-appendices/appendix-a-differentiable-manifolds/appendix-a-differentiable-manifolds.ipynb`; printed pp. 209-213; PDF pp. 224-228.
- Appendix B: `part-04-appendices/appendix-b-riemannian-manifolds/appendix-b-riemannian-manifolds.ipynb`; printed pp. 214-217; PDF pp. 229-232.
- Appendix C: `part-04-appendices/appendix-c-dirichlet-processes/appendix-c-dirichlet-processes.ipynb`; printed pp. 218-224; PDF pp. 233-239.
- Appendix D: `part-04-appendices/appendix-d-parametric-models/appendix-d-parametric-models.ipynb`; printed pp. 225-228; PDF pp. 240-243.

## Notebook Shape

Each canonical notebook should include:

1. Title and source span.
2. Translation guide from book concepts into computational language.
3. Route through the chapter.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations, diagrams, and synthetic examples.
6. Generated visual artifacts displayed near their explanations.
7. Applied lab or design exercise.
8. Sanity checks asserting core identities, generated artifact existence, and numeric invariants.
9. Takeaways.

## Geometry Stack

Use `numpy`, `scipy`, `matplotlib`, `plotly`, `sympy`, `networkx`, `geomstats`, `pyriemann`, and course-local helpers intentionally. Prefer `geomstats` for sphere/geodesic/manifold distance checks and `pyriemann` for SPD manifold examples that make the statistical-manifold analogy concrete.

## Worker Boundaries

Do not edit outside this course folder unless explicitly assigned. Chapter workers should read their assigned source span, consume or update the visualization storyboard, and edit only the assigned chapter folder, its artifact subtree, and any explicitly assigned helper.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts/generate_artifacts.py"
uv run python "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts/build_course_indexes.py"
uv run python -m compileall -q "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/utils" "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts"
uv run python "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts/audit_notebooks.py"
uv run python "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts/audit_visuals.py"
uv run python "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts/audit_artifacts.py"
uv run python "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts/validate_course.py" --limit 3 --timeout 240
git diff --check -- "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces"
```
