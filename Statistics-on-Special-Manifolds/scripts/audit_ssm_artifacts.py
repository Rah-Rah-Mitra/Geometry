import sys,json
from pathlib import Path
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(Path(__file__).resolve().parent)); import ssm_inventory as inv
def main():
 f=[]
 for e in inv.ENTRIES:
  r=BOOK_ROOT/'artifacts'/e['topic']
  if not list(r.rglob('*.png')) or not list(r.rglob('*.html')) or not list(r.rglob('*.json')): f.append(str(r))
 print(json.dumps({'findings':f},indent=2)); raise SystemExit(1 if f else 0)
if __name__=='__main__': main()
