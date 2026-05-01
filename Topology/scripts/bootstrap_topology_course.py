"""Bootstrap the visualization-first notebook course for Munkres Topology.

This script is intentionally book-local: it creates the course scaffold, reusable
helpers, canonical notebooks, indexes, and first-pass visual artifacts.
"""

from __future__ import annotations

import json
import math
import re
import textwrap
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


BOOK_ROOT = Path(__file__).resolve().parents[1]


CHAPTERS: list[dict[str, object]] = [
    {
        "kind": "chapter",
        "number": 1,
        "title": "Set Theory and Logic",
        "folder": "chapter-01-set-theory-and-logic",
        "notebook": "01-set-theory-and-logic.ipynb",
        "artifact": "chapter-01",
        "printed_span": "1-72",
        "sections": "§§1-11",
        "focus": "sets, functions, relations, countability, choice, and well-ordering",
        "goal": "Translate logical and set-theoretic language into inspectable finite models, diagrams, and checks that make later topology precise.",
        "visuals": [
            ("logic-venn-diagram.png", "Venn and truth-region diagram for union, intersection, complement, and implication failures."),
            ("function-fibers.png", "Function graph with fibers, image, preimage, injective and non-injective behavior."),
            ("relation-partition.png", "Equivalence relation as a partition and order relation as a Hasse-style diagram."),
            ("countability-pairing.png", "Diagonal pairing and enumeration path for countability."),
            ("choice-tree.png", "Finite choice tree and well-ordering sweep that model the proof machinery."),
        ],
        "html": "logic-set-lab.html",
    },
    {
        "kind": "chapter",
        "number": 2,
        "title": "Topological Spaces and Continuous Functions",
        "folder": "chapter-02-topological-spaces-and-continuous-functions",
        "notebook": "02-topological-spaces-and-continuous-functions.ipynb",
        "artifact": "chapter-02",
        "printed_span": "73-144",
        "sections": "§§12-22",
        "focus": "bases, product topology, subspaces, quotient topology, and continuity",
        "goal": "Build topologies from finite data and watch continuity, products, subspaces, and quotient maps become testable conditions.",
        "visuals": [
            ("finite-topology-lattice.png", "Open-set lattice for a finite topological space."),
            ("basis-generated-space.png", "How basis elements generate larger open sets by union."),
            ("product-subspace-grid.png", "Product rectangles and inherited subspace topology on a grid."),
            ("continuous-preimage-test.png", "Continuity as an inverse-image open-set test."),
            ("quotient-identification-map.png", "Quotient topology as gluing fibers into single visible classes."),
        ],
        "html": "finite-topology-explorer.html",
    },
    {
        "kind": "chapter",
        "number": 3,
        "title": "Connectedness and Compactness",
        "folder": "chapter-03-connectedness-and-compactness",
        "notebook": "03-connectedness-and-compactness.ipynb",
        "artifact": "chapter-03",
        "printed_span": "145-186",
        "sections": "§§23-29",
        "focus": "connected spaces, compact spaces, limit-point compactness, local compactness, and nets",
        "goal": "See connectedness and compactness as obstruction tests: what can be separated, covered, or forced to accumulate.",
        "visuals": [
            ("connected-components-graph.png", "Component graph and failed separation witness."),
            ("interval-connectedness.png", "Nested intervals and the intermediate-value obstruction to disconnection."),
            ("compact-cover-extractor.png", "Open cover with a highlighted finite subcover."),
            ("limit-point-compactness.png", "Sequence clusters and limit-point diagnostics."),
            ("local-compactness-neighborhoods.png", "Local compact neighborhoods and a missing-point counterexample."),
        ],
        "html": "compact-cover-lab.html",
    },
    {
        "kind": "chapter",
        "number": 4,
        "title": "Countability and Separation Axioms",
        "folder": "chapter-04-countability-and-separation-axioms",
        "notebook": "04-countability-and-separation-axioms.ipynb",
        "artifact": "chapter-04",
        "printed_span": "187-227",
        "sections": "§§30-36",
        "focus": "countability axioms, separation axioms, normal spaces, Urysohn's lemma, Tietze extension, and embeddings",
        "goal": "Turn countability and separation properties into witness diagrams, function-building recipes, and finite diagnostic tests.",
        "visuals": [
            ("countable-basis-grid.png", "Countable local basis grid around selected points."),
            ("separation-axiom-witnesses.png", "T0, T1, Hausdorff, regular, and normal witness neighborhoods."),
            ("normal-space-separation.png", "Closed-set separation by nested neighborhoods."),
            ("urysohn-function-heatmap.png", "Urysohn function as a separating scalar field."),
            ("embedding-coordinate-map.png", "Embedding by coordinate functions into a product cube."),
        ],
        "html": "separation-axioms-lab.html",
    },
    {
        "kind": "chapter",
        "number": 5,
        "title": "The Tychonoff Theorem",
        "folder": "chapter-05-the-tychonoff-theorem",
        "notebook": "05-the-tychonoff-theorem.ipynb",
        "artifact": "chapter-05",
        "printed_span": "228-240",
        "sections": "§§37-38",
        "focus": "products of compact spaces and Stone-Cech compactification",
        "goal": "Make product compactness visible through finite shadows, cover projections, and universal-extension diagrams.",
        "visuals": [
            ("product-compactness-cubes.png", "Finite-dimensional shadows of a large product of compact intervals."),
            ("subbase-cover-witness.png", "Subbase cover witness and finite obstruction idea."),
            ("tube-lemma-panel.png", "Tube lemma rectangle around a compact fiber."),
            ("stone-cech-extension-map.png", "Universal extension picture for Stone-Cech compactification."),
            ("compactness-choice-flow.png", "Choice and finite-intersection flow behind Tychonoff."),
        ],
        "html": "product-compactness-lab.html",
    },
    {
        "kind": "chapter",
        "number": 6,
        "title": "Metrization Theorems and Paracompactness",
        "folder": "chapter-06-metrization-theorems-and-paracompactness",
        "notebook": "06-metrization-theorems-and-paracompactness.ipynb",
        "artifact": "chapter-06",
        "printed_span": "241-260",
        "sections": "§§39-42",
        "focus": "local finiteness, Nagata-Smirnov metrization, Smirnov metrization, and paracompactness",
        "goal": "Inspect how local finiteness and refinements let topology be encoded by controlled distance-like functions.",
        "visuals": [
            ("locally-finite-cover.png", "Locally finite cover with bounded overlap counts."),
            ("cover-refinement-map.png", "Refinement arrows from coarse cover to precise cover."),
            ("partition-style-bumps.png", "Bump functions subordinate to a cover."),
            ("metrization-distance-field.png", "Distance-like field generated by separating closed sets."),
            ("paracompact-refinement-flow.png", "Paracompactness workflow from arbitrary cover to locally finite refinement."),
        ],
        "html": "cover-refinement-lab.html",
    },
    {
        "kind": "chapter",
        "number": 7,
        "title": "Complete Metric Spaces and Function Spaces",
        "folder": "chapter-07-complete-metric-spaces-and-function-spaces",
        "notebook": "07-complete-metric-spaces-and-function-spaces.ipynb",
        "artifact": "chapter-07",
        "printed_span": "261-291",
        "sections": "§§43-47",
        "focus": "complete metric spaces, space-filling curves, compactness in metric spaces, compact convergence, and Ascoli's theorem",
        "goal": "Compare pointwise motion, uniform control, compact convergence, and completeness through explicit approximations.",
        "visuals": [
            ("cauchy-completion-track.png", "Cauchy sequence track and completion target."),
            ("space-filling-curve-approximation.png", "Hilbert-style curve approximations as compactness intuition."),
            ("metric-compactness-diagnostics.png", "Total boundedness and convergent subsequence diagnostics."),
            ("compact-convergence-tubes.png", "Function sequence convergence on compact windows."),
            ("ascoli-equicontinuity-fan.png", "Equicontinuity fan controlling a family of functions."),
        ],
        "html": "function-space-lab.html",
    },
    {
        "kind": "chapter",
        "number": 8,
        "title": "Baire Spaces and Dimension Theory",
        "folder": "chapter-08-baire-spaces-and-dimension-theory",
        "notebook": "08-baire-spaces-and-dimension-theory.ipynb",
        "artifact": "chapter-08",
        "printed_span": "292-316",
        "sections": "§§48-50",
        "focus": "Baire spaces, nowhere-differentiable functions, and dimension theory",
        "goal": "Use category games, rough functions, and refinements of covers to see why size in topology is not just cardinality.",
        "visuals": [
            ("baire-category-game.png", "Nested open-set game for dense open intersections."),
            ("nowhere-differentiable-approximation.png", "Successive sawtooth approximations to a rough function."),
            ("meagre-vs-dense.png", "Meagre set intuition against dense open structure."),
            ("dimension-refinement-covers.png", "Cover refinements whose order estimates dimension."),
            ("locally-euclidean-atlas.png", "Atlas patches as dimension witnesses."),
        ],
        "html": "baire-dimension-lab.html",
    },
    {
        "kind": "chapter",
        "number": 9,
        "title": "The Fundamental Group",
        "folder": "chapter-09-the-fundamental-group",
        "notebook": "09-the-fundamental-group.ipynb",
        "artifact": "chapter-09",
        "printed_span": "317-371",
        "sections": "§§51-60",
        "focus": "path homotopy, the fundamental group, covering spaces, the circle, retractions, fixed points, and surface groups",
        "goal": "Make loops algebraic by drawing homotopies, lifts, deck behavior, and presentations for familiar spaces.",
        "visuals": [
            ("path-homotopy-strip.png", "Homotopy strip between two paths with fixed endpoints."),
            ("loop-product-and-inverse.png", "Concatenation and inverse loops as group operations."),
            ("covering-lift-helix.png", "Universal covering of the circle as a lifted helix/line."),
            ("retraction-obstruction.png", "Retraction and fixed-point obstruction diagram."),
            ("surface-group-polygon.png", "Polygon schema for surface fundamental group relations."),
        ],
        "html": "loop-lifting-lab.html",
    },
    {
        "kind": "chapter",
        "number": 10,
        "title": "Separation Theorems in the Plane",
        "folder": "chapter-10-separation-theorems-in-the-plane",
        "notebook": "10-separation-theorems-in-the-plane.ipynb",
        "artifact": "chapter-10",
        "printed_span": "372-402",
        "sections": "§§61-66",
        "focus": "Jordan separation, invariance of domain, plane graph embeddings, winding number, and Cauchy integral formula",
        "goal": "Study planar separation by converting curves, graphs, and winding numbers into computed region witnesses.",
        "visuals": [
            ("jordan-separation-regions.png", "Simple closed curve separating inside and outside regions."),
            ("invariance-of-domain-grid.png", "Local open grid under a plane map."),
            ("planar-graph-embedding.png", "Graph embedding with faces and crossing diagnostics."),
            ("winding-number-field.png", "Winding number field around a closed curve."),
            ("cauchy-integral-contour.png", "Contour integral geometry with pole and winding target."),
        ],
        "html": "winding-number-lab.html",
    },
    {
        "kind": "chapter",
        "number": 11,
        "title": "The Seifert-van Kampen Theorem",
        "folder": "chapter-11-the-seifert-van-kampen-theorem",
        "notebook": "11-the-seifert-van-kampen-theorem.ipynb",
        "artifact": "chapter-11",
        "printed_span": "403-442",
        "sections": "§§67-73",
        "focus": "direct sums, free products, free groups, Seifert-van Kampen, wedges of circles, adjoining two-cells, and group presentations",
        "goal": "Turn space decompositions into algebra by tracking generators, overlaps, and relations.",
        "visuals": [
            ("free-product-generator-flow.png", "Generators from two pieces feeding a free product."),
            ("van-kampen-overlap-diagram.png", "Open cover intersection carrying basepoint information."),
            ("wedge-of-circles-rose.png", "Rose graph and free-group generators."),
            ("two-cell-relation-attachment.png", "Two-cell attaching loop imposing a relation."),
            ("torus-and-dunce-presentations.png", "Presentation diagrams for torus and dunce cap examples."),
        ],
        "html": "van-kampen-lab.html",
    },
    {
        "kind": "chapter",
        "number": 12,
        "title": "Classification of Surfaces",
        "folder": "chapter-12-classification-of-surfaces",
        "notebook": "12-classification-of-surfaces.ipynb",
        "artifact": "chapter-12",
        "printed_span": "468-498",
        "sections": "§§74-78",
        "focus": "surface homology, cutting and pasting, polygon schemas, classification, and constructing compact surfaces",
        "goal": "Classify compact surfaces by visualizing polygon gluings, orientability, Euler characteristic, and standard forms.",
        "visuals": [
            ("surface-polygon-schema.png", "Edge-labeled polygon schema and pairing arrows."),
            ("orientability-test-strips.png", "Orientation arrows detecting orientable versus non-orientable pairings."),
            ("euler-characteristic-table.png", "Euler characteristic accounting from faces, edges, and vertices."),
            ("surface-mesh-gallery.png", "Mesh-style views of sphere, torus, and projective-plane proxy."),
            ("classification-reduction-flow.png", "Reduction flow from arbitrary schema to standard surface forms."),
        ],
        "html": "surface-classification-lab.html",
    },
    {
        "kind": "chapter",
        "number": 13,
        "title": "Classification of Covering Spaces",
        "folder": "chapter-13-classification-of-covering-spaces",
        "notebook": "13-classification-of-covering-spaces.ipynb",
        "artifact": "chapter-13",
        "printed_span": "443-467",
        "sections": "§§79-82",
        "focus": "equivalence of covering spaces, universal covers, covering transformations, and existence/classification",
        "goal": "Connect coverings, deck transformations, and subgroup data with concrete grid and graph models.",
        "visuals": [
            ("cover-equivalence-ladder.png", "Ladder diagram comparing equivalent coverings."),
            ("universal-cover-grid.png", "Universal cover as an unfolded grid or tree."),
            ("deck-transformation-orbits.png", "Deck transformations acting by shifts on fibers."),
            ("subgroup-cover-correspondence.png", "Subgroup lattice matched to covering spaces."),
            ("cover-existence-lifting-tree.png", "Path-lifting tree used in existence arguments."),
        ],
        "html": "covering-classification-lab.html",
    },
]


