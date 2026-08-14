"""FIR Filter - Finite Impulse Response Filters"""
import numpy as np
from scipy.signal import firwin, lfilter, filtfilt
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class FIRFilter:
    """FIR filter design and implementation"""
    
    def __init__(self, order: int, fs: float = 1e6):
        """Initialize FIR filter
        
        Args:
            order: Filter order
            fs: Sample rate
        """
        self.order = order
        self.fs = fs
        self.coeffs = None
        self.state = None
    
    def design_lowpass(self, cutoff: float) -> np.ndarray:
        """Design lowpass filter
        
        Args:
            cutoff: Cutoff frequency
        
        Returns:
            Filter coefficients
        """
        self.coeffs = firwin(self.order, cutoff, fs=self.fs, window='hamming')
        return self.coeffs
    
    def design_highpass(self, cutoff: float) -> np.ndarray:
        """Design highpass filter
        
        Args:
            cutoff: Cutoff frequency
        
        Returns:
            Filter coefficients
        """
        self.coeffs = firwin(self.order, cutoff, fs=self.fs, pass_zero=False, window='hamming')
        return self.coeffs
    
    def design_bandpass(self, low: float, high: float) -> np.ndarray:
        """Design bandpass filter
        
        Args:
            low: Low cutoff frequency
            high: High cutoff frequency
        
        Returns:
            Filter coefficients
        """
        self.coeffs = firwin(self.order, [low, high], fs=self.fs, window='hamming')
        return self.coeffs
    
    def apply(self, signal: np.ndarray, zero_phase: bool = False) -> np.ndarray:
        """Apply filter to signal
        
        Args:
            signal: Input signal
            zero_phase: Use zero-phase filtering
        
        Returns:
            Filtered signal
        """
        if self.coeffs is None:
            raise ValueError("Filter not designed yet")
        
        if zero_phase:
            return filtfilt(self.coeffs, 1, signal)
        else:
            return lfilter(self.coeffs, 1, signal)
    
    def get_frequency_response(self, n_points: int = 1024) -> Tuple[np.ndarray, np.ndarray]:
        """Get frequency response
        
        Args:
            n_points: Number of frequency points
        
        Returns:
            (Frequencies, Magnitude response)
        """
        if self.coeffs is None:
            raise ValueError("Filter not designed yet")
        
        from scipy.signal import freqz
        w, h = freqz(self.coeffs, [1], worN=n_points)
        freqs = w * self.fs / (2 * np.pi)
        return freqs, 20 * np.log10(np.abs(h) + 1e-10)
