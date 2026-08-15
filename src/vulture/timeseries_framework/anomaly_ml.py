"""Machine learning for anomaly detection."""

import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)

class AnomalyML:
    """ML-based anomaly detection."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = IsolationForest(contamination=0.05)
        self.is_trained = False
    
    def train(self, X):
        """Train anomaly detector."""
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        self.is_trained = True
        logger.info("Anomaly model trained")
    
    def predict(self, X):
        """Detect anomalies."""
        if not self.is_trained:
            return None
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        scores = self.model.score_samples(X_scaled)
        return predictions, scores
    
    def contextual_anomalies(self, data, context_window=5):
        """Detect contextual anomalies."""
        anomalies = []
        for i in range(context_window, len(data)-context_window):
            window = data[i-context_window:i+context_window]
            local_mean = np.mean(window)
            local_std = np.std(window)
            if np.abs(data[i] - local_mean) > 3 * local_std:
                anomalies.append(i)
        return anomalies
    
    def collective_anomalies(self, data, window_size=20):
        """Detect collective (subsequence) anomalies."""
        anomalous_windows = []
        global_mean = np.mean(data)
        global_std = np.std(data)
        
        for i in range(0, len(data)-window_size, window_size//2):
            window = data[i:i+window_size]
            window_mean = np.mean(window)
            if np.abs(window_mean - global_mean) > 2 * global_std:
                anomalous_windows.append((i, i+window_size))
        
        return anomalous_windows