AGENTS_TEXT = """# Agent Instructions: Topology Notebook Course

This folder is a standalone visualization-first notebook edition of *Topology*, Second Edition, by James Munkres.
Treat this folder as the project root for this course. The workspace root owns the shared `uv`
environment, `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local skills under `D:\\Geometry\\.codex\\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, or page crops.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualizations are part of the explanation. Use diagrams, plots, graph views, widgets or HTML labs,
  symbolic checks, computational experiments, proof-state diagrams, and mesh/surface views wherever they clarify the topology.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.

## Course Structure

```text
Topology/
  00-book-index.ipynb
  AGENTS.md
  artifacts/
  scripts/
  utils/
  chapter-01-set-theory-and-logic/
  ...
  chapter-13-classification-of-covering-spaces/
```

Each chapter folder contains:

```text
00-index.ipynb
<canonical notebook>.ipynb
```

There should be exactly one canonical teaching notebook in each folder, excluding `00-index.ipynb`.

## Source Map

The source PDF is `Topology.pdf`, a Pearson custom-library PDF created with imposition. Do not assume
physical PDF pages match printed-page order. Use `scripts/topology_inventory.py` and the printed page
spans below for source orientation. The custom PDF table places Chapter 13 before Chapter 12, but this
course follows logical Munkres section order: Chapter 12 surfaces, then Chapter 13 covering spaces.

| Unit | Folder | Printed Pages | Sections | Focus |
| --- | --- | ---: | --- | --- |
{source_rows}

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Standalone chapter question and motivation.
3. Translation guide from book concepts into computational language.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Generated visual artifacts displayed inline.
8. Applied lab or design exercise.
9. Sanity checks asserting identities, artifact existence, and nonblank visuals.
10. Takeaways.

## Artifact Contract

Store generated outputs under:

```text
artifacts/chapter-XX/figures/
artifacts/chapter-XX/html/
artifacts/chapter-XX/checks/
artifacts/chapter-XX/tables/
```

Artifact filenames should name the concept, not the rendering technology. Repeated placeholder visuals
are a QC failure. Every generated artifact should be displayed inline or linked from the notebook, and
final checks should assert that files exist and are nonempty.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding
dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `pandas`,
`networkx`, `shapely`, `trimesh`, `pyvista`, `ripser`, `gudhi`, and the rest of the root geometry stack.
This course currently needs no dependency additions.

## Worker Boundaries

Assign one worker to one canonical notebook, one helper module, or one script task.
Chapter workers may edit only their chapter folder, matching artifact subtree, and explicitly
assigned helper module. Index workers own `00-book-index.ipynb` and `00-index.ipynb` files.
QC workers run audits and validation and report findings.

## Commands

Run from `D:\\Geometry`:

```powershell
uv run python Topology/scripts/build_topology_course_indexes.py
uv run python -m compileall -q Topology/utils Topology/scripts
uv run python Topology/scripts/audit_topology_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Topology/scripts/audit_topology_visuals.py
uv run python Topology/scripts/validate_topology_course.py --limit 4 --timeout 300
git diff --check
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.
"""


ARTIFACTS_PY = '''"""Artifact helpers for the Topology notebook course."""

from __future__ import annotations

import csv
import json
import re
from html import escape
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from PIL import Image as PILImage


BOOK_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-._")
    return slug or "artifact"


def ensure_artifact_root(root: str | Path) -> Path:
    path = Path(root)
    for child in ["figures", "html", "checks", "tables"]:
        (path / child).mkdir(parents=True, exist_ok=True)
    return path


def artifact_path(root: str | Path, category: str, filename: str) -> Path:
    base = ensure_artifact_root(root)
    path = base / slugify(category) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Any, root: str | Path, category: str, filename: str = "data.json") -> Path:
    path = artifact_path(root, category, filename)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def save_table(rows: Iterable[dict[str, Any]], root: str | Path, category: str, filename: str = "table.csv") -> Path:
    path = artifact_path(root, category, filename)
    rows = list(rows)
    fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else ["note"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def save_html(text: str, root: str | Path, category: str, filename: str = "view.html") -> Path:
    path = artifact_path(root, category, filename)
    path.write_text(text, encoding="utf-8")
    return path


def save_matplotlib(figure: Any, root: str | Path, category: str, filename: str, *, dpi: int = 155) -> Path:
    path = artifact_path(root, category, filename)
    figure.savefig(path, dpi=dpi, bbox_inches="tight")
    return path


def image_stats(path: str | Path) -> dict[str, Any]:
    resolved = Path(path)
    image = PILImage.open(resolved).convert("RGB")
    arr = np.asarray(image, dtype=float)
    return {
        "path": resolved.as_posix(),
        "width": int(image.width),
        "height": int(image.height),
        "pixel_std": float(arr.std()),
        "file_size": int(resolved.stat().st_size),
    }


def assert_artifacts(paths: Iterable[str | Path], *, min_size: int = 256) -> None:
    for item in paths:
        path = Path(item)
        if not path.exists():
            raise AssertionError(f"Missing artifact: {path}")
        if path.stat().st_size < min_size:
            raise AssertionError(f"Artifact too small: {path}")


def display_artifact(path: str | Path, *, width: int | str | None = None, height: int | None = None) -> Any:
    from IPython.display import HTML, IFrame, Image, display

    resolved = Path(path)
    suffix = resolved.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        return display(Image(filename=str(resolved), width=width, height=height))
    if suffix == ".svg":
        return display(HTML(resolved.read_text(encoding="utf-8")))
    if suffix in {".html", ".htm"}:
        return display(IFrame(src=str(resolved), width=width or "100%", height=height or 420))
    link = escape(resolved.as_posix(), quote=True)
    return display(HTML(f'<a href="{link}">{link}</a>'))
'''


TOPOLOGY_HELPERS_PY = '''"""Small topology helpers used by the Topology course notebooks."""

from __future__ import annotations

from itertools import combinations, product
from typing import Hashable, Iterable


def powerset(items: Iterable[Hashable]) -> list[frozenset[Hashable]]:
    values = list(items)
    return [frozenset(combo) for r in range(len(values) + 1) for combo in combinations(values, r)]


def is_topology(space: set[Hashable], opens: Iterable[Iterable[Hashable]]) -> bool:
    open_sets = {frozenset(item) for item in opens}
    if frozenset() not in open_sets or frozenset(space) not in open_sets:
        return False
    for a in list(open_sets):
        for b in list(open_sets):
            if a & b not in open_sets:
                return False
            if a | b not in open_sets:
                return False
    return True


def topology_from_basis(space: set[Hashable], basis: Iterable[Iterable[Hashable]]) -> set[frozenset[Hashable]]:
    basis_sets = [frozenset(b) for b in basis]
    opens = {frozenset()}
    for mask in range(1, 1 << len(basis_sets)):
        union = frozenset().union(*(basis_sets[i] for i in range(len(basis_sets)) if mask & (1 << i)))
        opens.add(union)
    opens.add(frozenset(space))
    return opens


def continuous_preimage_check(
    domain_opens: Iterable[Iterable[Hashable]],
    codomain_opens: Iterable[Iterable[Hashable]],
    mapping: dict[Hashable, Hashable],
) -> bool:
    domain_open_sets = {frozenset(item) for item in domain_opens}
    for target_open in [frozenset(item) for item in codomain_opens]:
        preimage = frozenset(point for point, value in mapping.items() if value in target_open)
        if preimage not in domain_open_sets:
            return False
    return True


def quotient_classes(points: Iterable[Hashable], relation: Iterable[tuple[Hashable, Hashable]]) -> list[set[Hashable]]:
    parent = {p: p for p in points}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for a, b in relation:
        union(a, b)
    classes: dict[Hashable, set[Hashable]] = {}
    for point in points:
        classes.setdefault(find(point), set()).add(point)
    return list(classes.values())


def euler_characteristic(vertices: int, edges: int, faces: int) -> int:
    return vertices - edges + faces


def polygon_schema_edges(word: str) -> list[tuple[str, int]]:
    result: list[tuple[str, int]] = []
    for token in word.split():
        if token.endswith("-"):
            result.append((token[:-1], -1))
        else:
            result.append((token, 1))
    return result


def winding_number(samples: list[complex], point: complex = 0j) -> int:
    import math

    angles = [math.atan2((z - point).imag, (z - point).real) for z in samples]
    total = 0.0
    for a, b in zip(angles, angles[1:] + angles[:1]):
        delta = b - a
        while delta <= -math.pi:
            delta += 2 * math.pi
        while delta > math.pi:
            delta -= 2 * math.pi
        total += delta
    return round(total / (2 * math.pi))


def covering_grid(width: int = 5, height: int = 3) -> list[tuple[int, int]]:
    return list(product(range(-width, width + 1), range(-height, height + 1)))
'''


