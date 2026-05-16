"""Smoke-test the optimal-transport stack used by this course."""

from __future__ import annotations

from pathlib import Path
import sys

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))

import numpy as np

from utils.transport import cost_matrix, demo_measures, exact_plan, plan_checks, sinkhorn_demo_value


def main() -> None:
    source, target = demo_measures("smoke")
    cost = cost_matrix(source.points, target.points)
    plan = exact_plan(source.weights, target.weights, cost)
    checks = plan_checks(plan, source, target)
    if not checks["mass_conserved"]:
        raise SystemExit(checks)
    sinkhorn = sinkhorn_demo_value()
    print({"pot_plan_shape": tuple(plan.shape), "cost": checks["wasserstein"], "geomloss": sinkhorn, "numpy": np.__version__})


if __name__ == "__main__":
    main()
