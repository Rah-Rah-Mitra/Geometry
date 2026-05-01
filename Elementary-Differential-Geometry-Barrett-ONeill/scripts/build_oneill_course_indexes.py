
"""Rebuild Barrett O'Neill book, part, and chapter index notebooks."""
from __future__ import annotations
from pathlib import Path
import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook
import oneill_inventory as inventory
BOOK_ROOT=Path(__file__).resolve().parents[1]
def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip()+"\n")]), path)
def entry_folder(entry: dict) -> Path: return BOOK_ROOT/entry["part"]/entry["folder"]
def ensure_inventory() -> None:
    missing=[]
    for entry in inventory.ENTRIES:
        folder=entry_folder(entry)
        for path in [folder/"00-index.ipynb", folder/entry["notebook"]]:
            if not path.exists(): missing.append(path)
    if missing: raise FileNotFoundError("\n".join(str(p) for p in missing))
def build_book_index() -> str:
    lines=["# Elementary Differential Geometry: Barrett O'Neill","","This is a standalone visualization-first notebook course with original prose, executable examples, generated diagrams, interactive artifacts, and sanity checks. The local PDF is used only for source orientation and is not reproduced in the notebooks.","","## Course Map",""]
    for part in inventory.PARTS:
        lines.extend([f"## {part['title']}","",part["description"],"",f"- [Open part index]({part['folder']}/00-part-index.ipynb)"])
        for entry in inventory.ENTRIES:
            if entry["part"]==part["folder"]:
                lines.append(f"- [{entry['label']}: {entry['title']}]({entry['part']}/{entry['folder']}/00-index.ipynb) - [canonical]({entry['part']}/{entry['folder']}/{entry['notebook']}); printed pp. {entry['printed']}; PDF pp. {entry['pdf']}; {entry['focus']}")
        lines.append("")
    return "\n".join(lines)
def build_part_index(part: dict) -> str:
    lines=[f"# {part['title']}","","[Back to Book Index](../00-book-index.ipynb)","",part["description"],""]
    for entry in inventory.ENTRIES:
        if entry["part"]==part["folder"]:
            lines.extend([f"## {entry['label']}: {entry['title']}","",f"- Chapter index: [{entry['folder']}/00-index.ipynb]({entry['folder']}/00-index.ipynb)",f"- Canonical notebook: [{entry['notebook']}]({entry['folder']}/{entry['notebook']})",f"- Source span: printed pp. {entry['printed']}; PDF pp. {entry['pdf']}",f"- Focus: {entry['focus']}",""])
    return "\n".join(lines)
def build_chapter_index(entry: dict) -> str:
    lines=[f"# {entry['label']}: {entry['title']}","",f"Source orientation: printed pages {entry['printed']}; PDF pages {entry['pdf']}.","",f"Canonical notebook: [{entry['notebook']}]({entry['notebook']})","","## Focus","",entry["focus"],"","## Sections",""]
    lines.extend(f"- {s}" for s in entry["sections"]); lines.extend(["","## Visual Storyboard",""]); lines.extend(f"- {v}" for v in entry["visuals"]); lines.extend(["","## Checks",""]); lines.extend(f"- {c}" for c in entry["checks"]); return "\n".join(lines)
def main() -> None:
    ensure_inventory(); write_markdown_notebook(BOOK_ROOT/"00-book-index.ipynb", build_book_index())
    for part in inventory.PARTS: write_markdown_notebook(BOOK_ROOT/part["folder"]/"00-part-index.ipynb", build_part_index(part))
    for entry in inventory.ENTRIES: write_markdown_notebook(entry_folder(entry)/"00-index.ipynb", build_chapter_index(entry))
    print(f"Updated indexes for {len(inventory.ENTRIES)} entries in {len(inventory.PARTS)} parts.")
if __name__=="__main__": main()
