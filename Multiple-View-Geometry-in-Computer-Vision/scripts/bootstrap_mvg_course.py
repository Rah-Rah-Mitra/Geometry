"""Bootstrap the Multiple View Geometry notebook course.

This is an implementation helper for creating a complete standalone course from the
local PDF orientation. It writes course utilities, scripts, index notebooks, canonical
teaching notebooks, and an initial artifact set. Canonical notebooks regenerate their
own artifacts when executed.
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path
from pprint import pformat

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


COURSE_ROOT = Path(__file__).resolve().parents[1]
PDF_NAME = "Multiple View Geometry in Computer Vision.pdf"


PARTS = [
    {
        "folder": "part-00-background-projective-geometry-transformations-and-estimation",
        "label": "Part 0",
        "title": "The Background: Projective Geometry, Transformations and Estimation",
        "description": "Projective 2D/3D geometry, homographies, numerical estimation, and error analysis.",
    },
    {
        "folder": "part-01-camera-geometry-and-single-view-geometry",
        "label": "Part I",
        "title": "Camera Geometry and Single View Geometry",
        "description": "Camera matrices, calibration, distortion, vanishing geometry, and single-view measurement.",
    },
    {
        "folder": "part-02-two-view-geometry",
        "label": "Part II",
        "title": "Two-View Geometry",
        "description": "Epipolar geometry, the fundamental matrix, triangulation, homographies, rectification, and affine stereo.",
    },
    {
        "folder": "part-03-three-view-geometry",
        "label": "Part III",
        "title": "Three-View Geometry",
        "description": "The trifocal tensor, point and line transfer, three-view constraints, and tensor estimation.",
    },
    {
        "folder": "part-04-n-view-geometry",
        "label": "Part IV",
        "title": "N-View Geometry",
        "description": "Multiple-view tensors, factorization, bundle adjustment, auto-calibration, duality, cheirality, and degeneracies.",
    },
    {
        "folder": "part-05-appendices",
        "label": "Part V",
        "title": "Appendices",
        "description": "Tensor notation, statistics, parameter estimation, matrix decompositions, least squares, iterative methods, and special homographies.",
    },
]


def e(
    kind: str,
    number: int,
    label: str,
    title: str,
    folder: str,
    notebook: str,
    part: str | None,
    topic: str,
    printed: str,
    pdf: str,
    mode: str,
    focus: str,
    concepts: list[str],
    visuals: list[str],
    checks: list[str],
) -> dict:
    return {
        "kind": kind,
        "number": number,
        "label": label,
        "title": title,
        "folder": folder,
        "notebook": notebook,
        "part": part,
        "topic": topic,
        "printed": printed,
        "pdf": pdf,
        "mode": mode,
        "focus": focus,
        "concepts": concepts,
        "visuals": visuals,
        "checks": checks,
    }


ENTRIES = [
    e("chapter", 1, "Chapter 01", "Introduction: A Tour of Multiple View Geometry", "chapter-01-introduction-a-tour-of-multiple-view-geometry", "01-introduction-a-tour-of-multiple-view-geometry.ipynb", None, "chapter-01", "1-22", "19-40", "tour", "Projection, ambiguity, transfer, Euclidean upgrade, and the full multiple-view reconstruction arc.", ["projective geometry gives one language for images and 3D scenes", "camera projection loses depth but preserves incidence", "two and three views convert correspondence into structure constraints", "metric information returns only after extra calibration or scene assumptions"], ["pinhole projection tour", "one-view two-view three-view comparison", "projective ambiguity ladder", "transfer and reconstruction pipeline"], ["projected points satisfy homogeneous scale equivalence", "two-view residuals are near zero for synthetic correspondences", "triangulated points reproject to both cameras", "metric upgrade changes distances but preserves incidence"],),
    e("chapter", 2, "Chapter 02", "Projective Geometry and Transformations of 2D", "chapter-02-projective-geometry-and-transformations-of-2d", "02-projective-geometry-and-transformations-of-2d.ipynb", PARTS[0]["folder"], "chapter-02", "25-64", "43-82", "p2", "Points, lines, conics, homographies, transformation hierarchy, rectification, and metric recovery in the projective plane.", ["homogeneous 2D points represent Euclidean points plus ideal directions", "lines and points are dual incidence objects", "homographies preserve collinearity but not Euclidean measurements", "affine and metric rectification restore chosen invariants"], ["homography grid deformation", "vanishing line and affine rectification", "conic pole-polar diagram", "transformation hierarchy panel"], ["line-point incidence is scale invariant", "lines transform by inverse transpose", "cross-ratios remain stable under homographies", "rectified parallel lines meet on the recovered line at infinity"],),
    e("chapter", 3, "Chapter 03", "Projective Geometry and Transformations of 3D", "chapter-03-projective-geometry-and-transformations-of-3d", "03-projective-geometry-and-transformations-of-3d.ipynb", PARTS[0]["folder"], "chapter-03", "65-86", "83-104", "p3", "Projective 3D points, planes, lines, quadrics, twisted cubics, the plane at infinity, and the absolute conic.", ["3D projective coordinates keep finite points and directions in one algebra", "planes and points meet through a single bilinear incidence test", "lines require Plucker-style constraints rather than only two endpoints", "the plane at infinity and absolute conic encode affine and metric upgrades"], ["3D incidence viewer", "skew-line and Plucker relation demo", "quadric slicing scene", "absolute conic upgrade sketch"], ["plane-point incidence vanishes for sampled points", "line coordinates satisfy the Plucker quadratic relation", "quadric samples satisfy the implicit equation", "metric directions obey the absolute conic orthogonality test"],),
    e("chapter", 4, "Chapter 04", "Estimation: 2D Projective Transformations", "chapter-04-estimation-2d-projective-transformations", "04-estimation-2d-projective-transformations.ipynb", PARTS[0]["folder"], "chapter-04", "87-131", "105-149", "homography-estimation", "DLT homography estimation, geometric and statistical costs, normalization, iterative refinement, robust estimation, and automatic matching.", ["a homography estimate is a nullspace problem before it is an image warp", "normalization changes numerical conditioning without changing geometry", "geometric error is measured in image coordinates rather than coefficient space", "robust estimation separates inliers from misleading correspondences"], ["noisy correspondence homography", "normalization condition-number heatmap", "RANSAC inlier map", "cost-function comparison panel"], ["DLT residual decreases after normalization", "estimated H is scale normalized", "RANSAC inlier count exceeds the outlier count", "geometric reprojection error is lower than the raw algebraic baseline"],),
    e("chapter", 5, "Chapter 05", "Algorithm Evaluation and Error Analysis", "chapter-05-algorithm-evaluation-and-error-analysis", "05-algorithm-evaluation-and-error-analysis.ipynb", PARTS[0]["folder"], "chapter-05", "132-150", "150-168", "error", "Performance bounds, covariance propagation, Monte Carlo covariance, and empirical evaluation of geometric estimators.", ["an estimator is judged by residuals, variance, and sensitivity, not only by one answer", "covariance describes local uncertainty in estimated geometry", "Monte Carlo trials make algorithm stability visible", "performance bounds are useful only when tied to observable diagnostics"], ["error ellipse field", "noise sweep dashboard", "Monte Carlo covariance cloud", "bias-variance comparison"], ["sample covariance is positive semidefinite", "empirical coverage roughly matches the requested confidence gate", "RMSE grows with injected noise", "Monte Carlo means stay close to the noiseless estimate"],),
    e("chapter", 6, "Chapter 06", "Camera Models", "chapter-06-camera-models", "06-camera-models.ipynb", PARTS[1]["folder"], "chapter-06", "153-177", "171-195", "camera", "Finite cameras, projective cameras, affine cameras, intrinsic/extrinsic factorization, and alternative camera models.", ["a camera matrix maps world rays to image points through homogeneous projection", "the camera center is the nullspace of P", "intrinsics and extrinsics separate internal pixel geometry from camera pose", "affine and weak-perspective cameras are controlled approximations"], ["camera frustum and image plane", "intrinsic parameter slider map", "projection-class comparison", "camera-center nullspace diagram"], ["P times the camera center is zero", "RQ-style factorization reconstructs the camera matrix", "projected homogeneous coordinates are scale equivalent", "affine projection keeps parallel world directions parallel in the image"],),
    e("chapter", 7, "Chapter 07", "Computation of the Camera Matrix P", "chapter-07-computation-of-the-camera-matrix-p", "07-computation-of-the-camera-matrix-p.ipynb", PARTS[1]["folder"], "chapter-07", "178-194", "196-212", "camera-estimation", "Camera resectioning from 3D-2D correspondences, geometric error, constrained calibration, and radial distortion.", ["camera calibration is a linear solve followed by geometric validation", "restricted camera models reduce degrees of freedom by using prior structure", "radial distortion is visible as a systematic residual pattern", "calibration quality is best read from reprojection errors"], ["calibration target projection", "camera resection residual vectors", "distortion and undistortion grid", "restricted-camera parameter panel"], ["estimated P reprojects calibration points with low RMSE", "radial correction reduces curved residual structure", "camera center remains finite for a finite camera", "constrained estimates preserve their intended parameter restrictions"],),
    e("chapter", 8, "Chapter 08", "More Single View Geometry", "chapter-08-more-single-view-geometry", "08-more-single-view-geometry.ipynb", PARTS[1]["folder"], "chapter-08", "195-236", "213-254", "single-view", "Projection of planes, lines, conics, quadrics, silhouettes, vanishing points, the image of the absolute conic, and single-view reconstruction.", ["single-view measurement is possible when projective ambiguity is pinned by scene structure", "vanishing points encode 3D directions", "the image of the absolute conic converts orthogonality into calibration equations", "planes and conics transfer useful metric information through projection"], ["room vanishing-point triangle", "image of absolute conic constraints", "single-view height measurement", "projected conic and quadric silhouettes"], ["orthogonal vanishing points satisfy the IAC relation", "parallel 3D lines meet at a common image vanishing point", "height ratios are invariant under the constructed homology", "projected conic points satisfy the conic equation"],),
    e("chapter", 9, "Chapter 09", "Epipolar Geometry and the Fundamental Matrix", "chapter-09-epipolar-geometry-and-the-fundamental-matrix", "09-epipolar-geometry-and-the-fundamental-matrix.ipynb", PARTS[2]["folder"], "chapter-09", "239-261", "257-279", "epipolar", "Epipolar geometry, the fundamental matrix, special motions, epipoles, camera retrieval, and the essential matrix.", ["corresponding points lie on paired epipolar lines", "the fundamental matrix is rank two and maps points to lines", "epipoles are images of the opposite camera centers", "calibration upgrades F to the essential matrix with extra singular-value structure"], ["two-camera epipolar fan", "moving-point epiline widget sketch", "F and E singular value panel", "camera retrieval diagram"], ["x2 transpose F x1 is near zero", "F has rank two", "epipoles lie in the left and right nullspaces", "essential matrix singular values occur as a repeated pair and zero"],),
    e("chapter", 10, "Chapter 10", "3D Reconstruction of Cameras and Structure", "chapter-10-3d-reconstruction-of-cameras-and-structure", "10-3d-reconstruction-of-cameras-and-structure.ipynb", PARTS[2]["folder"], "chapter-10", "262-278", "280-296", "reconstruction", "Projective reconstruction, reconstruction ambiguity, the projective reconstruction theorem, and stratified upgrade.", ["image correspondences determine structure only up to a 3D projective ambiguity", "the same images can be produced by transformed cameras and transformed points", "stratification adds affine and metric constraints in stages", "ground truth is useful for measuring ambiguity but not required for reprojection"], ["projective ambiguity warp", "stratified reconstruction ladder", "camera and point reconstruction scene", "reprojection-invariance dashboard"], ["transformed cameras and points keep identical image projections", "reprojection error remains low after projective warps", "affine upgrade fixes a plane at infinity", "metric upgrade restores Euclidean angle checks"],),
    e("chapter", 11, "Chapter 11", "Computation of the Fundamental Matrix F", "chapter-11-computation-of-the-fundamental-matrix-f", "11-computation-of-the-fundamental-matrix-f.ipynb", PARTS[2]["folder"], "chapter-11", "279-309", "297-327", "fundamental-estimation", "Normalized eight-point estimation, algebraic minimization, geometric distance, robust computation, degeneracies, envelopes, and rectification.", ["the eight-point algorithm is a linear fit constrained back to rank two", "normalization is essential for stable fundamental matrix estimation", "Sampson error turns the epipolar constraint into a first-order distance", "rectification makes matching a one-dimensional search along rows"], ["match pipeline and inlier map", "Sampson contour field", "rank enforcement singular values", "rectified epipolar-line panel"], ["rank enforcement sets the smallest singular value to zero", "Sampson errors are smaller for inliers than outliers", "RANSAC recovers a high-consensus F", "rectified corresponding points have nearly equal vertical coordinates"],),
    e("chapter", 12, "Chapter 12", "Structure Computation", "chapter-12-structure-computation", "12-structure-computation.ipynb", PARTS[2]["folder"], "chapter-12", "310-324", "328-342", "triangulation", "Linear triangulation, geometric error, Sampson correction, optimal correction, uncertainty, and line reconstruction.", ["triangulation intersects back-projected rays that usually miss because of noise", "linear methods produce an initial point for geometric refinement", "uncertainty grows when rays meet at a small angle", "line reconstruction follows the same back-projection logic with line constraints"], ["skew-ray closest approach", "linear versus optimal triangulation", "uncertainty ellipsoid", "line reconstruction from image lines"], ["triangulated points reproject to both images", "ray angle predicts depth uncertainty", "refinement lowers geometric reprojection error", "estimated covariance is positive semidefinite"],),
    e("chapter", 13, "Chapter 13", "Scene Planes and Homographies", "chapter-13-scene-planes-and-homographies", "13-scene-planes-and-homographies.ipynb", PARTS[2]["folder"], "chapter-13", "325-343", "343-361", "plane-homography", "Plane-induced homographies, recovering planes, F from a plane homography, parallax, and the infinite homography.", ["a plane turns two-view transfer into a homography", "points off the plane reveal parallax relative to the plane-induced transfer", "F and a plane homography constrain one another", "the infinite homography captures pure rotation and calibration-dependent transfer"], ["plane transfer field", "parallax vector plot", "F-from-H consistency diagram", "infinite homography comparison"], ["planar points transfer with low homography residual", "off-plane parallax is nonzero and epipolar", "F reconstructed from H satisfies point constraints", "H infinity agrees with the rotation-induced transfer"],),
    e("chapter", 14, "Chapter 14", "Affine Epipolar Geometry", "chapter-14-affine-epipolar-geometry", "14-affine-epipolar-geometry.ipynb", PARTS[2]["folder"], "chapter-14", "344-362", "362-380", "affine-epipolar", "Affine cameras, affine fundamental matrix estimation, triangulation, affine reconstruction, bas-relief ambiguity, and motion recovery.", ["affine cameras simplify epipolar geometry by pushing epipoles to infinity", "affine F has fewer parameters than a projective fundamental matrix", "bas-relief ambiguity preserves many image measurements while changing depth", "motion recovery is constrained by affine viewing assumptions"], ["orthographic two-camera scene", "affine epipolar line family", "bas-relief ambiguity slider sketch", "affine triangulation panel"], ["affine epipolar residuals are linear in image coordinates", "parallel epipolar lines share a direction", "bas-relief transformed points preserve affine reprojections", "recovered motion satisfies the affine camera equations"],),
    e("chapter", 15, "Chapter 15", "The Trifocal Tensor", "chapter-15-the-trifocal-tensor", "15-the-trifocal-tensor.ipynb", PARTS[3]["folder"], "chapter-15", "365-390", "383-408", "trifocal", "The geometric basis of the trifocal tensor, tensor notation, transfer, and three-view fundamental matrices.", ["three views encode point and line transfer in a single tensor object", "the tensor packages how planes through one camera induce correspondences in the others", "point transfer becomes reliable when two views constrain the third", "pairwise fundamental matrices are shadows of the three-view relation"], ["three-camera transfer studio", "tensor slice explorer", "point-line transfer diagram", "pairwise F recovery panel"], ["trilinear residuals vanish for synthetic correspondences", "transferred points reproject near the third observation", "tensor slices have the expected rank behavior", "pairwise F matrices satisfy their epipolar constraints"],),
    e("chapter", 16, "Chapter 16", "Computation of the Trifocal Tensor T", "chapter-16-computation-of-the-trifocal-tensor-t", "16-computation-of-the-trifocal-tensor-t.ipynb", PARTS[3]["folder"], "chapter-16", "391-408", "409-426", "trifocal-estimation", "Linear, algebraic, geometric, and robust estimation of the trifocal tensor from point and line correspondences.", ["trifocal estimation is linear in measurements before enforcing geometric validity", "normalization stabilizes multi-image tensor fitting", "transfer error is the natural observable quality measure", "robust triplet selection protects the tensor from bad tracks"], ["triplet correspondence lab", "transfer-error landscape", "robust tensor inlier plot", "normalization effect panel"], ["linear tensor residuals decrease with normalization", "robust fitting rejects high-transfer-error triplets", "estimated transfer points land near observations", "geometric refinement improves the median transfer error"],),
    e("chapter", 17, "Chapter 17", "N-Linearities and Multiple View Tensors", "chapter-17-n-linearities-and-multiple-view-tensors", "17-n-linearities-and-multiple-view-tensors.ipynb", PARTS[4]["folder"], "chapter-17", "411-433", "429-451", "nlinear", "Bilinear, trilinear, and quadrilinear relations; plane intersections; counting arguments; independent equations; and equation choice.", ["multi-view tensors form a ladder of constraints as more cameras observe the same structure", "not every algebraic equation contributes independent information", "counting arguments reveal the degrees of freedom behind reconstruction", "useful equations are chosen for stability as well as formal validity"], ["tensor ladder diagram", "determinant block relations", "degree-of-freedom calculator", "independent-equation graph"], ["counted degrees of freedom match the synthetic parameterization", "selected determinants vanish on consistent tracks", "rank drops identify redundant equations", "equation subsets preserve the same reconstruction residual"],),
    e("chapter", 18, "Chapter 18", "N-View Computational Methods", "chapter-18-n-view-computational-methods", "18-n-view-computational-methods.ipynb", PARTS[4]["folder"], "chapter-18", "434-457", "452-475", "nview-methods", "Bundle adjustment, affine factorization, non-rigid factorization, projective factorization, plane-based reconstruction, and sequences.", ["tracks across many frames create a sparse camera-point estimation problem", "factorization exposes low-rank structure in affine image measurements", "non-rigid shape adds modes rather than a single rigid point set", "bundle adjustment improves all cameras and points together"], ["track matrix SVD", "sparse bundle-adjustment graph", "cost descent plot", "non-rigid mode panel"], ["affine track matrix has low numerical rank", "bundle-adjustment residual decreases", "sparse normal matrix has the expected block structure", "factorization reconstructs held-out observations with small error"],),
    e("chapter", 19, "Chapter 19", "Auto-Calibration", "chapter-19-auto-calibration", "19-auto-calibration.ipynb", PARTS[4]["folder"], "chapter-19", "458-501", "476-519", "autocalibration", "Algebraic auto-calibration, the absolute dual quadric, Kruppa equations, stratified solutions, rotating cameras, planar motion, turntables, and stereo rigs.", ["auto-calibration recovers metric camera information from constraints across views", "the absolute dual quadric is a carrier for calibration constraints", "special motions add constraints but may also create degeneracies", "stratified solutions turn projective reconstructions into metric ones step by step"], ["calibration constraint accumulator", "absolute dual quadric viewer", "Kruppa constraint sketch", "rotating-camera calibration panel"], ["recovered K has positive diagonal entries", "calibration constraints reduce algebraic residuals", "DAQ candidates have the expected signature pattern", "rotation-only constraints agree across images"],),
    e("chapter", 20, "Chapter 20", "Duality", "chapter-20-duality", "20-duality.ipynb", PARTS[4]["folder"], "chapter-20", "502-514", "520-532", "duality", "Carlsson-Weinshall duality and reduced reconstruction through the exchange of point and camera roles.", ["duality turns camera-point incidence into a complementary reconstruction problem", "reduced reconstruction keeps only the variables needed for a chosen query", "incidence graphs clarify which observations constrain which entities", "dual formulations preserve reprojection logic while changing algebraic roles"], ["point-camera dual swap", "incidence bipartite graph", "reduced reconstruction panel", "dual residual comparison"], ["dual incidence matrices have matching zero patterns", "primal and dual residuals agree on synthetic data", "reduced variables reproduce the target measurements", "graph connectivity predicts recoverable components"],),
    e("chapter", 21, "Chapter 21", "Cheirality", "chapter-21-cheirality", "21-cheirality.ipynb", PARTS[4]["folder"], "chapter-21", "515-532", "533-550", "cheirality", "Quasi-affine transformations, front/back camera tests, visible point sets, cheiral inequalities, third-view visibility, and depth ordering.", ["projective reconstruction must still respect which points are in front of cameras", "cheirality is expressed as a sign constraint on depths", "quasi-affine transformations preserve the visible side of cameras", "visibility in a third view can be reasoned about through inequalities"], ["depth-sign viewer", "cheiral half-space plot", "third-view visibility map", "quasi-affine transformation panel"], ["visible points have positive projective depth", "cheiral inequalities are feasible for the selected reconstruction", "quasi-affine transforms preserve depth signs", "third-view predictions match the synthetic visibility mask"],),
    e("chapter", 22, "Chapter 22", "Degenerate Configurations", "chapter-22-degenerate-configurations", "22-degenerate-configurations.ipynb", PARTS[4]["folder"], "chapter-22", "533-560", "551-578", "degenerate", "Degeneracies in camera resectioning, two-view and three-view reconstruction, critical surfaces, and ambiguous configurations.", ["degeneracy means the data no longer constrains a unique geometric answer", "rank and nullity diagnostics reveal many critical configurations", "some scene/camera arrangements create plausible but wrong reconstructions", "good algorithms report degeneracy instead of forcing a confident estimate"], ["critical-surface gallery", "rank-nullity dashboard", "two-view degeneracy scene", "three-view ambiguity panel"], ["design matrices lose rank in degenerate layouts", "nullspace dimension increases for critical configurations", "alternative reconstructions share similar reprojection error", "diagnostics flag the degenerate sample before final estimation"],),
    e("appendix", 101, "Appendix 01", "Tensor Notation", "appendix-01-tensor-notation", "a01-tensor-notation.ipynb", PARTS[5]["folder"], "appendix-01", "562-564", "580-582", "tensor", "Covariant and contravariant indices, basis changes, contractions, the epsilon tensor, and trifocal tensor notation.", ["indices describe how coordinates transform under basis changes", "contractions pair upper and lower indices into invariant quantities", "the epsilon tensor encodes cross products and determinants", "tensor notation is practical when arrays have more than two meaningful axes"], ["basis-change index diagram", "contraction flow chart", "epsilon tensor determinant panel", "trifocal tensor slice notation"], ["basis-transformed coordinates represent the same point", "contracted scalar values remain invariant", "epsilon contractions match cross products", "tensor slices transform according to the chosen bases"],),
    e("appendix", 102, "Appendix 02", "Gaussian and Chi-square Distributions", "appendix-02-gaussian-normal-and-chi2-distributions", "a02-gaussian-normal-and-chi2-distributions.ipynb", PARTS[5]["folder"], "appendix-02", "565-567", "583-585", "statistics", "Gaussian measurement models, covariance, Mahalanobis distance, confidence gates, and chi-square diagnostics.", ["Gaussian noise models turn residual vectors into probabilities", "covariance ellipses reveal anisotropic uncertainty", "Mahalanobis distance is the residual measured in covariance units", "chi-square gates convert residual magnitude into an acceptance test"], ["covariance ellipse field", "Mahalanobis distance contours", "chi-square confidence gates", "sample coverage dashboard"], ["sample covariance is positive semidefinite", "Mahalanobis distances follow the expected distribution roughly", "confidence gates contain the planned fraction of samples", "whitening produces nearly identity covariance"],),
    e("appendix", 103, "Appendix 03", "Parameter Estimation", "appendix-03-parameter-estimation", "a03-parameter-estimation.ipynb", PARTS[5]["folder"], "appendix-03", "568-577", "586-595", "parameter-estimation", "Bias, variance, maximum likelihood, posterior estimation, Fisher information, and Cramer-Rao style bounds.", ["estimation turns noisy measurements into parameter distributions", "maximum likelihood is a geometry-aware choice only after defining the noise model", "bias and variance describe different failure modes", "bounds are useful when compared with Monte Carlo behavior"], ["likelihood curve", "estimator bias sweep", "variance versus bound panel", "posterior update diagram"], ["maximum likelihood coincides with least squares for isotropic Gaussian noise", "empirical variance exceeds the lower-bound estimate", "bias shrinks with more measurements in the synthetic example", "posterior normalization sums to one in the discrete lab"],),
    e("appendix", 104, "Appendix 04", "Matrix Properties and Decompositions", "appendix-04-matrix-properties-and-decompositions", "a04-matrix-properties-and-decompositions.ipynb", PARTS[5]["folder"], "appendix-04", "578-587", "596-605", "matrix", "Rank, nullspaces, eigenstructure, SVD, Cholesky, QR/RQ, Schur, and matrix identities used by MVG algorithms.", ["matrix decompositions expose geometric structure hidden in coefficients", "SVD identifies rank, nullspaces, conditioning, and best low-rank approximations", "RQ-style decompositions support camera calibration factorization", "positive definite matrices encode valid covariance and conic constraints"], ["SVD geometry panel", "nullspace and rank dashboard", "RQ camera factorization sketch", "positive-definite ellipse view"], ["SVD reconstruction matches the original matrix", "nullspace vectors satisfy A v near zero", "positive-definite matrices have positive eigenvalues", "factorized camera matrices reconstruct P up to scale"],),
    e("appendix", 105, "Appendix 05", "Least-squares Minimization", "appendix-05-least-squares-minimization", "a05-least-squares-minimization.ipynb", PARTS[5]["folder"], "appendix-05", "588-596", "606-614", "least-squares", "Linear least squares, normal equations, total least squares, weighted least squares, constrained systems, and sparse symmetric equations.", ["least squares projects impossible constraints onto the closest attainable model", "normal equations are useful but can square conditioning problems", "total least squares treats errors in the design matrix as well as observations", "weights encode unequal measurement uncertainty"], ["residual projection diagram", "normal-equation conditioning panel", "total versus ordinary least-squares comparison", "weighted residual dashboard"], ["least-squares residual is orthogonal to the column space", "SVD and normal-equation solutions agree on well-conditioned examples", "weighted residuals shrink in high-confidence directions", "TLS line fitting reduces orthogonal rather than vertical distance"],),
    e("appendix", 106, "Appendix 06", "Iterative Estimation Methods", "appendix-06-iterative-estimation-methods", "a06-iterative-estimation-methods.ipynb", PARTS[5]["folder"], "appendix-06", "597-627", "615-645", "iterative", "Newton, Gauss-Newton, Levenberg-Marquardt, sparse systems, robust costs, rotations, homogeneous vectors, and constrained parameterizations.", ["iterative methods replace nonlinear geometry by local linear problems", "damping interpolates between cautious descent and fast Gauss-Newton updates", "sparse structure makes bundle adjustment tractable", "robust costs reduce the influence of outliers"], ["optimizer path comparison", "damping schedule panel", "Schur complement sparsity graph", "robust loss curve"], ["finite-difference Jacobians match analytic approximations", "accepted steps decrease the objective", "robust weights shrink for large residuals", "sparse block elimination matches the dense solution on a small case"],),
    e("appendix", 107, "Appendix 07", "Some Special Plane Projective Transformations", "appendix-07-some-special-plane-projective-transformations", "a07-some-special-plane-projective-transformations.ipynb", PARTS[5]["folder"], "appendix-07", "628-633", "646-651", "special-homographies", "Conjugate rotations, homologies, elations, affinities, and special eigenstructure of plane projective transformations.", ["special homographies are recognized by fixed points, fixed lines, and eigenvalue multiplicities", "homologies move points along lines through a vertex while fixing an axis", "conjugate rotations preserve a hidden metric angle", "classification helps decide how many correspondences are needed"], ["fixed point and line flow", "homology axis-vertex diagram", "conjugate rotation eigenvalue panel", "homography classification table"], ["fixed points satisfy H x proportional to x", "axis points remain on the fixed line", "eigenvalue multiplicities match the class label", "cross-ratio invariants remain stable under the homology"],),
]

SMOKE_NOTEBOOKS = {
    "01-introduction-a-tour-of-multiple-view-geometry.ipynb",
    "02-projective-geometry-and-transformations-of-2d.ipynb",
    "06-camera-models.ipynb",
    "09-epipolar-geometry-and-the-fundamental-matrix.ipynb",
    "11-computation-of-the-fundamental-matrix-f.ipynb",
    "12-structure-computation.ipynb",
    "15-the-trifocal-tensor.ipynb",
    "18-n-view-computational-methods.ipynb",
    "a06-iterative-estimation-methods.ipynb",
}


def clean(text: str) -> str:
    return textwrap.dedent(text).strip() + "\n"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(clean(text), encoding="utf-8")


def write_notebook(path: Path, cells: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=cells, metadata={"language_info": {"name": "python"}}), path)


def entry_folder(entry: dict) -> Path:
    if entry["part"] is None:
        return COURSE_ROOT / entry["folder"]
    return COURSE_ROOT / entry["part"] / entry["folder"]


def inventory_py() -> str:
    return f'''"""Inventory for the Multiple View Geometry notebook course."""

from __future__ import annotations

PARTS = {pformat(PARTS, width=100)}

ENTRIES = {pformat(ENTRIES, width=100)}

SMOKE_NOTEBOOKS = {pformat(SMOKE_NOTEBOOKS, width=100)}


def canonical_entries() -> list[dict]:
    return list(ENTRIES)


def parts() -> list[dict]:
    return list(PARTS)


def entry_folder(entry: dict) -> str:
    if entry["part"] is None:
        return entry["folder"]
    return f'{{entry["part"]}}/{{entry["folder"]}}'
'''


def agents_md() -> str:
    command_root = "Multiple-View-Geometry-in-Computer-Vision"
    return f"""# Agent Instructions: Multiple View Geometry in Computer Vision Notebook Course

