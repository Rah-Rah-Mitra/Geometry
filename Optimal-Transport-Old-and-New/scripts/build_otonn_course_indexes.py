"""Rebuild book, part, and unit index notebooks for the course."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

import otonn_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


def book_index() -> str:
    lines = [
        "# Optimal Transport: Old and New",
        "",
        "Standalone visualization-first notebook course with original prose, generated diagrams, executable transport examples, and validation checks. The local PDF is used only as a source map.",
        "",
        "- [Source map](source-map.md)",
        "- [Agent instructions](AGENTS.md)",
        "",
        "## Course Map",
        "",
    ]
    for part in inventory.PARTS:
        lines.extend([f"## {part['title']}", "", part["description"], "", f"- [Open part index]({part['folder']}/00-part-index.ipynb)"])
        for unit in inventory.UNITS:
            if unit["part"] != part["folder"]:
                continue
            unit_index = f"{unit['part']}/{unit['folder']}/00-index.ipynb"
            canonical = f"{unit['part']}/{unit['folder']}/{unit['notebook']}"
            lines.append(
                f"- [{unit['label']}: {unit['title']}]({unit_index}) - "
                f"[canonical]({canonical}); printed pp. {unit['printed']}; PDF pp. {unit['pdf']}; {unit['focus']}"
            )
        lines.append("")
    return "\n".join(lines)


def part_index(part: dict[str, str]) -> str:
    lines = [f"# {part['title']}", "", "[Back to Book Index](../00-book-index.ipynb)", "", part["description"], ""]
    for unit in inventory.UNITS:
        if unit["part"] != part["folder"]:
            continue
        lines.extend(
            [
                f"## {unit['label']}: {unit['title']}",
                "",
                f"- Unit index: [{unit['folder']}/00-index.ipynb]({unit['folder']}/00-index.ipynb)",
                f"- Canonical notebook: [{unit['notebook']}]({unit['folder']}/{unit['notebook']})",
                f"- Source span: printed pp. {unit['printed']}; PDF pp. {unit['pdf']}",
                f"- Focus: {unit['focus']}",
                "",
            ]
        )
    return "\n".join(lines)


def unit_index(unit: dict[str, object]) -> str:
    lines = [
        f"# {unit['label']}: {unit['title']}",
        "",
        f"Source orientation: printed pages {unit['printed']}; PDF pages {unit['pdf']}.",
        "",
        f"Canonical notebook: [{unit['notebook']}]({unit['notebook']})",
        "",
        "## Focus",
        "",
        str(unit["focus"]),
        "",
        "## Concepts Rebuilt in Original Prose",
        "",
    ]
    lines.extend(f"- {concept}" for concept in unit["concepts"])
    lines.extend(["", "## Visual Storyboard", "", f"- {unit['visual']}", "", "## Computational Check", "", f"- {unit['check']}", "", "## Lab Prompt", "", f"- {unit['lab']}"])
    return "\n".join(lines)


def main() -> None:
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", book_index())
    for part in inventory.PARTS:
        write_markdown_notebook(inventory.part_index_path(part), part_index(part))
    for unit in inventory.UNITS:
        write_markdown_notebook(inventory.unit_index_path(unit), unit_index(unit))
    print(f"Updated indexes for {len(inventory.UNITS)} units in {len(inventory.PARTS)} parts.")


if __name__ == "__main__":
    main()
