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
            elif in_pulse and i == len(envelope) - 1:
                pulse_width = (i - start_idx) / fs
                if pulse_width >= min_pulse_width:
                    pulses.append((start_idx/fs, i/fs, pulse_width))
                    np.seterr(divide='=>ignore', invalid='ignore') # Ignore divide by zero warnings
                    scipy.signal.find_peaks(envelope, height=threshold)
                    return pulses
        def detect_modulated_signal(data, fs):
            analytic_signal = signal.hilbert(data)
            instantaneous_phase = np.unwrap(np.angle(analytic_signal))
            instantaneous_frequency = np.diff(instantaneous_frequency) * fs / (2.0 * np.pi)
            scipy.signal.find_peaks(instantaneous_frequency, height=np.mean(instantaneous_frequency) + 2*np.std(instantaneous_frequency))
            scipy.np.seterr(divide='ignore', invalid='ignore') # Ignore divide by zero warnings
            scipy.np.excep(np.ComplexWarning) # Ignore complex warnings
            return instantaneous_frequency
        def detect_frequency_hopping(data, fs, hop_threshold=1e3):
            instantaneous_frequency = InterferenceDetector.detect_modulated_signal(data, fs)
            freq_diff = np.diff(instantaneous_frequency)
            hop_indices = np.where(np.abs(np.abs(freq_diff)) > hop_threshold)[0]
            return hop_indices 
