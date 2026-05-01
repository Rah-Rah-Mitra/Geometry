from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

import fpog_inventory as inv

BOOK_ROOT = Path(__file__).resolve().parents[1]


def wr(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


def main() -> None:
    lines = [
        "# The Four Pillars of Geometry",
        "",
        "Standalone visualization-first notebook course. The local PDF is source orientation only.",
        "",
        "## Course Map",
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
                f"printed pp. {chapter['printed_span']}; PDF pp. {chapter['pdf_span']}; "
                f"{chapter['focus']}"
            )
        lines.append("")
    wr(BOOK_ROOT / "00-book-index.ipynb", "\n".join(lines))

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
        wr(BOOK_ROOT / part["id"] / "00-part-index.ipynb", text)

    for chapter in inv.CHAPTERS:
        visuals = "\n".join(f"- {item}" for item in chapter["visuals"])
        text = "\n".join(
            [
                f"# Chapter {chapter['number']}: {chapter['title']}",
                "",
                f"- Source span: printed pages {chapter['printed_span']}; PDF pages {chapter['pdf_span']}; sections {chapter['sections']}.",
                f"- Focus: {chapter['focus']}",
                f"- Chapter question: {chapter['question']}",
                f"- Canonical notebook: [{chapter['notebook']}]({chapter['notebook']})",
                "",
                "## Visual spine",
                "",
                visuals,
                "",
                "Back to [book index](../../00-book-index.ipynb).",
            ]
        )
        wr(BOOK_ROOT / chapter["folder"] / "00-index.ipynb", text)
    print(f"Updated {1 + len(inv.PARTS) + len(inv.CHAPTERS)} index notebooks.")


if __name__ == "__main__":
    main()