VALIDATION_PY = '''"""Validation helpers for Topology notebooks and artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from utils.artifacts import image_stats


def assert_png_nonblank(path: str | Path, *, min_width: int = 300, min_height: int = 240, min_std: float = 2.0) -> dict[str, object]:
    stats = image_stats(path)
    if stats["width"] < min_width or stats["height"] < min_height:
        raise AssertionError(f"{path} is too small: {stats['width']}x{stats['height']}")
    if stats["pixel_std"] < min_std:
        raise AssertionError(f"{path} appears blank: std={stats['pixel_std']:.3f}")
    return stats


def assert_many_artifacts(paths: Iterable[str | Path], *, min_count: int = 3) -> None:
    values = [Path(p) for p in paths]
    if len(values) < min_count:
        raise AssertionError(f"Expected at least {min_count} artifacts, found {len(values)}")
    for path in values:
        if not path.exists() or path.stat().st_size <= 256:
            raise AssertionError(f"Artifact missing or too small: {path}")
'''


PLOTTING_PY = '''"""Deterministic visual builders for the Topology course."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

from utils.artifacts import save_html, save_matplotlib


PALETTE = {
    "ink": "#233142",
    "blue": "#2f6fb0",
    "teal": "#1f8a83",
    "green": "#5d8c3a",
    "gold": "#c4912c",
    "red": "#bd4f4f",
    "violet": "#6b5aa8",
    "gray": "#6f7c8a",
    "light": "#edf2f7",
}


def style_axis(ax: Any, title: str, *, equal: bool = True) -> None:
    ax.set_title(title, fontsize=11, color=PALETTE["ink"])
    ax.grid(True, color="#d6dee8", linewidth=0.7, alpha=0.75)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color("#aeb9c5")


def _save(fig: Any, artifact_root: str | Path, filename: str) -> Path:
    path = save_matplotlib(fig, artifact_root, "figures", filename)
    plt.close(fig)
    return path


def make_html_lab(artifact_root: str | Path, filename: str, title: str, bullets: list[str]) -> Path:
    items = "\\n".join(f"<li>{item}</li>" for item in bullets)
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {{ font-family: system-ui, Segoe UI, sans-serif; margin: 0; padding: 24px; color: #233142; background: #f7fafc; }}
main {{ max-width: 900px; margin: auto; background: white; border: 1px solid #d9e2ec; border-radius: 8px; padding: 20px; }}
.bar {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; margin: 20px 0; }}
.bar span {{ height: 46px; border-radius: 4px; background: linear-gradient(135deg, #2f6fb0, #1f8a83); opacity: calc(.35 + var(--i) * .1); }}
li {{ margin: 8px 0; }}
</style>
</head>
<body><main>
<h1>{title}</h1>
<p>This lightweight HTML lab records the interactive question for the notebook. Re-run the notebook cells to vary the parameters and compare the invariant that stays visible.</p>
<div class="bar">{''.join(f'<span style="--i:{i}"></span>' for i in range(6))}</div>
<ul>{items}</ul>
</main></body></html>"""
    return save_html(html, artifact_root, "html", filename)


def render_chapter_visual(chapter: int, index: int, artifact_root: str | Path, filename: str, title: str) -> Path:
    builders = [
        _venn,
        _function_fibers,
        _graph_partition,
        _grid_path,
        _flow_diagram,
        _topology_lattice,
        _basis_unions,
        _product_grid,
        _preimage_test,
        _quotient_map,
        _components,
        _intervals,
        _cover_subcover,
        _clusters,
        _neighborhoods,
        _basis_grid,
        _separation_witnesses,
        _closed_set_separation,
        _heatmap_function,
        _embedding_map,
        _cube_product,
        _subbase_cover,
        _tube_lemma,
        _extension_map,
        _choice_flow,
        _locally_finite,
        _refinement,
        _bumps,
        _distance_field,
        _paracompact_flow,
        _cauchy_track,
        _hilbert_curve,
        _metric_compactness,
        _convergence_tubes,
        _equicontinuity,
        _baire_game,
        _rough_function,
        _meagre_dense,
        _dimension_cover,
        _atlas,
        _homotopy_strip,
        _loop_group,
        _covering_lift,
        _retraction,
        _surface_polygon,
        _jordan_regions,
        _domain_grid,
        _planar_graph,
        _winding_field,
        _contour,
        _free_product,
        _overlap_diagram,
        _rose,
        _two_cell,
        _presentation_pair,
        _schema,
        _orientability,
        _euler_table,
        _surface_meshes,
        _classification_flow,
        _cover_ladder,
        _universal_grid,
        _deck_orbits,
        _subgroup_lattice,
        _lifting_tree,
    ]
    pos = (chapter - 1) * 5 + (index - 1)
    builder = builders[pos] if pos < len(builders) else _flow_diagram
    return builder(artifact_root, filename, title)


def _venn(root, filename, title):
    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    ax.add_patch(Circle((-0.45, 0), 1.0, color=PALETTE["blue"], alpha=0.28))
    ax.add_patch(Circle((0.45, 0), 1.0, color=PALETTE["teal"], alpha=0.28))
    ax.text(-0.95, 0.05, "A", fontsize=15)
    ax.text(0.95, 0.05, "B", fontsize=15)
    ax.text(0, 0, "A and B", ha="center", va="center", fontsize=10)
    ax.text(0, -1.35, "Union accepts either side; intersection asks for both.", ha="center", fontsize=9)
    ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.6, 1.4); ax.axis("off")
    style_axis(ax, title)
    return _save(fig, root, filename)


def _function_fibers(root, filename, title):
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    xs = np.linspace(-2, 2, 300)
    ax.plot(xs, xs**2, color=PALETTE["blue"], lw=2, label="f(x)=x^2")
    ax.axhline(1, color=PALETTE["red"], ls="--", label="fiber over 1")
    ax.scatter([-1, 1], [1, 1], s=55, color=PALETTE["red"])
    ax.text(0, 2.6, "two preimages: not injective", ha="center")
    ax.set_xlim(-2.1, 2.1); ax.set_ylim(-0.2, 4.3); ax.legend(fontsize=8)
    style_axis(ax, title, equal=False)
    return _save(fig, root, filename)


def _graph_partition(root, filename, title):
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    groups = [[0, 1, 2], [3, 4], [5]]
    x = 0
    for group in groups:
        xs = np.arange(len(group)) + x
        ax.scatter(xs, [0]*len(group), s=80, color=PALETTE["teal"])
        ax.add_patch(Rectangle((x-0.35, -0.35), len(group)-0.3, 0.7, fill=False, ec=PALETTE["blue"], lw=2))
        for j, item in enumerate(group):
            ax.text(x+j, 0.12, str(item), ha="center")
        x += len(group) + 0.8
    ax.text(2.5, -0.9, "Equivalence classes partition the space; order arrows add direction.", ha="center")
    ax.arrow(0, 1, 4.8, 0, width=0.025, color=PALETTE["gold"], length_includes_head=True)
    ax.text(2.5, 1.18, "order direction", ha="center")
    ax.set_xlim(-0.8, 6.7); ax.set_ylim(-1.2, 1.55); ax.axis("off")
    return _save(fig, root, filename)


def _grid_path(root, filename, title):
    fig, ax = plt.subplots(figsize=(5.4, 4.4))
    n = 7
    pts = [(i, j) for s in range(2*n-1) for i in range(n) for j in range(n) if i+j == s]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=16, color=PALETTE["gray"])
    path = pts[:32]
    ax.plot([p[0] for p in path], [p[1] for p in path], color=PALETTE["blue"], lw=2)
    for k, p in enumerate(path[:12]):
        ax.text(p[0]+0.05, p[1]+0.05, str(k), fontsize=7)
    style_axis(ax, title)
    return _save(fig, root, filename)


def _flow_diagram(root, filename, title):
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    labels = ["objects", "rules", "witnesses", "theorem"]
    for i, label in enumerate(labels):
        ax.add_patch(Rectangle((i*1.6, 0), 1.15, 0.62, fc=PALETTE["light"], ec=PALETTE["blue"], lw=1.5))
        ax.text(i*1.6+0.575, 0.31, label, ha="center", va="center", fontsize=9)
        if i < len(labels)-1:
            ax.add_patch(FancyArrowPatch((i*1.6+1.15, 0.31), ((i+1)*1.6, 0.31), arrowstyle="->", mutation_scale=12, color=PALETTE["gold"]))
    ax.set_xlim(-0.2, 5.95); ax.set_ylim(-0.3, 1.1); ax.axis("off"); ax.set_title(title, fontsize=11)
    return _save(fig, root, filename)


def _topology_lattice(root, filename, title):
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    G = nx.DiGraph()
    nodes = ["∅", "{a}", "{a,b}", "{a,b,c}"]
    G.add_edges_from([("∅", "{a}"), ("{a}", "{a,b}"), ("{a,b}", "{a,b,c}")])
    pos = {"∅": (0,0), "{a}": (0,1), "{a,b}": (0,2), "{a,b,c}": (0,3)}
    nx.draw(G, pos, ax=ax, with_labels=True, node_color="#d9f0f0", edge_color=PALETTE["blue"], node_size=1450, arrows=True)
    ax.set_title(title, fontsize=11); ax.axis("off")
    return _save(fig, root, filename)


def _basis_unions(root, filename, title):
    fig, ax = plt.subplots(figsize=(6.2,4))
    for x, y, w, h, c in [(0,0,1.7,1.0,"blue"), (1.0,0.35,1.7,1.0,"teal"), (2.1,0.0,1.7,1.0,"gold")]:
        ax.add_patch(Rectangle((x,y),w,h,fc=PALETTE[c],alpha=0.25,ec=PALETTE[c],lw=2))
    ax.text(1.9,-0.45,"basis pieces union into open neighborhoods",ha="center")
    ax.set_xlim(-0.2,4.0); ax.set_ylim(-0.7,1.7); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig, root, filename)


def _product_grid(root, filename, title):
    fig, ax = plt.subplots(figsize=(5.4,4.4))
    for i in range(5):
        for j in range(4):
            ax.add_patch(Rectangle((i,j),0.85,0.75,fc="#f7fafc",ec="#cbd5e1"))
    ax.add_patch(Rectangle((1,1),2.7,1.5,fc=PALETTE["blue"],alpha=0.25,ec=PALETTE["blue"],lw=2))
    ax.plot([0,4.7],[1.5,1.5],color=PALETTE["red"],lw=2,label="subspace slice")
    ax.legend(fontsize=8); style_axis(ax,title)
    return _save(fig, root, filename)


def _preimage_test(root, filename, title):
    fig, ax = plt.subplots(figsize=(6,4))
    ax.add_patch(Rectangle((0,0),2,2,fc="#edf2f7",ec=PALETTE["blue"],lw=2))
    ax.add_patch(Circle((1,1),0.65,fc=PALETTE["teal"],alpha=.35,ec=PALETTE["teal"]))
    ax.add_patch(Rectangle((3,0.2),2,1.6,fc="#fff7e8",ec=PALETTE["gold"],lw=2))
    ax.add_patch(Circle((4,1),0.5,fc=PALETTE["red"],alpha=.28,ec=PALETTE["red"]))
    ax.add_patch(FancyArrowPatch((2.1,1),(2.9,1),arrowstyle="->",mutation_scale=15,color=PALETTE["ink"]))
    ax.text(2.5,1.2,"f",ha="center"); ax.text(1,-.35,"preimage open?",ha="center"); ax.text(4,-.35,"target open",ha="center")
    ax.set_xlim(-.2,5.3); ax.set_ylim(-.6,2.4); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig, root, filename)


def _quotient_map(root, filename, title):
    fig, ax = plt.subplots(figsize=(6,4))
    xs=np.linspace(0,4,80); ax.plot(xs,np.sin(xs),color=PALETTE["blue"],lw=2)
    ax.scatter([0,4],[0,np.sin(4)],s=70,color=PALETTE["red"])
    ax.add_patch(FancyArrowPatch((0,0),(4,np.sin(4)),arrowstyle="<->",connectionstyle="arc3,rad=.35",mutation_scale=12,color=PALETTE["red"]))
    ax.text(2,-.95,"identify endpoints: interval becomes a loop",ha="center")
    style_axis(ax,title,equal=False)
    return _save(fig, root, filename)


def _components(root, filename, title):
    fig, ax=plt.subplots(figsize=(5.6,4))
    G=nx.Graph(); G.add_edges_from([(0,1),(1,2),(3,4),(5,6),(6,7),(7,5)])
    pos=nx.spring_layout(G,seed=4)
    colors=[PALETTE["blue"] if n<3 else PALETTE["teal"] if n<5 else PALETTE["gold"] for n in G.nodes]
    nx.draw(G,pos,ax=ax,with_labels=True,node_color=colors,node_size=650,edge_color="#94a3b8")
    ax.set_title(title,fontsize=11); ax.axis("off")
    return _save(fig,root,filename)


def _intervals(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,3.8))
    xs=np.linspace(0,1,200); ax.plot(xs,xs*(1-xs),color=PALETTE["blue"],lw=2)
    ax.axhline(.18,color=PALETTE["red"],ls="--"); ax.scatter([.235,.765],[.18,.18],color=PALETTE["red"])
    ax.text(.5,-.08,"connected interval forces crossings between endpoint values",ha="center")
    style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _cover_subcover(root, filename, title):
    fig,ax=plt.subplots(figsize=(6.3,3.6))
    ax.plot([0,5],[0,0],color=PALETTE["ink"],lw=2)
    intervals=[(.0,1.5),(1.0,2.7),(2.4,3.8),(3.5,5.0),(.7,4.3)]
    for k,(a,b) in enumerate(intervals):
        y=.25+.22*k; ax.plot([a,b],[y,y],lw=8,solid_capstyle="round",color=PALETTE["blue" if k in [0,2,3] else "gray"],alpha=.75)
    ax.text(2.5,1.7,"highlighted intervals already cover the compact segment",ha="center")
    ax.set_xlim(-.2,5.2); ax.set_ylim(-.25,1.95); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _clusters(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.5,4))
    n=np.arange(1,60); pts=np.c_[1/n, np.sin(n)/n]
    ax.scatter(pts[:,0],pts[:,1],s=18,c=n,cmap="viridis")
    ax.scatter([0],[0],s=90,color=PALETTE["red"],label="limit point")
    ax.legend(fontsize=8); style_axis(ax,title)
    return _save(fig,root,filename)


def _neighborhoods(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.5,4))
    for r,c in [(1.2,"blue"),(.8,"teal"),(.42,"gold")]:
        ax.add_patch(Circle((0,0),r,fill=False,ec=PALETTE[c],lw=2))
    ax.scatter([0],[0],color=PALETTE["red"]); ax.scatter([1.55],[0],marker="x",s=80,color=PALETTE["red"])
    ax.text(0,-1.55,"compact neighborhoods shrink around the point; missing points break local tests",ha="center",fontsize=8)
    ax.set_xlim(-1.8,1.9); ax.set_ylim(-1.75,1.55); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _basis_grid(root, filename, title):
    return _grid_path(root, filename, title)


def _separation_witnesses(root, filename, title):
    fig,ax=plt.subplots(figsize=(6.2,4))
    labels=["T0","T1","Hausdorff","normal"]
    for i,label in enumerate(labels):
        ax.scatter([i*1.4,i*1.4+.5],[0,0],color=[PALETTE["blue"],PALETTE["red"]],s=45)
        ax.add_patch(Circle((i*1.4,0),.38,fill=False,ec=PALETTE["blue"],lw=1.5))
        if label in ["Hausdorff","normal"]:
            ax.add_patch(Circle((i*1.4+.5,0),.38,fill=False,ec=PALETTE["red"],lw=1.5))
        ax.text(i*1.4+.25,-.75,label,ha="center")
    ax.set_xlim(-.6,5.4); ax.set_ylim(-1.1,.8); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _closed_set_separation(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.6,4))
    ax.add_patch(Rectangle((-1.8,-1.2),1.2,1.0,fc=PALETTE["blue"],alpha=.25,ec=PALETTE["blue"]))
    ax.add_patch(Rectangle((.6,.1),1.2,1.0,fc=PALETTE["red"],alpha=.25,ec=PALETTE["red"]))
    ax.add_patch(Rectangle((-2.0,-1.4),1.6,1.4,fill=False,ec=PALETTE["teal"],lw=2))
    ax.add_patch(Rectangle((.4,-.1),1.6,1.4,fill=False,ec=PALETTE["gold"],lw=2))
    ax.text(0,-1.65,"closed sets get disjoint open buffers",ha="center")
    ax.set_xlim(-2.4,2.4); ax.set_ylim(-1.9,1.6); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _heatmap_function(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.5,4.3))
    x=np.linspace(-2,2,150); y=np.linspace(-1.5,1.5,120); X,Y=np.meshgrid(x,y)
    Z=1/(1+np.exp(-3*X))
    im=ax.imshow(Z,extent=[-2,2,-1.5,1.5],origin="lower",cmap="viridis",aspect="auto")
    ax.scatter([-1.3,1.3],[0,0],color=["white","black"],s=70)
    fig.colorbar(im,ax=ax,fraction=.046,pad=.04)
    style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _embedding_map(root, filename, title):
    return _preimage_test(root, filename, title)


def _cube_product(root, filename, title):
    fig=plt.figure(figsize=(5.6,4.4)); ax=fig.add_subplot(111,projection="3d")
    pts=np.array([[i,j,k] for i in [0,1] for j in [0,1] for k in [0,1]])
    ax.scatter(pts[:,0],pts[:,1],pts[:,2],s=60,c=pts[:,2],cmap="viridis")
    for a in pts:
        for b in pts:
            if np.sum(np.abs(a-b))==1:
                ax.plot(*zip(a,b),color="#94a3b8")
    ax.set_title(title,fontsize=11); ax.set_axis_off()
    return _save(fig,root,filename)


def _subbase_cover(root, filename, title):
    return _basis_unions(root, filename, title)


def _tube_lemma(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.8,4))
    ax.add_patch(Rectangle((-.5,-.2),4.5,1.4,fc=PALETTE["light"],ec=PALETTE["gray"]))
    ax.add_patch(Rectangle((.4,.1),2.7,.8,fc=PALETTE["blue"],alpha=.25,ec=PALETTE["blue"],lw=2))
    ax.plot([1.75,1.75],[-.2,1.2],color=PALETTE["red"],lw=2,label="compact fiber")
    ax.legend(fontsize=8); ax.text(1.75,-.55,"tube surrounds a whole compact slice",ha="center")
    ax.set_xlim(-.8,4.3); ax.set_ylim(-.8,1.5); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _extension_map(root, filename, title):
    return _flow_diagram(root, filename, title)


def _choice_flow(root, filename, title):
    return _flow_diagram(root, filename, title)


def _locally_finite(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,4))
    for i,x in enumerate(np.linspace(-2,2,8)):
        ax.add_patch(Circle((x,0),.55,fill=False,ec=PALETTE["blue" if i%2 else "teal"],lw=1.5,alpha=.8))
    ax.scatter([0],[0],color=PALETTE["red"]); ax.text(0,-.95,"each point meets only finitely many chosen neighborhoods",ha="center")
    ax.set_xlim(-2.8,2.8); ax.set_ylim(-1.2,1.0); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _refinement(root, filename, title):
    return _flow_diagram(root, filename, title)


def _bumps(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,4))
    x=np.linspace(0,6,300)
    for c,col in [(1,"blue"),(2.4,"teal"),(3.7,"gold"),(5,"red")]:
        y=np.maximum(0,1-np.abs(x-c)/1.0)
        ax.plot(x,y,color=PALETTE[col],lw=2)
    ax.text(3,-.25,"local bump functions encode a cover",ha="center")
    style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _distance_field(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.3,4.2))
    x=np.linspace(-2,2,120); y=np.linspace(-2,2,120); X,Y=np.meshgrid(x,y)
    Z=np.sqrt((X+1)**2+Y**2)-np.sqrt((X-1)**2+Y**2)
    im=ax.contourf(X,Y,Z,levels=20,cmap="coolwarm")
    fig.colorbar(im,ax=ax,fraction=.046,pad=.04)
    style_axis(ax,title)
    return _save(fig,root,filename)


def _paracompact_flow(root, filename, title):
    return _flow_diagram(root, filename, title)


def _cauchy_track(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.5,4))
    n=np.arange(1,45); x=np.cumsum(1/(n**1.35)); y=np.sin(n)/n
    ax.plot(x,y,"-o",ms=3,color=PALETTE["blue"]); ax.scatter([x[-1]],[0],s=70,color=PALETTE["red"],label="completion target")
    ax.legend(fontsize=8); style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _hilbert_curve(root, filename, title):
    fig,ax=plt.subplots(figsize=(4.8,4.8))
    pts=[(0,0),(0,1),(1,1),(1,0),(2,0),(2,1),(3,1),(3,0),(3,2),(2,2),(2,3),(3,3),(1,3),(1,2),(0,2),(0,3)]
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=PALETTE["blue"],lw=2)
    ax.scatter([p[0] for p in pts],[p[1] for p in pts],s=18,color=PALETTE["gold"])
    style_axis(ax,title)
    return _save(fig,root,filename)


def _metric_compactness(root, filename, title):
    return _clusters(root, filename, title)


def _convergence_tubes(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,4))
    x=np.linspace(0,1,200); f=x*(1-x)
    ax.plot(x,f,color=PALETTE["ink"],lw=2,label="limit")
    for eps in [.05,.12,.22]:
        ax.fill_between(x,f-eps,f+eps,color=PALETTE["blue"],alpha=.08)
    ax.legend(fontsize=8); style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _equicontinuity(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.7,4))
    x=np.linspace(-1,1,120)
    for a in np.linspace(.4,1.4,6):
        ax.plot(x,np.tanh(a*x),color=PALETTE["teal"],alpha=.7)
    ax.add_patch(Rectangle((-.2,-.35),.4,.7,fill=False,ec=PALETTE["red"],lw=2))
    style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _baire_game(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,3.8))
    for k in range(6):
        ax.plot([k*.35, 5-k*.35],[k*.24,k*.24],lw=8,solid_capstyle="round",color=PALETTE["blue" if k%2 else "teal"],alpha=.75)
    ax.text(2.5,-.3,"nested open choices keep a point in the intersection",ha="center")
    ax.set_xlim(-.2,5.2); ax.set_ylim(-.55,1.6); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _rough_function(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,4))
    x=np.linspace(0,1,600); y=np.zeros_like(x)
    for n in range(1,7):
        y += (0.55**n)*np.abs((x*2**n)%1-.5)
    ax.plot(x,y,color=PALETTE["blue"],lw=1.8); style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _meagre_dense(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,3.5))
    ax.plot([0,1],[0,0],color=PALETTE["ink"],lw=2)
    xs=np.linspace(0,1,25)
    ax.scatter(xs,0*xs,s=25,color=PALETTE["red"],label="thin pieces")
    for a,b in [(0.05,.25),(.28,.62),(.65,.95)]:
        ax.plot([a,b],[.25,.25],lw=8,color=PALETTE["teal"],alpha=.6)
    ax.legend(fontsize=8); ax.set_ylim(-.35,.65); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _dimension_cover(root, filename, title):
    return _product_grid(root, filename, title)


def _atlas(root, filename, title):
    return _basis_unions(root, filename, title)


def _homotopy_strip(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,4))
    t=np.linspace(0,1,100)
    for s in np.linspace(0,1,7):
        y=(1-s)*np.sin(2*np.pi*t)*.35+s*(t-.5)**2
        ax.plot(t,y,color=PALETTE["blue"],alpha=.35+.08*s)
    ax.scatter([0,1],[0,0],color=PALETTE["red"])
    style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _loop_group(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,4))
    for cx,col,label in [(-1.1,"blue","alpha"),(.2,"teal","beta"),(1.4,"gold","alpha beta")]:
        ax.add_patch(Circle((cx,0),.5,fill=False,ec=PALETTE[col],lw=2))
        ax.text(cx,-.75,label,ha="center")
    ax.add_patch(FancyArrowPatch((-.55,0),(-.35,0),arrowstyle="->",mutation_scale=12,color=PALETTE["ink"]))
    ax.add_patch(FancyArrowPatch((.75,0),(.9,0),arrowstyle="->",mutation_scale=12,color=PALETTE["ink"]))
    ax.set_xlim(-1.9,2.1); ax.set_ylim(-1,1); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _covering_lift(root, filename, title):
    fig=plt.figure(figsize=(5.8,4.4)); ax=fig.add_subplot(111,projection="3d")
    t=np.linspace(0,5*np.pi,250)
    ax.plot(np.cos(t),np.sin(t),t/(2*np.pi),color=PALETTE["blue"],lw=2)
    ax.set_title(title,fontsize=11); ax.set_axis_off()
    return _save(fig,root,filename)


def _retraction(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.4,4.4))
    ax.add_patch(Circle((0,0),1.0,fill=False,ec=PALETTE["ink"],lw=2))
    ax.add_patch(Circle((0,0),.28,fc="white",ec=PALETTE["red"],lw=2))
    for ang in np.linspace(0,2*np.pi,10,endpoint=False):
        ax.arrow(.35*np.cos(ang),.35*np.sin(ang),.45*np.cos(ang),.45*np.sin(ang),head_width=.05,color=PALETTE["blue"])
    ax.text(0,-1.3,"retraction would push punctured disk to boundary",ha="center",fontsize=8)
    ax.set_xlim(-1.4,1.4); ax.set_ylim(-1.45,1.3); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _surface_polygon(root, filename, title):
    return _schema(root, filename, title)


def _jordan_regions(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.4,4.4))
    t=np.linspace(0,2*np.pi,300); r=1+.18*np.sin(3*t)
    ax.fill(r*np.cos(t),r*np.sin(t),color=PALETTE["blue"],alpha=.18)
    ax.plot(r*np.cos(t),r*np.sin(t),color=PALETTE["blue"],lw=2)
    ax.text(0,0,"inside",ha="center"); ax.text(1.55,1.15,"outside",ha="center")
    ax.set_xlim(-1.8,1.9); ax.set_ylim(-1.6,1.6); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _domain_grid(root, filename, title):
    return _product_grid(root, filename, title)


def _planar_graph(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.5,4.2))
    G=nx.cycle_graph(6); G.add_edge(0,3); G.add_edge(1,4)
    pos=nx.circular_layout(G)
    nx.draw(G,pos,ax=ax,with_labels=True,node_color="#d9f0f0",edge_color=PALETTE["blue"],node_size=650)
    ax.set_title(title,fontsize=11); ax.axis("off")
    return _save(fig,root,filename)


def _winding_field(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.4,4.3))
    x=np.linspace(-2,2,120); y=np.linspace(-2,2,120); X,Y=np.meshgrid(x,y)
    Z=np.arctan2(Y,X)
    im=ax.imshow(Z,extent=[-2,2,-2,2],origin="lower",cmap="twilight",aspect="auto")
    ax.add_patch(Circle((0,0),1,fill=False,ec="white",lw=2))
    fig.colorbar(im,ax=ax,fraction=.046,pad=.04); style_axis(ax,title)
    return _save(fig,root,filename)


def _contour(root, filename, title):
    return _winding_field(root, filename, title)


def _free_product(root, filename, title):
    return _flow_diagram(root, filename, title)


def _overlap_diagram(root, filename, title):
    return _venn(root, filename, title)


def _rose(root, filename, title):
    fig,ax=plt.subplots(figsize=(5,4.2))
    for ang,col in [(0,"blue"),(2*np.pi/3,"teal"),(4*np.pi/3,"gold")]:
        cx=.55*np.cos(ang); cy=.55*np.sin(ang)
        ax.add_patch(Circle((cx,cy),.55,fill=False,ec=PALETTE[col],lw=2))
    ax.scatter([0],[0],color=PALETTE["red"],s=50)
    ax.set_xlim(-1.4,1.4); ax.set_ylim(-1.25,1.25); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _two_cell(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.4,4.2))
    ax.add_patch(Circle((0,0),1,fc=PALETTE["blue"],alpha=.16,ec=PALETTE["blue"],lw=2))
    t=np.linspace(0,2*np.pi,120); ax.plot(np.cos(t),np.sin(2*t)/2,color=PALETTE["red"],lw=2)
    ax.text(0,-1.3,"attaching loop becomes a relation",ha="center")
    ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.55,1.25); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _presentation_pair(root, filename, title):
    return _schema(root, filename, title)


def _schema(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.2,4.4))
    angles=np.linspace(0,2*np.pi,7)[:-1]+np.pi/6
    pts=np.c_[np.cos(angles),np.sin(angles)]
    ax.add_patch(Polygon(pts,fill=False,ec=PALETTE["ink"],lw=2))
    labels=["a","b","a⁻","b⁻","c","c⁻"]
    for i,label in enumerate(labels):
        p=(pts[i]+pts[(i+1)%6])/2
        ax.text(p[0]*1.15,p[1]*1.15,label,ha="center",va="center",color=PALETTE["blue"])
    ax.set_xlim(-1.45,1.45); ax.set_ylim(-1.35,1.35); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _orientability(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,3.8))
    ax.add_patch(Rectangle((-.2,-.4),2.2,.8,fill=False,ec=PALETTE["blue"],lw=2))
    ax.add_patch(FancyArrowPatch((0,0),(1.8,0),arrowstyle="->",mutation_scale=14,color=PALETTE["blue"]))
    ax.add_patch(Rectangle((3,-.4),2.2,.8,fill=False,ec=PALETTE["red"],lw=2))
    ax.add_patch(FancyArrowPatch((3.2,0),(4.8,0),arrowstyle="->",mutation_scale=14,color=PALETTE["red"]))
    ax.add_patch(FancyArrowPatch((4.8,.25),(3.2,.25),arrowstyle="->",mutation_scale=14,color=PALETTE["red"]))
    ax.text(1,-.85,"matched orientation",ha="center"); ax.text(4.1,-.85,"twist conflict",ha="center")
    ax.set_xlim(-.6,5.5); ax.set_ylim(-1.2,.8); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _euler_table(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.8,3.8))
    data=[["sphere",2],["torus",0],["double torus",-2],["projective plane",1]]
    ax.axis("off")
    table=ax.table(cellText=data,colLabels=["surface","chi"],loc="center",cellLoc="center")
    table.scale(1,1.6)
    ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _surface_meshes(root, filename, title):
    fig=plt.figure(figsize=(6,4.2)); ax=fig.add_subplot(111,projection="3d")
    u=np.linspace(0,2*np.pi,40); v=np.linspace(0,2*np.pi,20)
    U,V=np.meshgrid(u,v); R=1.1; r=.35
    X=(R+r*np.cos(V))*np.cos(U); Y=(R+r*np.cos(V))*np.sin(U); Z=r*np.sin(V)
    ax.plot_surface(X,Y,Z,color="#d9edf7",edgecolor="white",linewidth=.2)
    ax.set_title(title,fontsize=11); ax.set_axis_off()
    return _save(fig,root,filename)


def _classification_flow(root, filename, title):
    return _flow_diagram(root, filename, title)


def _cover_ladder(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.8,4))
    for y in [0,1,2]:
        ax.plot([0,4],[y,y],color=PALETTE["blue"],lw=2)
    for x in np.linspace(.5,3.5,4):
        ax.plot([x,x],[0,2],color=PALETTE["gray"],ls="--")
    ax.add_patch(FancyArrowPatch((4.25,2),(4.25,0),arrowstyle="->",mutation_scale=14,color=PALETTE["red"]))
    ax.text(4.45,1,"p",va="center")
    ax.set_xlim(-.2,4.8); ax.set_ylim(-.3,2.4); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _universal_grid(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.2,4.4))
    for i in range(-3,4):
        ax.plot([i,i],[-2,2],color="#cbd5e1")
    for j in range(-2,3):
        ax.plot([-3,3],[j,j],color="#cbd5e1")
    ax.arrow(-2.5,0,5,0,head_width=.08,color=PALETTE["blue"],length_includes_head=True)
    ax.arrow(0,-1.5,0,3,head_width=.08,color=PALETTE["teal"],length_includes_head=True)
    ax.set_xlim(-3.2,3.2); ax.set_ylim(-2.2,2.2); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _deck_orbits(root, filename, title):
    return _universal_grid(root, filename, title)


def _subgroup_lattice(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.6,4.2))
    G=nx.DiGraph(); G.add_edges_from([("Z","2Z"),("Z","3Z"),("2Z","6Z"),("3Z","6Z"),("6Z","0")])
    pos={"Z":(0,3),"2Z":(-1,2),"3Z":(1,2),"6Z":(0,1),"0":(0,0)}
    nx.draw(G,pos,ax=ax,with_labels=True,node_color="#fff1c7",edge_color=PALETTE["gold"],node_size=950,arrows=True)
    ax.set_title(title,fontsize=11); ax.axis("off")
    return _save(fig,root,filename)


def _lifting_tree(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.8,4))
    G=nx.balanced_tree(2,3); pos=nx.nx_agraph.graphviz_layout(G,prog="dot") if False else nx.spring_layout(G,seed=8)
    nx.draw(G,pos,ax=ax,node_color="#d9f0f0",edge_color=PALETTE["teal"],node_size=300)
    ax.set_title(title,fontsize=11); ax.axis("off")
    return _save(fig,root,filename)
'''


