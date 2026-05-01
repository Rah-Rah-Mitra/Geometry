from __future__ import annotations
import argparse
import asyncio
import sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
import fpog_inventory as inv
BOOK_ROOT=Path(__file__).resolve().parents[1]
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--all',action='store_true'); ap.add_argument('--limit',type=int); ap.add_argument('--timeout',type=int,default=300); a=ap.parse_args(); ps=[BOOK_ROOT/c['folder']/c['notebook'] for c in inv.CHAPTERS]; ps=ps if a.all else ps[:a.limit or len(ps)]
    for i,p in enumerate(ps,1):
        print(f"[{i}/{len(ps)}] {p.relative_to(BOOK_ROOT)}"); nb=nbformat.read(p,as_version=4); NotebookClient(nb,timeout=a.timeout,kernel_name='python3',resources={'metadata':{'path':str(p.parent)}}).execute()
    print(f"Executed {len(ps)} notebooks successfully.")
if __name__=='__main__': main()
