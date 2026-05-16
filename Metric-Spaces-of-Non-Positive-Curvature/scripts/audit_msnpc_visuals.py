from __future__ import annotations
import json, sys
from pathlib import Path
from PIL import Image
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BOOK_ROOT))
from utils.source_map import UNITS, artifact_root
def varied(path):
    with Image.open(path) as img: return img.convert("L").getextrema()[0] != img.convert("L").getextrema()[1]
def main():
    failures=[]; names=set()
    for u in UNITS:
        root=artifact_root(u); expected=[root/"figures"/f'{u["artifact_stem"]}.png',root/"html"/f'{u["artifact_stem"]}-interactive.html',root/"tables"/"concept-routing.csv",root/"checks"/"source-span.json",root/"checks"/"visual-storyboard.json",root/"checks"/"final-sanity.json"]
        if expected[0].name in names: failures.append(f'duplicate figure name {expected[0].name}')
        names.add(expected[0].name)
        for path in expected:
            if not path.exists(): failures.append(f'{u["id"]}: missing {path.relative_to(BOOK_ROOT)}')
            elif path.stat().st_size < (1024 if path.suffix==".png" else 40): failures.append(f'{u["id"]}: small {path.relative_to(BOOK_ROOT)}')
        if expected[0].exists() and not varied(expected[0]): failures.append(f'{u["id"]}: blank image')
        if expected[-1].exists() and json.loads(expected[-1].read_text(encoding="utf-8")).get("status")!="pass": failures.append(f'{u["id"]}: sanity not pass')
    if failures:
        print("\n".join("FAIL "+f for f in failures), file=sys.stderr); raise SystemExit(1)
    print(f"Visual audit passed for {len(UNITS)} units")
if __name__=="__main__": main()
