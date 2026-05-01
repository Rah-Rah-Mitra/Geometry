from __future__ import annotations
import argparse, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PDF=ROOT/"Introduction to Geometry.pdf"
def main() -> int:
    p=argparse.ArgumentParser(description="Render scanned source pages to a temporary folder for private orientation only."); p.add_argument("--first",type=int,required=True); p.add_argument("--last",type=int,required=True); p.add_argument("--dpi",type=int,default=120); args=p.parse_args(); out=Path(tempfile.mkdtemp(prefix="itg-source-pages-")); subprocess.run(["pdftoppm","-png","-r",str(args.dpi),"-f",str(args.first),"-l",str(args.last),str(PDF),str(out/"page")],check=True); print(out); print("Temporary source renders only. Do not commit these page images or use them as notebook figures."); return 0
if __name__=="__main__": raise SystemExit(main())
