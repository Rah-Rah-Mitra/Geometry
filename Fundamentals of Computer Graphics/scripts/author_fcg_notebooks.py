"""Author the initial canonical FCG notebooks from the course inventory.

This is a bootstrap authoring aid for the first course conversion. Subsequent
chapter revisions should edit the canonical notebooks directly.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any

import fcg_inventory as inventory

BOOK_ROOT = inventory.BOOK_ROOT

CONCEPTS = {
    1: ["graphics areas", "applications", "APIs", "pipeline", "floating point", "debug images"],
    2: ["mappings", "quadratics", "vectors", "barycentric coordinates", "probability", "Monte Carlo"],
    3: ["raster devices", "pixels", "RGB", "gamma", "quantization", "alpha compositing"],
    4: ["viewing rays", "perspective", "ray intersection", "closest hit", "shading", "reflection"],
    5: ["point lights", "Lambert cosine", "diffuse color", "half vector", "specular exponent", "ambient fill"],
    6: ["determinants", "matrix maps", "inverse", "linear systems", "eigenvectors", "SVD"],
    7: ["linear transforms", "homogeneous coordinates", "composition order", "normal transforms", "coordinate frames", "inverses"],
    8: ["camera basis", "projection", "frustum", "homogeneous divide", "viewport", "field of view"],
    9: ["object order rendering", "rasterization", "barycentric interpolation", "z-buffer", "antialiasing", "culling"],
    10: ["sampling", "convolution", "filters", "Fourier spectra", "reconstruction", "aliasing"],
    11: ["texture coordinates", "perspective correction", "mipmaps", "bump mapping", "environment maps", "procedural textures"],
    12: ["triangle meshes", "adjacency", "scene graphs", "spatial data structures", "BSP trees", "tiled arrays"],
    13: ["measure", "inverse CDF", "rejection sampling", "stratification", "disk sampling", "hemisphere sampling"],
    14: ["radiometry", "Fresnel", "refraction", "attenuation", "BRDF", "rendering equation"],
    15: ["parametric curves", "continuity", "polynomial pieces", "Bezier", "B-splines", "NURBS"],
    16: ["timing", "keyframes", "splines", "quaternions", "rigs", "particles"],
    17: ["GPU pipeline", "buffers", "state", "shaders", "attributes", "textures"],
    18: ["spectra", "tristimulus values", "chromaticity", "RGB", "LAB", "adaptation"],
    19: ["contrast", "spatial vision", "illusions", "depth cues", "motion", "picture perception"],
    20: ["dynamic range", "tone curves", "luminance", "local contrast", "color preservation", "night mapping"],
    21: ["implicit fields", "level sets", "skeletal primitives", "blending", "CSG", "warping"],
    22: ["platform budgets", "LOD", "texture memory", "normal maps", "optimization", "production pipeline"],
    23: ["data types", "task abstraction", "visual encoding", "interaction", "linked views", "validation"],
}

STORYBOARDS = {
    1: ["a pipeline flow diagram", "a false-color debugging image", "IEEE special-value checks"],
    2: ["a barycentric triangle reconstruction", "a quadratic root plot", "a Monte Carlo convergence check"],
    3: ["a gamma and quantization strip", "an alpha-over compositing lab", "array shape and value-range checks"],
    4: ["a shaded sphere from generated rays", "a ray-sphere hit calculation", "a reflection-vector check"],
    5: ["a light-direction shading gallery", "a half-vector specular comparison", "falloff and clamping checks"],
    6: ["a unit circle transformed into an ellipse", "basis-vector column diagrams", "determinant identities"],
    7: ["a composed transform on a square", "a projected cube", "normal and homogeneous-coordinate checks"],
    8: ["a camera-space projection of a cube", "field-of-view reasoning", "basis orthogonality checks"],
    9: ["a barycentric raster triangle", "covered-pixel summaries", "edge and interpolation checks"],
    10: ["a sampled signal", "a normalized convolution kernel", "a Fourier magnitude plot"],
    11: ["affine vs perspective texture lookup", "UV range checks", "filtering and mip-level discussion"],
    12: ["a cube mesh adjacency view", "topology count bars", "edge-incidence checks"],
    13: ["disk and hemisphere samples", "CDF diagnostics", "integral estimates"],
    14: ["a transport-oriented sphere gallery", "Fresnel and path-sampling checks", "BRDF energy discussion"],
    15: ["Bezier control polygon and curve", "speed-vs-parameter plot", "endpoint and arc-length checks"],
    16: ["keyframe motion path", "quaternion slerp plot", "normalization checks"],
    17: ["a mini GPU style raster artifact", "buffer and shader-stage reasoning", "depth/interpolation checks"],
    18: ["xy chromaticity points", "sRGB transfer curve", "round-trip checks"],
    19: ["contrast sensitivity curve", "lightness context stimulus", "stimulus parameter checks"],
    20: ["HDR gradient tone mapping", "tone curve monotonicity", "output-range checks"],
    21: ["implicit field contours", "soft blend contours", "inside/outside statistics"],
    22: ["LOD frame-budget dashboard", "texture-memory tiers", "budget-ratio checks"],
    23: ["node-link data view", "encoding precision sketch", "graph and filtering checks"],
}


def nb(cells: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def md(source: str, cell_id: str) -> dict[str, Any]:
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": textwrap.dedent(source).strip().splitlines(keepends=True)}


def code(source: str, cell_id: str) -> dict[str, Any]:
    return {"cell_type": "code", "id": cell_id, "execution_count": None, "metadata": {}, "outputs": [], "source": textwrap.dedent(source).strip().splitlines(keepends=True)}


def prose(entry: dict[str, Any]) -> str:
    chapter = int(entry["chapter"])
    title = str(entry["title"])
    concepts = CONCEPTS[chapter]
    storyboard = STORYBOARDS[chapter]
    concept_sentence = ", ".join(concepts[:-1]) + f", and {concepts[-1]}"
    story_sentence = "; ".join(storyboard)
    guide_rows = "\n".join(
        f"| {concept} | Treat it as a quantity, transformation, image, or data structure that can be generated, measured, and checked in code. |"
        for concept in concepts
    )
    return f"""
    # Chapter {chapter:02d}: {title}

    Source orientation: printed pages {entry['printed']}; physical PDF pages {entry['pdf']}. This notebook is standalone: it uses the source span only to orient the topics and then teaches the material through original explanations, generated visuals, executable experiments, and reproducible checks.

    ## Chapter Question

    How can we make {title.lower()} inspectable instead of merely descriptive? In this course the answer is to translate each idea into a small computational object: an array, a vector, a transform, a field, a sampling rule, a diagram, or a measured invariant. For this chapter the central vocabulary is {concept_sentence}. The notebook is written for a reader who wants to understand the graphics idea well enough to test it, adapt it, and recognize when an implementation has gone wrong.

    ## Why This Chapter Matters

    Computer graphics is unusually visual even when the underlying topic looks algebraic or architectural. A renderer can fail because a sign convention is wrong, because a sample distribution is biased, because a color value is encoded in the wrong space, because a mesh adjacency relation is inconsistent, or because a transform has been applied in the wrong order. The best way to learn the chapter is therefore to build small objects whose behavior can be seen and audited. The figures below are not illustrations pasted next to the text; they are generated evidence for the claims the notebook makes.

    This chapter also acts as a bridge to the rest of the book. The ideas here feed later notebooks whenever pixels must be generated, geometry must be moved, light must be evaluated, a signal must be sampled, or a human viewer must interpret the result. The examples are deliberately compact, because compact examples make invariants easier to inspect. A production renderer or visualization system may be much larger, but the same checks still apply: dimensions must agree, ranges must be controlled, normals must be normalized, samples must match their intended measure, and every visual output must have a reason to exist.

    ## Translation guide

    | Book concept | Computational translation |
    | --- | --- |
    {guide_rows}

    The translation guide is the working contract for the notebook. If a paragraph introduces a geometric or imaging claim, a nearby cell either visualizes the claim or records a check that would catch a common mistake. This does not mean every idea needs a large figure. Sometimes a small numeric assertion is better than a plot. Sometimes a plotted construction is more useful than a long derivation. The point is to keep the explanation inspectable.

    ## Route Through The Chapter

    1. Establish the local vocabulary and the chapter question.
    2. Build a generated visual artifact that exposes the chapter's dependency structure.
    3. Build a second visual artifact focused on the most practical computation in the chapter.
    4. Record numeric checks that can be re-run after edits.
    5. Finish with an applied lab and takeaways that connect the chapter to later rendering, modeling, image, or visualization work.

    ## Visual storyboard

    The planned visual sequence is: {story_sentence}. Each artifact is saved under `artifacts/chapter-{chapter:02d}/` so the notebook can be executed from its own folder while still keeping outputs in the book-local artifact tree. The first figure is a concept dependency map. It helps the reader see which ideas should be held together when debugging or extending an implementation. The second figure is chapter-specific and turns one of the main algorithms or representations into an inspectable object.

    ## Concept Notes

    The first habit this chapter builds is separating representation from interpretation. A tuple of numbers may be a color, a point, a direction, a homogeneous coordinate, a probability sample, or a display-space pixel. The operations that are valid for one interpretation can be invalid for another. The notebook therefore names the meaning of every important array and records the checks that preserve that meaning. This is especially useful in computer graphics because the final output is often an image that can look plausible even when one part of the computation is conceptually wrong.

    The second habit is to use deliberately small scenes and synthetic data. Synthetic examples are not a compromise here; they are a microscope. A controlled triangle, sphere, color ramp, signal, curve, mesh, or graph lets us know the expected answer before the system becomes visually complicated. Once the simple case behaves correctly, the same machinery can be reused with richer assets. This is also why the notebook avoids external image or model files. All artifacts are reproducible from code cells.

    The third habit is to pair visuals with invariants. A plot can reveal structure quickly, but a check can keep the structure from silently drifting when code changes. In this chapter the checks emphasize quantities such as sums, ranges, reconstruction errors, normalization, monotonicity, topology counts, sample statistics, or transform consistency. These checks are intentionally small enough to read. They are not a substitute for a full test suite, but they make the notebook robust as a teaching artifact.

    ## Worked Example

    The worked example below uses the shared course helpers rather than a hidden external framework. The goal is not to build a production graphics engine inside a notebook. The goal is to make the core idea of {title.lower()} concrete enough that a learner can inspect inputs, outputs, and failure modes. The generated visual is saved as a durable PNG, displayed inline, and summarized by a JSON file containing the numeric checks.

    ## Applied lab

    Modify one parameter in the chapter-specific visual and predict which invariant should change. For example, change a vector, a light direction, a sampling seed, a transform, a tone curve exposure, a control point, or a graph layout seed. Re-run the visual and compare the JSON checks before and after the change. A good lab response names both a visual change and a numeric change. If the visual changes but the numeric check does not, the check is probably too weak. If the numeric check changes but the visual does not, the display may be hiding the behavior that matters.

    A second lab is to design a failure case. Choose one assumption from the translation guide and violate it: pass an unnormalized normal, move a point outside a triangle, set a field threshold too high, use an undersampled signal, apply a transform in the wrong order, or clip a color value too early. The purpose is to learn what the failure looks like. In graphics, recognizing the visual signature of an error is often faster than single-stepping through thousands of repeated pixel or vertex operations.

    ## Sanity checks

    The final cells assert that generated artifacts exist, are nonblank, and have nontrivial file size. They also write the chapter's numeric check summary. These checks make the notebook safe to execute with `nbclient` and useful for later QC.

    ## Takeaways

    - {title} becomes easier when concepts are converted into arrays, functions, diagrams, and invariants.
    - Visuals should expose structure or failure modes, not decorate the page.
    - The artifact JSON file is part of the lesson because it records what the figure is supposed to prove.
    - The small example is a seed for larger graphics systems: keep the checks, then scale the data.
    """


SETUP_CODE = """
from pathlib import Path
import sys

