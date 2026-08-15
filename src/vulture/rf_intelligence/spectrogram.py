"""Time-frequency analysis: Spectrograms with dB conversion and smoothing."""

import numpy as np
from scipy import signal
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class SpectrogramAnalyzer:
    """High-quality time-frequency spectrograms."""

    @staticmethod
    def compute(data: np.ndarray, fs: float = 1.0, nperseg: int = 256,
                noverlap: int = 128, cmap: str = 'viridis') -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Compute spectrogram.
        
        Args:
            data: Input signal
            fs: Sampling frequency
            nperseg: Segment length
            noverlap: Overlap length
            cmap: Colormap (for visualization)
            
        Returns:
            (times, frequencies, magnitude_db)
        """
        f, t, Sxx = signal.spectrogram(data, fs=fs, nperseg=nperseg, noverlap=noverlap)
        Sxx_db = 10 * np.log10(Sxx + 1e-12)
        return t, f, Sxx_db

    @staticmethod
    def compute_smooth(data: np.ndarray, fs: float = 1.0, nperseg: int = 256,
                       smooth_kernel: int = 3) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Compute spectrogram with smoothing.
        
        Args:
            data: Input signal
            fs: Sampling frequency
            nperseg: Segment length
            smooth_kernel: Kernel size for smoothing
            
        Returns:
            (times, frequencies, smoothed_magnitude_db)
        """
        t, f, Sxx_db = SpectrogramAnalyzer.compute(data, fs, nperseg)
        # Apply median filter for smoothing
        Sxx_smooth = signal.medfilt2d(Sxx_db, kernel_size=(smooth_kernel, smooth_kernel))
        return t, f, Sxx_smooth

    @staticmethod
    def extract_roi(data: np.ndarray, fs: float = 1.0, freq_start: float = 0,
                   freq_end: float = None, time_start: float = 0,
                   time_end: float = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Extract region of interest from spectrogram.
        
        Args:
            data: Input signal
            fs: Sampling frequency
            freq_start: Start frequency
            freq_end: End frequency
            time_start: Start time
            time_end: End time
            
        Returns:
            (times_roi, freqs_roi, Sxx_roi_db)
        """
        t, f, Sxx_db = SpectrogramAnalyzer.compute(data, fs)
        
        freq_mask = (f >= freq_start) & (f <= (freq_end or f.max()))
        time_mask = (t >= time_start) & (t <= (time_end or t.max()))
        
        return t[time_mask], f[freq_mask], Sxx_db[freq_mask][:, time_mask]
