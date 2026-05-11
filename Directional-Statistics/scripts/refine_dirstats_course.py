"""Regenerate notebooks with topic-specific visuals, checks, and offline artifacts."""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

import dirstats_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))


DETAILS = {
    "chapter-01": "The chapter opens the course by separating three ideas that are easy to blur: an angle as a coordinate, a direction as a point on a unit circle, and an axis as an unoriented line through the origin. The lab uses controlled compass-like and clock-like observations so the reader can see when a rose diagram, raw circular plot, or unrolled histogram is telling the truth.",
    "chapter-02": "The chapter replaces linear averaging with vector geometry. The worked example deliberately straddles the zero direction so the ordinary mean fails visibly, while the resultant vector still points into the actual cluster. The dispersion curve shows the minimization principle rather than asking the reader to accept it algebraically.",
    "chapter-03": "The chapter treats model families as generators of shapes on the circle. Fourier amplitudes, wrapped line distributions, and projected planar distributions are drawn together so that density formulas become inspectable signals rather than isolated expressions.",
    "chapter-04": "The chapter turns limit theory into random-walk geometry. Resultant-length distributions are shown as endpoint clouds, and the Rayleigh statistic is compared with its chi-square reference so the asymptotic statement has a visible scale.",
    "chapter-05": "The chapter focuses on likelihood as a surface over mean direction and concentration. The estimate is not just a number: it is the point where the observed resultant and the Bessel-ratio curve agree.",
    "chapter-06": "The chapter treats uniformity as the baseline model for no preferred direction. Rayleigh, Kuiper, and Watson diagnostics are drawn as endpoint and CDF discrepancies so that each test's alternative becomes visible.",
    "chapter-07": "The chapter uses grouped resultants to make von Mises testing and circular ANOVA geometric. Confidence arcs and group mean vectors show why concentration assumptions matter before comparing mean directions.",
    "chapter-08": "The chapter avoids parametric assumptions by moving ranks and runs onto the circle. Uniform scores, two-sample circular CDFs, and runs parity are used as direct checks that the procedure respects periodic order.",
    "chapter-09": "The chapter moves from one circular coordinate to a full spherical sample space. Mean vectors, inertia spectra, and density sketches distinguish pole-like concentration from axial or girdle structure.",
    "chapter-10": "The chapter is about inference on spheres: confidence cones, concentration inversion, and tests of uniformity or axial structure. The computations keep every fitted or predicted object on the sphere.",
    "chapter-11": "The chapter studies dependence when at least one variable is directional. The lab emphasizes embedded sine-cosine or vector representations, then checks that fitted directional responses remain unit vectors.",
    "chapter-12": "The chapter surveys modern methods by stressing robustness and resampling. Ordinary and robust summaries are compared under contamination, and density or bootstrap outputs are checked as geometric objects.",
    "chapter-13": "The chapter expands the sample-space catalog beyond spheres. Rotation matrices, Stiefel frames, Grassmann projections, and hyperboloid points are displayed with their defining constraints and checked numerically.",
    "chapter-14": "The chapter makes shape analysis concrete by removing translation, scale, and rotation from landmark configurations. Aligned Procrustes overlays, triangle-shape coordinates, and tangent coordinates expose the quotient-space idea.",
    "appendix-01": "The appendix turns special functions into calculators. Bessel ratios, approximations, and error bands are plotted so normalizing constants and concentration equations become inspectable numerical objects.",
    "appendix-02": "The appendix replaces circular printed tables with reproducible computations. Concentration inversions and null simulations show how lookup values arise and where approximations are trustworthy.",
    "appendix-03": "The appendix performs the same replacement for spherical tables. Fisher concentration, cap densities, and Watson-style axial behavior are visualized as curves and spherical scenes.",
    "appendix-04": "The appendix is an executable notation atlas. Symbols are grouped by sample space, model family, and diagnostic purpose so readers can navigate the course's notation by dependency rather than by alphabet.",
}


