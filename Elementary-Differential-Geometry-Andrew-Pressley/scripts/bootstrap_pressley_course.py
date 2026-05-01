"""Bootstrap the Pressley standalone visualization-first notebook course."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

import pressley_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = BOOK_ROOT.parent
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.visuals import build_unit_visuals  # noqa: E402


def markdown_for(entry: dict[str, object]) -> str:
    topics = list(entry["topics"])
    translations = "\n".join(
        f"| {topic.title()} | A data object, computation, or visual check that makes {topic} inspectable. |"
        for topic in topics
    )
    topic_list = "\n".join(f"- {topic}" for topic in topics)
    lenses = []
    for index, topic in enumerate(topics, start=1):
        lenses.append(
            f"**Lens {index}: {topic}.** The notebook treats this idea as something that can be built, "
            f"measured, or varied. A reader should be able to point to the relevant generated artifact and "
            f"say what object is being represented, which relation is being tested, and what value would "
            f"change if the construction were perturbed. For {topic}, the emphasis is on the bridge between "
            f"geometric language and computational state: coordinates, vectors, frames, metrics, curvature "
            f"scalars, topology counts, or transformation data. This is not a replacement for proof, but it "
            f"is a way to keep the proof's moving parts visible while the notation becomes more abstract."
        )
    lenses_text = "\n\n".join(lenses)
    storyboard = "\n".join(
        f"- `{kind}`: a generated artifact that makes the {str(kind).replace('-', ' ')} aspect visible and checkable."
        for kind in entry["visual_kinds"]
    )
    return f"""
# {entry['label']}: {entry['title']}

Source orientation: printed pages {entry['printed_span']}; PDF pages {entry['pdf_span']}; sections {entry['sections']}.

This notebook is an original standalone teaching version of the assigned span. It does not reproduce textbook prose, exercise text, figures, screenshots, or page crops. The local PDF is used only to orient the chapter structure and mathematical agenda. The explanations below are written so that a reader can work through the material with this notebook open and the PDF closed.

## Chapter Question

{entry['focus']}

The course treats that focus as a set of geometric objects, relations, transformations, and invariants that can be inspected. A static figure is used when a proof state, construction dependency, or comparison is clearest as a labeled diagram. A plotted surface is used when depth, tangent data, normal variation, or curvature sign is the teaching object. A numeric or symbolic check is used whenever the notebook can turn a geometric promise into a measurable residual.

## Translation Guide

| Book-side idea | Computational translation |
| --- | --- |
{translations}

## Route Through The Notebook

The route has four passes. First, the chapter idea is stated in ordinary mathematical language so the reader knows what problem is being solved. Second, the objects are translated into computational data: points, curves, level sets, frames, patches, metrics, forms, matrices, transformations, meshes, or topology counts. Third, the generated artifacts make the geometry visible and provide inspection targets. Fourth, the applied lab records small checks that can be rerun after changing parameters.

The route is intentionally visual-first. The notebook does not use diagrams as decoration after the theory has already happened. The diagrams and plots are the working surface of the explanation. If a construction claims that a tangent vector measures first-order motion, the code draws sample tangents. If a surface claim depends on the metric, the code displays local distortion and records a residual. If a theorem relates curvature to topology, the notebook keeps a visual ledger of both the local quantities and the global count.

## Core Topics

{topic_list}

{lenses_text}

## Visualization Storyboard

{storyboard}

Each artifact has a concept-naming filename and lives under `artifacts/{entry['artifact']}/`. Static PNGs are meant to remain readable in version control and exported notebooks. The final sanity cell checks that the artifacts exist and that the numerical checks are available as JSON.

## Worked Example Philosophy

A worked example in this course has three responsibilities. It must name the geometric claim, show the data that represents the claim, and report a check that would fail if the construction or model were wrong. A curve example is not just a trace; it includes the parameter values, speeds, tangents, curvature, or self-intersections that make the trace meaningful. A surface example is not just a shaded picture; it includes tangent vectors, normal changes, metric coefficients, or curvature signs. A hyperbolic model is not just a disk drawing; it distinguishes screen shape from model distance.

This style is deliberately modest. The code is not a formal proof assistant, and the visuals do not replace proofs. They provide a laboratory for seeing why a definition was chosen, where an assumption enters, and what invariant a theorem is trying to protect. The mathematical prose and the computation should therefore meet in the middle: prose names the concept; code makes it inspectable; checks prevent the picture from becoming empty illustration.

## Pitfalls To Watch

The first pitfall is confusing a convenient parameter with the geometry itself. Many quantities simplify under unit-speed parametrization, orthogonal coordinates, or a special surface patch, but the geometric statement should survive a legitimate reparametrization. The notebook therefore records what changes with the chosen coordinates and what is invariant.

The second pitfall is overfitting to one diagram. Classical differential geometry often starts from a beautifully chosen drawing, but a drawing can hide singular cases, orientation choices, or boundary behavior. The generated examples here keep a small amount of variation in view and pair each picture with a check. When a statement depends on regularity, orientability, compactness, or a model condition, the text says so.

