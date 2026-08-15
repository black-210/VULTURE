"""Real-time signal processing engine."""

import numpy as np
from scipy import signal
from collections import deque
import threading
import logging

logger = logging.getLogger(__name__)

class RealtimeProcessor:
    """High-performance real-time processing."""
    
    def __init__(self, window_size=1024, update_rate=1000):
        self.window_size = window_size
        self.update_rate = update_rate
        self.buffer = deque(maxlen=window_size)
        self.results = {}
        self.lock = threading.Lock()
    
    def process_stream(self, data_stream, callback=None):
        """Process streaming data."""
        for sample in data_stream:
            with self.lock:
                self.buffer.append(sample)
                if len(self.buffer) == self.window_size:
                    result = self._compute_features(np.array(self.buffer))
                    self.results = result
                    if callback:
                        callback(result)
    
    def _compute_features(self, window):
        """Fast feature computation."""
        return {
            'power': np.mean(np.abs(window)**2),
            'peak': np.max(np.abs(window)),
            'crest': np.max(np.abs(window)) / np.sqrt(np.mean(np.abs(window)**2)),
            'rms': np.sqrt(np.mean(np.abs(window)**2)),
        }
    
    def get_latest_results(self):
        """Thread-safe result retrieval."""
        with self.lock:
            return self.results.copy()
    
    def adaptive_filter(self, signal_data, reference, mu=0.01):
        """LMS adaptive filter."""
        y = np.zeros_like(signal_data)
        w = np.zeros(len(reference))
        
        for n in range(len(signal_data)):
            y[n] = np.dot(w, reference)
            e = signal_data[n] - y[n]
            w = w + mu * e * reference
        
        return y, w
    
    def kalman_filter(self, measurements, process_variance, measurement_variance):
        """Kalman filter estimation."""
        estimates = []
        p = 1.0
        x = 0.0
        
        for z in measurements:
            p = p + process_variance
            k = p / (p + measurement_variance)
            x = x + k * (z - x)
            p = (1 - k) * p
            estimates.append(x)
        
        return np.array(estimates)