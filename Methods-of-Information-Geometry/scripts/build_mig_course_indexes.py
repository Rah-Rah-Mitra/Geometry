"""Build course indexes and source-map files for Methods of Information Geometry."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import nbformat as nbf

import mig_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]


def md_cell(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(text)


def code_cell(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(text)


def write_notebook(path: Path, cells: list[nbf.NotebookNode]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python", "pygments_lexer": "ipython3"}
    nbf.write(nb, path)


def build_book_index() -> None:
    rows = "\n".join(
        f"| {entry['number']:02d} | [{entry['title']}]({inventory.notebook_path(entry)}) | {entry['printed_pages']} | {entry['physical_pages']} | {entry['summary']} |"
        for entry in inventory.ENTRIES
    )
    cells = [
        md_cell(
            "# Methods of Information Geometry\n\n"
            "This is a standalone visualization-first course built from the local DjVu source text layer. "
            "The lessons use original prose, computational experiments, and generated artifacts rather than copied page images or textbook passages.\n\n"
            "| Chapter | Notebook | Printed pages | Physical DjVu pages | Course focus |\n"
            "| --- | --- | --- | --- | --- |\n"
            f"{rows}\n"
        ),
        code_cell(
            "from pathlib import Path\n"
            "BOOK_ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'Methods of Information Geometry.djvu').exists())\n"
            "source_map = BOOK_ROOT / 'source' / 'source-map.json'\n"
            "assert source_map.exists(), source_map\n"
            "print(f'Course root: {BOOK_ROOT}')\n"
            "print(source_map.read_text(encoding='utf-8')[:900])\n"
        ),
        md_cell(
            "## How to read the course\n\n"
            "The first three chapters build the language: manifolds, statistical models, Fisher metric, alpha-connections, divergences, and dual flatness. "
            "Chapters 4 through 8 turn that geometry into inference, system theory, multiterminal information, quantum state geometry, and extensions. "
            "Every canonical notebook ends with executable checks so a reader can separate geometric claims from numerical accidents."
        ),
    ]
    write_notebook(BOOK_ROOT / "00-book-index.ipynb", cells)


def build_chapter_indexes() -> None:
    for entry in inventory.ENTRIES:
        path = BOOK_ROOT / entry["folder"] / "00-index.ipynb"
        terms = ", ".join(entry["terms"])
        cells = [
            md_cell(
                f"# Chapter {entry['number']:02d}: {entry['title']}\n\n"
                f"Canonical notebook: [{entry['notebook']}]({entry['notebook']}).\n\n"
                f"Source span: printed pp. {entry['printed_pages']}; physical DjVu pp. {entry['physical_pages']}.\n\n"
                f"Focus terms: {terms}.\n\n"
                f"{entry['summary']}"
            ),
            code_cell(
                "from pathlib import Path\n"
                "BOOK_ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'Methods of Information Geometry.djvu').exists())\n"
                f"expected = BOOK_ROOT / '{entry['folder']}' / '{entry['notebook']}'\n"
                "assert expected.exists(), expected\n"
                "print(expected.relative_to(BOOK_ROOT))\n"
            ),
        ]
        write_notebook(path, cells)


def build_source_map() -> None:
    source_root = BOOK_ROOT / "source"
    source_root.mkdir(parents=True, exist_ok=True)
    data = {
        "source": "Methods of Information Geometry.djvu",
        "extraction": {
            "method": "vendored read-only Rust extractor using djvu-rs 0.17.0 over DJVM/TXTz text chunks",
            "manifest": "source/djvu_text/djvu_text_manifest.json",
            "bookmark_status": "No NAVM bookmarks were present in the file.",
            "main_matter_page_rule": "physical_page = printed_page + 9",
        },
        "chapters": [
            {
                **entry,
                "notebook_path": inventory.notebook_path(entry),
                "source_files": inventory.physical_page_files(entry["physical_pages"]),
            }
            for entry in inventory.ENTRIES
        ],
        "supplements": [
            {**item, "source_files": inventory.physical_page_files(item["physical_pages"])}
            for item in inventory.SUPPLEMENTS
        ],
    }
    (source_root / "source-map.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    md_lines = [
        "# Source Map",
        "",
        "Extraction method: vendored read-only Rust extractor using `djvu-rs 0.17.0` over bundled `DJVM` pages and BZZ-compressed `TXTz` text chunks.",
        "",
        "| Unit | Notebook/source | Printed pages | Physical pages | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for entry in inventory.ENTRIES:
        md_lines.append(
            f"| Chapter {entry['number']:02d} | `{inventory.notebook_path(entry)}` | {entry['printed_pages']} | {entry['physical_pages']} | {entry['summary']} |"
        )
    for item in inventory.SUPPLEMENTS:
        md_lines.append(f"| {item['title']} | source only | {item['printed_pages']} | {item['physical_pages']} | Supplementary orientation material. |")
    (source_root / "source-map.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    with (source_root / "text_inventory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["unit", "printed_pages", "physical_pages", "notebook_path", "source_files"])
        writer.writeheader()
        for entry in inventory.ENTRIES:
            writer.writerow(
                {
                    "unit": f"Chapter {entry['number']:02d}: {entry['title']}",
                    "printed_pages": entry["printed_pages"],
                    "physical_pages": entry["physical_pages"],
                    "notebook_path": inventory.notebook_path(entry),
                    "source_files": ";".join(inventory.physical_page_files(entry["physical_pages"])),
                }
            )


def build_extraction_note() -> None:
    text = (
        "# DjVu Extraction Method\n\n"
        "No `djvutxt`, `djvused`, `djvudump`, or `ddjvu` executable was available on the worker PATH. "
        "The course therefore vendors `vendor/djvu_text_extractor`, a read-only Rust command that uses `djvu-rs 0.17.0`. "
        "It opens the bundled DjVu document, decodes each page text layer from `TXTz` chunks, and writes UTF-8 page text plus a JSON manifest. "
        "The extractor does not render, crop, screenshot, or modify the source.\n\n"
        "Observed result: 216 physical pages, 216 page text files, no NAVM bookmark entries. "
        "Physical page 10 begins printed page 1 of the main matter, matching the table of contents.\n"
    )
    (BOOK_ROOT / "source" / "extraction-method.md").write_text(text, encoding="utf-8")


def main() -> None:
    build_book_index()
    build_chapter_indexes()
    build_source_map()
    build_extraction_note()
    print("Built Methods of Information Geometry indexes and source map.")


if __name__ == "__main__":
    main()

