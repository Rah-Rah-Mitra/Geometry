from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from utils.course import CHAPTERS
def main() -> int:
    failures=[]; total=0
    for ch in CHAPTERS:
        base=ROOT/"artifacts"/f"chapter-{ch['no']:02d}"; figures=sorted((base/"figures").glob("*.svg")) if (base/"figures").exists() else []; check=base/"checks"/"visual_summary.json"
        if len(figures)<2: failures.append(f"chapter {ch['no']:02d}: expected at least 2 SVG figures, found {len(figures)}")
        for fig in figures:
            total+=1; text=fig.read_text(encoding="utf-8")
            if fig.stat().st_size<500 or "<svg" not in text: failures.append(f"{fig}: invalid or too small")
        if not check.exists(): failures.append(f"chapter {ch['no']:02d}: missing visual_summary.json")
        else:
            payload=json.loads(check.read_text(encoding="utf-8"))
            if payload.get("chapter")!=ch["no"]: failures.append(f"{check}: chapter mismatch")
    print(f"visual audit inspected {total} SVG figures")
    if failures:
        print("\nFAILURES:"); [print("-",f) for f in failures]; return 1
    print("visual audit passed"); return 0
if __name__=="__main__": raise SystemExit(main())
