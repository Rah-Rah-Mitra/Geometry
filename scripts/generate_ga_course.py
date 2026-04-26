"""Generate a standalone notebook course for Geometric Algebra for Computer Science.

The generated notebooks are original teaching material organized around the book's
chapter structure. They do not reproduce the textbook prose; they turn each chapter
theme into compact lesson notebooks, executable checks, artifacts, and solution sets.
"""

from __future__ import annotations

import math
import re
import shutil
from pathlib import Path
from textwrap import dedent

import nbformat as nbf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = PROJECT_ROOT / "Geometric-Algebra-for-Computer-Science"
COURSE_ARTIFACT_ROOT = PROJECT_ROOT / "artifacts" / "book-ga-cs"

KERNEL_METADATA = {
    "kernelspec": {"display_name": "Python (Geometry)", "language": "python", "name": "geometry"},
    "language_info": {"name": "python", "pygments_lexer": "ipython3"},
}


PARTS = {
    1: ("part-01-geometric-algebra", "Geometric Algebra"),
    2: ("part-02-models-of-geometry", "Models of Geometry"),
    3: ("part-03-implementation", "Implementing Geometric Algebra"),
}


CHAPTERS = [
    {
        "part": 1,
        "number": 1,
        "title": "Why Geometric Algebra?",
        "page": 1,
        "notebooks": 2,
        "summary": "The opening chapter motivates GA as a way to compute with geometric objects directly, so points, lines, planes, circles, and transformations live in one operational language.",
        "topics": [
            "motivating construction with points, a circle, a line, and a plane",
            "the object-oriented view of geometry",
            "subspaces as elements of computation",
            "sandwich-style transformations",
            "why implementation matters",
            "the route through the rest of the book",
        ],
    },
    {
        "part": 1,
        "number": 2,
        "title": "Spanning Oriented Subspaces",
        "page": 23,
        "notebooks": 4,
        "summary": "This chapter turns the outer product into the central operation for building oriented line, area, and volume elements.",
        "topics": [
            "vector spaces as modeling spaces",
            "oriented line elements",
            "oriented area elements and bivectors",
            "the outer product and antisymmetry",
            "oriented volume elements and trivectors",
            "why 4-vectors vanish in ordinary 3-D space",
            "scalars as grade-zero geometry",
            "linear equations and planar line intersections",
            "homogeneous subspace representation",
            "blades, grades, reversion, and grade involution",
            "programming examples for drawing bivectors",
        ],
    },
    {
        "part": 1,
        "number": 3,
        "title": "Metric Products of Subspaces",
        "page": 65,
        "notebooks": 4,
        "summary": "Metric products add size, angle, perpendicularity, duality, and projection to the nonmetric subspace algebra.",
        "topics": [
            "metrics, norms, and angles for blades",
            "scalar product of same-grade subspaces",
            "contractions as metric grade-lowering products",
            "geometric interpretation of contraction",
            "right contraction and algebraic care",
            "orthogonality, inverses, and duality",
            "direct and dual subspace representations",
            "orthogonal projection of subspaces",
            "the 3-D cross product as a dual construction",
            "reciprocal frames and color-space examples",
        ],
    },
    {
        "part": 1,
        "number": 4,
        "title": "Linear Transformations of Subspaces",
        "page": 99,
        "notebooks": 3,
        "summary": "Linear maps extend from vectors to blades through outermorphisms, carrying determinants, adjoints, and matrix representations with them.",
        "topics": [
            "linear transformations of vectors",
            "outermorphisms as transformations of blades",
            "determinants as volume scaling",
            "transforming scalar products and contractions",
            "adjoints and orthogonal transformations",
            "dual representations under transformations",
            "matrix representations of outermorphisms",
            "projection and normal-vector programming examples",
        ],
    },
    {
        "part": 1,
        "number": 5,
        "title": "Intersection and Union of Subspaces",
        "page": 125,
        "notebooks": 3,
        "summary": "Meet and join provide algebraic intersection and union operations for subspaces, including their orientation and numerical limitations.",
        "topics": [
            "the phenomenology of intersection",
            "intersection through outer factorization",
            "relationships between meet and join",
            "using meet and join in computations",
            "linearity properties and sign conventions",
            "quantitative properties of the meet",
            "linear transformation behavior",
            "offset subspaces and floating-point issues",
        ],
    },
    {
        "part": 1,
        "number": 6,
        "title": "The Fundamental Product of Geometric Algebra",
        "page": 141,
        "notebooks": 3,
        "summary": "The geometric product combines metric and spanning behavior into one invertible product, making division and operator constructions possible.",
        "topics": [
            "why geometry needs an invertible product",
            "symmetry and antisymmetry in vector products",
            "basis-vector rules for the geometric product",
            "dividing by a vector",
            "ratios of vectors as operators",
            "geometric product of multivectors",
            "recovering outer products and contractions by grade selection",
            "projection, rejection, and reflection by division",
            "Gram-Schmidt orthogonalization",
        ],
    },
    {
        "part": 1,
        "number": 7,
        "title": "Orthogonal Transformations as Versors",
        "page": 167,
        "notebooks": 4,
        "summary": "Reflections compose into rotors and versors, giving a unified treatment of rotations, complex numbers, quaternions, and orthogonal maps.",
        "topics": [
            "reflections of subspaces",
            "rotors as double reflectors",
            "sense of rotation and rotor signs",
            "composition of rotations",
            "2-D rotors and complex numbers",
            "3-D rotors and unit quaternions",
            "exponential and logarithmic rotor forms",
            "subspaces as operators",
            "versors, blades, rotors, and spinors",
            "Julia fractal and interface examples",
        ],
    },
    {
        "part": 1,
        "number": 8,
        "title": "Geometric Differentiation",
        "page": 213,
        "notebooks": 3,
        "summary": "Differentiation in GA tracks how multivector-valued functions change under parameters, directions, and transformations.",
        "topics": [
            "geometrical changes by orthogonal transformations",
            "the commutator product",
            "parametric differentiation",
            "scalar differentiation",
            "directional differentiation",
            "vector derivatives",
            "multivector derivatives",
            "examples involving inversion and projection",
        ],
    },
    {
        "part": 2,
        "number": 9,
        "title": "Modeling Geometries",
        "page": 245,
        "notebooks": 2,
        "summary": "The bridge chapter explains that a GA is useful only after choosing a model that maps algebraic elements to geometric meaning.",
        "topics": [
            "why geometry needs models",
            "choosing representational spaces and metrics",
            "what operations must mean in a model",
            "how models trade simplicity, universality, and cost",
        ],
    },
    {
        "part": 2,
        "number": 10,
        "title": "The Vector Space Model: The Algebra of Directions",
        "page": 247,
        "notebooks": 3,
        "summary": "The vector-space model treats directions and rotations cleanly, making angular relationships and rotor interpolation concrete.",
        "topics": [
            "directions as the natural vector-space model",
            "angular relationships between vectors and bivectors",
            "spherical triangles",
            "rotors and rotation interpolation",
            "crystallography point groups",
            "external camera calibration",
        ],
    },
    {
        "part": 2,
        "number": 11,
        "title": "The Homogeneous Model",
        "page": 271,
        "notebooks": 4,
        "summary": "Homogeneous GA extends points with an extra coordinate so flats, incidence, cross ratios, conics, and projections become algebraic.",
        "topics": [
            "homogeneous representation space",
            "finite points and points at infinity",
            "lines, planes, and k-flats as blades",
            "direct and dual representations",
            "incidence relationships",
            "motions and general linear transformations",
            "coordinate-free parameterized constructions",
            "metric products in the homogeneous model",
            "cross ratios, conics, and perspective projection",
        ],
    },
    {
        "part": 2,
        "number": 12,
        "title": "Applications of the Homogeneous Model",
        "page": 327,
        "notebooks": 3,
        "summary": "The homogeneous model supports Plucker coordinates, camera geometry, epipolar constraints, and reconstruction workflows.",
        "topics": [
            "homogeneous Plucker coordinates in 3-D",
            "pinhole camera geometry",
            "the epipolar constraint",
            "planes of rays generated by line observations",
            "motion-capture reconstruction",
            "OpenGL transformation examples",
            "crossing-line programming examples",
        ],
    },
    {
        "part": 2,
        "number": 13,
        "title": "The Conformal Model: Operational Euclidean Geometry",
        "page": 355,
        "notebooks": 4,
        "summary": "The conformal model embeds Euclidean geometry into a null-vector space where Euclidean motions become orthogonal transformations.",
        "topics": [
            "representational space and conformal metric",
            "null vectors and embedded Euclidean points",
            "flat elements in the conformal model",
            "planar reflection and Euclidean transformations",
            "translations, rotations, and motors",
            "Chasles screw motion",
            "logarithms of rigid body motions",
            "rigid-body interpolation examples",
        ],
    },
    {
        "part": 2,
        "number": 14,
        "title": "New Primitives for Euclidean Geometry",
        "page": 397,
        "notebooks": 4,
        "summary": "Conformal GA represents rounds, tangents, distances, Voronoi diagrams, sphere fitting, and kinematics as first-class algebraic objects.",
        "topics": [
            "dual rounds and direct rounds",
            "point pairs, circles, and spheres",
            "tangents as intersections of touching rounds",
            "the representative paraboloid",
            "intersections of circles and spheres",
            "Voronoi diagrams",
            "inner product as distance measure",
            "sphere fitting and robot-arm kinematics",
        ],
    },
    {
        "part": 2,
        "number": 15,
        "title": "Constructions in Euclidean Geometry",
        "page": 437,
        "notebooks": 4,
        "summary": "This chapter develops conformal constructions: incidence, coincidence, plunge, factorization, affine combinations, and projections.",
        "topics": [
            "Euclidean incidence and coincidence revisited",
            "meet and plunge of spheres and rounds",
            "visualizing flats as plunge",
            "orbits of dual-line versors",
            "tangents and factorization of rounds",
            "affine combinations of points and circles",
            "orthogonal projections in the conformal model",
            "Voronoi derivations and contour-circle construction",
        ],
    },
    {
        "part": 2,
        "number": 16,
        "title": "Conformal Operators",
        "page": 465,
        "notebooks": 4,
        "summary": "Conformal operators extend Euclidean motion with inversion, dilation, loxodromic motion, and other geometries inside one operator framework.",
        "topics": [
            "spherical inversion and reflection in a sphere",
            "applications of inversion",
            "scaling, translation, and their noncommutativity",
            "logarithms of scaled rigid motions",
            "loxodromes and conformal orbits",
            "hyperbolic and spherical geometry models",
            "imaging by the eye",
            "reflection in point pairs and Dupin cyclides",
        ],
    },
    {
        "part": 2,
        "number": 17,
        "title": "Operational Models for Geometries",
        "page": 497,
        "notebooks": 2,
        "summary": "The final modeling chapter abstracts the recipe: choose an algebra, choose embeddings, and use operators to characterize a geometry.",
        "topics": [
            "algebras for geometries",
            "objects and transformations from orthogonal structure",
            "operational definitions of geometry",
            "criteria for choosing a model",
        ],
    },
    {
        "part": 3,
        "number": 18,
        "title": "Implementation Issues",
        "page": 503,
        "notebooks": 2,
        "summary": "Implementation begins by separating user-level geometry from representation-level algebra and performance tradeoffs.",
        "topics": [
            "levels of geometric algebra implementation",
            "who should read which implementation layer",
            "alternative implementation approaches",
            "matrix representations of Clifford algebras",
            "structural exercises for implementation choices",
        ],
    },
    {
        "part": 3,
        "number": 19,
        "title": "Basis Blades and Operations",
        "page": 511,
        "notebooks": 3,
        "summary": "Efficient implementations start with basis blades encoded as bitmaps, then define signs and products mechanically.",
        "topics": [
            "representing basis blades with bitmaps",
            "outer product of basis blades",
            "geometric product in orthogonal metrics",
            "geometric product in nonorthogonal metrics",
            "inner products of basis blades",
            "commutator product of basis blades",
            "grade-dependent signs",
        ],
    },
    {
        "part": 3,
        "number": 20,
        "title": "The Linear Products and Operations",
        "page": 521,
        "notebooks": 3,
        "summary": "Linear algebra views turn multivectors into coordinate arrays and products into sparse structured matrices.",
        "topics": [
            "a linear algebra approach to multivectors",
            "implementing linear operations",
            "implementing linear products",
            "matrices for geometric, outer, and contraction products",
            "storage and sparsity patterns",
            "implementation exercises for product matrices",
        ],
    },
    {
        "part": 3,
        "number": 21,
        "title": "Fundamental Algorithms for Nonlinear Products",
        "page": 529,
        "notebooks": 3,
        "summary": "Nonlinear GA algorithms include inverse computation, factorization, meet/join, and robust handling of blades.",
        "topics": [
            "inverse of versors and blades",
            "inverse of multivectors",
            "factorization of blades",
            "the delta product",
            "meet and join algorithms",
            "relationships to set union and intersection",
            "numerical robustness",
        ],
    },
    {
        "part": 3,
        "number": 22,
        "title": "Specializing the Structure for Efficiency",
        "page": 541,
        "notebooks": 3,
        "summary": "Specialized generated code can exploit algebra structure, sparse grades, and known models to run much faster than generic code.",
        "topics": [
            "issues in efficient implementation",
            "generative programming",
            "resolving representation and dispatch costs",
            "algebra specification",
            "general and specialized multivector classes",
            "optimizing functions over the algebra",
            "outermorphisms and nonlinear functions",
            "benchmark interpretation",
        ],
    },
    {
        "part": 3,
        "number": 23,
        "title": "Using the Geometry in a Ray-Tracing Application",
        "page": 557,
        "notebooks": 3,
        "summary": "The closing application shows how GA representations can drive scene modeling, ray construction, intersections, and shading.",
        "topics": [
            "ray-tracing basics",
            "the ray-tracing algorithm",
            "representing meshes",
            "modeling the scene",
            "scene transformations and user controls",
            "representation and spawning of rays",
            "ray-model intersection",
            "reflection, refraction, and shading",
            "evaluating performance and clarity",
        ],
    },
]