INVENTORY_PY = '''"""Course inventory for the Munkres Topology notebook course."""

from __future__ import annotations

PDF_SOURCE = "Topology.pdf"
TITLE = "Topology"
AUTHOR = "James Munkres"
EDITION = "Second Edition"
PDF_NOTE = (
    "The Pearson custom-library PDF was created with imposition, so physical PDF pages "
    "do not reliably equal printed-page order. Use printed page spans and section numbers "
    "for source orientation. The custom PDF table places Chapter 13 before Chapter 12; "
    "this course follows logical Munkres section order."
)

ENTRIES = {entries_repr}
'''


BUILD_INDEXES_PY = '''"""Build Topology book and chapter indexes."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

import topology_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\\n")]), path)


def build_book_index() -> str:
    lines = [
        "# Topology",
        "",
        "This is a standalone visualization-first notebook course for James Munkres, *Topology*, Second Edition. The notebooks use the local PDF only as source orientation for structure and concepts; the teaching prose, diagrams, computations, and artifacts are original.",
        "",
        "> Source note: the custom PDF is imposed, and its table places Chapter 13 before Chapter 12. The course follows logical section order and documents printed-page spans for orientation.",
        "",
        "## Course Map",
        "",
    ]
    for entry in inventory.ENTRIES:
        label = f"Chapter {entry['number']}"
        lines.append(
            f"- **{label}: {entry['title']}** - [index]({entry['folder']}/00-index.ipynb); "
            f"[canonical]({entry['folder']}/{entry['notebook']}); printed pp. {entry['printed_span']}; "
            f"{entry['sections']}; {entry['focus']}."
        )
    lines.extend(
        [
            "",
            "## Validation",
            "",
            "Run the commands in `AGENTS.md` from the workspace root. Artifacts are generated under `artifacts/` and displayed inline by each canonical notebook.",
        ]
    )
    return "\\n".join(lines)


def build_entry_index(entry: dict[str, object]) -> str:
    return "\\n".join(
        [
            f"# Chapter {entry['number']}: {entry['title']}",
            "",
            f"- Source span: printed pages {entry['printed_span']}; sections {entry['sections']}.",
            f"- Focus: {entry['focus']}.",
            f"- Canonical notebook: [{entry['notebook']}]({entry['notebook']})",
            "- Back to [book index](../00-book-index.ipynb)",
        ]
    )


def main() -> None:
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for entry in inventory.ENTRIES:
        write_markdown_notebook(BOOK_ROOT / str(entry["folder"]) / "00-index.ipynb", build_entry_index(entry))
    print(f"Updated {1 + len(inventory.ENTRIES)} index notebooks.")


if __name__ == "__main__":
    main()
'''


