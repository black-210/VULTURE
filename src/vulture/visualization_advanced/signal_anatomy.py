"""Signal anatomy dissection."""

import numpy as np
import logging

logger = logging.getLogger(__name__)

class SignalAnatomy:
    """Detailed signal component analysis."""
    
    def __init__(self):
        self.components = {}
    
    def decompose_signal(self, data, fs=1e6):
        """Decompose signal into components."""
        from scipy import signal
        
        components = {}
        
        # Time domain
        components['time_domain'] = {
            'mean': np.mean(np.abs(data)),
            'std': np.std(np.abs(data)),
            'max': np.max(np.abs(data)),
            'peak_to_avg': np.max(np.abs(data)) / np.mean(np.abs(data))
        }
        
        # Frequency domain
        freqs, psd = signal.welch(data, fs=fs)
        components['frequency_domain'] = {
            'centroid': np.sum(freqs * psd) / np.sum(psd),
            'entropy': -np.sum(psd * np.log2(psd + 1e-10))
        }
        
        # Envelope
        envelope = np.abs(signal.hilbert(data))
        components['envelope'] = {
            'mean': np.mean(envelope),
            'variation': np.std(envelope) / np.mean(envelope)
        }
        
        # Phase
        phase = np.angle(signal.hilbert(data))
        components['phase'] = {
            'linearity': self._phase_linearity(phase),
            'jitter': np.std(np.diff(phase))
        }
        
        self.components = components
        return components
    
    @staticmethod
    def _phase_linearity(phase):
        """Measure phase linearity."""
        # Unwrap phase
        unwrapped = np.unwrap(phase)
        # Fit line
        coeffs = np.polyfit(np.arange(len(unwrapped)), unwrapped, 1)
        fit = np.polyval(coeffs, np.arange(len(unwrapped)))
        residual = np.std(unwrapped - fit)
        return 1.0 / (1.0 + residual) if residual > 0 else 1.0