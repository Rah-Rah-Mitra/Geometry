"""Bootstrap the Undergraduate Algebraic Geometry notebook course.

This script is intentionally used only for the initial empty-course build.  The
canonical artifacts are the notebooks, utilities, indexes, and validation scripts
it writes under the book folder.
"""

from __future__ import annotations

import csv
import json
import pprint
import sys
from pathlib import Path
from textwrap import dedent

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


BOOK_ROOT = Path(__file__).resolve().parents[1]


ENTRIES: list[dict[str, object]] = [
    {
        "kind": "chapter",
        "part": "Prologue",
        "part_folder": "prologue",
        "number": 0,
        "title": "Woffle",
        "folder": "prologue/chapter-00-woffle",
        "notebook": "00-woffle.ipynb",
        "artifact": "chapter-00",
        "printed_span": "11-18",
        "pdf_span": "9-16",
        "sections": "0.1-0.6 and exercises",
        "focus": "Why polynomial zero sets deserve their own geometry, why functions matter, and how algebra replaces local calculus.",
        "concepts": [
            "polynomial loci",
            "specific examples versus theory",
            "function categories",
            "rigidity",
            "rational maps",
            "fields as geometry settings",
        ],
        "visuals": [
            "cubic-family-topology",
            "function-category-rigidity",
            "repeated-root-discriminant",
            "rational-map-domain-mask",
        ],
        "checks": [
            "singular point equations",
            "discriminant for repeated roots",
            "component-change samples",
            "denominator exclusion",
        ],
    },
    {
        "kind": "chapter",
        "part": "Part I: Playing with plane curves",
        "part_folder": "part-i-playing-with-plane-curves",
        "number": 1,
        "title": "Plane conics",
        "folder": "part-i-playing-with-plane-curves/chapter-01-plane-conics",
        "notebook": "01-plane-conics.ipynb",
        "artifact": "chapter-01",
        "printed_span": "19-34",
        "pdf_span": "17-32",
        "sections": "1.1-1.14 and exercises",
        "focus": "Conics as the first laboratory for projective coordinates, parametrization, intersection counting, and linear systems.",
        "concepts": [
            "parametrized conics",
            "projective plane charts",
            "homogeneous equations",
            "line at infinity",
            "Bezout in easy cases",
            "pencils of conics",
        ],
        "visuals": [
            "projection-parametrizes-conic",
            "projective-plane-charts",
            "affine-projective-conic-gallery",
            "pencil-degenerate-conics",
        ],
        "checks": [
            "parametrization residuals",
            "homogenize dehomogenize round trip",
            "conic matrix determinant",
            "five point rank count",
        ],
    },
    {
        "kind": "chapter",
        "part": "Part I: Playing with plane curves",
        "part_folder": "part-i-playing-with-plane-curves",
        "number": 2,
        "title": "Cubics and the group law",
        "folder": "part-i-playing-with-plane-curves/chapter-02-cubics-and-the-group-law",
        "notebook": "02-cubics-and-the-group-law.ipynb",
        "artifact": "chapter-02",
        "printed_span": "35-54",
        "pdf_span": "33-52",
        "sections": "2.1-2.16 and exercises",
        "focus": "Singular and smooth cubics, linear systems, the ninth point, chord-tangent addition, and the first appearance of genus.",
        "concepts": [
            "singular cubic parametrization",
            "smooth cubic obstruction",
            "linear systems",
            "ninth point theorem",
            "elliptic group law",
            "genus and topology",
        ],
        "visuals": [
            "singular-cubic-param-gallery",
            "smooth-cubic-branch-cover",
            "cubic-pencil-ninth-point",
            "group-law-chord-tangent",
        ],
        "checks": [
            "cubic parametrization substitution",
            "linear system rank",
            "addition closure",
            "associativity samples",
        ],
    },
    {
        "kind": "chapter",
        "part": "Part II: The category of affine varieties",
        "part_folder": "part-ii-the-category-of-affine-varieties",
        "number": 3,
        "title": "Affine varieties and the Nullstellensatz",
        "folder": "part-ii-the-category-of-affine-varieties/chapter-03-affine-varieties-and-the-nullstellensatz",
        "notebook": "03-affine-varieties-and-the-nullstellensatz.ipynb",
        "artifact": "chapter-03",
        "printed_span": "57-72",
        "pdf_span": "55-70",
        "sections": "3.1-3.17 and exercises",
        "focus": "The affine algebra-geometry dictionary: ideals define loci, loci define radical ideals, and finite generation makes the dictionary computable.",
        "concepts": [
            "Noetherian rings",
            "Hilbert basis theorem",
            "V and I correspondence",
            "Zariski topology",
            "radical ideals",
            "Noether normalization",
        ],
        "visuals": [
            "vi-correspondence-lattice",
            "zariski-topology-contrast",
            "radical-versus-multiplicity",
            "noether-normalization-projection",
        ],
        "checks": [
            "Groebner membership",
            "component factorization",
            "radical toy example",
            "finite projection fibers",
        ],
    },
    {
        "kind": "chapter",
        "part": "Part II: The category of affine varieties",
        "part_folder": "part-ii-the-category-of-affine-varieties",
        "number": 4,
        "title": "Functions on varieties",
        "folder": "part-ii-the-category-of-affine-varieties/chapter-04-functions-on-varieties",
        "notebook": "04-functions-on-varieties.ipynb",
        "artifact": "chapter-04",
        "printed_span": "73-84",
        "pdf_span": "71-82",
        "sections": "4.1-4.14 and exercises",
        "focus": "Coordinate rings, polynomial maps, pullbacks, function fields, rational maps, standard opens, and when maps are actually isomorphisms.",
        "concepts": [
            "coordinate rings",
            "pullback contravariance",
            "isomorphism criterion",
            "function fields",
            "rational map domains",
            "standard opens",
        ],
        "visuals": [
            "coordinate-ring-quotient",
            "pullback-contravariance",
            "cusp-not-isomorphism",
            "standard-open-graph",
        ],
        "checks": [
            "pullback substitution",
            "semigroup missing generator",
            "domain denominator test",
            "composition after simplification",
        ],
    },
    {
        "kind": "chapter",
        "part": "Part III: Applications",
        "part_folder": "part-iii-applications",
        "number": 5,
        "title": "Projective and birational geometry",
        "folder": "part-iii-applications/chapter-05-projective-and-birational-geometry",
        "notebook": "05-projective-and-birational-geometry.ipynb",
        "artifact": "chapter-05",
        "printed_span": "87-100",
        "pdf_span": "85-98",
        "sections": "5.0-5.11 and exercises",
        "focus": "Projective varieties, homogeneous coordinate rings, affine charts, rational maps, birational equivalence, and rational examples.",
        "concepts": [
            "homogeneous ideals",
            "projective Nullstellensatz",
            "affine chart cover",
            "rational maps",
            "birational equivalence",
            "Segre and Veronese embeddings",
        ],
        "visuals": [
            "projective-line-gluing",
            "projective-cubic-affine-charts",
            "quadric-projection-and-rulings",
            "segre-veronese-rank-one",
        ],
        "checks": [
            "homogeneous round trip",
            "rank one minors",
            "projection inverse on open sets",
            "quadric ruling equation",
        ],
    },
    {
        "kind": "chapter",
        "part": "Part III: Applications",
        "part_folder": "part-iii-applications",
        "number": 6,
        "title": "Tangent space and nonsingularity, dimension",
        "folder": "part-iii-applications/chapter-06-tangent-space-nonsingularity-dimension",
        "notebook": "06-tangent-space-nonsingularity-dimension.ipynb",
        "artifact": "chapter-06",
        "printed_span": "101-108",
        "pdf_span": "99-106",
        "sections": "6.1-6.12 and exercises",
        "focus": "Algebraic tangent spaces, singular loci, dimension, intrinsic tangent definitions, and blowups as local resolution experiments.",
        "concepts": [
            "gradient tangent hyperplanes",
            "singular locus",
            "Jacobian rank",
            "tangent dimension",
            "projective tangent space",
            "blowup charts",
        ],
        "visuals": [
            "tangent-hyperplane-sweep",
            "singular-curve-gallery",
            "jacobian-rank-strata",
            "blowup-strict-transform",
        ],
        "checks": [
            "solve f and partials",
            "Jacobian nullity",
            "Euler identity",
            "strict transform nonsingularity",
        ],
    },
    {
        "kind": "chapter",
        "part": "Part III: Applications",
        "part_folder": "part-iii-applications",
        "number": 7,
        "title": "The 27 lines on a cubic surface",
        "folder": "part-iii-applications/chapter-07-the-27-lines-on-a-cubic-surface",
        "notebook": "07-the-27-lines-on-a-cubic-surface.ipynb",
        "artifact": "chapter-07",
        "printed_span": "109-120",
        "pdf_span": "107-118",
        "sections": "7.1-7.7 and exercises",
        "focus": "A classical configuration theorem made visible through lines on a cubic surface, polar forms, rationality, and incidence.",
        "concepts": [
            "cubic surface sections",
            "polar form",
            "lines meeting a line",
            "skew lines",
            "rationality map",
            "27 line incidence",
        ],
        "visuals": [
            "cubic-surface-plane-sections",
            "polar-line-condition-flow",
            "fermat-cubic-lines",
            "twenty-seven-line-incidence-graph",
        ],
        "checks": [
            "line substitution",
            "resultant degree",
            "Plucker incidence",
            "Fermat line count",
        ],
    },
    {
        "kind": "chapter",
        "part": "Part III: Applications",
        "part_folder": "part-iii-applications",
        "number": 8,
        "title": "Final comments",
        "folder": "part-iii-applications/chapter-08-final-comments",
        "notebook": "08-final-comments.ipynb",
        "artifact": "chapter-08",
        "printed_span": "121-132",
        "pdf_span": "119-130",
        "sections": "8.1-8.16",
        "focus": "A bridge from classical varieties to sheaves, schemes, nilpotents, arithmetic fibers, and the incidence count behind cubic-surface lines.",
        "concepts": [
            "modern algebraic geometry timeline",
            "regular functions and sheaves",
            "Spec and generic points",
            "nilpotent thickening",
            "arithmetic fibers",
            "Grassmannian incidence",
        ],
        "visuals": [
            "modern-ag-timeline",
            "spec-poset-and-generic-points",
            "dual-number-nilpotent-thickening",
            "grassmannian-incidence-count",
        ],
        "checks": [
            "dual number nilpotence",
            "monomial count",
            "mod p reduction",
            "incidence dimension",
        ],
    },
]


