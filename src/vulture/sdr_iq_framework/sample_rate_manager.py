"""Sample rate management: resample, decimate, interpolate."""

import numpy as np
from scipy import signal
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class SampleRateManager:
    """Efficient sample rate conversion."""

    @staticmethod
    def resample(data: np.ndarray, input_rate: float, output_rate: float,
                 method: str = 'scipy') -> Tuple[np.ndarray, float]:
        """Resample signal.
        
        Args:
            data: Input signal
            input_rate: Input sample rate
            output_rate: Target sample rate
            method: 'scipy' or 'polyphase'
            
        Returns:
            (resampled_data, output_rate)
        """
        ratio = output_rate / input_rate
        
        if method == 'scipy':
            num_samples = int(len(data) * ratio)
            resampled = signal.resample(data, num_samples)
        else:  # polyphase
            from scipy.signal import resample_poly
            up = int(output_rate)
            down = int(input_rate)
            resampled = resample_poly(data, up, down)
        
        logger.info(f"✓ Resampled: {input_rate/1e6:.1f}MHz -> {output_rate/1e6:.1f}MHz")
        return resampled, output_rate

    @staticmethod
    def decimate(data: np.ndarray, factor: int) -> np.ndarray:
        """Decimate signal (reduce sample rate).
        
        Args:
            data: Input signal
            factor: Decimation factor
            
        Returns:
            Decimated signal
        """
        decimated = signal.decimate(data, factor, zero_phase=True)
        logger.info(f"✓ Decimated by factor {factor}")
        return decimated

    @staticmethod
    def interpolate(data: np.ndarray, factor: int) -> np.ndarray:
        """Interpolate signal (increase sample rate).
        
        Args:
            data: Input signal
            factor: Interpolation factor
            
        Returns:
            Interpolated signal
        """
        # Insert zeros and apply lowpass filter
        upsampled = np.zeros(len(data) * factor, dtype=data.dtype)
        upsampled[::factor] = data
        
        # Design and apply lowpass filter
        b = signal.firwin(65, 1.0 / factor)
        interpolated = signal.convolve(upsampled, b, mode='same') * factor
        
        logger.info(f"✓ Interpolated by factor {factor}")
        return interpolated
