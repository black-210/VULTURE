"""Convolution Engine - Signal Convolution"""
import numpy as np
from scipy.signal import convolve, fftconvolve
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class ConvolutionEngine:
    """Compute signal convolutions"""
    
    @staticmethod
    def convolve_direct(signal1: np.ndarray, signal2: np.ndarray, mode: str = 'full') -> np.ndarray:
        """Direct convolution
        
        Args:
            signal1: First signal
            signal2: Second signal (usually filter)
            mode: 'full', 'same', or 'valid'
        
        Returns:
            Convolved signal
        """
        return convolve(signal1, signal2, mode=mode)
    
    @staticmethod
    def convolve_fft(signal1: np.ndarray, signal2: np.ndarray, mode: str = 'full') -> np.ndarray:
        """FFT-based convolution for large signals
        
        Args:
            signal1: First signal
            signal2: Second signal (usually filter)
            mode: 'full', 'same', or 'valid'
        
        Returns:
            Convolved signal
        """
        return fftconvolve(signal1, signal2, mode=mode)
    
    @staticmethod
    def deconvolve(signal: np.ndarray, kernel: np.ndarray, reg_param: float = 1e-6) -> np.ndarray:
        """Wiener deconvolution
        
        Args:
            signal: Observed signal
            kernel: Convolution kernel
            reg_param: Regularization parameter
        
        Returns:
            Deconvolved signal estimate
        """
        h_fft = np.fft.fft(kernel, len(signal))
        s_fft = np.fft.fft(signal)
        
        # Wiener filter
        wiener_filter = np.conj(h_fft) / (np.abs(h_fft) ** 2 + reg_param)
        result = np.real(np.fft.ifft(wiener_filter * s_fft))
        
        return result