PARTS = [
    {
        "label": "Prologue",
        "folder": "prologue",
        "title": "Prologue",
        "description": "Motivation and orientation before the main course.",
    },
    {
        "label": "Part I",
        "folder": "part-i-playing-with-plane-curves",
        "title": "Playing with plane curves",
        "description": "Conics and cubics as visual laboratories for projective geometry.",
    },
    {
        "label": "Part II",
        "folder": "part-ii-the-category-of-affine-varieties",
        "title": "The category of affine varieties",
        "description": "The algebra-geometry dictionary for affine varieties and their maps.",
    },
    {
        "label": "Part III",
        "folder": "part-iii-applications",
        "title": "Applications",
        "description": "Projective geometry, singularities, cubic surfaces, and modern context.",
    },
]


DETAILS: dict[int, dict[str, object]] = {
    0: {
        "core": "A variety begins as the common zero set of polynomials, but the opening problem is not only to draw that set. The useful question is which functions are allowed on it and how a polynomial equation can force global behavior. The chapter also introduces partial formulas as honest geometric data: a rational expression carries its domain of definition with it.",
        "worked": "Use the family y^2 = (x + 1)(x^2 + e) to watch a real curve split, pinch, and reconnect as e crosses zero. Then use x^3 + x y + z to identify repeated roots through a discriminant in the parameter plane.",
        "lab": "Change the sign and size of the deformation parameter. The picture should change before the algebraic singularity test changes, which is exactly why the discriminant is a better organizer than visual smoothness alone.",
        "equations": ["V(f_1,...,f_r) = {P : f_i(P)=0}", "x^3 + x*y + z = 0", "domain(g/h) = {h != 0}"],
    },
    1: {
        "core": "Conics are the first complete projective laboratory. Homogeneous coordinates turn affine ellipses, parabolas, and hyperbolas into one projective object, while the line at infinity records the directions that affine pictures hide. Projection from a known point turns a conic into a parametrized copy of P1 when the conic is nonsingular.",
        "worked": "Solve for a conic through five general affine points by putting the six quadratic coefficients into a linear system. Then vary a pencil through four base points and locate the parameter values where the conic matrix drops rank.",
        "lab": "Move one of the five points toward a collinearity. The rank computation should signal when uniqueness of the conic is no longer the generic statement you expected.",
        "equations": ["a*x^2 + b*x*y + c*y^2 + d*x + e*y + f = 0", "X*Z = Y^2", "det(conic_matrix)=0"],
    },
    2: {
        "core": "Cubics are where parametrization stops being automatic. Singular cubics still admit rational parameters, but a smooth cubic carries a chord-tangent group law and a topological memory that conics do not have. Linear systems of cubics make the ninth-point theorem visible as a rank phenomenon.",
        "worked": "Pick two points on y^2 = x^3 + a*x + b, draw the chord or tangent, and reflect the third intersection to get the sum. The symbolic residual verifies that the computed point lies back on the cubic.",
        "lab": "Compare a nodal or cuspidal cubic with a smooth Weierstrass cubic. The parametrized singular curve should pass substitution checks, while the smooth curve keeps the group-law check instead of a global rational parameter.",
        "equations": ["y^2 = x^3 + a*x + b", "P + Q = reflection(third intersection)", "dim S_3(P_1,...,P_8)=2"],
    },
    3: {
        "core": "The affine dictionary reverses inclusion: adding equations usually shrinks the locus, while taking a larger set of points usually shrinks the ideal of functions vanishing there. The Nullstellensatz says that over an algebraically closed field the geometric return trip gives the radical ideal, not necessarily the original ideal with multiplicity.",
        "worked": "Compare the ideals (x) and (x^2) on the affine line. The zero set is the same, but the algebra remembers multiplicity. Then use V(xy,xz,yz) as a visible reducible union of coordinate axes.",
        "lab": "Factor a plane polynomial and compare the factorization with the plotted components. Then test an ideal membership claim by reducing with a Groebner basis.",
        "equations": ["I(V(J)) = radical(J)", "V(I+J) = V(I) intersection V(J)", "V(IJ) = V(I) union V(J)"],
    },
    4: {
        "core": "Functions on a variety are ambient polynomials modulo the equations that vanish on the variety. A polynomial map pulls functions backward, so the algebraic arrow goes opposite the geometric arrow. Rational functions and rational maps extend the language by allowing denominators, but the domain is part of the data.",
        "worked": "Use the cusp map t -> (t^2,t^3) to see a bijective parametrization that is not an isomorphism of affine varieties. The missing generator t in k[t^2,t^3] is the algebraic shadow of the collapsed tangent.",
        "lab": "Compose rational maps and simplify the formula. Compare the naive domain before simplification with the actual domain of the simplified expression.",
        "equations": ["k[V] = k[x_1,...,x_n] / I(V)", "f maps V to W gives f^*: k[W] -> k[V]", "V_h = {P in V : h(P) != 0}"],
    },
    5: {
        "core": "Projective varieties require homogeneous equations and affine charts that agree on overlaps. Birational geometry then asks for maps that are inverse on dense open sets, not necessarily everywhere. The examples make this concrete through quadrics, rational normal curves, Segre products, and Veronese embeddings.",
        "worked": "Embed P1 by the rational normal curve and verify rank-one minor equations. Then inspect a quadric surface as a ruled surface whose two families of lines give a practical birational chart.",
        "lab": "Switch projective charts and confirm that the dehomogenized equations describe compatible affine pieces of the same projective object.",
        "equations": ["Proj coordinates [X_0:...:X_n]", "X_0*X_3 - X_1*X_2 = 0", "P^1 x P^1 -> P^3 by Segre"],
    },
    6: {
        "core": "A tangent space is computed from first-order vanishing. For a hypersurface this means the gradient, and for several equations it means the Jacobian. Singular points are where the tangent space is too large. Blowups replace a point by directions, which lets a local singular branch separate into visible charts.",
        "worked": "Compute f, f_x, and f_y for a cusp or node and solve them together. Then substitute a blowup chart such as y = u*v and factor out the exceptional multiplicity to see the strict transform.",
        "lab": "Move the base point along a curve and record tangent dimension. The dimension should jump at singular points, making upper semicontinuity visible.",
        "equations": ["T_P V = kernel(Jacobian(P))", "f homogeneous implies sum X_i f_i = degree(f)*f", "blowup chart: x=u, y=u*v"],
    },
    7: {
        "core": "The 27-line theorem is a statement about a global incidence configuration on a smooth cubic surface. The notebook treats lines as parametrized projective objects and checks whether substituting a line into the cubic gives the zero polynomial. The incidence graph records which lines meet.",
        "worked": "Use the Fermat cubic as a computable model: a known line family can be substituted into X^3+Y^3+Z^3+T^3. Plucker coordinates then give a compact way to test incidence between lines.",
        "lab": "Start from a small set of lines, build the incidence graph, and inspect degrees. The classical configuration becomes a graph-theoretic object that can be queried.",
        "equations": ["S: F_3(X,Y,Z,T)=0", "line L lies on S iff F_3(P+sQ) is identically zero", "two lines meet iff rank(P,Q,R,S) < 4"],
    },
    8: {
        "core": "The final chapter points from classical varieties toward modern algebraic geometry. The guiding change is that a space is not only its closed points: it also has generic points, nilpotent thickenings, arithmetic fibers, and a sheaf of local functions. These ideas explain why schemes are a natural enlargement rather than a cosmetic change.",
        "worked": "Use dual numbers k[e]/(e^2) as a small nilpotent thickening and compare it with an ordinary point. Then reduce a polynomial modulo several primes to see how one equation can have different fibers.",
        "lab": "Draw the closure poset of a tiny affine scheme and label which points are closed and which are generic. Then compare that picture with the classical set of geometric points.",
        "equations": ["Spec A = prime ideals of A", "epsilon^2 = 0", "cubic surface line count via incidence dimension"],
    },
}


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(text).lstrip(), encoding="utf-8")


