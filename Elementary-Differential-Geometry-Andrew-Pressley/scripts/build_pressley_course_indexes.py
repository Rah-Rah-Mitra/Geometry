"""Rebuild Pressley book and unit indexes from the inventory."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

import pressley_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook(cells=[new_markdown_cell(text.strip() + "\n")])
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nbformat.write(nb, path)


def canonical_link(entry: dict[str, object]) -> str:
    return f"{entry['folder']}/{entry['notebook']}"


def build_book_index() -> str:
    lines = [
        "# Pressley Elementary Differential Geometry - Standalone Notebook Course",
        "",
        "This is an original executable notebook course based on Andrew Pressley's chapter structure. The notebooks use the local PDF only for source orientation and rebuild the teaching in fresh prose, generated visuals, code experiments, and sanity checks.",
        "",
        f"Source PDF: `{inventory.PDF_SOURCE}`",
        "",
        "## Course Units",
        "",
    ]
    for entry in inventory.ENTRIES:
        lines.append(
            f"- [{entry['label']}: {entry['title']}]({entry['folder']}/00-index.ipynb) - "
            f"[canonical notebook]({canonical_link(entry)}); printed {entry['printed_span']}; PDF {entry['pdf_span']}; sections {entry['sections']}"
        )
    lines.extend(["", "## Back Matter Inventory", ""])
    for item in inventory.BACK_MATTER:
        lines.append(f"- {item['title']}: PDF pages {item['pdf_span']}. {item['policy']}")
    return "\n".join(lines)


def build_unit_index(entry: dict[str, object]) -> str:
    topics = "\n".join(f"- {topic}" for topic in entry["topics"])
    return f"""
# {entry['label']}: {entry['title']}

[Back to book index](../00-book-index.ipynb)

- Canonical notebook: [{entry['notebook']}]({entry['notebook']})
- Source span: printed pages {entry['printed_span']}; PDF pages {entry['pdf_span']}
- Sections: {entry['sections']}
- Artifact topic: `artifacts/{entry['artifact']}/`

## Focus

{entry['focus']}

## Topics

{topics}
""".strip()


def main() -> None:
    inventory.validate_inventory()
    missing = []
    for entry in inventory.ENTRIES:
        folder = BOOK_ROOT / str(entry["folder"])
        notebook = folder / str(entry["notebook"])
        if not notebook.exists():
            missing.append(notebook)
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for entry in inventory.ENTRIES:
        write_markdown_notebook(BOOK_ROOT / str(entry["folder"]) / "00-index.ipynb", build_unit_index(entry))
    print(f"Updated {1 + len(inventory.ENTRIES)} indexes for {len(inventory.ENTRIES)} units.")


if __name__ == "__main__":
    main()
