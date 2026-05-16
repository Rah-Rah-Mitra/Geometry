"""Build lightweight index notebooks for the course."""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat as nbf

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))

from utils.course_manifest import CHAPTERS, PARTS


def rel(path: Path, base: Path) -> str:
    return path.relative_to(base).as_posix()


def write_nb(path: Path, cells: list[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = nbf.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"]["course"] = "Nonparametric Inference on Manifolds"
    nbf.write(nb, path)


def markdown_cell(text: str) -> object:
    return nbf.v4.new_markdown_cell(text.strip() + "\n")


def main() -> None:
    rows = []
    for chapter in CHAPTERS:
        rows.append(
            f"| {chapter.number} | [{chapter.title}]({rel(chapter.path, BOOK_ROOT)}) | "
            f"{chapter.printed_pages} | {chapter.pdf_pages} | {chapter.focus} |"
        )
    write_nb(
        BOOK_ROOT / "00-book-index.ipynb",
        [
            markdown_cell(
                """# Nonparametric Inference on Manifolds: visualization-first course

This standalone notebook edition is built from the local PDF as an original computational course. It follows the book's order but teaches through synthetic data, executable geometry, and generated artifacts rather than copied prose or page images.

Use the table below to jump to the canonical chapter or appendix notebook. Printed pages come from the PDF table of contents; physical PDF pages use the observed offset where printed page 1 is PDF page 16.
"""
            ),
            markdown_cell(
                "| Unit | Notebook | Printed pages | PDF pages | Course focus |\n"
                "| --- | --- | --- | --- | --- |\n" + "\n".join(rows)
            ),
            markdown_cell(
                """## Validation entry points

Run these commands from `D:/Geometry`:

```powershell
uv run python "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts/generate_artifacts.py"
uv run python "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts/build_course_indexes.py"
uv run python -m compileall -q "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/utils" "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts"
uv run python "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts/audit_notebooks.py"
uv run python "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts/audit_visuals.py"
uv run python "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts/audit_artifacts.py"
uv run python "Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces/scripts/validate_course.py" --limit 3
```
"""
            ),
        ],
    )

    for part, title in PARTS.items():
        part_root = BOOK_ROOT / part
        part_rows = [
            f"| {chapter.number} | [{chapter.title}]({rel(chapter.path, part_root)}) | {chapter.focus} |"
            for chapter in CHAPTERS
            if chapter.part == part
        ]
        write_nb(
            part_root / "00-part-index.ipynb",
            [
                markdown_cell(f"# {title}"),
                markdown_cell("| Unit | Notebook | Focus |\n| --- | --- | --- |\n" + "\n".join(part_rows)),
            ],
        )

    for chapter in CHAPTERS:
        write_nb(
            chapter.index_path,
            [
                markdown_cell(f"# {chapter.number}. {chapter.title}"),
                markdown_cell(
                    f"Canonical notebook: [{chapter.notebook}]({chapter.notebook})\n\n"
                    f"Source span: printed pp. {chapter.printed_pages}; physical PDF pp. {chapter.pdf_pages}.\n\n"
                    f"Focus: {chapter.focus}"
                ),
                markdown_cell(
                    "Concept route: " + ", ".join(chapter.concepts) + ".\n\n"
                    "Library route: " + ", ".join(chapter.libraries) + ".\n\n"
                    "Core artifacts: " + ", ".join(f"`{name}`" for name in chapter.visuals) + "."
                ),
            ],
        )
    print("Index notebooks rebuilt")


if __name__ == "__main__":
    main()
