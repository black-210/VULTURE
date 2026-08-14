"""Resampler - IQ Data Resampling & Decimation"""
import numpy as np
from scipy.signal import resample, decimate
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class Resampler:
    """Resample and decimate IQ signals"""
    
    def resample_to_rate(self, data: np.ndarray, orig_rate: float,
                        target_rate: float) -> Tuple[np.ndarray, float]:
        """Resample to target rate
        
        Args:
            data: IQ data
            orig_rate: Original sample rate
            target_rate: Target sample rate
        
        Returns:
            (Resampled data, new rate)
        """
        ratio = target_rate / orig_rate
        new_length = int(len(data) * ratio)
        resampled = resample(data, new_length)
        return resampled, target_rate
    
    def decimate(self, data: np.ndarray, factor: int, order: int = 5) -> np.ndarray:
        """Decimate signal
        
        Args:
            data: IQ data
            factor: Decimation factor
            order: Filter order
        
        Returns:
            Decimated data
        """
        if factor <= 1:
            return data
        return decimate(data, factor, n=order, zero_phase=True)
