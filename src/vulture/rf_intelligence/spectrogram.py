"""Spectrogram generation."""
import numpy as np
from scipy import signal
import logging

logger = logging.getLogger(__name__)

class Spectrogram:
    """Spectrogram methods."""
    
    @staticmethod
    def compute(data, fs=1e6, window_size=256, overlap=0.75):
        nperseg = window_size
        noverlap = int(window_size * overlap)
        frequencies, times, Sxx = signal.spectrogram(data, fs=fs, nperseg=nperseg, noverlap=noverlap)
        return times, frequencies, Sxx
    
    @staticmethod
    def to_db(data, reference=1.0):
        return 10 * np.log10(data / reference + 1e-10)
    
    @staticmethod
    def to_linear(data_db):
        return 10 ** (data_db / 10.0)
    
    @staticmethod
    def normalize(data):
        return (data - np.min(data)) / (np.max(data) - np.min(data) + 1e-10)
    
    @staticmethod
    def smooth(data, window_size=5):
        return signal.savgol_filter(data, min(window_size, len(data) if len(data) % 2 == 1 else len(data)-1), 2)