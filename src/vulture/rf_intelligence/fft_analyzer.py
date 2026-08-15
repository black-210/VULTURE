"""FFT Analyzer utilities for RF intelligence.

Provides convenience around numpy.fft with windowing and zero-padding.
"""
from typing import Tuple, Optional
import numpy as np


class FFTAnalyzer:
    """Compute FFT with common options (windowing, zero-pad).

    Example:
        analyzer = FFTAnalyzer(fft_size=1024)
        freqs, mags = analyzer.compute_fft(signal, fs=1000)
    """

    def __init__(self, fft_size: int = 1024, window: Optional[str] = "hann"):
        self.fft_size = int(fft_size)
        self.window = window

    def compute_fft(self, data: np.ndarray, fs: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """Return frequency axis and magnitude spectrum (one-sided for real inputs).

        Args:
            data: 1D signal
            fs: sampling frequency
        """
        data = np.asarray(data)
        n = self.fft_size
        # apply window
        if self.window:
            win = np.hanning(len(data)) if self.window == "hann" else np.ones(len(data))
        else:
            win = np.ones(len(data))
        x = data * win
        # zero-pad or truncate
        if len(x) < n:
            x = np.pad(x, (0, n - len(x)))
        else:
            x = x[:n]
        X = np.fft.rfft(x)
        freqs = np.fft.rfftfreq(n, d=1.0 / fs)
        mags = np.abs(X)
        return freqs, mags
