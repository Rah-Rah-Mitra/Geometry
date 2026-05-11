from __future__ import annotations
import argparse, sys
from pathlib import Path
import nbformat
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from utils.course import CHAPTERS, canonical_notebook_name
from utils.validation import notebook_stats
def notebook_markers(path: Path) -> dict[str, bool | int]:
    nb = nbformat.read(path, as_version=4)
    markdown = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "markdown")
    code = "\n".join(cell.get("source", "") for cell in nb.cells if cell.cell_type == "code")
    return {
        "display": code.count("display_artifact(") + 4 * code.count("display_many("),
        "direct_visual_generation": any(
            marker in code
            for marker in [
                "savefig(",
                ".write_html(",
                "write_html(",
                "write_json(",
                "write_csv(",
                ".write_text(",
                "plt.",
            ]
        ),
        "legacy_scaffold": "render_chapter_visuals(" in code or "from utils.course_visuals import" in code,
        "setup": "BOOK_ROOT" in code and "artifacts" in code,
        "takeaways": "Takeaways" in markdown,
        "sanity": "final_sanity" in code or "final-sanity" in code or "sanity" in code.lower() or "Final sanity" in markdown,
        "crop": "crop" in code.lower() or "screenshot" in code.lower(),
    }
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--min-words",type=int,default=1200); p.add_argument("--min-code-cells",type=int,default=5); args=p.parse_args(); failures=[]
    for ch in CHAPTERS:
        path=ROOT/ch["folder"]/canonical_notebook_name(ch)
        if not path.exists(): failures.append(f"missing notebook: {path}"); continue
        stats=notebook_stats(path); markers=notebook_markers(path); print(f"chapter {ch['no']:02d}: words={stats['words']} code_cells={stats['code_cells']} cells={stats['cells']} displays={markers['display']}")
        if stats["words"]<args.min_words: failures.append(f"{path}: {stats['words']} words < {args.min_words}")
        if stats["code_cells"]<args.min_code_cells: failures.append(f"{path}: {stats['code_cells']} code cells < {args.min_code_cells}")
        if markers["display"] < 1: failures.append(f"{path}: does not display artifacts")
        for key in ["direct_visual_generation", "setup", "takeaways", "sanity"]:
            if not markers[key]: failures.append(f"{path}: missing {key}")
        if markers["legacy_scaffold"]: failures.append(f"{path}: still uses legacy course_visuals scaffold")
        if markers["crop"]: failures.append(f"{path}: appears to reference crops/screenshots")
    if failures:
        print("\nFAILURES:"); [print("-",f) for f in failures]; return 1
    print("notebook audit passed"); return 0
if __name__=="__main__": raise SystemExit(main())
