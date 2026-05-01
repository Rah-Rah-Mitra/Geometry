"""Bootstrap the Basic Topology standalone notebook course.

The generated notebooks are original teaching artifacts. The source PDF is used
only for structure, page spans, terminology, and problem orientation.
"""

from __future__ import annotations

import importlib
import json
import sys
import textwrap
from pathlib import Path
from typing import Any

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

BOOK_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = BOOK_ROOT.parent


ENTRIES: list[dict[str, Any]] = [
    {
        "id": "chapter-01",
        "kind": "chapter",
        "label": "Chapter 1",
        "number": 1,
        "title": "Introduction",
        "folder": "chapter-01-introduction",
        "notebook": "01-introduction.ipynb",
        "artifact": "chapter-01",
        "printed_span": "1-26",
        "pdf_span": "12-37",
        "sections": "Euler theorem, topological equivalence, surfaces, abstract spaces, classification, invariants",
        "focus": "Turns the opening motivation into a laboratory for Euler characteristic, surface examples, and the first invariant-thinking habits.",
        "topics": [
            "Euler characteristic as a computable invariant",
            "Homeomorphism and controlled deformation",
            "Surfaces built from local two-dimensional patches",
            "Classification as a promise that invariants can organize examples",
        ],
        "lab": "Vary a small cell decomposition and watch which counts change while the alternating sum remains stable.",
    },
    {
        "id": "chapter-02",
        "kind": "chapter",
        "label": "Chapter 2",
        "number": 2,
        "title": "Continuity",
        "folder": "chapter-02-continuity",
        "notebook": "02-continuity.ipynb",
        "artifact": "chapter-02",
        "printed_span": "27-42",
        "pdf_span": "38-53",
        "sections": "open and closed sets, continuous functions, space-filling curve, Tietze extension",
        "focus": "Recasts continuity as preimage control and uses approximating pictures to separate intuition from theorem statements.",
        "topics": [
            "Open and closed sets as observable neighborhoods",
            "Continuity by inverse images",
            "Approximation stages of a space-filling curve",
            "Extension from closed data to ambient spaces",
        ],
        "lab": "Change thresholds in a preimage test and compare the geometry of domain intervals against target neighborhoods.",
    },
    {
        "id": "chapter-03",
        "kind": "chapter",
        "label": "Chapter 3",
        "number": 3,
        "title": "Compactness and Connectedness",
        "folder": "chapter-03-compactness-and-connectedness",
        "notebook": "03-compactness-and-connectedness.ipynb",
        "artifact": "chapter-03",
        "printed_span": "43-64",
        "pdf_span": "54-75",
        "sections": "Heine-Borel, compact spaces, product spaces, connectedness, path connectedness",
        "focus": "Builds finite-subcover and no-separation instincts with covers, products, and examples where connectedness and paths differ.",
        "topics": [
            "Closed bounded subsets of Euclidean space",
            "Finite subcovers and Lebesgue-number style reasoning",
            "Product behavior for compactness and connectedness",
            "Connected, path connected, and locally path connected examples",
        ],
        "lab": "Sample increasingly fine covers and record the smallest finite family that still covers a compact interval.",
    },
    {
        "id": "chapter-04",
        "kind": "chapter",
        "label": "Chapter 4",
        "number": 4,
        "title": "Identification Spaces",
        "folder": "chapter-04-identification-spaces",
        "notebook": "04-identification-spaces.ipynb",
        "artifact": "chapter-04",
        "printed_span": "65-86",
        "pdf_span": "76-97",
        "sections": "Mobius strip, identification topology, topological groups, orbit spaces",
        "focus": "Makes quotient constructions visible by drawing gluing instructions, orbit representatives, and the maps that forget labels.",
        "topics": [
            "Constructing spaces by identifying points",
            "The quotient topology as the topology forced by a projection",
            "Topological groups and translations",
            "Orbit spaces from group actions",
        ],
        "lab": "Compare square-edge identifications and predict which surface is orientable before checking the edge labels.",
    },
    {
        "id": "chapter-05",
        "kind": "chapter",
        "label": "Chapter 5",
        "number": 5,
        "title": "The Fundamental Group",
        "folder": "chapter-05-the-fundamental-group",
        "notebook": "05-the-fundamental-group.ipynb",
        "artifact": "chapter-05",
        "printed_span": "87-118",
        "pdf_span": "98-128",
        "sections": "homotopy, construction of pi_1, calculations, homotopy type, Brouwer, separation, surface boundary",
        "focus": "Treats loops as movable data and turns group operations, winding, and deformation retraction into inspectable computations.",
        "topics": [
            "Homotopies of maps and based loops",
            "Loop product and inverse as group operations",
            "Fundamental group calculations by deformation",
            "Fixed-point and separation arguments as loop obstructions",
        ],
        "lab": "Move a loop across a puncture and compare the sampled winding number before and after the deformation.",
    },
    {
        "id": "chapter-06",
        "kind": "chapter",
        "label": "Chapter 6",
        "number": 6,
        "title": "Triangulations",
        "folder": "chapter-06-triangulations",
        "notebook": "06-triangulations.ipynb",
        "artifact": "chapter-06",
        "printed_span": "119-148",
        "pdf_span": "129-158",
        "sections": "simplicial complexes, barycentric subdivision, simplicial approximation, edge group, orbit spaces, infinite complexes",
        "focus": "Uses simple complexes as a computational language for spaces, maps, subdivisions, and edge-loop presentations.",
        "topics": [
            "Simplexes, faces, and finite complexes",
            "Barycentric subdivision as controlled refinement",
            "Simplicial approximation of continuous maps",
            "Edge groups and triangulated orbit spaces",
        ],
        "lab": "Subdivide a triangle mesh and verify that Euler characteristic is unchanged by the refinement.",
    },
    {
        "id": "chapter-07",
        "kind": "chapter",
        "label": "Chapter 7",
        "number": 7,
        "title": "Surfaces",
        "folder": "chapter-07-surfaces",
        "notebook": "07-surfaces.ipynb",
        "artifact": "chapter-07",
        "printed_span": "149-172",
        "pdf_span": "159-181",
        "sections": "classification, triangulation and orientation, Euler characteristics, surgery, surface symbols",
        "focus": "Builds the classification theorem as a hands-on system of symbols, cuts, handles, crosscaps, and Euler-characteristic checks.",
        "topics": [
            "Closed surface classification",
            "Orientability from consistent triangle orientations",
            "Euler characteristic across handles and crosscaps",
            "Surgery and surface symbols",
        ],
        "lab": "Parse a polygon word and compute the orientability and Euler characteristic predicted by its identifications.",
    },
    {
        "id": "chapter-08",
        "kind": "chapter",
        "label": "Chapter 8",
        "number": 8,
        "title": "Simplicial Homology",
        "folder": "chapter-08-simplicial-homology",
        "notebook": "08-simplicial-homology.ipynb",
        "artifact": "chapter-08",
        "printed_span": "173-194",
        "pdf_span": "182-202",
        "sections": "cycles, boundaries, homology groups, examples, simplicial maps, stellar subdivision, invariance",
        "focus": "Converts cycles, boundaries, and holes into chain groups, boundary matrices, ranks, and visible representatives.",
        "topics": [
            "Oriented chains and boundary operators",
            "Cycles versus bounding cycles",
            "Homology groups as quotient data",
            "Subdivision and simplicial maps preserving homology",
        ],
        "lab": "Build a small boundary matrix, verify boundary-after-boundary is zero, and read Betti numbers from ranks.",
    },
    {
        "id": "chapter-09",
        "kind": "chapter",
        "label": "Chapter 9",
        "number": 9,
        "title": "Degree and Lefschetz Number",
        "folder": "chapter-09-degree-and-lefschetz-number",
        "notebook": "09-degree-and-lefschetz-number.ipynb",
        "artifact": "chapter-09",
        "printed_span": "195-212",
        "pdf_span": "203-220",
        "sections": "sphere maps, Euler-Poincare formula, Borsuk-Ulam, Lefschetz fixed-point theorem, dimension",
        "focus": "Connects global map invariants to fixed points, antipodal symmetry, Euler-Poincare counts, and dimension tests.",
        "topics": [
            "Degree of maps between spheres",
            "Euler-Poincare formula",
            "Borsuk-Ulam as an antipodal obstruction",
            "Lefschetz number and fixed-point detection",
        ],
        "lab": "Compare sampled circle maps of different degrees and inspect how fixed-point counts respond.",
    },
    {
        "id": "chapter-10",
        "kind": "chapter",
        "label": "Chapter 10",
        "number": 10,
        "title": "Knots and Covering Spaces",
        "folder": "chapter-10-knots-and-covering-spaces",
        "notebook": "10-knots-and-covering-spaces.ipynb",
        "artifact": "chapter-10",
        "printed_span": "213-240",
        "pdf_span": "221-247",
        "sections": "knots, knot group, Seifert surfaces, covering spaces, Alexander polynomial",
        "focus": "Treats knots as embedded circles whose complements, coverings, and algebraic invariants can be computed from diagrams.",
        "topics": [
            "Knot projections and crossing data",
            "Wirtinger-style group presentations",
            "Seifert surface intuition",
            "Covering spaces and the Alexander polynomial",
        ],
        "lab": "Encode a small crossing matrix and compute the determinant that produces the trefoil Alexander polynomial.",
    },
    {
        "id": "appendix-generators-and-relations",
        "kind": "appendix",
        "label": "Appendix",
        "number": 11,
        "title": "Generators and Relations",
        "folder": "appendix-generators-and-relations",
        "notebook": "appendix-generators-and-relations.ipynb",
        "artifact": "appendix-generators-and-relations",
        "printed_span": "241-243",
        "pdf_span": "248-250",
        "sections": "free groups, group presentations, free products",
        "focus": "Supplies the algebraic grammar used by edge groups, knot groups, and presentation matrices.",
        "topics": [
            "Reduced words in a free group",
            "Generators and relations",
            "Free products",
            "Presentation matrices as computable algebra",
        ],
        "lab": "Reduce words and compare the unreduced path with the normal form that survives after cancellations.",
    },
]

