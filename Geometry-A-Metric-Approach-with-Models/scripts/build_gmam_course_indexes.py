"""Build GMAM book and chapter index notebooks."""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat as nbf

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import COURSE_MAP  # noqa: E402


def write_notebook(path: Path, markdown: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = nbf.v4.new_notebook()
    nb["cells"] = [nbf.v4.new_markdown_cell(markdown.strip() + "\n")]
    nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}
    nbf.write(nb, path)


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
    return f"""# Geometry: A Metric Approach with Models

This is a standalone visualization-first notebook course. The scanned PDF is used only for source orientation: title, chapter order, page spans, definitions, and exercises. The notebooks use original prose, original computational examples, and generated visual artifacts.

Body printed pages map to physical PDF pages by `pdf_page = printed_page + 15`.

The frontmatter note on computers and hyperbolic geometry is treated as motivation for the course design: the notebooks make the model calculations and graphical experiments executable with the modern shared geometry stack.

## Chapter Route

{chr(10).join(rows)}

## Course Contract

- One canonical notebook per chapter folder plus a local `00-index.ipynb`.
- Artifacts are saved under `artifacts/chapter-XX/`.
- Each chapter includes a storyboard, visual artifacts, computational checks, an applied lab, and takeaways.
- No textbook screenshots, crops, long exercise text, or copied prose are included.
"""


def chapter_index(item: dict) -> str:
    return f"""# Chapter {item['number']}: {item['title']}

- Source orientation: printed pages {item['printed']}; PDF pages {item['pdf']}; sections {item['sections']}.
- Focus: {item['focus']}
- Canonical notebook: [{item['notebook']}]({item['notebook']})
- Artifact root: `../artifacts/chapter-{item['number']:02d}/`

This chapter notebook is written to stand alone from the scanned textbook. Use the PDF only to confirm source orientation, not as a reading dependency.
"""


def main() -> None:
    write_notebook(BOOK_ROOT / "00-book-index.ipynb", book_index())
    for item in COURSE_MAP:
        write_notebook(BOOK_ROOT / item["folder"] / "00-index.ipynb", chapter_index(item))
    print(f"Built GMAM indexes for {len(COURSE_MAP)} chapters")


if __name__ == "__main__":
    main()
