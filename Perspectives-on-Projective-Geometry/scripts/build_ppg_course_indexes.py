from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

import ppg_inventory as inv

BOOK_ROOT = Path(__file__).resolve().parents[1]


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


def main() -> None:
    lines = [
        "# Perspectives on Projective Geometry",
        "",
        "Standalone visualization-first notebook course. The local PDF is source orientation only.",
        "",
        "## Course Map",
        "",
        "- [Chapter 1: Pappos's Theorem](chapter-01-pappos-theorem-nine-proofs-and-three-variations/00-index.ipynb)",
        "",
    ]
    for part in inv.PARTS:
        lines += [
            f"### Part {part['number']}: {part['title']}",
            "",
            f"[Part index]({part['id']}/00-part-index.ipynb). {part['focus']}",
            "",
        ]
        for chapter in inv.chapters_for_part(part["id"]):
            lines.append(
                f"- **Chapter {chapter['number']}: {chapter['title']}** - "
                f"[index]({chapter['folder']}/00-index.ipynb); "
                f"[canonical]({chapter['folder']}/{chapter['notebook']}); "
                f"sections {chapter['sections']}; printed pp. {chapter['printed_span']}; "
                f"PDF pp. {chapter['pdf_span']}; {chapter['focus']}"
            )
        lines.append("")
    lines += [
        "## Source Notes",
        "",
        "Main printed pages map to physical PDF pages by `pdf_page = printed_page + 22`.",
        "References and the printed index are linked as source orientation, not converted into notebooks.",
    ]
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", "\n".join(lines))

    for part in inv.PARTS:
        chapter_lines = [
            f"- Chapter {chapter['number']}: "
            f"[{chapter['title']}]({chapter['folder'].split('/', 1)[1]}/00-index.ipynb) - "
            f"{chapter['focus']}"
            for chapter in inv.chapters_for_part(part["id"])
        ]
        text = "\n".join(
            [
                f"# Part {part['number']}: {part['title']}",
                "",
                str(part["focus"]),
                "",
                "## Chapters",
                "",
                *chapter_lines,
                "",
                "Back to [book index](../00-book-index.ipynb).",
            ]
        )
        write_markdown_notebook(BOOK_ROOT / str(part["id"]) / "00-part-index.ipynb", text)

    for chapter in inv.CHAPTERS:
        visuals = "\n".join(f"- {item}" for item in chapter["visuals"])
        up = "../00-book-index.ipynb" if chapter["part"] is None else "../../00-book-index.ipynb"
        text = "\n".join(
            [
                f"# Chapter {chapter['number']}: {chapter['title']}",
                "",
                f"- Source span: printed pages {chapter['printed_span']}; PDF pages {chapter['pdf_span']}; sections {chapter['sections']}.",
                f"- Focus: {chapter['focus']}",
                f"- Chapter question: {chapter['question']}",
                f"- Canonical notebook: [{chapter['notebook']}]({chapter['notebook']})",
                "",
                "## Visual Spine",
                "",
                visuals,
                "",
                f"Back to [book index]({up}).",
            ]
        )
        write_markdown_notebook(BOOK_ROOT / str(chapter["folder"]) / "00-index.ipynb", text)
    print(f"Updated {1 + len(inv.PARTS) + len(inv.CHAPTERS)} index notebooks.")


if __name__ == "__main__":
    main()

