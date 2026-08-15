from typing import Any, Dict

try:
    import numpy as np
except Exception:
    np = None


def extract_basic_features(signal: Any) -> Dict[str, float]:
    """Extract simple time-domain features from a 1D signal (mean, std, max, min, rms)."""
    if np is None:
        # best-effort fallback
        return {"mean": 0.0, "std": 0.0, "max": 0.0, "min": 0.0, "rms": 0.0}
    arr = np.asarray(signal, dtype=float)
    mean = float(arr.mean())
    std = float(arr.std())
    mx = float(arr.max())
    mn = float(arr.min())
    rms = float((arr ** 2).mean() ** 0.5)
    return {"mean": mean, "std": std, "max": mx, "min": mn, "rms": rms}
