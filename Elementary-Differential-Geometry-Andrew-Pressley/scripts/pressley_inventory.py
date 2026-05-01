"""Chapter metadata inventory for Pressley's Elementary Differential Geometry."""

from __future__ import annotations

import argparse
import json
from typing import Any

PDF_SOURCE = "Elementary Differential Geometry (Andrew Pressley).pdf"
SOURCE_SPAN_NOTES = [
    "Physical PDF page spans are 1-based and were recovered from the table of contents and page extraction.",
    "Back matter hints, solutions, and index are inventoried only; do not copy or convert them into notebooks.",
]

ENTRIES: list[dict[str, Any]] = [
    {
        "id": 1,
        "kind": "chapter",
        "label": "Chapter 1",
        "title": "Curves in the plane and in space",
        "folder": "chapter-01-curves-in-the-plane-and-in-space",
        "notebook": "01-curves-in-the-plane-and-in-space.ipynb",
        "artifact": "chapter-01",
        "printed_span": "1-27",
        "pdf_span": "11-37",
        "sections": "1.1-1.5",
        "focus": "Introduces curves as parametrized paths and level sets, then develops tangent vectors, arc length, reparametrization, closed curves, and regularity.",
        "topics": ["parametrized and level curves", "tangent vectors and regular points", "arc length and unit-speed parameters", "reparametrization and singularities", "closed curves and self-intersections", "local passage between level and parametrized descriptions"],
        "visual_kinds": ["curve", "level", "arc", "singularity"],
    },
    {
        "id": 2,
        "kind": "chapter",
        "label": "Chapter 2",
        "title": "How much does a curve curve?",
        "folder": "chapter-02-how-much-does-a-curve-curve",
        "notebook": "02-how-much-does-a-curve-curve.ipynb",
        "artifact": "chapter-02",
        "printed_span": "29-54",
        "pdf_span": "38-63",
        "sections": "2.1-2.3",
        "focus": "Builds curvature and torsion for plane and space curves, including signed curvature, osculating circles, Frenet frames, and shape determination.",
        "topics": ["curvature of unit-speed curves", "curvature formulas for arbitrary parameters", "signed curvature and tangent turning", "osculating circles and evolutes", "space curves and torsion", "Frenet-Serret frame checks"],
        "visual_kinds": ["curvature", "osculating", "frame", "torsion"],
    },
    {
        "id": 3,
        "kind": "chapter",
        "label": "Chapter 3",
        "title": "Global properties of curves",
        "folder": "chapter-03-global-properties-of-curves",
        "notebook": "03-global-properties-of-curves.ipynb",
        "artifact": "chapter-03",
        "printed_span": "55-66",
        "pdf_span": "64-74",
        "sections": "3.1-3.3",
        "focus": "Moves from local curve quantities to global statements about simple closed curves, enclosed area, isoperimetry, and the four vertex theorem.",
        "topics": ["simple closed curves", "oriented area and Green-style computation", "isoperimetric inequality", "roundness deficit", "curvature extrema", "four vertex theorem experiments"],
        "visual_kinds": ["closed", "isoperimetric", "vertices", "lab"],
    },
    {
        "id": 4,
        "kind": "chapter",
        "label": "Chapter 4",
        "title": "Surfaces in three dimensions",
        "folder": "chapter-04-surfaces-in-three-dimensions",
        "notebook": "04-surfaces-in-three-dimensions.ipynb",
        "artifact": "chapter-04",
        "printed_span": "67-94",
        "pdf_span": "75-101",
        "sections": "4.1-4.5",
        "focus": "Defines surfaces through patches, smoothness, maps, tangent planes, derivatives, normals, and orientability.",
        "topics": ["surface patches and atlases", "smoothness and transition maps", "smooth maps between surfaces", "tangent planes from parameter curves", "surface normals", "orientability and the Mobius-band obstruction"],
        "visual_kinds": ["patch", "tangent", "normal", "orientability"],
    },
    {
        "id": 5,
        "kind": "chapter",
        "label": "Chapter 5",
        "title": "Examples of surfaces",
        "folder": "chapter-05-examples-of-surfaces",
        "notebook": "05-examples-of-surfaces.ipynb",
        "artifact": "chapter-05",
        "printed_span": "95-120",
        "pdf_span": "102-126",
        "sections": "5.1-5.6",
        "focus": "Catalogs level surfaces, quadrics, ruled surfaces, surfaces of revolution, compact surfaces, triply orthogonal systems, and inverse-function-theorem applications.",
        "topics": ["level surfaces", "quadric classification", "ruled surfaces", "surfaces of revolution", "compact surfaces and genus", "triply orthogonal systems", "inverse function theorem as local model control"],
        "visual_kinds": ["quadric", "ruled", "revolution", "topology"],
    },
    {
        "id": 6,
        "kind": "chapter",
        "label": "Chapter 6",
        "title": "The first fundamental form",
        "folder": "chapter-06-the-first-fundamental-form",
        "notebook": "06-the-first-fundamental-form.ipynb",
        "artifact": "chapter-06",
        "printed_span": "121-158",
        "pdf_span": "127-163",
        "sections": "6.1-6.5",
        "focus": "Turns surface parametrizations into intrinsic metric data for lengths, isometries, conformal maps, equiareal maps, Archimedes' theorem, and spherical geometry.",
        "topics": ["metric coefficients E, F, G", "lengths of curves on surfaces", "isometries and local isometries", "conformal maps", "equiareal maps", "spherical distance and spherical triangles"],
        "visual_kinds": ["metric", "conformal", "area", "spherical"],
    },
    {
        "id": 7,
        "kind": "chapter",
        "label": "Chapter 7",
        "title": "Curvature of surfaces",
        "folder": "chapter-07-curvature-of-surfaces",
        "notebook": "07-curvature-of-surfaces.ipynb",
        "artifact": "chapter-07",
        "printed_span": "159-178",
        "pdf_span": "164-182",
        "sections": "7.1-7.4",
        "focus": "Introduces the second fundamental form, Gauss and Weingarten maps, normal/geodesic curvature, parallel transport, and covariant derivative.",
        "topics": ["second fundamental form", "Gauss map", "Weingarten map", "normal curvature", "geodesic curvature", "parallel transport", "covariant derivative"],
        "visual_kinds": ["second-form", "gauss-map", "geodesic-curvature", "transport"],
    },
    {
        "id": 8,
        "kind": "chapter",
        "label": "Chapter 8",
        "title": "Gaussian, mean and principal curvatures",
        "folder": "chapter-08-gaussian-mean-and-principal-curvatures",
        "notebook": "08-gaussian-mean-and-principal-curvatures.ipynb",
        "artifact": "chapter-08",
        "printed_span": "179-214",
        "pdf_span": "183-217",
        "sections": "8.1-8.6",
        "focus": "Extracts Gaussian, mean, and principal curvatures from the shape operator and explores constant curvature, flat, constant mean curvature, and compact surface consequences.",
        "topics": ["Gaussian and mean curvature", "principal curvatures", "constant Gaussian curvature", "flat surfaces", "constant mean curvature", "compact-surface curvature constraints"],
        "visual_kinds": ["principal", "curvature-sign", "constant-k", "mean"],
    },
    {
        "id": 9,
        "kind": "chapter",
        "label": "Chapter 9",
        "title": "Geodesics",
        "folder": "chapter-09-geodesics",
        "notebook": "09-geodesics.ipynb",
        "artifact": "chapter-09",
        "printed_span": "215-246",
        "pdf_span": "218-248",
        "sections": "9.1-9.5",
        "focus": "Develops geodesics as straightest and shortest surface curves, with equations, surfaces of revolution, Clairaut's theorem, and geodesic coordinates.",
        "topics": ["geodesic definition", "geodesic equations", "surfaces of revolution", "Clairaut invariant", "shortest paths", "geodesic coordinates"],
        "visual_kinds": ["geodesic", "clairaut", "shortest", "polar"],
    },
    {
        "id": 10,
        "kind": "chapter",
        "label": "Chapter 10",
        "title": "Gauss' Theorema Egregium",
        "folder": "chapter-10-gauss-theorema-egregium",
        "notebook": "10-gauss-theorema-egregium.ipynb",
        "artifact": "chapter-10",
        "printed_span": "247-269",
        "pdf_span": "249-270",
        "sections": "10.1-10.4",
        "focus": "Proves and applies the intrinsic invariance of Gaussian curvature via Gauss-Codazzi-Mainardi equations, constant curvature surfaces, and geodesic mappings.",
        "topics": ["Gauss equations", "Codazzi-Mainardi equations", "intrinsic curvature", "bending without stretching", "constant curvature coordinates", "geodesic mappings"],
        "visual_kinds": ["egregium", "metric-k", "codazzi", "bending"],
    },
    {
        "id": 11,
        "kind": "chapter",
        "label": "Chapter 11",
        "title": "Hyperbolic geometry",
        "folder": "chapter-11-hyperbolic-geometry",
        "notebook": "11-hyperbolic-geometry.ipynb",
        "artifact": "chapter-11",
        "printed_span": "270-304",
        "pdf_span": "271-306",
        "sections": "11.1-11.5",
        "focus": "Builds hyperbolic geometry through the upper half-plane, isometries, Poincare disk, parallels, Beltrami-Klein model, and cross-ratio distance.",
        "topics": ["upper half-plane model", "hyperbolic isometries", "Poincare disk model", "hyperbolic parallels", "Beltrami-Klein model", "cross-ratio distance"],
        "visual_kinds": ["hyperbolic", "mobius", "parallels", "klein"],
    },
    {
        "id": 12,
        "kind": "chapter",
        "label": "Chapter 12",
        "title": "Minimal surfaces",
        "folder": "chapter-12-minimal-surfaces",
        "notebook": "12-minimal-surfaces.ipynb",
        "artifact": "chapter-12",
        "printed_span": "305-334",
        "pdf_span": "307-335",
        "sections": "12.1-12.5",
        "focus": "Connects Plateau's problem, zero mean curvature, catenoids, helicoids, Gauss maps, conformal parametrizations, and holomorphic data.",
        "topics": ["Plateau's problem", "zero mean curvature", "catenoid and helicoid examples", "Gauss map of a minimal surface", "conformal parametrization", "Weierstrass representation"],
        "visual_kinds": ["minimal", "catenoid", "helicoid", "weierstrass"],
    },
    {
        "id": 13,
        "kind": "chapter",
        "label": "Chapter 13",
        "title": "The Gauss-Bonnet theorem",
        "folder": "chapter-13-the-gauss-bonnet-theorem",
        "notebook": "13-the-gauss-bonnet-theorem.ipynb",
        "artifact": "chapter-13",
        "printed_span": "335-378",
        "pdf_span": "336-378",
        "sections": "13.1-13.8",
        "focus": "Develops Gauss-Bonnet from local curve versions to curvilinear polygons, compact surfaces, map coloring, holonomy, vector-field singularities, and critical points.",
        "topics": ["Gauss-Bonnet for simple closed curves", "curvilinear polygons", "integration on compact surfaces", "global Gauss-Bonnet", "map coloring", "holonomy", "vector-field indices", "critical points"],
        "visual_kinds": ["bonnet", "triangulation", "field", "critical"],
    },
    {
        "id": "A0",
        "kind": "appendix",
        "label": "Appendix A0",
        "title": "Inner product spaces and self-adjoint linear maps",
        "folder": "appendix-a0-inner-product-spaces-and-self-adjoint-linear-maps",
        "notebook": "a0-inner-product-spaces-and-self-adjoint-linear-maps.ipynb",
        "artifact": "appendix-a0",
        "printed_span": "A0",
        "pdf_span": "379-381",
        "sections": "Appendix 0",
        "focus": "Provides the linear-algebra language needed for metrics, self-adjoint maps, eigenvectors, and principal curvature directions.",
        "topics": ["inner products", "orthonormal bases", "bilinear and quadratic forms", "self-adjoint maps", "eigenvectors", "spectral theorem"],
        "visual_kinds": ["linear", "ellipse", "eigen", "basis"],
    },
    {
        "id": "A1",
        "kind": "appendix",
        "label": "Appendix A1",
        "title": "Isometries of Euclidean spaces",
        "folder": "appendix-a1-isometries-of-euclidean-spaces",
        "notebook": "a1-isometries-of-euclidean-spaces.ipynb",
        "artifact": "appendix-a1",
        "printed_span": "A1",
        "pdf_span": "382-389",
        "sections": "Appendix 1",
        "focus": "Summarizes Euclidean isometries as translations, rotations, reflections, and orthogonal affine maps.",
        "topics": ["Euclidean isometries", "translations", "orthogonal matrices", "reflections", "rotations", "orientation"],
        "visual_kinds": ["isometry", "rotation", "reflection", "composition"],
    },
    {
        "id": "A2",
        "kind": "appendix",
        "label": "Appendix A2",
        "title": "Mobius transformations",
        "folder": "appendix-a2-mobius-transformations",
        "notebook": "a2-mobius-transformations.ipynb",
        "artifact": "appendix-a2",
        "printed_span": "A2",
        "pdf_span": "390-398",
        "sections": "Appendix 2",
        "focus": "Collects the Mobius transformation facts used for stereographic projection, inversions, circles, and hyperbolic-model isometries.",
        "topics": ["extended complex plane", "Mobius transformations", "circle and line preservation", "inversion", "cross-ratio", "orientation and conjugation"],
        "visual_kinds": ["mobius", "inversion", "cross-ratio", "circle-line"],
    },
]