def dedent(text: str) -> str:
    return textwrap.dedent(text).strip() + "\n"


def markdown_cells(entry: dict) -> list:
    concepts = "\n".join(f"- {item}" for item in entry["concepts"])
    visuals = "\n".join(f"- {item}" for item in entry["visuals"])
    checks = "\n".join(f"- {item}" for item in entry["checks"])
    detail = DETAILS[entry["topic"]]
    title = f"{entry['label']}: {entry['title']}"
    return [
        new_markdown_cell(
            dedent(
                f"""
                # {title}

                Source span: printed pages {entry['printed']}; PDF pages {entry['pdf']}. The textbook PDF is used here only for orientation: chapter structure, terminology, and concept order. The prose, examples, diagrams, computations, and artifacts in this notebook are original course material.

                ## Chapter Question

                {entry['focus']} The question is how to make that statement visible and testable. Directional statistics is not ordinary Euclidean statistics with trigonometric decoration. Its sample spaces carry identifications: angles wrap, axes ignore sign, spherical data rotate, frames preserve orthogonality, and shapes forget translation, scale, and rotation. Each section below converts those identifications into a computational object and then into an artifact the reader can inspect.

                {detail}

                A useful reading habit is to pause before every formula and ask what transformation should leave it unchanged. If shifting the zero angle, rotating the sphere, changing the basis of a subspace, or translating a landmark configuration changes the scientific answer, the calculation is not yet respecting the sample space. The notebook's final checks are built around that habit.
                """
            )
        ),
        new_markdown_cell(
            dedent(
                f"""
                ## Translation Guide

                Concepts translated in this lesson:

                {concepts}

                The computational translation is intentionally concrete. Observations are represented as arrays only after the relevant geometry has been named. Circular observations are wrapped before differences are computed. Spherical observations are normalized and summarized by vector resultants or matrix spectra. Rotations, frames, and subspaces are checked by orthogonality, determinant, or idempotence identities. Shapes are centered, scaled, and aligned before comparison.

                This guide matters because the same numerical array can mean different things. A pair of columns might be two ordinary variables, sine-cosine coordinates for a circle, a two-frame on a Stiefel manifold, or a landmark configuration after centering. The formulas in the course are useful only when paired with the right interpretation.
                """
            )
        ),
        new_markdown_cell(
            dedent(
                f"""
                ## Visual Storyboard

                The visual sequence for this notebook is:

                {visuals}

                The static figure is the durable teaching artifact. It is designed to be understandable in a rendered notebook, a static export, or a file browser. The interactive HTML artifact is self-contained and book-local; it lets the reader rotate or inspect the geometry without relying on the PDF or a network connection. Together the two artifacts should answer two different questions: what invariant is being measured, and how does the picture change when the sample or model changes?

                The displayed figure is not a screenshot from the source. It is generated from small synthetic examples chosen to expose the chapter's geometry. Synthetic data keeps the lesson reproducible and avoids copying long tables. The examples are small by design: they make it easy to predict what should happen before the code runs.
                """
            )
        ),
        new_markdown_cell(
            dedent(
                f"""
                ## Worked Lab

                The lab cell below builds the chapter-specific artifact and records the numerical diagnostics that make the visual auditable. Read the numbers beside the figure rather than treating them as invisible bookkeeping. A resultant length, an integration residual, an idempotence norm, or a Procrustes invariance error is a compact statement about the geometry in the picture.

                Expected checks for this chapter:

                {checks}

                After running the visual cell, change one parameter in the helper call and predict the effect. Increase concentration and the cluster should tighten. Rotate all angles and origin-invariant tests should not change. Add axial symmetry and a mean-direction diagnostic should become less informative. Translate a shape and Procrustes comparisons should be stable. These small perturbations are the quickest way to find a hidden linear assumption.
                """
            )
        ),
        new_markdown_cell(
            dedent(
                f"""
                ## Interpretation Notes

                The key definitions in this notebook should be read operationally. The phrase `{entry['title']}` names a family of decisions about representation: which coordinates are safe to use, which transformations are nuisance transformations, and which numerical summaries survive those transformations. The concept list above is the local contract for those decisions. If a learner can explain why each listed concept is invariant, equivariant, or intentionally coordinate-dependent, then the formulas have become usable rather than memorized.

                The visual artifact is also an argument. It chooses one small scene where the chapter's main failure mode is visible: a bad cut point, a misleading linear average, a density that must integrate around a closed loop, a matrix that must remain orthogonal, or a shape comparison that must ignore translation and scale. In later applications the data may be larger and noisier, but the same small-scene logic applies. Start with a display that makes the invariant visible, then scale the computation.

                The saved JSON checks are deliberately plain. They are meant to be read by a person and by an audit script. A check such as `A_kappa_matches_R`, `unit_vectors_on_sphere`, `grassmann_projection_idempotent`, or `procrustes_ignores_translation` is a compact record of what would have gone wrong if the sample space had been flattened too early. When extending this notebook, add checks of the same kind before adding visual flourish.

                Finally, notice that the artifacts are book-local. The notebook does not depend on a PDF crop, an external web service, or a hidden interactive session. This matters pedagogically: the reader can inspect the figure, rerun the cells, compare the JSON diagnostics, and then use the same helper functions in a new data analysis. That is the course standard for a standalone visualization-first chapter.

                Before moving on, use this reader checklist. Identify the observation type in one sentence. Point to the panel or interactive scene where that type is visible. Name the statistic being computed and the transformation it should respect. Then open the final sanity JSON and find the value that supports that claim. If any of those four steps feels vague, the notebook should be extended at that point rather than treated as complete. The aim is not to make every chapter long; the aim is to make every chapter inspectable, portable, and honest about the geometry it uses.

                This short checklist is also the acceptance test for future revisions.
                """
            )
        ),
        new_markdown_cell(
            dedent(
                f"""
                ## Takeaways

                The central takeaway is that {entry['title'].lower()} is a geometry-first topic. The statistic, the visualization, and the final sanity check should all refer to the same invariant. If the artifact shows a rose plot but the chapter is about likelihood, the artifact is wrong; if a final JSON file only says that files exist, the check is too weak. This notebook therefore saves both concept-named artifacts and chapter-specific numerical checks.

                Keep three habits for later notebooks. First, name the sample space before choosing a coordinate system. Second, draw the invariant or failure mode directly. Third, keep a small numerical check beside every visual claim. That discipline is what makes the course standalone: the reader does not need the textbook open to understand what is being measured, why the geometry matters, and how to verify the computation.
                """
            )
        ),
    ]


