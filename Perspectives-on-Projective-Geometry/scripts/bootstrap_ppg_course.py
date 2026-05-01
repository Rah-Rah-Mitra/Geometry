from __future__ import annotations

import json
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

import ppg_inventory as inv

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.artifacts import ensure_artifact_root, save_json
from utils.chapter_visuals import render_chapter_visuals


def storyboard_for(chapter: dict[str, object]) -> dict[str, object]:
    sequence = []
    artifact_names = [
        "visual-route-map.png",
        _mode_artifact_name(str(chapter["visual_mode"])),
        "invariant-reparametrization-check.png",
        "parameter-lab.html",
        "visual-observation-targets.csv",
    ]
    for index, visual in enumerate(chapter["visuals"], start=1):
        sequence.append(
            {
                "order": index,
                "concept": visual,
                "representation": _representation(str(chapter["visual_mode"])),
                "library": "numpy, matplotlib, local projective/conic/Cayley-Klein helpers, and self-contained HTML",
                "artifact_filename": artifact_names[min(index - 1, len(artifact_names) - 1)],
                "learner_inspection_target": _inspection_prompt(chapter, str(visual)),
                "expected_observation": _expected_observation(chapter, str(visual)),
                "validation_target": _validation_target(str(chapter["visual_mode"])),
            }
        )
    return {
        "chapter goal": chapter["question"],
        "source span read": f"sections {chapter['sections']}; printed pages {chapter['printed_span']}; PDF pages {chapter['pdf_span']}",
        "visual sequence": sequence,
        "computational checks": [
            "cross-ratio invariance under a projective reparametrization",
            "join/meet incidence for generated homogeneous points",
            "artifact existence and nonzero size",
            "mode-specific conic or hyperbolic numeric check when relevant",
        ],
        "implementation notes": {
            "chapter_folder": chapter["folder"],
            "artifact_root": f"artifacts/{chapter['artifact']}",
            "helpers": [
                "utils.artifacts",
                "utils.projective",
                "utils.conics",
                "utils.cayley_klein",
                "utils.chapter_visuals",
            ],
        },
        "gaps": f"Proof-heavy material in Chapter {chapter['number']} is represented by {str(chapter['visual_mode']).replace('-', ' ')} diagrams, determinant/cross-ratio checks, or small parameter experiments rather than copied text.",
    }


def _inspection_prompt(chapter: dict[str, object], visual: str) -> str:
    return (
        f"For Chapter {chapter['number']}, inspect {visual.lower()} by identifying "
        f"which objects instantiate {str(chapter['focus']).split(',')[0].lower()}."
    )


def _expected_observation(chapter: dict[str, object], visual: str) -> str:
    mode = str(chapter["visual_mode"])
    observations = {
        "incidence": "The same point-line incidences remain readable after the layout changes.",
        "line": "The coordinate values move, but the cross-ratio check stays fixed.",
        "bracket": "Rescaling homogeneous data changes determinants individually, not the invariant relation.",
        "conic": "The conic matrix generates both a curve and its tangent/polar line data.",
        "space": "Affine charts hide infinity, while homogeneous rays keep finite and infinite elements in one model.",
        "tensor": "Contracted indices can be followed as paths through the diagram.",
        "complex": "Complex transformations move circles and lines through one CP1 language.",
        "measurement": "The absolute conic decides which transformations preserve angle or distance.",
        "hyperbolic": "Boundary data controls disk geodesics, distances, and model changes.",
    }
    return observations.get(mode, f"The visual makes {visual.lower()} inspectable without the source PDF.")


def _validation_target(mode: str) -> str:
    return {
        "incidence": "dot products for incident point-line pairs vanish",
        "line": "cross-ratio error is below tolerance",
        "bracket": "determinant signs and Grassmann-Plucker-style identities are stable",
        "conic": "sample point lies on its conic and tangent relation vanishes",
        "space": "homogeneous projection and incidence computations are finite",
        "tensor": "diagram metadata and invariant reparametrization checks exist",
        "complex": "Mobius/cross-ratio and stereographic samples are finite",
        "measurement": "absolute-conic pole/polar checks and distance sample are finite",
        "hyperbolic": "Poincare distance is positive and disk artifacts are nonblank",
    }.get(mode, "artifact existence and nonblank rendering")


