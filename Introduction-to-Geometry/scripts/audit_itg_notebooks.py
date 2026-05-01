from __future__ import annotations
import argparse, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from utils.course import CHAPTERS, canonical_notebook_name
from utils.validation import notebook_stats
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--min-words",type=int,default=1200); p.add_argument("--min-code-cells",type=int,default=5); args=p.parse_args(); failures=[]
    for ch in CHAPTERS:
        path=ROOT/ch["folder"]/canonical_notebook_name(ch)
        if not path.exists(): failures.append(f"missing notebook: {path}"); continue
        stats=notebook_stats(path); print(f"chapter {ch['no']:02d}: words={stats['words']} code_cells={stats['code_cells']} cells={stats['cells']}")
        if stats["words"]<args.min_words: failures.append(f"{path}: {stats['words']} words < {args.min_words}")
        if stats["code_cells"]<args.min_code_cells: failures.append(f"{path}: {stats['code_cells']} code cells < {args.min_code_cells}")
    if failures:
        print("\nFAILURES:"); [print("-",f) for f in failures]; return 1
    print("notebook audit passed"); return 0
if __name__=="__main__": raise SystemExit(main())
