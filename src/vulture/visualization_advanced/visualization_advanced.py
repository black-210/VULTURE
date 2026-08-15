"""Visualization Advanced Framework - Complete Implementation"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
import logging

logger = logging.getLogger(__name__)


class SignalAnatomy:
    """Signal component analysis"""
    
    def decompose_signal(self, data, fs=1e6):
        """Decompose signal into components"""
        from scipy import signal as sp_signal
        
        components = {}
        
        # Time domain
        components['time_domain'] = {
            'mean': np.mean(np.abs(data)),
            'std': np.std(np.abs(data)),
            'max': np.max(np.abs(data)),
            'peak_to_avg': np.max(np.abs(data)) / (np.mean(np.abs(data)) + 1e-10)
        }
        
        # Frequency domain
        freqs, psd = sp_signal.welch(data, fs=fs)
        components['frequency_domain'] = {
            'centroid': np.sum(freqs * psd) / np.sum(psd),
            'entropy': -np.sum(psd * np.log2(psd + 1e-10))
        }
        
        # Envelope
        envelope = np.abs(sp_signal.hilbert(data))
        components['envelope'] = {
            'mean': np.mean(envelope),
            'variation': np.std(envelope) / (np.mean(envelope) + 1e-10)
        }
        
        # Phase
        phase = np.angle(sp_signal.hilbert(data))
        components['phase'] = {
            'linearity': self._phase_linearity(phase),
            'jitter': np.std(np.diff(phase))
        }
        
        return components
    
    @staticmethod
    def _phase_linearity(phase):
        """Measure phase linearity"""
        unwrapped = np.unwrap(phase)
        coeffs = np.polyfit(np.arange(len(unwrapped)), unwrapped, 1)
        fit = np.polyval(coeffs, np.arange(len(unwrapped)))
        residual = np.std(unwrapped - fit)
        return 1.0 / (1.0 + residual) if residual > 0 else 1.0


class Spectrogram3D:
    """3D Spectrogram visualization"""
    
    def __init__(self, figsize=(12, 8)):
        self.figsize = figsize
        self.fig = None
        self.ax = None
    
    def plot_3d_spectrogram(self, data, fs=1e6, nperseg=256):
        """Create 3D spectrogram"""
        from scipy import signal as sp_signal
        
        f, t, Sxx = sp_signal.spectrogram(data, fs=fs, nperseg=nperseg)
        
        self.fig = plt.figure(figsize=self.figsize)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Create mesh
        X, Y = np.meshgrid(t, f)
        Z = 10 * np.log10(Sxx + 1e-10)
        
        # Plot surface
        surf = self.ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
        
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Frequency (Hz)')
        self.ax.set_zlabel('Power (dB)')
        self.ax.set_title('3D Spectrogram')
        
        self.fig.colorbar(surf, ax=self.ax)
        
        return self.fig, self.ax


class ConstellationPlotter:
    """IQ Constellation diagram"""
    
    def __init__(self, figsize=(8, 8)):
        self.figsize = figsize
    
    def plot_constellation(self, iq_data, title='Constellation Diagram'):
        """Plot IQ constellation"""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        I = np.real(iq_data)
        Q = np.imag(iq_data)
        
        # Plot points
        ax.scatter(I, Q, alpha=0.5, s=10)
        
        # Statistics
        avg_power = np.mean(np.abs(iq_data)**2)
        evm = self._calculate_evm(iq_data)
        
        ax.set_xlabel('I (In-phase)')
        ax.set_ylabel('Q (Quadrature)')
        ax.set_title(f'{title}\nAvg Power: {avg_power:.2f}, EVM: {evm:.2f}%')
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        
        return fig, ax
    
    @staticmethod
    def _calculate_evm(iq_data):
        """Calculate Error Vector Magnitude"""
        # Simplified EVM calculation
        mean_power = np.mean(np.abs(iq_data)**2)
        symbol_error = np.std(np.abs(iq_data) - np.sqrt(mean_power))
        evm = (symbol_error / np.sqrt(mean_power)) * 100
        return evm


class SpectrumAnalyzerUI:
    """Interactive spectrum analyzer"""
    
    def __init__(self, figsize=(14, 6)):
        self.figsize = figsize
        self.data = None
        self.fs = None
    
    def plot_spectrum(self, data, fs=1e6, window='hann'):
        """Plot frequency spectrum with controls"""
        from scipy import signal as sp_signal
        
        self.data = data
        self.fs = fs
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize)
        
        # Linear spectrum
        freqs, psd = sp_signal.welch(data, fs=fs, window=window)
        ax1.plot(freqs, np.sqrt(psd))
        ax1.set_ylabel('Magnitude')
        ax1.set_title('Linear Spectrum')
        ax1.grid(True, alpha=0.3)
        
        # Log spectrum (dB)
        ax2.semilogy(freqs, 10 * np.log10(psd + 1e-10))
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Power (dB)')
        ax2.set_title('Power Spectral Density (Log Scale)')
        ax2.grid(True, alpha=0.3)
        
        return fig, (ax1, ax2)


class RealtimeDashboard:
    """Real-time monitoring dashboard"""
    
    def __init__(self, figsize=(16, 10)):
        self.figsize = figsize
        self.data_history = []
        self.timestamp = []
    
    def create_dashboard(self, data_dict):
        """Create real-time dashboard with multiple metrics"""
        fig = plt.figure(figsize=self.figsize)
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Time domain
        ax1 = fig.add_subplot(gs[0, :])
        if 'time_data' in data_dict:
            ax1.plot(data_dict['time_data'])
            ax1.set_title('Real-time Signal')
            ax1.grid(True, alpha=0.3)
        
        # Spectrum
        ax2 = fig.add_subplot(gs[1, 0])
        if 'spectrum' in data_dict:
            ax2.semilogy(data_dict['spectrum'])
            ax2.set_title('Spectrum')
            ax2.grid(True, alpha=0.3)
        
        # Spectrogram
        ax3 = fig.add_subplot(gs[1, 1])
        if 'spectrogram' in data_dict:
            im = ax3.imshow(data_dict['spectrogram'], aspect='auto', origin='lower')
            ax3.set_title('Spectrogram')
            fig.colorbar(im, ax=ax3)
        
        # Metrics
        ax4 = fig.add_subplot(gs[2, 0])
        ax4.axis('off')
        if 'metrics' in data_dict:
            metrics_text = '\n'.join([f"{k}: {v:.2f}" for k, v in data_dict['metrics'].items()])
            ax4.text(0.1, 0.5, metrics_text, fontsize=10, family='monospace')
        
        # Status
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.axis('off')
        if 'status' in data_dict:
            status_text = '\n'.join([f"{k}: {v}" for k, v in data_dict['status'].items()])
            ax5.text(0.1, 0.5, status_text, fontsize=10, family='monospace')
        
        return fig


class HeatmapGenerator:
    """Frequency/Time heatmap visualization"""
    
    def __init__(self, figsize=(14, 6)):
        self.figsize = figsize
    
    def generate_heatmap(self, data, fs=1e6, nperseg=256, cmap='jet'):
        """Generate frequency/time heatmap"""
        from scipy import signal as sp_signal
        
        f, t, Sxx = sp_signal.spectrogram(data, fs=fs, nperseg=nperseg)
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Power in dB
        power_db = 10 * np.log10(Sxx + 1e-10)
        
        # Plot heatmap
        im = ax.pcolormesh(t, f, power_db, shading='auto', cmap=cmap)
        
        ax.set_ylabel('Frequency (Hz)')
        ax.set_xlabel('Time (s)')
        ax.set_title('Frequency/Time Heatmap')
        
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label('Power (dB)')
        
        return fig, ax, im
    
    def add_annotations(self, ax, peaks, colors='red'):
        """Add peak annotations to heatmap"""
        for peak in peaks:
            time_idx, freq_idx = peak
            ax.plot(time_idx, freq_idx, 'x', color=colors, markersize=10)
        
        return ax


# Export classes
__all__ = [
    'SignalAnatomy',
    'Spectrogram3D',
    'ConstellationPlotter',
    'SpectrumAnalyzerUI',
    'RealtimeDashboard',
    'HeatmapGenerator'
]