def _representation(mode: str) -> str:
    return {
        "incidence": "incidence diagram",
        "line": "projective-line parameter plot",
        "bracket": "determinant/bracket proof-state diagram",
        "conic": "conic contour with polar/tangent computation",
        "space": "3D homogeneous coordinate scene",
        "tensor": "tensor rewrite diagram",
        "complex": "complex-plane and Mobius transformation diagram",
        "measurement": "absolute-conic measurement diagram",
        "hyperbolic": "Poincare/Klein disk construction",
    }.get(mode, "geometry diagram")


def _mode_artifact_name(mode: str) -> str:
    return {
        "incidence": "incidence-configuration.png",
        "line": "projective-line-coordinate-change.png",
        "bracket": "bracket-orientation-lab.png",
        "conic": "conic-polar-tangent-system.png",
        "space": "homogeneous-space-model.png",
        "tensor": "tensor-diagram-proof-state.png",
        "complex": "complex-projective-motion.png",
        "measurement": "absolute-conic-measurement-lab.png",
        "hyperbolic": "hyperbolic-disk-geodesic-lab.png",
    }.get(mode, "incidence-configuration.png")


def notebook_for(chapter: dict[str, object]) -> nbformat.NotebookNode:
    chapter_json = json.dumps(
        {
            "number": chapter["number"],
            "title": chapter["title"],
            "focus": chapter["focus"],
            "question": chapter["question"],
            "visuals": chapter["visuals"],
            "visual_mode": chapter["visual_mode"],
            "artifact": chapter["artifact"],
            "sections": chapter["sections"],
        },
        indent=2,
    )
    cells = [
        new_markdown_cell(_opening_markdown(chapter)),
        new_code_cell(_setup_code(chapter)),
        new_markdown_cell(_translation_markdown(chapter)),
        new_code_cell(_import_code(chapter_json)),
        new_markdown_cell(_visual_markdown(chapter)),
        new_code_cell("bundle = render_chapter_visuals(CHAPTER, ARTIFACT_ROOT)\nbundle['display_paths']"),
        new_code_cell(
            "for artifact in bundle['display_paths']:\n"
            "    display_artifact(artifact, width=760, height=450)\n"
        ),
        new_markdown_cell(_artifact_gallery_markdown(chapter)),
        new_markdown_cell(_lab_markdown(chapter)),
        new_code_cell(_lab_code(chapter)),
        new_markdown_cell(_takeaways_markdown(chapter)),
        new_code_cell(_sanity_code()),
    ]
    return new_notebook(cells=cells, metadata={"kernelspec": {"name": "python3", "display_name": "Python 3"}})


def _opening_markdown(chapter: dict[str, object]) -> str:
    visuals = ", ".join(str(v).lower() for v in chapter["visuals"][:3])
    chapter_focus = _chapter_focus_paragraph(chapter)
    return f"""# Chapter {chapter['number']}: {chapter['title']}

**Source orientation.** Sections {chapter['sections']}; printed pages {chapter['printed_span']}; PDF pages {chapter['pdf_span']}. The textbook is used only to orient the structure and mathematical themes. This notebook is an original, standalone computational lesson.

**Chapter question.** {chapter['question']}

This chapter's working theme is: {chapter['focus']} The route here is deliberately visual-first. Instead of asking the reader to trust a finished figure, we build inspectable artifacts and then check the algebra that explains why the picture behaves as it does. The first pass identifies the geometric objects, the second pass translates them into coordinates or transformations, and the final pass records the invariant that survived the construction.

The initial visual route centers on {visuals}. These are not decorative captions. Each visual has a job: expose an incidence relation, make a limiting process visible, compare two algebraic representations, or put a proof state into a form that can be tested. The notebook therefore treats diagrams as data. Points, lines, conics, cycles, and transformations are rendered, but they are also queried by code.

{chapter_focus}
"""


