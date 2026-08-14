"""FFT Engine - Fast Fourier Transform Analysis"""
import numpy as np
from scipy.fft import fft, ifft, fftfreq
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class FFTEngine:
    """FFT/IFFT analysis engine"""
    
    def __init__(self, sample_rate: float = 1e6):
        self.sample_rate = sample_rate
    
    def compute_fft(self, signal: np.ndarray, n: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Compute FFT
        
        Args:
            signal: Input signal
            n: FFT size
        
        Returns:
            Frequencies and FFT magnitude
        """
        if n is None:
            n = len(signal)
        
        fft_result = fft(signal, n=n)
        freqs = fftfreq(n, 1/self.sample_rate)
        magnitude = np.abs(fft_result)
        
        return freqs, magnitude
    
    def compute_ifft(self, fft_data: np.ndarray) -> np.ndarray:
        """Compute inverse FFT
        
        Args:
            fft_data: FFT data
        
        Returns:
            Time-domain signal
        """
        return np.real(ifft(fft_data))
    
    def zero_pad(self, signal: np.ndarray, target_size: int) -> np.ndarray:
        """Zero-pad signal
        
        Args:
            signal: Input signal
            target_size: Target size
        
        Returns:
            Zero-padded signal
        """
        if len(signal) >= target_size:
            return signal[:target_size]
        return np.pad(signal, (0, target_size - len(signal)), mode='constant')
    
    def apply_window(self, signal: np.ndarray, window_type: str = 'hann') -> np.ndarray:
        """Apply window function
        
        Args:
            signal: Input signal
            window_type: Window type
        
        Returns:
            Windowed signal
        """
        from scipy.signal import get_window
        window = get_window(window_type, len(signal))
        return signal * window