BACK_MATTER = [
    {"title": "Bibliography", "printed_span": "244-245", "pdf_span": "251-252"},
    {"title": "Index", "printed_span": "246-251", "pdf_span": "253-258"},
]

SOURCE_SPAN_NOTES = [
    "The main PDF is text-extractable; printed page 1 starts at physical PDF page 12.",
    "The solutions PDF is a private cross-check for exercise intent only and is not copied.",
    "Back matter is inventoried but is not a canonical teaching notebook.",
]


def dedent(value: str) -> str:
    return textwrap.dedent(value).strip() + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_module(path: Path, content: str) -> None:
    write_text(path, dedent(content))


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook(cells=[new_markdown_cell(text.strip() + "\n")])
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python", "version": "3.13"}
    nbformat.write(nb, path)


AGENTS_MD = dedent(
    """
    # Agent Instructions: Basic Topology Notebook Course

    This folder is a standalone visualization-first notebook edition of M. A.
    Armstrong's *Basic Topology*. Treat this book folder as the course root. The
    workspace root owns the shared `uv` environment, `pyproject.toml`, and
    `uv.lock`.

    ## Repo-Local Skills

    Use the repo-local skills under `D:\\Geometry\\.codex\\skills`:

    - `geometry-visualization-planner` before planning or revising a chapter storyboard.
    - `geometry-chapter-notebook-author` when authoring a canonical notebook.
    - `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

    ## Non-Negotiables

    - Write original teaching prose, examples, code, diagrams, and checks.
    - Do not copy textbook passages, long exercise text, screenshots, page crops, or solution text.
    - The PDFs are source orientation only. A reader should not need the PDF open.
    - Visualization is part of delivery, not decoration or a quota.
    - Keep helpers in `utils/`, outputs in `artifacts/`, and validation tools in `scripts/`.
    - Every canonical notebook should execute with `nbclient`.
    - Generated paths in notebooks must be relative or book-local.
    - Preserve one canonical teaching notebook plus `00-index.ipynb` per content folder.

    ## Course Structure

    ```text
    Basic-Topology/
      00-book-index.ipynb
      AGENTS.md
      artifacts/
      scripts/
      utils/
      chapter-01-introduction/
      ...
      chapter-10-knots-and-covering-spaces/
      appendix-generators-and-relations/
    ```

    ## Source Map

    Printed page 1 starts at physical PDF page 12.

    | Unit | Folder | Printed Pages | PDF Pages | Focus |
    | --- | --- | ---: | ---: | --- |
    | Chapter 1 | `chapter-01-introduction` | 1-26 | 12-37 | Euler characteristic, equivalence, surfaces, classification, invariants. |
    | Chapter 2 | `chapter-02-continuity` | 27-42 | 38-53 | Open/closed sets, continuous maps, space-filling curves, extension. |
    | Chapter 3 | `chapter-03-compactness-and-connectedness` | 43-64 | 54-75 | Compactness, products, connectedness, path connectedness. |
    | Chapter 4 | `chapter-04-identification-spaces` | 65-86 | 76-97 | Quotients, Mobius strip, topological groups, orbit spaces. |
    | Chapter 5 | `chapter-05-the-fundamental-group` | 87-118 | 98-128 | Homotopy, pi_1, calculations, Brouwer, separation, boundaries. |
    | Chapter 6 | `chapter-06-triangulations` | 119-148 | 129-158 | Simplicial complexes, subdivision, approximation, edge groups. |
    | Chapter 7 | `chapter-07-surfaces` | 149-172 | 159-181 | Surface classification, orientation, surgery, symbols. |
    | Chapter 8 | `chapter-08-simplicial-homology` | 173-194 | 182-202 | Chains, cycles, boundaries, homology, invariance. |
    | Chapter 9 | `chapter-09-degree-and-lefschetz-number` | 195-212 | 203-220 | Degree, Euler-Poincare, Borsuk-Ulam, Lefschetz, dimension. |
    | Chapter 10 | `chapter-10-knots-and-covering-spaces` | 213-240 | 221-247 | Knots, knot groups, Seifert surfaces, coverings, Alexander polynomial. |
    | Appendix | `appendix-generators-and-relations` | 241-243 | 248-250 | Free groups, presentations, free products. |

    ## Notebook Shape

    Each canonical notebook should contain a title and source span, a standalone
    chapter question, a translation guide, setup cell, original concept sections,
    generated visual artifacts displayed inline, worked examples, an applied lab,
    sanity checks, and takeaways.

    ## Artifact Contract

    Store generated outputs under:

    ```text
    artifacts/chapter-01/
    ...
    artifacts/chapter-10/
    artifacts/appendix-generators-and-relations/
    ```

    Use subfolders such as `figures/`, `html/`, `checks/`, and `tables/`. Artifact
    filenames should name the concept, not the rendering technology. Every
    generated artifact should be displayed inline or linked from the notebook, and
    final checks should assert that files exist and are nonempty.

    ## Geometry Stack

    Use the shared `uv` environment at the workspace root. Prefer installed
    libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`,
    `plotly`, `ipywidgets`, `sympy`, `pandas`, `networkx`, `shapely`, `trimesh`,
    `pyvista`, `ripser`, `gudhi`, and the rest of the root geometry stack.
    This course currently needs no dependency additions.

    ## Worker Boundaries

    Assign one worker to one canonical notebook, one helper module, or one script
    task. Chapter workers may edit only their chapter folder, matching artifact
    subtree, and explicitly assigned helper module. Index workers own
    `00-book-index.ipynb` and `00-index.ipynb` files. QC workers run audits and
    validation and report findings.

    ## Commands

    Run from `D:\\Geometry`:

    ```powershell
    uv run python Basic-Topology/scripts/build_bt_course_indexes.py
    uv run python -m compileall -q Basic-Topology/utils Basic-Topology/scripts
    uv run python Basic-Topology/scripts/audit_bt_notebooks.py --min-words 1200 --min-code-cells 5
    uv run python Basic-Topology/scripts/audit_bt_visuals.py
    uv run python Basic-Topology/scripts/validate_bt_course.py --limit 4 --timeout 300
    git diff --check
    ```

    Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.
    """
)


UTILS_INIT = '"""Utilities for the Basic Topology notebook course."""\n'


ARTIFACTS_PY = r'''
"""Artifact helpers for the Basic Topology notebook course."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image as PILImage

BOOK_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-._")
    return slug or "artifact"


def artifact_dir(unit: str, kind: str | None = None, root: str | Path = ARTIFACT_ROOT) -> Path:
    parts = [slugify(unit)]
    if kind:
        parts.append(slugify(kind))
    path = Path(root).joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(unit: str, kind: str | None, filename: str, root: str | Path = ARTIFACT_ROOT) -> Path:
    path = artifact_dir(unit, kind, root) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_json(
    data: Any,
    unit: str,
    kind: str | None,
    filename: str = "data.json",
    *,
    root: str | Path = ARTIFACT_ROOT,
) -> Path:
    path = artifact_path(unit, kind, filename, root)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def save_text(
    text: str,
    unit: str,
    kind: str | None,
    filename: str = "notes.txt",
    *,
    root: str | Path = ARTIFACT_ROOT,
) -> Path:
    path = artifact_path(unit, kind, filename, root)
    path.write_text(text, encoding="utf-8")
    return path


def save_matplotlib(
    figure: Any,
    unit: str,
    kind: str | None,
    filename: str,
    *,
    dpi: int = 160,
    root: str | Path = ARTIFACT_ROOT,
    **kwargs: Any,
) -> Path:
    path = artifact_path(unit, kind, filename, root)
    figure.savefig(path, dpi=dpi, bbox_inches="tight", **kwargs)
    return path


def save_plotly_html(
    figure: Any,
    unit: str,
    kind: str | None,
    filename: str,
    *,
    root: str | Path = ARTIFACT_ROOT,
    include_plotlyjs: str | bool = "cdn",
    full_html: bool = True,
    **kwargs: Any,
) -> Path:
    path = artifact_path(unit, kind, filename, root)
    figure.write_html(path, include_plotlyjs=include_plotlyjs, full_html=full_html, **kwargs)
    return path


def save_image(
    image: Any,
    unit: str,
    kind: str | None,
    filename: str,
    *,
    root: str | Path = ARTIFACT_ROOT,
) -> Path:
    path = artifact_path(unit, kind, filename, root)
    if isinstance(image, PILImage.Image):
        image.save(path)
        return path
    array = np.asarray(image)
    if array.dtype != np.uint8:
        if np.issubdtype(array.dtype, np.floating) and array.size and float(np.nanmax(array)) <= 1.0:
            array = array * 255.0
        array = np.clip(array, 0, 255).astype(np.uint8)
    PILImage.fromarray(array).save(path)
    return path


def assert_artifact(path: str | Path, *, min_bytes: int = 512) -> Path:
    resolved = Path(path)
    if not resolved.exists():
        raise FileNotFoundError(resolved)
    size = resolved.stat().st_size
    if size < min_bytes:
        raise AssertionError(f"{resolved} is unexpectedly small: {size} bytes")
    return resolved


def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
    from IPython.display import HTML, IFrame, Image, display

    resolved = Path(path)
    suffix = resolved.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        return display(Image(filename=str(resolved), width=width, height=height))
    if suffix in {".html", ".htm"}:
        if height:
            return display(IFrame(src=str(resolved), width=width or "100%", height=height))
        return display(HTML(resolved.read_text(encoding="utf-8")))
    link = escape(resolved.as_posix(), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))
'''