def _translation_markdown(chapter: dict[str, object]) -> str:
    mode_text = _mode_translation(str(chapter["visual_mode"]))
    pitfalls = _pitfalls(chapter)
    return f"""## Computational Translation

{mode_text}

For this chapter the computational target is: {chapter['focus']} The definitions are written in prose first, then mirrored by small code checks. This prevents a common projective-geometry mistake: treating a visually plausible diagram as a proof while losing track of the exceptional or limiting case. The generated artifacts deliberately show both a picture and a validation record.

The chapter is also designed to be read without the book open. Names from the source chapter are used as orientation, but the explanations here are original. The reader should leave with a working model: which objects are being represented, which operation is being performed, which invariant is expected, and how the included sanity checks would fail if the construction were wrong.

**Common pitfall for this chapter.** {pitfalls}
"""


def _visual_markdown(chapter: dict[str, object]) -> str:
    lines = "\n".join(
        f"- **{visual}.** {_expected_observation(chapter, str(visual))} Validation target: {_validation_target(str(chapter['visual_mode']))}."
        for visual in chapter["visuals"]
    )
    return f"""## Visual Storyboard

The storyboard below was generated from the chapter source span and implemented as durable artifacts under `artifacts/{chapter['artifact']}`.

{lines}

The next cell renders the visual route, a chapter-specific geometric scene, an invariant panel, a local interactive HTML lab, and a table of inspection targets. The same renderer is used during validation, so a stale artifact or broken helper is caught by execution instead of hidden in the notebook.
"""


def _artifact_gallery_markdown(chapter: dict[str, object]) -> str:
    prefix = "../" if chapter["part"] is None else "../../"
    root = f"{prefix}artifacts/{chapter['artifact']}"
    mode_file = _mode_artifact_name(str(chapter["visual_mode"]))
    return f"""## Artifact Gallery

The key static artifacts are linked directly in markdown so the notebook remains readable even before execution.

![Visual route map]({root}/figures/visual-route-map.png)

![Chapter geometric scene]({root}/figures/{mode_file})

![Invariant reparametrization check]({root}/figures/invariant-reparametrization-check.png)

Open the [parameter lab]({root}/html/parameter-lab.html) and the [visual observation table]({root}/tables/visual-observation-targets.csv) when reading this notebook outside an executed kernel.
"""


def _lab_markdown(chapter: dict[str, object]) -> str:
    mode_lab = _mode_lab(str(chapter["visual_mode"]))
    return f"""## Applied Lab

Use the artifacts as a small laboratory for Chapter {chapter['number']}. Start with the visual route and ask which object is primary in this chapter: point, line, conic, tensor, complex point, or absolute conic. Then compare that answer with the invariant panel. {mode_lab}

The lab intentionally avoids a long exercise list. The useful habit is shorter and more repeatable: perturb one parameter, recompute the construction, and verify what did not change. In a projective setting this is often more informative than a single polished drawing, because the theorem is really about an equivalence class of drawings.
"""


def _takeaways_markdown(chapter: dict[str, object]) -> str:
    first_visual = str(chapter["visuals"][0])
    last_visual = str(chapter["visuals"][-1])
    return f"""## Takeaways

- The chapter's main question was: {chapter['question']}
- The first construction, **{first_visual}**, sets up the objects; the last construction, **{last_visual}**, records what the computation can verify.
- {_takeaway_by_mode(str(chapter['visual_mode']))}
- The final sanity cell records the artifact list and the numeric checks so future edits can detect broken diagrams or stale paths.
"""


def _setup_code(chapter: dict[str, object]) -> str:
    return f"""from pathlib import Path
import sys

START = Path.cwd().resolve()
BOOK_ROOT = None
for candidate in [START, *START.parents]:
    if (candidate / "AGENTS.md").exists() and (candidate / "Perspectives on Projective Geometry.pdf").exists():
        BOOK_ROOT = candidate
        break
if BOOK_ROOT is None:
    raise RuntimeError("Could not discover the course root")
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))
ARTIFACT_ROOT = BOOK_ROOT / "artifacts" / "{chapter['artifact']}"
ARTIFACT_ROOT
"""


