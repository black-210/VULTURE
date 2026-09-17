"""Public Chemical-RF integration package.

The package contains models, calibration, spectroscopy, material screening,
stoichiometry, and auditable reporting. Patent-style concepts are documented
as invention disclosures only; no patent grant or novelty claim is implied.
"""
from .chemical_rf import ChemicalBond, ChemicalEquationSolver, MolecularRFAnalyzer, NMRPeak
from .calibration import ImpedanceCalibrator, LinearCalibration, combine_uncertainty
from .models import CalibrationPoint, ExperimentRecord, Measurement
from .materials import complex_permittivity, dielectric_resonance_frequency, maxwell_garnett_permittivity, reflection_coefficient
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
