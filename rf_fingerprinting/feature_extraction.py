"""Feature extraction from RF IQ signals."""
import numpy as np
from scipy import stats
from sklearn.decomposition import PCA
from typing import Dict, Tuple
from utils.logging import setup_logger

logger = setup_logger(__name__)

class FeatureExtractor:
    """Extract features from RF signals for classification."""
    
    def __init__(self, n_features: int = 64, fft_size: int = 1024):
        """Initialize feature extractor.
        
        Args:
            n_features: Number of output features after dimensionality reduction.
            fft_size: FFT size for spectral analysis.
        """
        self.n_features = n_features
        self.fft_size = fft_size
        self.pca = None
    
    def extract_statistical_features(self, data: np.ndarray) -> np.ndarray:
        """Extract statistical features from signal.
        
        Args:
            data: Input IQ data.
        
        Returns:
            Statistical feature vector.
        """
        features = []
        
        # Basic statistics
        features.append(np.mean(np.abs(data)))
        features.append(np.std(np.abs(data)))
        features.append(np.max(np.abs(data)))
        features.append(np.min(np.abs(data)))
        
        # Power statistics
        power = np.abs(data) ** 2
        features.append(np.mean(power))
        features.append(np.std(power))
        
        # Amplitude statistics
        if np.iscomplexobj(data):
            i_component = np.real(data)
            q_component = np.imag(data)
            features.extend([
                np.mean(i_component),
                np.std(i_component),
                np.mean(q_component),
                np.std(q_component),
            ])
        
        # Crest factor
        features.append(np.max(np.abs(data)) / (np.sqrt(np.mean(power)) + 1e-10))
        
        # Skewness and Kurtosis
        if len(data) > 1:
            features.append(stats.skew(np.abs(data)))
            features.append(stats.kurtosis(np.abs(data)))
        
        return np.array(features)
    
    def extract_spectral_features(self, data: np.ndarray) -> np.ndarray:
        """Extract frequency domain features.
        
        Args:
            data: Input IQ data.
        
        Returns:
            Spectral feature vector.
        """
        # Compute power spectral density
        freqs, psd = self._compute_psd(data)
        
        # Normalize PSD
        psd = psd / (np.sum(psd) + 1e-10)
        
        # Spectral centroid
        spectral_centroid = np.sum(freqs * psd)
        
        # Spectral spread
        spectral_spread = np.sqrt(np.sum(((freqs - spectral_centroid) ** 2) * psd))
        
        # Spectral rolloff (95% of energy)
        cumsum = np.cumsum(psd)
        spectral_rolloff = freqs[np.argmax(cumsum >= 0.95)]
        
        # Peak frequency
        peak_freq = freqs[np.argmax(psd)]
        
        # Spectral flatness (Wiener entropy)
        spectral_flatness = np.exp(np.mean(np.log(psd + 1e-10))) / (np.mean(psd) + 1e-10)
        
        features = np.array([
            spectral_centroid,
            spectral_spread,
            spectral_rolloff,
            peak_freq,
            spectral_flatness,
        ])
        
        # Add top PSD bins
        top_psd_features = np.sort(psd)[-10:]
        features = np.concatenate([features, top_psd_features])
        
        return features
    
    def extract_iq_features(self, data: np.ndarray) -> np.ndarray:
        """Extract IQ plane features.
        
        Args:
            data: Input IQ data.
        
        Returns:
            IQ feature vector.
        """
        if not np.iscomplexobj(data):
            return np.array([])
        
        i_component = np.real(data)
        q_component = np.imag(data)
        
        # Correlation between I and Q
        correlation = np.corrcoef(i_component, q_component)[0, 1]
        
        # Phase features
        phase = np.angle(data)
        phase_diff = np.diff(phase)
        
        features = np.array([
            correlation,
            np.mean(phase),
            np.std(phase),
            np.mean(np.abs(phase_diff)),
            np.std(np.abs(phase_diff)),
        ])
        
        return features
    
    def _compute_psd(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute power spectral density using Welch method.
        
        Args:
            data: Input signal.
        
        Returns:
            Tuple of (frequencies, power spectral density).
        """
        freqs, psd = np.fft.welch(data, fs=1.0, nperseg=min(len(data), self.fft_size))
        return freqs, psd
    
    def extract_all_features(self, data: np.ndarray) -> np.ndarray:
        """Extract all features and apply dimensionality reduction.
        
        Args:
            data: Input IQ data.
        
        Returns:
            Reduced feature vector.
        """
        # Extract different feature types
        stat_features = self.extract_statistical_features(data)
        spec_features = self.extract_spectral_features(data)
        iq_features = self.extract_iq_features(data)
        
        # Combine features
        all_features = np.concatenate([
            stat_features,
            spec_features,
            iq_features,
        ])
        
        # Apply PCA if needed
        if len(all_features) > self.n_features:
            if self.pca is None:
                self.pca = PCA(n_components=self.n_features)
                return self.pca.fit_transform(all_features.reshape(1, -1))[0]
            else:
                return self.pca.transform(all_features.reshape(1, -1))[0]
        
        return all_features[:self.n_features]
    
    def fit_pca(self, training_data: np.ndarray) -> None:
        """Fit PCA on training data.
        
        Args:
            training_data: Training data matrix (n_samples, n_features).
        """
        self.pca = PCA(n_components=self.n_features)
        self.pca.fit(training_data)
        logger.info(f"PCA fitted with {self.n_features} components")
