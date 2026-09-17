"""Tests for the expanded Chemical-RF measurement pipeline."""
import numpy as np
import pytest

from vulture.chemical_rf import (
    CalibrationPoint, ChemicalRFAnalysisPipeline, ImpedanceCalibrator,
    complex_permittivity, dielectric_resonance_frequency, maxwell_garnett_permittivity,
    simulate_fid, spectrum_from_fid,
)


def test_calibration_recovers_complex_affine_correction():
    predicted = [50 + 1j, 25 - 2j, 75 + 3j]
    points = [CalibrationPoint(1e6, 2 * z + (1 - 4j)) for z in predicted]
    fit = ImpedanceCalibrator().fit(predicted, points)
    assert fit.gain == pytest.approx(2 + 0j)
    assert fit.offset == pytest.approx(1 - 4j)
    assert fit.residual_rms_ohm == pytest.approx(0)


def test_material_screening_and_reflection_are_bounded():
    matrix = complex_permittivity(2.5, 0.01, 13.56e6)
    inclusion = complex_permittivity(10, 0.02, 13.56e6)
    effective = maxwell_garnett_permittivity(matrix, inclusion, 0.1)
    assert dielectric_resonance_frequency(abs(effective.real), 0.1) > 0
    assert abs((effective - (50 + 0j)) / (effective + (50 + 0j))) >= 0


def test_fid_and_spectrum_have_matching_shapes():
    result = simulate_fid(duration_s=0.01, sample_rate_hz=1000)
    spectrum = spectrum_from_fid(result["fid"], 1000)
    assert len(result["time_s"]) == len(result["fid"]) == len(spectrum["frequency_hz"])
    assert np.iscomplexobj(result["fid"])


def test_pipeline_marks_uncalibrated_results_and_hashes_provenance():
    report = ChemicalRFAnalysisPipeline().analyze_impedance("sample-a", 48 - 2j, {"frequency_hz": 1e6})
    assert report.provenance_hash
    assert report.warnings
    record = ChemicalRFAnalysisPipeline.record(report)
    assert record.results["impedance_real_ohm"].value == 48
