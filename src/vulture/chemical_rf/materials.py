"""Material-facing RF observables and dielectric mixing estimates."""
from __future__ import annotations

from typing import Iterable, Tuple
import numpy as np


def complex_permittivity(epsilon_r: float, conductivity_s_m: float, frequency_hz: float) -> complex:
    """Return relative complex permittivity using exp(+jωt) convention."""
    if epsilon_r <= 0 or conductivity_s_m < 0 or frequency_hz <= 0:
        raise ValueError("epsilon_r/frequency_hz must be positive and conductivity non-negative")
    epsilon_0 = 8.8541878128e-12
    loss = conductivity_s_m / (2 * np.pi * frequency_hz * epsilon_0)
    return complex(epsilon_r, -loss)


def maxwell_garnett_permittivity(matrix: complex, inclusion: complex, volume_fraction: float) -> complex:
    """Estimate effective permittivity of dilute inclusions."""
    if not 0 <= volume_fraction < 1:
        raise ValueError("volume_fraction must be in [0, 1)")
    ratio = (inclusion - matrix) / (inclusion + 2 * matrix)
    return matrix * (1 + 3 * volume_fraction * ratio) / (1 - volume_fraction * ratio)


def dielectric_resonance_frequency(epsilon_r: float, length_m: float, mode: int = 1) -> float:
    """Half-wave resonator estimate, useful for screening material candidates."""
    if epsilon_r <= 0 or length_m <= 0 or mode < 1:
        raise ValueError("epsilon_r/length_m must be positive and mode >= 1")
    c = 299_792_458.0
    return mode * c / (2 * length_m * np.sqrt(epsilon_r))



def reflection_coefficient(load_ohm: complex, reference_ohm: complex = 50 + 0j) -> complex:
    """Return the complex reflection coefficient Γ = (Z_L - Z_0) / (Z_L + Z_0)."""
    if reference_ohm == 0:
        raise ValueError("reference impedance cannot be zero")
    return (load_ohm - reference_ohm) / (load_ohm + reference_ohm)


def absorption_coefficient(load_ohm: complex, reference_ohm: complex = 50 + 0j) -> float:
    """Return the power absorption coefficient derived from the reflection coefficient."""
    gamma = reflection_coefficient(load_ohm, reference_ohm)
    return 1 - abs(gamma) ** 2

