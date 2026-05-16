"""Bootstrap the LSG standalone visualization-first notebook course.

This one-time course build uses lecture-specific inventory data extracted from
the local PDF table of contents. It writes original notebook prose, executable
checks, and artifact displays. Future chapter improvements should edit the
canonical notebooks directly.
"""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

SCRIPT_DIR = Path(__file__).resolve().parent
BOOK_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lsg_inventory import ENTRIES, PARTS, inventory

KERNEL_METADATA = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "pygments_lexer": "ipython3"},
}


def _bullet(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def lesson_markdown(entry: dict[str, object]) -> list[str]:
    sections = list(entry["sections"])
    concepts = list(entry["concepts"])
    concept_sentence = ", ".join(str(item) for item in concepts[:-1]) + f", and {concepts[-1]}"
    section_sentence = "; ".join(str(item) for item in sections)
    return [
        f"""
# {entry['label']}: {entry['title']}

**Source span.** Printed pages {entry['printed_span']}; physical PDF pages {entry['pdf_span']} in `Lectures on Symplectic Geometry.pdf`.

**Lecture goal.** {entry['focus']} The notebook is written as a standalone computational lesson: the PDF fixes the lecture order and terminology, while the explanations, diagrams, checks, and labs here are original.

The fastest way to read this lecture visually is to keep two ledgers open at once. The first ledger is algebraic: which matrices, forms, vector fields, or quotient maps are being asserted to exist? The second ledger is geometric: which visible object should stay unchanged when coordinates, flows, group actions, or reductions are applied? In this lecture the main objects are {concept_sentence}. The diagrams and checks below turn those objects into something inspectable rather than merely named.
""",
        f"""
## Translation Guide

The lecture sections are: {section_sentence}. In computational terms, these sections ask us to build a small model with explicit coordinates and then test the invariant that survives a change of viewpoint. A two-form becomes a skew matrix or a callable bilinear pairing. A submanifold becomes a parametrized array whose tangent directions can be sampled. A group action becomes both a plotted orbit and an infinitesimal vector field. A quotient or normal form becomes a dimension count plus a residual that should vanish.

For this lecture, the key translation is:

{_bullet([str(item) for item in concepts])}

The useful habit is to identify the "witness" for each definition. Nondegeneracy is witnessed by an invertible matrix. A Lagrangian condition is witnessed by a zero pullback of the two-form. A Hamiltonian action is witnessed by the identity `d<mu,xi> = i_X omega`. A toric polytope is witnessed by primitive adjacent normals with determinant plus or minus one. The exact witness changes across the course, but the workflow stays stable: define the geometric object, visualize the structure it imposes, and then make the invariant fail loudly if a hypothesis is removed.
""",
        f"""
## Visual Storyboard

The artifact set for this lecture has three parts. The concept-route graph is a dependency map: it shows which definitions and proof moves feed the lecture's invariant. The primary PNG, `{entry['visual']}`, is the static inspection surface for the main construction. The interactive HTML parameter lab lets you vary or inspect the same model with a lighter touch than a long symbolic derivation.

The inspection target is deliberately concrete: {entry['lab']} A decorative plot would not be enough here; the figure must either preserve a form, expose a kernel, show a quotient, display a moment image, or record a positivity or determinant condition. When the notebook displays an artifact, read the nearby check in the same breath. The plot tells you what to look at; the JSON check records the numerical or symbolic invariant that keeps the picture honest.
""",
        f"""
## Proof And Invariant Scaffold

{entry['proof']} This notebook treats that proof idea as a testable scaffold. The scaffold has three rungs. First, it isolates the local model from the lecture: a standard symplectic vector space, a cotangent chart, a flow, a contact form, a complex triple, a Hamiltonian phase plane, a moment-map level, or a Delzant polygon. Second, it draws the part of the model that the learner should inspect. Third, it computes a residual: a skew-symmetry defect, a Lagrangian pullback, an energy derivative, a moment-map identity, a quotient dimension count, or a Delzant determinant defect.

The residual is not a substitute for proof, but it is a useful proof companion. It forces each visual to state what would go wrong if the hypotheses were loosened. For example, a non-closed deformation in a Moser argument will not be cancelled by the selected vector field; a nonsmooth toric corner fails the unimodular determinant test; a candidate Hamiltonian vector field that is not tangent to energy levels shows up immediately as a nonzero derivative of `H` along its own flow.
""",
        f"""
## Mini Lab

Use the displayed artifacts as a launch pad. Change one parameter in the code cell for the diagnostic and predict which check should remain zero. Then change a hypothesis: use a nonsymplectic matrix, a nonclosed one-form, a nonconvex Lagrangian, a nonfree group action, or a bad toric normal. The point of the lab is to distinguish coordinate accidents from structural invariants.

**Takeaways.**

- The source lecture is represented here by its definitions, theorem moves, and examples, not by copied prose or figures.
- The primary concept for this lecture is inspectable through `{entry['visual']}`.
- The final sanity cell asserts that the artifacts exist and that the lecture-specific diagnostic passes.
- The best next question is not "what formula was written?" but "which geometric quantity did the formula certify?"
""",
    ]


def setup_code(entry: dict[str, object]) -> str:
    return f"""
from pathlib import Path
import json
import sys

import numpy as np


def find_book_root(start=None):
    start = Path.cwd() if start is None else Path(start)
    for candidate in [start, *start.parents]:
        if (candidate / "AGENTS.md").exists() and (candidate / "Lectures on Symplectic Geometry.pdf").exists():
            return candidate
    raise RuntimeError("Could not locate the Lectures-on-Symplectic-Geometry course root.")


BOOK_ROOT = find_book_root()
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.artifacts import display_artifact, read_json
from utils.symplectic import (
    delzant_vertex_determinants,
    hamiltonian_vector_field,
    lagrangian_residual,
    lecture_diagnostic,
    moment_circle,
    poisson_bracket,
    rotation_symplectic,
    standard_omega,
    symplectic_residual,
)

LECTURE_NUMBER = {int(entry["number"])}
LECTURE_THEME = {entry["theme"]!r}
ARTIFACT_TOPIC = {entry["artifact_topic"]!r}
ARTIFACT_ROOT = BOOK_ROOT / "artifacts" / ARTIFACT_TOPIC
print(f"Book root: {{BOOK_ROOT}}")
print(f"Artifact root: {{ARTIFACT_ROOT.relative_to(BOOK_ROOT)}}")
"""


def display_code(entry: dict[str, object]) -> str:
    slug = f"{int(entry['number']):02d}-{entry['title']}".lower()
    return f"""
storyboard = read_json(ARTIFACT_ROOT / "checks" / "visual-storyboard.json")
for item in storyboard["visual_sequence"]:
    path = BOOK_ROOT / item["artifact"]
    print(f"{{item['concept']}} -> {{path.relative_to(BOOK_ROOT)}}")
    display_artifact(path, width=760, height=430 if path.suffix == ".html" else None)

storyboard["diagnostic"]
"""


def diagnostic_code(entry: dict[str, object]) -> str:
    theme = str(entry["theme"])
    if theme in {"linear", "complex", "kahler"}:
        return """
omega = standard_omega(1)
A = rotation_symplectic(0.17 * LECTURE_NUMBER)
residual = symplectic_residual(A, omega)
J = np.array([[0.0, -1.0], [1.0, 0.0]])
metric = omega @ J
print({"symplectic_residual": residual, "J_squared": J @ J, "metric_eigenvalues": np.linalg.eigvalsh(metric)})
assert residual < 1e-12
assert np.allclose(J @ J, -np.eye(2))
"""
    if theme in {"cotangent", "lagrangian", "generating", "darboux"}:
        return """
omega = standard_omega(1)
zero_section_tangent = np.array([[1.0], [0.0]])
graph_tangent = np.array([[1.0], [0.35 * np.cos(0.35)]])
zero_residual = lagrangian_residual(zero_section_tangent, omega)
graph_residual = lagrangian_residual(graph_tangent, omega)
print({"zero_section_lagrangian_residual": zero_residual, "one_dimensional_graph_residual": graph_residual})
assert zero_residual < 1e-12
assert graph_residual < 1e-12
"""
    if theme in {"hamiltonian", "variational", "legendre", "recurrence"}:
        return """
point = np.array([0.4, -0.7])
grad_h = point.copy()
X_H = hamiltonian_vector_field(grad_h)
energy_derivative = float(grad_h @ X_H)
bracket_hh = poisson_bracket(grad_h, grad_h)
print({"X_H": X_H, "dH(X_H)": energy_derivative, "{H,H}": bracket_hh})
assert abs(energy_derivative) < 1e-12
assert abs(bracket_hh) < 1e-12
"""
    if theme in {"actions", "moment", "reduction", "gauge", "cohomology"}:
        return """
theta = np.linspace(0, 2 * np.pi, 9)
orbit_values = [moment_circle(np.exp(1j * t)) for t in theta]
spread = float(max(orbit_values) - min(orbit_values))
print({"moment_values_on_unit_orbit": orbit_values[:4], "spread": spread})
assert spread < 1e-12
"""
    if theme in {"toric", "dh"}:
        return """
normals = [(1, 0), (0, 1), (-1, -1)]
determinants = delzant_vertex_determinants(normals)
defect = max(abs(abs(det) - 1) for det in determinants)
print({"adjacent_normal_determinants": determinants, "Delzant_defect": defect})
assert defect == 0
"""
    return """
diagnostic = lecture_diagnostic(LECTURE_THEME, LECTURE_NUMBER)
print(diagnostic)
assert diagnostic.passed
"""


def sanity_code(entry: dict[str, object]) -> str:
    return """
final_sanity = read_json(ARTIFACT_ROOT / "checks" / "final-sanity.json")
for relative in final_sanity["artifacts"]:
    path = BOOK_ROOT / relative
    assert path.exists(), f"missing artifact: {relative}"
    assert path.stat().st_size > 0, f"empty artifact: {relative}"

diagnostic = lecture_diagnostic(LECTURE_THEME, LECTURE_NUMBER)
assert diagnostic.passed, diagnostic
assert final_sanity["diagnostic"]["passed"] is True
print({
    "checked_artifact_count": len(final_sanity["artifacts"]),
    "diagnostic": diagnostic.name,
    "value": diagnostic.value,
})
"""


def write_notebook(entry: dict[str, object]) -> Path:
    cells = []
    for markdown in lesson_markdown(entry):
        cells.append(new_markdown_cell(textwrap.dedent(markdown).strip() + "\n"))
    cells.insert(1, new_code_cell(textwrap.dedent(setup_code(entry)).strip() + "\n"))
    cells.insert(4, new_code_cell(textwrap.dedent(display_code(entry)).strip() + "\n"))
    cells.insert(6, new_code_cell(textwrap.dedent(diagnostic_code(entry)).strip() + "\n"))
    cells.append(new_code_cell(textwrap.dedent(sanity_code(entry)).strip() + "\n"))
    notebook = new_notebook(cells=cells, metadata=KERNEL_METADATA)
    path = BOOK_ROOT / str(entry["part"]) / str(entry["folder"]) / str(entry["notebook"])
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, path)
    return path


def main() -> None:
    (BOOK_ROOT / "source-map.json").write_text(json.dumps(inventory(), indent=2), encoding="utf-8")
    for part in PARTS:
        (BOOK_ROOT / str(part["folder"])).mkdir(parents=True, exist_ok=True)
    paths = [write_notebook(entry) for entry in ENTRIES]
    subprocess.run([sys.executable, str(SCRIPT_DIR / "build_lsg_artifacts.py")], check=True)
    subprocess.run([sys.executable, str(SCRIPT_DIR / "build_lsg_course_indexes.py")], check=True)
    print(f"Bootstrapped {len(paths)} lecture notebooks.")


if __name__ == "__main__":
    main()
