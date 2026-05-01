# Agent Instructions: Introduction to Geometry Notebook Course

This folder is a standalone visualization-first notebook edition of Introduction to Geometry, Second Edition, by H. S. M. Coxeter. Treat this folder as the project root for this course. The workspace root owns the shared uv environment.

## Repo-Local Skills

Use the repo-local skills under D:\Geometry\.codex\skills:

- geometry-visualization-planner before planning a chapter storyboard.
- geometry-chapter-notebook-author when authoring canonical notebooks.
- geometry-notebook-qc when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or textbook figures.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualization is part of the explanation, not decoration or a quota.
- Keep helpers in utils/, generated outputs in artifacts/, and validation tools in scripts/.
- Every canonical notebook must execute with nbclient.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook per chapter folder plus a local 00-index.ipynb.

## Source Map

The PDF is scanned/image-only and has 487 physical pages. Body printed pages map to PDF pages by pdf_page = printed_page + 18. The book has four parts, 22 chapters, tables, references, answers to exercises, and an index. It has no appendices.

| Part | Chapter | Folder | Printed Pages | PDF Pages | Focus |
| --- | --- | --- | ---: | ---: | --- |
| I | 01. Triangles | chapter-01-triangles | 3-25 | 21-43 | Euclid, primitive concepts, congruence, medians and centroid, incenter, circumcenter, Euler line, nine-point circle, extremum problems, and Morley-style angle trisectors |
| I | 02. Regular Polygons | chapter-02-regular-polygons | 26-38 | 44-56 | cyclotomy, angle trisection, isometry, symmetry groups, products of reflections, kaleidoscopes, and star polygons |
| I | 03. Isometry in the Euclidean Plane | chapter-03-isometry-in-the-euclidean-plane | 39-49 | 57-67 | direct and opposite isometries, translations, glide reflections, half-turns, reflection products, and strip patterns |
| I | 04. Two-Dimensional Crystallography | chapter-04-two-dimensional-crystallography | 50-66 | 68-84 | lattices, Dirichlet regions, general lattice symmetry, Escher-style motifs, six brick patterns, crystallographic restriction, tessellations, and collinear-point problems |
| I | 05. Similarity in the Euclidean Plane | chapter-05-similarity-in-the-euclidean-plane | 67-76 | 85-94 | dilation, centers of similitude, nine-point center, invariant point of a similarity, direct similarity, and opposite similarity |
| I | 06. Circles and Spheres | chapter-06-circles-and-spheres | 77-95 | 95-113 | circle inversion, orthogonal circles, inversions of lines and circles, inverse plane, coaxal circles, Apollonius circles, circle-preserving transformations, sphere inversion, and the elliptic plane |
| I | 07. Isometry and Similarity in Euclidean Space | chapter-07-isometry-and-similarity-in-euclidean-space | 96-106 | 114-124 | direct and opposite spatial isometries, central inversion, rotations and translations, products of reflections, twists, dilative rotations, and sphere-preserving transformations |
| II | 08. Coordinates | chapter-08-coordinates | 107-134 | 125-152 | Cartesian coordinates, polar coordinates, circles, conics, tangent, arc length, area, hyperbolic functions, equiangular spiral, and three dimensions |
| II | 09. Complex Numbers | chapter-09-complex-numbers | 135-147 | 153-165 | rational and real numbers, Argand diagrams, modulus and amplitude, Euler formula, roots of equations, and conformal transformations |
| II | 10. The Five Platonic Solids | chapter-10-the-five-platonic-solids | 148-159 | 166-177 | pyramids, prisms, antiprisms, drawings and models, Euler formula, radii and angles, and reciprocal polyhedra |
| II | 11. The Golden Section and Phyllotaxis | chapter-11-the-golden-section-and-phyllotaxis | 160-174 | 178-192 | extreme and mean ratio, divine proportion, golden spiral, Fibonacci numbers, and phyllotaxis |
| III | 12. Ordered Geometry | chapter-12-ordered-geometry | 175-190 | 193-208 | extracting geometries from Euclid, intermediacy, collinear point problems, planes and hyperplanes, continuity, and parallelism |
| III | 13. Affine Geometry | chapter-13-affine-geometry | 191-228 | 209-246 | parallelism, Desargues axiom, dilatations, affinities, equiaffinities, lattices, vectors and centroids, barycentric coordinates, affine space, and three-dimensional lattices |
| III | 14. Projective Geometry | chapter-14-projective-geometry | 229-262 | 247-280 | projective-plane axioms, projective coordinates, Desargues theorem, quadrangular and harmonic sets, projectivities, collineations, correlations, conics, projective space, and Euclidean space |
| III | 15. Absolute Geometry | chapter-15-absolute-geometry | 263-286 | 281-304 | congruence, parallelism, isometry, finite rotation groups, finite isometry groups, geometrical crystallography, polyhedral kaleidoscopes, and discrete groups generated by inversions |
| III | 16. Hyperbolic Geometry | chapter-16-hyperbolic-geometry | 287-306 | 305-324 | Euclidean and hyperbolic parallel axioms, consistency, angle of parallelism, finiteness of triangles, area defect, equidistant curves, Poincare half-plane model, horospheres, and Euclidean interpretation |
| IV | 17. Differential Geometry of Curves | chapter-17-differential-geometry-of-curves | 307-327 | 325-345 | vectors in Euclidean space, vector functions, curvature, evolutes, involutes, catenary, tractrix, twisted curves, circular helix, general helix, and concho-spiral |
| IV | 18. The Tensor Notation | chapter-18-the-tensor-notation | 328-341 | 346-359 | dual bases, fundamental tensor, reciprocal lattices, critical lattice of a sphere, general coordinates, and alternating symbol |
| IV | 19. Differential Geometry of Surfaces | chapter-19-differential-geometry-of-surfaces | 342-365 | 360-383 | two-parameter surface patches, directions on a surface, normal curvature, principal curvatures, principal directions, umbilics, Dupin and Liouville theorems, and Dupin indicatrix |
| IV | 20. Geodesics | chapter-20-geodesics | 366-378 | 384-396 | theorema egregium, differential equations for geodesics, integral curvature of geodesic triangles, Euler-Poincare characteristic, constant-curvature surfaces, angle of parallelism, and pseudosphere |
| IV | 21. Topology of Surfaces | chapter-21-topology-of-surfaces | 379-395 | 397-413 | orientable surfaces, nonorientable surfaces, regular maps, four-color problem, six-color theorem, sufficient colors for arbitrary surfaces, and surfaces requiring full color counts |
| IV | 22. Four-Dimensional Geometry | chapter-22-four-dimensional-geometry | 396-412 | 414-430 | simple four-dimensional figures, conditions for honeycomb symbols, regular polytopes, close packing of equal spheres, and statistical honeycombs |

## Artifact Contract

Store generated outputs under artifacts/chapter-XX/{figures,html,checks,tables,data}/. Artifact filenames should name the concept, every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Commands

Run from D:\Geometry:

uv run python "Introduction-to-Geometry/scripts/build_itg_course_indexes.py"
uv run python -m compileall -q "Introduction-to-Geometry/utils" "Introduction-to-Geometry/scripts"
uv run python "Introduction-to-Geometry/scripts/audit_itg_notebooks.py" --min-words 1200 --min-code-cells 5
uv run python "Introduction-to-Geometry/scripts/audit_itg_visuals.py"
uv run python "Introduction-to-Geometry/scripts/validate_itg_course.py" --limit 6 --timeout 300
git diff --check

Run uv sync only if pyproject.toml or uv.lock changes.

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
