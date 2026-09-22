"""Basic uncertainty propagation for independent scalar measurements."""
from __future__ import annotations
import math


def combine_uncertainty(*uncertainties: float) -> float:
    if not uncertainties or any(value < 0 or not math.isfinite(value) for value in uncertainties):
        raise ValueError("uncertainties must be finite non-negative values")
    return math.sqrt(sum(value * value for value in uncertainties))
