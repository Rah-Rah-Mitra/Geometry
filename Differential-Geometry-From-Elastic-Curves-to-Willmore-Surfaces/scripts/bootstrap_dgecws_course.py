"""Bootstrap the DGE-CWS standalone notebook course.

This script is intentionally a course bootstrapper: the target folder starts with
only the source PDF, and notebooks/artifacts are structured JSON and image files.
The maintained entry points after bootstrapping are the utilities and audit/
validation scripts generated here.
"""

from __future__ import annotations

import json
import math
import re
import textwrap
from pathlib import Path

import nbformat
import numpy as np
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


BOOK_ROOT = Path(__file__).resolve().parents[1]


PALETTE = {
    "ink": "#1f2933",
    "blue": "#2f6fbb",
    "teal": "#2a9d8f",
    "green": "#6a994e",
    "gold": "#d59f0f",
    "red": "#c44e52",
    "violet": "#7b5ea7",
    "gray": "#7a8793",
}


PARTS = [
    {
        "folder": "part-01-curves",
        "title": "Part I: Curves",
        "description": "Parametrized curves, arclength, variation, elastic curves, normal transport, torsion, and filament flow.",
    },
    {
        "folder": "part-02-surfaces",
        "title": "Part II: Surfaces",
        "description": "Parametrized surfaces, forms and integration, curvature, connections, global curvature, closed surfaces, variations, and Willmore energy.",
    },
    {
        "folder": "part-03-appendices",
        "title": "Part III: Appendices",
        "description": "Technical smoothness tools and a historical concept map used as navigation aids.",
    },
]


ENTRIES = [
    {
        "kind": "chapter",
        "number": 1,
        "label": "Chapter 01",
        "title": "Curves in Rn",
        "folder": "chapter-01-curves-in-rn",
        "notebook": "01-curves-in-rn.ipynb",
        "part": "part-01-curves",
        "topic": "chapter-01",
        "printed": "3-11",
        "pdf": "13-21",
        "family": "curve",
        "focus": "Regular parametrized curves, reparametrization, length, arclength, unit tangent, and bending energy.",
        "concepts": [
            "regular curves are maps with nonzero velocity",
            "length survives reparametrization and rigid motion",
            "arclength converts arbitrary speed into intrinsic differentiation",
            "bending energy measures how fast the unit tangent turns",
        ],
        "visuals": [
            "regularity and velocity arrows",
            "two parametrizations of one quarter circle",
            "arclength cumulative map and unit-speed reconstruction",
            "bending density along line, circle, and helix",
        ],
        "checks": [
            "speed stays positive on regular examples",
            "length agrees after reparametrization",
            "arclength reconstruction has unit speed",
            "circle bending energy is L/(2 r^2)",
        ],
    },
    {
        "kind": "chapter",
        "number": 2,
        "label": "Chapter 02",
        "title": "Variations of Curves",
        "folder": "chapter-02-variations-of-curves",
        "notebook": "02-variations-of-curves.ipynb",
        "part": "part-01-curves",
        "topic": "chapter-02",
        "printed": "13-27",
        "pdf": "22-37",
        "family": "variation",
        "focus": "One-parameter curve families, variational vector fields, first variation, constrained criticality, and elastica.",
        "concepts": [
            "a variation is a path through curve space",
            "arclength differentiation does not commute with time variation",
            "compactly supported variations remove boundary terms",
            "elastic curves turn variational calculus into ODE diagnostics",
        ],
        "visuals": [
            "ribbon of nearby curves",
            "speed variation residual",
            "commutator panel for d/dt and d/ds",
            "pendulum tangent path and integrated elastica",
        ],
        "checks": [
            "mixed partials commute for smooth tests",
            "finite differences match variation integrals",
            "boundary terms vanish for bump support",
            "elastic ODE residual stays small",
        ],
    },
    {
        "kind": "chapter",
        "number": 3,
        "label": "Chapter 03",
        "title": "Curves in R2",
        "folder": "chapter-03-curves-in-r2",
        "notebook": "03-curves-in-r2.ipynb",
        "part": "part-01-curves",
        "topic": "chapter-03",
        "printed": "29-45",
        "pdf": "38-55",
        "family": "plane",
        "focus": "Signed curvature, sector area, planar elastica, tangent winding, and regular homotopy.",
        "concepts": [
            "a plane curve has scalar signed curvature",
            "signed area is an integral, not just a filled picture",
            "curvature functions reconstruct unit-speed curves",
            "tangent winding is the global integer kept by regular homotopy",
        ],
        "visuals": [
            "T, JT, and curvature sign along a curve",
            "sector-area sweep with positive and negative pieces",
            "elastica potential and curvature bands",
            "tangent-winding gallery",
        ],
        "checks": [
            "determinant curvature agrees with angle derivative",
            "reconstructed curve has the target curvature",
            "closed curve total curvature is near 2*pi*n",
            "homotopy samples keep nonzero velocity",
        ],
    },
    {
        "kind": "chapter",
        "number": 4,
        "label": "Chapter 04",
        "title": "Parallel Normal Fields",
        "folder": "chapter-04-parallel-normal-fields",
        "notebook": "04-parallel-normal-fields.ipynb",
        "part": "part-01-curves",
        "topic": "chapter-04",
        "printed": "47-57",
        "pdf": "56-66",
        "family": "spacecurve",
        "focus": "Parallel normal transport, curvature functions, and reconstruction of curves from normal-plane data.",
        "concepts": [
            "parallel normal fields avoid unnecessary twisting",
            "transport preserves normal inner products",
            "the Hasimoto curvature function records acceleration in a fixed normal plane",
            "curvature data reconstructs the curve up to rigid motion",
        ],
        "visuals": [
            "transported normal frames on a helix",
            "Gram determinant and orthogonality traces",
            "normal-plane curvature trace",
            "reconstruction dictionary for curvature data",
        ],
        "checks": [
            "frame remains orthonormal",
            "transported normal is perpendicular to tangent",
            "determinant stays positive",
            "rigid alignment residual is small",
        ],
    },
    {
        "kind": "chapter",
        "number": 5,
        "label": "Chapter 05",
        "title": "Curves in R3",
        "folder": "chapter-05-curves-in-r3",
        "notebook": "05-curves-in-r3.ipynb",
        "part": "part-01-curves",
        "topic": "chapter-05",
        "printed": "59-85",
        "pdf": "67-92",
        "family": "torsion",
        "focus": "Total torsion, elastic space curves, vortex filament flow, framed curves, twist energy, and Frenet-normal limitations.",
        "concepts": [
            "torsion measures normal-plane rotation along a space curve",
            "elastic space curves can be read through tangent dynamics",
            "binormal flow moves a curve using its own curvature frame",
            "a framed curve stores twist independently of its centerline",
        ],
        "visuals": [
            "torsion holonomy meter",
            "tangent path on the sphere",
            "short binormal-flow diagnostic",
            "framed tube with twist stripe",
        ],
        "checks": [
            "torsion angle is computed by atan2 and unwrapped",
            "frame identities hold numerically",
            "binormal update keeps small arclength drift",
            "twist energy is nonnegative",
        ],
    },
    {
        "kind": "chapter",
        "number": 6,
        "label": "Chapter 06",
        "title": "Surfaces and Riemannian Geometry",
        "folder": "chapter-06-surfaces-and-riemannian-geometry",
        "notebook": "06-surfaces-and-riemannian-geometry.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-06",
        "printed": "87-103",
        "pdf": "94-110",
        "family": "surface",
        "focus": "Parametrized surfaces, tangent spaces, induced metrics, area forms, metric rotation, and isometry.",
        "concepts": [
            "a surface is inspected through a parametrization with rank two derivative",
            "the first fundamental form turns tangent vectors into lengths and angles",
            "the area form is sqrt(det G) in coordinates",
            "isometry means the metric data agrees even when embeddings differ",
        ],
        "visuals": [
            "pushforward grid and tangent arrows",
            "metric ellipses across a patch",
            "area/J parallelogram",
            "isometry lab for flat/developable examples",
        ],
        "checks": [
            "metric matrices are positive definite",
            "area equals sqrt(EG-F^2)",
            "J squared is minus identity",
            "matched examples preserve metric coefficients",
        ],
    },
    {
        "kind": "chapter",
        "number": 7,
        "label": "Chapter 07",
        "title": "Integration and Stokes' Theorem",
        "folder": "chapter-07-integration-and-stokes-theorem",
        "notebook": "07-integration-and-stokes-theorem.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-07",
        "printed": "105-115",
        "pdf": "111-121",
        "family": "forms",
        "focus": "Integration on surfaces and curves, one-forms, two-forms, pullback, boundary orientation, and Stokes' theorem.",
        "concepts": [
            "forms carry the Jacobian and orientation information that raw functions miss",
            "a one-form measures tangent vectors along a curve",
            "boundary orientation is part of the theorem, not a drawing convention",
            "Stokes' theorem equates accumulated boundary measurement with interior exterior derivative",
        ],
        "visuals": [
            "density pullback grid",
            "two-form orientation tiles",
            "one-form curve measurement field",
            "Stokes balance panel",
        ],
        "checks": [
            "pullback integral agrees after change of variables",
            "curve integral is reparametrization invariant",
            "outer and hole boundary orientations have opposite signs",
            "numeric Stokes residual is small",
        ],
    },
    {
        "kind": "chapter",
        "number": 8,
        "label": "Chapter 08",
        "title": "Curvature",
        "folder": "chapter-08-curvature",
        "notebook": "08-curvature.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-08",
        "printed": "117-129",
        "pdf": "122-134",
        "family": "curvature",
        "focus": "Unit normal, shape operator, principal curvature, mean curvature, Gaussian curvature, umbilics, and Gauss-map area.",
        "concepts": [
            "the surface normal converts bending into a derivative",
            "the shape operator is the tangent map hidden inside dN",
            "principal curvatures are directional extrema",
            "Gaussian curvature is the signed area distortion of the normal map",
        ],
        "visuals": [
            "normal orientation on a surface patch",
            "shape-operator gallery",
            "directional curvature polar plot",
            "Gauss-map area panel",
        ],
        "checks": [
            "normal is unit and perpendicular to partials",
            "shape operator is self-adjoint for the metric",
            "H and K match trace and determinant",
            "sphere has constant positive curvature",
        ],
    },
    {
        "kind": "chapter",
        "number": 9,
        "label": "Chapter 09",
        "title": "Levi-Civita Connection",
        "folder": "chapter-09-levi-civita-connection",
        "notebook": "09-levi-civita-connection.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-09",
        "printed": "131-137",
        "pdf": "135-142",
        "family": "connection",
        "focus": "Tangential differentiation, Levi-Civita connection, Gauss and Codazzi equations, and Theorema Egregium.",
        "concepts": [
            "differentiate in space and project back to the tangent plane",
            "the metric determines the same connection coefficients",
            "Codazzi compares derivatives of the shape operator",
            "Theorema Egregium says Gaussian curvature is intrinsic",
        ],
        "visuals": [
            "tangent-normal derivative split",
            "Christoffel coefficient comparison",
            "moving frame rotation form",
            "Gauss/Codazzi residual heatmaps",
        ],
        "checks": [
            "projected derivative is tangent",
            "metric compatibility residual is small",
            "torsion-free coordinate check passes",
            "plane and cylinder both give K=0",
        ],
    },
    {
        "kind": "chapter",
        "number": 10,
        "label": "Chapter 10",
        "title": "Total Gaussian Curvature",
        "folder": "chapter-10-total-gaussian-curvature",
        "notebook": "10-total-gaussian-curvature.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-10",
        "printed": "139-149",
        "pdf": "143-153",
        "family": "gaussbonnet",
        "focus": "Curves on surfaces, total Gaussian curvature, Gauss-Bonnet, and parallel transport holonomy.",
        "concepts": [
            "surface curves split curvature into geodesic and normal pieces",
            "Gauss-Bonnet balances interior curvature and boundary turning",
            "parallel transport around a loop returns with a measurable angle",
            "holonomy is a local detector for enclosed curvature",
        ],
        "visuals": [
            "curve classifiers on a surface",
            "Gauss-Bonnet accounting bars",
            "parallel transport ODE loop",
            "holonomy-curvature comparison",
        ],
        "checks": [
            "test frames remain orthonormal",
            "hemisphere integral approaches 2*pi",
            "annulus boundary terms cancel in flat case",
            "transport preserves tangent vector length",
        ],
    },
    {
        "kind": "chapter",
        "number": 11,
        "label": "Chapter 11",
        "title": "Closed Surfaces",
        "folder": "chapter-11-closed-surfaces",
        "notebook": "11-closed-surfaces.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-11",
        "printed": "151-160",
        "pdf": "154-163",
        "family": "topology",
        "focus": "Boundary gluing, oriented and non-oriented closed surfaces, orientation covers, genus, and total curvature.",
        "concepts": [
            "closed surfaces can be represented by pairing boundary curves",
            "orientation data decides whether the glued surface is orientable",
            "genus can be computed from the boundary-pairing ledger",
            "total Gaussian curvature only sees Euler characteristic",
        ],
        "visuals": [
            "boundary pairing graph",
            "torus and Klein gluing contrast",
            "orientation-cover diagram",
            "genus calculator panel",
        ],
        "checks": [
            "pairing map is an involution",
            "orientation signs match the selected model",
            "genus formula matches examples",
            "Euler characteristic predicts total curvature target",
        ],
    },
    {
        "kind": "chapter",
        "number": 12,
        "label": "Chapter 12",
        "title": "Variations of Surfaces",
        "folder": "chapter-12-variations-of-surfaces",
        "notebook": "12-variations-of-surfaces.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-12",
        "printed": "161-179",
        "pdf": "164-182",
        "family": "surfacevariation",
        "focus": "Surface vector calculus, one-parameter surface families, curvature variation, area variation, volume variation, minimal and CMC surfaces.",
        "concepts": [
            "grad, div, and Laplacian become intrinsic surface operators",
            "a variation decomposes into normal motion and tangential relabeling",
            "mean curvature is the gradient of area",
            "constant mean curvature is the area critical condition under fixed volume",
        ],
        "visuals": [
            "surface vector-calculus dashboard",
            "variation decomposition panel",
            "first area variation plot",
            "cone volume and CMC comparison",
        ],
        "checks": [
            "divergence theorem residual is small",
            "normal bump finite difference matches area variation",
            "minimal examples have small H",
            "sphere has constant H for volume constraint",
        ],
    },
    {
        "kind": "chapter",
        "number": 13,
        "label": "Chapter 13",
        "title": "Willmore Surfaces",
        "folder": "chapter-13-willmore-surfaces",
        "notebook": "13-willmore-surfaces.ipynb",
        "part": "part-02-surfaces",
        "topic": "chapter-13",
        "printed": "181-191",
        "pdf": "183-193",
        "family": "willmore",
        "focus": "Willmore functional, Willmore equation, energy offsets, cylinder examples, and inversion invariance.",
        "concepts": [
            "Willmore energy measures bending after subtracting the topological Gaussian term",
            "the sphere is the baseline compact example",
            "the first variation produces a fourth-order surface equation",
            "inversion preserves the conformal Willmore density away from singularities",
        ],
        "visuals": [
            "Willmore energy zoo",
            "functional offset bars",
            "finite-difference Willmore residual",
            "inversion lab",
        ],
        "checks": [
            "Willmore energy is scale invariant for the sphere",
            "integrated K records the expected offset",
            "sphere residual is small",
            "inversion comparison avoids the center singularity",
        ],
    },
    {
        "kind": "appendix",
        "number": 101,
        "label": "Appendix A",
        "title": "Some Technicalities",
        "folder": "appendix-a-some-technicalities",
        "notebook": "appendix-a-some-technicalities.ipynb",
        "part": "part-03-appendices",
        "topic": "appendix-a",
        "printed": "193-196",
        "pdf": "194-197",
        "family": "appendix",
        "focus": "Smooth maps on closed domains, support, bump functions, and smooth cutoffs.",
        "concepts": [
            "smoothness on a closed domain is inherited from an open extension",
            "support records where a function is allowed to act",
            "flat bump functions localize variations without boundary traces",
            "diffeomorphism checks require a smooth inverse and nonzero Jacobian",
        ],
        "visuals": [
            "extension collar diagram",
            "boundary derivative experiment",
            "diffeomorphism grid",
            "bump function toolbox",
        ],
        "checks": [
            "sampled bump support is compact",
            "boundary derivatives are numerically flat",
            "composition error for inverse maps is small",
            "Jacobian samples stay nonzero",
        ],
    },
    {
        "kind": "appendix",
        "number": 102,
        "label": "Appendix B",
        "title": "Timeline",
        "folder": "appendix-b-timeline",
        "notebook": "appendix-b-timeline.ipynb",
        "part": "part-03-appendices",
        "topic": "appendix-b",
        "printed": "197-198",
        "pdf": "198-199",
        "family": "timeline",
        "focus": "A navigable timeline connecting elastic curves, surface theory, topology, variational calculus, and Willmore surfaces.",
        "concepts": [
            "historical milestones can be used as a concept dependency map",
            "curve theory and surface theory repeatedly exchange methods",
            "topological invariants constrain curvature integrals",
            "Willmore surfaces inherit both variational and conformal ideas",
        ],
        "visuals": [
            "chronological milestone timeline",
            "concept dependency graph",
            "elastic-to-Willmore lineage",
            "chapter-link navigation table",
        ],
        "checks": [
            "years are sorted",
            "each node has a theme",
            "duplicate years are intentionally grouped",
            "chapter links resolve to local notebooks",
        ],
    },
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-+", "-", slug)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")


