from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from utils.course import CHAPTERS
GENERIC_ARTIFACT_NAMES = {
    "concept_configuration.svg",
    "parameter_experiment.svg",
}
def main() -> int:
    failures=[]; total=0
    for ch in CHAPTERS:
        base=ROOT/"artifacts"/f"chapter-{ch['no']:02d}"; fig_dir=base/"figures"; html_dir=base/"html"; check=base/"checks"/"visual_summary.json"
        visuals=[]
        if fig_dir.exists():
            visuals.extend(sorted(fig_dir.glob("*.svg")))
            visuals.extend(sorted(fig_dir.glob("*.png")))
            visuals.extend(sorted(fig_dir.glob("*.jpg")))
            visuals.extend(sorted(fig_dir.glob("*.jpeg")))
        if html_dir.exists(): visuals.extend(sorted(html_dir.glob("*.html")))
        if len(visuals)<4: failures.append(f"chapter {ch['no']:02d}: expected at least 4 visual artifacts, found {len(visuals)}")
        stale=[item for item in visuals if item.name in GENERIC_ARTIFACT_NAMES]
        if stale: failures.append(f"chapter {ch['no']:02d}: still has generic scaffold artifacts: {', '.join(p.name for p in stale)}")
        for fig in visuals:
            total+=1
            if fig.stat().st_size<500: failures.append(f"{fig}: invalid or too small")
            if fig.suffix.lower()==".svg" and "<svg" not in fig.read_text(encoding="utf-8"):
                failures.append(f"{fig}: invalid SVG")
            if fig.suffix.lower()==".png":
                if fig.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n": failures.append(f"{fig}: invalid PNG signature")
            if fig.suffix.lower()==".html":
                head=fig.read_text(encoding="utf-8", errors="ignore")[:500].lower()
                if "<html" not in head and "<div" not in head: failures.append(f"{fig}: invalid HTML")
        if not check.exists(): failures.append(f"chapter {ch['no']:02d}: missing visual_summary.json")
        else:
            payload=json.loads(check.read_text(encoding="utf-8"))
            if payload.get("chapter")!=ch["no"]: failures.append(f"{check}: chapter mismatch")
    print(f"visual audit inspected {total} visual artifacts")
    if failures:
        print("\nFAILURES:"); [print("-",f) for f in failures]; return 1
    print("visual audit passed"); return 0
if __name__=="__main__": raise SystemExit(main())
