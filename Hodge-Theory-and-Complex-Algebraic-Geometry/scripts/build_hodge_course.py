"""Build indexes, source maps, artifacts, and initial notebooks for the course."""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import nbformat as nbf

from utils.artifacts import artifact_manifest_entry
from utils.course_data import CHAPTERS, PARTS, Chapter, chapter_to_dict, source_map_rows
from utils.visuals import ensure_chapter_artifacts


def md_cell(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(dedent(text).strip() + "\n")


def code_cell(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(dedent(text).strip() + "\n")


def bullet(items: tuple[str, ...] | list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def library_table(chapter: Chapter) -> str:
    rows = ["| Concept route | Library and reason |", "| --- | --- |"]
    for route in chapter.library_routes:
        if " for " in route:
            lib, reason = route.split(" for ", 1)
            rows.append(f"| {lib} | {reason} |")
        else:
            rows.append(f"| route | {route} |")
    return "\n".join(rows)


def worked_example(chapter: Chapter) -> str:
    kind = chapter.visual_kind
    first = chapter.concepts[0]
    second = chapter.concepts[min(1, len(chapter.concepts) - 1)]
    if kind in {"spectral-sequence"}:
        return (
            f"The worked model for this chapter is a small filtered complex. "
            f"Read the grid by total degree, not by rows alone: the visible classes "
            f"start as {first} data and are then tested by differentials that may "
            f"kill or move them before the associated graded object is reached."
        )
    if kind in {"period-map", "family-deformation"}:
        return (
            f"The worked model keeps topology fixed while the filtration moves. "
            f"The base path represents {first}; the target curve records {second}. "
            f"The key inspection is whether the derivative stays horizontal, meaning "
            f"it lowers the filtration by at most one step."
        )
    if kind in {"abel-jacobi"}:
        return (
            f"The worked model starts after the primary cycle class vanishes. "
            f"A chain integral is reduced modulo a period lattice, so {first} becomes "
            f"a point on a torus rather than an ordinary number. The invariant is the "
            f"torus point, not the chosen lift."
        )
    if kind in {"monodromy", "lefschetz-pencil"}:
        return (
            f"The worked model follows one loop in the base. A class crosses the "
            f"critical value and returns transformed by a matrix action. The check is "
            f"that this action preserves the relevant intersection form while changing "
            f"the component along the vanishing cycle."
        )
    if kind in {"filtration", "chow-filtration"}:
        return (
            f"The worked model is a nested ledger. Each step loses information in a "
            f"controlled way, and the associated graded pieces keep track of what is "
            f"new at that level. This is the right representation for {first} because "
            f"the theorem statements compare layers rather than isolated classes."
        )
    if kind in {"morse-lefschetz"}:
        return (
            f"The worked model is a Morse-level diagram. The only moments that can "
            f"change topology are critical levels; the index attached there predicts "
            f"which cohomological degree can change after passing a hyperplane section."
        )
    if kind in {"resolution-ladder"}:
        return (
            f"The worked model is a resolution ladder. Local objects are easy to glue, "
            f"but global sections do not preserve exactness automatically. The ladder "
            f"makes the failure visible as cohomology."
        )
    return (
        f"The worked model treats {first} and {second} as inspectable data rather than "
        f"as names. The figure and check below are deliberately small, so the invariant "
        f"can be verified without hiding the proof move in a black box."
    )


def proof_scaffold(chapter: Chapter) -> str:
    concept_line = ", ".join(chapter.concepts[:4])
    proof_line = "; ".join(chapter.proof_moves[:3])
    pitfall_line = "; ".join(chapter.pitfalls[:2])
    return (
        f"For this chapter, the proof scaffold starts with {concept_line}. "
        f"The notebook asks the reader to inspect those objects in the same order as "
        f"the main argument: {proof_line}. This is why the artifact is not a decorative "
        f"summary. It gives a finite place to test the hypothesis before the full theorem "
        f"is invoked. When a matrix, grid, torus, filtration, or graph appears below, it "
        f"should be read as a local model of the chapter's proof state: what data is known, "
        f"which map is being applied, and which invariant is supposed to survive. "
        f"The most common ways to misread this chapter are {pitfall_line}. The sanity "
        f"checks below are aimed exactly at those mistakes. They do not prove the book's "
        f"theorems, but they make the theorem's bookkeeping editable, inspectable, and "
        f"falsifiable in a small model."
    )


def notebook_for_chapter(chapter: Chapter) -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    concepts = bullet(chapter.concepts)
    proof_moves = bullet(chapter.proof_moves)
    pitfalls = bullet(chapter.pitfalls)
    checks = bullet(chapter.checks)
    sections = bullet(chapter.sections)
    routes = library_table(chapter)
    example = worked_example(chapter)
    scaffold = proof_scaffold(chapter)
    nb.cells = [
        md_cell(
            f"""
            # {chapter.number}. {chapter.title}

            **Source span.** {chapter.source_span} in `{chapter.pdf_file}`.

            **Course note.** This notebook is original teaching prose with generated
            diagrams and computational checks. It uses the local PDFs only for source
            orientation and page mapping; it does not copy textbook passages, figures,
            screenshots, crops, or exercise text.
            """
        ),
        md_cell(
            f"""
            ## Chapter Goal

            {chapter.goal}

            {chapter.overview}

            The route through this notebook is intentionally visual-first: define the
            objects, inspect a diagram that exposes the invariant, run a small symbolic
            or numeric check, then return to the theorem-level meaning.
            """
        ),
        md_cell(
            f"""
            ## Source Inventory

            The local source map for this chapter lists these sections:

            {sections}

            This source map is used as a coverage guide. The prose below is a fresh
            computational explanation rather than a paraphrase of the PDF.
            """
        ),
        md_cell(
            f"""
            ## Translation Guide

            {concepts}

            The chapter's proof moves are:

            {proof_moves}

            Common traps to keep in view:

            {pitfalls}
            """
        ),
        md_cell(
            f"""
            ## Library Routing

            {routes}

            The selected representation is: {chapter.visual_focus}
            """
        ),
        code_cell(
            f"""
            from pathlib import Path
            import sys

            BOOK_ROOT = Path.cwd()
            while not (BOOK_ROOT / "Hodge Theory and Complex Algebraic Geometry I.pdf").exists():
                if BOOK_ROOT.parent == BOOK_ROOT:
                    raise RuntimeError("Could not locate the Hodge course root")
                BOOK_ROOT = BOOK_ROOT.parent

            if str(BOOK_ROOT) not in sys.path:
                sys.path.insert(0, str(BOOK_ROOT))

            from utils.artifacts import display_artifact
            from utils.course_data import get_chapter
            from utils.visuals import chapter_numeric_checks, ensure_chapter_artifacts

            chapter = get_chapter("{chapter.id}")
            artifact_paths = ensure_chapter_artifacts(chapter, BOOK_ROOT)
            artifact_paths
            """
        ),
        md_cell(
            f"""
            ## Visual Storyboard

            {chapter.visual_focus}

            {example}

            The first artifact is a concept route. The second is the main geometric
            visualization. Read the labels as a dependency map: the arrows identify
            which object or condition is being used to make the next one meaningful.
            """
        ),
        md_cell(
            f"""
            ## Proof Scaffold

            {scaffold}

            The practical reading strategy is to keep three ledgers open at once:
            assumptions, maps, and surviving invariants. Assumptions record the local
            hypotheses that allow the construction to exist. Maps record how forms,
            filtrations, cycles, or cohomology classes move. Surviving invariants record
            what the chapter is really protecting: symmetry, exactness, rank, pairing,
            horizontal movement, support, or a quotient by periods.
            """
        ),
        code_cell(
            """
            display_artifact(artifact_paths["concept_map"])
            display_artifact(artifact_paths["primary_visual"])
            """
        ),
        md_cell(
            f"""
            ## Computational Checks

            The checks are deliberately small models of the chapter's invariants:

            {checks}

            They are not substitutes for the full proofs. Their job is to keep the
            objects honest: boundary maps should square to zero, filtrations should be
            nested, monodromy should preserve pairings, and Hodge ledgers should satisfy
            symmetry constraints when the toy model is meant to be Kahler.
            """
        ),
        code_cell(
            """
            checks = chapter_numeric_checks(chapter)
            checks
            """
        ),
        code_cell(
            """
            assert checks["hodge_symmetry"]
            assert abs(checks["boundary_squared_norm"]) < 1e-12
            assert checks["laplacian_min_eigenvalue"] > -1e-10
            assert checks["filtration_nested"]
            """
        ),
        md_cell(
            f"""
            ## Applied Lab

            {chapter.lab}

            A good way to use the lab is to change one visible input at a time: a
            filtration dimension, a monodromy matrix entry, a cycle support condition,
            or one Hodge number in the toy ledger. The first failing assertion usually
            points to the theorem hypothesis that was silently doing work.
            """
        ),
        code_cell(
            """
            import csv

            ledger_path = Path(artifact_paths["hodge_ledger"])
            with ledger_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

            total_rank = sum(int(row["betti"]) for row in rows)
            rows, total_rank
            """
        ),
        md_cell(
            """
            ## Takeaways

            - The chapter's objects are tracked by an explicit source span, not by
              copied source text.
            - Every visual has an inspection target and a nearby invariant check.
            - The toy computations are intentionally small so that a reader can edit
              them and see which hypothesis breaks.
            """
        ),
        code_cell(
            """
            required = [
                "concept_map",
                "primary_visual",
                "interactive",
                "hodge_ledger",
                "source_span",
                "visual_storyboard",
                "invariants",
                "final_sanity",
            ]
            for key in required:
                path = Path(artifact_paths[key])
                assert path.exists(), path
                assert path.stat().st_size > 0, path

            print(f"validated {chapter.id}: {chapter.title}")
            """
        ),
    ]
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python", "pygments_lexer": "ipython3"}
    return nb


def index_notebook(title: str, body: str) -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    nb.cells = [md_cell(f"# {title}\n\n{body}")]
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python", "pygments_lexer": "ipython3"}
    return nb


def write_nb(path: Path, nb: nbf.NotebookNode) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, path)


def write_source_maps() -> None:
    rows = source_map_rows()
    (ROOT / "inventory").mkdir(exist_ok=True)
    (ROOT / "indexes").mkdir(exist_ok=True)

    (ROOT / "inventory" / "source-map.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    (ROOT / "indexes" / "chapters.json").write_text(
        json.dumps([chapter_to_dict(chapter) for chapter in CHAPTERS], indent=2) + "\n",
        encoding="utf-8",
    )

    csv_path = ROOT / "inventory" / "source-map.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "id",
            "volume",
            "part",
            "chapter",
            "title",
            "printed_start",
            "printed_end",
            "pdf_start",
            "pdf_end",
            "pdf_file",
            "notebook",
            "artifact_key",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fieldnames})

    lines = [
        "# Source Map",
        "",
        "Body pages in both local PDFs use `pdf_page = printed_page + 12`.",
        "The map below is an original inventory from the local tables of contents.",
        "",
        "| id | volume | part | chapter | printed pages | PDF pages | notebook |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['id']} | {row['volume']} | {row['part']} | {row['chapter']} {row['title']} | "
            f"{row['printed_start']}-{row['printed_end']} | {row['pdf_start']}-{row['pdf_end']} | `{row['notebook']}` |"
        )
    (ROOT / "inventory" / "source-map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_indexes() -> None:
    by_volume: dict[int, list[Chapter]] = defaultdict(list)
    by_part: dict[tuple[int, str], list[Chapter]] = defaultdict(list)
    for chapter in CHAPTERS:
        by_volume[chapter.volume].append(chapter)
        by_part[(chapter.volume, chapter.part_slug)].append(chapter)

    book_lines = [
        "This is a standalone visualization-first notebook course for Claire Voisin's two-volume Hodge theory sequence.",
        "",
        "Use the notebooks as the canonical teaching path. The local PDFs remain source anchors for page spans and terminology, not copied content.",
        "",
        "## Volumes",
    ]
    for volume, chapters in by_volume.items():
        volume_slug = chapters[0].volume_slug
        book_lines.append(f"- [{chapters[0].volume_title}]({volume_slug}/00-volume-index.ipynb)")
    book_lines.extend(
        [
            "",
            "## Course-Level Indexes",
            "",
            "- [Source map](inventory/source-map.md)",
            "- [Chapter metadata](indexes/chapters.json)",
            "- [Artifact manifest](indexes/artifact-manifest.json)",
            "",
            "## Validation Commands",
            "",
            "```powershell",
            "uv run python Hodge-Theory-and-Complex-Algebraic-Geometry/scripts/build_hodge_course.py --indexes-only",
            "uv run python -m compileall -q Hodge-Theory-and-Complex-Algebraic-Geometry/utils Hodge-Theory-and-Complex-Algebraic-Geometry/scripts",
            "uv run python Hodge-Theory-and-Complex-Algebraic-Geometry/scripts/audit_hodge_notebooks.py",
            "uv run python Hodge-Theory-and-Complex-Algebraic-Geometry/scripts/audit_hodge_visuals.py",
            "uv run python Hodge-Theory-and-Complex-Algebraic-Geometry/scripts/validate_hodge_course.py --limit 3 --timeout 240",
            "```",
        ]
    )
    write_nb(ROOT / "00-book-index.ipynb", index_notebook("Hodge Theory and Complex Algebraic Geometry", "\n".join(book_lines)))

    for volume, chapters in by_volume.items():
        volume_root = ROOT / chapters[0].volume_slug
        part_lines = [f"## {chapters[0].volume_title}", ""]
        for part_slug, part_title in PARTS[volume]:
            part_chapters = by_part.get((volume, part_slug), [])
            if not part_chapters:
                continue
            part_lines.append(f"- [{part_title}]({part_slug}/00-part-index.ipynb)")
        write_nb(volume_root / "00-volume-index.ipynb", index_notebook(chapters[0].volume_title, "\n".join(part_lines)))

    for (volume, part_slug), chapters in by_part.items():
        part_title = chapters[0].part
        part_path = ROOT / chapters[0].volume_slug / part_slug
        lines = [f"## {part_title}", ""]
        for chapter in chapters:
            lines.append(f"- [{chapter.number}. {chapter.title}]({chapter.folder_slug}/{chapter.notebook_name})")
        write_nb(part_path / "00-part-index.ipynb", index_notebook(part_title, "\n".join(lines)))
        for chapter in chapters:
            body = (
                f"Canonical notebook: [{chapter.notebook_name}]({chapter.notebook_name})\n\n"
                f"Source span: {chapter.source_span}.\n\n"
                f"Artifacts: `artifacts/{chapter.artifact_key}`."
            )
            write_nb(ROOT / chapter.chapter_path / "00-index.ipynb", index_notebook(f"{chapter.number}. {chapter.title}", body))


def write_notebooks() -> None:
    for chapter in CHAPTERS:
        write_nb(ROOT / chapter.notebook_path, notebook_for_chapter(chapter))


def write_artifacts() -> None:
    for chapter in CHAPTERS:
        ensure_chapter_artifacts(chapter, ROOT)

    manifest = []
    for path in sorted((ROOT / "artifacts").rglob("*")):
        if path.is_file():
            manifest.append(artifact_manifest_entry(path, ROOT))
    (ROOT / "indexes" / "artifact-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    indexes_only = "--indexes-only" in sys.argv
    artifacts_only = "--artifacts-only" in sys.argv
    if not artifacts_only:
        write_source_maps()
        write_indexes()
    if not indexes_only:
        write_notebooks()
        write_artifacts()


if __name__ == "__main__":
    main()