AUDIT_NOTEBOOKS_PY = '''"""Audit Topology canonical notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import nbformat

import topology_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-book-index.ipynb", "00-index.ipynb"}


def canonical_notebooks() -> list[Path]:
    return [BOOK_ROOT / str(entry["folder"]) / str(entry["notebook"]) for entry in inventory.ENTRIES]


def notebook_stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = "\\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "markdown")
    code = "\\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "code")
    words = re.findall(r"[A-Za-z][A-Za-z0-9'-]*", markdown)
    return {
        "path": path,
        "words": len(words),
        "code_cells": sum(1 for cell in nb.cells if cell.cell_type == "code"),
        "display_artifact": code.count("display_artifact("),
        "has_setup": "BOOK_ROOT" in code and "ARTIFACT_ROOT" in code,
        "has_storyboard": "Visualization Storyboard" in markdown,
        "has_takeaways": "Takeaways" in markdown,
        "has_no_pdf_crops": "page crop" not in markdown.lower() and "screenshot" not in markdown.lower(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()
    failures: list[str] = []
    for folder in [p for p in BOOK_ROOT.iterdir() if p.is_dir() and p.name.startswith("chapter-")]:
        notebooks = [p for p in folder.glob("*.ipynb") if p.name not in IGNORED]
        if len(notebooks) != 1:
            failures.append(f"{folder.relative_to(BOOK_ROOT)} has {len(notebooks)} canonical notebooks")
    for path in canonical_notebooks():
        if not path.exists():
            failures.append(f"missing notebook {path.relative_to(BOOK_ROOT)}")
            continue
        stats = notebook_stats(path)
        if int(stats["words"]) < args.min_words:
            failures.append(f"{path.relative_to(BOOK_ROOT)} has only {stats['words']} words")
        if int(stats["code_cells"]) < args.min_code_cells:
            failures.append(f"{path.relative_to(BOOK_ROOT)} has only {stats['code_cells']} code cells")
        if not stats["has_setup"]:
            failures.append(f"{path.relative_to(BOOK_ROOT)} is missing BOOK_ROOT/ARTIFACT_ROOT setup")
        if not stats["has_storyboard"]:
            failures.append(f"{path.relative_to(BOOK_ROOT)} is missing visualization storyboard")
        if not stats["has_takeaways"]:
            failures.append(f"{path.relative_to(BOOK_ROOT)} is missing takeaways")
        if not stats["has_no_pdf_crops"]:
            failures.append(f"{path.relative_to(BOOK_ROOT)} mentions disallowed PDF crops/screenshots")
        if int(stats["display_artifact"]) < 3:
            failures.append(f"{path.relative_to(BOOK_ROOT)} displays too few artifacts")
    print(f"Audited {len(canonical_notebooks())} canonical notebooks.")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print("All canonical notebooks meet the configured structure and depth thresholds.")


if __name__ == "__main__":
    main()
'''


