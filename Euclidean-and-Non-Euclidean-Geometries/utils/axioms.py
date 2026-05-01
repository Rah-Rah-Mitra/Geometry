"""Structured, original summaries of axiom families used in the course."""

from __future__ import annotations


AXIOM_FAMILIES = {
    "incidence": [
        "points and lines are related by lies-on",
        "two suitable points determine a line",
        "there are enough points to avoid collapse into a one-point world",
    ],
    "order": [
        "betweenness makes a line behave like a one-dimensional ordering",
        "separation lets a line cut the plane into sides",
        "Pasch-type principles control how lines pass through triangles",
    ],
    "congruence": [
        "segments and angles can be transported",
        "triangle congruence can be used as a proof engine",
        "measurement is represented before coordinates are introduced",
    ],
    "continuity": [
        "nested or cut-like data have limiting points",
        "ruler and compass constructions do not leave gaps",
        "analytic models gain the completeness expected of the real line",
    ],
    "parallelism": [
        "Euclidean geometry chooses exactly one parallel through an external point",
        "hyperbolic geometry allows more than one parallel through an external point",
        "elliptic geometry allows no parallel through an external point",
    ],
}


MODEL_DICTIONARY = {
    "euclidean": "flat plane with zero curvature and unique parallels",
    "neutral": "incidence, order, congruence, and continuity without choosing a parallel axiom",
    "hyperbolic": "negative-curvature geometry modeled in disk or Klein coordinates",
    "elliptic": "positive-curvature geometry where antipodal points identify opposite directions",
    "finite incidence": "small combinatorial worlds that test which axioms are independent",
}


DEPENDENCIES = [
    ("incidence", "lines can be named by point pairs"),
    ("order", "segments, rays, and triangle interiors become meaningful"),
    ("congruence", "copying lengths and angles supports rigid proof steps"),
    ("continuity", "limiting constructions and coordinate models become complete"),
    ("parallelism", "angle sums and similarity split into Euclidean or hyperbolic behavior"),
]


def family_summary(name: str) -> str:
    items = AXIOM_FAMILIES[name]
    return "; ".join(items)

