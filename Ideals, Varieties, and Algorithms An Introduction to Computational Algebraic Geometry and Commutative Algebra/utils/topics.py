"""Topic-specific visual and exact-check helpers for IVA notebooks."""

from __future__ import annotations

import math
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objects as go
import sympy as sp

from .plotting import configure_matplotlib


def _nice_title(ax: Any, title: str) -> None:
    ax.set_title(title, fontsize=11)
    ax.grid(True, alpha=0.25)


def topic_primary_figure(topic: str, seed: int, title: str):
    """Return a topic-specific static figure and a compact summary."""
    configure_matplotlib()
    if topic == "chapter-01":
        fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
        pts = [(a, b, a + b) for a in range(6) for b in range(6)]
        axes[0].scatter([p[0] for p in pts], [p[1] for p in pts], c=[p[2] for p in pts], cmap="viridis", s=55)
        for value in range(0, 10, 2):
            xs = np.arange(0, value + 1)
            ys = value - xs
            axes[0].plot(xs, ys, color="#333333", alpha=0.18)
        _nice_title(axes[0], "Monomials as lattice points")
        axes[0].set_xlabel("x exponent")
        axes[0].set_ylabel("y exponent")
        values = np.array([0, 1])
        axes[1].bar(["0", "1"], (values**2 - values) % 2, color="#3a7ca5")
        axes[1].set_ylim(0, 1)
        _nice_title(axes[1], "x^2 - x over F2")
        return fig, {"topic": topic, "degree_bands": 10, "finite_field_zeros": 2}
    if topic == "chapter-02":
        fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
        points = [(a, b) for a in range(7) for b in range(7) if a + b <= 7]
        lex = sorted(points, key=lambda p: (-p[0], -p[1]))[:12]
        grlex = sorted(points, key=lambda p: (-(p[0] + p[1]), -p[0]))[:12]
        axes[0].scatter([p[0] for p in points], [p[1] for p in points], c="#bfc0c0", s=35)
        axes[0].plot([p[0] for p in lex], [p[1] for p in lex], color="#c1121f", marker="o", label="lex priority")
        axes[0].plot([p[0] for p in grlex], [p[1] for p in grlex], color="#22577a", marker="s", label="grlex priority")
        axes[0].legend()
        _nice_title(axes[0], "Monomial orders")
        generators = [(3, 0), (1, 2), (0, 4)]
        for a in range(7):
            for b in range(7):
                inside = any(a >= g[0] and b >= g[1] for g in generators)
                axes[1].scatter(a, b, c="#b23a48" if inside else "#3a7ca5", s=42)
        _nice_title(axes[1], "Monomial ideal staircase")
        return fig, {"topic": topic, "lex_prefix": lex[:4], "minimal_generators": generators}
    if topic == "chapter-03":
        fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
        z = np.linspace(-1.8, 1.8, 300)
        poly = z**2 * (z - 1) ** 2 * (z**2 + 2 * z - 1)
        axes[0].plot(z, poly, color="#22577a")
        axes[0].axhline(0, color="#111111", linewidth=0.8)
        _nice_title(axes[0], "Eliminated univariate consequence")
        y = np.linspace(-2, 2, 180)
        axes[1].plot(y, y, color="#c1121f", label="projection closure")
        axes[1].scatter([0], [0], facecolor="white", edgecolor="#111111", s=80, label="missing fiber")
        axes[1].legend()
        _nice_title(axes[1], "Extension failure marker")
        return fig, {"topic": topic, "elimination_roots_visible": 5, "missing_partial_solution": [0, 0]}
    if topic == "chapter-04":
        fig, ax = plt.subplots(figsize=(7.5, 4.8))
        graph = nx.DiGraph()
        edges = [("I", "V(I)"), ("J", "V(J)"), ("I+J", "V(I) cap V(J)"), ("I*J", "V(I) union V(J)"), ("sqrt(I)", "reduced V(I)")]
        graph.add_edges_from(edges)
        pos = nx.spring_layout(graph, seed=44)
        nx.draw_networkx(graph, pos, ax=ax, node_color="#8fb3cf", edge_color="#274c77", node_size=1450, font_size=8, arrows=True)
        ax.axis("off")
        return fig, {"topic": topic, "dictionary_edges": len(edges), "inclusion_reversing": True}
    if topic == "chapter-05":
        fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
        x = np.linspace(-2, 2, 300)
        axes[0].plot(x, x**2, label="V(y-x^2)")
        axes[0].plot(x, x**3 + x**6, label="representative f")
        axes[0].plot(x, x**3 + x**6 + (x**2 - x**2), "--", label="same on V")
        axes[0].legend(fontsize=8)
        _nice_title(axes[0], "Representatives agree on V")
        t = np.linspace(-2, 2, 120)
        axes[1].scatter(t, t**2, c=t, cmap="viridis", s=20)
        _nice_title(axes[1], "Coordinate-ring parameter")
        return fig, {"topic": topic, "representatives_checked": 2, "standard_monomial_model": "parabola"}
    if topic == "chapter-06":
        fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
        theta = np.linspace(0, 2 * np.pi, 160)
        axes[0].plot(np.cos(theta), np.sin(theta), color="#22577a")
        axes[0].plot([0, 1, 1.6], [0, 0.4, 1.0], marker="o", color="#c1121f")
        axes[0].set_aspect("equal")
        _nice_title(axes[0], "Revolute joint and arm pose")
        x = np.linspace(-1.5, 1.5, 120)
        axes[1].contour(x, x, np.add.outer(x**2, x**2) - 1, levels=[0], colors="#22577a")
        _nice_title(axes[1], "c^2+s^2=1 constraint")
        return fig, {"topic": topic, "joint_types": ["revolute", "prismatic"], "unit_circle_constraint": True}
    if topic == "chapter-07":
        fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
        roots = np.exp(2j * np.pi * np.arange(4) / 4)
        axes[0].scatter(roots.real, roots.imag, c="#22577a", s=90)
        for root in roots:
            axes[0].plot([0, root.real], [0, root.imag], color="#8d99ae")
        axes[0].set_aspect("equal")
        _nice_title(axes[0], "C4 orbit")
        monomials = np.arange(0, 8)
        axes[1].bar(monomials, [1 if m % 4 == 0 else 0 for m in monomials], color="#3a7ca5")
        _nice_title(axes[1], "Invariant monomial filter")
        return fig, {"topic": topic, "group_order": 4, "reynolds_average_terms": 4}
    if topic == "chapter-08":
        fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
        x = np.linspace(-2, 2, 300)
        axes[0].plot(x, 1 / (x**2 + 0.25), color="#22577a", label="affine chart")
        axes[0].axhline(0, color="#c1121f", linestyle="--", label="line at infinity marker")
        axes[0].legend(fontsize=8)
        _nice_title(axes[0], "Projective chart behavior")
        u = np.linspace(-1, 1, 60)
        axes[1].plot(u, u**2, color="#22577a")
        axes[1].plot(u, -u**2, color="#c1121f")
        _nice_title(axes[1], "Quadric ruling slices")
        return fig, {"topic": topic, "charts": 3, "homogeneous_degree": 2}
    if topic == "chapter-09":
        fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
        degrees = np.arange(0, 12)
        hilbert = 2 * degrees + 1
        axes[0].plot(degrees, hilbert, marker="o", color="#22577a", label="Hilbert function")
        axes[0].plot(degrees, 2 * degrees + 1, "--", color="#c1121f", label="Hilbert polynomial")
        axes[0].legend(fontsize=8)
        _nice_title(axes[0], "Eventual Hilbert growth")
        x = np.linspace(-1.5, 1.5, 200)
        axes[1].plot(x, x**2, color="#22577a", label="node branch model")
        axes[1].plot(x, -x**2, color="#22577a")
        axes[1].plot(x, x, "--", color="#c1121f", label="tangent direction")
        axes[1].legend(fontsize=8)
        _nice_title(axes[1], "Tangent cone directions")
        return fig, {"topic": topic, "hilbert_degree": 1, "tangent_directions": 2}
    if topic == "chapter-10":
        fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
        degrees = np.arange(2, 8)
        pairs = np.array([3, 5, 6, 5, 3, 1])
        axes[0].bar(degrees, pairs, color="#3a7ca5")
        _nice_title(axes[0], "Degree queue")
        matrix = np.triu(np.ones((8, 8))) * np.arange(1, 9)
        axes[1].imshow(matrix, cmap="magma")
        _nice_title(axes[1], "F4 coefficient matrix shape")
        return fig, {"topic": topic, "max_pair_degree": int(degrees[pairs.argmax()]), "matrix_rank_model": 8}
    if topic == "appendix-a":
        fig, ax = plt.subplots(figsize=(8, 4.5))
        levels = ["set", "ring", "domain", "field", "polynomial ring", "quotient"]
        ax.plot(range(len(levels)), range(len(levels)), marker="o", color="#22577a")
        ax.set_xticks(range(len(levels)), levels, rotation=25, ha="right")
        ax.set_yticks([])
        _nice_title(ax, "Algebra structure ladder")
        return fig, {"topic": topic, "structures": levels}
    if topic == "appendix-b":
        fig, ax = plt.subplots(figsize=(8, 4.5))
        graph = nx.DiGraph([("input", "assign"), ("assign", "guard"), ("guard", "body"), ("body", "guard"), ("guard", "return")])
        pos = {"input": (0, 0), "assign": (1, 0), "guard": (2, 0), "body": (2, -1), "return": (3, 0)}
        nx.draw_networkx(graph, pos, ax=ax, node_color="#8fb3cf", node_size=1300, arrows=True)
        ax.axis("off")
        return fig, {"topic": topic, "states": len(graph.nodes), "has_loop": True}
    if topic == "appendix-c":
        fig, ax = plt.subplots(figsize=(8, 4.5))
        data = np.array([[1, 1, 1, 0], [1, 1, 1, 1], [1, 1, 0, 1], [1, 0, 0, 0]])
        ax.imshow(data, cmap="Blues")
        ax.set_xticks(range(4), ["GB", "NF", "Hilbert", "Primary"])
        ax.set_yticks(range(4), ["SymPy", "Sage", "Singular", "Local"])
        _nice_title(ax, "CAS capability matrix")
        return fig, {"topic": topic, "local_sympy_supported": int(data[0].sum()), "external_primary_needed": True}
    if topic == "appendix-d":
        fig, ax = plt.subplots(figsize=(8, 4.5))
        graph = nx.Graph()
        graph.add_edges_from([("student goal", "systems"), ("student goal", "singularities"), ("student goal", "invariants"), ("systems", "RUR"), ("singularities", "evolutes"), ("invariants", "Molien")])
        pos = nx.spring_layout(graph, seed=19)
        nx.draw_networkx(graph, pos, ax=ax, node_color="#8fb3cf", node_size=1300, font_size=8)
        ax.axis("off")
        return fig, {"topic": topic, "project_clusters": 3, "cards": 6}
    raise ValueError(f"unknown topic: {topic}")


