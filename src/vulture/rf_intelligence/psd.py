"""PSD utilities using scipy.signal where available.

Provides a thin wrapper around scipy.signal.welch with sensible defaults.
"""
from typing import Tuple
import numpy as np

try:
    from scipy import signal
except Exception:  # pragma: no cover - scipy optional
    signal = None


class PSDAnalyzer:
    @staticmethod
    def welch(data: np.ndarray, fs: float = 1.0, nperseg: int = 256) -> Tuple[np.ndarray, np.ndarray]:
        """Compute Welch PSD. Falls back to numpy FFT-based periodogram if scipy not present."""
        x = np.asarray(data)
        if signal is not None:
            freqs, Pxx = signal.welch(x, fs=fs, nperseg=nperseg)
            return freqs, Pxx
        # fallback: simple periodogram
        n = len(x)
        X = np.fft.rfft(x * np.hanning(n))
        Pxx = (1.0 / (fs * n)) * (np.abs(X) ** 2)
        freqs = np.fft.rfftfreq(n, d=1.0 / fs)
        return freqs, Pxx