PLOTTING_PY = r'''
"""Small plotting helpers shared by the Basic Topology notebooks."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

PALETTE = {
    "ink": "#273043",
    "blue": "#1f77b4",
    "green": "#2ca25f",
    "gold": "#b8860b",
    "red": "#c23b22",
    "purple": "#6a51a3",
    "teal": "#008080",
    "gray": "#6b7280",
    "paper": "#f8fafc",
}


def new_figure(width: float = 7.0, height: float = 5.0) -> tuple[Any, Any]:
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_facecolor("white")
    return fig, ax


def set_equal_axes(ax: Any, margin: float = 0.12) -> None:
    ax.set_aspect("equal", adjustable="box")
    ax.margins(margin)
    ax.grid(True, color="#e5e7eb", linewidth=0.8)
    for spine in ax.spines.values():
        spine.set_color("#cbd5e1")


def label_point(
    ax: Any,
    point: Sequence[float],
    label: str,
    *,
    offset: tuple[float, float] = (0.04, 0.04),
    color: str = PALETTE["ink"],
) -> None:
    x, y = point
    ax.scatter([x], [y], s=42, color=color, zorder=4)
    ax.text(x + offset[0], y + offset[1], label, fontsize=10, color=color)


def draw_segment(
    ax: Any,
    a: Sequence[float],
    b: Sequence[float],
    *,
    label: str | None = None,
    color: str = PALETTE["blue"],
    linewidth: float = 2.2,
    linestyle: str = "-",
) -> None:
    ax.plot([a[0], b[0]], [a[1], b[1]], color=color, linewidth=linewidth, linestyle=linestyle)
    if label:
        mid = (np.asarray(a, dtype=float) + np.asarray(b, dtype=float)) / 2
        ax.text(mid[0], mid[1], label, fontsize=9, color=color)


def draw_arrow(
    ax: Any,
    start: Sequence[float],
    end: Sequence[float],
    *,
    color: str = PALETTE["red"],
    label: str | None = None,
) -> None:
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={"arrowstyle": "->", "linewidth": 1.8, "color": color},
    )
    if label:
        mid = (np.asarray(start, dtype=float) + np.asarray(end, dtype=float)) / 2
        ax.text(mid[0], mid[1], label, fontsize=9, color=color)


def draw_polygon(
    ax: Any,
    points: Iterable[Sequence[float]],
    *,
    closed: bool = True,
    color: str = PALETTE["blue"],
    fill: str | None = None,
    label: str | None = None,
    linewidth: float = 2.0,
) -> None:
    pts = np.asarray(list(points), dtype=float)
    if closed:
        pts = np.vstack([pts, pts[0]])
    ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=linewidth)
    if fill:
        ax.fill(pts[:, 0], pts[:, 1], color=fill, alpha=0.18)
    if label:
        centroid = pts[:-1].mean(axis=0) if closed else pts.mean(axis=0)
        ax.text(centroid[0], centroid[1], label, fontsize=10, color=color, ha="center")
'''


TOPOLOGY_PY = r'''
"""Computational topology helpers used by the Basic Topology notebooks."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from math import atan2, pi

import numpy as np


def euler_characteristic(vertices: int, edges: int, faces: int = 0, cells3: int = 0) -> int:
    return vertices - edges + faces - cells3


def graph_euler_characteristic(edge_list: Iterable[tuple[object, object]]) -> int:
    edges = list(edge_list)
    vertices = {item for edge in edges for item in edge}
    return len(vertices) - len(edges)


def surface_chi(kind: str, parameter: int = 0) -> int:
    if kind == "sphere":
        return 2
    if kind == "orientable":
        return 2 - 2 * parameter
    if kind == "nonorientable":
        return 2 - parameter
    raise ValueError(f"unknown surface kind: {kind}")


def winding_number(points: Sequence[Sequence[float]], center: Sequence[float] = (0.0, 0.0)) -> int:
    pts = np.asarray(points, dtype=float)
    c = np.asarray(center, dtype=float)
    shifted = pts - c
    angles = np.unwrap(np.arctan2(shifted[:, 1], shifted[:, 0]))
    total = angles[-1] - angles[0]
    return int(round(total / (2 * pi)))


def reduce_word(letters: Sequence[str]) -> list[str]:
    stack: list[str] = []
    for letter in letters:
        if stack and stack[-1].swapcase() == letter:
            stack.pop()
        else:
            stack.append(letter)
    return stack


def word_reduction_trace(letters: Sequence[str]) -> list[list[str]]:
    trace = [[]]
    stack: list[str] = []
    for letter in letters:
        if stack and stack[-1].swapcase() == letter:
            stack.pop()
        else:
            stack.append(letter)
        trace.append(stack.copy())
    return trace


def count_components(vertices: Sequence[object], edges: Iterable[tuple[object, object]]) -> int:
    parent = {vertex: vertex for vertex in vertices}

    def find(value: object) -> object:
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    return len({find(vertex) for vertex in vertices})


def polygon_word_summary(word: str) -> dict[str, object]:
    letters = [char for char in word if char.isalpha()]
    counts = Counter(char.lower() for char in letters)
    orientable = all(word.count(char.lower()) == 1 and word.count(char.upper()) == 1 for char in counts)
    pairs = len(counts)
    chi = 2 - 2 * max(1, pairs // 2) if orientable else 2 - pairs
    return {"word": word, "pairs": pairs, "orientable": orientable, "chi_estimate": chi}
'''


SIMPLICIAL_PY = r'''
"""Simplicial-complex helpers for visual and algebraic checks."""

from __future__ import annotations

from itertools import combinations
from typing import Sequence

import numpy as np


def simplex_faces(simplex: Sequence[int]) -> list[tuple[int, ...]]:
    return [tuple(face) for r in range(1, len(simplex)) for face in combinations(simplex, r)]


def boundary_matrix(k_simplices: Sequence[Sequence[int]], faces: Sequence[Sequence[int]]) -> np.ndarray:
    face_index = {tuple(face): i for i, face in enumerate(faces)}
    matrix = np.zeros((len(faces), len(k_simplices)), dtype=int)
    for col, simplex in enumerate(k_simplices):
        simplex = tuple(simplex)
        for i in range(len(simplex)):
            face = simplex[:i] + simplex[i + 1 :]
            row = face_index.get(face)
            sign = -1 if i % 2 else 1
            if row is None:
                reversed_face = tuple(reversed(face))
                row = face_index[reversed_face]
                sign *= -1
            matrix[row, col] = sign
    return matrix


def rank(matrix: np.ndarray, tol: float = 1e-9) -> int:
    if matrix.size == 0:
        return 0
    return int(np.linalg.matrix_rank(matrix.astype(float), tol=tol))


def betti_number(chain_dim: int, boundary_out: np.ndarray, boundary_in: np.ndarray) -> int:
    return chain_dim - rank(boundary_out) - rank(boundary_in)


def barycentric_triangle() -> tuple[np.ndarray, list[tuple[int, int, int]]]:
    vertices = np.array(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [0.35, 0.9],
            [0.5, 0.0],
            [0.675, 0.45],
            [0.175, 0.45],
            [0.45, 0.3],
        ]
    )
    triangles = [(0, 3, 6), (3, 1, 6), (1, 4, 6), (4, 2, 6), (2, 5, 6), (5, 0, 6)]
    return vertices, triangles
'''


KNOTS_PY = r'''
"""Small knot and presentation helpers."""

from __future__ import annotations

import sympy as sp


def trefoil_alexander_matrix() -> sp.Matrix:
    t = sp.symbols("t")
    return sp.Matrix([[1 - t, -1], [t, 1 - t]])


def trefoil_alexander_polynomial() -> sp.Expr:
    t = sp.symbols("t")
    return sp.expand(trefoil_alexander_matrix().det())


def presentation_to_text(generators: list[str], relators: list[str]) -> str:
    return "<" + ", ".join(generators) + " | " + ", ".join(relators) + ">"
'''


VALIDATION_PY = r'''
"""Validation helpers for the Basic Topology course scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import nbformat

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED_NOTEBOOKS = {"00-index.ipynb", "00-book-index.ipynb"}
STALE_PATH_PATTERNS = (
    "D:/Geometry/artifacts",
    "D:\\Geometry\\artifacts",
    "/mnt/d/Geometry/artifacts",
    "D:/Geometry/utils",
    "D:\\Geometry\\utils",
    "/mnt/d/Geometry/utils",
)


def discover_canonical_notebooks(book_root: Path = BOOK_ROOT) -> list[Path]:
    artifact_root = book_root / "artifacts"
    return [
        path
        for path in sorted(book_root.rglob("*.ipynb"))
        if artifact_root not in path.parents and path.name not in IGNORED_NOTEBOOKS
    ]


def notebook_stats(path: Path, book_root: Path = BOOK_ROOT) -> dict[str, Any]:
    nb = nbformat.read(path, as_version=4)
    markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
    code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
    source = "\n".join(markdown + code)
    return {
        "path": path.relative_to(book_root).as_posix(),
        "markdown_words": sum(len(text.split()) for text in markdown),
        "markdown_cells": len(markdown),
        "code_cells": len(code),
        "display_artifact_calls": source.count("display_artifact("),
        "visual_builder_calls": source.count("build_unit_visuals("),
        "assert_artifact_calls": source.count("assert_artifact("),
        "has_applied_lab": "## Applied Lab" in source,
        "has_takeaways": "## Takeaways" in source,
        "stale_paths": [pattern for pattern in STALE_PATH_PATTERNS if pattern in source],
    }


def write_report(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
'''


