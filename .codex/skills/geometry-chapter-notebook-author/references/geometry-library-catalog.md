# Geometry Library Catalog

This workspace uses `uv` with Python 3.13. Prefer installed libraries before adding dependencies.

## Installed Core Stack

| Use case | Libraries | Notes |
| --- | --- | --- |
| General numerics and plotting | `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `ipympl`, `pandas`, `polars`, `seaborn` | Use Matplotlib for durable static figures, Plotly for interactive 2D/3D HTML, and widgets for parameter exploration. |
| 3D surfaces and meshes | `pyvista`, `trimesh`, `meshio`, `gpytoolbox`, `manifold3d`, `potpourri3d`, `robust_laplacian`, `mapbox_earcut`, `xatlas`, `trame`, `trame_vtk`, `trame_vuetify` | Use PyVista/Trimesh for inspectable surfaces, normals, curvature, mesh operations, and 3D geometry artifacts. |
| Computational geometry | `scipy.spatial`, `shapely`, `networkx` | Use for Voronoi/Delaunay, intersections, planar geometry, graph structure, and proof dependency graphs. |
| Symbolic geometry | `sympy`, `galgebra` | Use for derivations, metrics, forms, Clifford/geometric algebra identities, and exact special cases. |
| Geometric algebra | `kingdon`, `clifford`, `galgebra`, `pyganja`, course-local `utils.ga` | Prefer course-local helpers for learner-readable code; use packages for richer algebra checks or visual experiments. |
| Computer vision and imaging | `cv2` from `opencv-contrib-python`, `skimage`, `kornia`, `torch`, `torchvision`, `PIL` | Use for projective geometry, epipolar geometry, image transforms, feature geometry, and tensor-based CV demos. |
| Riemannian and statistical geometry | `geomstats`, `pyriemann` | Use for manifolds, geodesics, Riemannian metrics, SPD matrices, and statistics on geometric spaces. |
| Optimal transport | `ot` from POT, `geomloss` | Use for transport plans, Wasserstein distances, barycenters, matching, and geometry of distributions. |
| Topological data analysis | `ripser`, `gudhi`, `persim` | Use for persistent homology/cohomology, persistence diagrams, filtrations, and shape signatures. |
| GIS and maps | `geopandas`, `shapely`, `rasterio`, `fiona`, `pyproj`, `pyogrio`, `osmnx`, `contextily`, `folium`, `pydeck` | Use only when geographic geometry clarifies the chapter. |
| Artifact and rendering support | `kaleido`, `imageio`, `imageio_ffmpeg`, `PIL`, `rich` | Use for static Plotly export, animations, image checks, and readable console output. |

## Optional Or External

| Tool | Status in this workspace | Guidance |
| --- | --- | --- |
| `open3d` | Not installed; available wheels stop before CPython 3.13 in this environment. | Document as an external option or use PyVista/Trimesh instead. |
| `meshplot` | Not installed; does not resolve from the package registry used by `uv` here. | Use Plotly, PyVista, or Trimesh. |
| SageMath | Not installed; `sagemath-standard` needs external system libraries and failed to build here. | Treat as an external Sage environment, especially for algebraic geometry. |
| Singular | Not installed as a Python package here. | Access through an external Sage/Singular setup if needed. |

## Selection Heuristics

- Start from the concept, then choose the representation.
- Use static Matplotlib diagrams for proof shape, orientation, incidence, and labeled constructions.
- Use Plotly or PyVista when rotation, depth, or surface inspection teaches the idea.
- Use SymPy or Galgebra when an identity is the teaching object.
- Use TDA, OT, CV, or GIS libraries only when their domain matches the chapter's geometry.
- Always pair visual artifacts with a check, invariant, or written inspection target.
