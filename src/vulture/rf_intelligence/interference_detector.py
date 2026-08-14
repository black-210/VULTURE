"""Interference detection and characterization."""
import numpy as np
from scipy import signal
import logging

logger = logging.getLogger(__name__)

class InterferenceDetector:
    """Interference detection methods."""
    
    @staticmethod
    def detect_cw_interference(psd, frequencies, threshold_db=10):
        psd_db = 10 * np.log10(psd + 1e-10)
        baseline = np.percentile(psd_db, 30)
        threshold = baseline + threshold_db
        cw_indices = np.where(psd_db > threshold)[0]
        return frequencies[cw_indices]
    
    @staticmethod
    def detect_chirp(data, fs):
        f0, f1, t1 = 0, fs/2, len(data)/fs
        instantaneous_freq = signal.instantaneous_frequency(data, fs)
        return instantaneous_freq
    
    @staticmethod
    def detect_pulse_train(data, fs, min_pulse_width=1e-6):
        envelope = np.abs(signal.hilbert(data))
        threshold = np.mean(envelope) + 2*np.std(envelope)
        pulses = []
        in_pulse = False
        start_idx = 0
        for i, amp in enumerate(envelope):
            if amp > threshold and not in_pulse:
                in_pulse = True
                start_idx = i
            elif amp <= threshold and in_pulse:
                pulse_width = (i - start_idx) / fs
                if pulse_width >= min_pulse_width:
                    pulses.append((start_idx/fs, i/fs, pulse_width))
                in_pulse = False
        return pulses