"""IQ quality gates for real capture pipelines."""
from __future__ import annotations

import numpy as np


def quality_report(samples: np.ndarray, sample_rate: float) -> dict[str, object]:
    values = np.asarray(samples)
    finite = bool(np.isfinite(values.real).all() and np.isfinite(values.imag).all()) if values.size else False
    return {
        "ok": bool(values.ndim == 1 and values.size > 0 and finite and sample_rate > 0),
        "sample_count": int(values.size),
        "sample_rate_hz": float(sample_rate),
        "finite": finite,
        "complex": bool(np.iscomplexobj(values)),
        "clipped_fraction": float(np.mean(np.abs(values) >= 1.0)) if values.size else 0.0,
    }