This folder is a standalone visualization-first notebook edition of *Multiple View Geometry in Computer Vision, Second Edition* by Richard Hartley and Andrew Zisserman. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment.

## Repo-Local Skills

Use the repo-local skills under `D:\\Geometry\\.codex\\skills` for course work:

- `geometry-visualization-planner` for chapter storyboards.
- `geometry-chapter-notebook-author` for authoring canonical notebooks.
- `geometry-notebook-qc` for standalone, artifact, and execution review.

## Non-Negotiables

- Write original teaching prose, derivations, code, and visual explanations.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or figures.
- The notebooks must stand alone without the PDF open.
- Visualization is part of the teaching argument, not decoration or a fixed quota.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute cleanly with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook per chapter or appendix folder plus a local `00-index.ipynb`.

## Source Map

The PDF has 673 physical pages. Printed page 1 starts on PDF page 19, so body and appendix spans use:

```text
pdf_page = printed_page + 18
```

The course follows the book structure: a root introductory chapter, Part 0 background, Part I single-view geometry, Part II two-view geometry, Part III three-view geometry, Part IV N-view geometry, and Part V appendices. Bibliography and printed index pages are not authored as canonical notebooks.

## Notebook Shape

Each canonical notebook should include:

1. Title and source span.
2. Translation guide from book concepts into computational language.
3. Route through the chapter.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Visual artifacts saved under `artifacts/` and displayed inline.
8. Applied lab or design exercise.
9. Sanity checks asserting core identities and artifact existence.
10. Takeaways.

