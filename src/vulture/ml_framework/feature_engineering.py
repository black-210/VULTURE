"""Feature engineering: Statistical, spectral, temporal, IQ features."""

import numpy as np
from scipy import signal, stats
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class FeatureEngineering:
    """Advanced feature extraction."""

    @staticmethod
    def extract_statistical_features(data: np.ndarray) -> Dict[str, float]:
        """Extract statistical features.
        
        Args:
            data: Input signal
            
        Returns:
            Dict of features
        """
        return {
            'mean': np.mean(data),
            'std': np.std(data),
            'max': np.max(data),
            'min': np.min(data),
            'median': np.median(data),
            'skew': stats.skew(data),
            'kurtosis': stats.kurtosis(data),
            'energy': np.sum(data ** 2),
            'power': np.mean(data ** 2),
            'range': np.max(data) - np.min(data),
        }

    @staticmethod
    def extract_spectral_features(data: np.ndarray, fs: float = 1.0) -> Dict[str, float]:
        """Extract spectral features.
        
        Args:
            data: Input signal
            fs: Sampling frequency
            
        Returns:
            Dict of spectral features
        """
        freqs, psd = signal.welch(data, fs=fs)
        
        return {
            'spectral_centroid': np.sum(freqs * psd) / np.sum(psd),
            'spectral_spread': np.sqrt(np.sum((freqs - np.sum(freqs * psd) / np.sum(psd)) ** 2 * psd) / np.sum(psd)),
            'spectral_entropy': -np.sum(psd * np.log(psd + 1e-12)),
            'spectral_flatness': np.exp(np.mean(np.log(psd + 1e-12))) / (np.mean(psd) + 1e-12),
            'spectral_rolloff': freqs[np.where(np.cumsum(psd) >= 0.85 * np.sum(psd))[0][0]],
        }

    @staticmethod
    def extract_temporal_features(data: np.ndarray) -> Dict[str, float]:
        """Extract temporal features.
        
        Args:
            data: Input signal
            
        Returns:
            Dict of temporal features
        """
        diff = np.diff(data)
        return {
            'zero_crossing_rate': np.sum(np.diff(np.sign(data)) != 0) / len(data),
            'mean_absolute_difference': np.mean(np.abs(diff)),
            'mean_square_difference': np.mean(diff ** 2),
            'autocorr_lag1': np.corrcoef(data[:-1], data[1:])[0, 1],
        }

    @staticmethod
    def extract_iq_features(iq_data: np.ndarray) -> Dict[str, float]:
        """Extract IQ-specific features.
        
        Args:
            iq_data: Complex IQ signal
            
        Returns:
            Dict of IQ features
        """
        magnitude = np.abs(iq_data)
        phase = np.angle(iq_data)
        
        return {
            'magnitude_mean': np.mean(magnitude),
            'magnitude_std': np.std(magnitude),
            'magnitude_max': np.max(magnitude),
            'phase_std': np.std(phase),
            'papr': np.max(magnitude ** 2) / np.mean(magnitude ** 2),  # Peak-to-avg power ratio
            'crest_factor': np.max(magnitude) / np.sqrt(np.mean(magnitude ** 2)),
            'i_power': np.mean(iq_data.real ** 2),
            'q_power': np.mean(iq_data.imag ** 2),
            'i_q_correlation': np.corrcoef(iq_data.real, iq_data.imag)[0, 1],
        }

    @staticmethod
    def extract_all_features(data: np.ndarray, fs: float = 1.0,
                            iq: bool = True) -> np.ndarray:
        """Extract all feature types.
        
        Args:
            data: Input signal
            fs: Sampling frequency
            iq: Whether data is complex IQ
            
        Returns:
            Feature vector
        """
        features = {}
        
        if iq and np.iscomplexobj(data):
            features.update(FeatureEngineering.extract_iq_features(data))
            features.update(FeatureEngineering.extract_spectral_features(np.abs(data), fs))
        else:
            features.update(FeatureEngineering.extract_statistical_features(data))
            features.update(FeatureEngineering.extract_spectral_features(data, fs))
            features.update(FeatureEngineering.extract_temporal_features(data))
        
        return np.array(list(features.values()))
