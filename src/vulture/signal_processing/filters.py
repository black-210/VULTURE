"""FIR filter design and application helpers.

Wraps scipy.signal firwin and lfilter/filtfilt where available, with numpy
fallbacks to keep the API usable in minimal environments.
"""
from typing import Sequence
import numpy as np

try:
    from scipy import signal
except Exception:  # pragma: no cover
    signal = None


class Filters:
    @staticmethod
    def design_fir(order: int, cutoff: float, window: str = 'hamming') -> np.ndarray:
        """Design a lowpass FIR filter.

        Args:
            order: filter order (number of taps)
            cutoff: normalized cutoff (0..0.5)
            window: window name
        """
        numtaps = max(3, order + 1)
        if signal is not None:
            return signal.firwin(numtaps, cutoff, window=window)
        # Simple sinc-based design
        n = np.arange(numtaps) - (numtaps - 1) / 2.0
        h = np.sinc(2 * cutoff * n)
        w = np.hamming(numtaps)
        h *= w
        h /= np.sum(h)
        return h

    @staticmethod
    def apply_fir(data: Sequence[float], b: np.ndarray) -> np.ndarray:
        data = np.asarray(data)
        if signal is not None:
            return signal.lfilter(b, [1.0], data)
        # naive convolution fallback
        return np.convolve(data, b, mode='same')
