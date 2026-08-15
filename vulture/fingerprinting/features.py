from typing import Any, Dict

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None


def extract_fingerprint_features(signal: Any, sample_rate: float = 1.0) -> Dict[str, float]:
    """Extract a set of RF fingerprinting features from a 1D IQ magnitude or power signal.

    Returns a dictionary of numeric features (statistical + spectral approximations).
    """
    if np is None:
        return {"mean": 0.0, "std": 0.0}

    arr = np.asarray(signal, dtype=float)
    out = {}
    out["mean"] = float(arr.mean())
    out["std"] = float(arr.std())
    out["max"] = float(arr.max())
    out["min"] = float(arr.min())
    out["rms"] = float((arr ** 2).mean() ** 0.5)

    # Simple spectral proxy using FFT magnitude moments
    try:
        spec = np.abs(np.fft.rfft(arr))
        spec_norm = spec / (spec.sum() + 1e-12)
        freqs = np.fft.rfftfreq(len(arr), d=1.0 / sample_rate)
        out["spec_centroid"] = float((freqs * spec_norm).sum())
        out["spec_spread"] = float(((freqs - out["spec_centroid"]) ** 2 * spec_norm).sum())
    except Exception:
        out["spec_centroid"] = 0.0
        out["spec_spread"] = 0.0

    return out