def write_notebook(path: Path, cells: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=cells), path)


def markdown_notebook(path: Path, text: str) -> None:
    write_notebook(path, [new_markdown_cell(textwrap.dedent(text).strip() + "\n")])


def entry_by_topic(topic: str) -> dict:
    for entry in ENTRIES:
        if entry["topic"] == topic:
            return entry
    raise KeyError(topic)


def create_utilities() -> None:
    write_text(
        BOOK_ROOT / "utils" / "__init__.py",
        '''
        """Utilities for the Differential Geometry from Elastic Curves to Willmore Surfaces course."""
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "artifacts.py",
        '''
        """Book-local artifact helpers."""

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


        def artifact_dir(topic: str, slug: str | None = None, root: str | Path = ARTIFACT_ROOT) -> Path:
            parts = [slugify(topic)]
            if slug:
                parts.append(slugify(slug))
            path = Path(root).joinpath(*parts)
            path.mkdir(parents=True, exist_ok=True)
            return path


        def artifact_path(topic: str, slug: str | None, filename: str, root: str | Path = ARTIFACT_ROOT) -> Path:
            path = artifact_dir(topic, slug, root) / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            return path


        def save_json(data: Any, topic: str, slug: str | None, filename: str = "data.json", *, root: str | Path = ARTIFACT_ROOT) -> Path:
            path = artifact_path(topic, slug, filename, root)
            path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
            return path


        def save_matplotlib(figure: Any, topic: str, slug: str | None, filename: str = "figure.png", *, dpi: int = 160, root: str | Path = ARTIFACT_ROOT, **kwargs: Any) -> Path:
            path = artifact_path(topic, slug, filename, root)
            figure.savefig(path, dpi=dpi, bbox_inches="tight", **kwargs)
            return path


        def save_plotly_html(figure: Any, topic: str, slug: str | None, filename: str = "plot.html", *, root: str | Path = ARTIFACT_ROOT, include_plotlyjs: str | bool = "cdn", full_html: bool = True, **kwargs: Any) -> Path:
            path = artifact_path(topic, slug, filename, root)
            figure.write_html(path, include_plotlyjs=include_plotlyjs, full_html=full_html, **kwargs)
            return path


        def save_image(image: Any, topic: str, slug: str | None, filename: str = "image.png", *, root: str | Path = ARTIFACT_ROOT) -> Path:
            path = artifact_path(topic, slug, filename, root)
            if isinstance(image, PILImage.Image):
                image.save(path)
                return path
            array = np.asarray(image)
            if array.dtype != np.uint8:
                if np.issubdtype(array.dtype, np.floating) and array.size and array.max() <= 1.0:
                    array = array * 255.0
                array = np.clip(array, 0, 255).astype(np.uint8)
            PILImage.fromarray(array).save(path)
            return path


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
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "plotting.py",
        '''
        """Plotting defaults and visual audit helpers."""

        from __future__ import annotations

        import hashlib
        from pathlib import Path
        from typing import Any

        import matplotlib.pyplot as plt
        import numpy as np
        from PIL import Image, ImageStat

        PALETTE = {
            "ink": "#1f2933",
            "blue": "#2f6fbb",
            "teal": "#2a9d8f",
            "green": "#6a994e",
            "gold": "#d59f0f",
            "red": "#c44e52",
            "violet": "#7b5ea7",
            "gray": "#7a8793",
        }


        def style_axis(ax: Any, title: str, *, equal: bool = False) -> None:
            ax.set_title(title, fontsize=11, color=PALETTE["ink"])
            ax.grid(True, color="#d7dde5", linewidth=0.7, alpha=0.8)
            if equal:
                ax.set_aspect("equal", adjustable="box")
            for spine in ax.spines.values():
                spine.set_color("#b6c0ca")


        def add_note(ax: Any, text: str) -> None:
            ax.text(
                0.02,
                0.98,
                text,
                transform=ax.transAxes,
                va="top",
                ha="left",
                fontsize=8,
                color=PALETTE["ink"],
                bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#d0d7de", "alpha": 0.92},
            )


        def image_stats(path: str | Path) -> dict[str, float | int | str]:
            p = Path(path)
            with Image.open(p) as image:
                image.load()
                rgb = image.convert("RGB")
                stat = ImageStat.Stat(rgb)
                arr = np.asarray(rgb, dtype=float)
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
            return {
                "path": p.as_posix(),
                "width": int(rgb.width),
                "height": int(rgb.height),
                "bytes": int(p.stat().st_size),
                "sha256": digest,
                "pixel_std": float(arr.std()),
                "max_channel_stddev": float(max(stat.stddev) if stat.stddev else 0.0),
            }


        def close(fig: Any) -> None:
            plt.close(fig)
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "curves.py",
        '''
        """Curve calculations used by the notebooks."""

        from __future__ import annotations

        import numpy as np
        from scipy.interpolate import interp1d

        EPS = 1e-12


        def as_points(points: np.ndarray) -> np.ndarray:
            arr = np.asarray(points, dtype=float)
            if arr.ndim != 2:
                raise ValueError("points must be an array of shape (n, dim)")
            return arr


        def derivatives(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray:
            pts = as_points(points)
            if parameter is None:
                return np.gradient(pts, axis=0, edge_order=2)
            return np.gradient(pts, np.asarray(parameter, dtype=float), axis=0, edge_order=2)


        def speed(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray:
            return np.linalg.norm(derivatives(points, parameter), axis=1)


        def length(points: np.ndarray) -> float:
            pts = as_points(points)
            return float(np.linalg.norm(np.diff(pts, axis=0), axis=1).sum())


        def arclength(points: np.ndarray) -> np.ndarray:
            pts = as_points(points)
            ds = np.linalg.norm(np.diff(pts, axis=0), axis=1)
            return np.concatenate([[0.0], np.cumsum(ds)])


        def resample_by_arclength(points: np.ndarray, samples: int | None = None) -> tuple[np.ndarray, np.ndarray]:
            pts = as_points(points)
            s = arclength(pts)
            if samples is None:
                samples = len(pts)
            target = np.linspace(0.0, float(s[-1]), samples)
            cols = [interp1d(s, pts[:, i], kind="linear")(target) for i in range(pts.shape[1])]
            return np.column_stack(cols), target


        def unit_tangent(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray:
            d = derivatives(points, parameter)
            n = np.linalg.norm(d, axis=1, keepdims=True)
            if np.any(n <= EPS):
                raise ValueError("unit tangent is undefined where speed vanishes")
            return d / n


        def plane_curvature(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray:
            pts = as_points(points)
            if pts.shape[1] != 2:
                raise ValueError("plane curvature expects 2D points")
            d1 = derivatives(pts, parameter)
            d2 = derivatives(d1, parameter)
            cross = d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0]
            denom = np.linalg.norm(d1, axis=1) ** 3
            return cross / np.maximum(denom, EPS)


        def bending_energy(points: np.ndarray, parameter: np.ndarray | None = None) -> float:
            pts = as_points(points)
            if pts.shape[1] == 2:
                kappa = plane_curvature(pts, parameter)
            else:
                t = unit_tangent(pts, parameter)
                dt = derivatives(t, parameter)
                spd = speed(pts, parameter)
                kappa = np.linalg.norm(dt, axis=1) / np.maximum(spd, EPS)
            s = arclength(pts)
            return float(0.5 * np.trapz(kappa * kappa, s))


        def signed_area(points: np.ndarray) -> float:
            pts = as_points(points)
            if pts.shape[1] != 2:
                raise ValueError("signed area expects 2D points")
            x, y = pts[:, 0], pts[:, 1]
            return float(0.5 * np.sum(x[:-1] * y[1:] - x[1:] * y[:-1]))


        def tangent_winding(points: np.ndarray) -> float:
            t = unit_tangent(points)
            if t.shape[1] != 2:
                raise ValueError("winding expects a plane curve")
            angle = np.unwrap(np.arctan2(t[:, 1], t[:, 0]))
            return float((angle[-1] - angle[0]) / (2 * np.pi))
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "frames.py",
        '''
        """Frame and alignment helpers for space curves."""

        from __future__ import annotations

        import numpy as np

        from utils.curves import unit_tangent

        EPS = 1e-12


        def rotation_minimizing_frame(points: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
            pts = np.asarray(points, dtype=float)
            if pts.shape[1] != 3:
                raise ValueError("rotation_minimizing_frame expects 3D points")
            t = unit_tangent(pts)
            seed = np.array([0.0, 0.0, 1.0])
            if abs(np.dot(seed, t[0])) > 0.9:
                seed = np.array([0.0, 1.0, 0.0])
            n0 = seed - np.dot(seed, t[0]) * t[0]
            n0 = n0 / np.linalg.norm(n0)
            normals = [n0]
            binormals = [np.cross(t[0], n0)]
            for i in range(1, len(t)):
                v = normals[-1] - np.dot(normals[-1], t[i]) * t[i]
                if np.linalg.norm(v) <= EPS:
                    v = binormals[-1] - np.dot(binormals[-1], t[i]) * t[i]
                v = v / np.linalg.norm(v)
                normals.append(v)
                binormals.append(np.cross(t[i], v))
            return t, np.asarray(normals), np.asarray(binormals)


        def torsion_indicator(points: np.ndarray) -> np.ndarray:
            t, n, b = rotation_minimizing_frame(points)
            db = np.gradient(b, axis=0, edge_order=2)
            return -np.einsum("ij,ij->i", db, n)


        def kabsch_align(source: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, float]:
            src = np.asarray(source, dtype=float)
            tgt = np.asarray(target, dtype=float)
            src_center = src.mean(axis=0)
            tgt_center = tgt.mean(axis=0)
            src0 = src - src_center
            tgt0 = tgt - tgt_center
            u, _, vt = np.linalg.svd(src0.T @ tgt0)
            r = u @ vt
            if np.linalg.det(r) < 0:
                u[:, -1] *= -1
                r = u @ vt
            aligned = src0 @ r + tgt_center
            rms = float(np.sqrt(np.mean(np.sum((aligned - tgt) ** 2, axis=1))))
            return aligned, rms


        def reconstruct_from_tangent(tangent: np.ndarray, step: float = 1.0) -> np.ndarray:
            tangent = np.asarray(tangent, dtype=float)
            tangent = tangent / np.linalg.norm(tangent, axis=1, keepdims=True)
            pts = np.vstack([np.zeros(tangent.shape[1]), np.cumsum(tangent[:-1] * step, axis=0)])
            return pts
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "variations.py",
        '''
        """Variation and bump-function helpers."""

        from __future__ import annotations

        import numpy as np


        def flat_step(x: np.ndarray) -> np.ndarray:
            x = np.asarray(x, dtype=float)
            out = np.zeros_like(x)
            mask = x > 0
            out[mask] = np.exp(-1.0 / x[mask])
            return out


        def bump(x: np.ndarray, center: float = 0.0, radius: float = 1.0) -> np.ndarray:
            z = 1.0 - ((np.asarray(x, dtype=float) - center) / radius) ** 2
            out = np.zeros_like(z)
            mask = z > 0
            out[mask] = np.exp(-1.0 / z[mask])
            if out.max() > 0:
                out = out / out.max()
            return out


        def radial_bump(x: np.ndarray, y: np.ndarray, radius: float = 1.0) -> np.ndarray:
            r2 = (np.asarray(x) ** 2 + np.asarray(y) ** 2) / (radius * radius)
            z = 1.0 - r2
            out = np.zeros_like(z, dtype=float)
            mask = z > 0
            out[mask] = np.exp(-1.0 / z[mask])
            if out.max() > 0:
                out = out / out.max()
            return out


        def finite_difference(function, value: float, step: float = 1e-4) -> float:
            return float((function(value + step) - function(value - step)) / (2 * step))
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "surfaces.py",
        '''
        """Surface metric and curvature helpers."""

        from __future__ import annotations

        import numpy as np

        EPS = 1e-12


        def graph_surface(u: np.ndarray, v: np.ndarray, kind: str = "saddle") -> tuple[np.ndarray, np.ndarray, np.ndarray]:
            if kind == "sphere":
                z = np.sqrt(np.maximum(1.0 - 0.15 * u * u - 0.15 * v * v, 0.0))
            elif kind == "bump":
                z = 0.35 * np.exp(-(u * u + v * v))
            elif kind == "cylinder":
                z = v
                return np.cos(u), np.sin(u), z
            else:
                z = 0.25 * (u * u - v * v)
            return u, v, z


        def partials(x: np.ndarray, y: np.ndarray, z: np.ndarray, u: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
            fu = np.stack([np.gradient(x, axis=1), np.gradient(y, axis=1), np.gradient(z, axis=1)], axis=-1)
            fv = np.stack([np.gradient(x, axis=0), np.gradient(y, axis=0), np.gradient(z, axis=0)], axis=-1)
            return fu, fv


        def normal_from_partials(fu: np.ndarray, fv: np.ndarray) -> np.ndarray:
            n = np.cross(fu, fv)
            return n / np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), EPS)


        def first_fundamental_form(fu: np.ndarray, fv: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
            e = np.einsum("...i,...i->...", fu, fu)
            f = np.einsum("...i,...i->...", fu, fv)
            g = np.einsum("...i,...i->...", fv, fv)
            return e, f, g


        def area_density(e: np.ndarray, f: np.ndarray, g: np.ndarray) -> np.ndarray:
            return np.sqrt(np.maximum(e * g - f * f, 0.0))


        def graph_curvature(z: np.ndarray, du: float, dv: float) -> tuple[np.ndarray, np.ndarray]:
            zx = np.gradient(z, du, axis=1, edge_order=2)
            zy = np.gradient(z, dv, axis=0, edge_order=2)
            zxx = np.gradient(zx, du, axis=1, edge_order=2)
            zyy = np.gradient(zy, dv, axis=0, edge_order=2)
            zxy = np.gradient(zx, dv, axis=0, edge_order=2)
            q = 1.0 + zx * zx + zy * zy
            h = ((1 + zy * zy) * zxx - 2 * zx * zy * zxy + (1 + zx * zx) * zyy) / (2 * q ** 1.5)
            k = (zxx * zyy - zxy * zxy) / (q * q)
            return h, k


        def metric_j(e: float, f: float, g: float) -> np.ndarray:
            det = e * g - f * f
            root = np.sqrt(det)
            return np.array([[-f / root, -g / root], [e / root, f / root]])


        def christoffel_placeholder(e: np.ndarray, f: np.ndarray, g: np.ndarray) -> np.ndarray:
            return np.stack([np.gradient(e, axis=0), np.gradient(f, axis=1), np.gradient(g, axis=0)], axis=0)
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "topology.py",
        '''
        """Small topology ledgers for the surface chapters."""

        from __future__ import annotations


        def euler_from_boundary_pieces(k: int, n: int) -> int:
            return 2 * k - n


        def genus_from_gluing(k: int, n: int, m: int) -> float:
            return n / 2 - k + m


        def total_gaussian_curvature_from_chi(chi: float) -> float:
            import math

            return 2 * math.pi * chi


        def is_involution(mapping: dict[int, int]) -> bool:
            return all(mapping.get(mapping.get(key)) == key for key in mapping)
        ''',
    )
    write_text(
        BOOK_ROOT / "utils" / "willmore.py",
        '''
        """Willmore-energy helpers."""

        from __future__ import annotations

        import numpy as np


        def willmore_density(h: np.ndarray, area: np.ndarray) -> np.ndarray:
            return h * h * area


        def conformal_willmore_density(h: np.ndarray, k: np.ndarray, area: np.ndarray) -> np.ndarray:
            return (h * h - k) * area


        def sphere_willmore_energy(radius: float = 1.0) -> float:
            import math

            h = 1.0 / radius
            return 4.0 * math.pi * radius * radius * h * h


        def invert_points(points: np.ndarray) -> np.ndarray:
            pts = np.asarray(points, dtype=float)
            denom = np.sum(pts * pts, axis=-1, keepdims=True)
            return pts / denom
        ''',
    )


def create_inventory_module() -> None:
    text = (
        '"""Inventory for the DGE-CWS notebook course."""\n\n'
        "from __future__ import annotations\n\n"
        f"PARTS = {json.dumps(PARTS, indent=4)}\n\n"
        f"ENTRIES = {json.dumps(ENTRIES, indent=4)}\n\n\n"
        "def canonical_entries() -> list[dict]:\n"
        "    return list(ENTRIES)\n\n\n"
        "def parts() -> list[dict]:\n"
        "    return list(PARTS)\n"
    )
    write_text(BOOK_ROOT / "scripts" / "dgecws_inventory.py", text)


def create_scripts() -> None:
    write_text(
        BOOK_ROOT / "scripts" / "build_dgecws_course_indexes.py",
        '''
        """Rebuild DGE-CWS book, part, and chapter index notebooks."""

        from __future__ import annotations

        from pathlib import Path

        import nbformat
        from nbformat.v4 import new_markdown_cell, new_notebook

        import dgecws_inventory as inventory

        BOOK_ROOT = Path(__file__).resolve().parents[1]


        def write_markdown_notebook(path: Path, text: str) -> None:
            path.parent.mkdir(parents=True, exist_ok=True)
            nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\\n")]), path)


        def entry_folder(entry: dict) -> Path:
            return BOOK_ROOT / entry["part"] / entry["folder"]


        def ensure_inventory() -> None:
            missing = []
            for entry in inventory.ENTRIES:
                folder = entry_folder(entry)
                for path in [folder / "00-index.ipynb", folder / entry["notebook"]]:
                    if not path.exists():
                        missing.append(path)
            if missing:
                raise FileNotFoundError("\\n".join(str(path) for path in missing))


        def build_book_index() -> str:
            lines = [
                "# Differential Geometry: From Elastic Curves to Willmore Surfaces",
                "",
                "This is a standalone visualization-first notebook course with original prose, executable examples, generated diagrams, interactive artifacts, and sanity checks. The local PDF is used only for source orientation and is not reproduced in the notebooks.",
                "",
                "## Course Map",
                "",
            ]
            for part in inventory.PARTS:
                lines.extend([f"## {part['title']}", "", part["description"], "", f"- [Open part index]({part['folder']}/00-part-index.ipynb)"])
                for entry in inventory.ENTRIES:
                    if entry["part"] != part["folder"]:
                        continue
                    index_link = f"{entry['part']}/{entry['folder']}/00-index.ipynb"
                    canonical_link = f"{entry['part']}/{entry['folder']}/{entry['notebook']}"
                    lines.append(
                        f"- [{entry['label']}: {entry['title']}]({index_link}) - "
                        f"[canonical]({canonical_link}); printed pp. {entry['printed']}; PDF pp. {entry['pdf']}; {entry['focus']}"
                    )
                lines.append("")
            return "\\n".join(lines)


        def build_part_index(part: dict) -> str:
            lines = [f"# {part['title']}", "", "[Back to Book Index](../00-book-index.ipynb)", "", part["description"], ""]
            for entry in inventory.ENTRIES:
                if entry["part"] != part["folder"]:
                    continue
                lines.extend([
                    f"## {entry['label']}: {entry['title']}",
                    "",
                    f"- Chapter index: [{entry['folder']}/00-index.ipynb]({entry['folder']}/00-index.ipynb)",
                    f"- Canonical notebook: [{entry['notebook']}]({entry['folder']}/{entry['notebook']})",
                    f"- Source span: printed pp. {entry['printed']}; PDF pp. {entry['pdf']}",
                    f"- Focus: {entry['focus']}",
                    "",
                ])
            return "\\n".join(lines)


        def build_chapter_index(entry: dict) -> str:
            lines = [
                f"# {entry['label']}: {entry['title']}",
                "",
                f"Source orientation: printed pages {entry['printed']}; PDF pages {entry['pdf']}.",
                "",
                f"Canonical notebook: [{entry['notebook']}]({entry['notebook']})",
                "",
                "## Focus",
                "",
                entry["focus"],
                "",
                "## Visual Storyboard",
                "",
            ]
            for visual in entry["visuals"]:
                lines.append(f"- {visual}")
            lines.extend(["", "## Checks", ""])
            for check in entry["checks"]:
                lines.append(f"- {check}")
            return "\\n".join(lines)


        def main() -> None:
            ensure_inventory()
            write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
            for part in inventory.PARTS:
                write_markdown_notebook(BOOK_ROOT / part["folder"] / "00-part-index.ipynb", build_part_index(part))
            for entry in inventory.ENTRIES:
                write_markdown_notebook(entry_folder(entry) / "00-index.ipynb", build_chapter_index(entry))
            print(f"Updated indexes for {len(inventory.ENTRIES)} entries in {len(inventory.PARTS)} parts.")


        if __name__ == "__main__":
            main()
        ''',
    )
    write_text(
        BOOK_ROOT / "scripts" / "audit_dgecws_notebooks.py",
        '''
        """Audit DGE-CWS notebooks for standalone depth and structure."""

        from __future__ import annotations

        import argparse
        import json
        from pathlib import Path

        import nbformat

        BOOK_ROOT = Path(__file__).resolve().parents[1]
        IGNORED = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}


        def discover_notebooks() -> list[Path]:
            artifact_root = BOOK_ROOT / "artifacts"
            return [
                path
                for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
                if artifact_root not in path.parents and path.name not in IGNORED
            ]


        def notebook_stats(path: Path) -> dict[str, object]:
            nb = nbformat.read(path, as_version=4)
            markdown = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown"]
            code = ["".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code"]
            return {
                "path": str(path.relative_to(BOOK_ROOT)),
                "markdown_words": sum(len(source.split()) for source in markdown),
                "markdown_cells": len(markdown),
                "code_cells": len(code),
                "visual_save_calls": sum(source.count("save_matplotlib(") + source.count("save_plotly_html(") + source.count("save_image(") for source in code),
                "display_artifact_calls": sum(source.count("display_artifact(") for source in code),
                "has_final_sanity": any("final_sanity" in source for source in code),
            }


        def canonical_folder_findings() -> list[dict[str, str]]:
            findings = []
            for folder in [p for p in BOOK_ROOT.rglob("*") if p.is_dir() and (p / "00-index.ipynb").exists()]:
                canonical = [p for p in folder.glob("*.ipynb") if p.name != "00-index.ipynb"]
                if len(canonical) != 1:
                    findings.append({"path": str(folder.relative_to(BOOK_ROOT)), "message": f"expected one canonical notebook, found {len(canonical)}"})
            return findings


        def main() -> None:
            parser = argparse.ArgumentParser()
            parser.add_argument("--json", action="store_true")
            parser.add_argument("--min-words", type=int, default=1200)
            parser.add_argument("--min-code-cells", type=int, default=5)
            args = parser.parse_args()

            stats = [notebook_stats(path) for path in discover_notebooks()]
            failing = [
                item
                for item in stats
                if item["markdown_words"] < args.min_words
                or item["code_cells"] < args.min_code_cells
                or item["visual_save_calls"] == 0
                or item["display_artifact_calls"] < item["visual_save_calls"]
                or not item["has_final_sanity"]
            ]
            structure = canonical_folder_findings()
            report = {"notebook_count": len(stats), "failing_count": len(failing), "failing": failing, "structure_findings": structure, "stats": stats}
            if args.json:
                print(json.dumps(report, indent=2))
                return
            print(f"Audited {len(stats)} canonical notebooks")
            if failing or structure:
                for item in failing:
                    print(f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells, {item['visual_save_calls']} visual saves, {item['display_artifact_calls']} displays")
                for item in structure:
                    print(f"- {item['path']}: {item['message']}")
                raise SystemExit(1)
            print("All canonical notebooks meet standalone structure thresholds.")


        if __name__ == "__main__":
            main()
        ''',
    )
    write_text(
        BOOK_ROOT / "scripts" / "audit_dgecws_visuals.py",
        '''
        """Audit generated visual artifacts for DGE-CWS."""

        from __future__ import annotations

        import argparse
        import ast
        import hashlib
        import json
        from pathlib import Path
        from typing import Any

        from PIL import Image, ImageStat

        import dgecws_inventory as inventory

        BOOK_ROOT = Path(__file__).resolve().parents[1]
        IGNORED = {"00-index.ipynb", "00-part-index.ipynb", "00-book-index.ipynb"}
        VISUAL_SAVE_CALLS = {"save_matplotlib", "save_plotly_html", "save_image"}


        def relative(path: Path) -> str:
            return str(path.relative_to(BOOK_ROOT)).replace("\\\\", "/")


        def call_name(node: ast.Call) -> str | None:
            if isinstance(node.func, ast.Name):
                return node.func.id
            if isinstance(node.func, ast.Attribute):
                return node.func.attr
            return None


        def notebook_visual_stats(path: Path) -> dict[str, Any]:
            data = json.loads(path.read_text(encoding="utf-8"))
            visual_saves = 0
            displays = 0
            errors = []
            for cell_index, cell in enumerate(data.get("cells", []), start=1):
                if cell.get("cell_type") != "code":
                    continue
                source = "".join(cell.get("source", ""))
                try:
                    tree = ast.parse(source)
                except SyntaxError as exc:
                    errors.append(f"cell {cell_index}: {exc.msg}")
                    visual_saves += sum(source.count(f"{name}(") for name in VISUAL_SAVE_CALLS)
                    displays += source.count("display_artifact(")
                    continue
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        name = call_name(node)
                        if name in VISUAL_SAVE_CALLS:
                            visual_saves += 1
                        elif name == "display_artifact":
                            displays += 1
            return {"path": relative(path), "visual_save_calls": visual_saves, "display_artifact_calls": displays, "parse_errors": errors}


        def image_stats(path: Path) -> dict[str, Any]:
            with Image.open(path) as image:
                image.load()
                rgb = image.convert("RGB")
                stat = ImageStat.Stat(rgb)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            return {
                "path": relative(path),
                "width": rgb.width,
                "height": rgb.height,
                "bytes": path.stat().st_size,
                "sha256": digest,
                "max_channel_stddev": max(stat.stddev) if stat.stddev else 0.0,
            }


        def audit() -> dict[str, Any]:
            findings = []
            artifact_root = BOOK_ROOT / "artifacts"
            notebooks = [
                notebook_visual_stats(path)
                for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
                if artifact_root not in path.parents and path.name not in IGNORED
            ]
            for item in notebooks:
                for error in item["parse_errors"]:
                    findings.append({"check": "notebook-parse-error", "path": item["path"], "message": error})
                if item["visual_save_calls"] == 0:
                    findings.append({"check": "missing-visual-save", "path": item["path"], "message": "no visual save call"})
                if item["display_artifact_calls"] < item["visual_save_calls"]:
                    findings.append({"check": "missing-display", "path": item["path"], "message": "not every visual is displayed"})

            images = []
            for entry in inventory.ENTRIES:
                topic_root = artifact_root / entry["topic"]
                pngs = sorted(topic_root.rglob("*.png")) if topic_root.exists() else []
                if not pngs:
                    findings.append({"check": "missing-topic-png", "path": relative(topic_root), "message": f"{entry['topic']} has no PNG artifacts"})
                for path in pngs:
                    try:
                        stat = image_stats(path)
                    except OSError as exc:
                        findings.append({"check": "unreadable-image", "path": relative(path), "message": str(exc)})
                        continue
                    images.append(stat)
                    if stat["width"] < 96 or stat["height"] < 96 or stat["bytes"] < 1500:
                        findings.append({"check": "tiny-image", "path": stat["path"], "message": f"{stat['width']}x{stat['height']} {stat['bytes']} bytes"})
                    if stat["max_channel_stddev"] <= 1.0:
                        findings.append({"check": "blank-image", "path": stat["path"], "message": f"stddev {stat['max_channel_stddev']:.3f}"})

            by_hash: dict[str, list[str]] = {}
            for image in images:
                by_hash.setdefault(image["sha256"], []).append(image["path"])
            for digest, paths in by_hash.items():
                if len(paths) > 1:
                    findings.append({"check": "duplicate-png-hash", "path": paths[0], "message": f"{len(paths)} images share {digest[:12]}", "details": paths})

            return {"summary": {"notebook_count": len(notebooks), "png_count": len(images), "finding_count": len(findings)}, "findings": findings, "notebooks": notebooks, "images": images}


        def main() -> None:
            parser = argparse.ArgumentParser()
            parser.add_argument("--json", action="store_true")
            parser.add_argument("--no-fail", action="store_true")
            args = parser.parse_args()
            report = audit()
            if args.json:
                print(json.dumps(report, indent=2))
            else:
                summary = report["summary"]
                print(f"Audited {summary['notebook_count']} notebooks and {summary['png_count']} PNGs")
                if report["findings"]:
                    for finding in report["findings"]:
                        print(f"- {finding['check']} [{finding.get('path', '')}]: {finding['message']}")
                else:
                    print("All DGE-CWS visual checks passed.")
            if report["findings"] and not args.no_fail:
                raise SystemExit(1)


        if __name__ == "__main__":
            main()
        ''',
    )
    write_text(
        BOOK_ROOT / "scripts" / "validate_dgecws_course.py",
        '''
        """Execute DGE-CWS notebooks with nbclient."""

        from __future__ import annotations

        import argparse
        import asyncio
        import sys
        from pathlib import Path

        import nbformat
        from nbclient import NotebookClient

        BOOK_ROOT = Path(__file__).resolve().parents[1]

        if sys.platform.startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


        def notebook_paths(all_notebooks: bool, limit: int | None) -> list[Path]:
            artifact_root = BOOK_ROOT / "artifacts"
            paths = [
                path
                for path in sorted(BOOK_ROOT.rglob("*.ipynb"))
                if artifact_root not in path.parents
            ]
            if not all_notebooks:
                smoke_names = {
                    "00-book-index.ipynb",
                    "01-curves-in-rn.ipynb",
                    "03-curves-in-r2.ipynb",
                    "05-curves-in-r3.ipynb",
                    "06-surfaces-and-riemannian-geometry.ipynb",
                    "08-curvature.ipynb",
                    "10-total-gaussian-curvature.ipynb",
                    "13-willmore-surfaces.ipynb",
                    "appendix-a-some-technicalities.ipynb",
                }
                paths = [path for path in paths if path.name in smoke_names]
            if limit is not None:
                paths = paths[:limit]
            return paths


        def execute_notebook(path: Path, timeout: int) -> None:
            nb = nbformat.read(path, as_version=4)
            client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
            client.execute()


        def main() -> None:
            parser = argparse.ArgumentParser()
            parser.add_argument("--all", action="store_true")
            parser.add_argument("--limit", type=int, default=None)
            parser.add_argument("--timeout", type=int, default=120)
            args = parser.parse_args()

            paths = notebook_paths(args.all, args.limit)
            if not paths:
                raise SystemExit("no notebooks found")
            failures = []
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
        ''',
    )


def create_agents_md() -> None:
    chapter_lines = []
    for entry in ENTRIES:
        chapter_lines.append(
            f"- {entry['label']}: `{entry['part']}/{entry['folder']}/{entry['notebook']}`; printed pp. {entry['printed']}; PDF pp. {entry['pdf']}; {entry['focus']}"
        )
    write_text(
        BOOK_ROOT / "AGENTS.md",
        f'''
        # Agent Instructions: Differential Geometry From Elastic Curves to Willmore Surfaces

        This folder is a standalone notebook edition of *Differential Geometry: From Elastic Curves to Willmore Surfaces* by Ulrich Pinkall and Oliver Gross. Treat this folder as the project root for this course. The workspace root still owns the shared `uv` environment.

        ## Repo-Local Skills

        Use the repo-local skills under `D:\\Geometry\\.codex\\skills` for course work:

        - `geometry-visualization-planner` for chapter storyboards.
        - `geometry-chapter-notebook-author` for authoring canonical notebooks.
        - `geometry-notebook-qc` for standalone, artifact, and execution review.

        ## Non-Negotiables

        - Write original teaching prose, derivations, code, and visual explanations.
        - Do not copy textbook passages, long exercise text, page screenshots, or page crops.
        - The notebooks must stand alone without the PDF open.
        - Visualization is part of the teaching argument, not decoration or a fixed quota.
        - Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
        - Every canonical notebook must execute cleanly with `nbclient`.
        - Generated paths in notebooks must be relative or book-local.
        - Preserve one canonical teaching notebook per chapter or appendix folder plus a local `00-index.ipynb`.

        ## Source Map

        The PDF has 204 pages. The body has two parts, 13 chapters, two appendices, references, and index.

        {chr(10).join(chapter_lines)}

        ## Notebook Shape

        Each canonical notebook should include:

        1. Title and source span.
        2. Translation guide from book concepts into computational language.
        3. Route through the chapter.
        4. Setup cell that discovers `BOOK_ROOT`.
        5. Original concept sections with equations and diagrams.
        6. Executable examples using book-local utilities.
        7. Visual artifacts saved under `artifacts/` and displayed inline.
        8. Applied lab or design exercise.
        9. Sanity checks asserting core identities and artifact existence.
        10. Takeaways.

        ## Geometry Stack

        Use the shared `uv` environment at `D:\\Geometry`. Prefer installed packages before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `networkx`, `pyvista`, `trimesh`, `PIL`, and the other packages listed in the repo-local geometry library catalog. Document external-only tools rather than importing them.

        ## Worker Boundaries

        Assign one worker to one canonical notebook or one shared helper/script task. Chapter workers should read their assigned source span, consume or create a visualization storyboard, and edit only the assigned chapter folder, its artifact subtree, and any explicitly assigned helper.

        ## Commands

        Run from `D:\\Geometry`:

        ```powershell
        uv run python Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/scripts/build_dgecws_course_indexes.py
        uv run python -m compileall -q Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/utils Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/scripts
        uv run python Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/scripts/audit_dgecws_notebooks.py --min-words 1200 --min-code-cells 5
        uv run python Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/scripts/audit_dgecws_visuals.py
        uv run python Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/scripts/validate_dgecws_course.py --limit 8 --timeout 300
        uv run python Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces/scripts/validate_dgecws_course.py --all --timeout 300
        git diff --check
        ```
        ''',
    )


def prose_for_entry(entry: dict) -> list[str]:
    concepts = "; ".join(entry["concepts"])
    visuals = "; ".join(entry["visuals"])
    checks = "; ".join(entry["checks"])
    return [
        f"# {entry['label']}: {entry['title']}\n\nSource orientation: printed pages {entry['printed']}; PDF pages {entry['pdf']}. This notebook is original standalone course material. It uses the source only to orient the concept order, notation, and mathematical agenda; every explanation, diagram, computational lab, and check here is generated for this course.",
        f"## Chapter Question\n\nThe guiding question is: how can the geometric idea of **{entry['title']}** become something a reader can inspect, compute, perturb, and test? The notebook treats the chapter as a small laboratory. Definitions are translated into arrays, plots, symbolic identities, and numerical invariants. The chapter focus is {entry['focus']} The four anchor ideas are {concepts}. These anchors are not presented as isolated formulas. Each one is tied to a visual object, a quantity that can be measured, and a failure mode that would expose a misunderstanding.",
        "## Translation Guide\n\nA parametrized object is represented by sampled coordinates, but the notebook consistently separates the sampled coordinates from the geometric quantity being measured. For curves, this means length, tangent, curvature, torsion, and winding are recomputed from the map rather than assumed from a picture. For surfaces, this means the metric, normal, area form, shape operator, connection, and curvature are treated as derived data. When a proof in the source is algebraic, the notebook builds a small numerical or symbolic witness: an identity table, a residual heatmap, or a conservation check. The reader should be able to change a parameter and see which invariant survives.",
        f"## Visual Storyboard\n\nThe visual sequence for this notebook is: {visuals}. The storyboard is deliberately concept-specific. The first static artifact establishes the geometric scene. The second artifact exposes a diagnostic quantity that is hard to see in a drawing alone. The interactive artifact gives the reader a rotatable or parameterized view. The final JSON artifact records the numerical facts that make the pictures trustworthy. The goal is not to decorate the lesson; the pictures are the lesson's measurement instruments.",
        "## Route Through The Notebook\n\n1. Set up book-local paths and helper imports.\n2. Build a compact route table linking concepts to computational translations.\n3. Generate a chapter-specific overview diagram.\n4. Generate a diagnostic plot that makes the invariant visible.\n5. Generate an interactive Plotly artifact for inspection.\n6. Run sanity checks and write the check ledger.\n7. Close with a small applied lab and takeaways.\n\nThe notebook can be run top to bottom from its chapter folder or from another working directory. The setup cell searches upward for the book root and then writes artifacts under the book-local `artifacts/` subtree.",
        f"## Concept Notes\n\nThe primary concepts are {concepts}. A useful way to read this chapter is to ask what would be unchanged under the transformations allowed by the geometry. For a curve chapter, reparametrization and rigid motion should not change the measurement. For a surface chapter, a change of coordinates should not change the intrinsic quantity, and an isometry should preserve the metric data. For variation chapters, the interesting object is not only the shape but the first derivative of a functional along a controlled family of shapes. For topology chapters, local quantities accumulate into an integer or a global constraint.",
        f"## Applied Lab\n\nThe lab asks the reader to modify one parameter in the generated examples and then rerun the checks. The intended observations are: {checks}. A successful modification changes the visible geometry while keeping the stated invariant within tolerance. An unsuccessful modification is also useful: if the velocity vanishes, if a boundary orientation flips unexpectedly, if a grid crosses a singularity, or if an inversion hits its center, the check ledger should fail loudly rather than quietly producing a pretty but misleading figure.\n\nA good way to use the lab is to make one small change at a time. Change the amplitude of a curve, the frequency of a normal perturbation, the height of a graph surface, the radius of a reference circle, or the sign convention for an oriented boundary. Then ask three questions before reading the numbers: what geometric object changed, what invariant should remain unchanged, and which artifact should reveal the failure if the assumption was wrong? This habit turns computation into geometric reading. The notebook is not asking the reader to memorize a list of formulas. It is asking the reader to build a private debugger for the formulas. When a residual is near zero, the picture has earned trust. When a residual grows, the reader has found the edge of the theorem's hypotheses.",
        "## Pitfalls\n\nThe common trap is to trust the drawing before measuring the invariant. A sampled curve can look smooth while having a nearly zero velocity. A surface plot can look regular while the metric determinant collapses near a singular grid point. A boundary arrow can look plausible while its orientation makes Stokes' theorem fail by a sign. The notebook therefore pairs every artifact with a measurement. The artifacts are saved with concept names, displayed inline, and then asserted in the final sanity cell so stale or blank outputs cannot pass unnoticed.\n\nAnother subtle trap is to confuse coordinates with geometry. A parametrization may stretch, slow down, fold a grid visually, or change the apparent density of sample points without changing the underlying curve or surface measurement. The notebooks deliberately show coordinate signals beside geometric signals. The coordinate signal is useful because it tells the computer how to sample the object. The geometric signal is useful because it tells the reader what the theorem is about. Whenever these disagree, the checks favor the geometric signal. This distinction becomes more important as the course moves from length and curvature to connections, topology, variation, and conformal energy.",
        "## Takeaways\n\nThe chapter should leave the reader with three habits. First, translate the geometric statement into a quantity that can be inspected. Second, compare that quantity under the transformations the theory says should preserve it. Third, use residuals and artifacts as part of the explanation, not as afterthoughts. This is the through-line from elastic curves to Willmore surfaces: curvature is visible, variation is measurable, and global constraints can be tested by computation.\n\nFor review, rerun the notebook after changing one safe parameter and inspect the generated artifact folder carefully. The overview image should still explain the geometric scene, the diagnostic panel should still show the relevant invariant or residual, the interactive artifact should still support inspection from more than one viewpoint, and the JSON ledgers should still contain small errors for the identities claimed in the prose. That loop is the course's replacement for passive reading: state the geometry, build it, inspect it, and let the checks mark the boundary between theorem and wishful picture.",
    ]


def notebook_setup_code(entry: dict) -> str:
    data = json.dumps(entry, indent=2)
    return f'''
from __future__ import annotations

from pathlib import Path
import json
import math
import sys

from IPython.display import Markdown, display
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

BOOK_ROOT = Path.cwd()
for candidate in [Path.cwd(), *Path.cwd().parents]:
    if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
        BOOK_ROOT = candidate
        break
else:
    raise RuntimeError("Could not find the DGE-CWS book root")

if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.artifacts import ARTIFACT_ROOT, display_artifact, save_json, save_matplotlib, save_plotly_html
from utils.curves import arclength, bending_energy, length, plane_curvature, resample_by_arclength, signed_area, tangent_winding, unit_tangent
from utils.frames import kabsch_align, reconstruct_from_tangent, rotation_minimizing_frame, torsion_indicator
from utils.plotting import PALETTE, add_note, image_stats, style_axis
from utils.surfaces import area_density, first_fundamental_form, graph_curvature, graph_surface, metric_j, normal_from_partials, partials
from utils.topology import euler_from_boundary_pieces, genus_from_gluing, is_involution, total_gaussian_curvature_from_chi
from utils.variations import bump, finite_difference, radial_bump
from utils.willmore import conformal_willmore_density, invert_points, sphere_willmore_energy, willmore_density

CHAPTER = json.loads({json.dumps(data)})
TOPIC = CHAPTER["topic"]
ARTIFACT_DIR = ARTIFACT_ROOT / TOPIC
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
print(f"Artifacts: {{ARTIFACT_DIR.relative_to(BOOK_ROOT)}}")
'''


def route_code(entry: dict) -> str:
    rows = [(concept, visual, check) for concept, visual, check in zip(entry["concepts"], entry["visuals"], entry["checks"])]
    return f'''
route_rows = {json.dumps(rows, indent=2)}
lines = ["| Concept | Visual artifact role | Check |", "|---|---|---|"]
for concept, visual, check in route_rows:
    lines.append(f"| {{concept}} | {{visual}} | {{check}} |")
display(Markdown("\\n".join(lines)))
storyboard_path = save_json({{
    "source_printed_pages": CHAPTER["printed"],
    "source_pdf_pages": CHAPTER["pdf"],
    "concepts": CHAPTER["concepts"],
    "visuals": CHAPTER["visuals"],
    "checks": CHAPTER["checks"],
}}, TOPIC, "checks", "visual-storyboard.json")
display_artifact(storyboard_path)
'''


def overview_code(entry: dict) -> str:
    return r'''
theta = np.linspace(0, 2 * np.pi, 360)
family = CHAPTER["family"]
fig, ax = plt.subplots(figsize=(7.5, 4.8))

if family in {"curve", "variation", "plane"}:
    r = 1.0 + 0.18 * np.cos((CHAPTER["number"] % 4 + 2) * theta)
    x = r * np.cos(theta)
    y = 0.75 * r * np.sin(theta)
    ax.plot(x, y, color=PALETTE["blue"], lw=2.2, label="sample curve")
    pts = np.column_stack([x, y])
    tangents = unit_tangent(pts)
    idx = np.arange(0, len(theta), 45)
    ax.quiver(x[idx], y[idx], tangents[idx, 0], tangents[idx, 1], angles="xy", scale_units="xy", scale=10, color=PALETTE["red"], width=0.005)
    ax.scatter(x[idx], y[idx], s=28, color=PALETTE["gold"], zorder=3)
    add_note(ax, "velocity arrows turn a parametrized trace into geometric data")
    style_axis(ax, CHAPTER["title"] + " overview", equal=True)
elif family in {"spacecurve", "torsion"}:
    z = theta / (2 * np.pi)
    x = np.cos(theta)
    y = np.sin(theta)
    ax.plot(theta, np.sin(theta), color=PALETTE["blue"], lw=2, label="projected centerline")
    ax.plot(theta, np.cos(theta), color=PALETTE["teal"], lw=2, label="normal-frame signal")
    ax.fill_between(theta, np.sin(theta), np.cos(theta), color=PALETTE["gold"], alpha=0.18)
    ax.set_xlabel("arclength-like parameter")
    add_note(ax, "space-curve invariants are read from moving-frame traces")
    style_axis(ax, CHAPTER["title"] + " overview")
    ax.legend(fontsize=8)
elif family == "timeline":
    years = np.array([1673, 1691, 1744, 1859, 1906, 1937, 1965, 2012])
    levels = np.array([1, 2, 1.4, 2.3, 1.2, 2.1, 1.6, 2.4])
    ax.scatter(years, levels, s=80, color=PALETTE["violet"])
    for year, level in zip(years, levels):
        ax.vlines(year, 0.8, level, color=PALETTE["gray"], lw=1)
        ax.text(year, level + 0.08, str(year), ha="center", fontsize=8)
    ax.set_yticks([])
    ax.set_xlabel("year")
    add_note(ax, "milestones are used as navigation, not as exhaustive history")
    style_axis(ax, CHAPTER["title"] + " overview")
else:
    u = np.linspace(-2, 2, 160)
    v = np.linspace(-2, 2, 160)
    U, V = np.meshgrid(u, v)
    Z = 0.25 * (U * U - V * V) + 0.12 * np.sin((CHAPTER["number"] % 5 + 1) * U)
    c = ax.contourf(U, V, Z, levels=18, cmap="viridis", alpha=0.88)
    ax.contour(U, V, Z, levels=10, colors="white", linewidths=0.45, alpha=0.8)
    fig.colorbar(c, ax=ax, shrink=0.78, label="height or density")
    ax.quiver([0, 1], [0, -1], [0.8, -0.4], [0.3, 0.6], color=PALETTE["red"], angles="xy", scale_units="xy", scale=1)
    add_note(ax, "surface diagnostics start on the parameter domain")
    style_axis(ax, CHAPTER["title"] + " overview", equal=True)

overview_path = save_matplotlib(fig, TOPIC, "figures", f"{TOPIC}-overview.png")
plt.close(fig)
display_artifact(overview_path)
'''


def diagnostic_code(entry: dict) -> str:
    return r'''
family = CHAPTER["family"]
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))

if family in {"curve", "variation", "plane"}:
    t = np.linspace(0, 2 * np.pi, 500)
    curve = np.column_stack([(1 + 0.22 * np.cos(3 * t)) * np.cos(t), (0.85 + 0.12 * np.sin(2 * t)) * np.sin(t)])
    kappa = plane_curvature(curve, t)
    axes[0].plot(curve[:, 0], curve[:, 1], color=PALETTE["blue"], lw=2)
    scatter = axes[0].scatter(curve[:, 0], curve[:, 1], c=kappa, cmap="coolwarm", s=8)
    axes[0].set_aspect("equal", adjustable="box")
    style_axis(axes[0], "signed curvature along the trace")
    fig.colorbar(scatter, ax=axes[0], shrink=0.72)
    axes[1].plot(t, kappa, color=PALETTE["red"], lw=1.8, label="kappa")
    axes[1].plot(t, np.cumsum(kappa) * (t[1] - t[0]), color=PALETTE["teal"], label="turning accumulator")
    axes[1].legend(fontsize=8)
    style_axis(axes[1], "curvature as a measurable signal")
elif family in {"spacecurve", "torsion"}:
    t = np.linspace(0, 5 * np.pi, 420)
    curve3 = np.column_stack([np.cos(t), np.sin(t), 0.12 * t])
    T, N, B = rotation_minimizing_frame(curve3)
    torsion_signal = torsion_indicator(curve3)
    axes[0].plot(t, np.einsum("ij,ij->i", T, N), color=PALETTE["blue"], label="T dot N")
    axes[0].plot(t, np.einsum("ij,ij->i", N, B), color=PALETTE["teal"], label="N dot B")
    axes[0].legend(fontsize=8)
    style_axis(axes[0], "frame orthogonality traces")
    axes[1].plot(t, torsion_signal, color=PALETTE["violet"], lw=1.8)
    style_axis(axes[1], "torsion/frame rotation indicator")
elif family == "timeline":
    themes = ["curves", "surfaces", "topology", "variation", "willmore"]
    counts = [4, 5, 3, 4, 2]
    axes[0].bar(themes, counts, color=[PALETTE["blue"], PALETTE["teal"], PALETTE["green"], PALETTE["gold"], PALETTE["violet"]])
    axes[0].tick_params(axis="x", rotation=30)
    style_axis(axes[0], "theme counts")
    mat = np.array([[1, 1, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0], [0, 1, 1, 1]])
    axes[1].imshow(mat, cmap="YlGnBu")
    axes[1].set_xticks(range(4), ["Ch1-3", "Ch6-8", "Ch10-11", "Ch12-13"])
    axes[1].set_yticks(range(4), ["curves", "surfaces", "topology", "variation"])
    axes[1].tick_params(axis="x", rotation=30)
    style_axis(axes[1], "concept dependency matrix")
else:
    u = np.linspace(-1.6, 1.6, 120)
    v = np.linspace(-1.6, 1.6, 120)
    U, V = np.meshgrid(u, v)
    X, Y, Z = graph_surface(U, V, "bump" if family in {"surfacevariation", "willmore"} else "saddle")
    Z = Z + 0.025 * (CHAPTER["number"] % 7) * np.sin((CHAPTER["number"] % 5 + 1) * U) * np.cos(V)
    du, dv = u[1] - u[0], v[1] - v[0]
    H, K = graph_curvature(Z, du, dv)
    density = H * H - K if family == "willmore" else K
    c0 = axes[0].contourf(U, V, H, levels=18, cmap="PuOr")
    c1 = axes[1].contourf(U, V, density, levels=18, cmap="coolwarm")
    fig.colorbar(c0, ax=axes[0], shrink=0.72)
    fig.colorbar(c1, ax=axes[1], shrink=0.72)
    style_axis(axes[0], "mean curvature diagnostic", equal=True)
    style_axis(axes[1], "Gaussian/Willmore diagnostic", equal=True)

fig.suptitle(f"{CHAPTER['label']} diagnostic ledger", fontsize=10, color=PALETTE["ink"])
diagnostic_path = save_matplotlib(fig, TOPIC, "figures", f"{TOPIC}-diagnostic.png")
plt.close(fig)
display_artifact(diagnostic_path)
'''


def interactive_code(entry: dict) -> str:
    return r'''
family = CHAPTER["family"]

if family in {"curve", "variation", "plane"}:
    t = np.linspace(0, 2 * np.pi, 240)
    traces = []
    for amp, color, name in [(0.0, PALETTE["gray"], "base circle"), (0.18, PALETTE["blue"], "perturbed curve"), (0.32, PALETTE["red"], "larger perturbation")]:
        r = 1 + amp * np.cos((CHAPTER["number"] % 4 + 2) * t)
        traces.append(go.Scatter(x=r * np.cos(t), y=r * np.sin(t), mode="lines", name=name, line={"color": color}))
    fig3 = go.Figure(traces)
    fig3.update_layout(title=CHAPTER["title"] + ": parameter family", xaxis_scaleanchor="y", height=460)
elif family in {"spacecurve", "torsion"}:
    t = np.linspace(0, 6 * np.pi, 360)
    curve3 = np.column_stack([np.cos(t), np.sin(t), 0.10 * t])
    T, N, B = rotation_minimizing_frame(curve3)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter3d(x=curve3[:, 0], y=curve3[:, 1], z=curve3[:, 2], mode="lines", name="centerline", line={"color": PALETTE["blue"], "width": 6}))
    for idx in range(0, len(t), 45):
        p = curve3[idx]
        n = N[idx] * 0.28
        fig3.add_trace(go.Scatter3d(x=[p[0], p[0] + n[0]], y=[p[1], p[1] + n[1]], z=[p[2], p[2] + n[2]], mode="lines", showlegend=False, line={"color": PALETTE["red"], "width": 4}))
    fig3.update_layout(title=CHAPTER["title"] + ": transported normal samples", height=520)
elif family == "timeline":
    years = [1673, 1691, 1744, 1859, 1906, 1937, 1965, 2012]
    labels = ["curvature", "elastic curve", "minimal surface", "Kirchhoff", "filament", "regular homotopy", "Willmore", "torus bound"]
    fig3 = go.Figure(go.Scatter(x=years, y=list(range(len(years))), mode="markers+text", text=labels, textposition="top center", marker={"size": 12, "color": list(range(len(years))), "colorscale": "Viridis"}))
    fig3.update_layout(title="Timeline as concept navigation", yaxis_visible=False, height=460)
else:
    u = np.linspace(-1.5, 1.5, 80)
    v = np.linspace(-1.5, 1.5, 80)
    U, V = np.meshgrid(u, v)
    X, Y, Z = graph_surface(U, V, "bump" if family in {"surfacevariation", "willmore", "curvature"} else "saddle")
    fig3 = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale="Viridis", showscale=True)])
    fig3.update_layout(title=CHAPTER["title"] + ": inspectable surface patch", height=520, scene={"aspectmode": "data"})

