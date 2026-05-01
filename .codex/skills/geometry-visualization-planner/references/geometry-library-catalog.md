# Geometry Library Catalog

This workspace uses `uv` with Python 3.13. Prefer installed libraries before adding dependencies. Start from the chapter concept, choose the representation, then choose the smallest reliable library that makes the geometry inspectable.

Use this catalog to prevent generic notebooks: every major visual should name the chapter concept, representation, library choice, learner inspection target, artifact path, and check/invariant.

## Visualization Decision Table

| Chapter concept | Preferred route | Check or invariant |
| --- | --- | --- |
| Euclidean construction/proof | Matplotlib diagram plus SymPy check if algebraic | incidence, equal length/angle, area, orientation, or determinant identity |
| Affine/projective transformation | Plotly or Matplotlib plus homogeneous-coordinate SymPy check | matrix rank, cross-ratio, line preservation, determinant scale, epipolar residual |
| Surface/curvature/frame | PyVista or Trimesh plus mesh/numeric invariant checks | normals, area, Euler characteristic, principal/mean/Gaussian curvature samples |
| Mesh Laplacian/geodesic | gpytoolbox, potpourri3d, robust_laplacian, Trimesh | Laplacian symmetry, boundary count, distance sanity, spectrum or residual |
| Topological invariant/shape | Gudhi, Ripser, Persim, NetworkX | Betti numbers, persistence pairs, boundary-squared-zero, component count |
| Manifold/geodesic/statistical geometry | Geomstats or PyRiemann plus Plotly/Matplotlib | geodesic endpoints, metric symmetry, SPD eigenvalues, distance consistency |
| Exterior/geometric algebra | Galgebra, Clifford, Kingdon, PyGanja, course-local GA helpers | grade, norm, wedge/dot identities, rotor sandwich, incidence equation |
| Computational geometry algorithm | scipy.spatial, Shapely, NetworkX, Matplotlib/Plotly | orientation predicates, intersection counts, graph connectivity, Delaunay/Voronoi duality |
| Camera/projective/image chapter | OpenCV, Kornia, Torch, scikit-image, Pillow | homography reprojection error, fundamental matrix rank, epipolar distance |
| Transport/metric geometry | POT (`ot`) or GeomLoss plus Matplotlib/Plotly | mass conservation, transport cost, barycenter normalization, convergence residual |
| Geographic geometry | GIS stack only when geographic geometry is central | CRS validity, area/length units, topology validity, tile/source attribution |

## A. Core Plotting And Interaction

| Library/group | Best use cases | Use with care | Preferred artifacts and caveats | Example concepts |
| --- | --- | --- | --- | --- |
| `matplotlib` | Durable 2D diagrams, constructions, proof sketches, curves, fields, labeled static figures | 3D rotation, dense interactive scenes, mesh inspection | PNG/SVG. Use equal aspect for geometry, labels, legends, and final image-size checks. | triangle centers, angle chase, curvature graph, Voronoi overlay |
| `plotly` | Interactive 2D/3D parameter exploration, transformations, surfaces, camera views, standalone HTML | Very large meshes or notebooks that must render without browser support | HTML for interaction, PNG via `kaleido` when static export is needed. Keep file sizes reasonable. | projective transforms, surface families, geodesic parameter sliders |
| `ipywidgets` | Parameter variation where changing one variable teaches the concept | Static course exports may not preserve live controls | Pair widgets with saved static/HTML artifacts and JSON checks. | hyperbolic model parameter, curve deformation, homotopy slider |
| `ipympl` | Interactive Matplotlib inspection inside notebooks | Headless validation and static export can be fragile | Use only when notebook interactivity matters; also save PNG/SVG fallback. | draggable construction, tangent-frame inspection |

## B. 3D Geometry, Surfaces, And Meshes

