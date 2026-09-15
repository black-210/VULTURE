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
    def analyze_signal(self, signal: np.ndarray, method: str = 'welch', nperseg: int = 1024) -> Tuple[np.ndarray, np.ndarray]:
        """Analyze signal and compute PSD
        
        Args:
            signal: Input signal
            method: Method to compute PSD ('welch' or 'periodogram')
            nperseg: Segment length for Welch method
        
        Returns:
            Frequencies and PSD
        """
        if method == 'welch':
            return self.compute_welch_psd(signal, nperseg)
        elif method == 'periodogram':
            return self.compute_periodogram(signal)
        else:
            logger.error(f"Unknown method {method}. Use 'welch' or 'periodogram'.")
            raise ValueError(f"Unknown method {method}. Use 'welch' or 'periodogram'.")
    def plot_psd(self, freqs: np.ndarray, psd: np.ndarray, title: str = 'Power Spectral Density'):
        """Plot PSD
        
        Args:
            freqs: Frequency array
            psd: Power spectral density
            title: Plot title
            """
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        plt.semilogy(freqs, psd)
        plt.title(title)
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('PSD [V**2/Hz]')
        plt.grid()
        plt.show()
    def save_psd(self, freqs: np.ndarray, psd: np.ndarray, filename: str):
        """Save PSD to file
        
        Args:
            freqs: Frequency array
            psd: Power spectral density
            filename: Output filename
        """
        np.savez(filename, freqs=freqs, psd=psd)
        np.savetxt(filename.replace('.npz', '.txt'), np.column_stack((freqs, psd)), header='Frequency [Hz]\tPSD [V**2/Hz]')
        scipy.io.savemat(filename.removeprefix('.npz') + '.mat', {'freqs': freqs, 'psd': psd})