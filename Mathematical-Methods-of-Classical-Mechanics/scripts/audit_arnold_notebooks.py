import sys,json
from pathlib import Path
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(Path(__file__).resolve().parent)); import arnold_inventory as inv
import nbformat
def main():
 f=[]; n=0
 for e in inv.ENTRIES:
  p=BOOK_ROOT/e['folder']/e['notebook']; n+=p.exists();
  if not p.exists(): f.append(str(p)); continue
  nb=nbformat.read(p,as_version=4); md=' '.join(''.join(c.source) for c in nb.cells if c.cell_type=='markdown'); code=' '.join(''.join(c.source) for c in nb.cells if c.cell_type=='code')
  if len(md.split())<500 or 'final_sanity' not in code: f.append(str(p))
 print(json.dumps({'notebook_count':n,'findings':f},indent=2)); raise SystemExit(1 if f else 0)
if __name__=='__main__': main()
