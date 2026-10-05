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
    def extract_features(self, data):
        features = {}
        features.update(FeatureEngineering.extract_statistical_features(data))
        features.update(FeatureEngineering.extract_spectral_features(data))
        features.update(FeatureEngineering.extract_temporal_features(data))
        return features
    def extract_features_from_iq(self, iq_data):
        return FeatureEngineering.extract_iq_features(iq_data)
    def extract_features_from_multiple_signals(self, signals):
        all_features = {}
        for idx, signal in enumerate(signals):
            all_features[f'signal_{idx}'] = self.extract_features(signal)
        return all_features
    def extract_features_from_multiple_iq_signals(self, iq_signals):
        all_features = {}
        for idx, iq_signal in enumerate(iq_signals):
            all_features[f'iq_signal_{idx}'] = self.extract_features_from_iq(iq_signal)
        return all_features
    def extract_features_with_custom_functions(self, data, custom_functions):
        features = {}
        for func in custom_functions:
            features.update(func(data))
        return features
    def extract_features_with_custom_functions_from_iq(self, iq_data, custom_functions):
        features = {}
        for func in custom_functions:
            features.update(func(iq_data))
        return features