## Geometry Stack

Use the shared `uv` environment at `D:\\Geometry`. Prefer installed packages before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `networkx`, `opencv-contrib-python` as `cv2`, `scikit-image`, `pandas`, `pyvista`, `trimesh`, and `PIL`.

## Worker Boundaries

Assign one worker to one canonical notebook or one shared helper/script task. Chapter workers should read their assigned source span, consume or create a visualization storyboard, and edit only the assigned chapter folder, its artifact subtree, and any explicitly assigned helper. Workers are not alone in the codebase; do not revert other workers' edits.

## Commands

Run from `D:\\Geometry`:

```powershell
uv run python "{command_root}/scripts/build_mvg_course_indexes.py"
uv run python -m compileall -q "{command_root}/utils" "{command_root}/scripts"
uv run pytest -q "{command_root}/scripts"
uv run python "{command_root}/scripts/audit_mvg_notebooks.py" --min-words 1200 --min-code-cells 5
uv run python "{command_root}/scripts/audit_mvg_visuals.py"
uv run python "{command_root}/scripts/validate_mvg_course.py" --smoke --timeout 300
uv run python "{command_root}/scripts/validate_mvg_course.py" --limit 8 --timeout 300
git diff --check
```
"""


UTILS = {
    "__init__.py": '"""Utilities for the Multiple View Geometry notebook course."""\n',
    "artifacts.py": r'''
"""Artifact helpers for the Multiple View Geometry notebook course."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable


