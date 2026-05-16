"""Course inventory and source map for Hartshorne Algebraic Geometry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PDF_SOURCE = "local user-provided textbook PDF; source text is used only for orientation"
BOOK_TITLE = "Algebraic Geometry"
BOOK_AUTHOR = "Robin Hartshorne"
SERIES = "Graduate Texts in Mathematics 52"

SOURCE_SPAN_NOTES = [
    "PDF spans are 1-based physical PDF pages.",
    "The source PDF has 511 physical pages.",
    "Main-matter printed page 1 is PDF page 16, so printed page n maps to PDF page n + 15.",
    "Notebook prose, examples, diagrams, exercises, and artifacts are original and do not copy the source.",
]

ENTRIES: list[dict[str, Any]] = [
    {
        "kind": "chapter",
        "number": 1,
        "label": "Chapter I",
        "title": "Varieties",
        "folder": "chapter-01-varieties",
        "notebook": "01-varieties.ipynb",
        "artifact": "chapter-01",
        "printed_span": "1-59",
        "pdf_span": "16-74",
        "sections": "Affine and projective varieties; morphisms; rational maps; nonsingularity; curves; intersections",
        "focus": "Classical varieties as solution sets, the algebra-geometry dictionary, Zariski topology, rational maps, blowups, tangent spaces, and degree.",
        "visuals": [
            "Zariski topology versus Euclidean intuition through finite closed sets and dense opens",
            "Affine/projective chart atlas for a conic and the line at infinity",
            "Blowup of the node with exceptional direction separator",
            "Jacobian tangent-space dashboard for smooth and singular plane curves",
            "Bezout-style intersection counter for line sweeps through a cubic",
        ],
        "checks": [
            "Nullstellensatz toy correspondences match radical ideals in small examples",
            "homogeneous scaling leaves projective zero sets well-defined",
            "Jacobian rank detects the chosen singular point",
            "line intersection counts agree with degree after multiplicity flags",
        ],
        "terms": ["affine variety", "projective variety", "Zariski topology", "rational map", "blowup", "Jacobian", "degree"],
    },
    {
        "kind": "chapter",
        "number": 2,
        "label": "Chapter II",
        "title": "Schemes",
        "folder": "chapter-02-schemes",
        "notebook": "02-schemes.ipynb",
        "artifact": "chapter-02",
        "printed_span": "60-200",
        "pdf_span": "75-215",
        "sections": "Sheaves; schemes; morphisms; sheaves of modules; divisors; projective morphisms; differentials; formal schemes",
        "focus": "Schemes as locally ringed spaces assembled from affine spectra, with nilpotents, generic points, sheaves, morphisms, divisors, differentials, and formal neighborhoods.",
        "visuals": [
            "Spec poset with generic points and specialization arrows",
            "Sheaf gluing board for compatible local sections",
            "Nilpotent thickening as a visible first-order shadow",
            "Cartier versus Weil divisor bookkeeping on a cover",
            "Formal neighborhood tower around a closed point",
        ],
        "checks": [
            "restriction maps satisfy identity and composition in a toy sheaf",
            "nilpotent elements vanish on points but survive in rings",
            "principal divisor coefficients sum to zero on P1",
            "Kahler differential relations annihilate the defining equation",
        ],
        "terms": ["scheme", "Spec", "sheaf", "locally ringed space", "divisor", "differential", "formal scheme"],
    },
    {
        "kind": "chapter",
        "number": 3,
        "label": "Chapter III",
        "title": "Cohomology",
        "folder": "chapter-03-cohomology",
        "notebook": "03-cohomology.ipynb",
        "artifact": "chapter-03",
        "printed_span": "201-292",
        "pdf_span": "216-307",
        "sections": "Derived functors; sheaf cohomology; affine/projective computations; Ext; Serre duality; direct images; flat and smooth morphisms",
        "focus": "Cohomology as a measurement of failed gluing, then as a computational engine for projective space, duality, direct images, semicontinuity, flatness, and smoothness.",
        "visuals": [
            "Cech cover graph with cochains and coboundary arrows",
            "Cohomology table for line bundles on projective space",
            "Long exact sequence dependency diagram",
            "Serre duality pairing heat map for a curve model",
            "Semicontinuity family chart showing jumps in fiber dimensions",
        ],
        "checks": [
            "toy Cech coboundary squares to zero",
            "P1 line-bundle h0 and h1 values satisfy Riemann-Roch",
            "exact-sequence dimensions obey alternating Euler characteristic",
            "flat family sample keeps Hilbert function stable",
        ],
        "terms": ["derived functor", "Cech cohomology", "quasi-coherent sheaf", "Ext", "Serre duality", "flat morphism", "semicontinuity"],
    },
    {
        "kind": "chapter",
        "number": 4,
        "label": "Chapter IV",
        "title": "Curves",
        "folder": "chapter-04-curves",
        "notebook": "04-curves.ipynb",
        "artifact": "chapter-04",
        "printed_span": "293-355",
        "pdf_span": "308-370",
        "sections": "Riemann-Roch; Hurwitz; embeddings; elliptic curves; canonical embeddings; classification in projective space",
        "focus": "Nonsingular projective curves through divisors, Riemann-Roch, finite maps, ramification, elliptic group law, canonical maps, and projective models.",
        "visuals": [
            "Divisor abacus balancing degree, genus, and sections",
            "Riemann-Roch region plot for curves of several genera",
            "Hurwitz ramification ledger for a finite cover of P1",
            "Elliptic chord-and-tangent group law with exact cubic check",
            "Canonical embedding comparison by genus",
        ],
        "checks": [
            "Riemann-Roch numerical identity holds for sampled degrees",
            "Hurwitz formula balances ramification and genus",
            "elliptic line through two points meets the cubic in the computed third point",
            "canonical degree equals 2g-2 for g at least two",
        ],
        "terms": ["divisor", "Riemann-Roch", "Hurwitz", "elliptic curve", "canonical embedding", "genus"],
    },
    {
        "kind": "chapter",
        "number": 5,
        "label": "Chapter V",
        "title": "Surfaces",
        "folder": "chapter-05-surfaces",
        "notebook": "05-surfaces.ipynb",
        "artifact": "chapter-05",
        "printed_span": "356-423",
        "pdf_span": "371-438",
        "sections": "Geometry on a surface; ruled surfaces; monoidal transformations; cubic surfaces; birational transformations; classification",
        "focus": "Nonsingular projective surfaces through intersection forms, ruled surfaces, blowups, cubic-surface incidence, birational transformations, and classification invariants.",
        "visuals": [
            "Intersection-form grid for divisor classes on a blowup",
            "Ruled surface fiber/base coordinate model",
            "Blowup transformation dashboard for self-intersections",
            "Cubic surface line-incidence graph via a Schlaefli-style model",
            "Classification geography chart using Kodaira dimension landmarks",
        ],
        "checks": [
            "blowup self-intersection update subtracts exceptional multiplicity squared",
            "intersection pairing is symmetric on the sample basis",
            "cubic-surface line graph has the expected regular degree in the model",
            "birational invariant fields are unchanged in the toy transformation",
        ],
        "terms": ["surface", "intersection form", "ruled surface", "monoidal transformation", "cubic surface", "birational classification"],
    },
    {
        "kind": "appendix",
        "number": 6,
        "label": "Appendix A",
        "title": "Intersection Theory",
        "folder": "appendix-a-intersection-theory",
        "notebook": "appendix-a-intersection-theory.ipynb",
        "artifact": "appendix-a",
        "printed_span": "424-437",
        "pdf_span": "439-452",
        "sections": "Chow rings; Chern classes; Riemann-Roch; complements",
        "focus": "Intersection theory beyond surfaces: cycles, rational equivalence, Chow rings, Chern classes, and Riemann-Roch as a structured accounting system.",
        "visuals": [
            "Cycle dimension ladder and push-pull bookkeeping",
            "Chow ring multiplication table for projective space",
            "Chern class total-polynomial dashboard",
            "Riemann-Roch term ledger for a line bundle",
        ],
        "checks": [
            "projective-space Chow relation truncates powers above dimension",
            "Chern classes multiply in short exact sequence examples",
            "top-degree extraction matches intersection number",
            "Euler characteristic ledger matches a sample Hilbert polynomial",
        ],
        "terms": ["cycle", "Chow ring", "Chern class", "Riemann-Roch", "intersection product"],
    },
    {
        "kind": "appendix",
        "number": 7,
        "label": "Appendix B",
        "title": "Transcendental Methods",
        "folder": "appendix-b-transcendental-methods",
        "notebook": "appendix-b-transcendental-methods.ipynb",
        "artifact": "appendix-b",
        "printed_span": "438-448",
        "pdf_span": "453-463",
        "sections": "Analytic spaces; GAGA comparison; algebraicity criteria; Kahler manifolds; exponential sequence",
        "focus": "The bridge from algebraic varieties over the complex numbers to analytic spaces, comparison theorems, Kahler geometry, and the exponential sequence.",
        "visuals": [
            "Algebraic-to-analytic comparison ladder",
            "Sheaf comparison square for coherent data",
            "Kahler form local matrix positivity panel",
            "Exponential sequence winding-and-Chern-class diagram",
        ],
        "checks": [
            "transition from additive to multiplicative cocycle respects exponentiation in a toy cover",
            "Hermitian sample matrix is positive definite",
            "first Chern class ledger is integral in the toy example",
            "analytic and algebraic section dimensions are matched in a finite model",
        ],
        "terms": ["complex analytic space", "GAGA", "Kahler manifold", "exponential sequence", "Chern class"],
    },
    {
        "kind": "appendix",
        "number": 8,
        "label": "Appendix C",
        "title": "The Weil Conjectures",
        "folder": "appendix-c-weil-conjectures",
        "notebook": "appendix-c-weil-conjectures.ipynb",
        "artifact": "appendix-c",
        "printed_span": "449-458",
        "pdf_span": "464-473",
        "sections": "Zeta functions; history; l-adic cohomology; cohomological interpretation",
        "focus": "Finite-field point counting, zeta functions, cohomological explanations, Frobenius eigenvalues, and the shape of the Weil conjectures.",
        "visuals": [
            "Finite-field point-count table for projective examples",
            "Zeta function coefficient dashboard",
            "Frobenius eigenvalue circle schematic",
            "Cohomological trace formula dependency graph",
        ],
        "checks": [
            "P1 over Fq has q+1 projective points",
            "sample curve point counts feed the zeta exponential coefficients",
            "reciprocal-root magnitudes are marked against the expected weight",
            "trace formula signs match cohomological degree in the toy model",
        ],
        "terms": ["finite field", "zeta function", "Weil conjectures", "Frobenius", "l-adic cohomology", "trace formula"],
    },
]

AUXILIARY_SOURCE_MAP: list[dict[str, str]] = [
    {"label": "Introduction", "printed_span": "xiii-xvi", "pdf_span": "11-15"},
    {"label": "Bibliography", "printed_span": "459-469", "pdf_span": "474-484"},
    {"label": "Results from Algebra", "printed_span": "470-471", "pdf_span": "485-486"},
    {"label": "Glossary of Notations", "printed_span": "472-477", "pdf_span": "487-492"},
    {"label": "Index", "printed_span": "478-end", "pdf_span": "493-511"},
]


def canonical_notebooks(book_root: str | Path) -> list[Path]:
    root = Path(book_root)
    return [root / entry["folder"] / entry["notebook"] for entry in ENTRIES]


def source_map() -> dict[str, Any]:
    return {
        "title": BOOK_TITLE,
        "author": BOOK_AUTHOR,
        "series": SERIES,
        "pdf_source": PDF_SOURCE,
        "notes": SOURCE_SPAN_NOTES,
        "entries": ENTRIES,
        "auxiliary": AUXILIARY_SOURCE_MAP,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = source_map()
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(f"{BOOK_AUTHOR}, {BOOK_TITLE} ({SERIES})")
    for entry in ENTRIES:
        print(f"{entry['label']}: {entry['title']} (printed {entry['printed_span']} -> PDF {entry['pdf_span']})")
    print("Auxiliary source apparatus:")
    for entry in AUXILIARY_SOURCE_MAP:
        print(f"{entry['label']}: printed {entry['printed_span']} -> PDF {entry['pdf_span']}")


if __name__ == "__main__":
    main()