| Library/group | Best use cases | Use with care | Preferred artifacts and caveats | Example concepts |
| --- | --- | --- | --- | --- |
| `pyvista`, `vtk`, `trame` | Surfaces, normals, curvature coloring, slicing, vector fields, 3D frames, web-backed 3D views | Headless rendering may need off-screen settings; avoid huge scenes | PNG for static views, HTML/trame only when interaction is essential. Record mesh stats in JSON. | shape operator, Gauss map, polyhedra, Willmore surface samples |
| `trimesh`, `meshio` | Mesh creation/loading, adjacency, topology counts, format conversion, simple geometry processing | Not a full teaching renderer by itself | OBJ/PLY/STL/GLB only when needed, PNG/HTML for display, JSON for counts. | triangulated surface, mesh normals, Euler characteristic |
| `gpytoolbox`, `potpourri3d`, `robust_laplacian` | Mesh Laplacians, geodesics, differential operators, curvature/geodesic diagnostics | Numerical tolerances and manifold/boundary assumptions matter | JSON/CSV residuals plus PNG/HTML overlays. Keep small reproducible meshes. | heat geodesics, cotangent Laplacian, eigenfunctions |
| `manifold3d`, `xatlas` | Robust mesh booleans/repair and UV parameterization/unwrapping | Use only when repair or parameterization is the chapter concept or required asset step | Mesh files plus before/after PNG and JSON validity checks. | constructive solids, atlas charts, mesh parameterization |

## C. Computational Geometry And Planar Structures

| Library/group | Best use cases | Use with care | Preferred artifacts and caveats | Example concepts |
| --- | --- | --- | --- | --- |
| `scipy.spatial` | Delaunay, Voronoi, KDTree, convex hulls, nearest neighbors | Degenerate inputs need explicit handling | PNG/SVG/HTML overlays plus JSON counts/residuals. | Delaunay triangulation, Voronoi duality, nearest site |
| `shapely` | Planar intersections, predicates, buffers, polygon validity, arrangements | CRS/geodesic questions need GIS stack; floating tolerances matter | GeoJSON/JSON plus Matplotlib/Plotly overlays. | segment intersection, polygon clipping, offset curves |
| `networkx` | Graphs, dependency diagrams, planar/mesh adjacency, proof dependency graphs | Layouts can become decorative; tie nodes/edges to the proof or algorithm | PNG/SVG plus JSON graph stats. | proof graph, visibility graph, homology boundary graph |

## D. Symbolic And Algebraic Geometry

| Library/group | Best use cases | Use with care | Preferred artifacts and caveats | Example concepts |
| --- | --- | --- | --- | --- |
| `sympy` | Exact algebra, determinants, polynomial identities, homogeneous coordinates, symbolic derivatives, small Groebner-style checks | Large polynomial systems can be slow; avoid pretending SymPy replaces Sage/Singular | Markdown equations, JSON string summaries, small exact asserts. | Ceva/Menelaus checks, cross-ratio invariance, curvature formula |
| `galgebra` | Symbolic exterior/geometric algebra identities in readable notation | Can be heavier than needed for simple linear algebra | Markdown/LaTeX displays plus exact identity checks. | wedge identities, forms, metric signatures, rotor formula |

## E. Geometric Algebra

| Library/group | Best use cases | Use with care | Preferred artifacts and caveats | Example concepts |
| --- | --- | --- | --- | --- |
| `clifford` | Numeric multivectors, rotors, conformal/projective models, geometric products | API details and metric conventions must be visible to learners | JSON checks for grades/norms/incidence plus diagrams/HTML for objects. | rotors, reflections, conformal points/spheres |
| `kingdon` | Efficient symbolic/numeric GA experiments and model-specific operations | Keep examples small and explain basis/metric choices | JSON/CSV identity checks plus readable notebook cells. | bivectors, versors, projective/conformal operators |
| `galgebra` | Exact symbolic GA derivations | Same caveats as symbolic algebra: avoid oversized expressions | Markdown/LaTeX plus exact asserts. | contraction identities, duality, blade operations |
| `pyganja` | GA visualizations when supported by the notebook environment | Rendering support can be environment-sensitive; include fallback static diagrams | HTML or screenshot-like generated artifacts only when reproducible, plus fallback PNG. | conformal primitives, lines/circles/spheres |

## F. Topology And TDA

| Library/group | Best use cases | Use with care | Preferred artifacts and caveats | Example concepts |
| --- | --- | --- | --- | --- |
| `gudhi` | Simplicial complexes, filtrations, alpha/Rips complexes, persistence computations | Filtration choices must be explained; examples should be small | Persistence diagrams PNG/SVG, JSON Betti/pair summaries. | homology, nerves, alpha complexes, filtration proofs |
| `ripser` | Fast persistent homology from point clouds/distance matrices | Point cloud examples need clear geometry, not random decoration | Persim/Matplotlib diagrams plus JSON lifetimes. | circle vs disk signatures, noisy shape invariants |
| `persim` | Persistence diagram plotting and comparisons | Diagrams need nearby prose explaining features | PNG/SVG diagrams plus bottleneck/Wasserstein summaries. | persistence interpretation, stability, feature death |

