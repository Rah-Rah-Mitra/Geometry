# Visualization Storyboards

Each unit has source-specific visual artifacts, library routing, and checks. All visuals are generated from synthetic data or exact constructions; no textbook image is copied.

## 01. Introduction

- chapter goal: Why landmark data lead to quotient manifolds and why Frechet means are the main statistical object.
- source span read: printed pp. 1-7; PDF pp. 16-22.
- concept inventory: landmarks, transformation groups, extrinsic versus intrinsic distance, two-sample mean testing.
- library routing: matplotlib, networkx.
- visual sequence: `shape-inference-roadmap.png` then `quotient-ladder.png`.
- artifact plan: `artifacts/chapter-01/figures`, optional `artifacts/chapter-01/interactive`, and `artifacts/chapter-01/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## 02. Examples

- chapter goal: A visual gallery of directional and shape-data examples that will reappear as computational laboratories.
- source span read: printed pp. 8-20; PDF pp. 23-35.
- concept inventory: circle data, sphere data, planar shapes, affine shapes, reflection shapes.
- library routing: matplotlib, plotly.
- visual sequence: `application-gallery.png` then `sphere-observations.html`.
- artifact plan: `artifacts/chapter-02/figures`, optional `artifacts/chapter-02/interactive`, and `artifacts/chapter-02/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## 03. Location and spread on metric spaces

- chapter goal: Frechet functions, metric variation, sample means, and asymptotic behavior before smooth structure is assumed.
- source span read: printed pp. 21-35; PDF pp. 36-50.
- concept inventory: Frechet function, metric variation, sample mean set, circle example, bootstrap.
- library routing: numpy, scipy, matplotlib.
- visual sequence: `metric-frechet-landscape.png` then `circle-bootstrap-bands.png`.
- artifact plan: `artifacts/chapter-03/figures`, optional `artifacts/chapter-03/interactive`, and `artifacts/chapter-03/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## 04. Extrinsic analysis on manifolds

- chapter goal: Embedding a manifold, averaging in the ambient space, and projecting back with tangent covariance diagnostics.
- source span read: printed pp. 36-56; PDF pp. 51-71.
- concept inventory: embedding, projection, extrinsic mean, extrinsic covariance, equivariance.
- library routing: geomstats, matplotlib, numpy.
- visual sequence: `sphere-extrinsic-projection.png` then `extrinsic-covariance-ellipse.png`.
- artifact plan: `artifacts/chapter-04/figures`, optional `artifacts/chapter-04/interactive`, and `artifacts/chapter-04/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## 05. Intrinsic analysis on manifolds

- chapter goal: Geodesic-distance Frechet means, log-map coordinates, cut-locus caveats, and bootstrap inference on spheres.
- source span read: printed pp. 57-76; PDF pp. 72-91.
- concept inventory: geodesic distance, intrinsic mean, log map, cut locus, two-sample tests.
- library routing: geomstats, matplotlib, scipy.
- visual sequence: `intrinsic-mean-iteration.png` then `log-map-bootstrap-cloud.png`.
- artifact plan: `artifacts/chapter-05/figures`, optional `artifacts/chapter-05/interactive`, and `artifacts/chapter-05/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## 06. Landmark-based shape spaces

- chapter goal: The landmark pipeline from labeled configurations to quotient spaces under increasingly large transformation groups.
- source span read: printed pp. 77-81; PDF pp. 92-96.
- concept inventory: k-ads, centering, scale, group orbit, shape manifold.
- library routing: matplotlib, numpy.
- visual sequence: `landmark-normalization-pipeline.png` then `group-orbit-comparison.png`.
- artifact plan: `artifacts/chapter-06/figures`, optional `artifacts/chapter-06/interactive`, and `artifacts/chapter-06/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## 07. Kendall similarity shape spaces

- chapter goal: Preshape spheres, rotation quotients, horizontal directions, and geodesic distance on similarity shapes.
- source span read: printed pp. 82-86; PDF pp. 97-101.
- concept inventory: preshape sphere, rotation quotient, horizontal tangent, Procrustes distance.
- library routing: numpy, matplotlib, plotly.
- visual sequence: `preshape-sphere-orbits.png` then `kendall-geodesic.html`.
- artifact plan: `artifacts/chapter-07/figures`, optional `artifacts/chapter-07/interactive`, and `artifacts/chapter-07/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## 08. The planar shape space Sigma_k2

- chapter goal: Complex projective planar shape space, intrinsic and extrinsic means, size-and-shape, and two-sample inference.
- source span read: printed pp. 87-109; PDF pp. 102-124.
- concept inventory: complex preshape, CP space, Veronese embedding, Procrustes mean, bootstrap.
- library routing: geomstats, matplotlib, plotly.
- visual sequence: `planar-shape-sphere.png` then `procrustes-bootstrap.png`.
- artifact plan: `artifacts/chapter-08/figures`, optional `artifacts/chapter-08/interactive`, and `artifacts/chapter-08/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## 09. Reflection similarity shape spaces

