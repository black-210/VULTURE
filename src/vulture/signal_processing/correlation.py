"""Cross/auto correlation and fast methods."""

import numpy as np
from scipy import signal
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class CorrelationEngine:
    """High-performance correlation."""

    @staticmethod
    def xcorr(x: np.ndarray, y: np.ndarray, mode: str = 'full') -> Tuple[np.ndarray, np.ndarray]:
        """Cross-correlation.
        
        Args:
            x, y: Input signals
            mode: 'full', 'same', 'valid'
            
        Returns:
            (correlation, lags)
        """
        corr = signal.correlate(x, y, mode=mode)
        lags = signal.correlation_lags(len(x), len(y), mode=mode)
        return corr, lags

    @staticmethod
    def acorr(x: np.ndarray, mode: str = 'full') -> Tuple[np.ndarray, np.ndarray]:
        """Auto-correlation.
        
        Args:
            x: Input signal
            mode: 'full', 'same', 'valid'
            
        Returns:
            (autocorrelation, lags)
        """
        corr = signal.correlate(x, x, mode=mode)
        lags = signal.correlation_lags(len(x), len(x), mode=mode)
        return corr, lags

    @staticmethod
    def xcorr_fft(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Fast cross-correlation via FFT.
        
        Args:
            x, y: Input signals
            
        Returns:
            Cross-correlation
        """
        X = np.fft.fft(x, n=len(x) + len(y) - 1)
        Y = np.fft.fft(y, n=len(x) + len(y) - 1)
        return np.fft.ifft(X * np.conj(Y)).real

    @staticmethod
    def find_delay(x: np.ndarray, y: np.ndarray) -> int:
        """Find delay between signals.
        
        Args:
            x, y: Input signals
            
        Returns:
            Estimated delay (samples)
        """
        corr, lags = CorrelationEngine.xcorr(x, y, mode='full')
        delay_idx = np.argmax(np.abs(corr))
        return lags[delay_idx]
