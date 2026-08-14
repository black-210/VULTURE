"""PSD Analyzer - Power Spectral Density Computation"""
import numpy as np
from scipy.signal import welch, periodogram
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class PSDAnalyzer:
    """Power Spectral Density analysis"""
    
    def __init__(self, sample_rate: float = 1e6):
        self.sample_rate = sample_rate
    
    def compute_welch_psd(self, signal: np.ndarray, nperseg: int = 1024) -> Tuple[np.ndarray, np.ndarray]:
        """Compute Welch PSD
        
        Args:
            signal: Input signal
            nperseg: Segment length
        
        Returns:
            Frequencies and PSD
        """
        freqs, psd = welch(signal, fs=self.sample_rate, nperseg=nperseg)
        return freqs, psd
    
    def compute_periodogram(self, signal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute periodogram
        
        Args:
            signal: Input signal
        
        Returns:
            Frequencies and PSD
        """
        freqs, psd = periodogram(signal, fs=self.sample_rate)
        return freqs, psd
    
    def get_power_in_band(self, psd: np.ndarray, freqs: np.ndarray, 
                         freq_start: float, freq_stop: float) -> float:
        """Get power in frequency band
        
        Args:
            psd: Power spectral density
            freqs: Frequency array
            freq_start: Start frequency
            freq_stop: Stop frequency
        
        Returns:
            Power in band
        """
        mask = (freqs >= freq_start) & (freqs <= freq_stop)
        return np.sum(psd[mask])