- chapter goal: Reflection invariance as an unoriented quotient and extrinsic analysis through Gram-style representations.
- source span read: printed pp. 110-129; PDF pp. 125-144.
- concept inventory: reflection quotient, Gram matrix, unoriented shape, matched pairs, two-sample tests.
- library routing: matplotlib, numpy, scipy.
- visual sequence: `reflection-quotient-diagnostic.png` then `gram-embedding-spectrum.png`.
- artifact plan: `artifacts/chapter-09/figures`, optional `artifacts/chapter-09/interactive`, and `artifacts/chapter-09/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## 10. Stiefel manifolds V_k,m

- chapter goal: Orthogonal frames as manifold data, projection onto Stiefel constraints, and extrinsic mean diagnostics.
- source span read: printed pp. 130-134; PDF pp. 145-149.
- concept inventory: orthonormal frame, polar projection, tangent residual, extrinsic mean.
- library routing: numpy, matplotlib, scipy.
- visual sequence: `stiefel-frame-projection.png` then `orthogonality-residuals.png`.
- artifact plan: `artifacts/chapter-10/figures`, optional `artifacts/chapter-10/interactive`, and `artifacts/chapter-10/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## 11. Affine shape spaces A Sigma_km

- chapter goal: Affine normalization, rank conditions, and digit-like landmark examples where similarity information is intentionally discarded.
- source span read: printed pp. 135-146; PDF pp. 150-161.
- concept inventory: affine orbit, rank, normalization, classification, landmark covariance.
- library routing: numpy, matplotlib, scikit-learn.
- visual sequence: `affine-normalization-grid.png` then `digit-shape-affine-features.png`.
- artifact plan: `artifacts/chapter-11/figures`, optional `artifacts/chapter-11/interactive`, and `artifacts/chapter-11/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## 12. Real projective spaces and projective shape spaces

- chapter goal: Projective points as lines through the origin, antipodal quotients, and extrinsic analysis on real projective space.
- source span read: printed pp. 147-155; PDF pp. 162-170.
- concept inventory: real projective space, antipodal quotient, projective distance, projective shape.
- library routing: geomstats, matplotlib, plotly.
- visual sequence: `projective-antipodal-quotient.png` then `projective-distance-field.html`.
- artifact plan: `artifacts/chapter-12/figures`, optional `artifacts/chapter-12/interactive`, and `artifacts/chapter-12/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## 13. Nonparametric Bayes inference on manifolds

- chapter goal: Density estimation, posterior consistency intuition, and manifold mixture computation with spherical and SPD examples.
- source span read: printed pp. 156-181; PDF pp. 171-196.
- concept inventory: metric support, kernel mixture, Dirichlet process, posterior computation, classification.
- library routing: pyriemann, matplotlib, scipy, numpy.
- visual sequence: `manifold-density-mixture.png` then `spd-riemannian-mean.png`.
- artifact plan: `artifacts/chapter-13/figures`, optional `artifacts/chapter-13/interactive`, and `artifacts/chapter-13/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## 14. Nonparametric Bayes regression, classification, and testing

- chapter goal: Mixture-of-kernels regression, classification probabilities, and posterior testing as geometry-aware predictive workflows.
- source span read: printed pp. 182-208; PDF pp. 197-223.
- concept inventory: product kernels, regression, classification, Bayes testing, posterior predictive checks.
- library routing: matplotlib, scipy, numpy.
- visual sequence: `manifold-kernel-classifier.png` then `posterior-test-calibration.png`.
- artifact plan: `artifacts/chapter-14/figures`, optional `artifacts/chapter-14/interactive`, and `artifacts/chapter-14/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## A. Differentiable manifolds

- chapter goal: An executable atlas for charts, tangent vectors, immersions, submersions, and quotient-map intuition.
- source span read: printed pp. 209-213; PDF pp. 224-228.
- concept inventory: chart, tangent vector, immersion, submersion, quotient.
- library routing: matplotlib, sympy.
- visual sequence: `atlas-transition-map.png` then `tangent-pushforward.png`.
- artifact plan: `artifacts/appendix-a/figures`, optional `artifacts/appendix-a/interactive`, and `artifacts/appendix-a/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## B. Riemannian manifolds

- chapter goal: Metrics, geodesics, exponential and logarithm maps, curvature intuition, and SPD comparison checks.
- source span read: printed pp. 214-217; PDF pp. 229-232.
- concept inventory: metric tensor, geodesic, exponential map, logarithm map, curvature.
- library routing: geomstats, pyriemann, matplotlib.
- visual sequence: `riemannian-exp-log-map.png` then `spd-geodesic-comparison.png`.
- artifact plan: `artifacts/appendix-b/figures`, optional `artifacts/appendix-b/interactive`, and `artifacts/appendix-b/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## C. Dirichlet processes

- chapter goal: Stick-breaking, Polya urns, random discrete measures, and why DP mixtures adapt to manifold support.
- source span read: printed pp. 218-224; PDF pp. 233-239.
- concept inventory: stick breaking, Polya urn, base measure, random measure, posterior update.
- library routing: numpy, matplotlib, scipy.
- visual sequence: `stick-breaking-measure.png` then `polya-urn-clusters.png`.
- artifact plan: `artifacts/appendix-c/figures`, optional `artifacts/appendix-c/interactive`, and `artifacts/appendix-c/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.

## D. Parametric models on S_d and Sigma_k2

- chapter goal: Parametric sphere and planar-shape models used as baselines for the nonparametric methods.
- source span read: printed pp. 225-228; PDF pp. 240-243.
- concept inventory: von Mises-Fisher, axial models, planar shape model, normalizing constant.
- library routing: geomstats, matplotlib, scipy.
- visual sequence: `sphere-parametric-family.png` then `shape-space-parametric-baseline.png`.
- artifact plan: `artifacts/appendix-d/figures`, optional `artifacts/appendix-d/interactive`, and `artifacts/appendix-d/checks`.
- computational checks: JSON invariants plus final artifact-size and source-span checks in the canonical notebook.
- acceptance criteria: notebook executes, visuals display near prose, invariants pass, and no source prose or page imagery is copied.
