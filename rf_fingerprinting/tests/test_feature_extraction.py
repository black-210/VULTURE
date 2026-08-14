"""Tests for feature extraction."""
import pytest
import numpy as np
from rf_fingerprinting.feature_extraction import FeatureExtractor


class TestFeatureExtractor:
    """Test feature extraction functions."""
    
    @pytest.fixture
    def extractor(self):
        return FeatureExtractor(n_features=64, fft_size=1024)
    
    @pytest.fixture
    def sample_signal(self):
        """Create sample IQ signal."""
        t = np.linspace(0, 1, 1000)
        i = np.sin(2 * np.pi * 100e3 * t)
        q = np.cos(2 * np.pi * 100e3 * t)
        return i + 1j * q
    
    def test_extract_statistical_features(self, extractor, sample_signal):
        """Test statistical feature extraction."""
        features = extractor.extract_statistical_features(sample_signal)
        assert len(features) > 0
        assert np.all(np.isfinite(features))
    
    def test_extract_spectral_features(self, extractor, sample_signal):
        """Test spectral feature extraction."""
        features = extractor.extract_spectral_features(sample_signal)
        assert len(features) > 0
        assert np.all(np.isfinite(features))
    
    def test_extract_iq_features(self, extractor, sample_signal):
        """Test IQ plane features."""
        features = extractor.extract_iq_features(sample_signal)
        assert len(features) > 0
        assert np.all(np.isfinite(features))
    
    def test_extract_all_features(self, extractor, sample_signal):
        """Test combined feature extraction."""
        features = extractor.extract_all_features(sample_signal)
        assert len(features) <= extractor.n_features
        assert np.all(np.isfinite(features))
    
    def test_fit_pca(self, extractor):
        """Test PCA fitting."""
        training_data = np.random.randn(100, 200)
        extractor.fit_pca(training_data)
        assert extractor.pca is not None
        assert extractor.pca.n_components_ == extractor.n_features


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
