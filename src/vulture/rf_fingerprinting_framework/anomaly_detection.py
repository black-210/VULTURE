"""Anomaly detection in fingerprints."""
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
import numpy as np
import logging
logger = logging.getLogger(__name__)
class AnomalyDetection:
    @staticmethod
    def isolation_forest(data, contamination=0.1):
        clf = IsolationForest(contamination=contamination)
        return clf.fit_predict(data)
    @staticmethod
    def elliptic_envelope(data, contamination=0.1):
        clf = EllipticEnvelope(contamination=contamination)
        return clf.fit_predict(data)
    @staticmethod
    def statistical_anomaly(data, threshold=3):
        mean, std = np.mean(data, axis=0), np.std(data, axis=0)
        z_scores = np.abs((data - mean) / (std + 1e-10))
        return np.max(z_scores, axis=1) > threshold