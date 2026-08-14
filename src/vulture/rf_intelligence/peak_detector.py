"""Peak detection in frequency domain."""
import numpy as np
from scipy import signal
import logging

logger = logging.getLogger(__name__)

class PeakDetector:
    """Peak detection methods."""
    
    @staticmethod
    def find_peaks(magnitude, height=None, distance=10, prominence=None):
        peaks, properties = signal.find_peaks(magnitude, height=height, distance=distance, prominence=prominence)
        return peaks, properties
    
    @staticmethod
    def get_peak_frequencies(peaks, frequencies):
        return frequencies[peaks]
    
    @staticmethod
    def get_top_peaks(magnitude, frequencies, num_peaks=5):
        peaks, _ = signal.find_peaks(magnitude)
        if len(peaks) == 0:
            return np.array([]), np.array([])
        top_indices = np.argsort(magnitude[peaks])[-num_peaks:]
        top_peaks = peaks[top_indices]
        return top_peaks, frequencies[top_peaks]
    
    @staticmethod
    def cwt_peak_detection(data, widths=None):
        if widths is None:
            widths = np.arange(1, 31)
        cwtmatr = signal.morlet2(min(10, len(data)), m=6)
        peaks = signal.find_peaks_cwt(data, widths)
        return peaks