# Binder Setup

This repository is configured for [mybinder.org](https://mybinder.org/) with
the files in `binder/`. Binder uses repo2docker, which looks for configuration
files such as `environment.yml`, `apt.txt`, and `postBuild` in a top-level
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
cover the interactive notebooks and course artifacts. Putting
`environment.yml` under `binder/` keeps the Binder image independent from the
root `requirements.txt` and avoids installing platform-specific local packages.

## Binder Files

- `binder/environment.yml` defines the Python 3.11 JupyterLab course image.
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
import yaml

env = yaml.safe_load(Path("binder/environment.yml").read_text())
assert env["name"] == "geometry-course"
assert "python=3.11" in env["dependencies"]
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
  `binder/environment.yml`.
- If a build becomes too slow, the main tradeoff is repository size: this Binder
  setup intentionally keeps all prebuilt figures and HTML labs so learners get
  the complete course atlas.
