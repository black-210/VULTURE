"""Compatibility exports for the historical Chemical-RF module.

The repository contains the original ``src/vulture/chemical_rf.py`` module and
this newer ``chemical_rf`` package.  Python resolves the package first, so the
legacy implementation is loaded explicitly and kept available without
copying or deleting its public API.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_legacy_path = Path(__file__).resolve().parents[1] / "chemical_rf.py"
_spec = importlib.util.spec_from_file_location("vulture._chemical_rf_legacy", _legacy_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"cannot load legacy Chemical-RF module: {_legacy_path}")
_legacy = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_legacy)

ChemicalBond = _legacy.ChemicalBond
ChemicalEquationSolver = _legacy.ChemicalEquationSolver
MolecularRFAnalyzer = _legacy.MolecularRFAnalyzer
NMRPeak = _legacy.NMRPeak

from .calibration import ImpedanceCalibrator, LinearCalibration, combine_uncertainty
from .models import CalibrationPoint, ExperimentRecord, Measurement
from .materials import (
    complex_permittivity, dielectric_resonance_frequency,
    maxwell_garnett_permittivity, reflection_coefficient,
)
from .pipeline import ChemicalRFAnalysisPipeline, ChemicalRFReport
from .spectroscopy import larmor_frequency_hz, simulate_fid, spectrum_from_fid

__all__ = [
    "ChemicalBond", "ChemicalEquationSolver", "MolecularRFAnalyzer", "NMRPeak",
    "CalibrationPoint", "ExperimentRecord", "Measurement", "ImpedanceCalibrator",
    "LinearCalibration", "combine_uncertainty", "complex_permittivity",
    "dielectric_resonance_frequency", "maxwell_garnett_permittivity",
    "reflection_coefficient", "ChemicalRFAnalysisPipeline", "ChemicalRFReport",
    "larmor_frequency_hz", "simulate_fid", "spectrum_from_fid",
]