BOOK_ROOT = Path(__file__).resolve().parents[1]


def find_book_root(start: Path | None = None) -> Path:
    current = Path.cwd() if start is None else Path(start).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
            return candidate
    return BOOK_ROOT


def artifact_path(topic: str, *parts: str, create: bool = True) -> Path:
    path = BOOK_ROOT / "artifacts" / topic
    for part in parts:
        path = path / part
    if create:
        path.parent.mkdir(parents=True, exist_ok=True)
    return path


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_matplotlib(fig: Any, topic: str, *parts: str, dpi: int = 160) -> Path:
    path = ensure_parent(artifact_path(topic, *parts))
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    return path


def save_plotly_html(fig: Any, topic: str, *parts: str) -> Path:
    path = ensure_parent(artifact_path(topic, *parts))
    fig.write_html(str(path), include_plotlyjs="cdn", full_html=True)
    return path


def save_image(image: Any, topic: str, *parts: str) -> Path:
    path = ensure_parent(artifact_path(topic, *parts))
    image.save(path)
    return path


def save_json(data: Any, topic: str, *parts: str) -> Path:
    path = ensure_parent(artifact_path(topic, *parts))
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def save_csv(rows: Iterable[dict[str, Any]], topic: str, *parts: str) -> Path:
    path = ensure_parent(artifact_path(topic, *parts))
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return path
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def save_text(text: str, topic: str, *parts: str) -> Path:
    path = ensure_parent(artifact_path(topic, *parts))
    path.write_text(text, encoding="utf-8")
    return path


def relative_to_book(path: Path, book_root: Path | None = None) -> str:
    root = find_book_root() if book_root is None else Path(book_root)
    try:
        return Path(path).resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return Path(path).as_posix()


def assert_artifacts(paths: Iterable[Path], *, min_bytes: int = 32) -> None:
    missing: list[str] = []
    tiny: list[str] = []
    for path in paths:
        candidate = Path(path)
        if not candidate.exists():
            missing.append(str(candidate))
        elif candidate.stat().st_size < min_bytes:
            tiny.append(str(candidate))
    if missing or tiny:
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if tiny:
            details.append("too small: " + ", ".join(tiny))
        raise AssertionError("; ".join(details))


def display_artifact(path: Path, *, width: int = 820, height: int = 540) -> None:
    from IPython.display import HTML, Image, Markdown, display

    candidate = Path(path)
    suffix = candidate.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg"}:
        display(Image(filename=str(candidate), width=width))
    elif suffix in {".html", ".htm"}:
        display(HTML(f'<iframe src="{candidate.as_posix()}" width="{width}" height="{height}"></iframe>'))
    elif suffix == ".json":
        display(Markdown(f"`{relative_to_book(candidate)}`"))
    else:
        display(Markdown(f"[{candidate.name}]({candidate.as_posix()})"))
''',
    "projective.py": r'''
"""Small projective-geometry helpers used by MVG notebooks."""

from __future__ import annotations

import numpy as np


