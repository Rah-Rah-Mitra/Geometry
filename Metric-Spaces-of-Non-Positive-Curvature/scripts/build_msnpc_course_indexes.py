from __future__ import annotations
import json, sys
from pathlib import Path
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BOOK_ROOT))
from utils.source_map import UNITS, canonical_notebook_path, index_notebook_path
def md(text): return {"cell_type":"markdown","metadata":{},"source":text.splitlines(True)}
def code(text): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":text.splitlines(True)}
def write_nb(path,cells):
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps({"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python","pygments_lexer":"ipython3"}},"nbformat":4,"nbformat_minor":5}, indent=1), encoding="utf-8")
def main():
    lines=["# Metric Spaces of Non-Positive Curvature","","A standalone visualization-first notebook course from the local Bridson-Haefliger PDF. All prose, figures, code, and checks are original.","","- [Source map](inventory/source-map.md)","- [Course inventory](inventory/course-inventory.md)","- [Visualization storyboard](inventory/visual-storyboard.md)",""]
    for part in dict.fromkeys([u["part"]+" - "+u["part_title"] for u in UNITS]):
        lines += [f"## {part}",""]
        for u in [x for x in UNITS if x["part"]+" - "+x["part_title"]==part]:
            lines.append(f'- [{u["number"]} {u["title"]}]({canonical_notebook_path(u).relative_to(BOOK_ROOT).as_posix()})')
        lines.append("")
    write_nb(BOOK_ROOT/"00-book-index.ipynb",[md("\n".join(lines)),code("from pathlib import Path\nassert Path('AGENTS.md').exists()\n")])
    for u in UNITS:
        text=f'# {u["number"]} {u["title"]}\n\n- Canonical notebook: [{u["notebook"]}]({u["notebook"]})\n- Source span: printed {u["printed_pages"][0]}-{u["printed_pages"][1]}, PDF {u["pdf_pages"][0]}-{u["pdf_pages"][1]}\n- Focus: {u["focus"]}\n\n## Concept Route\n\n{", ".join(u["concepts"])}\n'
        write_nb(index_notebook_path(u),[md(text),code(f"from pathlib import Path\nassert Path('{u['notebook']}').exists()\n")])
    print(f"Wrote book index and {len(UNITS)} unit indexes")
if __name__=="__main__": main()
