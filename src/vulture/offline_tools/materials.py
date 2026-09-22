"""Offline material screening primitives."""
from __future__ import annotations
import math


def half_wave_resonance(epsilon_r: float, length_m: float) -> float:
    if epsilon_r <= 0 or length_m <= 0:
        raise ValueError("epsilon_r and length_m must be positive")
    return 299_792_458.0 / (2 * length_m * math.sqrt(epsilon_r))