## G. Manifolds And Statistical Geometry

| Library/group | Best use cases | Use with care | Preferred artifacts and caveats | Example concepts |
| --- | --- | --- | --- | --- |
| `geomstats` | Riemannian manifolds, geodesics, metrics, exponential/log maps, Frechet means | Backend and shape conventions must be made explicit | Plotly/Matplotlib curves plus JSON distance/endpoints checks. | sphere geodesics, SPD geodesics, statistical manifolds |
| `pyriemann` | SPD covariance geometry and Riemannian signal/statistics tools | Use only when SPD/statistical geometry is central | CSV/JSON eigenvalue/distances plus plots. | covariance means, tangent-space maps, information geometry |

## H. Projective Geometry, Vision, And Image Geometry

| Library/group | Best use cases | Use with care | Preferred artifacts and caveats | Example concepts |
| --- | --- | --- | --- | --- |
| `opencv-contrib-python` / `cv2` | Homographies, epipolar geometry, calibration, feature geometry, image warps | Avoid external copyrighted images; use synthetic or permissive images | PNG overlays, JSON reprojection errors, matrix checks. | fundamental matrix, vanishing points, camera projection |
| `kornia`, `torch`, `torchvision` | Differentiable geometry, tensor image transforms, batched projective/CV operations | Heavy imports; use small tensors and CPU-friendly examples | PNG grids plus JSON tensor residuals. | differentiable homography, epipolar loss, feature maps |
| `scikit-image`, `pillow` | Image generation, filtering, morphology, IO, simple geometric transforms | Do not use textbook scans or page crops | PNG artifacts plus pixel/stat checks. | affine image warp, edge geometry, raster sampling |

## I. Optimal Transport And Metric Geometry

| Library/group | Best use cases | Use with care | Preferred artifacts and caveats | Example concepts |
| --- | --- | --- | --- | --- |
| POT / `ot` | Exact/discrete transport plans, Wasserstein distances, barycenters | Cost matrix and mass normalization must be explicit | Matplotlib/Plotly transport diagrams plus JSON mass/cost checks. | transport between point clouds, metric geometry of distributions |
| `geomloss` | Sinkhorn losses and differentiable large-ish transport examples | GPU is optional; keep examples CPU-safe and small | CSV/JSON convergence summaries plus plots. | entropic OT, barycenter path, shape matching |

## J. GIS And Geographic Geometry

Use the GIS stack only when geographic geometry is actually relevant to the chapter.

| Library/group | Best use cases | Use with care | Preferred artifacts and caveats | Example concepts |
| --- | --- | --- | --- | --- |
| `geopandas`, `shapely` | Vector geometries, spatial joins, planar topology with CRS metadata | CRS choice affects measurements; not for abstract Euclidean examples unless maps matter | GeoJSON, PNG/HTML maps, JSON validity/area checks. | geodesic vs planar area, map projections |
| `rasterio`, `fiona`, `pyproj`, `pyogrio` | Raster/vector IO, CRS transforms, robust geodata pipelines | File paths, CRS, and data licenses must be explicit | GeoTIFF/GeoJSON only when needed, plus metadata JSON. | coordinate systems, projected distance |
| `osmnx`, `contextily`, `folium`, `pydeck` | Street networks, basemap context, interactive geographic maps | Network/data fetching may need internet/cache; basemap attribution matters | HTML maps plus JSON graph/CRS summaries. | route geometry, geographic networks, map tile projections |

## K. Artifact And Rendering Support

| Library/group | Best use cases | Use with care | Preferred artifacts and caveats | Example concepts |
| --- | --- | --- | --- | --- |
| `kaleido` | Static Plotly export | Version/browser compatibility can fail; keep HTML fallback | PNG/SVG/PDF export from Plotly plus HTML fallback. | static projective transform snapshots |
| `imageio`, `imageio-ffmpeg` | Small reproducible animations or frame sequences | Avoid large videos; provide static keyframes and checks | GIF/MP4 only when motion teaches; PNG keyframes plus JSON frame metadata. | deformation, limiting process, geodesic flow |
| `pillow` | Image creation, compositing, validation, thumbnails | Use numeric checks to avoid blank/constant images | PNG plus pixel-stat JSON. | raster artifacts, masks, image geometry |
| `rich` | Readable CLI output for audits and validation scripts | Not part of notebook pedagogy unless output is shown intentionally | Console summaries, optional text artifacts. | audit reports, invariant tables |