def _import_code(chapter_json: str) -> str:
    return f"""import numpy as np

from utils.artifacts import assert_artifacts, display_artifact, save_json
from utils.chapter_visuals import render_chapter_visuals
from utils.projective import cross_ratio, hpoint, incidence, join

CHAPTER = {chapter_json}
"""


def _lab_code(chapter: dict[str, object]) -> str:
    return """sample = [-1.4, -0.2, 0.75, 1.6]
image = [(1.1*x - 0.25) / (0.22*x + 1.0) for x in sample]
cr_error = abs(cross_ratio(*sample) - cross_ratio(*image))

p = hpoint(-0.7, 0.4)
q = hpoint(0.85, -0.25)
line = join(p, q)
incidence_ok = incidence(p, line) and incidence(q, line)

{"cross_ratio_error": float(abs(cr_error)), "incidence_ok": bool(incidence_ok)}
"""


def _sanity_code() -> str:
    return """assert_artifacts(bundle["display_paths"])
checks = bundle["checks"]
assert checks["cross_ratio_error"] < 1e-9
assert checks["join_incidence_check"]
assert checks["all_files_exist"]

final = {
    "chapter": CHAPTER["number"],
    "artifacts": bundle["relative_display_paths"],
    "checks": checks,
    "notebook_executed": True,
}
save_json(final, ARTIFACT_ROOT, "checks", "final-sanity.json")
final
"""


def write_notebook(path: Path, notebook: nbformat.NotebookNode) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, path)


def _chapter_focus_paragraph(chapter: dict[str, object]) -> str:
    return (
        f"In this chapter, the named source sections ({chapter['sections']}) are compressed into a "
        f"working notebook around {str(chapter['visuals'][0]).lower()} and "
        f"{str(chapter['visuals'][-1]).lower()}. The aim is not to reproduce the source ordering line by line; "
        f"it is to reconstruct the chapter's mathematical machinery so that a reader can experiment with it."
    )


def _mode_translation(mode: str) -> str:
    return {
        "incidence": "The core representation is an incidence structure: points and lines are data, and a theorem is checked by seeing which incidences force a new incidence. Homogeneous joins and meets keep parallel and finite cases in one calculation.",
        "line": "The core representation is the projective line. Coordinates are temporary charts; the cross-ratio is the durable quantity that survives when the chart is changed by a linear fractional map.",
        "bracket": "The core representation is bracket algebra. Determinants encode oriented area, collinearity, and scaling behavior; relations among brackets become proof states that can be checked symbolically or numerically.",
        "conic": "The core representation is a symmetric quadratic form. The same matrix evaluates points on the conic, sends a point to its polar line, produces tangents, and reveals degeneracy through rank and factorization.",
        "space": "The core representation is homogeneous space. Points, lines, and planes are subspaces; finite charts are only views of a higher-dimensional join-and-meet calculus.",
        "tensor": "The core representation is a tensor diagram. Wires track indices, nodes represent invariant tensors, and algebraic simplification is shown as a controlled diagram rewrite.",
        "complex": "The core representation is the complex projective line. Circles, lines, infinity, inversion, and Mobius motion are handled in one coordinate language, with stereographic projection as the visual bridge.",
        "measurement": "The core representation is an absolute conic. Distance, angle, orthogonality, reflection, and rotation are not assumed; they are recovered from projective data relative to that absolute.",
        "hyperbolic": "The core representation is the disk model and its boundary. Projective boundary data, Mobius maps, geodesic arcs, and cross-ratio distances cooperate to define hyperbolic measurement.",
    }.get(mode, "The core representation is chosen so that a geometric claim can be rendered and checked.")


