"""Feature engineering for ML."""
import numpy as np
from scipy import signal, stats
import logging
logger = logging.getLogger(__name__)
class FeatureEngineering:
    @staticmethod
    def extract_statistical_features(data):
        return {
            'mean': np.mean(data),
            'std': np.std(data),
            'max': np.max(data),
            'min': np.min(data),
            'median': np.median(data),
            'rms': np.sqrt(np.mean(data**2)),
            'skewness': stats.skew(data),
            'kurtosis': stats.kurtosis(data),
        }
    @staticmethod
    def extract_spectral_features(data, fs=1e6):
        freqs, psd = signal.welch(data, fs=fs)
        return {'spectral_centroid': np.sum(freqs * psd) / np.sum(psd), 'spectral_entropy': stats.entropy(psd)}
    @staticmethod
    def extract_temporal_features(data):
        return {'autocorrelation': np.correlate(data, data, mode='same')[len(data)//2], 'zero_crossing_rate': np.sum(np.diff(np.sign(data)) != 0) / len(data)}
    @staticmethod
    def extract_iq_features(iq_data):
        features = {}
        features.update(FeatureEngineering.extract_statistical_features(np.abs(iq_data)))
        features.update(FeatureEngineering.extract_spectral_features(iq_data))
        features['phase_deviation'] = np.std(np.angle(iq_data))
        return features