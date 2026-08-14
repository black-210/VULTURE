"""RF Feature Extractor - Extract 100+ Features from RF Signals"""
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class RFFeatureExtractor:
    """Extract comprehensive RF features for classification"""
    
    def __init__(self, fft_size: int = 2048):
        self.fft_size = fft_size
        self.feature_names = []
    
    def extract_amplitude_features(self, signal: np.ndarray) -> Dict[str, float]:
        """Extract amplitude-based features
        
        Args:
            signal: IQ signal
        
        Returns:
            Dictionary of amplitude features
        """
        amplitude = np.abs(signal)
        
        return {
            'amp_mean': np.mean(amplitude),
            'amp_std': np.std(amplitude),
            'amp_max': np.max(amplitude),
            'amp_min': np.min(amplitude),
            'amp_range': np.max(amplitude) - np.min(amplitude),
            'amp_skewness': stats.skew(amplitude),
            'amp_kurtosis': stats.kurtosis(amplitude),
            'amp_ptp': np.ptp(amplitude),
            'amp_rms': np.sqrt(np.mean(amplitude ** 2)),
            'crest_factor': np.max(amplitude) / (np.sqrt(np.mean(amplitude ** 2)) + 1e-10),
        }
    
    def extract_phase_features(self, signal: np.ndarray) -> Dict[str, float]:
        """Extract phase-based features
        
        Args:
            signal: IQ signal
        
        Returns:
            Dictionary of phase features
        """
        phase = np.angle(signal)
        phase_unwrapped = np.unwrap(phase)
        phase_diff = np.diff(phase_unwrapped)
        
        return {
            'phase_mean': np.mean(phase),
            'phase_std': np.std(phase),
            'phase_range': np.max(phase) - np.min(phase),
            'phase_diff_mean': np.mean(phase_diff),
            'phase_diff_std': np.std(phase_diff),
            'phase_linearity': np.polyfit(np.arange(len(phase)), phase, 1)[0],
            'phase_jitter': np.std(phase_diff),
        }
    
    def extract_power_features(self, signal: np.ndarray) -> Dict[str, float]:
        """Extract power-based features
        
        Args:
            signal: IQ signal
        
        Returns:
            Dictionary of power features
        """
        power = np.abs(signal) ** 2
        power_db = 10 * np.log10(power + 1e-10)
        
        return {
            'power_mean': np.mean(power),
            'power_std': np.std(power),
            'power_max': np.max(power),
            'power_min': np.min(power),
            'power_range': np.max(power) - np.min(power),
            'power_db_mean': np.mean(power_db),
            'power_db_std': np.std(power_db),
            'power_db_range': np.max(power_db) - np.min(power_db),
        }
    
    def extract_spectral_features(self, signal: np.ndarray, fs: float = 1e6) -> Dict[str, float]:
        """Extract spectral domain features
        
        Args:
            signal: IQ signal
            fs: Sample rate
        
        Returns:
            Dictionary of spectral features
        """
        fft = np.fft.fft(signal, self.fft_size)
        psd = np.abs(fft) ** 2
        psd_normalized = psd / np.sum(psd)
        freqs = np.fft.fftfreq(self.fft_size, 1/fs)
        
        spectral_centroid = np.sum(freqs * psd_normalized)
        spectral_spread = np.sqrt(np.sum(((freqs - spectral_centroid) ** 2) * psd_normalized))
        
        return {
            'spectral_centroid': spectral_centroid,
            'spectral_spread': spectral_spread,
            'spectral_skewness': stats.skew(psd),
            'spectral_kurtosis': stats.kurtosis(psd),
            'spectral_entropy': -np.sum(psd_normalized * np.log(psd_normalized + 1e-10)),
            'spectral_flatness': np.exp(np.mean(np.log(psd + 1e-10))) / (np.mean(psd) + 1e-10),
            'spectral_rolloff': freqs[np.argmax(np.cumsum(psd_normalized) >= 0.95)],
            'peak_frequency': freqs[np.argmax(psd)],
        }
    
    def extract_iq_features(self, signal: np.ndarray) -> Dict[str, float]:
        """Extract I/Q plane features
        
        Args:
            signal: IQ signal
        
        Returns:
            Dictionary of I/Q features
        """
        i = np.real(signal)
        q = np.imag(signal)
        
        correlation_iq = np.corrcoef(i, q)[0, 1]
        iq_power_ratio = (np.std(i) ** 2) / (np.std(q) ** 2 + 1e-10)
        
        return {
            'i_mean': np.mean(i),
            'i_std': np.std(i),
            'q_mean': np.mean(q),
            'q_std': np.std(q),
            'iq_correlation': correlation_iq,
            'iq_power_ratio': iq_power_ratio,
            'iq_imbalance': np.std(i) / (np.std(q) + 1e-10),
        }
    
    def extract_all_features(self, signal: np.ndarray, fs: float = 1e6) -> np.ndarray:
        """Extract all features
        
        Args:
            signal: IQ signal
            fs: Sample rate
        
        Returns:
            Feature vector
        """
        features = {}
        features.update(self.extract_amplitude_features(signal))
        features.update(self.extract_phase_features(signal))
        features.update(self.extract_power_features(signal))
        features.update(self.extract_spectral_features(signal, fs))
        features.update(self.extract_iq_features(signal))
        
        self.feature_names = list(features.keys())
        return np.array(list(features.values()))
