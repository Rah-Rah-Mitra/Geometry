"""Build book, part, and chapter index notebooks for the robotics course."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

from robotics_inventory import ENTRIES, PARTS

BOOK_ROOT = Path(__file__).resolve().parents[1]


def write_notebook(path: Path, markdown: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(markdown.strip() + "\n")]), path)


def build_book_index() -> str:
    lines = [
        "# A Mathematical Introduction to Robotic Manipulation - Standalone Notebook Course",
        "",
        "This original executable course follows the textbook structure while replacing passive reading with generated diagrams, robotics computations, applied labs, and sanity checks. The source PDF is used only for orientation and page spans; the notebooks do not reproduce textbook prose, photos, screenshots, or long exercise text.",
        "",
        "Printed page mapping: `pdf_page = printed_page + 18`.",
        "",
    ]
    for part in PARTS:
        lines += [f"## {part['title']}", "", part["description"], "", f"- [Open part index]({part['folder']}/00-part-index.ipynb)"]
        for entry in ENTRIES:
            if entry["part"] == part["folder"]:
                chapter = f"{entry['part']}/{entry['folder']}/00-index.ipynb"
                canonical = f"{entry['part']}/{entry['folder']}/{entry['notebook']}"
                lines.append(f"- [{entry['label']}: {entry['title']}]({chapter}) - [canonical]({canonical}); printed pp. {entry['printed']}; PDF pp. {entry['pdf']}; {entry['focus']}")
        lines.append("")
    return "\n".join(lines)


def build_part_index(part: dict[str, str]) -> str:
    lines = [f"# {part['title']}", "", "[Back to Book Index](../00-book-index.ipynb)", "", part["description"], ""]
    for entry in ENTRIES:
        if entry["part"] != part["folder"]:
            continue
        lines += [
            f"## {entry['label']}: {entry['title']}",
            "",
            f"- Chapter index: [{entry['folder']}/00-index.ipynb]({entry['folder']}/00-index.ipynb)",
            f"- Canonical notebook: [{entry['notebook']}]({entry['folder']}/{entry['notebook']})",
            f"- Source span: printed pp. {entry['printed']}; PDF pp. {entry['pdf']}",
            f"- Focus: {entry['focus']}",
            "",
        ]
    return "\n".join(lines)


def build_chapter_index(entry: dict[str, object]) -> str:
    label = str(entry["label"])
    return "\n".join(
        [
            f"# {label}: {entry['title']}",
            "",
            "[Back to Book Index](../../00-book-index.ipynb)",
            "",
            f"- Canonical notebook: [{entry['notebook']}]({entry['notebook']})",
            f"- Source orientation: printed pp. {entry['printed']}; PDF pp. {entry['pdf']}",
            f"- Artifact topic: `artifacts/{entry['artifact']}`",
            f"- Focus: {entry['focus']}",
            "",
            "The notebook is written to stand alone: definitions, computations, generated visuals, labs, checks, and takeaways are inside the canonical notebook.",
        ]
    )


def main() -> None:
    missing = []
    for entry in ENTRIES:
        folder = BOOK_ROOT / str(entry["part"]) / str(entry["folder"])
        if not (folder / str(entry["notebook"])).exists():
            missing.append(folder / str(entry["notebook"]))
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))

    write_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for part in PARTS:
        write_notebook(BOOK_ROOT / str(part["folder"]) / "00-part-index.ipynb", build_part_index(part))
    for entry in ENTRIES:
        write_notebook(BOOK_ROOT / str(entry["part"]) / str(entry["folder"]) / "00-index.ipynb", build_chapter_index(entry))
    print(f"Updated book index, {len(PARTS)} part indexes, and {len(ENTRIES)} chapter indexes.")


if __name__ == "__main__":
    main()