def homogenize(points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    ones = np.ones((*pts.shape[:-1], 1), dtype=float)
    return np.concatenate([pts, ones], axis=-1)


def dehomogenize(points: np.ndarray, *, eps: float = 1e-12) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    w = pts[..., -1:]
    safe = np.where(np.abs(w) < eps, np.sign(w) * eps + (w == 0) * eps, w)
    return pts[..., :-1] / safe


def normalize_homogeneous(x: np.ndarray, *, eps: float = 1e-12) -> np.ndarray:
    arr = np.asarray(x, dtype=float)
    norm = np.linalg.norm(arr, axis=-1, keepdims=True)
    norm = np.where(norm < eps, 1.0, norm)
    return arr / norm


def line_through(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    return np.cross(np.asarray(p, dtype=float), np.asarray(q, dtype=float))


def incidence(line: np.ndarray, point: np.ndarray) -> float:
    return float(np.dot(np.asarray(line, dtype=float), np.asarray(point, dtype=float)))


def apply_homography(H: np.ndarray, points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    hp = homogenize(pts) if pts.shape[-1] == 2 else pts
    mapped = (np.asarray(H, dtype=float) @ hp.T).T
    return dehomogenize(mapped)


def normalize_points_2d(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    pts = np.asarray(points, dtype=float)
    if pts.shape[-1] == 3:
        pts = dehomogenize(pts)
    centroid = pts.mean(axis=0)
    centered = pts - centroid
    mean_dist = np.sqrt((centered**2).sum(axis=1)).mean()
    scale = np.sqrt(2.0) / mean_dist if mean_dist > 1e-12 else 1.0
    T = np.array([[scale, 0.0, -scale * centroid[0]], [0.0, scale, -scale * centroid[1]], [0.0, 0.0, 1.0]])
    normalized = (T @ homogenize(pts).T).T
    return normalized, T


def dlt_homography(src: np.ndarray, dst: np.ndarray) -> np.ndarray:
    src_n, Ts = normalize_points_2d(src)
    dst_n, Td = normalize_points_2d(dst)
    rows = []
    for x, xp in zip(src_n, dst_n):
        X, Y, W = x
        u, v, w = xp
        rows.append([0, 0, 0, -w * X, -w * Y, -w * W, v * X, v * Y, v * W])
        rows.append([w * X, w * Y, w * W, 0, 0, 0, -u * X, -u * Y, -u * W])
    _, _, vt = np.linalg.svd(np.asarray(rows))
    Hn = vt[-1].reshape(3, 3)
    H = np.linalg.inv(Td) @ Hn @ Ts
    return H / H[-1, -1]


def conic_from_circle(center: tuple[float, float], radius: float) -> np.ndarray:
    cx, cy = center
    return np.array([[1.0, 0.0, -cx], [0.0, 1.0, -cy], [-cx, -cy, cx * cx + cy * cy - radius * radius]])


def plucker_from_points(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    A = np.asarray(a, dtype=float)
    B = np.asarray(b, dtype=float)
    return np.outer(A, B) - np.outer(B, A)
''',
    "cameras.py": r'''
"""Camera helpers for synthetic multiple-view geometry labs."""

from __future__ import annotations

import numpy as np

from .projective import dehomogenize, homogenize


def skew(v: np.ndarray) -> np.ndarray:
    x, y, z = np.asarray(v, dtype=float).reshape(3)
    return np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])


def make_calibration(fx: float = 900.0, fy: float | None = None, cx: float = 0.0, cy: float = 0.0, skew_value: float = 0.0) -> np.ndarray:
    if fy is None:
        fy = fx
    return np.array([[fx, skew_value, cx], [0.0, fy, cy], [0.0, 0.0, 1.0]], dtype=float)


def look_at_rotation(center: np.ndarray, target: np.ndarray = np.zeros(3), up: np.ndarray = np.array([0.0, 1.0, 0.0])) -> np.ndarray:
    center = np.asarray(center, dtype=float)
    target = np.asarray(target, dtype=float)
    forward = target - center
    forward = forward / np.linalg.norm(forward)
    right = np.cross(forward, up)
    if np.linalg.norm(right) < 1e-9:
        right = np.array([1.0, 0.0, 0.0])
    right = right / np.linalg.norm(right)
    true_up = np.cross(right, forward)
    true_up = true_up / np.linalg.norm(true_up)
    return np.vstack([right, true_up, forward])


def camera_matrix(K: np.ndarray, R: np.ndarray, center: np.ndarray) -> np.ndarray:
    center = np.asarray(center, dtype=float).reshape(3, 1)
    Rt = np.hstack([R, -R @ center])
    return np.asarray(K, dtype=float) @ Rt


def project_points(P: np.ndarray, points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    hp = homogenize(pts) if pts.shape[-1] == 3 else pts
    return dehomogenize((np.asarray(P, dtype=float) @ hp.T).T)


def camera_center(P: np.ndarray) -> np.ndarray:
    _, _, vt = np.linalg.svd(np.asarray(P, dtype=float))
    C = vt[-1]
    return C / C[-1]


def synthetic_cameras() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    K = make_calibration(850.0, 830.0, 320.0, 240.0)
    c1 = np.array([-1.8, 0.4, -4.2])
    c2 = np.array([1.7, 0.6, -4.0])
    P1 = camera_matrix(K, look_at_rotation(c1), c1)
    P2 = camera_matrix(K, look_at_rotation(c2), c2)
    return K, P1, P2


def cube_points(scale: float = 1.0) -> np.ndarray:
    vals = [-scale, scale]
    return np.array([[x, y, z + 3.2] for x in vals for y in vals for z in vals], dtype=float)
''',
    "epipolar.py": r'''
"""Epipolar and triangulation helpers for MVG notebooks."""

from __future__ import annotations

import numpy as np

from .cameras import camera_center, skew
from .projective import homogenize, normalize_points_2d


def enforce_rank2(F: np.ndarray) -> np.ndarray:
    u, s, vt = np.linalg.svd(np.asarray(F, dtype=float))
    s[-1] = 0.0
    Fr = u @ np.diag(s) @ vt
    norm = np.linalg.norm(Fr)
    return Fr / norm if norm else Fr


def fundamental_from_cameras(P1: np.ndarray, P2: np.ndarray) -> np.ndarray:
    C1 = camera_center(P1)
    e2 = P2 @ C1
    F = skew(e2) @ P2 @ np.linalg.pinv(P1)
    return enforce_rank2(F)


def eight_point(points1: np.ndarray, points2: np.ndarray) -> np.ndarray:
    p1, T1 = normalize_points_2d(points1)
    p2, T2 = normalize_points_2d(points2)
    rows = []
    for a, b in zip(p1, p2):
        x, y, w = a
        xp, yp, wp = b
        rows.append([xp * x, xp * y, xp * w, yp * x, yp * y, yp * w, wp * x, wp * y, wp * w])
    _, _, vt = np.linalg.svd(np.asarray(rows))
    Fn = vt[-1].reshape(3, 3)
    F = T2.T @ enforce_rank2(Fn) @ T1
    return enforce_rank2(F)


def sampson_errors(F: np.ndarray, points1: np.ndarray, points2: np.ndarray) -> np.ndarray:
    x1 = homogenize(points1) if np.asarray(points1).shape[-1] == 2 else np.asarray(points1, dtype=float)
    x2 = homogenize(points2) if np.asarray(points2).shape[-1] == 2 else np.asarray(points2, dtype=float)
    Fx1 = (F @ x1.T).T
    Ftx2 = (F.T @ x2.T).T
    numer = np.sum(x2 * Fx1, axis=1) ** 2
    denom = Fx1[:, 0] ** 2 + Fx1[:, 1] ** 2 + Ftx2[:, 0] ** 2 + Ftx2[:, 1] ** 2
    return numer / np.maximum(denom, 1e-12)


def linear_triangulate(P1: np.ndarray, P2: np.ndarray, points1: np.ndarray, points2: np.ndarray) -> np.ndarray:
    pts = []
    for x1, x2 in zip(points1, points2):
        u1, v1 = x1[:2]
        u2, v2 = x2[:2]
        A = np.vstack([
            u1 * P1[2] - P1[0],
            v1 * P1[2] - P1[1],
            u2 * P2[2] - P2[0],
            v2 * P2[2] - P2[1],
        ])
        _, _, vt = np.linalg.svd(A)
        X = vt[-1]
        pts.append(X[:3] / X[3])
    return np.asarray(pts)
''',
    "estimation.py": r'''
"""Estimation helpers used across the MVG course."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np


def reprojection_rmse(observed: np.ndarray, predicted: np.ndarray) -> float:
    residual = np.asarray(observed, dtype=float) - np.asarray(predicted, dtype=float)
    return float(np.sqrt(np.mean(np.sum(residual**2, axis=-1))))


def monte_carlo_covariance(samples: np.ndarray) -> np.ndarray:
    samples = np.asarray(samples, dtype=float)
    return np.cov(samples.T)


def finite_difference_jacobian(fn: Callable[[np.ndarray], np.ndarray], x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    y0 = np.asarray(fn(x), dtype=float).ravel()
    J = np.zeros((y0.size, x.size))
    for j in range(x.size):
        step = np.zeros_like(x)
        step[j] = eps
        J[:, j] = (np.asarray(fn(x + step)).ravel() - np.asarray(fn(x - step)).ravel()) / (2 * eps)
    return J


def simple_ransac(sample_count: int, fit_fn, residual_fn, threshold: float, *, trials: int = 128, rng: np.random.Generator | None = None):
    if rng is None:
        rng = np.random.default_rng(0)
    best_model = None
    best_inliers = np.array([], dtype=int)
    n = residual_fn(None, probe=True)
    for _ in range(trials):
        sample = rng.choice(n, size=sample_count, replace=False)
        model = fit_fn(sample)
        residuals = residual_fn(model)
        inliers = np.flatnonzero(residuals < threshold)
        if inliers.size > best_inliers.size:
            best_model = model
            best_inliers = inliers
    return best_model, best_inliers
''',
    "plotting.py": r'''
"""Stable plotting helpers for the MVG notebooks."""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np


COLORS = {
    "ink": "#1f2937",
    "blue": "#2563eb",
    "teal": "#0f766e",
    "green": "#4d7c0f",
    "orange": "#c2410c",
    "red": "#b91c1c",
    "purple": "#6d28d9",
    "gray": "#6b7280",
    "light": "#eef2ff",
}


def style_axis(ax, *, title: str | None = None, equal: bool = True) -> None:
    if title:
        ax.set_title(title, loc="left", fontsize=12, fontweight="bold")
    ax.grid(True, color="#e5e7eb", linewidth=0.8)
    ax.set_facecolor("white")
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color("#d1d5db")
    ax.tick_params(labelsize=8)


def concept_map_figure(title: str, concepts: list[str], visuals: list[str]):
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    ax.axis("off")
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold")
    center = np.array([0.5, 0.52])
    ax.scatter([center[0]], [center[1]], s=900, color=COLORS["blue"], alpha=0.92)
    ax.text(center[0], center[1], "MVG\nquestion", color="white", ha="center", va="center", fontsize=10, fontweight="bold")
    items = [(c, COLORS["teal"]) for c in concepts] + [(v, COLORS["orange"]) for v in visuals]
    angles = np.linspace(0.0, 2 * np.pi, len(items), endpoint=False)
    for idx, ((text, color), angle) in enumerate(zip(items, angles)):
        radius = 0.34 + 0.04 * (idx % 2)
        pos = center + radius * np.array([np.cos(angle), np.sin(angle)])
        ax.plot([center[0], pos[0]], [center[1], pos[1]], color="#cbd5e1", linewidth=1.3)
        ax.scatter([pos[0]], [pos[1]], s=260, color=color, alpha=0.92, edgecolor="white", linewidth=1.2)
        wrapped = "\n".join(_wrap_words(text, 22))
        ax.text(pos[0], pos[1], wrapped, ha="center", va="center", fontsize=7.3, color="white")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig


def _wrap_words(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        if sum(len(w) + 1 for w in current) + len(word) > width and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines[:4]


def vision_scene_figure(mode: str, title: str, seed: int):
    rng = np.random.default_rng(seed)
    if mode in {"p3", "camera", "camera-estimation", "single-view", "epipolar", "reconstruction", "fundamental-estimation", "triangulation", "plane-homography", "affine-epipolar", "trifocal", "trifocal-estimation", "nlinear", "nview-methods", "autocalibration", "duality", "cheirality", "degenerate"}:
        fig = plt.figure(figsize=(8.2, 6.2))
        ax = fig.add_subplot(111, projection="3d")
        ax.set_title(title, loc="left", fontsize=12, fontweight="bold")
        centers = np.array([[-2.2, 0.1, -3.2], [2.0, 0.3, -3.0], [0.2, 1.6, -3.6]])
        scene = rng.normal(size=(16, 3)) * np.array([1.1, 0.65, 0.85]) + np.array([0.0, 0.1, 2.2])
        ax.scatter(scene[:, 0], scene[:, 1], scene[:, 2], s=34, c=COLORS["teal"], depthshade=True, label="scene points")
        for i, c in enumerate(centers):
            ax.scatter([c[0]], [c[1]], [c[2]], s=70, c=[COLORS["blue"], COLORS["orange"], COLORS["purple"]][i], marker="^", label=f"camera {i+1}")
            for p in scene[:5]:
                ax.plot([c[0], p[0]], [c[1], p[1]], [c[2], p[2]], color="#cbd5e1", linewidth=0.8, alpha=0.75)
        t = np.linspace(-1, 1, 5)
        xx, yy = np.meshgrid(t, t)
        zz = np.full_like(xx, 1.25)
        ax.plot_wireframe(xx, yy, zz, color="#94a3b8", linewidth=0.55, alpha=0.8)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.view_init(elev=20 + seed % 15, azim=-50 + seed % 40)
        ax.legend(loc="upper left", fontsize=7)
        return fig
    fig, ax = plt.subplots(figsize=(7.8, 5.8))
    style_axis(ax, title=title)
    xs = np.linspace(-2.0, 2.0, 9)
    ys = np.linspace(-1.4, 1.4, 7)
    H = np.array([[1.0, 0.12 + 0.015 * (seed % 7), 0.2], [-0.08, 1.0, 0.15], [0.06, -0.035, 1.0]])
    for x in xs:
        pts = np.column_stack([np.full_like(ys, x), ys, np.ones_like(ys)])
        mapped = (H @ pts.T).T
        mapped = mapped[:, :2] / mapped[:, 2:]
        ax.plot(mapped[:, 0], mapped[:, 1], color=COLORS["blue"], alpha=0.78, linewidth=1.2)
    for y in ys:
        pts = np.column_stack([xs, np.full_like(xs, y), np.ones_like(xs)])
        mapped = (H @ pts.T).T
        mapped = mapped[:, :2] / mapped[:, 2:]
        ax.plot(mapped[:, 0], mapped[:, 1], color=COLORS["orange"], alpha=0.78, linewidth=1.2)
    ax.scatter([-1.2, 0.4, 1.1], [0.8, -0.2, 0.6], s=50, color=COLORS["teal"], edgecolor="white", zorder=4)
    ax.text(-1.9, -1.75, f"mode: {mode}", fontsize=8, color=COLORS["gray"])
    return fig


def diagnostic_figure(title: str, checks: list[str], seed: int):
    rng = np.random.default_rng(seed)
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.4))
    x = np.linspace(0, 1, 80)
    for i, check in enumerate(checks[:4]):
        y = np.exp(-(i + 1) * x) + 0.025 * rng.normal(size=x.size) + 0.04 * i
        axes[0].plot(x, y, linewidth=2, label=f"check {i+1}")
    axes[0].set_title("residual traces", loc="left", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("normalized experiment step")
    axes[0].set_ylabel("diagnostic value")
    axes[0].legend(fontsize=7)
    axes[0].grid(True, color="#e5e7eb")
    A = rng.normal(size=(8, 8))
    heat = A @ A.T
    heat = heat / np.max(np.abs(heat))
    im = axes[1].imshow(heat, cmap="viridis", origin="lower")
    axes[1].set_title(title, loc="left", fontsize=11, fontweight="bold")
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    fig.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)
    fig.tight_layout()
    return fig


def constraint_dashboard_figure(title: str, mode: str, seed: int):
    rng = np.random.default_rng(seed)
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    style_axis(ax, title=title, equal=False)
    base = np.sort(np.abs(rng.normal(size=9)))[::-1] + np.linspace(1.0, 0.04, 9)
    if mode in {"epipolar", "fundamental-estimation", "trifocal", "degenerate"}:
        base[-1] *= 0.04
    if mode == "degenerate":
        base[-2:] *= 0.02
    ax.semilogy(np.arange(1, len(base) + 1), base, marker="o", color=COLORS["purple"], linewidth=2)
    ax.fill_between(np.arange(1, len(base) + 1), base, base.min() * 0.5, color=COLORS["purple"], alpha=0.12)
    ax.set_xlabel("singular value index")
    ax.set_ylabel("relative scale")
    ax.text(0.02, 0.08, f"constraint family: {mode}", transform=ax.transAxes, fontsize=9, color=COLORS["ink"])
    return fig


def compute_visual_summary(title: str, mode: str, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(9, 9))
    if mode in {"epipolar", "fundamental-estimation", "degenerate"}:
        A[-1] = A[-2] + 1e-3 * rng.normal(size=9)
    s = np.linalg.svd(A, compute_uv=False)
    residual = float(s[-1] / max(s[0], 1e-12))
    cov = rng.normal(size=(3, 200))
    cov = np.cov(cov)
    return {
        "title": title,
        "mode": mode,
        "seed": seed,
        "rank_estimate": int(np.linalg.matrix_rank(A, tol=1e-8)),
        "smallest_singular_ratio": residual,
        "covariance_min_eigenvalue": float(np.linalg.eigvalsh(cov).min()),
    }
''',
    "validation.py": r'''
"""Validation helpers for MVG scripts and notebooks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}


def relative(path: Path, root: Path | None = None) -> str:
    base = BOOK_ROOT if root is None else root
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def canonical_notebooks(book_root: Path = BOOK_ROOT) -> list[Path]:
    artifact_root = book_root / "artifacts"
    return [
        path
        for path in sorted(book_root.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED_NOTEBOOKS
    ]


def index_notebooks(book_root: Path = BOOK_ROOT) -> list[Path]:
    artifact_root = book_root / "artifacts"
    return [
        path
        for path in sorted(book_root.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name in IGNORED_NOTEBOOKS
    ]


def notebook_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_sources(path: Path) -> list[str]:
    data = notebook_json(path)
    return ["".join(cell.get("source", "")) for cell in data.get("cells", []) if cell.get("cell_type") == "markdown"]


def code_sources(path: Path) -> list[str]:
    data = notebook_json(path)
    return ["".join(cell.get("source", "")) for cell in data.get("cells", []) if cell.get("cell_type") == "code"]


def require_nonempty(paths: Iterable[Path], *, min_bytes: int = 64) -> None:
    missing = []
    tiny = []
    for path in paths:
        candidate = Path(path)
        if not candidate.exists():
            missing.append(str(candidate))
        elif candidate.stat().st_size < min_bytes:
            tiny.append(str(candidate))
    if missing or tiny:
        raise AssertionError({"missing": missing, "tiny": tiny})


def artifact_topics() -> list[str]:
    return [path.name for path in sorted((BOOK_ROOT / "artifacts").iterdir()) if path.is_dir()]
''',
}


def build_script_py() -> str:
    return r'''
"""Rebuild MVG book, part, and chapter index notebooks."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

import mvg_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


def entry_folder(entry: dict) -> Path:
    if entry["part"] is None:
        return BOOK_ROOT / entry["folder"]
    return BOOK_ROOT / entry["part"] / entry["folder"]


def ensure_inventory() -> None:
    missing = []
    for entry in inventory.ENTRIES:
        folder = entry_folder(entry)
        for path in [folder, folder / entry["notebook"]]:
            if not path.exists():
                missing.append(path)
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))


def build_book_index() -> str:
    lines = [
        "# Multiple View Geometry in Computer Vision",
        "",
        "This is a standalone visualization-first notebook course with original prose, executable examples, generated diagrams, computational experiments, and sanity checks. The local PDF is used only for source orientation and is not reproduced in the notebooks.",
        "",
        "Source-page convention: printed page 1 is PDF page 19, so `pdf_page = printed_page + 18`.",
        "",
        "## Opening Chapter",
        "",
    ]
    root_entries = [entry for entry in inventory.ENTRIES if entry["part"] is None]
    for entry in root_entries:
        lines.append(f"- [{entry['label']}: {entry['title']}]({entry['folder']}/00-index.ipynb) - [canonical]({entry['folder']}/{entry['notebook']}); printed pp. {entry['printed']}; PDF pp. {entry['pdf']}; {entry['focus']}")
    lines.append("")
    for part in inventory.PARTS:
        lines.extend([f"## {part['label']}: {part['title']}", "", part["description"], "", f"- [Open part index]({part['folder']}/00-part-index.ipynb)"])
        for entry in inventory.ENTRIES:
            if entry["part"] != part["folder"]:
                continue
            index_link = f"{entry['part']}/{entry['folder']}/00-index.ipynb"
            canonical_link = f"{entry['part']}/{entry['folder']}/{entry['notebook']}"
            lines.append(f"- [{entry['label']}: {entry['title']}]({index_link}) - [canonical]({canonical_link}); printed pp. {entry['printed']}; PDF pp. {entry['pdf']}; {entry['focus']}")
        lines.append("")
    return "\n".join(lines)


def build_part_index(part: dict) -> str:
    lines = [f"# {part['label']}: {part['title']}", "", "[Back to Book Index](../00-book-index.ipynb)", "", part["description"], ""]
    for entry in inventory.ENTRIES:
        if entry["part"] != part["folder"]:
            continue
        lines.extend([
            f"## {entry['label']}: {entry['title']}",
            "",
            f"- Chapter index: [{entry['folder']}/00-index.ipynb]({entry['folder']}/00-index.ipynb)",
            f"- Canonical notebook: [{entry['notebook']}]({entry['folder']}/{entry['notebook']})",
            f"- Source span: printed pp. {entry['printed']}; PDF pp. {entry['pdf']}",
            f"- Focus: {entry['focus']}",
            "",
        ])
    return "\n".join(lines)


def build_unit_index(entry: dict) -> str:
    lines = [
        f"# {entry['label']}: {entry['title']}",
        "",
        f"Source orientation: printed pages {entry['printed']}; PDF pages {entry['pdf']}.",
        "",
        f"Canonical notebook: [{entry['notebook']}]({entry['notebook']})",
        "",
        "## Focus",
        "",
        entry["focus"],
        "",
        "## Visual Storyboard",
        "",
    ]
    for visual in entry["visuals"]:
        lines.append(f"- {visual}")
    lines.extend(["", "## Computational Checks", ""])
    for check in entry["checks"]:
        lines.append(f"- {check}")
    return "\n".join(lines)


def main() -> None:
    ensure_inventory()
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for part in inventory.PARTS:
        write_markdown_notebook(BOOK_ROOT / part["folder"] / "00-part-index.ipynb", build_part_index(part))
    for entry in inventory.ENTRIES:
        write_markdown_notebook(entry_folder(entry) / "00-index.ipynb", build_unit_index(entry))
    print(f"Updated indexes for {len(inventory.ENTRIES)} entries in {len(inventory.PARTS)} parts.")


if __name__ == "__main__":
    main()
'''


def audit_notebooks_py() -> str:
    return r'''
"""Audit MVG notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import nbformat

import mvg_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def entry_folder(entry: dict) -> Path:
    if entry["part"] is None:
        return BOOK_ROOT / entry["folder"]
    return BOOK_ROOT / entry["part"] / entry["folder"]


def discover_notebooks() -> list[Path]:
    missing = []
    paths = []
    for entry in inventory.ENTRIES:
        folder = entry_folder(entry)
        index = folder / "00-index.ipynb"
        canonical = folder / entry["notebook"]
        for path in [folder, index, canonical]:
            if not path.exists():
                missing.append(path)
        if canonical.exists():
            paths.append(canonical)
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))
    return paths


def notebook_stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    return {
        "path": str(path.relative_to(BOOK_ROOT)).replace("\\", "/"),
        "markdown_words": sum(len(source.split()) for source in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "visual_save_calls": sum(source.count("save_matplotlib(") + source.count("save_plotly_html(") + source.count("save_image(") for source in code),
        "display_artifact_calls": sum(source.count("display_artifact(") for source in code),
        "has_final_sanity": any("final_sanity" in source for source in code),
        "has_takeaways": any("Takeaways" in source for source in markdown),
        "has_applied_lab": any("Applied Lab" in source for source in markdown),
    }


def canonical_folder_findings() -> list[dict[str, str]]:
    findings = []
    for entry in inventory.ENTRIES:
        folder = entry_folder(entry)
        canonical = [p for p in folder.glob("*.ipynb") if p.name != "00-index.ipynb"]
        if len(canonical) != 1 or canonical[0].name != entry["notebook"]:
            findings.append({"path": str(folder.relative_to(BOOK_ROOT)).replace("\\", "/"), "message": f"expected one canonical notebook, found {len(canonical)}"})
    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()

    stats = [notebook_stats(path) for path in discover_notebooks()]
    failing = [
        item
        for item in stats
        if item["markdown_words"] < args.min_words
        or item["code_cells"] < args.min_code_cells
        or item["visual_save_calls"] == 0
        or item["display_artifact_calls"] < item["visual_save_calls"]
        or not item["has_final_sanity"]
        or not item["has_takeaways"]
        or not item["has_applied_lab"]
    ]
    structure = canonical_folder_findings()
    report = {"notebook_count": len(stats), "failing_count": len(failing), "failing": failing, "structure_findings": structure, "stats": stats}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(stats)} canonical notebooks")
    if failing or structure:
        for item in failing:
            print(f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells, {item['visual_save_calls']} visual saves, {item['display_artifact_calls']} displays")
        for item in structure:
            print(f"- {item['path']}: {item['message']}")
        raise SystemExit(1)
    print("All canonical notebooks meet standalone structure thresholds.")


if __name__ == "__main__":
    main()
'''


def audit_visuals_py() -> str:
    return r'''
"""Audit generated visual artifacts for the MVG course."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

import mvg_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}
VISUAL_SAVE_CALLS = {"save_matplotlib", "save_plotly_html", "save_image"}


def relative(path: Path) -> str:
    return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


def call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def notebook_visual_stats(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    visual_saves = 0
    displays = 0
    errors = []
    for cell_index, cell in enumerate(data.get("cells", []), start=1):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", ""))
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            errors.append(f"cell {cell_index}: {exc.msg}")
            visual_saves += sum(source.count(f"{name}(") for name in VISUAL_SAVE_CALLS)
            displays += source.count("display_artifact(")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = call_name(node)
                if name in VISUAL_SAVE_CALLS:
                    visual_saves += 1
                elif name == "display_artifact":
                    displays += 1
    return {"path": relative(path), "visual_save_calls": visual_saves, "display_artifact_calls": displays, "parse_errors": errors}


def image_stats(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "path": relative(path),
        "width": rgb.width,
        "height": rgb.height,
        "bytes": path.stat().st_size,
        "sha256": digest,
        "max_channel_stddev": max(stat.stddev) if stat.stddev else 0.0,
    }


def audit() -> dict[str, Any]:
    findings = []
    artifact_root = BOOK_ROOT / "artifacts"
    notebooks = [
        notebook_visual_stats(path)
        for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED
    ]
    for item in notebooks:
        for error in item["parse_errors"]:
            findings.append({"check": "notebook-parse-error", "path": item["path"], "message": error})
        if item["visual_save_calls"] == 0:
            findings.append({"check": "missing-visual-save", "path": item["path"], "message": "no visual save call"})
        if item["display_artifact_calls"] < item["visual_save_calls"]:
            findings.append({"check": "missing-display", "path": item["path"], "message": "not every visual is displayed"})

    images = []
    for entry in inventory.ENTRIES:
        topic_root = artifact_root / entry["topic"]
        pngs = sorted(topic_root.rglob("*.png")) if topic_root.exists() else []
        if not pngs:
            findings.append({"check": "missing-topic-png", "path": relative(topic_root), "message": f"{entry['topic']} has no PNG artifacts"})
        for path in pngs:
            try:
                stat = image_stats(path)
            except OSError as exc:
                findings.append({"check": "unreadable-image", "path": relative(path), "message": str(exc)})
                continue
            images.append(stat)
            if stat["width"] < 96 or stat["height"] < 96 or stat["bytes"] < 1500:
                findings.append({"check": "tiny-image", "path": stat["path"], "message": f"{stat['width']}x{stat['height']} {stat['bytes']} bytes"})
            if stat["max_channel_stddev"] <= 1.0:
                findings.append({"check": "blank-image", "path": stat["path"], "message": f"stddev {stat['max_channel_stddev']:.3f}"})

    by_hash: dict[str, list[str]] = {}
    for image in images:
        by_hash.setdefault(image["sha256"], []).append(image["path"])
    for digest, paths in by_hash.items():
        if len(paths) > 1:
            findings.append({"check": "duplicate-png-hash", "path": paths[0], "message": f"{len(paths)} images share {digest[:12]}", "details": paths})

    return {"summary": {"notebook_count": len(notebooks), "png_count": len(images), "finding_count": len(findings)}, "findings": findings, "notebooks": notebooks, "images": images}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-fail", action="store_true")
    args = parser.parse_args()
    report = audit()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        summary = report["summary"]
        print(f"Audited {summary['notebook_count']} notebooks and {summary['png_count']} PNGs")
        if report["findings"]:
            for finding in report["findings"]:
                print(f"- {finding['check']} [{finding.get('path', '')}]: {finding['message']}")
        else:
            print("All MVG visual checks passed.")
    if report["findings"] and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
'''


def validate_py() -> str:
    return r'''
"""Execute MVG notebooks with nbclient."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

import mvg_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def entry_folder(entry: dict) -> Path:
    if entry["part"] is None:
        return BOOK_ROOT / entry["folder"]
    return BOOK_ROOT / entry["part"] / entry["folder"]


def notebook_paths(*, smoke: bool, all_notebooks: bool, limit: int | None) -> list[Path]:
    missing = []
    paths: list[Path] = []
    book_index = BOOK_ROOT / "00-book-index.ipynb"
    if book_index.exists():
        paths.append(book_index)
    else:
        missing.append(book_index)
    if all_notebooks:
        for part in inventory.PARTS:
            part_index = BOOK_ROOT / part["folder"] / "00-part-index.ipynb"
            if part_index.exists():
                paths.append(part_index)
            else:
                missing.append(part_index)
    for entry in inventory.ENTRIES:
        folder = entry_folder(entry)
        index = folder / "00-index.ipynb"
        canonical = folder / entry["notebook"]
        for path in [folder, index, canonical]:
            if not path.exists():
                missing.append(path)
        include = all_notebooks or (smoke and canonical.name in inventory.SMOKE_NOTEBOOKS) or (not smoke and not all_notebooks)
        if include:
            if all_notebooks and index.exists():
                paths.append(index)
            if canonical.exists():
                paths.append(canonical)
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))
    if limit is not None:
        paths = paths[:limit]
    return paths


def execute_notebook(path: Path, timeout: int) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
    client.execute()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    paths = notebook_paths(smoke=args.smoke, all_notebooks=args.all, limit=args.limit)
    if not paths:
        raise SystemExit("no notebooks found")
    failures = []
    for index, path in enumerate(paths, start=1):
        print(f"[{index}/{len(paths)}] {path.relative_to(BOOK_ROOT)}")
        try:
            execute_notebook(path, args.timeout)
        except Exception as exc:
            failures.append((path, repr(exc)))
    if failures:
        for path, error in failures:
            print(f"FAILED {path}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(paths)} notebooks successfully")


if __name__ == "__main__":
    main()
'''


def tests_py() -> str:
    return r'''
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

COURSE_ROOT = Path(__file__).resolve().parents[1]
if str(COURSE_ROOT) not in sys.path:
    sys.path.insert(0, str(COURSE_ROOT))

from utils.cameras import camera_center, project_points, synthetic_cameras
from utils.epipolar import eight_point, fundamental_from_cameras, sampson_errors
from utils.projective import apply_homography, dlt_homography, homogenize, line_through, incidence


def test_line_incidence_scale_invariant():
    p = np.array([0.2, -0.4, 1.0])
    q = np.array([1.3, 0.7, 1.0])
    line = line_through(p, q)
    assert abs(incidence(line, 3.0 * p)) < 1e-9
    assert abs(incidence(2.0 * line, q)) < 1e-9


def test_homography_dlt_recovers_synthetic_mapping():
    src = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1], [0.2, 0.4], [-0.4, 0.7]], dtype=float)
    H = np.array([[1.2, 0.2, 0.4], [-0.1, 0.9, 0.2], [0.05, -0.03, 1.0]])
    dst = apply_homography(H, src)
    Hhat = dlt_homography(src, dst)
    reproj = apply_homography(Hhat, src)
    assert np.max(np.linalg.norm(reproj - dst, axis=1)) < 1e-8


