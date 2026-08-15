"""Enterprise test suite for VULTURE."""

import pytest
import numpy as np
from scipy import signal

class TestTimeSeriesFramework:
    def test_timeseries_stats(self, sample_signal):
        from vulture.timeseries_framework import TimeSeriesEngine
        engine = TimeSeriesEngine()
        engine.add_data(sample_signal)
        stats = engine.get_statistics()
        assert 'mean' in stats
        assert 'std' in stats
        assert stats['mean'] > 0
    
    def test_multi_resolution(self, sample_signal):
        from vulture.timeseries_framework import TimeSeriesEngine
        engine = TimeSeriesEngine(buffer_size=len(sample_signal))
        engine.add_data(sample_signal)
        resolutions = engine.multi_resolution_analysis(levels=3)
        assert len(resolutions) == 3
    
    def test_trend_decomposition(self, sample_signal):
        from vulture.timeseries_framework import TimeSeriesEngine
        engine = TimeSeriesEngine(buffer_size=len(sample_signal))
        engine.add_data(sample_signal)
        decomp = engine.trend_decomposition()
        assert 'trend' in decomp
        assert 'seasonal' in decomp
        assert 'residual' in decomp

class TestProtocolsFramework:
    def test_modulation_features(self, qpsk_signal):
        from vulture.protocols_framework import ModulationClassifier
        features = ModulationClassifier.extract_modulation_features(qpsk_signal)
        assert 'amp_mean' in features
        assert 'phase_mean' in features
        assert 'spectral_centroid' in features
    
    def test_packet_detection(self):
        from vulture.protocols_framework import PacketAnalyzer
        analyzer = PacketAnalyzer()
        data = np.concatenate([np.ones(100), np.zeros(100), np.ones(100)])
        packets = analyzer.detect_packets(data, threshold=0.5)
        assert len(packets) >= 1

class TestVisualizationFramework:
    def test_spectrum_computation(self, sample_signal):
        from vulture.visualization_advanced import SpectrumViewer
        viewer = SpectrumViewer()
        freqs, psd = viewer.compute_spectrum(sample_signal, method='welch')
        assert len(freqs) > 0
        assert len(psd) > 0
    
    def test_constellation_analysis(self, qpsk_signal):
        from vulture.visualization_advanced import IQConstellation
        const = IQConstellation()
        i_vals, q_vals = const.plot_constellation(qpsk_signal)
        assert len(i_vals) == len(qpsk_signal)
        assert len(q_vals) == len(qpsk_signal)