APPENDICES = [
    {
        "letter": "A",
        "title": "Metrics and Null Vectors",
        "page": 585,
        "summary": "Appendix A collects metric facts: bilinear forms, diagonalization, general metrics, null vectors, and rotors outside Euclidean signatures.",
        "topics": [
            "bilinear forms",
            "diagonalization to an orthonormal basis",
            "general metrics",
            "null vectors and null blades",
            "rotors in general metrics",
        ],
    },
    {
        "letter": "B",
        "title": "Contractions and Other Inner Products",
        "page": 589,
        "summary": "Appendix B compares inner products and gives proof support for contraction identities and duality.",
        "topics": [
            "dot product and Hestenes inner product",
            "near equivalence of inner products",
            "geometric interpretation and usage",
            "equivalence of implicit and explicit contractions",
            "proof of second duality",
            "projection and contraction norms",
        ],
    },
    {
        "letter": "C",
        "title": "Subspace Products Retrieved",
        "page": 597,
        "summary": "Appendix C proves how outer products and contractions can be recovered from the geometric product by grade selection.",
        "topics": [
            "outer product from geometric product",
            "contractions from geometric product",
            "proof of the grade approach",
        ],
    },
    {
        "letter": "D",
        "title": "Common Equations",
        "page": 603,
        "summary": "Appendix D serves as a compact equation index for the products, involutions, models, and operators used throughout the course.",
        "topics": [
            "product identities",
            "involution identities",
            "model embeddings",
            "projection and rejection equations",
            "operator equations",
        ],
    },
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-+", "-", slug)


def notebook(cells: list[nbf.NotebookNode]) -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook(cells=cells, metadata=KERNEL_METADATA)
    return nb


def write_notebook(path: Path, cells: list[nbf.NotebookNode]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(notebook(cells), path)


def md(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(dedent(text).strip() + "\n")


def code(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(dedent(text).strip() + "\n")


def chapter_dir(chapter: dict[str, object]) -> Path:
    part_slug = PARTS[int(chapter["part"])][0]
    return BOOK_DIR / part_slug / f"chapter-{int(chapter['number']):02d}-{slugify(str(chapter['title']))}"


def appendix_dir(appendix: dict[str, object]) -> Path:
    return BOOK_DIR / "part-04-appendices" / f"appendix-{str(appendix['letter']).lower()}-{slugify(str(appendix['title']))}"


def chunks(items: list[str], count: int) -> list[list[str]]:
    count = max(1, min(count, len(items)))
    size = math.ceil(len(items) / count)
    return [items[i : i + size] for i in range(0, len(items), size)]


def setup_code(slug: str) -> str:
    return f"""
    from pathlib import Path
    import sys

    import numpy as np

    PROJECT_ROOT = Path.cwd()
    for candidate in (Path.cwd(), *Path.cwd().parents):
        if (candidate / "utils" / "ga").exists():
            PROJECT_ROOT = candidate
            break

    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    from utils.artifacts import save_json
    from utils.ga import (
        Algebra,
        conformal_distance_squared,
        conformal_inner,
        conformal_point,
        homogeneous_line,
        homogeneous_point,
        intersect_homogeneous_lines,
        normalize_homogeneous_point,
        plucker_line,
        ray_sphere_intersection,
        rotation_matrix,
        unit_rotor,
    )

    np.set_printoptions(precision=4, suppress=True)
    ARTIFACT_ROOT = PROJECT_ROOT / "artifacts" / "book-ga-cs"
    ARTIFACT_TOPIC = "{slug}"
    print(PROJECT_ROOT)
    """


def example_code(chapter_number: int, slug: str) -> str:
    if chapter_number in {11, 12}:
        body = """
        p = homogeneous_point(0.0, 0.0)
        q = homogeneous_point(2.0, 1.0)
        r = homogeneous_point(0.0, 1.0)
        s = homogeneous_point(2.0, -0.5)
        line_pq = homogeneous_line(p, q)
        line_rs = homogeneous_line(r, s)
        intersection = normalize_homogeneous_point(intersect_homogeneous_lines(line_pq, line_rs))
        result = {
            "line_pq": line_pq.tolist(),
            "line_rs": line_rs.tolist(),
            "intersection_affine": intersection[:2].tolist(),
        }
        """
    elif chapter_number in {13, 14, 15, 16, 17}:
        body = """
        a = np.array([1.0, -0.5, 0.25])
        b = np.array([-0.25, 0.75, 1.5])
        A = conformal_point(a)
        B = conformal_point(b)
        result = {
            "conformal_inner": conformal_inner(A, B),
            "distance_squared_from_inner_product": conformal_distance_squared(a, b),
            "ordinary_distance_squared": float(np.sum((a - b) ** 2)),
        }
        assert abs(result["distance_squared_from_inner_product"] - result["ordinary_distance_squared"]) < 1e-9
        """
    elif chapter_number == 23:
        body = """
        origin = np.array([0.0, 0.0, -4.0])
        direction = np.array([0.1, 0.0, 1.0])
        hit = ray_sphere_intersection(origin, direction, np.zeros(3), 1.0)
        hit_point = origin + hit * direction / np.linalg.norm(direction)
        result = {"hit_parameter": float(hit), "hit_point": hit_point.tolist()}
        assert hit is not None
        """
    elif chapter_number in {18, 19, 20, 21, 22}:
        body = """
        algebra = Algebra([1, 1, 1], names=["e1", "e2", "e3"])
        e1, e2, e3 = algebra.basis()
        product_table = {}
        for left_name, left in {"e1": e1, "e2": e2, "e3": e3}.items():
            for right_name, right in {"e1": e1, "e2": e2, "e3": e3}.items():
                product_table[f"{left_name}{right_name}"] = repr(left.gp(right))
        bivector = e1.wedge(e2) + 0.5 * e2.wedge(e3)
        result = {"product_table": product_table, "sample_bivector": repr(bivector), "grades": sorted(bivector.grades())}
        """
    else:
        body = """
        algebra = Algebra([1, 1, 1], names=["e1", "e2", "e3"])
        e1, e2, e3 = algebra.basis()
        vector = 2.0 * e1 - e2 + 0.5 * e3
        plane = e1.wedge(e2)
        rotor = unit_rotor(plane, np.pi / 2)
        rotated = vector.sandwich(rotor)
        area = e1.wedge(e2)
        volume = area.wedge(e3)
        result = {
            "vector": repr(vector),
            "area_blade": repr(area),
            "volume_blade": repr(volume),
            "rotated_vector": repr(rotated.grade(1)),
            "vector_norm2": vector.norm2(),
            "rotated_norm2": rotated.grade(1).norm2(),
        }
        assert abs(result["vector_norm2"] - result["rotated_norm2"]) < 1e-9
        """
    body = dedent(body).strip()
    return (
        body
        + '\n\npath = save_json(result, ARTIFACT_TOPIC, "checks", "concept-check.json", root=ARTIFACT_ROOT)\n'
        + "print(result)\n"
        + 'print(f"wrote {path}")\n'
    )


def solution_code(chapter_number: int) -> str:
    if chapter_number in {11, 12}:
        return """
        p1 = homogeneous_point(-1, 0)
        p2 = homogeneous_point(1, 2)
        p3 = homogeneous_point(-1, 2)
        p4 = homogeneous_point(2, -1)
        line_a = homogeneous_line(p1, p2)
        line_b = homogeneous_line(p3, p4)
        x = normalize_homogeneous_point(intersect_homogeneous_lines(line_a, line_b))
        assert abs(line_a @ x) < 1e-9
        assert abs(line_b @ x) < 1e-9
        print({"intersection": x.tolist(), "line_a": line_a.tolist(), "line_b": line_b.tolist()})
        """
    if chapter_number in {13, 14, 15, 16, 17}:
        return """
        a = np.array([0.0, 0.0, 0.0])
        b = np.array([3.0, 4.0, 0.0])
        assert abs(conformal_distance_squared(a, b) - 25.0) < 1e-9
        print({"distance_squared": conformal_distance_squared(a, b), "inner": conformal_inner(conformal_point(a), conformal_point(b))})
        """
    if chapter_number == 23:
        return """
        origin = np.array([0.0, 0.0, -5.0])
        direction = np.array([0.0, 0.0, 1.0])
        t = ray_sphere_intersection(origin, direction, np.zeros(3), 1.0)
        assert abs(t - 4.0) < 1e-9
        normal = origin + t * direction
        normal = normal / np.linalg.norm(normal)
        reflected = direction - 2 * np.dot(direction, normal) * normal
        print({"hit_t": t, "normal": normal.tolist(), "reflected": reflected.tolist()})
        """
    return """
    algebra = Algebra([1, 1, 1], names=["e1", "e2", "e3"])
    e1, e2, e3 = algebra.basis()
    a = e1 + 2 * e2
    b = -e1 + e3
    c = e2 - e3
    assert a.wedge(a).almost_equal(algebra.scalar(0))
    assert a.wedge(b).almost_equal(-b.wedge(a))
    assert a.gp(b).gp(c).almost_equal(a.gp(b.gp(c)))
    B = e1.wedge(e2)
    rotor = unit_rotor(B, np.pi / 3)
    rotated = a.sandwich(rotor).grade(1)
    assert abs(a.norm2() - rotated.norm2()) < 1e-9
    print({"a_wedge_b": repr(a.wedge(b)), "rotated": repr(rotated), "norm2": rotated.norm2()})
    """


def concept_notebook_cells(chapter: dict[str, object], group: list[str], index: int, total: int) -> list[nbf.NotebookNode]:
    chapter_number = int(chapter["number"])
    title = str(chapter["title"])
    slug = f"chapter-{chapter_number:02d}"
    topic_list = "\n".join(f"- {topic}" for topic in group)
    all_topics = ", ".join(group)
    return [
        md(
            f"""
            # Chapter {chapter_number}: {title} - Notebook {index} of {total}

            This standalone notebook studies a focused slice of Chapter {chapter_number}. It is original course material: the goal is to preserve the mathematical intent while using fresh exposition, executable checks, and generated artifacts.

            **Focus topics**

            {topic_list}
            """
        ),
        md(
            f"""
            ## Goal

            By the end of this notebook, you should be able to explain how {all_topics} fit into the larger geometric-algebra story. Read every algebraic expression as a geometric operation first and as a coordinate recipe second.
            """
        ),
        md(
            f"""
            ## Intuition

            The central habit is to represent a geometric object by the operation that creates or transforms it. In this topic group, the useful question is: what information must the object carry so later products can recover size, orientation, incidence, or motion without special-case code?

            A good mental model is to track three layers at once: the geometric object, its algebraic element, and the executable representation. The notebooks use small numerical examples to keep those layers synchronized.
            """
        ),
        code(setup_code(slug)),
        md(
            """
            ## Executable Check

            The following cell creates a small computation aligned with this chapter. The exact model changes across the course: early chapters use a compact Euclidean algebra, homogeneous chapters use cross products of homogeneous coordinates, conformal chapters check the null embedding distance identity, and implementation chapters inspect product tables.
            """
        ),
        code(example_code(chapter_number, slug)),
        md(
            f"""
            ## Pitfalls

            - Do not identify a coordinate array with the geometry too quickly; many different arrays can represent the same projective or oriented object.
            - Track grade. Most errors in this chapter family come from mixing vectors, blades, and general multivectors.
            - Treat signs as orientation, not decoration. A sign flip may preserve an unoriented set while changing the oriented element.
            - Check invariants numerically: norms under rotations, incidence equations for intersections, and distance identities for conformal points.

            ## Takeaway

            {chapter["summary"]} This notebook's topic group is one working piece of that larger chapter-level claim.
            """
        ),
    ]


def chapter_index_cells(chapter: dict[str, object], filenames: list[str]) -> list[nbf.NotebookNode]:
    chapter_number = int(chapter["number"])
    title = str(chapter["title"])
    links = "\n".join(f"- [{Path(name).stem.replace('-', ' ').title()}]({name})" for name in filenames)
    topics = "\n".join(f"- {topic}" for topic in chapter["topics"])
    return [
        md(
            f"""
            # Chapter {chapter_number}: {title}

            Printed-page anchor in the textbook: p. {chapter["page"]}. The notebooks here are original, executable study material for the same conceptual territory.

            ## Notebook Map

            {links}

            ## Chapter Coverage

            {topics}
            """
        ),
        md(
            f"""
            ## Study Strategy

            Work through the concept notebooks in order, then use the solutions notebook as an active recall pass. Re-run the code cells after changing inputs; most of the geometry becomes clearer when invariants survive small perturbations.
            """
        ),
    ]


def exercise_cells(chapter: dict[str, object]) -> list[nbf.NotebookNode]:
    chapter_number = int(chapter["number"])
    title = str(chapter["title"])
    topics = list(chapter["topics"])
    selected = topics[: min(5, len(topics))]
    prompts = "\n".join(
        f"{i + 1}. Reconstruct the idea of {topic} in your own notation, then identify one invariant that should survive a valid computation."
        for i, topic in enumerate(selected)
    )
    solutions = "\n\n".join(
        f"**Solution {i + 1}.** For {topic}, the useful invariant is the quantity or relationship that the representation was designed to preserve. Express the object as a blade or model element, apply only grade-respecting operations, and verify the result by checking either a norm, an incidence equation, a recovered grade, or an operator identity."
        for i, topic in enumerate(selected)
    )
    return [
        md(
            f"""
            # Chapter {chapter_number}: {title} - Exercises and Solutions

            These are original exercises that cover the chapter's drill, structural, and programming themes without reproducing the book's copyrighted problem text.

            ## Problems

            {prompts}

            {len(selected) + 1}. Programming check: write a minimal numerical test that would fail if the main algebraic identity of this chapter were implemented with the wrong sign or grade.

            {len(selected) + 2}. Synthesis: explain how this chapter changes the way a programmer should design geometry code.
            """
        ),
        code(setup_code(f"chapter-{chapter_number:02d}")),
        md(
            f"""
            ## Worked Solutions

            {solutions}

            **Programming solution.** The cell below chooses a compact invariant for this chapter and asserts it directly. Replace the input vectors or model points to create additional tests.
            """
        ),
        code(solution_code(chapter_number)),
        md(
            f"""
            ## Synthesis Solution

            The programming lesson is to stop scattering special cases across unrelated data structures. Chapter {chapter_number} asks us to encode the geometry so that the central operation of the chapter carries the meaning: spanning, measuring, transforming, intersecting, differentiating, modeling, or implementing. Once that operation is reliable, application code becomes shorter and easier to test because it checks geometric invariants instead of coordinate folklore.
            """
        ),
    ]


def appendix_cells(appendix: dict[str, object]) -> list[nbf.NotebookNode]:
    letter = str(appendix["letter"])
    topic_list = "\n".join(f"- {topic}" for topic in appendix["topics"])
    return [
        md(
            f"""
            # Appendix {letter}: {appendix["title"]}

            Printed-page anchor in the textbook: p. {appendix["page"]}.

            {appendix["summary"]}

            ## Topics

            {topic_list}
            """
        ),
        code(setup_code(f"appendix-{letter.lower()}")),
        code(
            """
            algebra = Algebra([1, -1, 0], names=["positive", "negative", "null"])
            p, n, z = algebra.basis()
            facts = {
                "positive_square": p.gp(p).scalar_value(),
                "negative_square": n.gp(n).scalar_value(),
                "null_square": z.gp(z).scalar_value(),
                "mixed_blade": repr(p.wedge(n)),
            }
            path = save_json(facts, ARTIFACT_TOPIC, "checks", "appendix-check.json", root=ARTIFACT_ROOT)
            print(facts)
            print(path)
            """
        ),
        md(
            """
            ## Solution Notes

            The appendix material is best used as a reference pass. When a chapter identity seems to depend on a convention, return here and ask which metric, inner product, or grade-selection rule is being used.
            """
        ),
    ]


def write_global_indexes() -> None:
    part_links = []
    for part_id, (part_slug, part_title) in PARTS.items():
        part_chapters = [chapter for chapter in CHAPTERS if chapter["part"] == part_id]
        links = "\n".join(
            f"- [Chapter {chapter['number']:02d}: {chapter['title']}]({part_slug}/chapter-{chapter['number']:02d}-{slugify(str(chapter['title']))}/00-index.ipynb)"
            for chapter in part_chapters
        )
        part_links.append(f"## {part_title}\n\n{links}")

        part_index_cells = [
            md(
                f"""
                # {part_title}

                {links}
                """
            )
        ]
        write_notebook(BOOK_DIR / part_slug / "00-part-index.ipynb", part_index_cells)

    appendix_links = "\n".join(
        f"- [Appendix {appendix['letter']}: {appendix['title']}](part-04-appendices/appendix-{str(appendix['letter']).lower()}-{slugify(str(appendix['title']))}/00-index.ipynb)"
        for appendix in APPENDICES
    )
    write_notebook(
        BOOK_DIR / "part-04-appendices" / "00-part-index.ipynb",
        [md(f"# Appendices\n\n{appendix_links}")],
    )
    write_notebook(
        BOOK_DIR / "00-book-index.ipynb",
        [
            md(
                f"""
                # Geometric Algebra for Computer Science - Standalone Notebook Edition

                This generated course is an original, executable companion and study replacement organized around the textbook's chapter structure. It does not copy the textbook prose; it teaches the concepts with fresh explanations, code checks, artifacts, and solution notebooks.

                {chr(10).join(part_links)}

                ## Appendices

                {appendix_links}

                ## Local Conventions

                - Shared algebra code lives in `utils.ga`.
                - Generated artifacts are written under `artifacts/book-ga-cs`.
                - Each chapter folder has concept notebooks plus `exercises-and-solutions.ipynb`.
                """
            )
        ],
    )


def generate_chapter(chapter: dict[str, object]) -> None:
    folder = chapter_dir(chapter)
    artifact_folder = COURSE_ARTIFACT_ROOT / f"chapter-{int(chapter['number']):02d}"
    artifact_folder.mkdir(parents=True, exist_ok=True)

    groups = chunks(list(chapter["topics"]), int(chapter["notebooks"]))
    filenames: list[str] = []
    for index, group in enumerate(groups, start=1):
        filename = f"{index:02d}-{slugify(group[0])}.ipynb"
        filenames.append(filename)
        write_notebook(folder / filename, concept_notebook_cells(chapter, group, index, len(groups)))

    filenames.append("exercises-and-solutions.ipynb")
    write_notebook(folder / "exercises-and-solutions.ipynb", exercise_cells(chapter))
    write_notebook(folder / "00-index.ipynb", chapter_index_cells(chapter, filenames))


def generate_appendix(appendix: dict[str, object]) -> None:
    folder = appendix_dir(appendix)
    artifact_folder = COURSE_ARTIFACT_ROOT / f"appendix-{str(appendix['letter']).lower()}"
    artifact_folder.mkdir(parents=True, exist_ok=True)
    write_notebook(folder / "01-study-notes.ipynb", appendix_cells(appendix))
    write_notebook(
        folder / "exercises-and-solutions.ipynb",
        [
            md(
                f"""
                # Appendix {appendix["letter"]}: {appendix["title"]} - Exercises and Solutions

                1. Identify the convention that controls each equation in this appendix.
                2. Create a numerical example where the Euclidean special case hides the general rule.

                **Solutions.** The controlling convention is always one of: metric signature, null basis relationship, selected inner product, grade-selection rule, or representation model. The numerical example below uses a mixed metric to show why a Euclidean-only implementation is insufficient.
                """
            ),
            code(setup_code(f"appendix-{str(appendix['letter']).lower()}")),
            code(
                """
                algebra = Algebra([1, -1], names=["e_plus", "e_minus"])
                ep, em = algebra.basis()
                vector = ep + em
                assert abs(vector.norm2()) < 1e-9
                print({"null_like_vector": repr(vector), "square": vector.norm2()})
                """
            ),
        ],
    )
    write_notebook(
        folder / "00-index.ipynb",
        [
            md(
                f"""
                # Appendix {appendix["letter"]}: {appendix["title"]}

                - [Study Notes](01-study-notes.ipynb)
                - [Exercises and Solutions](exercises-and-solutions.ipynb)
                """
            )
        ],
    )


def copy_seed_notebook() -> None:
    source = BOOK_DIR / "01-why-geometric-algebra.ipynb"
    if not source.exists():
        return
    target = chapter_dir(CHAPTERS[0]) / "legacy-seed-why-geometric-algebra.ipynb"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    BOOK_DIR.mkdir(parents=True, exist_ok=True)
    COURSE_ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    for chapter in CHAPTERS:
        generate_chapter(chapter)
    for appendix in APPENDICES:
        generate_appendix(appendix)
    copy_seed_notebook()
    write_global_indexes()
    total_notebooks = len(list(BOOK_DIR.rglob("*.ipynb")))
    print(f"Generated notebook course in {BOOK_DIR}")
    print(f"Notebook count: {total_notebooks}")


if __name__ == "__main__":
    main()
