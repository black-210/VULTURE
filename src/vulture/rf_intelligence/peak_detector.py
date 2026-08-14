"""Peak Detector - Signal Peak Analysis"""
import numpy as np
from scipy.signal import find_peaks
from typing import Tuple, List, Dict
import logging

logger = logging.getLogger(__name__)

class PeakDetector:
    """Detect and analyze signal peaks"""
    
    def detect_peaks(self, signal: np.ndarray, height: float = None,
                    distance: int = None) -> Tuple[np.ndarray, Dict]:
        """Detect peaks in signal
        
        Args:
            signal: Input signal
            height: Minimum peak height
            distance: Minimum distance between peaks
        
        Returns:
            Peak indices and properties
        """
        peaks, properties = find_peaks(signal, height=height, distance=distance)
        return peaks, properties
    
    def get_strongest_peaks(self, freqs: np.ndarray, psd: np.ndarray,
                           num_peaks: int = 10) -> List[Tuple[float, float]]:
        """Get strongest peaks
        
        Args:
            freqs: Frequency array
            psd: Power spectral density
            num_peaks: Number of peaks to return
        
        Returns:
            List of (frequency, power) tuples
        """
        peak_indices = np.argsort(psd)[-num_peaks:]
        peaks = [(freqs[i], psd[i]) for i in sorted(peak_indices, reverse=True)]
        return peaks
