# Runtime Guide

The Geometry atlas is readable first and executable second. The source repo
keeps notebooks, artifacts, metadata, and runtime profiles; execution happens
through Colab, JupyterLite-compatible browser notebooks, or a local Python
environment.

## Colab

Colab is the default cloud runtime for most notebooks. Manifest entries include
direct Colab links for every discovered course and notebook.

For large courses, start with a sparse checkout instead of cloning the whole
repository:

```python
# Course setup
!git clone --depth 1 --filter=blob:none --sparse https://github.com/Rah-Rah-Mitra/Geometry.git
%cd Geometry
!git sparse-checkout set "The-Four-Pillars-of-Geometry"
%pip install -q -r requirements/classic.txt
```

Switch the final two lines for another course and profile:

```python
!git sparse-checkout set "Computational-Topology-An-Introduction"
%pip install -q -r requirements/topology.txt
```

Colab runtimes are temporary. Put setup cells near the top of notebooks that
need extra packages, generated artifacts, or a sparse checkout.

## Runtime Profiles

Use the smallest profile that covers the course:

| Profile | File | Use for |
| --- | --- | --- |
| `classic` | [`requirements/classic.txt`](./requirements/classic.txt) | Numerical, symbolic, plotting, graph, and lightweight geometry notebooks. |
| `topology` | [`requirements/topology.txt`](./requirements/topology.txt) | Persistent homology, computational topology, shape, and topology-heavy notebooks. |
| `graphics` | [`requirements/graphics.txt`](./requirements/graphics.txt) | Meshes, graphics, computer vision, OpenCV, PyVista, and 3D visualization. |
| `robotics` | [`requirements/robotics.txt`](./requirements/robotics.txt) | Rigid motion, robot visualization, manipulation, and motion-planning courses. |
| `algebraic_geometry` | [`requirements/algebraic-geometry.txt`](./requirements/algebraic-geometry.txt) | Symbolic algebraic geometry and polynomial computation. |
| `ml_geometry` | [`requirements/ml-geometry.txt`](./requirements/ml-geometry.txt) | Geometric ML, optimal transport, statistics on manifolds, and information geometry. |
| `full` | [`requirements/full.txt`](./requirements/full.txt) | The broad local lab stack from the root requirements file. |

The machine-readable profile definitions live in
[`metadata/runtime_profiles.yml`](./metadata/runtime_profiles.yml).

## Local Setup

For the full local lab:

```bash
uv sync
jupyter lab
```

For a smaller pip environment:

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -U pip
.venv\Scripts\python -m pip install -r requirements/classic.txt
.venv\Scripts\python -m ipykernel install --user --name geometry-classic --display-name "Python (Geometry Classic)"
jupyter lab
```

Use the matching `requirements/*.txt` file for heavier tracks.

## JupyterLite

JupyterLite should be used only for notebooks marked compatible in
[`course-manifest.json`](./course-manifest.json). Good candidates are notebooks
that stay within browser-compatible packages such as NumPy, SciPy, SymPy,
Matplotlib, Plotly, ipywidgets, NetworkX, and small generated assets.

Avoid JupyterLite for notebooks that need PyVista, OpenCV-heavy workflows,
PyTorch, large datasets, compiled topology libraries, or local helper behavior
that assumes a normal filesystem.

The future Lite deployment should be generated from the manifest by copying only
compatible notebooks into a dedicated build tree.

## Future Full-Lab Launches

The main repository no longer ships one large public JupyterLab image. If a
full-lab cloud launch is useful later, create separate slim repositories such as
`Geometry-Binder-Classic`, `Geometry-Binder-Topology`, `Geometry-Binder-Graphics`,
and `Geometry-Binder-ML`. Each should contain only the notebooks and artifacts
needed for that track, plus a small runtime profile.
