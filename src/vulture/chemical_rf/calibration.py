"""Calibration and uncertainty propagation for equivalent RF models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List
import numpy as np

from .models import CalibrationPoint


@dataclass(frozen=True)
class LinearCalibration:
    """Complex affine correction Z_corrected = gain * Z + offset."""

    gain: complex
    offset: complex
    residual_rms_ohm: float
    points_used: int

    def apply(self, impedance: complex) -> complex:
        return self.gain * impedance + self.offset


class ImpedanceCalibrator:
    """Fit a stable one-parameter complex correction from reference loads."""

    def fit(self, predicted: Iterable[complex], measured: Iterable[CalibrationPoint]) -> LinearCalibration:
        predicted_values = np.asarray(list(predicted), dtype=complex)
        points: List[CalibrationPoint] = list(measured)
        if len(predicted_values) != len(points) or len(points) < 2:
            raise ValueError("at least two matching prediction/reference points are required")
        observed = np.asarray([p.measured_impedance_ohm for p in points], dtype=complex)
        design = np.column_stack((predicted_values, np.ones(len(points), dtype=complex)))
        real_design = np.block([[design.real, -design.imag], [design.imag, design.real]])
        real_observed = np.r_[observed.real, observed.imag]
        coefficients, *_ = np.linalg.lstsq(real_design, real_observed, rcond=None)
        gain = complex(coefficients[0], coefficients[2])
        offset = complex(coefficients[1], coefficients[3])
        residual = gain * predicted_values + offset - observed
        return LinearCalibration(gain, offset, float(np.sqrt(np.mean(np.abs(residual) ** 2))), len(points))


def combine_uncertainty(*uncertainties: float) -> float:
    """Combine independent standard uncertainties by root-sum-square."""
    if any(value < 0 for value in uncertainties):
        raise ValueError("uncertainties cannot be negative")
    return float(np.sqrt(np.sum(np.square(uncertainties))))