def notebook_cells(entry: dict) -> list:
    entry_repr = repr(entry)
    setup = f"""
    from pathlib import Path
    import sys

    def find_book_root(start: Path) -> Path:
        for candidate in [start.resolve(), *start.resolve().parents]:
            if (
                (candidate / "AGENTS.md").exists()
                and (candidate / "scripts" / "validate_dirstats_course.py").exists()
                and (candidate / "utils").exists()
            ):
                return candidate
        raise RuntimeError("Could not locate Directional-Statistics course root")

    BOOK_ROOT = find_book_root(Path.cwd())
    if str(BOOK_ROOT) not in sys.path:
        sys.path.insert(0, str(BOOK_ROOT))

    ENTRY = {entry_repr}
    TOPIC = ENTRY["topic"]
    print(f"Course root: {{BOOK_ROOT}}")
    print(f"Working topic: {{TOPIC}}")
    """
    imports = """
    import numpy as np
    import matplotlib.pyplot as plt

    from utils.artifacts import display_artifact, save_json, save_matplotlib, save_plotly_html
    from utils.topic_visuals import make_topic_interactive_figure, make_topic_static_figure, topic_numeric_checks
    from utils.validation import assert_artifacts

    np.set_printoptions(precision=4, suppress=True)
    source_span = {"printed": ENTRY["printed"], "pdf": ENTRY["pdf"]}
    source_span
    """
    static = """
    fig, static_diagnostics = make_topic_static_figure(ENTRY)
    png_path = save_matplotlib(fig, TOPIC, "core", "concept-diagnostic.png")
    plt.close(fig)
    display_artifact(png_path, width=860)
    static_diagnostics
    """
    interactive = """
    interactive_fig = make_topic_interactive_figure(ENTRY)
    html_path = save_plotly_html(interactive_fig, TOPIC, "interactive", "exploration.html", include_plotlyjs=True)
    display_artifact(html_path, width="100%", height=520)
    """
    checks = """
    numeric_checks = topic_numeric_checks(ENTRY, static_diagnostics)
    # Every chapter should contribute at least one boolean mathematical invariant
    # in addition to artifact existence checks.
    boolean_checks = [value for key, value in numeric_checks.items() if isinstance(value, bool)]
    assert boolean_checks, "no topic-specific boolean checks were recorded"
    assert all(boolean_checks), numeric_checks
    checks_path = save_json(numeric_checks, TOPIC, "checks", "numeric-checks.json")
    numeric_checks
    """
    final = """
    final_sanity = {
        "artifacts": assert_artifacts([png_path, html_path, checks_path], min_bytes=100),
        "topic_checks": numeric_checks,
        "standalone_contract": "original prose, generated visuals, executable checks",
        "pdf_used_for": "source orientation only",
    }
    final_path = save_json(final_sanity, TOPIC, "checks", "final-sanity.json")
    assert final_path.exists() and final_path.stat().st_size > 100
    final_sanity
    """
    md = markdown_cells(entry)
    return [
        md[0],
        md[1],
        new_code_cell(dedent(setup)),
        new_code_cell(dedent(imports)),
        md[2],
        new_code_cell(dedent(static)),
        md[3],
        new_code_cell(dedent(interactive)),
        new_code_cell(dedent(checks)),
        md[4],
        md[5],
        new_code_cell(dedent(final)),
    ]


