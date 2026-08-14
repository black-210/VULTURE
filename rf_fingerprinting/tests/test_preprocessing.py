"""Tests for signal preprocessing."""
import pytest
import numpy as np
from rf_fingerprinting.preprocessing import Preprocessor


class TestPreprocessor:
    """Test preprocessing functions."""
    
    @pytest.fixture
    def preprocessor(self):
        return Preprocessor(sample_rate=1e6)
    
    @pytest.fixture
    def sample_signal(self):
        """Create sample IQ signal."""
        t = np.linspace(0, 1, 1000)
        i = np.sin(2 * np.pi * 100e3 * t)
        q = np.cos(2 * np.pi * 100e3 * t)
        return i + 1j * q
    
    def test_normalize_complex(self, preprocessor, sample_signal):
        """Test normalization of complex signal."""
        normalized = preprocessor.normalize(sample_signal)
        assert np.max(np.abs(normalized)) <= 1.0 + 1e-6
    
    def test_normalize_real(self, preprocessor):
        """Test normalization of real signal."""
        signal = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        normalized = preprocessor.normalize(signal)
        assert np.abs(np.mean(normalized)) < 1e-6
    
    def test_remove_dc(self, preprocessor, sample_signal):
        """Test DC removal."""
        signal_with_dc = sample_signal + (1 + 1j)
        clean_signal = preprocessor.remove_dc(signal_with_dc)
        dc_value = np.mean(clean_signal)
        assert np.abs(dc_value) < 1e-6
    
    def test_apply_window(self, preprocessor, sample_signal):
        """Test window application."""
        windowed = preprocessor.apply_window(sample_signal, 'hann')
        assert len(windowed) == len(sample_signal)
        # Edges should be attenuated
        assert np.abs(windowed[0]) < np.abs(sample_signal[0])
    
    def test_decimate(self, preprocessor):
        """Test decimation."""
        signal = np.sin(2 * np.pi * np.arange(1000) / 1000)
        decimated = preprocessor.decimate(signal, 10)
        assert len(decimated) < len(signal)
    
    def test_preprocess_pipeline(self, preprocessor, sample_signal):
        """Test full preprocessing pipeline."""
        result = preprocessor.preprocess(
            sample_signal,
            normalize=True,
            remove_dc=True,
            window=True,
            decimate_factor=2
        )
        assert len(result) <= len(sample_signal)
        assert result.dtype in [np.complex64, np.complex128]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
