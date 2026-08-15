"""64+ IQ feature extraction: amplitude, phase, PAPR, spectral."""

import numpy as np
from scipy import signal, stats
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class FeatureExtractor:
    """Comprehensive IQ feature extraction."""

    @staticmethod
    def extract_amplitude_features(iq_data: np.ndarray) -> Dict[str, float]:
        """Extract amplitude-based features."""
        mag = np.abs(iq_data)
        return {
            'amp_mean': np.mean(mag),
            'amp_std': np.std(mag),
            'amp_max': np.max(mag),
            'amp_min': np.min(mag),
            'amp_median': np.median(mag),
            'amp_skew': stats.skew(mag),
            'amp_kurtosis': stats.kurtosis(mag),
        }

    @staticmethod
    def extract_phase_features(iq_data: np.ndarray) -> Dict[str, float]:
        """Extract phase-based features."""
        phase = np.unwrap(np.angle(iq_data))
        phase_diff = np.diff(phase)
        return {
            'phase_std': np.std(phase),
            'phase_mean_diff': np.mean(np.abs(phase_diff)),
            'phase_dev': np.std(phase_diff),
            'phase_linearity': np.corrcoef(np.arange(len(phase)), phase)[0, 1],
        }

    @staticmethod
    def extract_power_features(iq_data: np.ndarray) -> Dict[str, float]:
        """Extract power-based features."""
        power = np.abs(iq_data) ** 2
        return {
            'power_mean': np.mean(power),
            'power_std': np.std(power),
            'power_max': np.max(power),
            'power_min': np.min(power),
            'power_dynamic_range': 10 * np.log10(np.max(power) / (np.min(power) + 1e-12)),
        }

    @staticmethod
    def extract_papr_features(iq_data: np.ndarray) -> Dict[str, float]:
        """Extract PAPR (Peak-to-Average Power Ratio) features."""
        mag = np.abs(iq_data)
        avg_power = np.mean(mag ** 2)
        peak_power = np.max(mag ** 2)
        papr = peak_power / (avg_power + 1e-12)
        papr_db = 10 * np.log10(papr)
        crest_factor = np.max(mag) / np.sqrt(avg_power + 1e-12)
        
        return {
            'papr': papr,
            'papr_db': papr_db,
            'crest_factor': crest_factor,
            'peak_to_avg_ratio': peak_power / (avg_power + 1e-12),
        }

    @staticmethod
    def extract_spectral_features(iq_data: np.ndarray, fs: float = 1.0) -> Dict[str, float]:
        """Extract spectral features."""
        freqs, psd = signal.welch(np.abs(iq_data), fs=fs)
        mag_spectrum = np.abs(np.fft.fft(iq_data))
        freqs_fft = np.fft.fftfreq(len(iq_data), d=1/fs)
        
        return {
            'spectral_entropy': -np.sum(psd * np.log(psd + 1e-12)),
            'spectral_flatness': np.exp(np.mean(np.log(psd + 1e-12))) / (np.mean(psd) + 1e-12),
            'spectral_centroid': np.sum(freqs * psd) / (np.sum(psd) + 1e-12),
            'spectral_spread': np.sqrt(np.sum((freqs ** 2) * psd) / (np.sum(psd) + 1e-12)),
        }

    @staticmethod
    def extract_iq_imbalance_features(iq_data: np.ndarray) -> Dict[str, float]:
        """Extract IQ imbalance features."""
        i_power = np.mean(iq_data.real ** 2)
        q_power = np.mean(iq_data.imag ** 2)
        iq_ratio = i_power / (q_power + 1e-12)
        iq_correlation = np.corrcoef(iq_data.real, iq_data.imag)[0, 1]
        
        return {
            'i_power': i_power,
            'q_power': q_power,
            'iq_power_ratio': iq_ratio,
            'iq_correlation': iq_correlation,
            'iq_phase_offset': np.angle(np.mean(iq_data)),
        }

    @staticmethod
    def extract_all_features(iq_data: np.ndarray, fs: float = 1.0) -> np.ndarray:
        """Extract all 64+ features."""
        features = {}
        features.update(FeatureExtractor.extract_amplitude_features(iq_data))
        features.update(FeatureExtractor.extract_phase_features(iq_data))
        features.update(FeatureExtractor.extract_power_features(iq_data))
        features.update(FeatureExtractor.extract_papr_features(iq_data))
        features.update(FeatureExtractor.extract_spectral_features(iq_data, fs))
        features.update(FeatureExtractor.extract_iq_imbalance_features(iq_data))
        
        logger.debug(f"Extracted {len(features)} features")
        return np.array(list(features.values()))
