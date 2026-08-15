"""FIR/IIR filter design and application."""

import numpy as np
from scipy import signal
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class Filters:
    """Production-grade filter design and application."""

    @staticmethod
    def design_fir(order: int, cutoff: float, window: str = 'hamming') -> np.ndarray:
        """Design FIR filter.
        
        Args:
            order: Filter order
            cutoff: Normalized cutoff frequency (0-1)
            window: Window type
            
        Returns:
            FIR coefficients
        """
        b = signal.firwin(order, cutoff, window=window)
        logger.debug(f"Designed FIR filter: order={order}, cutoff={cutoff}")
        return b

    @staticmethod
    def design_iir(order: int, cutoff: float, btype: str = 'low') -> Tuple[np.ndarray, np.ndarray]:
        """Design IIR Butterworth filter.
        
        Args:
            order: Filter order
            cutoff: Normalized cutoff frequency
            btype: 'low', 'high', 'band', 'stop'
            
        Returns:
            (b, a) coefficients
        """
        b, a = signal.butter(order, cutoff, btype=btype)
        logger.debug(f"Designed IIR filter: order={order}, type={btype}")
        return b, a

    @staticmethod
    def apply_fir(data: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Apply FIR filter using filtfilt (zero-phase).
        
        Args:
            data: Input signal
            b: FIR coefficients
            
        Returns:
            Filtered signal
        """
        return signal.filtfilt(b, [1], data)

    @staticmethod
    def apply_iir(data: np.ndarray, b: np.ndarray, a: np.ndarray) -> np.ndarray:
        """Apply IIR filter using filtfilt (zero-phase).
        
        Args:
            data: Input signal
            b, a: IIR coefficients
            
        Returns:
            Filtered signal
        """
        return signal.filtfilt(b, a, data)

    @staticmethod
    def cascade_filters(data: np.ndarray, filters: list) -> np.ndarray:
        """Apply multiple filters in cascade.
        
        Args:
            data: Input signal
            filters: List of (b, a) or (b,) tuples
            
        Returns:
            Filtered signal
        """
        result = data.copy()
        for f in filters:
            if len(f) == 2:
                result = Filters.apply_iir(result, f[0], f[1])
            else:
                result = Filters.apply_fir(result, f[0])
        return result
