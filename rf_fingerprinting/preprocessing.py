"""IQ data preprocessing and normalization."""
import numpy as np
from scipy import signal
from typing import Tuple, Optional
from utils.logging import setup_logger

logger = setup_logger(__name__)

class Preprocessor:
    """Preprocess and normalize RF IQ data."""
    
    def __init__(self, sample_rate: float = 1e6):
        """Initialize preprocessor.
        
        Args:
            sample_rate: Sample rate in Hz.
        """
        self.sample_rate = sample_rate
    
    def normalize(self, data: np.ndarray) -> np.ndarray:
        """Normalize IQ data to [-1, 1] range.
        
        Args:
            data: Input IQ data.
        
        Returns:
            Normalized data.
        """
        if np.iscomplexobj(data):
            # For complex data, normalize by max magnitude
            max_val = np.max(np.abs(data))
            if max_val > 0:
                return data / max_val
            return data
        else:
            # For real data, use standard normalization
            data_mean = np.mean(data)
            data_std = np.std(data)
            if data_std > 0:
                return (data - data_mean) / data_std
            return data
    
    def decimate(self, data: np.ndarray, factor: int) -> np.ndarray:
        """Decimate signal by given factor.
        
        Args:
            data: Input signal.
            factor: Decimation factor.
        
        Returns:
            Decimated signal.
        """
        if factor <= 1:
            return data
        return signal.decimate(data, factor, zero_phase=True)
    
    def apply_window(self, data: np.ndarray, window_type: str = 'hann') -> np.ndarray:
        """Apply window function to data.
        
        Args:
            data: Input signal.
            window_type: Type of window ('hann', 'hamming', 'blackman', etc.).
        
        Returns:
            Windowed signal.
        """
        window = signal.get_window(window_type, len(data))
        return data * window
    
    def remove_dc(self, data: np.ndarray) -> np.ndarray:
        """Remove DC component from signal.
        
        Args:
            data: Input signal.
        
        Returns:
            Signal with DC removed.
        """
        if np.iscomplexobj(data):
            return data - np.mean(data)
        return data - np.mean(data)
    
    def filter_signal(self, data: np.ndarray, freq_low: float, freq_high: float, order: int = 5) -> np.ndarray:
        """Apply bandpass filter.
        
        Args:
            data: Input signal.
            freq_low: Low frequency cutoff (Hz).
            freq_high: High frequency cutoff (Hz).
            order: Filter order.
        
        Returns:
            Filtered signal.
        """
        nyquist = self.sample_rate / 2
        if freq_high >= nyquist:
            freq_high = nyquist * 0.99
        
        sos = signal.butter(order, [freq_low, freq_high], btype='band', fs=self.sample_rate, output='sos')
        return signal.sosfilt(sos, data)
    
    def preprocess(self, data: np.ndarray, normalize: bool = True, remove_dc: bool = True, 
                   window: bool = False, decimate_factor: int = 1) -> np.ndarray:
        """Apply full preprocessing pipeline.
        
        Args:
            data: Input IQ data.
            normalize: Whether to normalize data.
            remove_dc: Whether to remove DC component.
            window: Whether to apply window.
            decimate_factor: Decimation factor.
        
        Returns:
            Preprocessed data.
        """
        result = data.copy()
        
        if remove_dc:
            result = self.remove_dc(result)
        
        if window:
            result = self.apply_window(result)
        
        if decimate_factor > 1:
            result = self.decimate(result, decimate_factor)
        
        if normalize:
            result = self.normalize(result)
        
        return result
