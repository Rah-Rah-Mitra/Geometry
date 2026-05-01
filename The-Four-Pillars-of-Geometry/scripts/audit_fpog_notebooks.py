from __future__ import annotations

import argparse
import re
from pathlib import Path

import nbformat

import fpog_inventory as inv

BOOK_ROOT = Path(__file__).resolve().parents[1]
IGNORED = {"00-book-index.ipynb", "00-part-index.ipynb", "00-index.ipynb"}


def stats(path: Path) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    markdown = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "markdown")
    code = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "code")
    return {
        "words": len(re.findall(r"[A-Za-z][A-Za-z0-9'-]*", markdown)),
        "code_cells": sum(cell.cell_type == "code" for cell in nb.cells),
        "display": code.count("display_artifact("),
        "render": "render_chapter_visuals(" in code,
        "setup": "BOOK_ROOT" in code and "ARTIFACT_ROOT" in code,
        "takeaways": "Takeaways" in markdown,
        "crop": "crop" in code.lower() or "screenshot" in code.lower(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()
    failures: list[str] = []
    for chapter in inv.CHAPTERS:
        folder = BOOK_ROOT / chapter["folder"]
        notebooks = [path for path in folder.glob("*.ipynb") if path.name not in IGNORED]
        if len(notebooks) != 1:
            failures.append(f"{folder.relative_to(BOOK_ROOT)} has {len(notebooks)} canonical notebooks")
        path = folder / chapter["notebook"]
        if not path.exists():
            failures.append(f"missing {path.relative_to(BOOK_ROOT)}")
            continue
        item = stats(path)
        if item["words"] < args.min_words:
            failures.append(f"{path.relative_to(BOOK_ROOT)} has only {item['words']} words")
        if item["code_cells"] < args.min_code_cells:
            failures.append(f"{path.relative_to(BOOK_ROOT)} has only {item['code_cells']} code cells")
        if item["display"] < 4:
            failures.append(f"{path.relative_to(BOOK_ROOT)} displays too few artifacts")
        for key in ["render", "setup", "takeaways"]:
            if not item[key]:
                failures.append(f"{path.relative_to(BOOK_ROOT)} missing {key}")
        if item["crop"]:
            failures.append(f"{path.relative_to(BOOK_ROOT)} appears to reference crops/screenshots")
    print(f"Audited {len(inv.CHAPTERS)} canonical notebooks.")
    if failures:
        for failure in failures:
            print("FAIL:", failure)
        raise SystemExit(1)
    print("All canonical notebooks meet the configured structure and depth thresholds.")


if __name__ == "__main__":
    main()
