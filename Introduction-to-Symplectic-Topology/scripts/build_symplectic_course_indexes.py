"""Build book, part, chapter, and appendix index notebooks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import nbformat as nbf

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.course_data import BOOK_TITLE, COURSE_UNITS, PARTS, units_by_part


def write_notebook(path: Path, cells: list[nbf.NotebookNode]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    notebook = nbf.v4.new_notebook(cells=cells, metadata={"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}})
    nbf.write(notebook, path)


def link(path: str, text: str) -> str:
    return f"[{text}]({path})"


def build_book_index() -> None:
    rows = [
        f"| {unit.label} | {unit.part_title} | {unit.printed_span} | {unit.pdf_span} | {link(unit.notebook_relpath, unit.filename)} | {unit.visual_concept} |"
        for unit in COURSE_UNITS
    ]
    markdown = "\n".join(
        [
            f"# {BOOK_TITLE}",
            "",
            "A standalone visualization-first course built from the local McDuff-Salamon PDF. The source is used for structure and topic coverage only; all prose, code, and generated artifacts are original.",
            "",
            "## Course Index",
            "",
            "| Unit | Part | Printed pages | PDF pages | Notebook | Visual/check spine |",
            "| --- | --- | ---: | ---: | --- | --- |",
            *rows,
            "",
            "## Local Course Tools",
            "",
            "- `inventory/source-map.md` records page spans and source-use policy.",
            "- `utils/` contains reusable symplectic computations and artifact helpers.",
            "- `scripts/` contains inventory, artifact generation, audits, tests, and notebook validation.",
        ]
    )
    code = "\n".join(
        [
            "from pathlib import Path",
            "BOOK_ROOT = Path.cwd()",
            "notebooks = [p for p in BOOK_ROOT.rglob('*.ipynb') if 'artifacts' not in p.parts]",
            "artifacts = [p for p in (BOOK_ROOT / 'artifacts').rglob('*') if p.is_file()] if (BOOK_ROOT / 'artifacts').exists() else []",
            "print({'notebook_count': len(notebooks), 'artifact_count': len(artifacts)})",
        ]
    )
    write_notebook(BOOK_ROOT / "00-book-index.ipynb", [nbf.v4.new_markdown_cell(markdown), nbf.v4.new_code_cell(code)])


def build_part_index(part: dict[str, str]) -> None:
    units = units_by_part(part["slug"])
    title = "Appendix Index" if part["slug"].startswith("appendix") else "Part Index"
    rows = [
        f"| {unit.label} | {unit.printed_span} | {unit.pdf_span} | {link(f'{unit.slug}/{unit.filename}', unit.filename)} | {unit.goal} |"
        for unit in units
    ]
    markdown = "\n".join(
        [
            f"# {part['title']}: {title}",
            "",
            f"This index collects canonical notebooks for `{part['slug']}`.",
            "",
            "| Unit | Printed pages | PDF pages | Notebook | Standalone goal |",
            "| --- | ---: | ---: | --- | --- |",
            *rows,
        ]
    )
    filename = "00-appendix-index.ipynb" if part["slug"].startswith("appendix") else "00-part-index.ipynb"
    write_notebook(BOOK_ROOT / part["slug"] / filename, [nbf.v4.new_markdown_cell(markdown)])


def build_unit_index(unit) -> None:
    markdown = "\n".join(
        [
            f"# {unit.label}: {unit.focus.split('.')[0]}",
            "",
            f"- Canonical notebook: `{unit.filename}`",
            f"- Source span: printed pages {unit.printed_span}; PDF pages {unit.pdf_span}.",
            f"- Sections: {', '.join(unit.sections)}.",
            f"- Visual/check: {unit.visual_concept}.",
            "",
            link(unit.filename, "Open the canonical teaching notebook"),
        ]
    )
    write_notebook(BOOK_ROOT / unit.part_slug / unit.slug / "00-index.ipynb", [nbf.v4.new_markdown_cell(markdown)])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    build_book_index()
    for part in PARTS:
        build_part_index(part)
    for unit in COURSE_UNITS:
        build_unit_index(unit)
    print(f"wrote indexes for {len(PARTS)} parts and {len(COURSE_UNITS)} units")


if __name__ == "__main__":
    main()