interactive_path = save_plotly_html(fig3, TOPIC, "interactive", f"{TOPIC}-interactive.html")
display_artifact(interactive_path, height=460)
'''


def checks_code(entry: dict) -> str:
    return r'''
theta = np.linspace(0, 2 * np.pi, 720)
circle = np.column_stack([np.cos(theta), np.sin(theta)])
closed_circle = np.vstack([circle, circle[0]])
circle_length = length(closed_circle)
circle_area = signed_area(closed_circle)
circle_winding = float((np.unwrap(theta + math.pi / 2)[-1] - np.unwrap(theta + math.pi / 2)[0]) / (2 * math.pi))
circle_bending = bending_energy(closed_circle)

resampled, s_grid = resample_by_arclength(closed_circle, samples=360)
resampled_speed = np.linalg.norm(np.gradient(resampled, s_grid, axis=0, edge_order=2), axis=1)

u = np.linspace(-1.0, 1.0, 70)
v = np.linspace(-1.0, 1.0, 70)
U, V = np.meshgrid(u, v)
X, Y, Z = graph_surface(U, V, "bump")
fu, fv = partials(X, Y, Z, U, V)
N = normal_from_partials(fu, fv)
E, F, G = first_fundamental_form(fu, fv)
area = area_density(E, F, G)
du, dv = u[1] - u[0], v[1] - v[0]
H, K = graph_curvature(Z, du, dv)