The third pitfall is treating symbolic formulas as the endpoint. Pressley's subject is full of formulas, but the formulas are useful because they measure visible geometric behavior: turning, bending, stretching, holonomy, area distortion, and topological bookkeeping. The notebook asks the reader to inspect that behavior before and after reading the formula.

## Applied Lab

The lab table below is intentionally small. It is a set of reproducible checkpoints that can be inspected before the reader changes parameters or extends the notebook. The values are not meant to exhaust the chapter. They anchor the chapter's core invariant: speed and arc length, curvature and torsion, Euler characteristic, metric distortion, surface curvature, hyperbolic distance, minimal-surface mean curvature, or matrix eigenstructure.

## Takeaways

By the end of this unit, the reader should be able to state the main geometric objects, identify the assumptions or operations that create them, read the generated artifacts as evidence, and rerun the sanity checks. The course will reuse this habit throughout: every important classical claim is paired with a model, a diagram, or a small computation that makes the claim visible without copying the textbook.
""".strip()


def setup_code(unit: str) -> str:
    return f'''
from pathlib import Path
import sys

BOOK_ROOT = Path.cwd()
for candidate in [BOOK_ROOT, *BOOK_ROOT.parents]:
    if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
        BOOK_ROOT = candidate
        break
else:
    raise RuntimeError("Could not find the Pressley book root")

if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

UNIT = "{unit}"
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"
UNIT_ARTIFACT_ROOT = ARTIFACT_ROOT / UNIT
UNIT_ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)

from utils.artifacts import assert_artifact, display_artifact, save_json
from utils.visuals import build_unit_visuals, unit_lab_data
'''.strip()


def notebook_for(entry: dict[str, object]) -> nbformat.NotebookNode:
    cells = [
        new_markdown_cell(markdown_for(entry)),
        new_code_cell(setup_code(str(entry["artifact"]))),
        new_markdown_cell(
            "## Generated Visual Artifacts\n\n"
            "The next cell creates or refreshes the durable artifacts for this unit. "
            "The following display cell renders the PNG figures inline so the notebook remains a visual lesson, not merely a script."
        ),
        new_code_cell('visuals = build_unit_visuals(UNIT, root=ARTIFACT_ROOT)\nvisuals["checks"]'),
        new_code_cell(
            'for artifact in visuals["paths"]:\n'
            '    if artifact.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:\n'
            "        display_artifact(artifact, width=920)"
        ),
        new_markdown_cell(
            "## Applied Lab Data\n\n"
            "This table is a deliberately small numerical foothold. It records the kind of invariant that the chapter will keep returning to."
        ),
        new_code_cell("import pandas as pd\n\nlab_table = pd.DataFrame(unit_lab_data(UNIT))\nlab_table"),
        new_markdown_cell(
            "## Sanity Checks\n\n"
            "The final cell asserts that every generated artifact exists and writes a compact JSON summary into the unit's check folder."
        ),
        new_code_cell(
            'artifact_paths = [assert_artifact(path, min_bytes=(32 if path.suffix.lower() == ".json" else 256)) for path in visuals["paths"]]\n'
            "summary = {\n"
            "    \"unit\": UNIT,\n"
            "    \"artifact_count\": len(artifact_paths),\n"
            "    \"artifact_names\": [path.name for path in artifact_paths],\n"
            "    \"visual_checks\": visuals[\"checks\"],\n"
            "    \"lab_rows\": len(lab_table),\n"
            "}\n"
            'sanity_path = save_json(summary, UNIT, "checks", "notebook-sanity.json", root=ARTIFACT_ROOT)\n'
            "assert_artifact(sanity_path, min_bytes=128)\n"
            "assert summary[\"artifact_count\"] >= 1\n"
            "assert summary[\"lab_rows\"] >= 1\n"
            "summary"
        ),
    ]
    nb = new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python", "pygments_lexer": "ipython3"}
    return nb


def write_notebooks() -> None:
    for entry in inventory.ENTRIES:
        folder = BOOK_ROOT / str(entry["folder"])
        folder.mkdir(parents=True, exist_ok=True)
        nbformat.write(notebook_for(entry), folder / str(entry["notebook"]))


def generate_artifacts() -> None:
    for entry in inventory.ENTRIES:
        build_unit_visuals(str(entry["artifact"]), root=BOOK_ROOT / "artifacts")


def main() -> None:
    inventory.validate_inventory()
    write_notebooks()
    generate_artifacts()
    subprocess.run(
        [sys.executable, str(BOOK_ROOT / "scripts" / "build_pressley_course_indexes.py")],
        cwd=WORKSPACE_ROOT,
        check=True,
    )
    print(f"Bootstrapped {len(inventory.ENTRIES)} Pressley notebooks and generated visual artifacts.")


if __name__ == "__main__":
    main()
