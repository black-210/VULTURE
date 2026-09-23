"""Numerically stable descriptive statistics for complex IQ captures."""
from __future__ import annotations

import numpy as np


def summarize(samples: np.ndarray) -> dict[str, float | int]:
    values = np.asarray(samples, dtype=np.complex64)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("samples must be a non-empty one-dimensional array")
    if not np.isfinite(values.real).all() or not np.isfinite(values.imag).all():
        raise ValueError("samples must be finite")
    magnitude = np.abs(values)
    power = magnitude * magnitude
    return {
        "samples": int(values.size),
        "mean_i": float(values.real.mean()),
        "mean_q": float(values.imag.mean()),
        "rms": float(np.sqrt(power.mean())),
        "peak": float(magnitude.max()),
        "mean_power": float(power.mean()),
        "crest_factor": float(magnitude.max() / np.sqrt(power.mean())) if power.mean() else 0.0,
    }
