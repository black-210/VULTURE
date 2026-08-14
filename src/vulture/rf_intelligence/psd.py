"""Power Spectral Density computation."""
import numpy as np
from scipy import signal
import logging

logger = logging.getLogger(__name__)

class PowerSpectralDensity:
    """PSD computation methods."""
    
    @staticmethod
    def welch(data, fs=1e6, window_size=1024, overlap=0.5):
        nperseg = window_size
        noverlap = int(window_size * overlap)
        frequencies, psd = signal.welch(data, fs=fs, nperseg=nperseg, noverlap=noverlap, scaling='density')
        return frequencies, psd
    
    @staticmethod
    def periodogram(data, fs=1e6):
        frequencies, psd = signal.periodogram(data, fs=fs, scaling='density')
        return frequencies, psd
    
    @staticmethod
    def lombscargle(times, data, frequencies):
        angular_freq = 2.0 * np.pi * frequencies
        psd = signal.lombscargle(times, data, angular_freq, normalize=True)
        return frequencies, psd
    
    @staticmethod
    def multitaper(data, fs=1e6, window_size=1024):
        from scipy.signal.windows import dpss
        tapers = dpss(window_size, 4, 8)
        psd_list = []
        for taper in tapers:
            windowed = data[:window_size] * taper
            fft_result = np.fft.fft(windowed)
            psd_list.append(np.abs(fft_result) ** 2)
        psd = np.mean(psd_list, axis=0)
        frequencies = np.fft.fftfreq(window_size, 1/fs)
        return frequencies, psd