VISUALS_PY = r'''
"""Visualization builders for the Basic Topology notebooks."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sympy as sp
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Polygon

from .artifacts import save_json, save_matplotlib, save_plotly_html
from .knots import trefoil_alexander_polynomial
from .plotting import PALETTE, draw_arrow, draw_polygon, draw_segment, new_figure, set_equal_axes
from .simplicial import barycentric_triangle, boundary_matrix, rank
from .topology import euler_characteristic, reduce_word, surface_chi, winding_number, word_reduction_trace

UNIT_TOPICS: dict[str, list[str]] = {
    "chapter-01": ["Euler characteristic", "equivalence", "surfaces", "classification", "invariants"],
    "chapter-02": ["open sets", "preimages", "continuity", "Peano stages", "extension"],
    "chapter-03": ["compactness", "finite subcovers", "products", "connectedness", "paths"],
    "chapter-04": ["quotients", "gluing", "Mobius strip", "groups", "orbits"],
    "chapter-05": ["homotopy", "loops", "pi_1", "winding", "fixed points"],
    "chapter-06": ["simplexes", "complexes", "subdivision", "edge loops", "orbit triangulations"],
    "chapter-07": ["classification", "orientability", "Euler characteristic", "surgery", "symbols"],
    "chapter-08": ["chains", "cycles", "boundaries", "homology", "invariance"],
    "chapter-09": ["degree", "Euler-Poincare", "Borsuk-Ulam", "Lefschetz", "dimension"],
    "chapter-10": ["knots", "presentations", "Seifert surfaces", "coverings", "Alexander polynomial"],
    "appendix-generators-and-relations": ["free words", "relations", "presentations", "free products", "matrices"],
}


def _close(fig: Any) -> None:
    plt.close(fig)


def _concept_map(unit: str, title: str) -> Path:
    topics = UNIT_TOPICS[unit]
    graph = nx.Graph()
    graph.add_node(title)
    for topic in topics:
        graph.add_edge(title, topic)
    for a, b in zip(topics, topics[1:]):
        graph.add_edge(a, b)
    fig, ax = new_figure(8.2, 5.2)
    pos = nx.spring_layout(graph, seed=sum(ord(c) for c in unit), k=1.0)
    colors = [PALETTE["gold"] if node == title else PALETTE["blue"] for node in graph.nodes]
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="#94a3b8", width=1.6)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=colors, node_size=1700, edgecolors="white", linewidths=2)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=9, font_color="white")
    ax.set_title(f"{title}: dependency map", fontsize=13)
    ax.axis("off")
    path = save_matplotlib(fig, unit, "figures", "concept-dependency-map.png")
    _close(fig)
    return path


def _save_check(unit: str, data: dict[str, Any]) -> Path:
    data = {"unit": unit, **data}
    return save_json(data, unit, "checks", "sanity-checks.json")


def _chapter01(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Introduction")]
    polyhedra = pd.DataFrame(
        [
            {"space": "tetrahedron", "vertices": 4, "edges": 6, "faces": 4},
            {"space": "cube", "vertices": 8, "edges": 12, "faces": 6},
            {"space": "octahedron", "vertices": 6, "edges": 12, "faces": 8},
            {"space": "torus cell model", "vertices": 1, "edges": 2, "faces": 1},
        ]
    )
    polyhedra["chi"] = polyhedra.apply(lambda row: euler_characteristic(row.vertices, row.edges, row.faces), axis=1)
    fig, ax = new_figure(8.0, 4.8)
    x = np.arange(len(polyhedra))
    width = 0.2
    ax.bar(x - width, polyhedra.vertices, width, label="vertices", color=PALETTE["blue"])
    ax.bar(x, polyhedra.edges, width, label="edges", color=PALETTE["red"])
    ax.bar(x + width, polyhedra.faces, width, label="faces", color=PALETTE["green"])
    ax.plot(x, polyhedra.chi, color=PALETTE["ink"], marker="o", linewidth=2.5, label="chi")
    ax.set_xticks(x, polyhedra.space, rotation=18, ha="right")
    ax.set_title("Cell counts change; Euler characteristic is the invariant to inspect")
    ax.legend(ncols=4, fontsize=8)
    pngs.append(save_matplotlib(fig, unit, "figures", "euler-characteristic-counts.png"))
    _close(fig)

    fig = plt.figure(figsize=(8, 4.8))
    ax = fig.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * np.pi, 48)
    v = np.linspace(0, 2 * np.pi, 24)
    u, v = np.meshgrid(u, v)
    R, r = 1.5, 0.42
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    ax.plot_surface(x, y, z, color="#80b1d3", alpha=0.88, linewidth=0)
    ax.set_title("A torus is locally surface-like but globally different from a sphere")
    ax.set_axis_off()
    pngs.append(save_matplotlib(fig, unit, "figures", "torus-local-global-surface.png"))
    _close(fig)
    checks = [_save_check(unit, {"polyhedra": polyhedra.to_dict("records"), "sphere_chi_values": polyhedra.chi[:3].tolist(), "torus_chi": int(polyhedra.chi.iloc[3])})]
    return pngs, [], checks, {"stable_chi_for_convex_examples": int(polyhedra.chi[:3].nunique()) == 1}


def _chapter02(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Continuity")]
    fig, ax = new_figure(8, 4.5)
    xs = np.linspace(-3, 3, 600)
    ys = np.sin(xs) + 0.2 * xs
    band = (ys > -0.45) & (ys < 0.55)
    ax.plot(xs, ys, color=PALETTE["blue"], linewidth=2.2, label="f(x)")
    ax.fill_between(xs, -0.45, 0.55, color=PALETTE["gold"], alpha=0.16, label="target open band")
    ax.scatter(xs[band][::12], ys[band][::12], s=8, color=PALETTE["red"], label="preimage samples")
    ax.set_title("Continuity as inverse-image control")
    ax.legend(fontsize=8)
    pngs.append(save_matplotlib(fig, unit, "figures", "preimage-continuity-test.png"))
    _close(fig)

    fig, ax = new_figure(6.5, 6.0)
    t = np.linspace(0, 1, 256)
    x = np.mod(8 * t, 1)
    y = np.floor(8 * t) / 7
    ax.plot(x, y, color=PALETTE["purple"], linewidth=1.6)
    ax.scatter(x[::16], y[::16], s=18, color=PALETTE["ink"])
    ax.set_title("A stage approximation to a square-filling path")
    set_equal_axes(ax)
    pngs.append(save_matplotlib(fig, unit, "figures", "space-filling-curve-stage.png"))
    _close(fig)
    checks = [_save_check(unit, {"preimage_sample_count": int(band.sum()), "curve_samples": int(len(t)), "band_bounds": [-0.45, 0.55]})]
    return pngs, [], checks, {"preimage_is_nonempty": bool(band.any())}


def _chapter03(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Compactness and connectedness")]
    fig, ax = new_figure(8, 3.5)
    intervals = [(-0.05, 0.32), (0.2, 0.58), (0.47, 0.83), (0.72, 1.05)]
    ax.plot([0, 1], [0, 0], color=PALETTE["ink"], linewidth=5, solid_capstyle="round")
    for i, (a, b) in enumerate(intervals):
        ax.plot([a, b], [0.25 + i * 0.15] * 2, color=[PALETTE["blue"], PALETTE["green"], PALETTE["gold"], PALETTE["red"]][i], linewidth=9, solid_capstyle="round")
        ax.text((a + b) / 2, 0.35 + i * 0.15, f"U{i+1}", ha="center", fontsize=9)
    ax.set_xlim(-0.12, 1.12)
    ax.set_ylim(-0.2, 1.1)
    ax.axis("off")
    ax.set_title("A compact interval admits a finite visible subcover")
    pngs.append(save_matplotlib(fig, unit, "figures", "finite-subcover-interval.png"))
    _close(fig)

    fig, ax = new_figure(7, 4.6)
    xs = np.linspace(0.02, 1, 900)
    ax.plot(xs, np.sin(1 / xs), color=PALETTE["blue"], linewidth=1.2, label="oscillating graph")
    ax.plot([0, 0], [-1, 1], color=PALETTE["red"], linewidth=3, label="limit segment")
    ax.set_title("A connected closure where paths require extra care")
    ax.legend(fontsize=8)
    pngs.append(save_matplotlib(fig, unit, "figures", "connected-not-path-connected-model.png"))
    _close(fig)
    checks = [_save_check(unit, {"finite_subcover_size": len(intervals), "cover_left": min(a for a, _ in intervals), "cover_right": max(b for _, b in intervals), "oscillation_samples": int(len(xs))})]
    return pngs, [], checks, {"covers_unit_interval": min(a for a, _ in intervals) <= 0 and max(b for _, b in intervals) >= 1}


def _chapter04(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Identification spaces")]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.6))
    labels = [("cylinder", "a", "a"), ("Mobius strip", "a", "A"), ("torus", "a,b", "a,b")]
    for ax, (title, left, right) in zip(axes, labels):
        ax.add_patch(Polygon([[0, 0], [1, 0], [1, 1], [0, 1]], closed=True, fill=False, edgecolor=PALETTE["ink"], linewidth=2))
        draw_arrow(ax, (0, 0.18), (0, 0.82), color=PALETTE["blue"], label=left)
        if right == "A":
            draw_arrow(ax, (1, 0.82), (1, 0.18), color=PALETTE["red"], label=right)
        else:
            draw_arrow(ax, (1, 0.18), (1, 0.82), color=PALETTE["blue"], label=right)
        if title == "torus":
            draw_arrow(ax, (0.18, 0), (0.82, 0), color=PALETTE["green"], label="b")
            draw_arrow(ax, (0.18, 1), (0.82, 1), color=PALETTE["green"], label="b")
        ax.set_title(title)
        ax.set_aspect("equal")
        ax.axis("off")
    pngs.append(save_matplotlib(fig, unit, "figures", "edge-identification-gallery.png"))
    _close(fig)

    theta = np.linspace(0, 2 * np.pi, 160)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.cos(theta), y=np.sin(theta), mode="lines", name="orbit circle"))
    fig.add_trace(go.Scatter(x=np.cos(theta[::20]), y=np.sin(theta[::20]), mode="markers", name="sample representatives"))
    fig.update_layout(title="Orbit representatives for a rotation action", width=700, height=480)
    htmls = [save_plotly_html(fig, unit, "html", "rotation-orbit-representatives.html")]
    checks = [_save_check(unit, {"edge_models": [item[0] for item in labels], "html_artifacts": [path.name for path in htmls], "orbit_sample_count": int(len(theta[::20]))})]
    return pngs, htmls, checks, {"has_nonorientable_model": True}


def _chapter05(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "The fundamental group")]
    fig, ax = new_figure(6.5, 6.0)
    theta = np.linspace(0, 2 * np.pi, 400)
    for radius, color, label in [(1.2, PALETTE["blue"], "loop before"), (0.75, PALETTE["green"], "loop after")]:
        pts = np.column_stack([radius * np.cos(theta), radius * np.sin(theta)])
        ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=2.2, label=label)
    ax.scatter([0], [0], s=90, color=PALETTE["red"], label="puncture")
    ax.set_title("Homotopic loops around the same puncture preserve winding")
    ax.legend(fontsize=8)
    set_equal_axes(ax)
    pngs.append(save_matplotlib(fig, unit, "figures", "loop-homotopy-winding.png"))
    _close(fig)

    fig, ax = new_figure(8, 4.0)
    radii = np.linspace(0.2, 1.1, 8)
    for r in radii:
        ax.add_patch(Circle((0, 0), r, fill=False, edgecolor=PALETTE["purple"], alpha=0.22 + 0.06 * r, linewidth=1.5))
    ax.scatter([0], [0], color=PALETTE["ink"], s=70)
    ax.set_title("Deformation retraction: annulus loops slide to a core circle")
    set_equal_axes(ax)
    pngs.append(save_matplotlib(fig, unit, "figures", "deformation-retraction-annulus.png"))
    _close(fig)
    sample = np.column_stack([np.cos(theta), np.sin(theta)])
    checks = [_save_check(unit, {"winding_number_unit_loop": winding_number(sample), "loop_samples": int(len(theta)), "radii_count": int(len(radii))})]
    return pngs, [], checks, {"unit_loop_winds_once": winding_number(sample) == 1}


def _chapter06(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Triangulations")]
    vertices, triangles = barycentric_triangle()
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
    base = np.array([[0, 0], [1, 0], [0.35, 0.9]])
    axes[0].add_patch(Polygon(base, closed=True, fill=True, facecolor="#dbeafe", edgecolor=PALETTE["blue"], linewidth=2))
    axes[0].set_title("one 2-simplex")
    axes[0].set_aspect("equal")
    axes[0].axis("off")
    for tri in triangles:
        axes[1].add_patch(Polygon(vertices[list(tri)], closed=True, fill=True, facecolor="#dcfce7", edgecolor=PALETTE["green"], linewidth=1.5, alpha=0.75))
    axes[1].scatter(vertices[:, 0], vertices[:, 1], color=PALETTE["ink"], s=22)
    axes[1].set_title("barycentric subdivision")
    axes[1].set_aspect("equal")
    axes[1].axis("off")
    pngs.append(save_matplotlib(fig, unit, "figures", "barycentric-subdivision-triangle.png"))
    _close(fig)

    fig, ax = new_figure(6.5, 4.8)
    graph_edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (4, 1)]
    graph = nx.Graph(graph_edges)
    pos = {0: (0, 0), 1: (1, 0), 2: (0.5, 0.8), 3: (1.8, 0), 4: (1.4, 0.75)}
    nx.draw_networkx(graph, pos, ax=ax, node_color="#fde68a", edge_color=PALETTE["ink"], node_size=550, font_size=9)
    ax.set_title("Edge loops are words in a triangulated graph")
    ax.axis("off")
    pngs.append(save_matplotlib(fig, unit, "figures", "edge-loop-complex.png"))
    _close(fig)
    chi_before = euler_characteristic(3, 3, 1)
    chi_after = euler_characteristic(len(vertices), 12, len(triangles))
    checks = [_save_check(unit, {"chi_before_subdivision": chi_before, "chi_after_subdivision": chi_after, "subdivision_triangles": len(triangles)})]
    return pngs, [], checks, {"subdivision_preserves_chi": chi_before == chi_after}


def _chapter07(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Surfaces")]
    surfaces = pd.DataFrame(
        [
            {"surface": "sphere", "kind": "sphere", "parameter": 0},
            {"surface": "torus", "kind": "orientable", "parameter": 1},
            {"surface": "double torus", "kind": "orientable", "parameter": 2},
            {"surface": "projective plane", "kind": "nonorientable", "parameter": 1},
            {"surface": "Klein bottle", "kind": "nonorientable", "parameter": 2},
        ]
    )
    surfaces["chi"] = surfaces.apply(lambda row: surface_chi(row.kind, row.parameter), axis=1)
    fig, ax = new_figure(8, 4.5)
    ax.bar(surfaces.surface, surfaces.chi, color=[PALETTE["green"], PALETTE["blue"], PALETTE["blue"], PALETTE["red"], PALETTE["red"]])
    ax.axhline(0, color=PALETTE["ink"], linewidth=1)
    ax.set_title("Euler characteristic separates many closed surfaces")
    ax.set_ylabel("chi")
    ax.tick_params(axis="x", rotation=18)
    pngs.append(save_matplotlib(fig, unit, "figures", "surface-classification-chi-table.png"))
    _close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8))
    for ax, word, title in [(axes[0], "a b A B", "torus word"), (axes[1], "a a b b", "Klein-style word")]:
        ax.add_patch(Polygon([[0, 0], [1, 0], [1, 1], [0, 1]], closed=True, fill=False, edgecolor=PALETTE["ink"], linewidth=2))
        ax.text(0.5, -0.08, word.split()[0], ha="center", color=PALETTE["blue"])
        ax.text(1.08, 0.5, word.split()[1], va="center", color=PALETTE["green"])
        ax.text(0.5, 1.06, word.split()[2], ha="center", color=PALETTE["blue"])
        ax.text(-0.08, 0.5, word.split()[3], va="center", color=PALETTE["green"])
        ax.set_title(title)
        ax.set_aspect("equal")
        ax.axis("off")
    pngs.append(save_matplotlib(fig, unit, "figures", "surface-symbol-edge-words.png"))
    _close(fig)
    checks = [_save_check(unit, {"surfaces": surfaces.to_dict("records"), "torus_chi": int(surfaces.loc[surfaces.surface == "torus", "chi"].iloc[0])})]
    return pngs, [], checks, {"torus_chi_zero": int(surfaces.loc[surfaces.surface == "torus", "chi"].iloc[0]) == 0}


def _chapter08(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Simplicial homology")]
    vertices = [(0,), (1,), (2,)]
    edges = [(0, 1), (1, 2), (0, 2)]
    triangles = [(0, 1, 2)]
    d1 = boundary_matrix(edges, vertices)
    d2 = boundary_matrix(triangles, edges)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    axes[0].imshow(d1, cmap="coolwarm", vmin=-1, vmax=1)
    axes[0].set_title("boundary d1: edges to vertices")
    axes[0].set_xlabel("edges")
    axes[0].set_ylabel("vertices")
    axes[1].imshow(d2, cmap="coolwarm", vmin=-1, vmax=1)
    axes[1].set_title("boundary d2: triangle to edges")
    axes[1].set_xlabel("triangle")
    axes[1].set_ylabel("edges")
    pngs.append(save_matplotlib(fig, unit, "figures", "boundary-matrices-simplex.png"))
    _close(fig)

    fig, ax = new_figure(6, 5)
    pts = np.array([[0, 0], [1, 0], [0.45, 0.82]])
    draw_polygon(ax, pts, color=PALETTE["blue"], fill="#dbeafe", label="2-chain")
    for i, label in enumerate(["v0", "v1", "v2"]):
        ax.text(pts[i, 0], pts[i, 1] + 0.06, label, ha="center")
    ax.set_title("The boundary of a filled triangle is a cycle")
    set_equal_axes(ax)
    pngs.append(save_matplotlib(fig, unit, "figures", "cycle-as-boundary-triangle.png"))
    _close(fig)
    composition = d1 @ d2
    checks = [_save_check(unit, {"d1": d1.tolist(), "d2": d2.tolist(), "d1_d2": composition.tolist(), "rank_d1": rank(d1), "rank_d2": rank(d2)})]
    return pngs, [], checks, {"boundary_squared_zero": bool(np.all(composition == 0))}


def _chapter09(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Degree and Lefschetz number")]
    theta = np.linspace(0, 2 * np.pi, 500)
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))
    for ax, degree in zip(axes, [1, 2, -1]):
        ax.plot(np.cos(theta), np.sin(theta), color="#e5e7eb", linewidth=3)
        ax.plot(np.cos(degree * theta), np.sin(degree * theta), color=PALETTE["blue"], linewidth=1.5)
        ax.set_title(f"circle map degree {degree}")
        ax.set_aspect("equal")
        ax.axis("off")
    pngs.append(save_matplotlib(fig, unit, "figures", "circle-map-degrees.png"))
    _close(fig)

    fig, ax = new_figure(6.5, 4.5)
    x = np.linspace(-2, 2, 400)
    f = 0.55 * x**3 - x + 0.25
    ax.plot(x, f, color=PALETTE["blue"], label="f(x)")
    ax.plot(x, x, color=PALETTE["ink"], linestyle="--", label="identity")
    roots = np.roots([0.55, 0, -2, 0.25])
    real_roots = [root.real for root in roots if abs(root.imag) < 1e-8 and -2 <= root.real <= 2]
    ax.scatter(real_roots, real_roots, color=PALETTE["red"], zorder=4, label="fixed points")
    ax.legend(fontsize=8)
    ax.set_title("Fixed points appear where graph and identity meet")
    pngs.append(save_matplotlib(fig, unit, "figures", "lefschetz-fixed-point-sketch.png"))
    _close(fig)
    checks = [_save_check(unit, {"degrees": [1, 2, -1], "fixed_point_samples": [float(v) for v in real_roots], "fixed_point_count": len(real_roots)})]
    return pngs, [], checks, {"found_fixed_points": len(real_roots) >= 1}


def _chapter10(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Knots and covering spaces")]
    t = np.linspace(0, 2 * np.pi, 800)
    x = np.sin(t) + 2 * np.sin(2 * t)
    y = np.cos(t) - 2 * np.cos(2 * t)
    z = -np.sin(3 * t)
    fig = plt.figure(figsize=(8, 5.2))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot3D(x, y, z, color=PALETTE["blue"], linewidth=2)
    ax.set_title("Trefoil-style parametrized knot for spatial inspection")
    ax.set_axis_off()
    pngs.append(save_matplotlib(fig, unit, "figures", "trefoil-parametric-knot.png"))
    _close(fig)

    t_symbol = sp.symbols("t")
    matrix = sp.Matrix([[1 - t_symbol, -1], [t_symbol, 1 - t_symbol]])
    fig, ax = new_figure(5.8, 4.8)
    ax.imshow(np.array([[1, -1], [1, 1]], dtype=float), cmap="coolwarm", vmin=-1, vmax=1)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(matrix[i, j]), ha="center", va="center", fontsize=14, color=PALETTE["ink"])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Presentation matrix behind the trefoil Alexander polynomial")
    pngs.append(save_matplotlib(fig, unit, "figures", "trefoil-alexander-matrix.png"))
    _close(fig)
    polynomial = sp.expand(trefoil_alexander_polynomial())
    checks = [_save_check(unit, {"alexander_polynomial": str(polynomial), "trefoil_samples": int(len(t)), "matrix_determinant": str(matrix.det())})]
    return pngs, [], checks, {"trefoil_polynomial": str(polynomial)}


def _appendix(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Generators and relations")]
    word = list("abBAcCAb")
    trace = word_reduction_trace(word)
    fig, ax = new_figure(8, 4.8)
    lengths = [len(item) for item in trace]
    ax.step(range(len(lengths)), lengths, where="post", color=PALETTE["blue"], linewidth=2.5)
    ax.scatter(range(len(lengths)), lengths, color=PALETTE["red"], s=30)
    ax.set_title("Free-word reduction as cancellation over time")
    ax.set_xlabel("letters read")
    ax.set_ylabel("reduced length")
    pngs.append(save_matplotlib(fig, unit, "figures", "free-word-reduction-trace.png"))
    _close(fig)

    fig, ax = new_figure(7, 4.5)
    graph = nx.Graph()
    graph.add_edges_from([("free group", "generators"), ("free group", "reduced words"), ("presentation", "relations"), ("presentation", "quotient"), ("free product", "universal property")])
    pos = nx.spring_layout(graph, seed=42)
    nx.draw_networkx(graph, pos, ax=ax, node_color="#c7d2fe", edge_color=PALETTE["ink"], node_size=1500, font_size=9)
    ax.set_title("Algebra objects used by edge and knot groups")
    ax.axis("off")
    pngs.append(save_matplotlib(fig, unit, "figures", "presentation-algebra-map.png"))
    _close(fig)
    checks = [_save_check(unit, {"word": "".join(word), "reduced": "".join(reduce_word(word)), "trace_lengths": lengths})]
    return pngs, [], checks, {"reduced_word": "".join(reduce_word(word))}


BUILDERS = {
    "chapter-01": _chapter01,
    "chapter-02": _chapter02,
    "chapter-03": _chapter03,
    "chapter-04": _chapter04,
    "chapter-05": _chapter05,
    "chapter-06": _chapter06,
    "chapter-07": _chapter07,
    "chapter-08": _chapter08,
    "chapter-09": _chapter09,
    "chapter-10": _chapter10,
    "appendix-generators-and-relations": _appendix,
}


def build_unit_visuals(unit: str, *, force: bool = True) -> dict[str, list[Path]]:
    if unit not in BUILDERS:
        raise KeyError(f"unknown Basic Topology unit: {unit}")
    pngs, htmls, checks, _ = BUILDERS[unit](unit)
    return {"png": pngs, "html": htmls, "checks": checks}


def run_unit_lab(unit: str) -> dict[str, Any]:
    if unit == "chapter-01":
        return {"chi_tetrahedron": euler_characteristic(4, 6, 4), "chi_torus_cell_model": euler_characteristic(1, 2, 1)}
    if unit == "chapter-02":
        xs = np.linspace(-2, 2, 200)
        return {"samples": len(xs), "preimage_count": int(((xs**2 > 0.25) & (xs**2 < 1.5)).sum())}
    if unit == "chapter-03":
        intervals = [(-0.05, 0.32), (0.2, 0.58), (0.47, 0.83), (0.72, 1.05)]
        return {"finite_subcover_size": len(intervals), "covers_unit_interval": min(a for a, _ in intervals) <= 0 and max(b for _, b in intervals) >= 1}
    if unit == "chapter-04":
        return {"quotient_models": ["cylinder", "Mobius strip", "torus"], "nonorientable_example": "Mobius strip"}
    if unit == "chapter-05":
        theta = np.linspace(0, 2 * np.pi, 300)
        loop = np.column_stack([np.cos(theta), np.sin(theta)])
        return {"winding_number": winding_number(loop), "loop_samples": len(theta)}
    if unit == "chapter-06":
        return {"chi_before": euler_characteristic(3, 3, 1), "chi_after": euler_characteristic(7, 12, 6)}
    if unit == "chapter-07":
        return {"sphere_chi": surface_chi("sphere"), "genus_2_chi": surface_chi("orientable", 2), "klein_chi": surface_chi("nonorientable", 2)}
    if unit == "chapter-08":
        d1 = boundary_matrix([(0, 1), (1, 2), (0, 2)], [(0,), (1,), (2,)])
        d2 = boundary_matrix([(0, 1, 2)], [(0, 1), (1, 2), (0, 2)])
        return {"boundary_squared_zero": bool(np.all(d1 @ d2 == 0)), "rank_d1": rank(d1), "rank_d2": rank(d2)}
    if unit == "chapter-09":
        return {"circle_map_degrees": [1, 2, -1], "lefschetz_identity_on_circle": 0}
    if unit == "chapter-10":
        return {"trefoil_alexander_polynomial": str(trefoil_alexander_polynomial())}
    if unit == "appendix-generators-and-relations":
        word = list("abBAcCAb")
        return {"word": "".join(word), "reduced": "".join(reduce_word(word))}
    raise KeyError(unit)
'''


