"""Anomaly detection: Interference, burst detection, Isolation Forest."""

import numpy as np
from scipy import signal
from sklearn.ensemble import IsolationForest
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """RF anomaly detection."""

    @staticmethod
    def detect_bursts(signal_iq: np.ndarray, window_size: int = 100,
                      threshold_std: float = 3.0) -> List[Tuple[int, int]]:
        """Detect signal bursts using moving average.
        
        Args:
            signal_iq: Complex IQ signal
            window_size: Moving window size
            threshold_std: Std dev threshold
            
        Returns:
            List of (start, end) burst indices
        """
        power = np.abs(signal_iq) ** 2
        moving_avg = signal.savgol_filter(power, min(window_size, len(power)-1), 1)
        moving_std = signal.savgol_filter(np.abs(power - moving_avg), min(window_size, len(power)-1), 1)
        
        threshold = moving_avg + threshold_std * (moving_std + 1e-6)
        bursts = power > threshold
        
        # Find burst edges
        transitions = np.diff(bursts.astype(int))
        starts = np.where(transitions == 1)[0]
        ends = np.where(transitions == -1)[0] + 1
        
        return list(zip(starts, ends))

    @staticmethod
    def isolation_forest(feature_matrix: np.ndarray, contamination: float = 0.1) -> np.ndarray:
        """Detect anomalies using Isolation Forest.
        
        Args:
            feature_matrix: Feature matrix (n_samples, n_features)
            contamination: Expected proportion of anomalies
            
        Returns:
            Anomaly labels (-1 for anomaly, 1 for normal)
        """
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        return iso_forest.fit_predict(feature_matrix)

    @staticmethod
    def detect_interference(power_db: np.ndarray, freqs: np.ndarray,
                           threshold_db: float = 20) -> Dict:
        """Detect interference signatures.
        
        Args:
            power_db: Power spectrum in dB
            freqs: Frequency array
            threshold_db: Interference threshold above noise
            
        Returns:
            Dict with interference info
        """
        noise_floor = np.percentile(power_db, 10)
        interference_level = noise_floor + threshold_db
        interference_mask = power_db > interference_level
        
        return {
            'num_interference_bins': np.sum(interference_mask),
            'max_interference_db': np.max(power_db),
            'interference_bandwidth': np.sum(interference_mask) * (freqs[1] - freqs[0]),
            'center_freq': freqs[np.argmax(power_db)],
        }
