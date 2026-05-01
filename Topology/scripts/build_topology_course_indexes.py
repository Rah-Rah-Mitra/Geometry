"""Build Topology book and chapter indexes."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

import topology_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


def build_book_index() -> str:
    lines = [
        "# Topology",
        "",
        "This is a standalone visualization-first notebook course for James Munkres, *Topology*, Second Edition. The notebooks use the local PDF only as source orientation for structure and concepts; the teaching prose, diagrams, computations, and artifacts are original.",
        "",
        "> Source note: the custom PDF is imposed, and its table places Chapter 13 before Chapter 12. The course follows logical section order and documents printed-page spans for orientation.",
        "",
        "## Course Map",
        "",
    ]
    for entry in inventory.ENTRIES:
        label = f"Chapter {entry['number']}"
        lines.append(
            f"- **{label}: {entry['title']}** - [index]({entry['folder']}/00-index.ipynb); "
            f"[canonical]({entry['folder']}/{entry['notebook']}); printed pp. {entry['printed_span']}; "
            f"{entry['sections']}; {entry['focus']}."
        )
    lines.extend(
        [
            "",
            "## Validation",
            "",
            "Run the commands in `AGENTS.md` from the workspace root. Artifacts are generated under `artifacts/` and displayed inline by each canonical notebook.",
        ]
    )
    return "\n".join(lines)


def build_entry_index(entry: dict[str, object]) -> str:
    return "\n".join(
        [
            f"# Chapter {entry['number']}: {entry['title']}",
            "",
            f"- Source span: printed pages {entry['printed_span']}; sections {entry['sections']}.",
            f"- Focus: {entry['focus']}.",
            f"- Canonical notebook: [{entry['notebook']}]({entry['notebook']})",
            "- Back to [book index](../00-book-index.ipynb)",
        ]
    )


def main() -> None:
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for entry in inventory.ENTRIES:
        write_markdown_notebook(BOOK_ROOT / str(entry["folder"]) / "00-index.ipynb", build_entry_index(entry))
    print(f"Updated {1 + len(inventory.ENTRIES)} index notebooks.")


if __name__ == "__main__":
    main()
