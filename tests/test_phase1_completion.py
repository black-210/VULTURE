"""Phase 1 Completion Tests"""
import pytest
import numpy as np
from src.vulture.timeseries_framework.timeseries_framework import (
    TimeseriesAnalyzer, AnomalyDetector, Forecasting, 
    TrendAnalyzer, SeasonalityDetector, WaveletAnalysis
)
from src.vulture.visualization_advanced.visualization_advanced import (
    SignalAnatomy, Spectrogram3D, ConstellationPlotter,
    SpectrumAnalyzerUI, RealtimeDashboard, HeatmapGenerator
)
from src.vulture.physics_laboratory.physics_laboratory import (
    Electromagnetic, LinkBudget, AntennaCalculator,
    PropagationModels, SignalPath, RadarSimulator
)

class TestTimeseriesFramework:
    """Test Timeseries Framework"""
    
    def test_decomposition(self):
        """Test time series decomposition"""
        analyzer = TimeseriesAnalyzer()
        data = np.sin(np.linspace(0, 4*np.pi, 1000)) + np.random.normal(0, 0.1, 1000)
        
        components = analyzer.decompose(data, period=100)
        
        assert 'trend' in components
        assert 'seasonal' in components
        assert 'residual' in components
        assert len(components['trend']) == len(data)
    
    def test_stationarity(self):
        """Test stationarity detection"""
        analyzer = TimeseriesAnalyzer()
        stationary_data = np.random.normal(0, 1, 1000)
        
        result = analyzer.stationarity_test(stationary_data)
        
        assert 'is_stationary' in result
        assert 'variance_ratio' in result
    
    def test_anomaly_detection_statistical(self):
        """Test statistical anomaly detection"""
        detector = AnomalyDetector(threshold=2.0)
        data = np.random.normal(0, 1, 1000)
        data[100:110] = 10  # Inject anomalies
        
        result = detector.detect_statistical(data)
        
        assert result['count'] > 0
        assert len(result['anomalies']) == len(data)
    
    def test_forecasting_arima(self):
        """Test ARIMA forecasting"""
        data = np.sin(np.linspace(0, 4*np.pi, 100))
        forecast = Forecasting.arima_simple(data, order=1, forecast_steps=10)
        
        assert len(forecast) == 10
        assert isinstance(forecast, np.ndarray)
    
    def test_trend_detection(self):
        """Test trend detection"""
        data = np.linspace(0, 10, 100) + np.random.normal(0, 0.5, 100)
        result = TrendAnalyzer.detect_trend(data)
        
        assert 'trend' in result
        assert result['direction'] in ['uptrend', 'downtrend']
        assert 0 <= result['strength'] <= 1
    
    def test_seasonality_detection(self):
        """Test seasonality detection"""
        # Create seasonal data
        t = np.arange(0, 100, 0.1)
        data = np.sin(2 * np.pi * t / 10) + np.random.normal(0, 0.1, len(t))
        
        result = SeasonalityDetector.detect_period(data, max_period=50)
        
        assert 'period' in result
        assert 'acf' in result

class TestVisualizationAdvanced:
    """Test Visualization Advanced Framework"""
    
    def test_signal_anatomy(self):
        """Test signal anatomy decomposition"""
        anatomy = SignalAnatomy()
        data = np.sin(2 * np.pi * 0.1 * np.arange(1000)) + np.random.normal(0, 0.1, 1000)
        
        components = anatomy.decompose_signal(data)
        
        assert 'time_domain' in components
        assert 'frequency_domain' in components
        assert 'envelope' in components
        assert 'phase' in components
    
    def test_constellation_plotter(self):
        """Test constellation plotter"""
        plotter = ConstellationPlotter()
        iq_data = np.exp(1j * 2 * np.pi * 0.1 * np.arange(1000))
        
        fig, ax = plotter.plot_constellation(iq_data)
        
        assert fig is not None
        assert ax is not None
    
    def test_spectrum_analyzer_ui(self):
        """Test spectrum analyzer UI"""
        analyzer = SpectrumAnalyzerUI()
        data = np.sin(2 * np.pi * 0.1 * np.arange(1000))
        
        fig, axes = analyzer.plot_spectrum(data)
        
        assert fig is not None
        assert len(axes) == 2

class TestPhysicsLaboratory:
    """Test Physics Laboratory Framework"""
    
    def test_electromagnetic_wavelength(self):
        """Test wavelength calculation"""
        frequency = 2.4e9  # 2.4 GHz
        wavelength = Electromagnetic.wavelength(frequency)
        
        assert wavelength > 0
        assert abs(wavelength - 0.125) < 0.01  # ~12.5 cm
    
    def test_link_budget(self):
        """Test link budget calculation"""
        result = LinkBudget.calculate_link_budget(
            tx_power_dbm=10,
            tx_gain_db=15,
            rx_gain_db=15,
            path_loss_db=110
        )
        
        assert 'received_power_dbm' in result
        assert 'link_margin_db' in result
    
    def test_antenna_gain(self):
        """Test antenna gain calculation"""
        gain = AntennaCalculator.isotropic_gain()
        assert gain['gain_db'] == 0
        
        dipole = AntennaCalculator.dipole_gain(2.4e9)
        assert dipole['gain_db'] > 0
    
    def test_path_loss(self):
        """Test free space path loss"""
        result = PropagationModels.free_space_path_loss(
            frequency=2.4e9,
            distance=100
        )
        
        assert result['path_loss_db'] > 0
    
    def test_radar_range(self):
        """Test radar range calculation"""
        result = RadarSimulator.calculate_radar_range(
            tx_power_dbm=20,
            frequency=10e9,
            antenna_gain_db=30,
            rcs_dbsm=10
        )
        
        assert result['max_range_m'] > 0
        assert result['max_range_km'] > 0
    
    def test_doppler_shift(self):
        """Test Doppler shift calculation"""
        result = RadarSimulator.doppler_shift(
            target_velocity_ms=100,
            frequency=10e9
        )
        
        assert result['doppler_shift_hz'] > 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