def inventory_py() -> str:
    return dedent(
        f'''
        """Inventory for the Basic Topology standalone notebook course."""

        from __future__ import annotations

        from typing import Any

        PDF_SOURCE = "armstrong-basic-topology.pdf"
        SOLUTIONS_SOURCE = "armstrong-basic-topology-solutions.pdf"
        SOURCE_SPAN_NOTES = {SOURCE_SPAN_NOTES!r}
        ENTRIES: list[dict[str, Any]] = {ENTRIES!r}
        BACK_MATTER: list[dict[str, str]] = {BACK_MATTER!r}
        '''
    )


BUILD_INDEXES_PY = r'''
"""Build Basic Topology book and unit indexes."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

from bt_inventory import BACK_MATTER, ENTRIES, SOURCE_SPAN_NOTES

BOOK_ROOT = Path(__file__).resolve().parents[1]


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook(cells=[new_markdown_cell(text.strip() + "\n")])
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python", "version": "3.13"}
    nbformat.write(nb, path)


def canonical_link(entry: dict[str, object]) -> str:
    return f"{entry['folder']}/{entry['notebook']}"


def build_book_index() -> str:
    lines = [
        "# Basic Topology - Standalone Notebook Course",
        "",
        "This course is an original executable notebook edition of M. A. Armstrong's *Basic Topology*. It uses the local PDFs only for source orientation and replaces passive reading with generated diagrams, plots, algebra checks, and computational labs.",
        "",
        "## Source Notes",
        "",
    ]
    for note in SOURCE_SPAN_NOTES:
        lines.append(f"- {note}")
    lines.extend(["", "## Course Units", ""])
    for entry in ENTRIES:
        lines.append(
            f"- [{entry['label']}: {entry['title']}]({entry['folder']}/00-index.ipynb) - "
            f"[canonical notebook]({canonical_link(entry)}); printed pp. {entry['printed_span']}; "
            f"PDF pp. {entry['pdf_span']}; {entry['focus']}"
        )
    lines.extend(["", "## Back Matter Inventory", ""])
    for item in BACK_MATTER:
        lines.append(f"- {item['title']}: printed pp. {item['printed_span']}; PDF pp. {item['pdf_span']}")
    lines.extend(
        [
            "",
            "## Validation",
            "",
            "Run the book-local index builder, compile check, notebook audit, visual audit, limited execution, and `git diff --check` from the workspace root.",
        ]
    )
    return "\n".join(lines)


def build_unit_index(entry: dict[str, object]) -> str:
    topics = "\n".join(f"- {topic}" for topic in entry["topics"])
    return f"""
# {entry['label']}: {entry['title']}

[Back to Book Index](../00-book-index.ipynb)

- Canonical notebook: [{entry['notebook']}]({entry['notebook']})
- Source span: printed pp. {entry['printed_span']}; PDF pp. {entry['pdf_span']}
- Sections: {entry['sections']}
- Focus: {entry['focus']}

## Topics

{topics}

## Artifact Root

Generated diagrams, interactive HTML, and check JSON for this unit live under
`artifacts/{entry['artifact']}/`.
"""


def main() -> None:
    missing = []
    for entry in ENTRIES:
        canonical = BOOK_ROOT / str(entry["folder"]) / str(entry["notebook"])
        if not canonical.exists():
            missing.append(canonical)
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))

    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for entry in ENTRIES:
        write_markdown_notebook(BOOK_ROOT / str(entry["folder"]) / "00-index.ipynb", build_unit_index(entry))
    print(f"Updated book index and {len(ENTRIES)} unit indexes.")


if __name__ == "__main__":
    main()
'''


