"""Spectral Profiler - Device Spectral Signature Analysis"""
import numpy as np
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class SpectralProfiler:
    """Analyze spectral signatures of RF devices"""
    
    def compute_spectral_mask(self, signal: np.ndarray, fs: float = 1e6,
                             threshold_db: float = -40) -> Tuple[np.ndarray, np.ndarray]:
        """Compute spectral occupancy mask
        
        Args:
            signal: IQ signal
            fs: Sample rate
            threshold_db: Detection threshold in dB
        
        Returns:
            (Frequencies, Mask)
        """
        fft = np.fft.fft(signal)
        power_db = 10 * np.log10(np.abs(fft) ** 2 + 1e-10)
        freqs = np.fft.fftfreq(len(signal), 1/fs)
        
        max_power = np.max(power_db)
        mask = power_db > (max_power + threshold_db)
        
        return freqs, mask
    
    def compute_spectral_signature(self, signal: np.ndarray, num_bins: int = 256) -> np.ndarray:
        """Compute spectral signature for device fingerprinting
        
        Args:
            signal: IQ signal
            num_bins: Number of frequency bins
        
        Returns:
            Normalized spectral signature
        """
        fft = np.fft.fft(signal)
        psd = np.abs(fft) ** 2
        
        # Bin PSD
        bin_size = len(psd) // num_bins
        signature = np.zeros(num_bins)
        for i in range(num_bins):
            signature[i] = np.mean(psd[i*bin_size:(i+1)*bin_size])
        
        # Normalize
        signature = signature / (np.sum(signature) + 1e-10)
        
        return signature
