"""Noise Estimator - SNR and Noise Floor Analysis"""
import numpy as np
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)

class NoiseEstimator:
    """Estimate noise floor and SNR"""
    
    def estimate_noise_floor(self, psd: np.ndarray, percentile: float = 10) -> float:
        """Estimate noise floor
        
        Args:
            psd: Power spectral density
            percentile: Percentile for noise floor
        
        Returns:
            Noise floor level
        """
        return np.percentile(psd, percentile)
    
    def estimate_snr(self, signal: np.ndarray, noise_only: np.ndarray) -> float:
        """Estimate SNR
        
        Args:
            signal: Signal + noise
            noise_only: Noise-only sample
        
        Returns:
            SNR in dB
        """
        signal_power = np.mean(np.abs(signal) ** 2)
        noise_power = np.mean(np.abs(noise_only) ** 2)
        snr_db = 10 * np.log10(signal_power / (noise_power + 1e-10))
        return snr_db
    
    def estimate_cnr(self, freqs: np.ndarray, psd: np.ndarray,
                    carrier_freq: float, bandwidth: float) -> float:
        """Estimate Carrier-to-Noise Ratio
        
        Args:
            freqs: Frequency array
            psd: Power spectral density
            carrier_freq: Carrier frequency
            bandwidth: Signal bandwidth
        
        Returns:
            CNR in dB
        """
        carrier_mask = np.abs(freqs - carrier_freq) < bandwidth / 2
        carrier_power = np.max(psd[carrier_mask]) if np.any(carrier_mask) else 1
        
        noise_mask = (np.abs(freqs - carrier_freq) > bandwidth) & \
                     (np.abs(freqs - carrier_freq) < bandwidth * 5)
        noise_power = np.mean(psd[noise_mask]) if np.any(noise_mask) else 1e-10
        
        cnr_db = 10 * np.log10(carrier_power / noise_power)
        return cnr_db