AUDIT_NOTEBOOKS_PY = r'''
"""Audit Basic Topology notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import discover_canonical_notebooks, notebook_stats  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()

    stats = [notebook_stats(path, BOOK_ROOT) for path in discover_canonical_notebooks(BOOK_ROOT)]
    failing = [
        item
        for item in stats
        if item["markdown_words"] < args.min_words
        or item["code_cells"] < args.min_code_cells
        or item["display_artifact_calls"] < 1
        or item["visual_builder_calls"] < 1
        or item["assert_artifact_calls"] < 1
        or not item["has_applied_lab"]
        or not item["has_takeaways"]
        or item["stale_paths"]
    ]
    report = {"notebook_count": len(stats), "failing_count": len(failing), "failing": failing, "stats": stats}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(stats)} canonical notebooks")
    if failing:
        print(f"{len(failing)} notebooks failed the audit:")
        for item in failing:
            print(
                f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells, "
                f"display calls={item['display_artifact_calls']}, visual builders={item['visual_builder_calls']}, "
                f"assert calls={item['assert_artifact_calls']}, stale_paths={item['stale_paths']}"
            )
        raise SystemExit(1)
    print("All canonical notebooks meet the configured standalone structure thresholds.")


if __name__ == "__main__":
    main()
'''


AUDIT_VISUALS_PY = r'''
"""Audit Basic Topology generated visual artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

from bt_inventory import ENTRIES

BOOK_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ImageStats:
    path: str
    width: int
    height: int
    bytes: int
    sha256: str
    max_channel_stddev: float


def _relative(path: Path) -> str:
    return path.relative_to(BOOK_ROOT).as_posix()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_stats(path: Path) -> ImageStats:
    with Image.open(path) as image:
        image.load()
        width, height = image.size
        stat = ImageStat.Stat(image.convert("RGB"))
    return ImageStats(
        path=_relative(path),
        width=width,
        height=height,
        bytes=path.stat().st_size,
        sha256=_sha256(path),
        max_channel_stddev=max(stat.stddev) if stat.stddev else 0.0,
    )


def audit() -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    image_items: list[ImageStats] = []
    artifact_root = BOOK_ROOT / "artifacts"
    for entry in ENTRIES:
        unit = str(entry["artifact"])
        unit_root = artifact_root / unit
        pngs = sorted(unit_root.rglob("*.png")) if unit_root.exists() else []
        htmls = sorted(unit_root.rglob("*.html")) if unit_root.exists() else []
        checks = sorted(unit_root.rglob("*.json")) if unit_root.exists() else []
        if not pngs:
            findings.append({"check": "missing-png", "path": _relative(unit_root), "message": f"{unit} has no PNG artifact."})
        if not checks:
            findings.append({"check": "missing-json-check", "path": _relative(unit_root), "message": f"{unit} has no JSON check artifact."})
        for html in htmls:
            if html.stat().st_size < 512:
                findings.append({"check": "tiny-html", "path": _relative(html), "message": "Interactive HTML is unexpectedly small."})
        for check in checks:
            try:
                json.loads(check.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                findings.append({"check": "bad-json", "path": _relative(check), "message": str(exc)})
        for png in pngs:
            try:
                item = image_stats(png)
            except OSError as exc:
                findings.append({"check": "unreadable-image", "path": _relative(png), "message": str(exc)})
                continue
            image_items.append(item)
            if item.width < 64 or item.height < 64 or item.width * item.height < 4096:
                findings.append({"check": "tiny-image", "path": item.path, "message": f"Image is too small: {item.width}x{item.height}."})
            if item.max_channel_stddev <= 1.0:
                findings.append({"check": "blank-image", "path": item.path, "message": "Image appears blank or nearly constant."})
    by_hash: dict[str, list[ImageStats]] = {}
    for item in image_items:
        by_hash.setdefault(item.sha256, []).append(item)
    for digest, matches in by_hash.items():
        if len(matches) > 1:
            findings.append(
                {
                    "check": "duplicate-image",
                    "path": ", ".join(item.path for item in matches),
                    "message": f"{len(matches)} PNG artifacts share the same hash {digest[:12]}.",
                }
            )
    return {
        "image_count": len(image_items),
        "findings_count": len(findings),
        "findings": findings,
        "images": [asdict(item) for item in image_items],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit()
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {report['image_count']} PNG artifacts")
    if report["findings"]:
        print(f"{len(report['findings'])} visual audit findings:")
        for item in report["findings"]:
            print(f"- {item['check']} {item['path']}: {item['message']}")
        raise SystemExit(1)
    print("Visual artifacts are present, readable, nonblank, and nonduplicate.")


if __name__ == "__main__":
    main()
'''


