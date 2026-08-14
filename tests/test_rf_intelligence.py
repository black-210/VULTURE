"""Tests for RF Intelligence Framework."""
import pytest
import numpy as np
from vulture.rf_intelligence import FFTAnalyzer, PeakDetector, Spectrogram

class TestFFTAnalyzer:
    def test_fft_computation(self):
        analyzer = FFTAnalyzer(fft_size=1024)
        data = np.sin(2 * np.pi * 0.1 * np.arange(1024))
        freqs, mags = analyzer.compute_fft(data)
        assert len(freqs) == 1024
        assert len(mags) == 1024
    
    def test_ifft_reconstruction(self):
        analyzer = FFTAnalyzer()
        data = np.sin(2 * np.pi * 0.1 * np.arange(1024))
        freqs, mags = analyzer.compute_fft(data)
        fft_result = np.fft.fft(data)
        reconstructed = analyzer.compute_ifft(fft_result)
        assert np.allclose(reconstructed, data[:len(reconstructed)], atol=1e-2)

class TestPeakDetector:
    def test_peak_detection(self):
        detector = PeakDetector()
        data = np.array([1, 5, 2, 8, 3, 7, 1])
        peaks, _ = detector.find_peaks(data)
        assert len(peaks) > 0

class TestSpectrogram:
    def test_spectrogram_computation(self):
        data = np.sin(2 * np.pi * 0.1 * np.arange(2000))
        times, freqs, Sxx = Spectrogram.compute(data)
        assert len(times) > 0
        assert len(freqs) > 0
        assert Sxx.shape[0] == len(freqs)
