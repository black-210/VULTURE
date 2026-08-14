"""Correlation Engine - Signal Correlation Analysis"""
import numpy as np
from scipy.signal import correlate, correlation_lags
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class CorrelationEngine:
    """Compute signal correlations"""
    
    @staticmethod
    def autocorrelation(signal: np.ndarray, max_lag: int = None) -> Tuple[np.ndarray, np.ndarray]:
        """Compute autocorrelation
        
        Args:
            signal: Input signal
            max_lag: Maximum lag to compute
        
        Returns:
            (Lags, Autocorrelation values)
        """
        if max_lag is None:
            max_lag = len(signal) - 1
        
        auto_corr = correlate(signal, signal, mode='full')
        lags = correlation_lags(len(signal), len(signal), mode='full')
        
        center = len(auto_corr) // 2
        return lags[center:center+max_lag], auto_corr[center:center+max_lag]
    
    @staticmethod
    def cross_correlation(signal1: np.ndarray, signal2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute cross-correlation
        
        Args:
            signal1: First signal
            signal2: Second signal
        
        Returns:
            (Lags, Cross-correlation values)
        """
        cross_corr = correlate(signal1, signal2, mode='full')
        lags = correlation_lags(len(signal1), len(signal2), mode='full')
        return lags, cross_corr
    
    @staticmethod
    def find_delay(signal1: np.ndarray, signal2: np.ndarray) -> int:
        """Find delay between two signals
        
        Args:
            signal1: Reference signal
            signal2: Signal with potential delay
        
        Returns:
            Estimated delay in samples
        """
        lags, cross_corr = CorrelationEngine.cross_correlation(signal1, signal2)
        max_idx = np.argmax(np.abs(cross_corr))
        return lags[max_idx]
