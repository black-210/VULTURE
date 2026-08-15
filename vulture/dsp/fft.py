from typing import Any

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None


def fft(samples: Any):
    """Compute FFT of input samples. Returns frequency-domain complex values."""
    if np is None:
        raise RuntimeError("numpy is required for FFT")
    return np.fft.fft(samples)

def ifft(spectrum: Any):
    if np is None:
        raise RuntimeError("numpy is required for IFFT")
    return np.fft.ifft(spectrum)
