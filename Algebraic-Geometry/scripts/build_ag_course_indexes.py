"""Rebuild Hartshorne Algebraic Geometry book and chapter index notebooks."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

import ag_inventory as inventory


BOOK_ROOT = Path(__file__).resolve().parents[1]


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


def ensure_inventory() -> None:
    missing = []
    for entry in inventory.ENTRIES:
        folder = BOOK_ROOT / entry["folder"]
        for path in [folder / "00-index.ipynb", folder / entry["notebook"]]:
            if not path.exists():
                missing.append(path)
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))


def build_book_index() -> str:
    lines = [
        f"# {inventory.BOOK_TITLE}",
        "",
        f"Author: {inventory.BOOK_AUTHOR}. Series: {inventory.SERIES}.",
        "",
        "This is a standalone visualization-first notebook course with original prose, generated diagrams, interactive HTML artifacts, exact symbolic checks, and local audit scripts. The local PDF is used only for source orientation and is not reproduced.",
        "",
        "## Course Map",
        "",
    ]
    for entry in inventory.ENTRIES:
        index_link = f"{entry['folder']}/00-index.ipynb"
        canonical_link = f"{entry['folder']}/{entry['notebook']}"
        lines.append(
            f"- [{entry['label']}: {entry['title']}]({index_link}) - "
            f"[canonical]({canonical_link}); printed pp. {entry['printed_span']}; "
            f"PDF pp. {entry['pdf_span']}; {entry['focus']}"
        )
    lines.extend(["", "## Source Map Notes", ""])
    lines.extend(f"- {note}" for note in inventory.SOURCE_SPAN_NOTES)
    lines.extend(["", "## Auxiliary Source Apparatus", ""])
    for entry in inventory.AUXILIARY_SOURCE_MAP:
        lines.append(f"- {entry['label']}: printed {entry['printed_span']}; PDF pp. {entry['pdf_span']}.")
    return "\n".join(lines)


def build_chapter_index(entry: dict) -> str:
    lines = [
        f"# {entry['label']}: {entry['title']}",
        "",
        "[Back to Book Index](../00-book-index.ipynb)",
        "",
        f"Source orientation: printed pages {entry['printed_span']}; PDF pages {entry['pdf_span']}.",
        "",
        f"Canonical notebook: [{entry['notebook']}]({entry['notebook']})",
        "",
        "## Focus",
        "",
        entry["focus"],
        "",
        "## Visual Storyboard",
        "",
    ]
    lines.extend(f"- {visual}" for visual in entry["visuals"])
    lines.extend(["", "## Checks", ""])
    lines.extend(f"- {check}" for check in entry["checks"])
    lines.extend(["", "## Chapter Terms", ""])
    lines.extend(f"- {term}" for term in entry["terms"])
    return "\n".join(lines)


def main() -> None:
    ensure_inventory()
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for entry in inventory.ENTRIES:
        write_markdown_notebook(BOOK_ROOT / entry["folder"] / "00-index.ipynb", build_chapter_index(entry))
    print(f"Updated indexes for {len(inventory.ENTRIES)} Algebraic Geometry entries.")


if __name__ == "__main__":
    main()