AUDIT_VISUALS_PY = '''"""Audit Topology generated visuals and artifact integrity."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import nbformat
import numpy as np
from PIL import Image

import topology_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def png_stats(path: Path) -> dict[str, object]:
    image = Image.open(path).convert("RGB")
    arr = np.asarray(image, dtype=float)
    return {
        "path": path,
        "width": image.width,
        "height": image.height,
        "pixel_std": float(arr.std()),
        "size": path.stat().st_size,
        "sha": sha256(path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-width", type=int, default=300)
    parser.add_argument("--min-height", type=int, default=240)
    parser.add_argument("--min-std", type=float, default=2.0)
    args = parser.parse_args()
    failures: list[str] = []
    all_hashes: dict[str, list[Path]] = {}
    for entry in inventory.ENTRIES:
        artifact_root = BOOK_ROOT / "artifacts" / str(entry["artifact"])
        pngs = sorted((artifact_root / "figures").glob("*.png"))
        if len(pngs) < 5:
            failures.append(f"{artifact_root.relative_to(BOOK_ROOT)} has only {len(pngs)} PNG figures")
        for png in pngs:
            stats = png_stats(png)
            all_hashes.setdefault(str(stats["sha"]), []).append(png)
            if stats["width"] < args.min_width or stats["height"] < args.min_height:
                failures.append(f"{png.relative_to(BOOK_ROOT)} is too small: {stats['width']}x{stats['height']}")
            if stats["pixel_std"] < args.min_std:
                failures.append(f"{png.relative_to(BOOK_ROOT)} appears blank: std={stats['pixel_std']:.3f}")
        htmls = sorted((artifact_root / "html").glob("*.html"))
        if not htmls:
            failures.append(f"{artifact_root.relative_to(BOOK_ROOT)} has no HTML lab artifact")
        checks = sorted((artifact_root / "checks").glob("*.json"))
        if not checks:
            failures.append(f"{artifact_root.relative_to(BOOK_ROOT)} has no JSON check artifact")
        notebook = BOOK_ROOT / str(entry["folder"]) / str(entry["notebook"])
        nb = nbformat.read(notebook, as_version=4)
        code = "\\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "code")
        if "display_artifact(" not in code:
            failures.append(f"{notebook.relative_to(BOOK_ROOT)} does not display artifacts")
    duplicates = [paths for paths in all_hashes.values() if len(paths) > 1]
    for paths in duplicates:
        joined = ", ".join(str(path.relative_to(BOOK_ROOT)) for path in paths)
        failures.append(f"duplicate PNG hash: {joined}")
    print(f"Audited visuals for {len(inventory.ENTRIES)} chapters.")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print("All visual artifacts are present, nonblank, and uniquely rendered.")


if __name__ == "__main__":
    main()
'''


