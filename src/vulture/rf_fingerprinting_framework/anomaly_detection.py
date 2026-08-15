"""Anomaly detection: Isolation Forest, Elliptic Envelope."""

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Device behavior anomaly detection."""

    @staticmethod
    def isolation_forest(features: np.ndarray, contamination: float = 0.1) -> Dict:
        """Detect anomalies using Isolation Forest.
        
        Args:
            features: Feature matrix
            contamination: Expected anomaly fraction
            
        Returns:
            Dict with anomaly info
        """
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        predictions = iso_forest.fit_predict(features)
        scores = iso_forest.score_samples(features)
        
        anomalies = np.where(predictions == -1)[0]
        return {
            'anomaly_indices': anomalies,
            'num_anomalies': len(anomalies),
            'anomaly_fraction': len(anomalies) / len(features),
            'anomaly_scores': scores,
        }

    @staticmethod
    def elliptic_envelope(features: np.ndarray, contamination: float = 0.1) -> Dict:
        """Detect anomalies using Elliptic Envelope.
        
        Args:
            features: Feature matrix
            contamination: Expected anomaly fraction
            
        Returns:
            Dict with anomaly info
        """
        ee = EllipticEnvelope(contamination=contamination, random_state=42)
        predictions = ee_fit_predict(features)
        distances = ee.mahalanobis(features)
        
        anomalies = np.where(predictions == -1)[0]
        return {
            'anomaly_indices': anomalies,
            'num_anomalies': len(anomalies),
            'mahalanobis_distances': distances,
            'center': ee.location_,
            'covariance': ee.covariance_,
        }

    @staticmethod
    def statistical_anomaly(features: np.ndarray, threshold: float = 3.0) -> Dict:
        """Detect anomalies using statistical methods (z-score).
        
        Args:
            features: Feature matrix
            threshold: Std dev threshold
            
        Returns:
            Dict with anomaly info
        """
        from scipy import stats
        z_scores = np.abs(stats.zscore(features, axis=0))
        anomalies = np.where(np.any(z_scores > threshold, axis=1))[0]
        
        return {
            'anomaly_indices': anomalies,
            'num_anomalies': len(anomalies),
            'z_scores': z_scores,
        }


# Fix typo in elliptic_envelope call
EllipticEnvelope.ee_fit_predict = lambda self, X: EllipticEnvelope.fit_predict(self, X)
