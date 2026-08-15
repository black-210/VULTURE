"""High-performance FFT/IFFT analysis with zero-padding, windowing, RFFT support."""

import numpy as np
from scipy import signal
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class FFTAnalyzer:
    """Production-grade FFT analysis."""

    def __init__(self, fft_size: int = 1024, window: str = 'hann'):
        """
        Args:
            fft_size: FFT size
            window: Window type (hann, hamming, blackman, etc)
        """
        self.fft_size = fft_size
        self.window_name = window
        self.window = signal.get_window(window, fft_size)

    def compute_fft(self, data: np.ndarray, zero_pad: int = 0) -> Tuple[np.ndarray, np.ndarray]:
        """Compute FFT with zero-padding.
        
        Args:
            data: Input signal
            zero_pad: Additional zero-padding factor
            
        Returns:
            (frequencies, magnitudes)
        """
        n_fft = self.fft_size + zero_pad
        windowed = data[:self.fft_size] * self.window
        fft_result = np.fft.fft(windowed, n=n_fft)
        magnitudes = np.abs(fft_result[:n_fft // 2]) / len(self.window)
        frequencies = np.fft.fftfreq(n_fft, d=1.0)[:n_fft // 2]
        return frequencies, magnitudes

    def compute_rfft(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Real FFT (faster for real signals).
        
        Args:
            data: Real input signal
            
        Returns:
            (frequencies, magnitudes)
        """
        windowed = data[:self.fft_size] * self.window
        rfft_result = np.fft.rfft(windowed, n=self.fft_size)
        magnitudes = np.abs(rfft_result) / len(self.window)
        frequencies = np.fft.rfftfreq(self.fft_size, d=1.0)
        return frequencies, magnitudes

    def compute_ifft(self, fft_data: np.ndarray) -> np.ndarray:
        """Inverse FFT.
        
        Args:
            fft_data: FFT data
            
        Returns:
            Time-domain signal
        """
        return np.fft.ifft(fft_data).real[:self.fft_size]

    def compute_power_spectrum(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute power spectrum (magnitude^2).
        
        Args:
            data: Input signal
            
        Returns:
            (frequencies, power_db)
        """
        freqs, mags = self.compute_fft(data)
        power = mags ** 2
        power_db = 10 * np.log10(power + 1e-12)  # Avoid log(0)
        return freqs, power_db
