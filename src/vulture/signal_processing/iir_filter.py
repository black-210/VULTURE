"""IIR Filter - Infinite Impulse Response Filters"""
import numpy as np
from scipy.signal import butter, iirfilter, lfilter, filtfilt, sosfilt, sosfilt_zi
from typing import Tuple, List
import logging

logger = logging.getLogger(__name__)

class IIRFilter:
    """IIR filter design and implementation"""
    
    def __init__(self, order: int, fs: float = 1e6):
        """Initialize IIR filter
        
        Args:
            order: Filter order
            fs: Sample rate
        """
        self.order = order
        self.fs = fs
        self.b = None
        self.a = None
        self.sos = None
    
    def design_butterworth_lowpass(self, cutoff: float) -> Tuple[np.ndarray, np.ndarray]:
        """Design Butterworth lowpass filter
        
        Args:
            cutoff: Cutoff frequency
        
        Returns:
            (Numerator, Denominator) coefficients
        """
        nyquist = self.fs / 2
        normalized_cutoff = cutoff / nyquist
        self.b, self.a = butter(self.order, normalized_cutoff, btype='low')
        return self.b, self.a
    
    def design_butterworth_highpass(self, cutoff: float) -> Tuple[np.ndarray, np.ndarray]:
        """Design Butterworth highpass filter
        
        Args:
            cutoff: Cutoff frequency
        
        Returns:
            (Numerator, Denominator) coefficients
        """
        nyquist = self.fs / 2
        normalized_cutoff = cutoff / nyquist
        self.b, self.a = butter(self.order, normalized_cutoff, btype='high')
        return self.b, self.a
    
    def design_butterworth_bandpass(self, low: float, high: float) -> Tuple[np.ndarray, np.ndarray]:
        """Design Butterworth bandpass filter
        
        Args:
            low: Low cutoff frequency
            high: High cutoff frequency
        
        Returns:
            (Numerator, Denominator) coefficients
        """
        nyquist = self.fs / 2
        normalized_low = low / nyquist
        normalized_high = high / nyquist
        self.b, self.a = butter(self.order, [normalized_low, normalized_high], btype='band')
        return self.b, self.a
    
    def apply(self, signal: np.ndarray, zero_phase: bool = False) -> np.ndarray:
        """Apply filter to signal
        
        Args:
            signal: Input signal
            zero_phase: Use zero-phase filtering
        
        Returns:
            Filtered signal
        """
        if self.b is None or self.a is None:
            raise ValueError("Filter not designed yet")
        
        if zero_phase:
            return filtfilt(self.b, self.a, signal)
        else:
            return lfilter(self.b, self.a, signal)
