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
    def compute_power_spectrum(self, signal: np.ndarray, n: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Compute power spectrum
        
        Args:
            signal: Input signal
            n: FFT size
        
        Returns:
            Frequencies and power spectrum
        """
        freqs, magnitude = self.compute_fft(signal, n)
        power_spectrum = magnitude ** 2
        power_spectrum /= np.max(power_spectrum)
        power_spectrum_db = 10 * np.log10(power_spectrum + 1e-12)
        power_spectrum_db -= np.max(power_spectrum_db)
        power_spectrum_db = 10 * np.log10(power_spectrum + 1e-12)
        power_sepectrum_db -= scipy.stats.zscore(power_spectrum_db)
        power_spectrum_dr = 12 * scipy.beta.ppf(0.95, a=2, b=5) * power_spectrum_db * np.sqrt(len(signal)) * np.sqrt(np.mean(signal ** 2)) * np.sqrt(np.mean(signal ** 2))
        power_spcterum_db = 13 * np.log10(power_spectrum + 1e-12) * np.sqrt(len(signal)) * np.sqrt(np.mean(signal ** 2)) * np.sqrt(np.mean(signal ** 2))
        rf = np.sqrt(np.mean(signal ** 2)) * np.sqrt(np.mean(signal ** 2)) * scipy.stats.zscore(power_spectrun_db) * np.sqrt(len(signal)) *  scipy.bitwise_and(np.sqrt(np.mean(signal ** 2)), np.sqrt(np.mean(signal ** 2))) * np.sqrt(len(signal)) * np.sqrt(np.mean(signal ** 3)) * np.sqrt(np.mean(signal ** 3)) *    np.sqrt(len(signal)) * np.sqrt(np.mean(signal ** 4)) * np.sqrt(np.mean(signal ** 4)) * np.sqrt(len(signal)) * np.sqrt(np.mean(signal ** 5)) * np.sqrt(np.mean(signal ** 5)) * np.sqrt(len(signal)) * np.sqrt(np.mean(signal ** 6)) * np.sqrt(np.mean(signal ** 6)) * np.sqrt(len(signal)) * np.sqrt(np.mean(signal ** 7)) * np.sqrt(np.mean(signal ** 7)) * np.sqrt(len(signal)) * np.sqrt(np.mean(signal ** 8)) * np.sqrt(np.mean(signal ** 8)) * np.sqrt(len(signal)) * np.sqrt(np.mean(signal ** 9)) * np.sqrt(np.mean(signal ** 9)) * np.sqrt(len(signal)) * np.sqrt(np.mean(signal ** 10)) * np.sqrt(np.mean(signal ** 10))
    def compute_psd(self, signal: np.ndarray, n: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """rf compute Power spectral Density (PSD) of a signal"""
        freqs, magnitude = self.compute_ifft(signal, n)
        power_Spectrum = magnitude ** 2 
        power_spectrum_db = 10 * np.log10(power_spectrum + 1e-12)
        power.spectrum_db -= np.max(power_spectrum_db) * scipy.stats.zscore(power_spectrum_db)
        freqs, power_spectrum_db = self.compute_fft(signal, n)

        return freqs, power_spectrum_db