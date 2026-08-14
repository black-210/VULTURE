"""Feature extraction for RF fingerprinting."""
import numpy as np
from scipy import signal, stats
import logging
logger = logging.getLogger(__name__)
class FeatureExtraction:
    @staticmethod
    def extract_iq_features(iq_data):
        features = {}
        features['amplitude_max'] = np.max(np.abs(iq_data))
        features['amplitude_min'] = np.min(np.abs(iq_data))
        features['amplitude_mean'] = np.mean(np.abs(iq_data))
        features['amplitude_std'] = np.std(np.abs(iq_data))
        features['phase_mean'] = np.mean(np.angle(iq_data))
        features['phase_std'] = np.std(np.angle(iq_data))
        features['i_mean'] = np.mean(np.real(iq_data))
        features['q_mean'] = np.mean(np.imag(iq_data))
        features['papr'] = np.max(np.abs(iq_data)**2) / np.mean(np.abs(iq_data)**2)
        return features
    @staticmethod
    def extract_spectral_features(iq_data, fs=1e6):
        freqs, psd = signal.welch(iq_data, fs=fs)
        features = {}
        features['spectral_centroid'] = np.sum(freqs * psd) / np.sum(psd)
        features['spectral_entropy'] = stats.entropy(psd)
        features['spectral_flatness'] = np.exp(np.mean(np.log(psd + 1e-10))) / (np.mean(psd) + 1e-10)
        return features
    @staticmethod
    def extract_crest_factor(iq_data):
        return np.max(np.abs(iq_data)) / np.sqrt(np.mean(np.abs(iq_data)**2))
    @staticmethod
    def extract_all_features(iq_data, fs=1e6):
        features = {}
        features.update(FeatureExtraction.extract_iq_features(iq_data))
        features.update(FeatureExtraction.extract_spectral_features(iq_data, fs))
        features['crest_factor'] = FeatureExtraction.extract_crest_factor(iq_data)
        return features