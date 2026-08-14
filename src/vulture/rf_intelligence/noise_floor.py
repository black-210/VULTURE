"""Noise floor estimation."""
import numpy as np
import logging

logger = logging.getLogger(__name__)

class NoiseFloorEstimation:
    """Noise floor estimation methods."""
    
    @staticmethod
    def estimate_noise_floor(psd, percentile=10.0):
        return np.percentile(psd, percentile)
    
    @staticmethod
    def estimate_snr(signal_power, noise_floor):
        if noise_floor <= 0:
            return float('inf')
        return 10 * np.log10(signal_power / noise_floor)
    
    @staticmethod
    def noise_figure(input_snr, output_snr):
        return input_snr - output_snr
    
    @staticmethod
    def thermal_noise(bandwidth, temperature=290):
        k_b = 1.38e-23
        return 10 * np.log10(k_b * temperature * bandwidth / 1e-3)