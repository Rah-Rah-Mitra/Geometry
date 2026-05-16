from __future__ import annotations
import json, sys
from pathlib import Path
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BOOK_ROOT))
from utils.source_map import PDF_NAME, PRINTED_TO_PDF_OFFSET, UNITS
def main():
    inv=BOOK_ROOT/"inventory"; inv.mkdir(exist_ok=True)
    rows=["# Source Map","",f"PDF: `{PDF_NAME}`",f"Main-body conversion: `pdf_page = printed_page + {PRINTED_TO_PDF_OFFSET}`.","","| Unit | Folder | Printed Pages | PDF Pages | Focus |","| --- | --- | ---: | ---: | --- |"]
    for u in UNITS: rows.append(f'| {u["number"]} {u["title"]} | `{u["folder"]}` | {u["printed_pages"][0]}-{u["printed_pages"][1]} | {u["pdf_pages"][0]}-{u["pdf_pages"][1]} | {u["focus"]} |')
    (inv/"source-map.md").write_text("\n".join(rows)+"\n", encoding="utf-8")
    ci=["# Course Inventory",""]
    sb=["# Visualization Storyboard",""]
    for u in UNITS:
        ci += [f'## {u["number"]} {u["title"]}',f'- Folder: `{u["folder"]}`',f'- Canonical notebook: `{u["notebook"]}`',f'- Concepts: {", ".join(u["concepts"])}',f'- Library route: {", ".join(u["libraries"])}',""]
        sb += [f'## {u["number"]} {u["title"]}',f'- Chapter goal: {u["focus"]}',f'- Source span read: printed {u["printed_pages"][0]}-{u["printed_pages"][1]} / PDF {u["pdf_pages"][0]}-{u["pdf_pages"][1]}',f'- Visual sequence: `{u["artifact_stem"]}.png`, `{u["artifact_stem"]}-interactive.html`, `concept-routing.csv`.',f'- Proof visualization strategy: {u["proof_strategy"]}',""]
    (inv/"course-inventory.md").write_text("\n".join(ci), encoding="utf-8")
    (inv/"visual-storyboard.md").write_text("\n".join(sb), encoding="utf-8")
    (inv/"source-map.json").write_text(json.dumps({"pdf":PDF_NAME,"printed_to_pdf_offset":PRINTED_TO_PDF_OFFSET,"units":UNITS}, indent=2), encoding="utf-8")
    print(f"Wrote inventory files to {inv}")
if __name__=="__main__": main()
