from __future__ import annotations

import hashlib
import re
from pathlib import Path

import nbformat
import numpy as np
from PIL import Image


def notebook_markdown_words(path: str | Path) -> int:
    nb = nbformat.read(path, as_version=4)
    markdown = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "markdown")
    return len(re.findall(r"[A-Za-z][A-Za-z0-9'-]*", markdown))


def sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    digest.update(Path(path).read_bytes())
    return digest.hexdigest()


def png_stats(path: str | Path) -> dict[str, object]:
    resolved = Path(path)
    image = Image.open(resolved).convert("RGB")
    arr = np.asarray(image, dtype=float)
    return {
        "path": resolved,
        "width": image.width,
        "height": image.height,
        "pixel_std": float(arr.std()),
        "size": resolved.stat().st_size,
        "sha": sha256(resolved),
    }
