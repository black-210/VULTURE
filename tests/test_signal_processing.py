"""Tests for Signal Processing Framework."""
import pytest
import numpy as np
from vulture.signal_processing import FIRFilter, IIRFilter, Correlation

class TestFIRFilter:
    def test_fir_filter_application(self):
        fir = FIRFilter(numtaps=51, cutoff=0.5, filter_type='low')
        data = np.random.randn(1000)
        filtered = fir.apply(data)
        assert len(filtered) == len(data)

class TestIIRFilter:
    def test_iir_filter_application(self):
        iir = IIRFilter(order=4, cutoff=0.5, filter_type='low')
        data = np.random.randn(1000)
        filtered = iir.apply(data)
        assert len(filtered) == len(data)

class TestCorrelation:
    def test_auto_correlation(self):
        data = np.sin(2 * np.pi * 0.1 * np.arange(100))
        corr = Correlation.auto_correlation(data)
        assert len(corr) == 2 * len(data) - 1