BOOK_ROOT = Path.cwd()
for candidate in [BOOK_ROOT, *BOOK_ROOT.parents]:
    if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
        BOOK_ROOT = candidate
        break
else:
    raise RuntimeError("Could not find the FCG book root")

if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

ARTIFACT_ROOT = BOOK_ROOT / "artifacts" / f"chapter-{CHAPTER:02d}"
ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
"""


def notebook_for(entry: dict[str, Any]) -> dict[str, Any]:
    chapter = int(entry["chapter"])
    title = str(entry["title"])
    concepts = CONCEPTS[chapter]
    return nb(
        [
            md(prose(entry), f"chapter-{chapter:02d}-prose"),
            code(
                f"""
                CHAPTER = {chapter}
                TITLE = {title!r}
                CONCEPTS = {concepts!r}
                PRINTED_PAGES = {entry['printed']!r}
                PDF_PAGES = {entry['pdf']!r}
                """,
                f"chapter-{chapter:02d}-metadata",
            ),
            code(SETUP_CODE, f"chapter-{chapter:02d}-setup"),
            code(
                """
                from utils.artifacts import assert_artifacts, display_artifact, save_json
                from utils.course_visuals import create_chapter_visuals
                from utils.notebook_checks import assert_nonblank_image
                """,
                f"chapter-{chapter:02d}-imports",
            ),
            code(
                """
                result = create_chapter_visuals(CHAPTER, TITLE, CONCEPTS, f"chapter-{CHAPTER:02d}")
                artifact_paths = result["paths"]
                check_path = result["check_path"]
                result["checks"]
                """,
                f"chapter-{chapter:02d}-generate-visuals",
            ),
            code(
                """
                for path in artifact_paths:
                    display_artifact(path, width=760)
                display_artifact(check_path)
                """,
                f"chapter-{chapter:02d}-display-artifacts",
            ),
            code(
                """
                artifact_records = assert_artifacts([*artifact_paths, check_path])
                image_records = [assert_nonblank_image(path) for path in artifact_paths]
                assert result["checks"]["concept_count"] == len(CONCEPTS)
                artifact_records
                """,
                f"chapter-{chapter:02d}-artifact-checks",
            ),
            code(
                """
                final_report = {
                    "chapter": CHAPTER,
                    "title": TITLE,
                    "printed_pages": PRINTED_PAGES,
                    "pdf_pages": PDF_PAGES,
                    "artifact_count": len(artifact_paths),
                    "nonblank_images": len(image_records),
                    "checks": result["checks"],
                }
                final_path = save_json(final_report, f"chapter-{CHAPTER:02d}", "final-sanity.json")
                display_artifact(final_path)
                final_report
                """,
                f"chapter-{chapter:02d}-final-sanity",
            ),
        ]
    )


def main() -> None:
    for entry in inventory.ENTRIES:
        folder = BOOK_ROOT / str(entry["folder"])
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / str(entry["notebook"])
        path.write_text(json.dumps(notebook_for(entry), indent=2), encoding="utf-8")
    print(f"Authored {len(inventory.ENTRIES)} canonical notebooks")


if __name__ == "__main__":
    main()
