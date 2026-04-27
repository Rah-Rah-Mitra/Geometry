"""Rebuild VDGF book and part indexes from the inventory."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

from pathlib import Path

import vdgf_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def slugify(value: str) -> str:
    import re

    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-+", "-", slug)


PART_FOLDER_BY_TITLE = {
    "Front Matter": "part-00-prologue",
    "Act I: The Nature of Space": "part-01-the-nature-of-space",
    "Act II: The Metric": "part-02-the-metric",
    "Act III: Curvature": "part-03-curvature",
    "Act IV: Parallel Transport": "part-04-parallel-transport",
    "Act V: Forms": "part-05-forms",
}


def normalized_parts() -> list[dict[str, object]]:
    if hasattr(inventory, "PARTS"):
        return list(inventory.PARTS)
    seen: list[str] = []
    for item in inventory.INVENTORY:
        part = item["part"]
        if part not in seen:
            seen.append(part)
    return [
        {
            "folder": PART_FOLDER_BY_TITLE[part],
            "title": "Prologue" if part == "Front Matter" else part,
            "description": part,
        }
        for part in seen
    ]


def normalized_entries() -> list[dict[str, object]]:
    if hasattr(inventory, "ENTRIES"):
        return list(inventory.ENTRIES)
    entries = []
    for item in inventory.INVENTORY:
        identifier = item["id"]
        is_prologue = identifier == "prologue"
        number = 0 if is_prologue else int(identifier)
        title = item["title"]
        if is_prologue:
            folder = "prologue"
            notebook = "prologue.ipynb"
            label = "Prologue"
        else:
            slug = slugify(title)
            folder = f"chapter-{number:02d}-{slug}"
            notebook = f"{number:02d}-{slug}.ipynb"
            label = f"Chapter {number:02d}"
        entries.append(
            {
                "kind": "prologue" if is_prologue else "chapter",
                "part": PART_FOLDER_BY_TITLE[item["part"]],
                "label": label,
                "number": number,
                "title": title,
                "folder": folder,
                "notebook": notebook,
                "printed": item["printed_span"],
                "pdf": item["pdf_span"],
                "focus": item["focus"],
                "topics": item["topics"],
            }
        )
    return entries


PARTS = normalized_parts()
ENTRIES = normalized_entries()


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip() + "\n")]), path)


def entry_link(entry: dict[str, object]) -> str:
    return f"{entry['part']}/{entry['folder']}/00-index.ipynb"


def canonical_link(entry: dict[str, object]) -> str:
    return f"{entry['part']}/{entry['folder']}/{entry['notebook']}"


def build_book_index() -> str:
    lines = [
        "# Visual Differential Geometry and Forms - Standalone Notebook Edition",
        "",
        "This course is an original executable notebook edition organized around the book's prologue, five acts, and 39 chapters. The notebooks teach the mathematical ideas with fresh prose, derivations, code, generated artifacts, and sanity checks. The source PDF remains local and is not redistributed through notebook outputs.",
        "",
        "Body printed pages map to PDF pages by `pdf_page = printed_page + 29`.",
        "",
    ]
    for part in PARTS:
        lines.extend([f"## {part['title']}", "", str(part["description"]), ""])
        lines.append(f"- [Open part index]({part['folder']}/00-part-index.ipynb)")
        for entry in ENTRIES:
            if entry["part"] == part["folder"]:
                lines.append(
                    f"- [{entry['label']}: {entry['title']}]({entry_link(entry)}) - "
                    f"[canonical]({canonical_link(entry)}); printed pp. {entry['printed']}; PDF pp. {entry['pdf']}; {entry['focus']}"
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
                f"- Source span: printed pp. {entry['printed']}; PDF pp. {entry['pdf']}",
                f"- Focus: {entry['focus']}",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    missing = []
    for entry in ENTRIES:
        folder = BOOK_ROOT / str(entry["part"]) / str(entry["folder"])
        for path in [folder / "00-index.ipynb", folder / str(entry["notebook"])]:
            if not path.exists():
                missing.append(path)
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for part in PARTS:
        write_markdown_notebook(BOOK_ROOT / str(part["folder"]) / "00-part-index.ipynb", build_part_index(part))
    print(f"Updated {1 + len(PARTS)} indexes for {len(ENTRIES)} entries.")


if __name__ == "__main__":
    main()