BACK_MATTER: list[dict[str, str]] = [
    {"title": "Hints to selected exercises", "pdf_span": "399-403", "policy": "Inventory only; do not copy hint prose into notebooks."},
    {"title": "Solutions", "pdf_span": "404-464", "policy": "Inventory only; do not copy solutions or long exercise text."},
    {"title": "Index", "pdf_span": "465-469", "policy": "Inventory only; do not reproduce index pages."},
]


def validate_inventory() -> None:
    expected = [*range(1, 14), "A0", "A1", "A2"]
    actual = [entry["id"] for entry in ENTRIES]
    if actual != expected:
        raise ValueError(f"Unexpected unit ids: {actual!r}")
    seen = set()
    for entry in ENTRIES:
        for field in ["label", "title", "folder", "notebook", "artifact", "pdf_span", "topics"]:
            if not entry.get(field):
                raise ValueError(f"Missing {field} in {entry!r}")
        if entry["folder"] in seen:
            raise ValueError(f"Duplicate folder {entry['folder']}")
        seen.add(entry["folder"])
        if len(entry["topics"]) < 5:
            raise ValueError(f"Too few topics for {entry['id']}")


def to_markdown() -> str:
    lines = ["# Pressley Chapter Metadata Inventory", "", f"Source: `{PDF_SOURCE}`", "", "## Source Span Notes", ""]
    lines.extend(f"- {note}" for note in SOURCE_SPAN_NOTES)
    lines.extend(["", "## Units", ""])
    for entry in ENTRIES:
        lines.append(f"### {entry['label']}: {entry['title']}")
        lines.append(f"- Folder: `{entry['folder']}`")
        lines.append(f"- Printed span: {entry['printed_span']}")
        lines.append(f"- PDF span: {entry['pdf_span']}")
        lines.append(f"- Sections: {entry['sections']}")
        lines.append(f"- Focus: {entry['focus']}")
        lines.append("- Topics:")
        lines.extend(f"  - {topic}" for topic in entry["topics"])
        lines.append("")
    lines.extend(["## Back Matter", ""])
    for item in BACK_MATTER:
        lines.append(f"- {item['title']}: PDF pages {item['pdf_span']}. {item['policy']}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    validate_inventory()
    if args.check:
        print(f"ok: {len(ENTRIES)} units")
        return
    if args.json:
        print(json.dumps({"source": PDF_SOURCE, "source_span_notes": SOURCE_SPAN_NOTES, "units": ENTRIES, "back_matter": BACK_MATTER}, indent=2))
        return
    print(to_markdown(), end="")


if __name__ == "__main__":
    main()
