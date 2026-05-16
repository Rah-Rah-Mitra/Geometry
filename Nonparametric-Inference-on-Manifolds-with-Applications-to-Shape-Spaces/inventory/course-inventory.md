# Course Inventory

This fresh course build contains one source PDF, one root index, part indexes, canonical notebooks for fourteen chapters and four appendices, local utilities, generated artifacts, and validation scripts.

## Top-level map

- `00-book-index.ipynb`: course entry and validation command map.
- `AGENTS.md`: worker boundaries, source spans, notebook shape, and command list.
- `inventory/`: source map, visual storyboards, and inventory.
- `utils/`: course-local helpers for artifacts, manifold statistics, and shape-space computations.
- `scripts/`: artifact generation, index building, audits, and notebook execution validation.
- `artifacts/`: generated PNG/HTML visuals plus JSON checks for each unit.

## Canonical notebooks

- `part-01-foundations-and-examples/chapter-01-introduction/01-introduction.ipynb`: Why landmark data lead to quotient manifolds and why Frechet means are the main statistical object.
- `part-01-foundations-and-examples/chapter-02-examples/02-examples.ipynb`: A visual gallery of directional and shape-data examples that will reappear as computational laboratories.
- `part-01-foundations-and-examples/chapter-03-location-and-spread/03-location-and-spread.ipynb`: Frechet functions, metric variation, sample means, and asymptotic behavior before smooth structure is assumed.
- `part-01-foundations-and-examples/chapter-04-extrinsic-analysis/04-extrinsic-analysis.ipynb`: Embedding a manifold, averaging in the ambient space, and projecting back with tangent covariance diagnostics.
- `part-01-foundations-and-examples/chapter-05-intrinsic-analysis/05-intrinsic-analysis.ipynb`: Geodesic-distance Frechet means, log-map coordinates, cut-locus caveats, and bootstrap inference on spheres.
- `part-02-shape-spaces/chapter-06-landmark-shape-spaces/06-landmark-shape-spaces.ipynb`: The landmark pipeline from labeled configurations to quotient spaces under increasingly large transformation groups.
- `part-02-shape-spaces/chapter-07-kendall-similarity-shapes/07-kendall-similarity-shapes.ipynb`: Preshape spheres, rotation quotients, horizontal directions, and geodesic distance on similarity shapes.
- `part-02-shape-spaces/chapter-08-planar-shape-space/08-planar-shape-space.ipynb`: Complex projective planar shape space, intrinsic and extrinsic means, size-and-shape, and two-sample inference.
- `part-02-shape-spaces/chapter-09-reflection-shape-spaces/09-reflection-shape-spaces.ipynb`: Reflection invariance as an unoriented quotient and extrinsic analysis through Gram-style representations.
- `part-02-shape-spaces/chapter-10-stiefel-manifolds/10-stiefel-manifolds.ipynb`: Orthogonal frames as manifold data, projection onto Stiefel constraints, and extrinsic mean diagnostics.
- `part-02-shape-spaces/chapter-11-affine-shape-spaces/11-affine-shape-spaces.ipynb`: Affine normalization, rank conditions, and digit-like landmark examples where similarity information is intentionally discarded.
- `part-02-shape-spaces/chapter-12-projective-shape-spaces/12-projective-shape-spaces.ipynb`: Projective points as lines through the origin, antipodal quotients, and extrinsic analysis on real projective space.
- `part-03-bayes-on-manifolds/chapter-13-bayes-inference/13-bayes-inference.ipynb`: Density estimation, posterior consistency intuition, and manifold mixture computation with spherical and SPD examples.
- `part-03-bayes-on-manifolds/chapter-14-bayes-regression-classification-testing/14-bayes-regression-classification-testing.ipynb`: Mixture-of-kernels regression, classification probabilities, and posterior testing as geometry-aware predictive workflows.
- `part-04-appendices/appendix-a-differentiable-manifolds/appendix-a-differentiable-manifolds.ipynb`: An executable atlas for charts, tangent vectors, immersions, submersions, and quotient-map intuition.
- `part-04-appendices/appendix-b-riemannian-manifolds/appendix-b-riemannian-manifolds.ipynb`: Metrics, geodesics, exponential and logarithm maps, curvature intuition, and SPD comparison checks.
- `part-04-appendices/appendix-c-dirichlet-processes/appendix-c-dirichlet-processes.ipynb`: Stick-breaking, Polya urns, random discrete measures, and why DP mixtures adapt to manifold support.
- `part-04-appendices/appendix-d-parametric-models/appendix-d-parametric-models.ipynb`: Parametric sphere and planar-shape models used as baselines for the nonparametric methods.