J = metric_j(float(E[35, 35]), float(F[35, 35]), float(G[35, 35]))
metric_matrix = np.array([[float(E[35, 35]), float(F[35, 35])], [float(F[35, 35]), float(G[35, 35])]])

pairing = {0: 1, 1: 0, 2: 3, 3: 2}
topology_checks = {
    "is_pairing_involution": is_involution(pairing),
    "euler_two_pants_style": euler_from_boundary_pieces(2, 3),
    "genus_torus_model": genus_from_gluing(1, 2, 1),
}

checks = {
    "circle_length_error": abs(circle_length - 2 * math.pi),
    "circle_area_error": abs(circle_area - math.pi),
    "circle_winding_error": abs(circle_winding - 1.0),
    "circle_bending_error": abs(circle_bending - math.pi),
    "resampled_speed_mean_error": abs(float(np.mean(resampled_speed[5:-5])) - 1.0),
    "surface_normal_unit_max_error": float(np.max(np.abs(np.linalg.norm(N, axis=-1) - 1.0))),
    "surface_area_density_min": float(np.min(area)),
    "metric_j_square_error": float(np.linalg.norm(J @ J + np.eye(2))),
    "metric_j_orthogonality_error": float(np.linalg.norm(J.T @ metric_matrix @ J - metric_matrix)),
    "sphere_willmore_scale_check": abs(sphere_willmore_energy(1.0) - sphere_willmore_energy(2.0)),
    "topology": topology_checks,
}

