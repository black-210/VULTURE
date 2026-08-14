"""Spectrogram Generator - Time-Frequency Analysis"""
import numpy as np
from scipy.signal import spectrogram
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class SpectrogramGenerator:
    """Generate spectrograms for time-frequency analysis"""
    
    def __init__(self, sample_rate: float = 1e6):
        self.sample_rate = sample_rate
    
    def compute_spectrogram(self, signal: np.ndarray, nperseg: int = 256,
                           noverlap: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Compute spectrogram
        
        Args:
            signal: Input signal
            nperseg: Segment length
            noverlap: Overlap length
        
        Returns:
            Frequencies, times, and spectrogram
        """
        if noverlap is None:
            noverlap = nperseg // 2
        
        freqs, times, Sxx = spectrogram(signal, fs=self.sample_rate,
                                        nperseg=nperseg, noverlap=noverlap)
        return freqs, times, Sxx
    
    def compute_waterfall(self, signal: np.ndarray, frame_size: int = 1024,
                         hop_size: Optional[int] = None) -> np.ndarray:
        """Compute waterfall display data
        
        Args:
            signal: Input signal
            frame_size: FFT frame size
            hop_size: Hop size
        
        Returns:
            Waterfall matrix
        """
        if hop_size is None:
            hop_size = frame_size // 2
        
        num_frames = (len(signal) - frame_size) // hop_size + 1
        waterfall = np.zeros((num_frames, frame_size))
        
        for i in range(num_frames):
            frame = signal[i*hop_size:i*hop_size+frame_size]
            if len(frame) < frame_size:
                frame = np.pad(frame, (0, frame_size - len(frame)))
            waterfall[i] = np.abs(np.fft.fft(frame))
        
        return waterfall

from typing import Optional