def _pitfalls(chapter: dict[str, object]) -> str:
    mode = str(chapter["visual_mode"])
    return {
        "incidence": "Do not infer incidence from a near miss in a drawing; use the algebraic incidence check.",
        "line": "Do not confuse a coordinate value with a projective point; a different chart can move infinity into a finite location.",
        "bracket": "Do not compare raw determinants after rescaling points; compare the invariant relation they define.",
        "conic": "Do not treat every contour as nondegenerate; rank and polar behavior matter.",
        "space": "Do not expect the affine chart to show every object; some objects are only visible through homogeneous representatives.",
        "tensor": "Do not read a diagram as decoration; every wire corresponds to an index contraction.",
        "complex": "Do not separate lines and circles too early; in CP1 they are handled by the same extended object.",
        "measurement": "Do not assume Euclidean distance is primitive; the absolute conic is doing the measuring.",
        "hyperbolic": "Do not measure disk pictures with Euclidean distance unless the model explicitly says the property is conformal.",
    }.get(mode, "Do not let visual plausibility replace the explicit invariant check.")


def _mode_lab(mode: str) -> str:
    return {
        "incidence": "For incidence chapters, identify the dot products or determinant vanishings that turn the figure into a theorem.",
        "line": "For line chapters, recompute the same four marked points after a Mobius map and confirm the cross-ratio.",
        "bracket": "For bracket chapters, rescale one point and watch which determinant values change and which relation remains.",
        "conic": "For conic chapters, pick a point and compare its tangent with its polar line.",
        "space": "For higher-dimensional chapters, switch between affine and homogeneous viewpoints and note what disappears at infinity.",
        "tensor": "For diagram chapters, follow a wire through the diagram and translate it into one contracted index.",
        "complex": "For complex chapters, track how a Mobius map moves roots, circles, and the point at infinity.",
        "measurement": "For measurement chapters, change the absolute conic and observe which constructions still look Euclidean.",
        "hyperbolic": "For hyperbolic chapters, move points toward the boundary and watch distances grow while angles may remain visually conformal.",
    }.get(mode, "Perturb the displayed construction and recompute its check.")


def _takeaway_by_mode(mode: str) -> str:
    return {
        "incidence": "Incidence geometry becomes dependable when every visually suggested meeting is backed by a join, meet, or determinant check.",
        "line": "A projective line is best understood through transformations of coordinates and invariants that ignore those coordinates.",
        "bracket": "Bracket expressions provide a compact algebraic memory of projective configurations.",
        "conic": "Conics are computational operators, not just curves drawn on the page.",
        "space": "Projective d-space replaces special cases with a uniform subspace calculus.",
        "tensor": "Tensor diagrams make invariant algebra inspectable as a proof object.",
        "complex": "Complex projective geometry turns measurement and circularity into projective statements.",
        "measurement": "Cayley-Klein thinking makes metric geometry a projective construction relative to an absolute.",
        "hyperbolic": "Hyperbolic models are coordinated views of one geometry, each preserving different features visually.",
    }.get(mode, "The visual and computational forms support the same geometric claim.")


def main() -> None:
    (BOOK_ROOT / "artifacts").mkdir(exist_ok=True)
    (BOOK_ROOT / "scripts").mkdir(exist_ok=True)
    (BOOK_ROOT / "utils").mkdir(exist_ok=True)
    for part in inv.PARTS:
        (BOOK_ROOT / str(part["id"])).mkdir(parents=True, exist_ok=True)

    for chapter in inv.CHAPTERS:
        folder = BOOK_ROOT / str(chapter["folder"])
        folder.mkdir(parents=True, exist_ok=True)
        root = ensure_artifact_root(inv.artifact_root(chapter))
        save_json(storyboard_for(chapter), root, "checks", "storyboard.json")
        bundle = render_chapter_visuals(chapter, root)
        save_json(
            {
                "chapter": chapter["number"],
                "artifacts": bundle["relative_display_paths"],
                "checks": bundle["checks"],
                "prebuilt_artifacts": True,
            },
            root,
            "checks",
            "final-sanity.json",
        )
        write_notebook(folder / str(chapter["notebook"]), notebook_for(chapter))
    print(f"Bootstrapped {len(inv.CHAPTERS)} canonical notebooks and artifact trees.")


if __name__ == "__main__":
    main()
