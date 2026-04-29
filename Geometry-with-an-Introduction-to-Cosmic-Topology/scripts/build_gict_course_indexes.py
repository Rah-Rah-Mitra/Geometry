"""Build GICT book, chapter, and appendix indexes."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

import gict_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


def build_book_index() -> str:
    lines = [
        "# Geometry with an Introduction to Cosmic Topology",
        "",
        "This is a standalone visualization-first notebook course. The notebooks use the local PDF only as source orientation for structure and concepts; the teaching prose, diagrams, computations, and artifacts are original.",
        "",
        "## Course Map",
        "",
    ]
    for entry in inventory.ENTRIES:
        label = "Appendix A" if entry["kind"] == "appendix" else f"Chapter {entry['number']}"
        lines.append(
            f"- **{label}: {entry['title']}** - [index]({entry['folder']}/00-index.ipynb); "
            f"[canonical]({entry['folder']}/{entry['notebook']}); printed pp. {entry['printed_span']}; "
            f"PDF pp. {entry['pdf_span']}; {entry['focus']}"
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
    label = "Appendix A" if entry["kind"] == "appendix" else f"Chapter {entry['number']}"
    return "\n".join(
        [
            f"# {label}: {entry['title']}",
            "",
            f"- Source span: printed pages {entry['printed_span']}; PDF pages {entry['pdf_span']}; sections {entry['sections']}.",
            f"- Focus: {entry['focus']}",
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
