from __future__ import annotations
import json
from pathlib import Path
BOOK_ROOT = Path(__file__).resolve().parents[1]
source = json.loads((BOOK_ROOT / "source_map.json").read_text(encoding="utf-8"))
print(f"{source['title']}: {len(source['units'])} canonical units")
for item in source["units"]:
    print(f"- {item['label']}: {item['title']} [{item.get('printed', '')}] -> {item['folder_path']}/{item['notebook']}")
