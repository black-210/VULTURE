"""Modulation classification."""

import numpy as np
from scipy import signal
import logging

logger = logging.getLogger(__name__)

class ModulationClassifier:
    """Classify modulation schemes."""
    
    MODULATIONS = ['BPSK', 'QPSK', 'PSK8', 'QAM16', 'QAM64', 'FSK', 'ASK', 'OOK']
    
    @staticmethod
    def extract_modulation_features(iq_data):
        """Extract features for modulation classification."""
        features = {}
        
        # Amplitude statistics
        amplitude = np.abs(iq_data)
        features['amp_mean'] = np.mean(amplitude)
        features['amp_std'] = np.std(amplitude)
        features['amp_max'] = np.max(amplitude)
        
        # Phase statistics
        phase = np.angle(iq_data)
        phase_diff = np.diff(phase)
        features['phase_mean'] = np.mean(np.abs(phase_diff))
        features['phase_std'] = np.std(phase_diff)
        
        # Spectral features
        freqs, psd = signal.welch(iq_data)
        features['spectral_centroid'] = np.sum(freqs * psd) / np.sum(psd)
        features['spectral_entropy'] = -np.sum(psd * np.log2(psd + 1e-10))
        
        # Constellation features
        features['const_std'] = np.std(np.abs(iq_data))
        
        return features
    
    @staticmethod
    def classify_modulation(iq_data):
        """Classify modulation type."""
        features = ModulationClassifier.extract_modulation_features(iq_data)
        
        amp_std = features['amp_std']
        phase_std = features['phase_std']
        amp_max = features['amp_max']
        
        # Simple heuristic classifier
        if amp_std < 0.1:
            return 'PSK'
        elif phase_std < 0.5:
            return 'QAM'
        elif amp_max / np.mean(np.abs(iq_data)) > 2:
            return 'FSK'
        else:
            return 'UNKNOWN'
    
    @staticmethod
    def estimate_symbol_rate(iq_data, fs=1e6):
        """Estimate symbol rate."""
        # Autocorrelation method
        autocorr = np.correlate(np.abs(iq_data), np.abs(iq_data), mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        
        # Find peaks
        peaks, _ = signal.find_peaks(autocorr[1:], height=np.max(autocorr)*0.3)
        
        if len(peaks) > 0:
            symbol_period = peaks[0] + 1
            symbol_rate = fs / symbol_period
            return symbol_rate
        return None