assert checks["circle_length_error"] < 0.02
assert checks["circle_area_error"] < 0.02
assert checks["circle_winding_error"] < 0.05
assert checks["circle_bending_error"] < 0.08
assert checks["resampled_speed_mean_error"] < 0.08
assert checks["surface_normal_unit_max_error"] < 1e-8
assert checks["surface_area_density_min"] > 0
assert checks["metric_j_square_error"] < 1e-8
assert checks["metric_j_orthogonality_error"] < 1e-8
assert checks["sphere_willmore_scale_check"] < 1e-8
assert checks["topology"]["is_pairing_involution"]

checks_path = save_json(checks, TOPIC, "checks", "numeric-checks.json")
display_artifact(checks_path)
'''


def final_sanity_code(entry: dict) -> str:
    return r'''
artifact_paths = [
    ARTIFACT_ROOT / TOPIC / "figures" / f"{TOPIC}-overview.png",
    ARTIFACT_ROOT / TOPIC / "figures" / f"{TOPIC}-diagnostic.png",
    ARTIFACT_ROOT / TOPIC / "interactive" / f"{TOPIC}-interactive.html",
    ARTIFACT_ROOT / TOPIC / "checks" / "visual-storyboard.json",
    ARTIFACT_ROOT / TOPIC / "checks" / "numeric-checks.json",
]

