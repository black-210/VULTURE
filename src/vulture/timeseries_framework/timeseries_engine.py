"""Advanced time series engine with multi-resolution analysis."""

import numpy as np
from scipy import signal, stats
import logging

logger = logging.getLogger(__name__)

class TimeSeriesEngine:
    """Enterprise-grade time series processing."""
    
    def __init__(self, sample_rate=1e6, buffer_size=10000):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.buffer = np.zeros(buffer_size, dtype=np.complex128)
        self.position = 0
        self.stats = {'min': np.inf, 'max': -np.inf, 'mean': 0, 'std': 0}
    
    def add_data(self, data):
        """Add data with circular buffer."""
        data = np.asarray(data)
        n = len(data)
        if self.position + n <= self.buffer_size:
            self.buffer[self.position:self.position+n] = data
            self.position += n
        else:
            remaining = self.buffer_size - self.position
            self.buffer[self.position:] = data[:remaining]
            self.buffer[:n-remaining] = data[remaining:]
            self.position = n - remaining
        self._update_stats()
    
    def _update_stats(self):
        """Update running statistics."""
        filled = self.buffer[:self.position] if self.position > 0 else self.buffer
        self.stats['min'] = np.min(np.abs(filled))
        self.stats['max'] = np.max(np.abs(filled))
        self.stats['mean'] = np.mean(np.abs(filled))
        self.stats['std'] = np.std(np.abs(filled))
    
    def get_statistics(self):
        """Get current statistics."""
        return self.stats.copy()
    
    def multi_resolution_analysis(self, levels=5):
        """Wavelet-based multi-resolution."""
        filled = self.buffer[:self.position]
        resolutions = []
        for level in range(1, levels+1):
            decimated = signal.decimate(filled, min(2**level, len(filled)), zero_phase=True)
            resolutions.append(decimated)
        return resolutions
    
    def trend_decomposition(self):
        """STL-like decomposition."""
        filled = np.abs(self.buffer[:self.position])
        if len(filled) < 10:
            return None
        window = max(3, len(filled)//10)
        if window % 2 == 0:
            window += 1
        trend = signal.savgol_filter(filled, window, 2)
        seasonal = signal.savgol_filter(filled - trend, window//2 if window//2 % 2 else window//2+1, 1)
        residual = filled - trend - seasonal
        return {'trend': trend, 'seasonal': seasonal, 'residual': residual}
    
    def detect_patterns(self, pattern_length=100):
        """Motif discovery."""
        filled = np.abs(self.buffer[:self.position])
        if len(filled) < pattern_length * 2:
            return []
        patterns = []
        for i in range(0, len(filled)-pattern_length, pattern_length//2):
            pattern = filled[i:i+pattern_length]
            corr = np.correlate(filled, pattern, mode='valid')
            matches = np.where(corr > np.max(corr) * 0.8)[0]
            if len(matches) > 1:
                patterns.append({'position': i, 'matches': matches})
        return patterns