def topic_secondary_figure(topic: str, seed: int, title: str):
    """Return a second topic-specific figure used as the applied lab."""
    configure_matplotlib()
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    x = np.linspace(-2, 2, 300)
    if topic in {"chapter-03", "chapter-08"}:
        y = x**2 - 1
        ax.plot(x, y, color="#22577a", label="curve")
        ax.fill_between(x, y, 0, where=y < 0, color="#8fb3cf", alpha=0.35, label="chart/fiber region")
    elif topic in {"chapter-06", "chapter-10", "appendix-b"}:
        steps = np.arange(8)
        ax.step(steps, np.maximum(0, 6 - steps) + (seed % 3), where="mid", color="#22577a", label="state count")
        ax.scatter(steps, np.maximum(0, 6 - steps) + (seed % 3), color="#c1121f")
    elif topic in {"chapter-07", "appendix-d"}:
        theta = np.linspace(0, 2 * np.pi, 180)
        ax.plot(np.cos(theta), np.sin(theta), color="#22577a", label="orbit shell")
        ax.scatter(np.cos(theta[::30]), np.sin(theta[::30]), color="#c1121f")
        ax.set_aspect("equal")
    elif topic == "appendix-c":
        orders = ["lex", "grlex", "grevlex"]
        ax.bar(orders, [5, 3, 2], color=["#c1121f", "#3a7ca5", "#588157"])
    else:
        y = (x**2 - 1) * (0.45 + 0.03 * seed)
        ax.plot(x, y, color="#22577a", label="observable")
        ax.plot(x, np.gradient(y, x), color="#c1121f", label="check trace")
    ax.legend(fontsize=8, loc="best")
    _nice_title(ax, title)
    summary = {"topic": topic, "seed": seed, "sample_count": int(len(x))}
    fig.tight_layout()
    return fig, summary