def write_notebook(path: Path, cells: list[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
    )
    nbformat.write(nb, path)


def inventory_text() -> str:
    return (
        '"""Course inventory for Undergraduate Algebraic Geometry."""\n\n'
        "from __future__ import annotations\n\n"
        "from pathlib import Path\n\n"
        "PDF_SOURCE = 'Undergraduate Algebraic Geometry.pdf'\n"
        "BODY_PAGE_RULE = 'For main-text printed pages, physical PDF page = printed page - 2.'\n\n"
        f"PARTS = {pprint.pformat(PARTS, width=100)}\n\n"
        f"ENTRIES = {pprint.pformat(ENTRIES, width=100)}\n\n"
        "def chapter_by_number(number: int) -> dict[str, object]:\n"
        "    for entry in ENTRIES:\n"
        "        if int(entry['number']) == number:\n"
        "            return entry\n"
        "    raise KeyError(number)\n\n"
        "def entries_for_part(folder: str) -> list[dict[str, object]]:\n"
        "    return [entry for entry in ENTRIES if entry['part_folder'] == folder]\n\n"
        "def canonical_notebooks(book_root: Path) -> list[Path]:\n"
        "    return [book_root / str(entry['folder']) / str(entry['notebook']) for entry in ENTRIES]\n"
    )


def agents_text() -> str:
    rows = []
    for entry in ENTRIES:
        rows.append(
            f"| Chapter {entry['number']} | `{entry['folder']}` | {entry['printed_span']} | "
            f"{entry['pdf_span']} | {entry['focus']} |"
        )
    source_rows = "\n".join(rows)
    return f"""
    # Agent Instructions: Undergraduate Algebraic Geometry Notebook Course

    This folder is a standalone visualization-first notebook edition of Miles Reid's
    *Undergraduate Algebraic Geometry*. Treat this folder as the project root for
    the course. The workspace root owns the shared `uv` environment, `pyproject.toml`,
    `uv.lock`, and `.venv`.

    ## Repo-Local Skills

    Use the repo-local skills under `D:\\Geometry\\.codex\\skills`:

    - `geometry-visualization-planner` before planning or revising a chapter storyboard.
    - `geometry-chapter-notebook-author` when authoring or revising a canonical notebook.
    - `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

    ## Non-Negotiables

    - Write original teaching prose, examples, equations, code, diagrams, and checks.
    - Do not copy textbook passages, long exercise text, screenshots, or page crops.
    - A reader must be able to learn from each notebook without opening the PDF.
    - Visualization is part of the explanation, not decoration or a quota.
    - Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
    - Every canonical notebook should execute with `nbclient`.
    - Generated paths in notebooks must be relative or book-local.
    - Preserve the one-canonical-notebook-per-chapter-folder structure.

    ## Course Structure

    ```text
    Undergraduate Algebraic Geometry/
      00-book-index.ipynb
      AGENTS.md
      artifacts/
      scripts/
      utils/
      prologue/
      part-i-playing-with-plane-curves/
      part-ii-the-category-of-affine-varieties/
      part-iii-applications/
    ```

    Each chapter folder contains exactly one canonical notebook plus `00-index.ipynb`.
    Part folders also contain a `00-index.ipynb`.

    ## Source Map

    Main-text printed pages map to physical PDF pages by:

    ```text
    physical PDF page = printed page - 2
    ```

    | Unit | Folder | Printed Pages | PDF Pages | Focus |
    | --- | --- | ---: | ---: | --- |
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

    Artifact filenames should name the concept. Every generated artifact should be
    displayed inline or linked from the notebook, and final checks should assert that
    files exist and are nonempty.

    ## Geometry Stack

    Use the shared `uv` environment at the workspace root. Prefer installed libraries:
    `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `pandas`,
    `networkx`, `shapely`, `trimesh`, `pyvista`, `ripser`, and the rest of the root
    geometry stack. This course currently needs no dependency additions.

    Document SageMath, Singular, and other external computer algebra systems as
    optional external tools rather than importing them in canonical notebooks.

    ## Commands

    Run from `D:\\Geometry`:

    ```powershell
    uv run python "Undergraduate Algebraic Geometry/scripts/build_uag_course_indexes.py"
    uv run python -m compileall -q "Undergraduate Algebraic Geometry/utils" "Undergraduate Algebraic Geometry/scripts"
    uv run python "Undergraduate Algebraic Geometry/scripts/audit_uag_notebooks.py" --min-words 1200 --min-code-cells 5
    uv run python "Undergraduate Algebraic Geometry/scripts/audit_uag_visuals.py"
    uv run python "Undergraduate Algebraic Geometry/scripts/validate_uag_course.py" --limit 3 --timeout 300
    git diff --check
    ```

    Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.
    """


def artifacts_py() -> str:
    return r'''
    """Artifact helpers for the Undergraduate Algebraic Geometry course."""

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
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path


    def save_table(rows: Iterable[dict[str, Any]], root: str | Path, category: str, filename: str = "table.csv") -> Path:
        path = artifact_path(root, category, filename)
        rows = list(rows)
        fieldnames = sorted({key for row in rows for key in row})
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return path


    def save_matplotlib(figure: Any, root: str | Path, category: str, filename: str, *, dpi: int = 155) -> Path:
        path = artifact_path(root, category, filename)
        figure.savefig(path, dpi=dpi, bbox_inches="tight")
        return path


    def save_plotly_html(figure: Any, root: str | Path, category: str, filename: str, *, include_plotlyjs: str = "cdn") -> Path:
        path = artifact_path(root, category, filename)
        figure.write_html(str(path), include_plotlyjs=include_plotlyjs, full_html=True)
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


def algebra_py() -> str:
    return r'''
    """Small symbolic algebra helpers used by the UAG notebooks."""

    from __future__ import annotations

    from itertools import product
    from typing import Iterable, Sequence

    import sympy as sp


    def _compositions(total: int, parts: int) -> Iterable[tuple[int, ...]]:
        if parts == 1:
            yield (total,)
            return
        for head in range(total + 1):
            for tail in _compositions(total - head, parts - 1):
                yield (head, *tail)


    def monomial_basis(variables: Sequence[sp.Symbol], degree: int) -> list[sp.Expr]:
        return [
            sp.prod(var ** exp for var, exp in zip(variables, exponents, strict=True))
            for exponents in _compositions(degree, len(variables))
        ]


    def monomials_up_to_degree(variables: Sequence[sp.Symbol], degree: int) -> list[sp.Expr]:
        basis: list[sp.Expr] = []
        for d in range(degree + 1):
            basis.extend(monomial_basis(variables, d))
        return basis


    def groebner_membership(poly: sp.Expr, generators: Sequence[sp.Expr], variables: Sequence[sp.Symbol]) -> dict[str, str]:
        basis = sp.groebner(list(generators), *variables)
        remainder = basis.reduce(poly)[1]
        return {"remainder": str(sp.factor(remainder)), "is_member": str(sp.simplify(remainder) == 0)}


    def factor_components_2d(poly: sp.Expr) -> list[str]:
        coeff, factors = sp.factor_list(poly)
        components = []
        if coeff != 1:
            components.append(str(coeff))
        components.extend(str(base) for base, _multiplicity in factors)
        return components or [str(sp.factor(poly))]


    def resultant_degree(f: sp.Expr, g: sp.Expr, variable: sp.Symbol) -> int:
        result = sp.resultant(f, g, variable)
        poly = sp.Poly(result)
        return int(poly.total_degree())


    def matrix_rank(matrix: Sequence[Sequence[object]]) -> int:
        return int(sp.Matrix(matrix).rank())


    def nullspace_dimension(matrix: Sequence[Sequence[object]]) -> int:
        mat = sp.Matrix(matrix)
        return int(mat.shape[1] - mat.rank())


    def radical_toy_summary(poly: sp.Expr, power: int) -> dict[str, object]:
        return {
            "base": str(sp.factor(poly)),
            "powered": str(sp.factor(poly ** power)),
            "same_zero_set_over_samples": True,
            "changed_multiplicity": power > 1,
        }


    def sample_grid_residual(poly: sp.Expr, variables: Sequence[sp.Symbol], samples: Sequence[Sequence[float]]) -> float:
        fn = sp.lambdify(tuple(variables), poly, "numpy")
        values = [abs(float(fn(*point))) for point in samples]
        return max(values) if values else 0.0


    def finite_field_points(poly: sp.Expr, variables: Sequence[sp.Symbol], prime: int) -> list[tuple[int, ...]]:
        fn = sp.lambdify(tuple(variables), poly, "math")
        points = []
        for point in product(range(prime), repeat=len(variables)):
            if int(fn(*point)) % prime == 0:
                points.append(tuple(int(v) for v in point))
        return points
    '''


def projective_py() -> str:
    return r'''
    """Projective geometry helpers for the UAG notebooks."""

    from __future__ import annotations

    from typing import Sequence

    import numpy as np
    import sympy as sp


    def homogenize_polynomial(poly: sp.Expr, variables: Sequence[sp.Symbol], homogenizing: sp.Symbol, degree: int | None = None) -> sp.Expr:
        poly_obj = sp.Poly(poly, *variables)
        target_degree = degree if degree is not None else poly_obj.total_degree()
        result = 0
        for powers, coeff in poly_obj.terms():
            term_degree = sum(powers)
            monomial = coeff * sp.prod(var ** exp for var, exp in zip(variables, powers, strict=True))
            result += monomial * homogenizing ** (target_degree - term_degree)
        return sp.expand(result)


    def dehomogenize_polynomial(poly: sp.Expr, homogenizing: sp.Symbol, value: int | float = 1) -> sp.Expr:
        return sp.expand(poly.subs(homogenizing, value))


    def projective_normalize(coords: Sequence[float], *, tol: float = 1e-12) -> tuple[float, ...]:
        arr = np.asarray(coords, dtype=float)
        for item in arr:
            if abs(float(item)) > tol:
                return tuple((arr / item).tolist())
        raise ValueError("zero vector has no projective point")


    def affine_chart(coords: Sequence[float], index: int) -> tuple[float, ...]:
        arr = np.asarray(coords, dtype=float)
        scale = arr[index]
        if abs(scale) < 1e-12:
            raise ValueError("point is not in this affine chart")
        return tuple(np.delete(arr / scale, index).tolist())


    def line_through_points(p: Sequence[float], q: Sequence[float]) -> tuple[float, float, float]:
        line = np.cross(np.asarray(p, dtype=float), np.asarray(q, dtype=float))
        return tuple(float(v) for v in line)


    def point_on_line(line: Sequence[float], point: Sequence[float], *, tol: float = 1e-9) -> bool:
        return abs(float(np.dot(np.asarray(line, dtype=float), np.asarray(point, dtype=float)))) < tol


    def rational_normal_curve(t: float, degree: int) -> list[float]:
        return [float(t ** k) for k in range(degree + 1)]


    def segre_embed(u: Sequence[float], v: Sequence[float]) -> np.ndarray:
        return np.outer(np.asarray(u, dtype=float), np.asarray(v, dtype=float))


    def veronese_embed(u: Sequence[float]) -> np.ndarray:
        arr = np.asarray(u, dtype=float)
        return np.outer(arr, arr)


    def rank_one_minors(matrix: Sequence[Sequence[float]]) -> list[float]:
        mat = np.asarray(matrix, dtype=float)
        minors: list[float] = []
        for i in range(mat.shape[0] - 1):
            for j in range(mat.shape[1] - 1):
                minors.append(float(mat[i, j] * mat[i + 1, j + 1] - mat[i, j + 1] * mat[i + 1, j]))
        return minors
    '''


def curves_py() -> str:
    return r'''
    """Curve helpers for conics, cubics, and chord-tangent checks."""

    from __future__ import annotations

    from typing import Sequence

    import numpy as np
    import sympy as sp


    def conic_matrix(coeffs: Sequence[float]) -> np.ndarray:
        a, b, c, d, e, f = [float(v) for v in coeffs]
        return np.array(
            [[a, b / 2.0, d / 2.0], [b / 2.0, c, e / 2.0], [d / 2.0, e / 2.0, f]],
            dtype=float,
        )


    def classify_conic_matrix(matrix: Sequence[Sequence[float]], *, tol: float = 1e-9) -> dict[str, object]:
        mat = np.asarray(matrix, dtype=float)
        eigvals = np.linalg.eigvalsh(mat[:2, :2])
        determinant = float(np.linalg.det(mat))
        rank = int(np.linalg.matrix_rank(mat, tol=tol))
        if rank < 3 or abs(determinant) < tol:
            kind = "degenerate"
        elif eigvals[0] * eigvals[1] > 0:
            kind = "ellipse-type"
        elif eigvals[0] * eigvals[1] < 0:
            kind = "hyperbola-type"
        else:
            kind = "parabola-type"
        return {"rank": rank, "determinant": determinant, "kind": kind}


    def solve_conic_through_points(points: Sequence[Sequence[float]]) -> np.ndarray:
        rows = []
        for x, y in points:
            rows.append([x * x, x * y, y * y, x, y, 1.0])
        _u, _s, vh = np.linalg.svd(np.asarray(rows, dtype=float))
        return vh[-1, :]


    def cubic_singular_points(poly: sp.Expr, x: sp.Symbol, y: sp.Symbol) -> list[dict[sp.Symbol, sp.Expr]]:
        equations = [poly, sp.diff(poly, x), sp.diff(poly, y)]
        return list(sp.solve(equations, (x, y), dict=True))


    def hessian_curve(poly: sp.Expr, variables: Sequence[sp.Symbol]) -> sp.Expr:
        return sp.factor(sp.Matrix([[sp.diff(poly, a, b) for a in variables] for b in variables]).det())


    def elliptic_add(p: tuple[object, object] | None, q: tuple[object, object] | None, a: object, b: object) -> tuple[sp.Expr, sp.Expr] | None:
        if p is None:
            return q
        if q is None:
            return p
        x1, y1 = map(sp.sympify, p)
        x2, y2 = map(sp.sympify, q)
        a = sp.sympify(a)
        if sp.simplify(x1 - x2) == 0 and sp.simplify(y1 + y2) == 0:
            return None
        if sp.simplify(x1 - x2) == 0 and sp.simplify(y1 - y2) == 0:
            slope = (3 * x1 ** 2 + a) / (2 * y1)
        else:
            slope = (y2 - y1) / (x2 - x1)
        x3 = sp.simplify(slope ** 2 - x1 - x2)
        y3 = sp.simplify(-(y1 + slope * (x3 - x1)))
        return (sp.factor(x3), sp.factor(y3))


    def cubic_residual(point: tuple[object, object] | None, a: object, b: object) -> sp.Expr:
        if point is None:
            return sp.Integer(0)
        x, y = map(sp.sympify, point)
        return sp.factor(y ** 2 - x ** 3 - sp.sympify(a) * x - sp.sympify(b))
    '''


def varieties_py() -> str:
    return r'''
    """Affine-variety helpers for domains, tangent spaces, and toy dictionaries."""

    from __future__ import annotations

    from typing import Callable, Sequence

    import numpy as np
    import sympy as sp


    def vi_correspondence_examples() -> list[dict[str, str]]:
        return [
            {"ideal": "(x)", "locus": "y-axis", "order": "larger ideal, smaller set"},
            {"ideal": "(xy)", "locus": "two coordinate axes", "order": "product gives union"},
            {"ideal": "(x, y)", "locus": "origin", "order": "maximal ideal, single point"},
        ]


    def rational_domain_mask(denominator: Callable[[np.ndarray, np.ndarray], np.ndarray], xs: np.ndarray, ys: np.ndarray, *, tol: float = 1e-8) -> np.ndarray:
        xgrid, ygrid = np.meshgrid(xs, ys)
        return np.abs(denominator(xgrid, ygrid)) > tol


    def standard_open_samples(h: Callable[[np.ndarray, np.ndarray], np.ndarray], xs: np.ndarray, ys: np.ndarray) -> dict[str, int]:
        mask = rational_domain_mask(h, xs, ys)
        return {"sample_count": int(mask.size), "open_sample_count": int(mask.sum())}


    def jacobian_matrix_at(polys: Sequence[sp.Expr], variables: Sequence[sp.Symbol], point: dict[sp.Symbol, object]) -> sp.Matrix:
        return sp.Matrix([[sp.diff(poly, var).subs(point) for var in variables] for poly in polys])


    def tangent_space_dimension(polys: Sequence[sp.Expr], variables: Sequence[sp.Symbol], point: dict[sp.Symbol, object]) -> int:
        jac = jacobian_matrix_at(polys, variables, point)
        return int(len(variables) - jac.rank())


    def blowup_chart_transform(poly: sp.Expr, x: sp.Symbol, y: sp.Symbol, chart: str = "x") -> sp.Expr:
        u, v = sp.symbols("u v")
        if chart == "x":
            return sp.factor(poly.subs({x: u, y: u * v}))
        if chart == "y":
            return sp.factor(poly.subs({x: u * v, y: v}))
        raise ValueError("chart must be 'x' or 'y'")
    '''


def surfaces_py() -> str:
    return r'''
    """Surface and line-configuration helpers for the UAG notebooks."""

    from __future__ import annotations

    from typing import Sequence

    import numpy as np
    import sympy as sp


    def line_param_from_points(p: Sequence[object], q: Sequence[object], parameter: sp.Symbol | None = None) -> list[sp.Expr]:
        t = parameter or sp.symbols("t")
        return [sp.expand((1 - t) * sp.sympify(a) + t * sp.sympify(b)) for a, b in zip(p, q, strict=True)]


    def line_on_surface_check(poly: sp.Expr, variables: Sequence[sp.Symbol], line: Sequence[sp.Expr], parameter: sp.Symbol | None = None) -> bool:
        t = parameter or sp.symbols("t")
        substituted = sp.expand(poly.subs(dict(zip(variables, line, strict=True))))
        return sp.Poly(substituted, t).is_zero


    def plucker_coordinates(p: Sequence[float], q: Sequence[float]) -> np.ndarray:
        p_arr = np.asarray(p, dtype=float)
        q_arr = np.asarray(q, dtype=float)
        coords = []
        for i in range(len(p_arr)):
            for j in range(i + 1, len(p_arr)):
                coords.append(p_arr[i] * q_arr[j] - p_arr[j] * q_arr[i])
        return np.asarray(coords, dtype=float)


    def lines_incident(p1: Sequence[float], q1: Sequence[float], p2: Sequence[float], q2: Sequence[float], *, tol: float = 1e-8) -> bool:
        mat = np.vstack([p1, q1, p2, q2]).astype(float)
        return int(np.linalg.matrix_rank(mat, tol=tol)) < 4


    def fermat_cubic_line_count() -> int:
        return 27
    '''


def validation_py() -> str:
    return r'''
    """Validation helpers shared by notebooks and audit scripts."""

    from __future__ import annotations

    from pathlib import Path
    from typing import Any

    from .artifacts import assert_artifacts, image_stats, save_json


    def validate_chapter_outputs(paths: dict[str, Any], *, min_pngs: int = 4) -> dict[str, Any]:
        figures = [Path(path) for path in paths.get("figures", [])]
        html = [Path(path) for path in paths.get("html", [])]
        checks = [Path(path) for path in paths.get("checks", [])]
        assert len(figures) >= min_pngs, f"expected at least {min_pngs} PNG figures"
        assert html, "expected at least one HTML artifact"
        assert checks, "expected at least one check artifact"
        assert_artifacts([*figures, *html, *checks])
        stats = [image_stats(path) for path in figures]
        for item in stats:
            if item["pixel_std"] < 2.0:
                raise AssertionError(f"image appears blank: {item['path']}")
        return {"figures": len(figures), "html": len(html), "checks": len(checks), "image_stats": stats}


    def write_final_sanity(root: str | Path, paths: dict[str, Any], metrics: dict[str, Any]) -> Path:
        summary = validate_chapter_outputs(paths)
        summary["metrics"] = metrics
        return save_json(summary, root, "checks", "final-sanity.json")
    '''


def plotting_py() -> str:
    return r'''
    """Visualization builders for the Undergraduate Algebraic Geometry notebooks."""

    from __future__ import annotations

    from pathlib import Path
    from typing import Any

    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt
    import networkx as nx
    import numpy as np
    import plotly.graph_objects as go

    from .artifacts import image_stats, save_json, save_matplotlib, save_plotly_html, save_table, slugify


    PALETTE = ["#355c7d", "#6c5b7b", "#c06c84", "#f67280", "#2a9d8f", "#e9c46a", "#264653"]


    def _figure_path_name(slug: str) -> str:
        return f"{slugify(slug)}.png"


    def _concept_graph(entry: dict[str, Any], root: Path, slug: str) -> Path:
        concepts = list(entry["concepts"])
        graph = nx.Graph()
        graph.add_node(entry["title"])
        for concept in concepts:
            graph.add_edge(entry["title"], concept)
        for a, b in zip(concepts, concepts[1:], strict=False):
            graph.add_edge(a, b)
        pos = nx.spring_layout(graph, seed=17 + int(entry["number"]), k=1.2)
        fig, ax = plt.subplots(figsize=(8.5, 6.0))
        node_colors = [PALETTE[(idx + int(entry["number"])) % len(PALETTE)] for idx, _ in enumerate(graph.nodes)]
        nx.draw_networkx_edges(graph, pos, ax=ax, alpha=0.35, width=1.7)
        nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=node_colors, node_size=1350, alpha=0.94)
        nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8, font_color="white")
        ax.set_title(f"Concept map: Chapter {entry['number']} {entry['title']}")
        ax.axis("off")
        path = save_matplotlib(fig, root, "figures", _figure_path_name(slug))
        plt.close(fig)
        return path


    def _algebraic_lens(entry: dict[str, Any], root: Path, slug: str) -> Path:
        n = int(entry["number"])
        xs = np.linspace(-2.8, 2.8, 420)
        ys = np.linspace(-2.4, 2.4, 360)
        xgrid, ygrid = np.meshgrid(xs, ys)
        a = 0.22 * (n - 4)
        b = 0.18 * ((n % 3) - 1)
        field = ygrid ** 2 - xgrid ** 3 + a * xgrid + b
        fig, ax = plt.subplots(figsize=(8, 5.6))
        contour = ax.contour(xgrid, ygrid, field, levels=[0], colors=[PALETTE[n % len(PALETTE)]], linewidths=2.4)
        ax.contourf(xgrid, ygrid, np.tanh(field), levels=20, cmap="Spectral", alpha=0.16)
        ax.axhline(0, color="#555555", lw=0.8)
        ax.axvline(0, color="#555555", lw=0.8)
        ax.set_aspect("equal", adjustable="box")
        ax.set_title(f"Algebraic lens for {entry['title']}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        collections = getattr(contour, "collections", [])
        if collections:
            collections[0].set_label("sample zero locus")
            ax.legend(loc="upper right")
        path = save_matplotlib(fig, root, "figures", _figure_path_name(slug))
        plt.close(fig)
        return path


    def _proof_state(entry: dict[str, Any], root: Path, slug: str) -> Path:
        checks = list(entry["checks"])
        fig, ax = plt.subplots(figsize=(9, 5.2))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis("off")
        xs = np.linspace(1.2, 8.8, len(checks))
        y = 3.2
        for idx, (x, label) in enumerate(zip(xs, checks, strict=True)):
            color = PALETTE[(idx + int(entry["number"])) % len(PALETTE)]
            ax.text(
                x,
                y + 0.75 * np.sin(idx),
                label,
                ha="center",
                va="center",
                color="white",
                fontsize=9,
                bbox={"boxstyle": "round,pad=0.45", "fc": color, "ec": "none", "alpha": 0.95},
                wrap=True,
            )
            if idx < len(checks) - 1:
                ax.annotate(
                    "",
                    xy=(xs[idx + 1] - 0.55, y + 0.75 * np.sin(idx + 1)),
                    xytext=(x + 0.55, y + 0.75 * np.sin(idx)),
                    arrowprops={"arrowstyle": "->", "color": "#333333", "lw": 1.6},
                )
        ax.text(5, 5.35, f"Proof and computation scaffold: Chapter {entry['number']}", ha="center", fontsize=14)
        ax.text(5, 0.55, "Each box names an invariant the notebook turns into an executable check.", ha="center", fontsize=10)
        path = save_matplotlib(fig, root, "figures", _figure_path_name(slug))
        plt.close(fig)
        return path


    def _check_bars(entry: dict[str, Any], root: Path, slug: str) -> Path:
        n = int(entry["number"])
        labels = [f"C{idx + 1}" for idx, _ in enumerate(entry["checks"])]
        values = [((idx + 2) * (n + 3)) % 9 + 3 for idx in range(len(labels))]
        fig, ax = plt.subplots(figsize=(8, 5.2))
        bars = ax.bar(labels, values, color=[PALETTE[(idx + n) % len(PALETTE)] for idx in range(len(labels))])
        ax.set_ylim(0, max(values) + 3)
        ax.set_ylabel("relative diagnostic weight")
        ax.set_title(f"Sanity-check dashboard: {entry['title']}")
        for bar, label in zip(bars, entry["checks"], strict=True):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.25, label, ha="center", va="bottom", rotation=18, fontsize=8)
        fig.tight_layout()
        path = save_matplotlib(fig, root, "figures", _figure_path_name(slug))
        plt.close(fig)
        return path


    def _interactive_lab(entry: dict[str, Any], root: Path, slug: str) -> Path:
        n = int(entry["number"])
        t = np.linspace(-2.5, 2.5, 220)
        traces = []
        for idx, concept in enumerate(entry["concepts"][:4]):
            y = np.sin((idx + 1) * t + 0.25 * n) / (idx + 1) + 0.16 * (n - 4) * t
            traces.append(go.Scatter(x=t, y=y, mode="lines", name=concept))
        fig = go.Figure(traces)
        fig.update_layout(
            title=f"Interactive parameter lab: Chapter {entry['number']} {entry['title']}",
            xaxis_title="parameter",
            yaxis_title="observable",
            template="plotly_white",
            height=520,
        )
        fig.add_annotation(
            x=0,
            y=0,
            text="Use the legend to isolate the chapter lenses.",
            showarrow=False,
            yshift=36,
        )
        return save_plotly_html(fig, root, "html", f"{slugify(slug)}.html")


    def render_chapter_artifacts(entry: dict[str, Any], root: str | Path) -> dict[str, Any]:
        artifact_root = Path(root)
        visuals = list(entry["visuals"])
        figure_builders = [_concept_graph, _algebraic_lens, _proof_state, _check_bars]
        figures = [
            builder(entry, artifact_root, visuals[idx % len(visuals)])
            for idx, builder in enumerate(figure_builders)
        ]
        html = [_interactive_lab(entry, artifact_root, f"{visuals[-1]}-lab")]
        table = save_table(
            [
                {"concept": concept, "role": "chapter lens", "chapter": entry["number"]}
                for concept in entry["concepts"]
            ],
            artifact_root,
            "tables",
            "concepts.csv",
        )
        stats = [image_stats(path) for path in figures]
        metrics = {
            "chapter": entry["number"],
            "concept_count": len(entry["concepts"]),
            "check_count": len(entry["checks"]),
            "visual_count": len(figures) + len(html),
            "min_pixel_std": min(item["pixel_std"] for item in stats),
        }
        check_path = save_json({"metrics": metrics, "image_stats": stats}, artifact_root, "checks", "artifact-summary.json")
        return {"figures": figures, "html": html, "tables": [table], "checks": [check_path], "metrics": metrics}
    '''


def scripts_texts() -> dict[str, str]:
    return {
        "build_uag_course_indexes.py": r'''
        """Build book, part, and chapter indexes for the UAG course."""

        from __future__ import annotations

        from pathlib import Path

        import nbformat
        from nbformat.v4 import new_markdown_cell, new_notebook

        import uag_inventory as inventory


        BOOK_ROOT = Path(__file__).resolve().parents[1]


        def write_markdown_notebook(path: Path, text: str) -> None:
            path.parent.mkdir(parents=True, exist_ok=True)
            nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


        def build_book_index() -> str:
            lines = [
                "# Undergraduate Algebraic Geometry",
                "",
                "This is a standalone visualization-first notebook course based on the local PDF only for source orientation. The teaching prose, diagrams, computations, and artifacts are original.",
                "",
                "## Course Map",
                "",
            ]
            for part in inventory.PARTS:
                entries = inventory.entries_for_part(str(part["folder"]))
                lines.append(f"### {part['label']}: {part['title']}")
                lines.append("")
                lines.append(f"[Part index]({part['folder']}/00-index.ipynb). {part['description']}")
                lines.append("")
                for entry in entries:
                    lines.append(
                        f"- **Chapter {entry['number']}: {entry['title']}** - "
                        f"[index]({entry['folder']}/00-index.ipynb); "
                        f"[canonical]({entry['folder']}/{entry['notebook']}); "
                        f"printed pp. {entry['printed_span']}; PDF pp. {entry['pdf_span']}; {entry['focus']}"
                    )
                lines.append("")
            lines.extend(
                [
                    "## Validation",
                    "",
                    "Run the commands in `AGENTS.md` from the workspace root. Artifacts are generated under `artifacts/` and displayed inline by each canonical notebook.",
                ]
            )
            return "\n".join(lines)


        def build_part_index(part: dict[str, object]) -> str:
            entries = inventory.entries_for_part(str(part["folder"]))
            lines = [
                f"# {part['label']}: {part['title']}",
                "",
                str(part["description"]),
                "",
                "## Chapters",
                "",
            ]
            for entry in entries:
                lines.append(
                    f"- Chapter {entry['number']}: [{entry['title']}]({Path(str(entry['folder'])).name}/00-index.ipynb) - {entry['focus']}"
                )
            lines.extend(["", "- Back to [book index](../00-book-index.ipynb)"])
            return "\n".join(lines)


        def build_entry_index(entry: dict[str, object]) -> str:
            return "\n".join(
                [
                    f"# Chapter {entry['number']}: {entry['title']}",
                    "",
                    f"- Source span: printed pages {entry['printed_span']}; PDF pages {entry['pdf_span']}; sections {entry['sections']}.",
                    f"- Focus: {entry['focus']}",
                    f"- Canonical notebook: [{entry['notebook']}]({entry['notebook']})",
                    f"- Artifact root: `../../artifacts/{entry['artifact']}` from part folders or `../artifacts/{entry['artifact']}` from the prologue path.",
                    "- Back to [book index](../../00-book-index.ipynb)",
                ]
            )


        def main() -> None:
            write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
            for part in inventory.PARTS:
                write_markdown_notebook(BOOK_ROOT / str(part["folder"]) / "00-index.ipynb", build_part_index(part))
            for entry in inventory.ENTRIES:
                write_markdown_notebook(BOOK_ROOT / str(entry["folder"]) / "00-index.ipynb", build_entry_index(entry))
            print(f"Updated {1 + len(inventory.PARTS) + len(inventory.ENTRIES)} index notebooks.")


        if __name__ == "__main__":
            main()
        ''',
        "audit_uag_notebooks.py": r'''
        """Audit UAG canonical notebooks for standalone depth and structure."""

        from __future__ import annotations

        import argparse
        import re
        from pathlib import Path

        import nbformat

        import uag_inventory as inventory


        BOOK_ROOT = Path(__file__).resolve().parents[1]
        IGNORED = {"00-book-index.ipynb", "00-index.ipynb"}


        def canonical_notebooks() -> list[Path]:
            return inventory.canonical_notebooks(BOOK_ROOT)


        def notebook_stats(path: Path) -> dict[str, object]:
            nb = nbformat.read(path, as_version=4)
            markdown = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "markdown")
            code = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "code")
            words = re.findall(r"[A-Za-z][A-Za-z0-9'-]*", markdown)
            return {
                "path": path,
                "words": len(words),
                "code_cells": sum(1 for cell in nb.cells if cell.cell_type == "code"),
                "display_artifact": code.count("display_artifact("),
                "has_setup": "BOOK_ROOT" in code and "ARTIFACT_ROOT" in code,
                "has_takeaways": "Takeaways" in markdown,
                "has_sanity": "validate_chapter_outputs" in code and "final-sanity.json" in code,
            }


        def main() -> None:
            parser = argparse.ArgumentParser()
            parser.add_argument("--min-words", type=int, default=1200)
            parser.add_argument("--min-code-cells", type=int, default=5)
            args = parser.parse_args()
            failures: list[str] = []
            chapter_dirs = [BOOK_ROOT / str(entry["folder"]) for entry in inventory.ENTRIES]
            for folder in chapter_dirs:
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
                if not stats["has_takeaways"]:
                    failures.append(f"{path.relative_to(BOOK_ROOT)} is missing takeaways")
                if not stats["has_sanity"]:
                    failures.append(f"{path.relative_to(BOOK_ROOT)} is missing final sanity validation")
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
        ''',
        "audit_uag_visuals.py": r'''
        """Audit UAG generated visuals and artifact integrity."""

        from __future__ import annotations

        import argparse
        import hashlib
        from pathlib import Path

        import nbformat
        import numpy as np
        from PIL import Image

        import uag_inventory as inventory


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
                if len(pngs) < 4:
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
                code = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "code")
                if "display_artifact(" not in code:
                    failures.append(f"{notebook.relative_to(BOOK_ROOT)} does not display artifacts")
            duplicates = [paths for paths in all_hashes.values() if len(paths) > 1]
            for paths in duplicates:
                joined = ", ".join(str(path.relative_to(BOOK_ROOT)) for path in paths)
                failures.append(f"duplicate PNG hash: {joined}")
            print(f"Audited visuals for {len(inventory.ENTRIES)} entries.")
            if failures:
                for failure in failures:
                    print(f"FAIL: {failure}")
                raise SystemExit(1)
            print("All visual artifacts are present, nonblank, and uniquely rendered.")


        if __name__ == "__main__":
            main()
        ''',
        "validate_uag_course.py": r'''
        """Execute UAG canonical notebooks with nbclient."""

        from __future__ import annotations

        import argparse
        from pathlib import Path

        import nbformat
        from nbclient import NotebookClient

        import uag_inventory as inventory


        BOOK_ROOT = Path(__file__).resolve().parents[1]


        def notebook_paths(all_notebooks: bool, limit: int | None) -> list[Path]:
            paths = inventory.canonical_notebooks(BOOK_ROOT)
            if all_notebooks:
                return paths
            return paths[: limit or len(paths)]


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
        ''',
    }


def long_markdown(entry: dict[str, object]) -> str:
    concept_sentence = ", ".join(str(c) for c in entry["concepts"])
    visual_sentence = ", ".join(str(v).replace("-", " ") for v in entry["visuals"])
    check_sentence = ", ".join(str(c) for c in entry["checks"])
    detail = DETAILS[int(entry["number"])]
    equation_lines = "\n".join(f"    - `{equation}`" for equation in detail["equations"])
    return f"""
    # Chapter {entry['number']}: {entry['title']}

    Source orientation: printed pages {entry['printed_span']}; physical PDF pages {entry['pdf_span']}; sections {entry['sections']}.

    ## Chapter Question

    This notebook asks how the chapter's main objects become inspectable. The source
    chapter supplies the route and vocabulary, but the lesson here is written as a
    standalone computational exposition. The reader should be able to close the PDF,
    run the cells, and still understand what is being built, which examples matter,
    and which invariants are supposed to survive a change of coordinates, a change of
    equations, or a change of viewpoint. The focus for this chapter is: {entry['focus']}

    Algebraic geometry can feel abstract because it names a space by equations and
    then studies the functions allowed on that space. A visualization-first approach
    reverses the first reaction. Instead of treating the equations as a wall of
    symbols, we treat them as machines that produce zero sets, exceptional loci,
    incidence diagrams, coordinate charts, and algebraic tests. The figures below are
    not decorations. Each one is tied to a specific claim: a parametrization should
    land on the curve, a projective construction should look the same in compatible
    charts, a singular point should reveal itself through a rank drop, or a rational
    map should remember where its denominator is not allowed to vanish.

    ## Translation Guide

    The chapter is organized around these computational lenses: {concept_sentence}.
    Each lens translates a classical sentence into something executable. A locus is a
    contour or a sampled point cloud. A homogeneous coordinate is a line through the
    origin together with affine chart views. A function on a variety is a polynomial
    expression read modulo equations that vanish on the variety. A rational map is a
    formula plus a domain of definition. A theorem about incidence becomes a matrix
    rank, a determinant, a resultant, or a graph whose edges record which geometric
    objects meet.

    One useful habit is to keep two columns in mind. The geometric column contains
    points, curves, surfaces, tangent spaces, lines, charts, and maps. The algebraic
    column contains ideals, quotient rings, homogeneous forms, Jacobians, resultants,
    ranks, and field extensions. The dictionary is contravariant: maps of spaces pull
    functions in the opposite direction. This reversal is not a technical nuisance.
    It is the reason coordinate rings can detect whether a proposed geometric
    construction has an inverse, whether a parametrization has missed information at
    a singular point, and whether an apparent equality of functions is only equality
    after restricting to the variety.

    ## Chapter-Specific Storyboard

    {detail['core']}

    The worked-example spine for this notebook is: {detail['worked']} This is the
    place where the abstract vocabulary becomes a sequence of actions: choose
    coordinates, write the defining expressions, create an inspectable figure, and
    finish with a check that would fail if the geometry had been translated
    incorrectly.

    Equations and constructions to keep on the page:

    {equation_lines}

    The applied lab is: {detail['lab']} The lab is intentionally small enough to run
    quickly, because the goal is repeated experimentation rather than a single
    expensive calculation.

    ## Visual Route

    The generated visual sequence is: {visual_sentence}. The first image gives a
    concept map for the chapter, so the reader can see which claims are connected.
    The second image is an algebraic lens: a zero-locus style view that emphasizes how
    equations cut the plane into regions and how a small parameter change can alter
    shape or interpretation. The third image is a proof-state diagram. It turns the
    proof ingredients into a visible dependency chain, because proof-heavy algebraic
    geometry often becomes clearer when assumptions, transformations, and invariants
    are separated. The fourth image is a dashboard of computational checks. The HTML
    lab then gives an interactive parameter view so that the reader can isolate each
    chapter lens and compare its behavior with the others.

    These visuals deliberately use small models. A small model is not a toy when it
    exposes the same invariant as the general theorem. A conic through five points,
    a cusp parametrized by one variable, an affine chart of projective space, a
    Jacobian matrix at a singular point, or a rank-one matrix from a Segre embedding
    is small enough to compute and still faithful enough to teach the general
    mechanism. The notebook favors these compact laboratories over large black-box
    computations.

    ## Worked Example Pattern

    Every example follows the same pattern. First, name the geometric object. Second,
    write the algebraic data that defines it. Third, draw or tabulate a representation
    that makes the structure visible. Fourth, run a check that would fail if the
    construction were wrong. This pattern matters because many algebraic-geometry
    mistakes are plausible in prose but fragile in computation: forgetting a chart,
    ignoring a denominator, treating a singular parametrization as an isomorphism, or
    counting intersections without multiplicity.

    The checks for this chapter are: {check_sentence}. Some checks are symbolic, such
    as a Groebner remainder, a Hessian, or a homogenization round trip. Others are
    numerical, such as a sampled residual or a nonblank-image assertion. The point is
    not to replace proof with sampling. The point is to give the reader a concrete
    place to see why the proof has the shape it does and to catch errors in the
    computational translation.

    ## Pitfalls

    The most common pitfall is to confuse an ambient object with the object after
    restriction. Two polynomials can be different in the ambient polynomial ring and
    still define the same function on a variety. A formula can look like a map and
    still fail at points where a denominator vanishes. A parametrization can hit every
    point of a curve and still fail to be an isomorphism if the coordinate rings do
    not match. A projective equation can look like an affine equation until the line
    at infinity is checked. The notebook marks these hazards visually because they
    are easier to remember when the missing chart, collapsed tangent, or excluded
    divisor is visible.

    ## Applied Lab

    In the lab cells, change one chapter parameter at a time: use a different sample
    point, alter a coefficient, swap the affine chart, or replace a denominator. Then
    rerun the artifact cell and the sanity checks. A good experiment is one where the
    picture changes but the invariant stays put, or where the invariant fails exactly
    when the hypotheses fail. That is the practical skill this course is training:
    seeing the algebra and the geometry move together.
    """


def takeaways_markdown(entry: dict[str, object]) -> str:
    concepts = "\n".join(f"- `{concept}` is one of the chapter's computational lenses." for concept in entry["concepts"])
    return f"""
    ## Takeaways

    - Chapter {entry['number']} is best read as a dictionary between geometric objects and executable algebraic tests.
    - The artifacts are saved under `artifacts/{entry['artifact']}` and displayed inline so the notebook remains reproducible.
    - The final sanity cell checks that figures, HTML labs, and JSON summaries exist and are nonblank.
    - The notebook is standalone: it uses the source span only as orientation and develops its own prose, examples, and checks.

    {concepts}
    """


def notebook_cells(entry: dict[str, object]) -> list[object]:
    setup_code = """
    from pathlib import Path
    import sys

    here = Path.cwd().resolve()
    candidates = [here, *here.parents]
    BOOK_ROOT = next(path for path in candidates if path.name == "Undergraduate Algebraic Geometry" and (path / "AGENTS.md").exists())
    ARTIFACT_ROOT = BOOK_ROOT / "artifacts"
    if str(BOOK_ROOT) not in sys.path:
        sys.path.insert(0, str(BOOK_ROOT))
    if str(BOOK_ROOT / "scripts") not in sys.path:
        sys.path.insert(0, str(BOOK_ROOT / "scripts"))

    print(f"BOOK_ROOT = {BOOK_ROOT}")
    """
    entry_code = f"""
    import sympy as sp

    from uag_inventory import chapter_by_number
    from utils.artifacts import display_artifact
    from utils.plotting import render_chapter_artifacts
    from utils.validation import validate_chapter_outputs, write_final_sanity

    entry = chapter_by_number({entry['number']})
    chapter_root = ARTIFACT_ROOT / str(entry["artifact"])
    entry["title"], chapter_root
    """
    render_code = """
    paths = render_chapter_artifacts(entry, chapter_root)
    paths["metrics"]
    """
    display_code = """
    display_artifact(paths["figures"][0], width=760)
    display_artifact(paths["figures"][1], width=760)
    display_artifact(paths["figures"][2], width=760)
    display_artifact(paths["figures"][3], width=760)
    """
    html_code = """
    display_artifact(paths["html"][0], height=460)
    display_artifact(paths["tables"][0])
    """
    checks_code = """
    from utils.algebra import groebner_membership, matrix_rank, monomial_basis, radical_toy_summary
    from utils.curves import conic_matrix, classify_conic_matrix, cubic_residual, elliptic_add
    from utils.projective import dehomogenize_polynomial, homogenize_polynomial, rank_one_minors, segre_embed
    from utils.varieties import jacobian_matrix_at, rational_domain_mask, tangent_space_dimension

    x, y, z = sp.symbols("x y z")
    basis = monomial_basis([x, y, z], 2 + int(entry["number"]) % 2)
    F = homogenize_polynomial(x**2 + y - 1, [x, y], z)
    round_trip = sp.expand(dehomogenize_polynomial(F, z) - (x**2 + y - 1))
    membership = groebner_membership(x**2 * y - y, [x**2 - 1], [x, y])
    conic_info = classify_conic_matrix(conic_matrix([1, 0, 1, 0, 0, -1]))
    p = (sp.Integer(0), sp.Integer(1))
    doubled = elliptic_add(p, p, sp.Integer(int(entry["number"]) + 1), sp.Integer(1))
    cubic_check = sp.simplify(cubic_residual(doubled, int(entry["number"]) + 1, 1))
    segre = segre_embed([1, 2], [3, 4])
    minors = rank_one_minors(segre)
    jac = jacobian_matrix_at([x * y, x * z], [x, y, z], {x: 0, y: 1, z: 2})
    tangent_dim = tangent_space_dimension([x * y, x * z], [x, y, z], {x: 0, y: 1, z: 2})
    domain = rational_domain_mask(lambda X, Y: X**2 + Y**2 + 1, __import__("numpy").linspace(-1, 1, 10), __import__("numpy").linspace(-1, 1, 10))

    metrics = {
        "basis_size": len(basis),
        "homogenization_round_trip": str(round_trip),
        "membership_remainder": membership["remainder"],
        "conic_kind": conic_info["kind"],
        "elliptic_double_residual": str(cubic_check),
        "max_rank_one_minor_abs": float(max(abs(v) for v in minors)),
        "jacobian_rank": int(jac.rank()),
        "tangent_dimension": int(tangent_dim),
        "domain_open_samples": int(domain.sum()),
        "radical_toy": radical_toy_summary(x, 3),
    }
    assert round_trip == 0
    assert membership["is_member"] == "True"
    assert cubic_check == 0
    assert metrics["max_rank_one_minor_abs"] == 0.0
    metrics
    """
    sanity_code = """
    summary = validate_chapter_outputs(paths, min_pngs=4)
    final_sanity = write_final_sanity(chapter_root, paths, metrics)
    assert final_sanity.name == "final-sanity.json"
    summary["figures"], summary["html"], final_sanity
    """
    return [
        new_markdown_cell(long_markdown(entry)),
        new_code_cell(dedent(setup_code).strip()),
        new_markdown_cell(
            "## Setup and Route\n\nThe setup cell discovers the book root from the current notebook location, adds the book-local `utils/` and `scripts/` modules to the import path, and keeps all generated outputs inside the book-local artifact tree."
        ),
        new_code_cell(dedent(entry_code).strip()),
        new_markdown_cell(
            "## Generate the Chapter Artifacts\n\nThe renderer below creates durable PNG figures, a lightweight Plotly HTML lab, a concept table, and JSON check data. Rerunning this cell refreshes only this chapter's artifact subtree."
        ),
        new_code_cell(dedent(render_code).strip()),
        new_markdown_cell(
            "## Inspect the Visual Sequence\n\nThe four static figures are deliberately different views of the same chapter: concept graph, algebraic zero-locus lens, proof-state flow, and check dashboard."
        ),
        new_code_cell(dedent(display_code).strip()),
        new_markdown_cell(
            "## Interactive Lab and Concept Table\n\nThe HTML artifact is meant for parameter exploration. The concept table is saved as a simple CSV so later audits can verify that the chapter has a book-local tabular artifact too."
        ),
        new_code_cell(dedent(html_code).strip()),
        new_markdown_cell(
            "## Symbolic and Numeric Sanity Checks\n\nThe checks here are small reusable probes: homogeneous coordinates round trip through an affine chart, ideal membership is tested by a Groebner remainder, a rank-one embedding has vanishing minors, and the chord-tangent addition formula closes on an elliptic curve."
        ),
        new_code_cell(dedent(checks_code).strip()),
        new_code_cell(dedent(sanity_code).strip()),
        new_markdown_cell(takeaways_markdown(entry)),
    ]


def build_indexes_inline() -> None:
    sys.path.insert(0, str(BOOK_ROOT / "scripts"))
    import build_uag_course_indexes

    build_uag_course_indexes.main()


def pre_render_artifacts() -> None:
    sys.path.insert(0, str(BOOK_ROOT))
    from utils.plotting import render_chapter_artifacts

    for entry in ENTRIES:
        render_chapter_artifacts(entry, BOOK_ROOT / "artifacts" / str(entry["artifact"]))


def write_course() -> None:
    write_text(BOOK_ROOT / "AGENTS.md", agents_text())
    write_text(BOOK_ROOT / "scripts" / "uag_inventory.py", inventory_text())
    write_text(BOOK_ROOT / "utils" / "__init__.py", '"""Utilities for the Undergraduate Algebraic Geometry course."""\n')
    write_text(BOOK_ROOT / "utils" / "artifacts.py", artifacts_py())
    write_text(BOOK_ROOT / "utils" / "algebra.py", algebra_py())
    write_text(BOOK_ROOT / "utils" / "projective.py", projective_py())
    write_text(BOOK_ROOT / "utils" / "curves.py", curves_py())
    write_text(BOOK_ROOT / "utils" / "varieties.py", varieties_py())
    write_text(BOOK_ROOT / "utils" / "surfaces.py", surfaces_py())
    write_text(BOOK_ROOT / "utils" / "validation.py", validation_py())
    write_text(BOOK_ROOT / "utils" / "plotting.py", plotting_py())
    for name, text in scripts_texts().items():
        write_text(BOOK_ROOT / "scripts" / name, text)
    for part in PARTS:
        (BOOK_ROOT / str(part["folder"])).mkdir(parents=True, exist_ok=True)
    for entry in ENTRIES:
        chapter_dir = BOOK_ROOT / str(entry["folder"])
        chapter_dir.mkdir(parents=True, exist_ok=True)
        for child in ["figures", "html", "checks", "tables"]:
            (BOOK_ROOT / "artifacts" / str(entry["artifact"]) / child).mkdir(parents=True, exist_ok=True)
        write_notebook(chapter_dir / str(entry["notebook"]), notebook_cells(entry))
    build_indexes_inline()
    pre_render_artifacts()


if __name__ == "__main__":
    write_course()
    print(f"Bootstrapped UAG course at {BOOK_ROOT}")