VALIDATE_COURSE_PY = r'''
"""Execute Basic Topology notebooks with nbclient."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import discover_canonical_notebooks  # noqa: E402

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


SMOKE_NAMES = {
    "01-introduction.ipynb",
    "02-continuity.ipynb",
    "05-the-fundamental-group.ipynb",
    "08-simplicial-homology.ipynb",
    "10-knots-and-covering-spaces.ipynb",
}


def notebook_paths(all_notebooks: bool, smoke: bool, limit: int | None) -> list[Path]:
    paths = discover_canonical_notebooks(BOOK_ROOT)
    if smoke:
        paths = [path for path in paths if path.name in SMOKE_NAMES]
    if not all_notebooks and not smoke:
        paths = paths[:]
    if limit is not None:
        paths = paths[:limit]
    return paths


def execute_notebook(path: Path, timeout: int) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    paths = notebook_paths(args.all, args.smoke, args.limit)
    if not paths:
        raise SystemExit("no notebooks found")
    failures: list[tuple[Path, str]] = []
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


def setup_cell() -> str:
    return dedent(
        """
        from pathlib import Path
        import sys

        def find_book_root(start: Path) -> Path:
            for candidate in [start, *start.parents]:
                if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
                    return candidate
            raise RuntimeError("Could not find Basic-Topology book root")

        BOOK_ROOT = find_book_root(Path.cwd())
        if str(BOOK_ROOT) not in sys.path:
            sys.path.insert(0, str(BOOK_ROOT))

        BOOK_ROOT
        """
    )


def teaching_markdown(entry: dict[str, Any]) -> str:
    topics = entry["topics"]
    topic_lines = "\n".join(f"- **{topic}.** This notebook turns the phrase into an object we can inspect, compute with, or test against a small model." for topic in topics)
    artifact_root = entry["artifact"]
    figure_plan = {
        "chapter-01": "Euler-count bars, a concept-dependency graph, and a torus surface model introduce the course habit of separating cell counts from invariant alternating sums.",
        "chapter-02": "A preimage band, sampled curve data, and a stage approximation to a square-filling path make continuity a test about neighborhoods rather than a drawing style.",
        "chapter-03": "A finite-subcover interval display and an oscillating closure model compare compactness, connectedness, and the extra work needed for path connectedness.",
        "chapter-04": "Edge-identification panels and an orbit-representative HTML artifact show how quotient maps remember equivalence classes while forgetting original labels.",
        "chapter-05": "Loop-winding and deformation-retraction figures turn homotopy classes into measured loop behavior around an obstruction.",
        "chapter-06": "Subdivision and edge-loop diagrams show how triangulations turn continuous spaces into finite combinatorial data without changing the target invariant.",
        "chapter-07": "Surface-symbol panels and Euler-characteristic tables connect the classification theorem to orientability, handles, crosscaps, and surgery.",
        "chapter-08": "Boundary-matrix heatmaps and a filled-triangle cycle diagram make chains, cycles, and boundaries visible as both pictures and linear maps.",
        "chapter-09": "Circle-map degree panels and a fixed-point graph sketch connect homological invariants to global consequences of a map.",
        "chapter-10": "A generated trefoil-style spatial curve and an Alexander-matrix heatmap join knot geometry to the algebra of presentations.",
        "appendix-generators-and-relations": "A free-word reduction trace and presentation map give the algebraic grammar later used for edge groups and knot groups.",
    }[entry["id"]]
    visual_lines = "\n".join(
        [
            f"- Build a concept map connecting `{topics[0]}` to the rest of the chapter's vocabulary.",
            f"- Generate concrete artifacts for `{artifact_root}` and pair each one with an invariant or observation.",
            f"- Specific visual commitment: {figure_plan}",
            "- Record a JSON check so the figure is not just illustrative; it carries a reproducible numerical claim.",
            "- Use the applied lab to make the reader change a parameter, compute a value, and state what stayed invariant.",
        ]
    )
    concept_paragraphs = [
        f"This notebook is a standalone computational lesson for {entry['label'].lower()}, {entry['title']}. The source pages are printed pp. {entry['printed_span']} and PDF pp. {entry['pdf_span']}, but the goal here is not to paraphrase the book. The goal is to make the chapter's topology visible enough that a reader can learn from this notebook without opening the PDF. The original text is a guide for structure and emphasis; the explanations, examples, diagrams, checks, and labs below are rebuilt for this course.",
        f"The chapter question is: how can we recognize the same topological idea when the geometry has been redrawn, deformed, subdivided, or encoded algebraically? In this unit the central focus is {entry['focus']} That means every definition is paired with an operation a reader can perform: count cells, test a preimage, follow a quotient map, reduce a loop word, build a boundary matrix, or compare a map invariant.",
        "A useful habit in topology is to distinguish flexible data from rigid data. Coordinates, drawings, and triangulations often change. Incidence, separation, homotopy class, orientability, Euler characteristic, degree, or a quotient relation may survive those changes. The notebook keeps returning to this distinction because it is the thread connecting point-set topology, geometric topology, and algebraic topology in this book.",
        "The visual artifacts are not decorations. Each figure is designed as a small instrument: it marks what the learner should inspect, exposes the relevant local or global structure, and gives the later code cell something to check. If a picture shows a loop, the code asks what invariant of the loop is being preserved. If a picture shows a quotient, the code asks what information the projection forgets. If a picture shows a matrix, the code asks which algebraic condition encodes the topological statement.",
        "The worked examples intentionally use small models. A small model can be incomplete as geometry while still being perfect as a microscope for a theorem. A triangle, square-edge schema, sampled loop, or two-by-two presentation matrix lets the reader see the mechanism before meeting the general statement. After the mechanism is clear, the same code pattern scales to more complicated complexes, surfaces, covering spaces, or knot diagrams.",
        f"The applied lab for this unit is: {entry['lab']} The expected output is not a long proof. It is a short diagnostic: name the quantity that changed, name the quantity that did not change, and explain why the invariant is the better topological description. That habit is the course's substitute for rote exercise copying.",
        "The sanity checks at the end are part of the teaching. They assert that artifact files exist, that the nonblank figures were actually generated under the book-local artifact tree, and that the numerical or symbolic claim used in the prose is reproducible. A notebook that cannot regenerate its own evidence is not yet a standalone lesson.",
        f"Copyright discipline matters for this course. Standard mathematical vocabulary is unavoidable, but the exposition, captions, examples, code, and visuals here are original course material. The artifacts are generated from formulas, graph layouts, matrices, or meshes in `utils.visuals`; they are not screenshots, traced textbook figures, page crops, or copied solution text. When a notebook mentions a source span, it is giving provenance for topic coverage rather than asking the reader to consult the PDF.",
        f"Reader workflow is intentionally active. First run the setup cell so `BOOK_ROOT` is discovered from the notebook location. Then build the artifacts, inspect each inline display, and read the JSON check as a compact certificate. Finally rerun the applied lab after changing a parameter. The important question after every rerun is whether the visual form changed while the topological invariant in the check remained stable.",
        f"For this unit, the artifact subtree is `artifacts/{artifact_root}/`. Keeping the evidence local to the book has two benefits: it makes the notebook portable, and it lets the visual audit reject blank, duplicated, or missing files. The course is meant to be rebuilt, not merely viewed once.",
        f"Concept-to-code checklist: identify the topological object, identify the allowed transformations, choose the smallest computable model that still preserves the issue, and only then inspect the invariant. In this chapter the model is intentionally modest: it may be a sampled path, a finite graph, a cell count, a matrix, a word, or a schematic surface. The point is not to pretend the model is the entire theorem. The point is to make the theorem's moving parts explicit enough that the reader can test one claim at a time. When a visual artifact looks simple, ask which assumption it is isolating.",
        "Common traps are called out implicitly by the checks. A drawing that looks connected may still fail a path test. A bijection can fail to be a homeomorphism if the inverse mishandles neighborhoods. A quotient picture can hide several original points inside one displayed point. A triangulation may be replaced by a subdivision without changing the underlying polyhedron. A chain can be closed without being the boundary of a higher-dimensional chain. Keeping these traps visible is what makes the notebook a course rather than a gallery.",
        f"After studying the unit, a reader should be able to narrate the artifact sequence without textbook support: `{topics[0]}` supplies the opening object, the middle visuals expose the mechanism, and the final check records the invariant. That narration is the acceptance criterion for the chapter. If the reader can explain why the JSON value belongs next to the diagram, the visualization has done real mathematical work.",
    ]
    return "\n\n".join(
        [
            f"# {entry['label']}: {entry['title']}",
            f"**Source orientation:** printed pp. {entry['printed_span']}; PDF pp. {entry['pdf_span']}.",
            "## Chapter Question",
            concept_paragraphs[0],
            concept_paragraphs[1],
            "## Translation Guide",
            topic_lines,
            "## Route Through The Notebook",
            concept_paragraphs[2],
            concept_paragraphs[3],
            "## Visual Storyboard",
            visual_lines,
            "## Worked Example Strategy",
            concept_paragraphs[4],
            "## Concept-To-Code Checklist",
            concept_paragraphs[10],
            concept_paragraphs[11],
            concept_paragraphs[12],
            "## Applied Lab",
            concept_paragraphs[5],
            "## Sanity Check Contract",
            concept_paragraphs[6],
        ]
    )


def reflection_markdown(entry: dict[str, Any]) -> str:
    topics = ", ".join(entry["topics"])
    return dedent(
        f"""
        ## Reading The Checks

        The dictionary produced below is deliberately small. It is a set of
        computational witnesses for the chapter vocabulary: {topics}. For a
        first pass, read the values as claims attached to the figures. For a
        second pass, change one of the parameters in the code cells, rerun the
        notebook, and decide whether the output changed for geometric reasons
        or merely because the drawing changed.

        This is the main habit Armstrong's course rewards. The object in front
        of us may be a surface drawing, a quotient square, a loop, a finite
        complex, a chain group, or a knot diagram. The topological question is
        never simply what the object looks like. The question is which
        transformation is allowed, and which quantity remains meaningful after
        that transformation has been applied.
        """
    )


def takeaways_markdown(entry: dict[str, Any]) -> str:
    bullets = "\n".join(f"- {topic} is useful when it is tied to a visible model and a checkable invariant." for topic in entry["topics"][:3])
    return dedent(
        f"""
        ## Takeaways

        {bullets}
        - The artifact files under `artifacts/{entry['artifact']}/` are part of the lesson, not disposable output.
        - The source PDF oriented the structure, but this notebook supplies the standalone explanations, examples, and checks.
        """
    )


def notebook_for(entry: dict[str, Any]) -> Any:
    unit = entry["id"]
    nb = new_notebook()
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python", "version": "3.13"}
    nb.cells = [
        new_markdown_cell(teaching_markdown(entry)),
        new_code_cell(setup_cell()),
        new_code_cell(
            dedent(
                f"""
                from utils.visuals import build_unit_visuals, run_unit_lab
                from utils.artifacts import assert_artifact, display_artifact

                outputs = build_unit_visuals("{unit}")
                outputs
                """
            )
        ),
        new_markdown_cell(
            "## Inline Visual Artifacts\n\nThe following artifacts are generated under the book-local artifact tree and displayed inline. Inspect the labels first, then compare the figure with the JSON checks in the next cell."
        ),
        new_code_cell(
            dedent(
                """
                for path in outputs["png"]:
                    assert_artifact(path, min_bytes=1024)
                    display_artifact(path, width=760)

                for path in outputs["html"]:
                    assert_artifact(path, min_bytes=512)
                    display_artifact(path, width="100%", height=480)
                """
            )
        ),
        new_code_cell(
            dedent(
                """
                import json
                import pandas as pd
                from pathlib import Path

                checks = [json.loads(Path(path).read_text(encoding="utf-8")) for path in outputs["checks"]]
                pd.json_normalize(checks)
                """
            )
        ),
        new_markdown_cell(reflection_markdown(entry)),
        new_code_cell(
            dedent(
                f"""
                lab = run_unit_lab("{unit}")
                lab
                """
            )
        ),
        new_code_cell(
            dedent(
                """
                assert outputs["png"], "expected at least one PNG artifact"
                assert outputs["checks"], "expected at least one JSON check artifact"
                for path in outputs["png"]:
                    assert_artifact(path, min_bytes=1024)
                for path in outputs["html"]:
                    assert_artifact(path, min_bytes=512)
                for path in outputs["checks"]:
                    assert_artifact(path, min_bytes=64)
                assert isinstance(lab, dict) and lab, "lab output should be a nonempty dictionary"
                """
            )
        ),
        new_markdown_cell(takeaways_markdown(entry)),
    ]
    return nb


def book_index_text() -> str:
    lines = [
        "# Basic Topology - Standalone Notebook Course",
        "",
        "This course is an original executable notebook edition of M. A. Armstrong's *Basic Topology*. It uses the local PDFs only for source orientation and replaces passive reading with generated diagrams, plots, algebra checks, and computational labs.",
        "",
        "## Source Notes",
        "",
    ]
    for note in SOURCE_SPAN_NOTES:
        lines.append(f"- {note}")
    lines.extend(["", "## Course Units", ""])
    for entry in ENTRIES:
        lines.append(
            f"- [{entry['label']}: {entry['title']}]({entry['folder']}/00-index.ipynb) - "
            f"[canonical notebook]({entry['folder']}/{entry['notebook']}); printed pp. {entry['printed_span']}; "
            f"PDF pp. {entry['pdf_span']}; {entry['focus']}"
        )
    lines.extend(["", "## Back Matter Inventory", ""])
    for item in BACK_MATTER:
        lines.append(f"- {item['title']}: printed pp. {item['printed_span']}; PDF pp. {item['pdf_span']}")
    return "\n".join(lines)


def unit_index_text(entry: dict[str, Any]) -> str:
    topics = "\n".join(f"- {topic}" for topic in entry["topics"])
    return f"""
# {entry['label']}: {entry['title']}

[Back to Book Index](../00-book-index.ipynb)

- Canonical notebook: [{entry['notebook']}]({entry['notebook']})
- Source span: printed pp. {entry['printed_span']}; PDF pp. {entry['pdf_span']}
- Sections: {entry['sections']}
- Focus: {entry['focus']}

## Topics

{topics}

## Artifact Root

Generated diagrams, interactive HTML, and check JSON for this unit live under
`artifacts/{entry['artifact']}/`.
"""


def write_course_files() -> None:
    (BOOK_ROOT / "artifacts").mkdir(exist_ok=True)
    (BOOK_ROOT / "utils").mkdir(exist_ok=True)
    (BOOK_ROOT / "scripts").mkdir(exist_ok=True)

    write_text(BOOK_ROOT / "AGENTS.md", AGENTS_MD)
    write_module(BOOK_ROOT / "utils" / "__init__.py", UTILS_INIT)
    write_module(BOOK_ROOT / "utils" / "artifacts.py", ARTIFACTS_PY)
    write_module(BOOK_ROOT / "utils" / "plotting.py", PLOTTING_PY)
    write_module(BOOK_ROOT / "utils" / "topology.py", TOPOLOGY_PY)
    write_module(BOOK_ROOT / "utils" / "simplicial.py", SIMPLICIAL_PY)
    write_module(BOOK_ROOT / "utils" / "knots.py", KNOTS_PY)
    write_module(BOOK_ROOT / "utils" / "validation.py", VALIDATION_PY)
    write_module(BOOK_ROOT / "utils" / "visuals.py", VISUALS_PY)

    write_module(BOOK_ROOT / "scripts" / "bt_inventory.py", inventory_py())
    write_module(BOOK_ROOT / "scripts" / "build_bt_course_indexes.py", BUILD_INDEXES_PY)
    write_module(BOOK_ROOT / "scripts" / "audit_bt_notebooks.py", AUDIT_NOTEBOOKS_PY)
    write_module(BOOK_ROOT / "scripts" / "audit_bt_visuals.py", AUDIT_VISUALS_PY)
    write_module(BOOK_ROOT / "scripts" / "validate_bt_course.py", VALIDATE_COURSE_PY)

    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", book_index_text())
    for entry in ENTRIES:
        folder = BOOK_ROOT / entry["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        nbformat.write(notebook_for(entry), folder / entry["notebook"])
        write_markdown_notebook(folder / "00-index.ipynb", unit_index_text(entry))


def build_initial_artifacts() -> None:
    if str(BOOK_ROOT) not in sys.path:
        sys.path.insert(0, str(BOOK_ROOT))
    importlib.invalidate_caches()
    visuals = importlib.import_module("utils.visuals")
    for entry in ENTRIES:
        visuals.build_unit_visuals(entry["id"])


def main() -> None:
    write_course_files()
    build_initial_artifacts()
    manifest = {
        "course": "Basic Topology",
        "unit_count": len(ENTRIES),
        "folders": [entry["folder"] for entry in ENTRIES],
    }
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
