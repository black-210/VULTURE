"""Anomaly Detector - Signal Anomaly Detection"""
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Tuple, np.ndarray
import logging

logger = logging.getLogger(__name__)

class AnomalyDetector:
    """Detect anomalies in RF signals"""
    
    def __init__(self, contamination: float = 0.1):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_fitted = False
    
    def fit(self, features: np.ndarray) -> 'AnomalyDetector':
        """Fit anomaly detector
        
        Args:
            features: Feature matrix
        
        Returns:
            Self
        """
        self.model.fit(features)
        self.is_fitted = True
        return self
    
    def detect(self, features: np.ndarray) -> np.ndarray:
        """Detect anomalies
        
        Args:
            features: Feature matrix
        
        Returns:
            Anomaly labels (-1 for anomaly, 1 for normal)
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted")
        return self.model.predict(features)
    
    def get_anomaly_scores(self, features: np.ndarray) -> np.ndarray:
        """Get anomaly scores
        
        Args:
            features: Feature matrix
        
        Returns:
            Anomaly scores
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted")
        return self.model.score_samples(features)
