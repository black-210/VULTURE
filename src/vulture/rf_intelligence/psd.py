"""Multi-method PSD: Welch, Periodogram, Lombscargle, Multitaper."""

import numpy as np
from scipy import signal
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class PSDAnalyzer:
    """Production-grade power spectral density computation."""

    @staticmethod
    def welch(data: np.ndarray, fs: float = 1.0, nperseg: int = 256, 
              noverlap: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Welch's method (preferred for noisy signals).
        
        Args:
            data: Input signal
            fs: Sampling frequency
            nperseg: Segment length
            noverlap: Overlap length
            
        Returns:
            (frequencies, psd_db)
        """
        if noverlap is None:
            noverlap = nperseg // 2
        freqs, psd = signal.welch(data, fs=fs, nperseg=nperseg, noverlap=noverlap)
        psd_db = 10 * np.log10(psd + 1e-12)
        return freqs, psd_db

    @staticmethod
    def periodogram(data: np.ndarray, fs: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """Periodogram method.
        
        Args:
            data: Input signal
            fs: Sampling frequency
            
        Returns:
            (frequencies, psd_db)
        """
        freqs, psd = signal.periodogram(data, fs=fs)
        psd_db = 10 * np.log10(psd + 1e-12)
        return freqs, psd_db

    @staticmethod
    def multitaper(data: np.ndarray, fs: float = 1.0, NW: float = 4) -> Tuple[np.ndarray, np.ndarray]:
        """Multitaper method (high resolution, low bias).
        
        Args:
            data: Input signal
            fs: Sampling frequency
            NW: Time-bandwidth product (3-4 typical)
            
        Returns:
            (frequencies, psd_db)
        """
        from scipy.signal.windows import dpss
        N = len(data)
        tapers = dpss(N, NW, 2*NW-1)
        psd_list = []
        for taper in tapers:
            windowed = data * taper
            freqs, psd = signal.periodogram(windowed, fs=fs)
            psd_list.append(psd)
        psd_avg = np.mean(psd_list, axis=0)
        psd_db = 10 * np.log10(psd_avg + 1e-12)
        return freqs, psd_db

    @staticmethod
    def lombscargle(time: np.ndarray, data: np.ndarray, fs: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """Lomb-Scargle for unevenly sampled data.
        
        Args:
            time: Time values
            data: Signal values
            fs: Average sampling frequency
            
        Returns:
            (frequencies, psd_db)
        """
        freqs = np.fft.fftfreq(len(data), d=1/fs)[:len(data)//2]
        psd = signal.lombscargle(time, data, 2*np.pi*freqs)
        psd_db = 10 * np.log10(psd + 1e-12)
        return freqs, psd_db
