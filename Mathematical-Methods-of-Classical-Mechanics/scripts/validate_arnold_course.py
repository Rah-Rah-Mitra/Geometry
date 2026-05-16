import sys,json
from pathlib import Path
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(Path(__file__).resolve().parent)); import arnold_inventory as inv
import argparse,asyncio,nbformat
from nbclient import NotebookClient
if sys.platform.startswith('win'): asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--limit',type=int,default=3); ap.add_argument('--timeout',type=int,default=180); a=ap.parse_args(); paths=[BOOK_ROOT/e['folder']/e['notebook'] for e in inv.ENTRIES][:a.limit]
 for p in paths:
  print(p.relative_to(BOOK_ROOT)); nb=nbformat.read(p,as_version=4); NotebookClient(nb,timeout=a.timeout,kernel_name='python3',resources={'metadata':{'path':str(p.parent)}}).execute(); nbformat.write(nb,p)
 print('executed',len(paths))
if __name__=='__main__': main()
