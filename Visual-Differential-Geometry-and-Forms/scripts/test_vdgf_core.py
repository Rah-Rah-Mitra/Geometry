"""Core smoke tests for the VDGF course utilities."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from PIL import Image

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from audit_vdgf_visuals import audit_visuals
from utils.dg import gaussian_curvature_2d, metric_tensor, plane_curve_curvature, sphere_embedding
from utils.forms import CoordinateSystem, basis_form, d, evaluate, hodge_star
from utils.visuals import build_chapter_visual


def test_plane_curve_curvature_unit_circle() -> None:
    theta = np.linspace(0, 2 * np.pi, 64)
    velocity = np.column_stack([-np.sin(theta), np.cos(theta)])
    acceleration = np.column_stack([-np.cos(theta), -np.sin(theta)])
    kappa = plane_curve_curvature(velocity, acceleration)
    assert np.allclose(kappa, 1.0)


def test_sphere_gaussian_curvature() -> None:
    u, v = sp.symbols("u v", positive=True)
    param = sphere_embedding(u, v)
    metric = metric_tensor(param, [u, v])
    K = gaussian_curvature_2d(metric, [u, v])
    assert sp.simplify(K - 1) == 0


def test_forms_exterior_derivative_squared_zero() -> None:
    coords = CoordinateSystem("R3", "x y z")
    x, y, z = coords.symbols
    dx, dy, dz = [basis_form(coords, i) for i in range(3)]
    omega = x * dy + y * dz + z * dx
    assert not bool(d(d(omega)))


def test_form_evaluate_and_hodge() -> None:
    coords = CoordinateSystem("R3", "x y z")
    dx, dy, dz = [basis_form(coords, i) for i in range(3)]
    area = dx.wedge(dy)
    assert evaluate(area, [1, 0, 0], [0, 1, 0]) == 1
    assert hodge_star(dx).components == {(1, 2): 1}


def test_build_chapter_visual_smoke(tmp_path: Path) -> None:
    spec = {
        "chapter": 12,
        "filename": "gauss-map-distortion.png",
        "family": "surface",
        "title": "Gauss Map Distortion",
        "caption": "surface patch and normal drift",
    }
    path, stats = build_chapter_visual(spec, tmp_path, "chapter-12")
    assert path.exists()
    assert path.name == "gauss-map-distortion.png"
    assert stats["width"] >= 300
    assert stats["height"] >= 200
    assert stats["file_size"] > 1000
    assert stats["pixel_std"] > 1.0


def _write_notebook(path: Path, source: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": source,
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(notebook), encoding="utf-8")


def _save_png(path: Path, array: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(array.astype(np.uint8)).save(path)


def test_visual_audit_detects_requested_failure_modes(tmp_path: Path) -> None:
    _write_notebook(
        tmp_path / "part-01" / "chapter-01-example" / "01-example.ipynb",
        'figure_path = save_matplotlib(fig, "chapter-01", "figures", "constant-curvature-circles.png")',
    )

    placeholder = np.zeros((80, 80, 3), dtype=np.uint8)
    placeholder[:, :40] = [255, 0, 0]
    placeholder[:, 40:] = [0, 0, 255]
    _save_png(
        tmp_path / "artifacts" / "chapter-01" / "figures" / "constant-curvature-circles.png",
        placeholder,
    )
    _save_png(
        tmp_path / "artifacts" / "chapter-02" / "figures" / "constant-curvature-circles.png",
        placeholder,
    )
    _save_png(
        tmp_path / "artifacts" / "chapter-02" / "figures" / "chapter-02-blank.png",
        np.full((8, 8, 3), 255, dtype=np.uint8),
    )

    report = audit_visuals(
        tmp_path,
        expected_topics=["chapter-01", "chapter-02"],
        min_width=16,
        min_height=16,
        min_pixels=256,
    )
    checks = {finding["check"] for finding in report["findings"]}

    assert "missing-display-artifact" in checks
    assert "missing-chapter-specific-png" in checks
    assert "duplicate-png-hash" in checks
    assert "repeated-placeholder-png" in checks
    assert "blank-image" in checks
    assert "tiny-image" in checks