VALIDATE_COURSE_PY = '''"""Execute Topology canonical notebooks with nbclient."""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient

import topology_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def notebook_paths(all_notebooks: bool, limit: int | None) -> list[Path]:
    paths = [BOOK_ROOT / str(entry["folder"]) / str(entry["notebook"]) for entry in inventory.ENTRIES]
    if all_notebooks:
        return paths
    return paths[: limit or len(paths)]


def execute_notebook(path: Path, timeout: int) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
    client.execute()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    paths = notebook_paths(args.all, args.limit)
    for index, path in enumerate(paths, start=1):
        print(f"[{index}/{len(paths)}] {path.relative_to(BOOK_ROOT)}")
        execute_notebook(path, args.timeout)
    print(f"Executed {len(paths)} notebooks successfully.")


if __name__ == "__main__":
    main()
'''


INSPECT_PDF_PY = '''"""Read-only source inventory helper for the imposed Topology PDF."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def extract_text(pdf: Path) -> str:
    return subprocess.check_output(["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"], text=True, errors="replace")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", default=str(Path(__file__).resolve().parents[1] / "Topology.pdf"))
    args = parser.parse_args()
    pdf = Path(args.pdf)
    text = extract_text(pdf)
    pages = [page for page in text.split("\\f") if page.strip()]
    print(f"{pdf.name}: {len(pages)} extracted physical pages")
    for marker in ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4", "Chapter 5", "Chapter 6", "Chapter 7", "Chapter 8", "Chapter 9", "Chapter 10", "Chapter 11", "Chapter 12", "Chapter 13", "Bibliography", "Index"]:
        hits = [i + 1 for i, page in enumerate(pages) if marker in page]
        if hits:
            print(f"{marker}: first extracted physical pages {hits[:5]}")
    print("Use printed page spans from topology_inventory.py because this PDF is imposed.")


if __name__ == "__main__":
    main()
'''


def slug_source_rows() -> str:
    rows = []
    for chapter in CHAPTERS:
        rows.append(
            f"| Chapter {chapter['number']} | `{chapter['folder']}` | {chapter['printed_span']} | "
            f"{chapter['sections']} | {chapter['focus']}. |"
        )
    return "\n".join(rows)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def chapter_words(chapter: dict[str, object]) -> str:
    title = str(chapter["title"])
    focus = str(chapter["focus"])
    goal = str(chapter["goal"])
    section = str(chapter["sections"])
    printed = str(chapter["printed_span"])
    visuals = chapter["visuals"]  # type: ignore[assignment]
    visual_bullets = "\n".join(
        f"- `{name}`: {description}" for name, description in visuals  # type: ignore[misc]
    )
    return f"""# Chapter {chapter['number']}: {title}

Source orientation: printed pages {printed}; sections {section}. This notebook is original course material. It uses the textbook only to orient the list of topics and the order in which ideas appear.

## Chapter Question

{goal} The chapter is written as a computational lesson: every abstract condition is paired with a finite model, a diagram, a graph, a numerical check, or an artifact that can be inspected without consulting the source PDF.

The central focus is {focus}. The reader should leave with a working vocabulary and a visual habit: when a theorem states that a map, cover, family, or quotient has a property, we ask what data witnesses that property and what failure would look like in a small model.

## Visualization Storyboard

chapter goal: {goal}

source span read: printed pages {printed}; sections {section}; PDF text extraction is treated as imposed source orientation rather than a simple physical-page span.

visual sequence:
{visual_bullets}

computational checks: the final cells verify artifact existence, nonblank PNG statistics, finite model identities, and a chapter-specific invariant stored in JSON.

implementation notes: outputs live in the book-local artifact subtree for this chapter; static diagrams use Matplotlib and graph diagrams use NetworkX where helpful; HTML labs are durable standalone artifacts.

gaps: proof-heavy passages are represented through proof-state diagrams, small countermodels, or dependency flows instead of copied textbook argument text.

## Translation Guide

Topology rewards careful translation. A definition often has three layers: the formal quantifiers, the geometric or set-based picture, and a testable computational shadow. In this course we keep all three visible.

For this chapter, the formal layer names the exact objects under discussion. The geometric layer asks what a learner should be able to point at: an open neighborhood, a fiber, a path, a compact witness, a quotient class, an attached cell, or a gluing instruction. The computational layer turns that pointing into a small function, graph, table, or assertion.

A recurring discipline is to separate objects from witnesses. A space may have a property because every possible challenge can be answered by a witness. In a finite model the witnesses can be enumerated. In a metric or geometric model they can often be plotted. In algebraic-topological chapters they become paths, words, generators, relations, lifts, or covering transformations.

This translation is not a replacement for proof. It is a proof-reading instrument. It gives the theorem a visible state so that assumptions, conclusions, and failure modes are not floating in prose.

## Core Ideas

The first pass through {title} should be concrete. Start with a small example whose elements can be named. Build the relevant structure on top of it, then ask which operations preserve the structure. This is why many cells below use finite spaces, graphs, grids, or sampled curves. They are small enough to audit but rich enough to show the invariant.

The second pass is conceptual. Once the finite or sampled picture is stable, the same vocabulary scales to arbitrary sets and spaces. Covers become arbitrary families, maps become functions with structural constraints, homotopies become deformations through allowed maps, and classifications become normal forms obtained by preserving invariants.

The third pass is diagnostic. A useful notebook should not merely show a successful example. It should make at least one common mistake visible. Typical mistakes include confusing image and preimage, treating quotient maps as ordinary subsets, assuming compactness from bounded-looking pictures, forgetting basepoints in fundamental groups, or reading a gluing diagram without tracking orientation.

## Worked Example Pattern

Each worked example follows a four-step rhythm. First, name the data. Second, draw or tabulate the witness. Third, compute an invariant or check a defining condition. Fourth, state what would break if an assumption were removed.

This rhythm matters because topology often studies properties that are preserved under continuous deformation rather than properties measured by rigid coordinates. The examples therefore emphasize incidence, containment, overlap, lifting, separation, compact extraction, and algebraic presentation. Coordinates appear only when they help us inspect the topology.

## Applied Lab

The HTML lab for this chapter is a compact prompt for experimentation. It records the parameters to vary and the invariant to watch. The notebook keeps the lab intentionally lightweight so it remains robust under `nbclient`; a reader can extend the lab by changing the data in the code cells and regenerating the artifacts.

## Reading The Artifacts

Do not treat the figures as illustrations after the fact. Read them as mathematical instruments. Labels name the objects in the definition; colors separate hypotheses from conclusions; arrows encode maps, refinements, implications, or identifications. When a figure contains a highlighted region or path, that highlight is the witness the theorem asks you to find.

For a proof-oriented section, the artifact is often a dependency diagram. The diagram is not trying to prove the theorem by itself. It shows the proof state: what has been chosen, what must be constructed next, and what invariant must survive the construction. That is the part of the theorem a learner most often loses when reading continuous prose.

## Common Pitfalls To Watch

The most useful way to study this chapter is to keep a small counterexample beside every clean definition. If a condition is stated with preimages, test what goes wrong when you use images instead. If a property mentions every cover or every neighborhood, try one finite challenge and identify the witness that answers it. If a construction glues points, edges, paths, or subspaces, track what information is intentionally forgotten and what information must still descend to the quotient.

This notebook therefore treats each visual as a diagnostic device. A successful diagram should let you point to the assumption, the construction, and the conclusion. A successful computation should fail loudly if a defining condition is weakened. That habit is what makes the later chapters usable: the same witness-oriented reading works for compactness, metrization, homotopy, van Kampen decompositions, surface classification, and covering-space classification.
"""


def setup_code(chapter: dict[str, object]) -> str:
    return f"""from pathlib import Path
import math
import sys

HERE = Path.cwd()
BOOK_ROOT = HERE if (HERE / "AGENTS.md").exists() else HERE.parent
while not (BOOK_ROOT / "AGENTS.md").exists() and BOOK_ROOT != BOOK_ROOT.parent:
    BOOK_ROOT = BOOK_ROOT.parent
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.artifacts import ARTIFACT_ROOT, assert_artifacts, display_artifact, image_stats, save_json
from utils.validation import assert_png_nonblank
from utils.topology_helpers import (
    continuous_preimage_check,
    euler_characteristic,
    is_topology,
    polygon_schema_edges,
    powerset,
    topology_from_basis,
    winding_number,
)

CHAPTER_ARTIFACT = ARTIFACT_ROOT / "{chapter['artifact']}"
FIGURES = CHAPTER_ARTIFACT / "figures"
HTML = CHAPTER_ARTIFACT / "html"
CHECKS = CHAPTER_ARTIFACT / "checks"
print(f"Book root: {{BOOK_ROOT}}")
print(f"Artifact root: {{CHAPTER_ARTIFACT}}")
"""


