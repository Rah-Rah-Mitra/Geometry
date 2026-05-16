"""Generate course-local symplectic visual artifacts and invariant checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.course_data import COURSE_UNITS, unit_by_slug
from utils.symplectic_visuals import build_unit_artifacts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="generate all unit artifacts")
    parser.add_argument("--unit", action="append", default=[], help="unit slug to generate; may be repeated")
    args = parser.parse_args()

    units = list(COURSE_UNITS) if args.all or not args.unit else [unit_by_slug(slug) for slug in args.unit]
    results = []
    for unit in units:
        result = build_unit_artifacts(unit.slug)
        results.append({"unit": unit.slug, "artifact_count": len(result["artifacts"]), "assertions": result["assertions"]})
        print(f"{unit.slug}: {len(result['artifacts'])} artifacts")
    print(json.dumps({"generated": len(results), "units": results}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
