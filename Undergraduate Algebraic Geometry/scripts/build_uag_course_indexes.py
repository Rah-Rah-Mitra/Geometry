"""Build book, part, and chapter indexes for the UAG course."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

import uag_inventory as inventory


BOOK_ROOT = Path(__file__).resolve().parents[1]


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


def build_book_index() -> str:
    lines = [
        "# Undergraduate Algebraic Geometry",
        "",
        "This is a standalone visualization-first notebook course based on the local PDF only for source orientation. The teaching prose, diagrams, computations, and artifacts are original.",
        "",
        "## Course Map",
        "",
    ]
    for part in inventory.PARTS:
        entries = inventory.entries_for_part(str(part["folder"]))
        lines.append(f"### {part['label']}: {part['title']}")
        lines.append("")
        lines.append(f"[Part index]({part['folder']}/00-index.ipynb). {part['description']}")
        lines.append("")
        for entry in entries:
            lines.append(
                f"- **Chapter {entry['number']}: {entry['title']}** - "
                f"[index]({entry['folder']}/00-index.ipynb); "
                f"[canonical]({entry['folder']}/{entry['notebook']}); "
                f"printed pp. {entry['printed_span']}; PDF pp. {entry['pdf_span']}; {entry['focus']}"
            )
        lines.append("")
    lines.extend(
        [
            "## Validation",
            "",
            "Run the commands in `AGENTS.md` from the workspace root. Artifacts are generated under `artifacts/` and displayed inline by each canonical notebook.",
        ]
    )
    return "\n".join(lines)


def build_part_index(part: dict[str, object]) -> str:
    entries = inventory.entries_for_part(str(part["folder"]))
    lines = [
        f"# {part['label']}: {part['title']}",
        "",
        str(part["description"]),
        "",
        "## Chapters",
        "",
    ]
    for entry in entries:
        lines.append(
            f"- Chapter {entry['number']}: [{entry['title']}]({Path(str(entry['folder'])).name}/00-index.ipynb) - {entry['focus']}"
        )
    lines.extend(["", "- Back to [book index](../00-book-index.ipynb)"])
    return "\n".join(lines)


def build_entry_index(entry: dict[str, object]) -> str:
    return "\n".join(
        [
            f"# Chapter {entry['number']}: {entry['title']}",
            "",
            f"- Source span: printed pages {entry['printed_span']}; PDF pages {entry['pdf_span']}; sections {entry['sections']}.",
            f"- Focus: {entry['focus']}",
            f"- Canonical notebook: [{entry['notebook']}]({entry['notebook']})",
            f"- Artifact root: `../../artifacts/{entry['artifact']}` from part folders or `../artifacts/{entry['artifact']}` from the prologue path.",
            "- Back to [book index](../../00-book-index.ipynb)",
        ]
    )


def main() -> None:
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for part in inventory.PARTS:
        write_markdown_notebook(BOOK_ROOT / str(part["folder"]) / "00-index.ipynb", build_part_index(part))
    for entry in inventory.ENTRIES:
        write_markdown_notebook(BOOK_ROOT / str(entry["folder"]) / "00-index.ipynb", build_entry_index(entry))
    print(f"Updated {1 + len(inventory.PARTS) + len(inventory.ENTRIES)} index notebooks.")


if __name__ == "__main__":
    main()
