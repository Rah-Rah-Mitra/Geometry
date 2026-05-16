"""Build book and chapter index notebooks for A Course in Metric Geometry."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import nbformat as nbf

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.source import BIBLIOGRAPHY, COURSE_MAP, INDEX, source_map_payload  # noqa: E402


def write_notebook(path: Path, markdown: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = nbf.v4.new_notebook()
    nb["cells"] = [nbf.v4.new_markdown_cell(markdown.strip() + "\n")]
    nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}
    nbf.write(nb, path)


def section_list(item: dict) -> str:
    return "\n".join(
        f"- {section['number']} {section['title']} starts on printed page {section['printed_start']} "
        f"(PDF page {section['pdf_start']})."
        for section in item["sections"]
    )


def book_index() -> str:
    rows = [
        "| Chapter | Notebook | Printed Pages | PDF Pages | Focus |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for item in COURSE_MAP:
        rows.append(
            f"| {item['number']} | [{item['title']}]({item['folder']}/{item['notebook']}) | "
            f"{item['printed']} | {item['pdf']} | {item['focus']} |"
        )
    return f"""# A Course in Metric Geometry

This is a standalone visualization-first notebook course for Dmitri Burago, Yuri Burago, and Sergei Ivanov's *A Course in Metric Geometry*. The PDF is used only for source orientation: title, author list, chapter order, page spans, terminology, and concept coverage. The notebooks use original prose, original computational examples, and generated visual artifacts.

Body printed pages map to physical PDF pages by `pdf_page = printed_page + 15`.

## Chapter Route

{chr(10).join(rows)}

## Back Matter

- Bibliography: printed pages {BIBLIOGRAPHY['printed']}; PDF pages {BIBLIOGRAPHY['pdf']}.
- Index: printed pages {INDEX['printed']}; PDF pages {INDEX['pdf']}.

## Course Contract

- One canonical notebook per chapter folder plus a local `00-index.ipynb`.
- Artifacts are saved under `artifacts/chapter-XX/`.
- Each chapter includes a storyboard, visual artifacts, computational checks, an applied lab, and takeaways.
- No textbook screenshots, crops, long exercise text, or copied prose are included.
"""


def chapter_index(item: dict) -> str:
    return f"""# Chapter {item['number']}: {item['title']}

- Source orientation: printed pages {item['printed']}; PDF pages {item['pdf']}.
- Focus: {item['focus']}
- Canonical notebook: [{item['notebook']}]({item['notebook']})
- Artifact root: `../artifacts/chapter-{item['number']:02d}/`

## Section Starts

{section_list(item)}

This chapter notebook is written to stand alone from the PDF. Use the source only to confirm orientation and terminology, not as a reading dependency.
"""


def main() -> None:
    write_notebook(BOOK_ROOT / "00-book-index.ipynb", book_index())
    (BOOK_ROOT / "source_map.json").write_text(
        json.dumps(source_map_payload(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    for item in COURSE_MAP:
        write_notebook(BOOK_ROOT / item["folder"] / "00-index.ipynb", chapter_index(item))
    print(f"Built ACMG indexes for {len(COURSE_MAP)} chapters")


if __name__ == "__main__":
    main()

