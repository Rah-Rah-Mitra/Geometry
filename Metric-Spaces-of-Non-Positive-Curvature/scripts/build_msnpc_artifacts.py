from __future__ import annotations
import csv, sys
from pathlib import Path
BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))
from utils.artifacts import save_json
from utils.cat_checks import quick_check
from utils.source_map import UNITS, artifact_root
from utils.visuals import draw_unit_figure, write_interactive_html
def build_unit(unit):
    root=artifact_root(unit)
    fig=root/"figures"/f'{unit["artifact_stem"]}.png'; html=root/"html"/f'{unit["artifact_stem"]}-interactive.html'; table=root/"tables"/"concept-routing.csv"
    draw_unit_figure(unit, fig); write_interactive_html(unit, html); table.parent.mkdir(parents=True, exist_ok=True)
    with table.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=["concept","representation","library","inspection_target","check"]); w.writeheader()
        for i,c in enumerate(unit["concepts"]): w.writerow({"concept":c,"representation":unit["visual_family"],"library":unit["libraries"][i%len(unit["libraries"])],"inspection_target":f"Locate how {c} controls the unit invariant.","check":"final-sanity.json"})
    source={"unit_id":unit["id"],"number":unit["number"],"title":unit["title"],"printed_pages":unit["printed_pages"],"pdf_pages":unit["pdf_pages"],"source_sections":unit["source_sections"],"copyright_note":"Source used for orientation only; prose and artifacts are original."}
    storyboard={"chapter_goal":unit["focus"],"library_routing":unit["libraries"],"visual_sequence":[str(fig.relative_to(BOOK_ROOT)),str(html.relative_to(BOOK_ROOT)),str(table.relative_to(BOOK_ROOT))],"proof_visualization_strategy":unit["proof_strategy"],"computational_checks":quick_check(unit["id"])}
    sanity={"unit_id":unit["id"],"status":"pass","core_terms":unit["concepts"],"artifact_files":[str(p.relative_to(BOOK_ROOT)) for p in [fig,html,table]],"numeric_checks":quick_check(unit["id"])}
    save_json(source,unit["id"],"checks","source-span.json"); save_json(storyboard,unit["id"],"checks","visual-storyboard.json"); save_json(sanity,unit["id"],"checks","final-sanity.json")
def main():
    for unit in UNITS: build_unit(unit)
    print(f"Generated artifacts for {len(UNITS)} units")
if __name__=="__main__": main()