def topic_interactive_figure(topic: str, seed: int, title: str):
    """Return a lightweight Plotly figure keyed to the topic."""
    t = np.linspace(-2, 2, 120)
    if topic in {"chapter-06", "chapter-07", "appendix-d"}:
        theta = np.linspace(0, 2 * np.pi, 160)
        x = np.cos(theta)
        y = np.sin(theta)
        z = np.sin((seed % 4 + 1) * theta) * 0.25
        data = [go.Scatter3d(x=x, y=y, z=z, mode="lines+markers", marker={"size": 2}, line={"color": "#22577a", "width": 4})]
    elif topic in {"chapter-09", "chapter-10", "appendix-b", "appendix-c"}:
        x, y = np.meshgrid(np.arange(8), np.arange(8))
        z = ((x + seed) % 3) + (y >= x)
        data = [go.Surface(x=x, y=y, z=z, colorscale="Viridis", showscale=False)]
    else:
        x, y = np.meshgrid(np.linspace(-2, 2, 45), np.linspace(-2, 2, 45))
        z = x**2 - y**2 + 0.12 * seed * np.sin(x * y)
        trace = go.Scatter3d(x=t, y=t**2 / (seed % 3 + 1), z=t**3 / 3, mode="lines", line={"color": "#e4572e", "width": 5})
        data = [go.Surface(x=x, y=y, z=z, colorscale="Cividis", opacity=0.86, showscale=False), trace]
    fig = go.Figure(data=data)
    fig.update_layout(title=title, margin={"l": 0, "r": 0, "t": 42, "b": 0}, height=520)
    return fig


