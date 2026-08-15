"""Time series forecasting."""

import numpy as np
from scipy import signal
from sklearn.linear_model import LinearRegression
import logging

logger = logging.getLogger(__name__)

class Forecasting:
    """Enterprise forecasting engine."""
    
    @staticmethod
    def arima_like(data, order=(1,0,1), forecast_steps=10):
        """Simplified ARIMA-like forecasting."""
        p, d, q = order
        
        # Differencing
        diff_data = data.copy()
        for _ in range(d):
            diff_data = np.diff(diff_data)
        
        # Simple AR(p) fitting
        X = np.column_stack([diff_data[i-p:i] for i in range(p, len(diff_data))])
        y = diff_data[p:]
        
        if len(X) > 0:
            model = LinearRegression()
            model.fit(X, y)
            
            # Forecast
            forecasts = []
            last_values = diff_data[-p:]
            
            for _ in range(forecast_steps):
                next_val = model.predict([last_values])[0]
                forecasts.append(next_val)
                last_values = np.append(last_values[1:], next_val)
            
            # Inverse differencing
            final_data = data.copy()
            for i in range(len(forecasts)):
                final_data = np.append(final_data, final_data[-1] + forecasts[i])
            
            return final_data[-forecast_steps:]
        return np.zeros(forecast_steps)
    
    @staticmethod
    def exponential_smoothing(data, alpha=0.3, forecast_steps=10):
        """Exponential smoothing."""
        smoothed = [data[0]]
        
        for i in range(1, len(data)):
            smoothed.append(alpha * data[i] + (1-alpha) * smoothed[i-1])
        
        forecasts = [smoothed[-1]] * forecast_steps
        return np.array(forecasts)
    
    @staticmethod
    def fourier_forecast(data, forecast_steps=10, n_harmonics=5):
        """Fourier series based forecasting."""
        # FFT
        fft_vals = np.fft.fft(data)
        freqs = np.fft.fftfreq(len(data))
        
        # Keep top harmonics
        top_indices = np.argsort(np.abs(fft_vals))[-n_harmonics:]
        
        # Reconstruct and forecast
        reconstructed = np.zeros(len(data) + forecast_steps, dtype=complex)
        for idx in top_indices:
            freq = freqs[idx]
            amp = fft_vals[idx]
            reconstructed += amp * np.exp(2j * np.pi * freq * np.arange(len(reconstructed)))
        
        return np.real(reconstructed[-forecast_steps:])
    
    @staticmethod
    def seasonal_decomposition(data, period=12):
        """Seasonal decomposition for forecasting."""
        # Trend
        trend = signal.savgol_filter(data, min(period*2-1, len(data)), 2)
        
        # Detrend
        detrended = data - trend
        
        # Seasonal
        seasonal = np.zeros_like(data)
        for i in range(period):
            seasonal[i::period] = np.mean(detrended[i::period])
        
        # Residual
        residual = data - trend - seasonal
        
        return {'trend': trend, 'seasonal': seasonal, 'residual': residual}