"""
PSD computation using SciPy with numpy fallback.
Provides Welch and periodogram methods and a simple API returning freqs and psd.
"""
from typing import Tuple, Dict, Any

try:
    import numpy as np
except Exception:  # pragma: no cover - optional
    np = None


def compute_psd(samples, fs: float = 1.0, method: str = "welch", **kwargs) -> Dict[str, Any]:
    """Compute power spectral density (PSD) of the signal.

    Args:
        samples: 1D array-like real or complex samples.
        fs: Sampling frequency in Hz.
        method: 'welch' or 'periodogram'.
        kwargs: forwarded to scipy.signal functions (nperseg, noverlap, window, etc.).

    Returns:
        dict with keys: 'freqs', 'psd'
    """
    if np is None:
        raise RuntimeError("numpy is required for PSD computation")

    samples = np.asarray(samples)

    try:
        from scipy import signal

        if method == "welch":
            nperseg = kwargs.get("nperseg", 1024)
            noverlap = kwargs.get("noverlap", nperseg // 2)
            freqs, psd = signal.welch(samples, fs=fs, nperseg=nperseg, noverlap=noverlap, window=kwargs.get("window", "hann"))
            return {"freqs": freqs, "psd": psd}
        elif method == "periodogram":
            freqs, psd = signal.periodogram(samples, fs=fs, window=kwargs.get("window", "hann"))
            return {"freqs": freqs, "psd": psd}
        else:
            raise ValueError(f"Unsupported PSD method: {method}")
    except Exception:
        # Fallback: naive FFT-based periodogram approximation
        N = len(samples)
        spec = np.fft.rfft(samples * np.hanning(N))
        psd = (np.abs(spec) ** 2) / (fs * N)
        freqs = np.fft.rfftfreq(N, d=1.0 / fs)
        return {"freqs": freqs, "psd": psd}