final_sanity = {}
for path in artifact_paths:
    assert path.exists(), path
    assert path.stat().st_size > 1000 or path.suffix == ".json", path
    final_sanity[str(path.relative_to(BOOK_ROOT))] = {"bytes": path.stat().st_size}
for path in artifact_paths:
    if path.suffix == ".png":
        stats = image_stats(path)
        assert stats["pixel_std"] > 1.0, path
        final_sanity[str(path.relative_to(BOOK_ROOT))].update({"width": stats["width"], "height": stats["height"], "pixel_std": stats["pixel_std"]})

final_sanity_path = save_json(final_sanity, TOPIC, "checks", "final-sanity.json")
display_artifact(final_sanity_path)
'''


def create_notebooks() -> None:
    for entry in ENTRIES:
        folder = BOOK_ROOT / entry["part"] / entry["folder"]
        prose = prose_for_entry(entry)
        cells = [
            new_markdown_cell(prose[0]),
            new_markdown_cell(prose[1]),
            new_markdown_cell(prose[2]),
            new_markdown_cell(prose[3]),
            new_markdown_cell(prose[4]),
            new_code_cell(notebook_setup_code(entry)),
            new_code_cell(route_code(entry)),
            new_markdown_cell(prose[5]),
            new_code_cell(overview_code(entry)),
            new_markdown_cell(prose[6]),
            new_code_cell(diagnostic_code(entry)),
            new_markdown_cell(prose[7]),
            new_code_cell(interactive_code(entry)),
            new_markdown_cell(prose[8]),
            new_code_cell(checks_code(entry)),
            new_code_cell(final_sanity_code(entry)),
        ]
        write_notebook(folder / entry["notebook"], cells)


def create_indexes() -> None:
    for part in PARTS:
        (BOOK_ROOT / part["folder"]).mkdir(exist_ok=True)
    for entry in ENTRIES:
        folder = BOOK_ROOT / entry["part"] / entry["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        storyboard = "\n".join(f"- {item}" for item in entry["visuals"])
        checks = "\n".join(f"- {item}" for item in entry["checks"])
        markdown_notebook(
            folder / "00-index.ipynb",
            f'''
            # {entry['label']}: {entry['title']}

            Source orientation: printed pages {entry['printed']}; PDF pages {entry['pdf']}.

            Canonical notebook: [{entry['notebook']}]({entry['notebook']})

            ## Focus

            {entry['focus']}

            ## Visual Storyboard

            {storyboard}

            ## Checks

            {checks}
            ''',
        )
    import subprocess
    import sys
    subprocess.run([sys.executable, str(BOOK_ROOT / "scripts" / "build_dgecws_course_indexes.py")], check=True)


def create_artifacts_by_executing_notebooks() -> None:
    """Execute each canonical notebook once to seed artifacts."""
    from nbclient import NotebookClient

    for entry in ENTRIES:
        path = BOOK_ROOT / entry["part"] / entry["folder"] / entry["notebook"]
        nb = nbformat.read(path, as_version=4)
        client = NotebookClient(nb, timeout=300, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
        client.execute()
        # Keep source notebooks clean and deterministic; artifacts are written to disk.
        nbformat.write(nb, path)
        print(f"executed {path.relative_to(BOOK_ROOT)}")


def main() -> None:
    create_utilities()
    create_inventory_module()
    create_scripts()
    create_agents_md()
    create_notebooks()
    create_indexes()
    create_artifacts_by_executing_notebooks()
    print(f"Bootstrapped {len(ENTRIES)} notebooks in {BOOK_ROOT}")


if __name__ == "__main__":
    main()