## Optional Or External

| Tool | Status in this workspace | Guidance |
| --- | --- | --- |
| `open3d` | Not installed; available wheels may not support this CPython 3.13 environment. | Document as external or use PyVista/Trimesh instead. |
| `meshplot` | Not installed in the current environment. | Use Plotly, PyVista, or Trimesh. |
| SageMath | Not installed; standard packages need external system libraries. | Treat as an external Sage environment, especially for algebraic geometry. |
| Singular | Not installed as a Python package here. | Access through external Sage/Singular if explicitly required. |

## Artifact Rules

- Store generated outputs under the book-local `artifacts/` subtree, usually in `figures/`, `interactive/` or `html/`, `checks/`, and `tables/`.
- Prefer PNG/SVG for durable static diagrams, HTML for interactive Plotly/trame views, JSON/CSV for invariant summaries, and small mesh/image files only when the file itself is a teaching artifact.
- Display or link every generated artifact near the prose that explains it.
- Assert artifact existence, nonzero size, and concept-specific checks in final notebook cells.
- Do not use textbook screenshots, PDF crops, page images, or decorative stock images.

## Anti-Generic Audit Ideas

Useful course scripts can check:

- repeated markdown shingles across notebooks
- repeated code-cell fingerprints
- repeated artifact names and duplicate artifact hashes
- identical notebook outlines across unrelated chapters
- missing chapter-specific terms in headings, markdown, code, artifacts, or checks
- missing source-span/source-map notes
- missing library-routing notes
- visuals with no nearby explanatory markdown
- notebooks dominated by one monolithic generation script or one generic visual builder call

These scripts should audit and report. They should not mass-populate canonical teaching notebooks.

## Concise Routing Examples

### Proof-Heavy Euclidean/Synthetic Geometry

- Source-specific concept: angle bisector, concurrence, or parallel-postulate theorem from the assigned pages.
- Route: Matplotlib construction diagram plus NetworkX proof dependency graph; SymPy determinant or distance check if coordinates clarify the invariant.
- Artifacts/checks: `artifacts/chapter-XX/figures/angle-bisector-incidence.png`, `artifacts/chapter-XX/checks/incidence-invariants.json`.
- Inspection target: learner checks which assumptions feed the theorem and which lengths/angles/incidences remain invariant.

### Differential Geometry Surface/Curvature

- Source-specific concept: shape operator, principal curvature, Gauss map, or frame transport.
- Route: PyVista or Trimesh surface view plus Matplotlib curvature cross-section; SymPy or numeric checks for fundamental forms/curvature samples.
- Artifacts/checks: surface PNG/HTML, curvature CSV, JSON normal/area/curvature sanity checks.
- Inspection target: learner rotates or compares the surface and reads where curvature sign or frame behavior changes.

### Topology/TDA

- Source-specific concept: simplicial homology, filtration, nerve, or shape invariant.
- Route: Gudhi/Ripser computation plus Persim persistence diagram and NetworkX boundary/dependency graph.
- Artifacts/checks: persistence diagram PNG, Betti JSON, boundary-matrix CSV.
- Inspection target: learner connects visible cycles/components to computed Betti numbers or persistence intervals.

### Projective/Computer-Vision Geometry

- Source-specific concept: homography, camera projection, epipolar constraint, or vanishing point.
- Route: OpenCV/Kornia/Torch synthetic image geometry plus Matplotlib/Plotly overlays and SymPy homogeneous-coordinate check.
- Artifacts/checks: warped image PNG, correspondence overlay, JSON reprojection/epipolar residuals.
- Inspection target: learner sees lines stay lines, points satisfy homogeneous equations, and residuals catch a bad matrix.

### Geometric Algebra

- Source-specific concept: blade orientation, rotor action, conformal incidence, or projective model operation.
- Route: course-local GA helpers plus Clifford/Kingdon/Galgebra for identities; Matplotlib/PyGanja/Plotly for objects when useful.
- Artifacts/checks: blade/rotor diagram, JSON grade/norm/incidence checks, symbolic identity markdown.
- Inspection target: learner tracks grade, orientation, metric convention, and invariant preservation under the algebraic operation.
