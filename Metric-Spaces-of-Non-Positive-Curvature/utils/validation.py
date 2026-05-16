from pathlib import Path
from .source_map import BOOK_ROOT, UNITS, canonical_notebook_path
def discover_canonical_notebooks(root: Path = BOOK_ROOT):
    return [canonical_notebook_path(unit) for unit in UNITS if canonical_notebook_path(unit).exists()]
