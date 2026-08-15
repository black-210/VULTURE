"""Test suite: RF Intelligence, ML, Signal Processing."""

import pytest
import numpy as np
from scipy import signal


class TestRFIntelligence:
    """RF Intelligence tests."""

    @pytest.fixture
    def sample_signal(self):
        """Generate test signal."""
        fs = 1000
        t = np.arange(0, 1, 1/fs)
        return np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 150 * t)

    def test_fft_analyzer(self, sample_signal):
        """Test FFT analysis."""
        from vulture.rf_intelligence import FFTAnalyzer
        analyzer = FFTAnalyzer(fft_size=1024)
        freqs, mags = analyzer.compute_fft(sample_signal)
        assert len(freqs) == len(mags)
        assert np.max(mags) > 0

    def test_psd_welch(self, sample_signal):
        """Test Welch PSD."""
        from vulture.rf_intelligence import PSDAnalyzer
        freqs, psd = PSDAnalyzer.welch(sample_signal, fs=1000)
        assert len(freqs) == len(psd)
        assert np.all(psd >= 0)

    def test_peak_detection(self, sample_signal):
        """Test peak detection."""
        from vulture.rf_intelligence import PeakDetector
        freqs, psd = signal.welch(sample_signal, fs=1000)
        peaks, props = PeakDetector.find_peaks(psd, prominence=0.5)
        assert len(peaks) >= 2  # Should find 50Hz and 150Hz peaks

    def test_spectrogram(self, sample_signal):
        """Test spectrogram."""
        from vulture.rf_intelligence import SpectrogramAnalyzer
        t, f, Sxx = SpectrogramAnalyzer.compute(sample_signal, fs=1000)
        assert Sxx.shape[0] == len(f)
        assert Sxx.shape[1] == len(t)


class TestMLFramework:
    """Machine Learning tests."""

    @pytest.fixture
    def synthetic_data(self):
        """Generate synthetic ML data."""
        np.random.seed(42)
        X = np.random.randn(100, 10)
        y = (X[:, 0] + X[:, 1] > 0).astype(int)
        return X, y

    def test_preprocessing_normalize(self, synthetic_data):
        """Test data normalization."""
        from vulture.ml_framework import Preprocessing
        X, y = synthetic_data
        X_norm = Preprocessing.normalize(X, method='standard')
        assert np.abs(np.mean(X_norm)) < 1e-6
        assert np.abs(np.std(X_norm) - 1.0) < 1e-6

    def test_feature_extraction(self, synthetic_data):
        """Test feature extraction."""
        from vulture.ml_framework import FeatureEngineering
        X, _ = synthetic_data
        features = FeatureEngineering.extract_statistical_features(X[0])
        assert 'mean' in features
        assert 'std' in features
        assert len(features) > 0

    def test_model_training(self, synthetic_data):
        """Test model training."""
        from vulture.ml_framework import ModelTrainer
        X, y = synthetic_data
        trainer = ModelTrainer(model_type='rf', task='classification', n_estimators=10)
        trainer.train(X, y)
        assert trainer.is_trained
        predictions = trainer.predict(X[:5])
        assert len(predictions) == 5

    def test_evaluation_metrics(self, synthetic_data):
        """Test evaluation metrics."""
        from vulture.ml_framework import ModelTrainer, Evaluation
        X, y = synthetic_data
        trainer = ModelTrainer(model_type='rf')
        trainer.train(X, y)
        predictions = trainer.predict(X)
        metrics = Evaluation.compute_metrics(y, predictions, task='classification')
        assert 'accuracy' in metrics
        assert 'f1' in metrics
        assert 0 <= metrics['accuracy'] <= 1


class TestSignalProcessing:
    """Signal Processing tests."""

    @pytest.fixture
    def test_signal(self):
        """Generate test signal."""
        return np.random.randn(1000)

    def test_fir_filter(self, test_signal):
        """Test FIR filter."""
        from vulture.signal_processing import Filters
        b = Filters.design_fir(order=64, cutoff=0.2)
        filtered = Filters.apply_fir(test_signal, b)
        assert len(filtered) == len(test_signal)

    def test_correlation(self, test_signal):
        """Test correlation."""
        from vulture.signal_processing import CorrelationEngine
        corr, lags = CorrelationEngine.acorr(test_signal, mode='same')
        assert len(corr) == len(test_signal)
        assert corr[len(corr)//2] > np.max(corr[10:50])  # Center should be max

    def test_matched_filter(self, test_signal):
        """Test matched filtering."""
        from vulture.signal_processing import MatchedFilter
        template = test_signal[:100]
        output, normalized = MatchedFilter.filter(test_signal, template)
        assert len(output) == len(test_signal)


class TestRFFingerprinting:
    """RF Fingerprinting tests."""

    @pytest.fixture
    def iq_data(self):
        """Generate IQ data."""
        return np.exp(1j * 2 * np.pi * 0.1 * np.arange(10000))

    def test_feature_extraction(self, iq_data):
        """Test IQ feature extraction."""
        from vulture.rf_fingerprinting_framework import FeatureExtractor
        features = FeatureExtractor.extract_all_features(iq_data)
        assert len(features) > 0
        assert np.all(np.isfinite(features))

    def test_device_classification(self, iq_data):
        """Test device classification."""
        from vulture.rf_fingerprinting_framework import FeatureExtractor, DeviceClassifier
        # Generate training data
        X_train = np.vstack([FeatureExtractor.extract_all_features(iq_data) for _ in range(50)])
        y_train = np.repeat([0, 1], 25)
        
        clf = DeviceClassifier(model_type='svm')
        clf.train(X_train, y_train)
        predictions = clf.predict(X_train[:5])
        assert len(predictions) == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
