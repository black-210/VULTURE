"""Advanced peak detection: CWT, distance/prominence filtering, thresholding."""

import numpy as np
from scipy import signal
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class PeakDetector:
    """Production-grade peak detection."""

    @staticmethod
    def find_peaks(data: np.ndarray, height: float = None, distance: int = None,
                   prominence: float = None) -> Tuple[np.ndarray, Dict]:
        """Find peaks with filtering.
        
        Args:
            data: Input signal
            height: Minimum peak height
            distance: Minimum distance between peaks
            prominence: Minimum peak prominence
            
        Returns:
            (peak_indices, properties_dict)
        """
        peaks, properties = signal.find_peaks(
            data, height=height, distance=distance, prominence=prominence
        )
        return peaks, properties

    @staticmethod
    def cwt_ridge_detection(data: np.ndarray, scales: np.ndarray = None,
                           wavelet: str = 'morlet') -> Tuple[np.ndarray, np.ndarray]:
        """Continuous Wavelet Transform ridge detection.
        
        Args:
            data: Input signal
            scales: Scales to use
            wavelet: Wavelet type
            
        Returns:
            (ridge_frequencies, ridge_magnitudes)
        """
        if scales is None:
            scales = np.arange(1, min(len(data)//2, 128))
        
        coefficients = signal.cwt(data, signal.morlet2, scales)
        ridge = np.argmax(np.abs(coefficients), axis=0)
        ridge_magnitudes = np.abs(coefficients)[ridge, np.arange(len(data))]
        ridge_frequencies = ridge / (len(data) * 0.5)
        return ridge_frequencies, ridge_magnitudes

    @staticmethod
    def threshold_adaptive(data: np.ndarray, method: str = 'otsu') -> Tuple[np.ndarray, float]:
        """Adaptive thresholding for peak detection.
        
        Args:
            data: Input signal
            method: 'otsu', 'percentile', or 'median'
            
        Returns:
            (thresholded_data, threshold_value)
        """
        if method == 'otsu':
            threshold = 0.3 * (np.max(data) - np.min(data)) + np.min(data)  # Simple Otsu approximation
        elif method == 'percentile':
            threshold = np.percentile(data, 75)
        else:  # median
            threshold = np.median(data) * 1.5
        
        thresholded = np.maximum(data - threshold, 0)
        return thresholded, threshold