def write_notebook(path: Path, cells: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=cells), path)


def regenerate_notebooks() -> None:
    for entry in inventory.ENTRIES:
        folder = BOOK_ROOT / entry["part"] / entry["folder"]
        write_notebook(folder / entry["notebook"], notebook_cells(entry))


def regenerate_artifacts() -> None:
    import matplotlib

    matplotlib.use("Agg")
    from utils.artifacts import save_json, save_matplotlib, save_plotly_html
    from utils.topic_visuals import make_topic_interactive_figure, make_topic_static_figure, topic_numeric_checks
    from utils.validation import assert_artifacts

    for entry in inventory.ENTRIES:
        fig, diagnostics = make_topic_static_figure(entry)
        png_path = save_matplotlib(fig, entry["topic"], "core", "concept-diagnostic.png")
        plt = __import__("matplotlib.pyplot").pyplot
        plt.close(fig)
        html_path = save_plotly_html(
            make_topic_interactive_figure(entry),
            entry["topic"],
            "interactive",
            "exploration.html",
            include_plotlyjs=True,
        )
        numeric_checks = topic_numeric_checks(entry, diagnostics)
        checks_path = save_json(numeric_checks, entry["topic"], "checks", "numeric-checks.json")
        save_json(
            {
                "artifacts": assert_artifacts([png_path, html_path, checks_path], min_bytes=100),
                "topic_checks": numeric_checks,
                "standalone_contract": "original prose, generated visuals, executable checks",
                "pdf_used_for": "source orientation only",
            },
            entry["topic"],
            "checks",
            "final-sanity.json",
        )


def main() -> None:
    regenerate_notebooks()
    regenerate_artifacts()
    print(f"Refined {len(inventory.ENTRIES)} notebooks with topic-specific visuals and checks.")


if __name__ == "__main__":
    main()
