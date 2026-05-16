from pathlib import Path
import json
from IPython.display import HTML, Image, display
def save_json(data,path): path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(data,indent=2),encoding="utf-8"); return path
def display_artifact(path,width=760): path=Path(path); display(Image(filename=str(path),width=width) if path.suffix==".png" else HTML(path.read_text(encoding="utf-8")))
