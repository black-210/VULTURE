"""Validation helpers for deterministic local analysis."""
from __future__ import annotations

import math
from collections.abc import Iterable


def finite_values(values: Iterable[float]) -> list[float]:
    result = [float(value) for value in values]
    if not result:
        raise ValueError("at least one value is required")
    if not all(math.isfinite(value) for value in result):
        raise ValueError("all values must be finite")
    return result
