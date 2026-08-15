"""Noise floor estimation and SNR/NF computation."""

import numpy as np
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class NoiseFloorEstimator:
    """Production-grade noise floor estimation."""

    @staticmethod
    def estimate_percentile(power_db: np.ndarray, percentile: float = 10) -> float:
        """Estimate noise floor using percentile method.
        
        Args:
            power_db: Power spectrum in dB
            percentile: Percentile level (lower = more noise-only)
            
        Returns:
            Noise floor in dB
        """
        return np.percentile(power_db, percentile)

    @staticmethod
    def estimate_median(power_db: np.ndarray, robust: bool = True) -> float:
        """Estimate noise floor using median.
        
        Args:
            power_db: Power spectrum in dB
            robust: Use MAD (Median Absolute Deviation) for robustness
            
        Returns:
            Noise floor in dB
        """
        median = np.median(power_db)
        if robust:
            mad = np.median(np.abs(power_db - median))
            return median + 1.4826 * mad  # 1.4826 for Gaussian
        return median

    @staticmethod
    def compute_snr(signal_power_db: float, noise_floor_db: float) -> float:
        """Compute SNR in dB.
        
        Args:
            signal_power_db: Signal power in dB
            noise_floor_db: Noise floor in dB
            
        Returns:
            SNR in dB
        """
        return signal_power_db - noise_floor_db

    @staticmethod
    def compute_nf(all_power_db: np.ndarray, noise_floor_db: float) -> float:
        """Compute Noise Figure.
        
        Args:
            all_power_db: All power measurements in dB
            noise_floor_db: Noise floor in dB
            
        Returns:
            Noise Figure in dB
        """
        signal_power = np.mean(all_power_db)
        return signal_power - noise_floor_db