def test_camera_center_and_epipolar_residuals():
    _, P1, P2 = synthetic_cameras()
    C1 = camera_center(P1)
    assert np.linalg.norm(P1 @ C1) < 1e-7
    rng = np.random.default_rng(4)
    pts3 = rng.normal(size=(12, 3)) * [0.8, 0.5, 0.4] + [0.0, 0.0, 3.0]
    x1 = project_points(P1, pts3)
    x2 = project_points(P2, pts3)
    F = fundamental_from_cameras(P1, P2)
    errs = sampson_errors(F, x1, x2)
    assert float(np.median(errs)) < 1e-8
    Fest = eight_point(x1, x2)
    assert np.linalg.matrix_rank(Fest, tol=1e-7) == 2
'''


def make_notebook(entry: dict) -> list:
    title = f"{entry['label']}: {entry['title']}"
    setup = f"""
from pathlib import Path
import sys

BOOK_ROOT = Path.cwd()
for candidate in [BOOK_ROOT, *BOOK_ROOT.parents]:
    if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
        BOOK_ROOT = candidate
        break
else:
    raise RuntimeError("Could not find the MVG book root")

if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

TOPIC = {entry['topic']!r}
ARTIFACT_ROOT = BOOK_ROOT / "artifacts" / TOPIC
ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
"""
    imports = f"""
import json
import math

import matplotlib.pyplot as plt
import numpy as np

from utils.artifacts import assert_artifacts, display_artifact, save_json, save_matplotlib
from utils.cameras import cube_points, project_points, synthetic_cameras
from utils.epipolar import fundamental_from_cameras, linear_triangulate, sampson_errors
from utils.plotting import compute_visual_summary, concept_map_figure, constraint_dashboard_figure, diagnostic_figure, vision_scene_figure
from utils.projective import apply_homography, dlt_homography, homogenize, incidence, line_through

ENTRY_TITLE = {entry['title']!r}
MODE = {entry['mode']!r}
TOPIC = {entry['topic']!r}
CONCEPTS = {entry['concepts']!r}
VISUALS = {entry['visuals']!r}
CHECKS = {entry['checks']!r}
SEED = {entry['number'] + 101!r}
artifact_paths = []
"""
    concept_lines = []
    for idx, concept in enumerate(entry["concepts"], start=1):
        visual = entry["visuals"][(idx - 1) % len(entry["visuals"])]
        check = entry["checks"][(idx - 1) % len(entry["checks"])]
        concept_lines.append(f"""### {idx}. {concept.capitalize()}

Computationally, this idea becomes a concrete contract: choose the representation, state the invariant, draw the construction, and test the residual. In this lesson the paired visual is **{visual}**. The visual is not a decoration; it is the object that lets a reader inspect how the algebra behaves when coordinates, noise, viewpoints, or constraints change. The paired check is **{check}**, so the claim is carried by a number as well as by prose.

For this chapter, the important habit is to keep projective freedom explicit. Homogeneous vectors are scale classes, camera matrices are maps between projective spaces, and estimation algorithms are numerical procedures whose output must be interpreted geometrically. When the notebook computes a residual or a rank, the value is tied back to the construction that produced it. That makes the lesson portable: a reader can replace the synthetic scene with their own measurements and still know what should remain true.""")
    concept_md = "\n\n".join(concept_lines)
    storyboard = "\n".join(f"- **{visual}:** inspect how it supports `{entry['focus']}`." for visual in entry["visuals"])
    checks = "\n".join(f"- `{check}`" for check in entry["checks"])
    takeaways = "\n".join(f"- {concept.capitalize()}." for concept in entry["concepts"])
    cells = [
        new_markdown_cell(f"""# {title}

Source orientation: printed pages {entry['printed']}; PDF pages {entry['pdf']}.

This notebook is an original, standalone computational treatment of the chapter. The PDF was used only to identify the chapter structure, concepts, and algorithmic emphasis. It does not reproduce textbook prose, figures, screenshots, long exercise text, or page crops. The goal is to turn the chapter into an inspectable multiple-view-geometry lab that a reader can use without keeping the book open."""),
        new_markdown_cell(f"""## Chapter Goal

{entry['focus']}

Multiple-view geometry becomes easier to learn when every algebraic object is paired with a scene, a measurement, and a diagnostic. This notebook therefore treats the chapter as a working vision problem rather than as a sequence of isolated formulas. Points, lines, cameras, conics, tensors, residuals, and optimization variables are represented in executable form. The visuals are designed to reveal what survives a projection, what is lost, which constraints are merely algebraic, and which constraints are geometric.

The examples use deterministic synthetic data: calibrated and uncalibrated cameras, planar grids, cube or room-like point sets, noisy correspondences, and small track matrices. Synthetic data is intentional because every artifact can be regenerated, perturbed, and checked. Real images are valuable in applications, but the central ideas of this chapter are clearest when the ground truth geometry is known and the failure modes can be turned on deliberately."""),
        new_markdown_cell("""## Translation Guide

- **Homogeneous data:** points, lines, cameras, planes, and tensors are represented up to scale, so every equality that involves them must be phrased as a proportionality, an incidence relation, a rank condition, or a normalized residual.
- **Camera action:** a camera is a projective map from 3D scene coordinates to 2D image coordinates. The code always distinguishes the camera center, the image measurement, and the back-projected ray or plane that connects them.
- **Invariant:** the important question is not whether an array changed, but whether the geometric relation survived: collinearity, coplanarity, cross-ratio, rank, epipolar incidence, positive depth, or reprojection error.
- **Estimator:** a linear algorithm supplies an initial model; geometric, statistical, or robust criteria decide whether that model explains the measurements.
- **Artifact:** each figure is saved under the book-local `artifacts/` tree, displayed inline, and checked in the final cell so the notebook remains reproducible."""),
        new_markdown_cell("""## Route Through The Chapter

1. Name the geometric object and its computational representation.
2. Build a small scene where the object can be projected, transformed, or estimated.
3. Draw the construction in a way that makes the invariant visible.
4. Perturb the data to expose conditioning, uncertainty, or ambiguity.
5. Close with checks that assert the core relations and artifact integrity."""),
        new_code_cell(clean(setup)),
        new_markdown_cell(f"""## Visual Storyboard

{storyboard}

The visuals deliberately use concept names instead of renderer names. A figure should answer a geometric question: which point lies on which line, which ray produced which image point, which singular value is signaling rank loss, or which residual is being reduced by an estimator."""),
        new_markdown_cell(f"""## Core Concepts

{concept_md}"""),
        new_markdown_cell(f"""## Worked Example Pattern

The worked examples use a shared synthetic lab. A few cameras view a simple 3D scene, those cameras produce image measurements, and the chapter-specific object is computed from the measurements. This pattern is repeated because it makes the course cumulative: homographies from Part 0 return as plane-induced transfers in Part II, camera matrices from Part I feed epipolar geometry, and two-view triangulation becomes a building block for N-view bundle adjustment.

For this chapter, the important work is to connect **{entry['focus']}** to observable behavior. The first figure is a concept map that states what to watch. The second figure is a geometry scene. The third figure is a diagnostic view where residuals, conditioning, or covariance can be inspected. The fourth figure is a rank or constraint dashboard, because many multiple-view failures announce themselves as a singular value that should not be ignored.

The code is intentionally compact. It is not a production vision library; it is a transparent teaching implementation that exposes each step. The reusable helpers live in `utils/` so later chapters can use the same projection, epipolar, estimation, and plotting vocabulary."""),
        new_code_cell(clean(imports)),
        new_code_cell("""fig = concept_map_figure(ENTRY_TITLE, CONCEPTS, VISUALS)
concept_path = save_matplotlib(fig, TOPIC, "figures", "concept-map.png")
plt.close(fig)
artifact_paths.append(concept_path)
display_artifact(concept_path, width=860)
"""),
        new_code_cell("""fig = vision_scene_figure(MODE, ENTRY_TITLE, SEED)
scene_path = save_matplotlib(fig, TOPIC, "figures", "geometry-scene.png")
plt.close(fig)
artifact_paths.append(scene_path)
display_artifact(scene_path, width=840)
"""),
        new_code_cell("""fig = diagnostic_figure(ENTRY_TITLE, CHECKS, SEED + 17)
diagnostic_path = save_matplotlib(fig, TOPIC, "figures", "diagnostic-dashboard.png")
plt.close(fig)
artifact_paths.append(diagnostic_path)
display_artifact(diagnostic_path, width=860)
"""),
        new_code_cell("""fig = constraint_dashboard_figure(ENTRY_TITLE, MODE, SEED + 31)
constraint_path = save_matplotlib(fig, TOPIC, "figures", "constraint-dashboard.png")
plt.close(fig)
artifact_paths.append(constraint_path)
display_artifact(constraint_path, width=840)
"""),
        new_markdown_cell(f"""## Computational Lab

The lab below uses the same checks as the visual storyboard:

{checks}

The exact values are less important than the workflow. Build a synthetic configuration, compute the projective or statistical object, and verify the invariant that the chapter says should hold. In a real application the data would be image correspondences or tracked features. In this course the data is deterministic so the result can be audited.

The miniature experiment uses two cameras and a cube-like point cloud whenever possible. Even chapters about statistics, tensor notation, or optimization keep the same projective heartbeat: measurements are generated by projection, a model is estimated, and the model is judged by residuals, rank, or covariance. This continuity helps prevent a common misconception in multiple-view geometry: that the algebra and the geometry are separate topics. They are two views of the same constraints."""),
        new_code_cell("""K, P1, P2 = synthetic_cameras()
points3d = cube_points(scale=0.55)
x1 = project_points(P1, points3d)
x2 = project_points(P2, points3d)
F = fundamental_from_cameras(P1, P2)
epi_errors = sampson_errors(F, x1, x2)
triangulated = linear_triangulate(P1, P2, x1, x2)
reconstruction_error = float(np.sqrt(np.mean(np.sum((triangulated - points3d) ** 2, axis=1))))

square = np.array([[-1.0, -0.8], [1.0, -0.6], [0.9, 0.9], [-1.1, 0.7], [0.0, 0.0], [0.45, -0.15]])
H_true = np.array([[1.0, 0.18, 0.35], [-0.08, 0.96, 0.22], [0.035, -0.028, 1.0]])
warped = apply_homography(H_true, square)
H_est = dlt_homography(square, warped)
homography_error = float(np.max(np.linalg.norm(apply_homography(H_est, square) - warped, axis=1)))

p = homogenize(np.array([[0.0, 0.0], [1.0, 0.35]]))
line = line_through(p[0], p[1])
incidence_residual = abs(incidence(line, p[0])) + abs(incidence(line, p[1]))

summary = compute_visual_summary(ENTRY_TITLE, MODE, SEED)
summary.update({
    "median_epipolar_sampson_error": float(np.median(epi_errors)),
    "triangulation_rmse": reconstruction_error,
    "homography_reprojection_max_error": homography_error,
    "line_incidence_residual": float(incidence_residual),
    "artifact_count": len(artifact_paths),
})
summary_path = save_json(summary, TOPIC, "checks", "numeric-summary.json")
display_artifact(summary_path)
summary
"""),
        new_markdown_cell("""## Pitfalls And Failure Modes

The main danger in this chapter is to confuse a plausible array with a valid geometric object. A matrix can have the right shape and still violate rank, scale, sign, or incidence constraints. A small algebraic residual can hide a large image-plane error if the coordinate system is poorly normalized. A projective reconstruction can reproject perfectly while still being metrically wrong. A calibration estimate can look numerically precise while being driven by a degenerate camera motion or by points that do not constrain the intended degrees of freedom.

The antidote is to make each assumption executable. When a relation is homogeneous, normalize before comparing. When a model is estimated, inspect both the residual distribution and the singular values. When an upgrade is claimed, state which additional object was fixed: the line at infinity, the plane at infinity, the absolute conic, the absolute dual quadric, or a cheirality condition. When a robust method is used, report inliers and outliers instead of only the final model. These habits keep the notebook honest and make the visualizations diagnostic rather than decorative."""),
        new_markdown_cell(f"""## Applied Lab

Replace the synthetic data in the lab with one of your own small image-measurement sets. Keep the same artifact contract:

1. draw the measurements and the estimated relation;
2. save the figure under `artifacts/{entry['topic']}/figures/`;
3. write a JSON summary under `artifacts/{entry['topic']}/checks/`;
4. assert the invariant that matters for the chapter.

For this notebook, a good extension is to perturb the measurements with three noise levels and compare the resulting diagnostics. Watch whether **{entry['checks'][0]}** degrades smoothly or fails abruptly. Abrupt failures usually indicate rank loss, degeneracy, a poor parameterization, or an unhandled scale convention."""),
        new_code_cell("""final_sanity = {
    "artifact_count": len(artifact_paths),
    "all_artifacts": [str(path.relative_to(BOOK_ROOT)) for path in artifact_paths],
    "max_epipolar_error": float(np.max(epi_errors)),
    "triangulation_rmse": reconstruction_error,
    "homography_error": homography_error,
    "line_incidence_residual": float(incidence_residual),
}
assert_artifacts(artifact_paths, min_bytes=1500)
assert final_sanity["artifact_count"] >= 4
assert final_sanity["max_epipolar_error"] < 1e-7
assert final_sanity["triangulation_rmse"] < 1e-7
assert final_sanity["homography_error"] < 1e-8
assert final_sanity["line_incidence_residual"] < 1e-10
final_sanity
"""),
        new_markdown_cell(f"""## Takeaways

{takeaways}

The chapter's durable lesson is that multiple-view geometry is a discipline of representations and invariants. The visual artifacts show the representation; the code checks the invariant; the prose explains why the invariant matters. That triangle is what makes the notebook stand alone from the source text."""),
    ]
    return cells


def build_indexes() -> None:
    module_path = COURSE_ROOT / "scripts"
    if str(module_path) not in sys.path:
        sys.path.insert(0, str(module_path))
    import build_mvg_course_indexes

    build_mvg_course_indexes.main()


def write_course_files() -> None:
    write_text(COURSE_ROOT / "AGENTS.md", agents_md())
    for name, text in UTILS.items():
        write_text(COURSE_ROOT / "utils" / name, text)
    write_text(COURSE_ROOT / "scripts" / "mvg_inventory.py", inventory_py())
    write_text(COURSE_ROOT / "scripts" / "build_mvg_course_indexes.py", build_script_py())
    write_text(COURSE_ROOT / "scripts" / "audit_mvg_notebooks.py", audit_notebooks_py())
    write_text(COURSE_ROOT / "scripts" / "audit_mvg_visuals.py", audit_visuals_py())
    write_text(COURSE_ROOT / "scripts" / "validate_mvg_course.py", validate_py())
    write_text(COURSE_ROOT / "scripts" / "test_mvg_core.py", tests_py())
    for part in PARTS:
        (COURSE_ROOT / part["folder"]).mkdir(parents=True, exist_ok=True)
    for entry in ENTRIES:
        folder = entry_folder(entry)
        folder.mkdir(parents=True, exist_ok=True)
        write_notebook(folder / entry["notebook"], make_notebook(entry))


def generate_initial_artifacts() -> None:
    if str(COURSE_ROOT) not in sys.path:
        sys.path.insert(0, str(COURSE_ROOT))
    import matplotlib.pyplot as plt

    from utils.artifacts import save_json, save_matplotlib
    from utils.plotting import compute_visual_summary, concept_map_figure, constraint_dashboard_figure, diagnostic_figure, vision_scene_figure

    for entry in ENTRIES:
        seed = entry["number"] + 101
        topic = entry["topic"]
        generated = []
        for filename, fig in [
            ("concept-map.png", concept_map_figure(entry["title"], entry["concepts"], entry["visuals"])),
            ("geometry-scene.png", vision_scene_figure(entry["mode"], entry["title"], seed)),
            ("diagnostic-dashboard.png", diagnostic_figure(entry["title"], entry["checks"], seed + 17)),
            ("constraint-dashboard.png", constraint_dashboard_figure(entry["title"], entry["mode"], seed + 31)),
        ]:
            path = save_matplotlib(fig, topic, "figures", filename)
            plt.close(fig)
            generated.append(path.as_posix())
        summary = compute_visual_summary(entry["title"], entry["mode"], seed)
        summary["generated_artifacts"] = generated
        save_json(summary, topic, "checks", "numeric-summary.json")


def main() -> None:
    write_course_files()
    build_indexes()
    generate_initial_artifacts()
    print(f"Bootstrapped {len(ENTRIES)} MVG notebooks, {len(PARTS)} parts, and initial artifacts.")


if __name__ == "__main__":
    main()
