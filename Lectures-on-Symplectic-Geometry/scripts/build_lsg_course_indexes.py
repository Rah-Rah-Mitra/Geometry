"""Rebuild book, part, and lecture indexes for the LSG course."""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

SCRIPT_DIR = Path(__file__).resolve().parent
BOOK_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lsg_inventory import ENTRIES, PARTS

KERNEL_METADATA = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "pygments_lexer": "ipython3"},
}


def write_markdown_notebook(path: Path, markdown: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    notebook = new_notebook(cells=[new_markdown_cell(markdown.strip() + "\n")], metadata=KERNEL_METADATA)
    nbformat.write(notebook, path)


def canonical_path(entry: dict[str, object]) -> str:
    return f"{entry['part']}/{entry['folder']}/{entry['notebook']}"


def lecture_index_path(entry: dict[str, object]) -> str:
    return f"{entry['part']}/{entry['folder']}/00-index.ipynb"


def build_book_index() -> str:
    lines = [
        "# Lectures on Symplectic Geometry - Standalone Notebook Edition",
        "",
        "This course is an original executable notebook edition organized around the thirty lecture chapters in Ana Cannas da Silva's local PDF. It uses fresh prose, generated diagrams, computational checks, and book-local artifacts. The source PDF stays local and is not redistributed through screenshots or page crops.",
        "",
        "Source map: Arabic printed body pages map to physical PDF pages by `physical_pdf_page = printed_page + 14`.",
        "",
    ]
    for part in PARTS:
        lines.extend([f"## {part['title']}", "", str(part["description"]), "", f"- [Open part index]({part['folder']}/00-part-index.ipynb)"])
        for entry in ENTRIES:
            if entry["part"] != part["folder"]:
                continue
            lines.append(
                f"- [{entry['label']}: {entry['title']}]({lecture_index_path(entry)}) - "
                f"[canonical notebook]({canonical_path(entry)}); printed pp. {entry['printed_span']}; "
                f"PDF pp. {entry['pdf_span']}; {entry['focus']}"
            )
        lines.append("")
    return "\n".join(lines)


def build_part_index(part: dict[str, object]) -> str:
    lines = [
        f"# {part['title']}",
        "",
        "[Back to Book Index](../00-book-index.ipynb)",
        "",
        str(part["description"]),
        "",
    ]
    for entry in ENTRIES:
        if entry["part"] != part["folder"]:
            continue
        lines.extend(
            [
                f"## {entry['label']}: {entry['title']}",
                "",
                f"- Chapter index: [{entry['folder']}/00-index.ipynb]({entry['folder']}/00-index.ipynb)",
                f"- Canonical notebook: [{entry['notebook']}]({entry['folder']}/{entry['notebook']})",
                f"- Source span: printed pp. {entry['printed_span']}; physical PDF pp. {entry['pdf_span']}",
                f"- Focus: {entry['focus']}",
                f"- Primary visual: {entry['visual']}",
                "",
            ]
        )
    return "\n".join(lines)


def build_lecture_index(entry: dict[str, object]) -> str:
    concepts = "\n".join(f"- {concept}" for concept in entry["concepts"])
    sections = "\n".join(f"- {section}" for section in entry["sections"])
    return f"""
# {entry['label']}: {entry['title']}

[Back to Part Index](../00-part-index.ipynb) | [Back to Book Index](../../00-book-index.ipynb)

- Canonical notebook: [{entry['notebook']}]({entry['notebook']})
- Source span: printed pp. {entry['printed_span']}; physical PDF pp. {entry['pdf_span']}
- Artifact topic: `artifacts/{entry['artifact_topic']}`
- Focus: {entry['focus']}

## Lecture Sections

{sections}

## Computational Concepts

{concepts}

## Visual Route

{entry['visual']}

## Lab Prompt

{entry['lab']}
"""


def main() -> None:
    missing = []
    for entry in ENTRIES:
        canonical = BOOK_ROOT / str(entry["part"]) / str(entry["folder"]) / str(entry["notebook"])
        if not canonical.exists():
            missing.append(canonical)
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for part in PARTS:
        write_markdown_notebook(BOOK_ROOT / str(part["folder"]) / "00-part-index.ipynb", build_part_index(part))
    for entry in ENTRIES:
        write_markdown_notebook(BOOK_ROOT / str(entry["part"]) / str(entry["folder"]) / "00-index.ipynb", build_lecture_index(entry))
    print(f"Updated indexes for {len(PARTS)} parts and {len(ENTRIES)} lectures.")


if __name__ == "__main__":
    main()