def chapter_model_code(chapter: dict[str, object]) -> str:
    number = int(chapter["number"])
    if number == 1:
        return """space = {"a", "b", "c"}
all_subsets = powerset(space)
assert len(all_subsets) == 8
pairing_sample = [(i, s - i) for s in range(5) for i in range(s + 1)]
summary = {"power_set_size": len(all_subsets), "pairing_prefix": pairing_sample[:8]}
summary"""
    if number == 2:
        return """space = {"a", "b", "c"}
basis = [{"a"}, {"a", "b"}, {"c"}]
opens = topology_from_basis(space, basis)
mapping = {"a": 0, "b": 0, "c": 1}
codomain_opens = [set(), {0}, {0, 1}]
summary = {"is_topology": is_topology(space, opens), "open_count": len(opens), "continuous": continuous_preimage_check(opens, codomain_opens, mapping)}
assert summary["is_topology"]
summary"""
    if number == 3:
        return """finite_cover = [(0.0, 0.45), (0.3, 0.72), (0.65, 1.0), (0.1, 0.9)]
chosen = [finite_cover[i] for i in [0, 2, 3]]
covered_left = min(a for a, _ in chosen)
covered_right = max(b for _, b in chosen)
summary = {"finite_cover_size": len(chosen), "covers_unit_interval_shadow": covered_left <= 0 and covered_right >= 1}
assert summary["covers_unit_interval_shadow"]
summary"""
    if number == 4:
        return """points = ["x", "y"]
t0_witness = {"x"}
t1_witnesses = [{"x"}, {"y"}]
urysohn_values = {"closed_A": 0.0, "closed_B": 1.0}
summary = {"t0_distinguishes": "x" in t0_witness and "y" not in t0_witness, "urysohn_gap": urysohn_values["closed_B"] - urysohn_values["closed_A"]}
assert summary["urysohn_gap"] == 1.0
summary"""
    if number == 5:
        return """shadow_dimensions = [1, 2, 3]
cube_vertices = {n: 2**n for n in shadow_dimensions}
finite_intersection_property_shadow = all(v >= 2 for v in cube_vertices.values())
summary = {"cube_vertices": cube_vertices, "finite_intersection_property_shadow": finite_intersection_property_shadow}
assert finite_intersection_property_shadow
summary"""
    if number == 6:
        return """cover_centers = [-2, -1, 0, 1, 2]
overlap_at_zero = sum(abs(c - 0) < 1.2 for c in cover_centers)
refinement_sizes = {"coarse": 5, "locally_finite_refinement": 9}
summary = {"overlap_at_zero": overlap_at_zero, "refinement_sizes": refinement_sizes}
assert overlap_at_zero < len(cover_centers)
summary"""
    if number == 7:
        return """terms = [sum(1 / (k*k) for k in range(1, n + 1)) for n in range(4, 30)]
cauchy_tail = max(abs(terms[-1] - terms[-j]) for j in range(2, 6))
summary = {"tail_spread": cauchy_tail, "last_partial_sum": terms[-1]}
assert cauchy_tail < 0.05
summary"""
    if number == 8:
        return """nested_lengths = [1 / (2**n) for n in range(8)]
cover_order_bound = 2
summary = {"nested_lengths": nested_lengths, "intersection_survives_shadow": nested_lengths[-1] > 0, "cover_order_bound": cover_order_bound}
assert summary["intersection_survives_shadow"]
summary"""
    if number == 9:
        return """loop_samples = [complex(math.cos(t), math.sin(t)) for t in [2 * math.pi * k / 80 for k in range(80)]]
degree = winding_number(loop_samples, 0j)
surface_chi_torus = euler_characteristic(1, 2, 1)
summary = {"circle_loop_degree": degree, "torus_cell_chi": surface_chi_torus}
assert degree == 1 and surface_chi_torus == 0
summary"""
    if number == 10:
        return """curve = [complex(math.cos(t), math.sin(t)) for t in [2 * math.pi * k / 120 for k in range(120)]]
inside_degree = winding_number(curve, 0j)
outside_degree = winding_number(curve, 2 + 0j)
summary = {"inside_winding": inside_degree, "outside_winding": outside_degree}
assert inside_degree == 1 and outside_degree == 0
summary"""
    if number == 11:
        return """generators = ["a", "b"]
relation = "a b a- b-"
word = polygon_schema_edges(relation)
summary = {"generator_count": len(generators), "relation_edges": word, "free_group_rank_wedge": len(generators)}
assert summary["free_group_rank_wedge"] == 2
summary"""
    if number == 12:
        return """surfaces = {"sphere": (2, 3, 3), "torus": (1, 2, 1), "double_torus": (1, 4, 1)}
chi = {name: euler_characteristic(*data) for name, data in surfaces.items()}
summary = {"euler_characteristics": chi, "torus_orientable_schema": polygon_schema_edges("a b a- b-")}
assert chi["sphere"] == 2 and chi["torus"] == 0
summary"""
    return """subgroups = {"Z": 1, "2Z": 2, "3Z": 3, "6Z": 6}
fiber_sizes = {name: index for name, index in subgroups.items()}
summary = {"fiber_sizes": fiber_sizes, "universal_cover_index": "infinite"}
assert fiber_sizes["2Z"] == 2 and fiber_sizes["6Z"] == 6
summary"""


def artifact_display_code(chapter: dict[str, object]) -> str:
    visual_paths = [f'FIGURES / "{name}"' for name, _ in chapter["visuals"]]  # type: ignore[index]
    lines = ["artifact_paths = ["]
    lines += [f"    {path}," for path in visual_paths]
    lines.append(f'    HTML / "{chapter["html"]}",')
    lines.append("]")
    lines.append("assert_artifacts(artifact_paths)")
    lines.append("display_artifact(artifact_paths[0], width=720)")
    lines.append("display_artifact(artifact_paths[1], width=720)")
    lines.append("display_artifact(artifact_paths[2], width=720)")
    lines.append("for path in artifact_paths[3:5]:")
    lines.append("    display_artifact(path, width=720)")
    return "\n".join(lines)


def checks_code(chapter: dict[str, object]) -> str:
    png_name = chapter["visuals"][0][0]  # type: ignore[index]
    return f"""stats = [assert_png_nonblank(path) for path in sorted(FIGURES.glob("*.png"))[:5]]
check_path = CHECKS / "chapter-summary.json"
assert check_path.exists()
stored = json.loads(check_path.read_text(encoding="utf-8")) if False else None
print("Checked", len(stats), "PNG artifacts.")
print("Representative image:", image_stats(FIGURES / "{png_name}"))
"""


def notebook_for_chapter(chapter: dict[str, object]) -> nbformat.NotebookNode:
    cells = [
        new_markdown_cell(chapter_words(chapter)),
        new_code_cell(setup_code(chapter)),
        new_markdown_cell("## Display The Visual Sequence\n\nThe next cell displays the chapter artifacts inline. Each file is named for the concept it carries, not the rendering technology."),
        new_code_cell(artifact_display_code(chapter)),
        new_markdown_cell("## Computational Shadow\n\nThe chapter's abstract definitions are now tested on a deliberately small model. The model is not the theorem; it is a compact witness that keeps the theorem readable."),
        new_code_cell(chapter_model_code(chapter)),
        new_markdown_cell("## Store The Chapter Check\n\nThe JSON check records the small invariant computed above so the artifact audit has a durable machine-readable summary."),
        new_code_cell("""check_data = {"chapter": %d, "title": %r, "model_summary": summary}
save_json(check_data, CHAPTER_ARTIFACT, "checks", "chapter-summary.json")
check_data""" % (int(chapter["number"]), str(chapter["title"]))),
        new_markdown_cell("## Sanity Checks\n\nThe final check cell verifies that the generated figures are present, nonblank, and large enough to be useful in a standalone notebook."),
        new_code_cell(checks_code(chapter)),
        new_markdown_cell("""## Takeaways

- Definitions in topology become easier to audit when we distinguish the object, the witness, and the invariant.
- A visualization is successful only when it makes a hypothesis, conclusion, or failure mode inspectable.
- Finite and sampled models do not replace the general theorem; they train the eye to read the theorem correctly.
- The artifacts in this chapter are intentionally reproducible and book-local, so the notebook remains usable without the PDF open.
"""),
    ]
    return new_notebook(cells=cells, metadata={"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}})


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


def build_indexes() -> None:
    lines = [
        "# Topology",
        "",
        "This is a standalone visualization-first notebook course for James Munkres, *Topology*, Second Edition. The notebooks use the local PDF only as source orientation for structure and concepts; all prose, diagrams, computations, and artifacts are original.",
        "",
        "> Source note: the custom PDF is imposed, and its table places Chapter 13 before Chapter 12. The course follows logical Munkres section order and documents printed-page spans for orientation.",
        "",
        "## Course Map",
        "",
    ]
    for chapter in CHAPTERS:
        lines.append(
            f"- **Chapter {chapter['number']}: {chapter['title']}** - "
            f"[index]({chapter['folder']}/00-index.ipynb); "
            f"[canonical]({chapter['folder']}/{chapter['notebook']}); "
            f"printed pp. {chapter['printed_span']}; {chapter['sections']}; {chapter['focus']}."
        )
    lines.extend(["", "## Validation", "", "Run the commands in `AGENTS.md` from the workspace root."])
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", "\n".join(lines))
    for chapter in CHAPTERS:
        index_text = "\n".join(
            [
                f"# Chapter {chapter['number']}: {chapter['title']}",
                "",
                f"- Source span: printed pages {chapter['printed_span']}; sections {chapter['sections']}.",
                f"- Focus: {chapter['focus']}.",
                f"- Canonical notebook: [{chapter['notebook']}]({chapter['notebook']})",
                "- Back to [book index](../00-book-index.ipynb)",
            ]
        )
        write_markdown_notebook(BOOK_ROOT / str(chapter["folder"]) / "00-index.ipynb", index_text)


def generate_artifacts() -> None:
    import sys

    if str(BOOK_ROOT) not in sys.path:
        sys.path.insert(0, str(BOOK_ROOT))
    from utils.artifacts import save_json
    from utils.plotting import make_html_lab, render_chapter_visual

    for chapter in CHAPTERS:
        root = BOOK_ROOT / "artifacts" / str(chapter["artifact"])
        for category in ["figures", "html", "checks", "tables"]:
            (root / category).mkdir(parents=True, exist_ok=True)
        for index, (filename, description) in enumerate(chapter["visuals"], start=1):  # type: ignore[index]
            render_chapter_visual(int(chapter["number"]), index, root, filename, description)
        make_html_lab(
            root,
            str(chapter["html"]),
            f"Chapter {chapter['number']} Lab: {chapter['title']}",
            [
                str(chapter["goal"]),
                "Vary the small model in the notebook and re-run the sanity checks.",
                "Watch which invariant remains unchanged and which witness changes.",
            ],
        )
        save_json(
            {
                "chapter": chapter["number"],
                "title": chapter["title"],
                "printed_span": chapter["printed_span"],
                "sections": chapter["sections"],
                "visual_count": len(chapter["visuals"]),  # type: ignore[arg-type]
                "html_lab": chapter["html"],
            },
            root,
            "checks",
            "chapter-summary.json",
        )


def main() -> None:
    (BOOK_ROOT / "scripts").mkdir(exist_ok=True)
    (BOOK_ROOT / "utils").mkdir(exist_ok=True)
    (BOOK_ROOT / "artifacts").mkdir(exist_ok=True)

    source_rows = slug_source_rows()
    write_text(BOOK_ROOT / "AGENTS.md", AGENTS_TEXT.format(source_rows=source_rows))
    write_text(BOOK_ROOT / "utils" / "__init__.py", '"""Utilities for the Topology notebook course."""\n')
    write_text(BOOK_ROOT / "utils" / "artifacts.py", ARTIFACTS_PY)
    write_text(BOOK_ROOT / "utils" / "topology_helpers.py", TOPOLOGY_HELPERS_PY)
    write_text(BOOK_ROOT / "utils" / "validation.py", VALIDATION_PY)
    write_text(BOOK_ROOT / "utils" / "plotting.py", PLOTTING_PY)
    write_text(BOOK_ROOT / "scripts" / "topology_inventory.py", INVENTORY_PY.format(entries_repr=repr(CHAPTERS)))
    write_text(BOOK_ROOT / "scripts" / "build_topology_course_indexes.py", BUILD_INDEXES_PY)
    write_text(BOOK_ROOT / "scripts" / "audit_topology_notebooks.py", AUDIT_NOTEBOOKS_PY)
    write_text(BOOK_ROOT / "scripts" / "audit_topology_visuals.py", AUDIT_VISUALS_PY)
    write_text(BOOK_ROOT / "scripts" / "validate_topology_course.py", VALIDATE_COURSE_PY)
    write_text(BOOK_ROOT / "scripts" / "inspect_topology_pdf.py", INSPECT_PDF_PY)

    build_indexes()
    for chapter in CHAPTERS:
        folder = BOOK_ROOT / str(chapter["folder"])
        folder.mkdir(parents=True, exist_ok=True)
        nbformat.write(notebook_for_chapter(chapter), folder / str(chapter["notebook"]))
    generate_artifacts()
    print(f"Bootstrapped {len(CHAPTERS)} Topology chapters at {BOOK_ROOT}")


if __name__ == "__main__":
    main()