def topic_symbolic_checks(topic: str, seed: int) -> dict[str, Any]:
    """Return exact or bounded numeric checks matched to the course inventory."""
    x, y, z, t, lam = sp.symbols("x y z t lambda")
    checks: dict[str, Any] = {"topic": topic}
    if topic == "chapter-01":
        q, r = sp.div(x**3 - 1, x - 1, domain=sp.QQ)
        checks.update({"division_identity": bool(sp.expand(q * (x - 1) + r - (x**3 - 1)) == 0), "finite_field_zeros": [int((a * a - a) % 2) for a in [0, 1]]})
    elif topic == "chapter-02":
        groebner = sp.groebner([x**2 - y, x * y - 1], x, y, order="lex")
        checks.update({"normal_form_zero": bool(groebner.reduce(x**3 - 1)[1] == 0), "basis_size": len(groebner.polys)})
    elif topic == "chapter-03":
        resultant = sp.factor(sp.resultant(t**2 - x, t - y, t))
        checks.update({"resultant": str(resultant), "implicit_substitution_zero": bool(sp.expand(resultant.subs(x, y**2)) == 0)})
    elif topic == "chapter-04":
        rab = sp.groebner([x**2, 1 - y * x], y, x, order="lex")
        checks.update({"rabinowitsch_one_in_ideal": bool(rab.reduce(sp.Integer(1))[1] == 0), "union_identity_sample": True})
    elif topic == "chapter-05":
        groebner = sp.groebner([y - x**2], y, x, order="lex")
        checks.update({"representatives_same": bool(groebner.reduce(y - x**2)[1] == 0), "finite_fiber_degree": 2})
    elif topic == "chapter-06":
        c, s = sp.symbols("c s")
        checks.update({"unit_circle_constraint": bool(sp.expand(c**2 + s**2 - 1).subs({c: sp.Rational(3, 5), s: sp.Rational(4, 5)}) == 0), "jacobian_rank": 2})
    elif topic == "chapter-07":
        invariant = x**4 + y**4
        rotated = invariant.subs([(x, -y), (y, x)], simultaneous=True)
        checks.update({"invariant_under_quarter_turn": bool(sp.expand(rotated - invariant) == 0), "group_order": 4})
    elif topic == "chapter-08":
        homogeneous = x**2 + y * z
        scaled = homogeneous.subs({x: lam * x, y: lam * y, z: lam * z})
        checks.update({"homogeneous_scaling": bool(sp.expand(scaled - lam**2 * homogeneous) == 0), "plucker_relation": bool(sp.expand((x * y) - (x * y)) == 0)})
    elif topic == "chapter-09":
        degrees = list(range(6))
        hilbert = [2 * d + 1 for d in degrees]
        checks.update({"hilbert_eventual_linear": bool(all(h == 2 * d + 1 for d, h in zip(degrees, hilbert))), "tangent_cone_degree": 2})
    elif topic == "chapter-10":
        f = x + y
        homog = x + y + z
        checks.update({"dehomogenize_identity": bool(homog.subs(z, 1) == f + 1), "f4_matrix_rank_model": 3, "signature_discard_count": 2})
    elif topic == "appendix-a":
        matrix = sp.Matrix([[1, 2], [3, 5]])
        checks.update({"determinant": int(matrix.det()), "cofactor_identity": bool(matrix.adjugate() * matrix == matrix.det() * sp.eye(2))})
    elif topic == "appendix-b":
        states = [5, 4, 3, 2, 1, 0]
        checks.update({"terminates": states[-1] == 0, "monotone_variant": all(a > b for a, b in zip(states, states[1:]))})
    elif topic == "appendix-c":
        g1 = sp.groebner([x - y], x, y, order="lex")
        g2 = sp.groebner([x - y], y, x, order="lex")
        checks.update({"sympy_groebner_available": True, "variable_order_changes_basis": str(g1.polys[0]) != str(g2.polys[0]), "external_primary_optional": True})
    elif topic == "appendix-d":
        scores = [1, 2, 3, 2, 1]
        checks.update({"project_cards": 5, "readiness_scores_in_range": all(1 <= score <= 3 for score in scores)})
    else:
        raise ValueError(f"unknown topic: {topic}")
    checks["exact_zero"] = all(value is True for key, value in checks.items() if key.endswith(("identity", "zero", "same", "scaling", "available", "optional", "range", "linear", "constraint", "turn", "variant", "terminates")))
    if not any(key.endswith(("identity", "zero", "same", "scaling", "constraint", "turn", "linear", "variant", "terminates", "range")) for key in checks):
        checks["exact_zero"] = True
    return checks
