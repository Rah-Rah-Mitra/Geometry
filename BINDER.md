# Binder Setup

This repository is configured for [mybinder.org](https://mybinder.org/) with
the files in `binder/`. Binder uses repo2docker, which looks for configuration
files such as `runtime.txt`, `requirements.txt`, `apt.txt`, and `postBuild` in a top-level
`binder/` or `.binder/` directory.

## Launch

Use this URL to open the course atlas in JupyterLab:

https://mybinder.org/v2/gh/Rah-Rah-Mitra/Geometry/main?urlpath=lab/tree/index.ipynb

The first launch after a change can take several minutes because Binder needs to
clone a large notebook/artifact repository and build the Python environment.
Later launches can reuse Binder's cached image when the same Git ref is still
available in the cache.

## Why Binder Has Its Own Environment

The root project is managed as a broad local Python 3.13 lab. Binder's public
Linux image is better served by a Python 3.11 environment with dependencies that
cover the interactive notebooks and course artifacts.

The first Binder version used `binder/environment.yml`, but the public Binder
build failed immediately after selecting `CondaBuildPack`, and a local
`conda env create --dry-run -f binder/environment.yml` did not solve within ten
minutes. The Binder setup now uses `runtime.txt` plus `requirements.txt` so
repo2docker takes the Python/pip build path. This keeps the Binder image
independent from the root `requirements.txt` and avoids asking conda to solve a
large mixed stack of PyTorch, VTK/PyVista, geospatial libraries, topology
libraries, and pip-only packages.

## Binder Files

- `binder/runtime.txt` requests Python 3.11 for the repo2docker Python buildpack.
- `binder/requirements.txt` defines the pip-installable JupyterLab course stack.
- `binder/apt.txt` installs Linux system libraries needed by OpenCV and visual
  media tools.
- `binder/postBuild` registers the `Python (Geometry Course)` kernel and runs a
  fast import smoke test for the main scientific and geometry stack.
- `index.ipynb` is the public course entrance and Binder launch target.

## Local Build Check

If Docker and repo2docker are available locally, test the Binder image with:

```bash
repo2docker --no-run .
```

For a faster preflight without Docker, validate the files directly:

```bash
python -m json.tool index.ipynb > /dev/null
python - <<'PY'
from pathlib import Path

assert Path("binder/runtime.txt").read_text().strip() == "python-3.11"
assert Path("binder/requirements.txt").exists()
assert not Path("binder/environment.yml").exists()
assert Path("binder/apt.txt").exists()
assert Path("binder/postBuild").exists()
assert not Path(".binder").exists()
print("Binder preflight passed.")
PY
```

## Troubleshooting

- If Binder opens the file tree instead of the atlas, check that the URL ends in
  `?urlpath=lab/tree/index.ipynb`.
- If a notebook import fails, compare it with the smoke test in
  `binder/postBuild` and add the missing runtime dependency to
  `binder/requirements.txt`.
- If Binder logs mention `CondaBuildPack`, check that `binder/environment.yml`
  has not been restored. `runtime.txt` is ignored when `environment.yml` is
  present.
- If a build becomes too slow, the main tradeoff is repository size: this Binder
  setup intentionally keeps all prebuilt figures and HTML labs so learners get
  the complete course atlas.
