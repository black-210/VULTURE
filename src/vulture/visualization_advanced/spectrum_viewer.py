"""Advanced spectrum viewer."""

import numpy as np
import logging

logger = logging.getLogger(__name__)

class SpectrumViewer:
    """Professional spectrum visualization."""
    
    def __init__(self, freq_range=(0, 1e9), resolution=1000):
        self.freq_range = freq_range
        self.resolution = resolution
        self.spectrum_history = []
        self.annotations = []
    
    def compute_spectrum(self, data, fs=1e6, method='welch', window='hann'):
        """Compute spectrum with multiple methods."""
        from scipy import signal
        
        if method == 'welch':
            freqs, psd = signal.welch(data, fs=fs, window=window)
        elif method == 'periodogram':
            freqs, psd = signal.periodogram(data, fs=fs)
        elif method == 'multitaper':
            from scipy.signal.windows import dpss
            tapers = dpss(len(data), 4, 8)
            psd_list = []
            for taper in tapers:
                windowed = data * taper
                fft_result = np.fft.fft(windowed)
                psd_list.append(np.abs(fft_result)**2)
            psd = np.mean(psd_list, axis=0)
            freqs = np.fft.fftfreq(len(data), 1/fs)
        else:
            freqs, psd = signal.welch(data, fs=fs)
        
        self.spectrum_history.append({'freqs': freqs, 'psd': 10*np.log10(psd + 1e-10)})
        return freqs, 10*np.log10(psd + 1e-10)
    
    def add_annotation(self, frequency, label, marker_type='marker'):
        """Add annotation to spectrum."""
        self.annotations.append({
            'frequency': frequency,
            'label': label,
            'marker_type': marker_type
        })
    
    def detect_peaks(self, psd, threshold_db=10):
        """Detect spectral peaks."""
        from scipy import signal
        threshold_linear = 10**(threshold_db/10)
        psd_linear = 10**(psd/10)
        peaks, _ = signal.find_peaks(psd_linear, height=np.max(psd_linear)*0.3)
        return peaks
    
    def get_spectrogram_data(self, data, fs=1e6):
        """Get spectrogram for visualization."""
        from scipy import signal
        f, t, Sxx = signal.spectrogram(data, fs=fs)
        return t, f, 10*np.log10(Sxx + 1e-10)