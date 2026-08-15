"""Spectrum Intelligence core utilities.

Basic SpectrumAnalyzer placeholder to support higher-level integrations.
"""
from typing import Tuple
import numpy as np


class SpectrumAnalyzer:
    """Simple spectrum analyzer placeholder.

    Methods:
        analyze(samples, fs) -> (freqs, spectrum)
    """

    @staticmethod
    def analyze(samples: np.ndarray, fs: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        samples = np.asarray(samples)
        n = len(samples)
        X = np.fft.rfft(samples * np.hanning(n))
        freqs = np.fft.rfftfreq(n, d=1.0 / fs)
        spectrum = np.abs(X)
        return freqs, spectrum
