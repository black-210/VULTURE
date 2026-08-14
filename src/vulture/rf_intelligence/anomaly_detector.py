"""Anomaly detection in RF signals."""
import numpy as np
from scipy import signal
import logging

logger = logging.getLogger(__name__)

class AnomalyDetector:
    """Anomaly detection methods."""
    
    @staticmethod
    def detect_interference(psd, frequencies, threshold_multiplier=5.0):
        noise_floor = np.percentile(psd, 20)
        threshold = noise_floor * threshold_multiplier
        anomalies = []
        for i, power in enumerate(psd):
            if power > threshold:
                anomalies.append((frequencies[i], power))
        return anomalies
    
    @staticmethod
    def detect_burst(data, fs=1e6, threshold=3.0):
        envelope = np.abs(signal.hilbert(data))
        mean = np.mean(envelope)
        std = np.std(envelope)
        burst_threshold = mean + threshold * std
        bursts = []
        in_burst = False
        start_idx = 0
        for i, amp in enumerate(envelope):
            if amp > burst_threshold and not in_burst:
                in_burst = True
                start_idx = i
            elif amp <= burst_threshold and in_burst:
                in_burst = False
                duration = (i - start_idx) / fs
                bursts.append((start_idx / fs, i / fs, duration))
        return bursts
    
    @staticmethod
    def isolation_forest_detection(data, contamination=0.1):
        from sklearn.ensemble import IsolationForest
        X = data.reshape(-1, 1)
        clf = IsolationForest(contamination=contamination)
        return clf.fit_predict(X)