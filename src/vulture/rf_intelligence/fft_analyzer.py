"""FFT Analysis module."""
import numpy as np
from scipy import signal
import logging

logger = logging.getLogger(__name__)

class FFTAnalyzer:
    """Fast Fourier Transform analysis."""
    def __init__(self, fft_size: int = 1024, window: str = 'hann'):
        self.fft_size = fft_size
        self.window_type = window
        self.window = signal.get_window(window, fft_size)
        logger.info(f"FFTAnalyzer initialized (size={fft_size}, window={window})")
    
    def compute_fft(self, data: np.ndarray):
        windowed = data[:self.fft_size] * self.window
        fft_result = np.fft.fft(windowed)
        magnitudes = np.abs(fft_result) / self.fft_size
        frequencies = np.fft.fftfreq(self.fft_size)
        return frequencies, magnitudes
    
    def compute_ifft(self, fft_data: np.ndarray):
        return np.fft.ifft(fft_data).real
    
    def zero_padding(self, data: np.ndarray, factor: int = 2):
        padded = np.pad(data, (0, len(data) * (factor - 1)))
        return padded
    
    def rfft(self, data: np.ndarray):
        windowed = data[:self.fft_size] * self.window
        fft_result = np.fft.rfft(windowed)
        magnitudes = np.abs(fft_result) / self.fft_size
        frequencies = np.fft.rfftfreq(self.fft_size)
        return frequencies, magnitudes