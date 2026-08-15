"""CW, chirp, and pulse train interference classification."""

import numpy as np
from scipy import signal
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class InterferenceDetector:
    """Classify interference types."""

    @staticmethod
    def detect_cw(power_db: np.ndarray, freqs: np.ndarray, threshold_factor: float = 1.5) -> Dict:
        """Detect continuous wave (CW) interference.
        
        Args:
            power_db: Power spectrum in dB
            freqs: Frequency array
            threshold_factor: Peak prominence threshold
            
        Returns:
            Dict with CW detection results
        """
        noise_floor = np.percentile(power_db, 10)
        peaks, props = signal.find_peaks(power_db, height=noise_floor + threshold_factor,
                                        prominence=2.0, distance=5)
        
        is_cw = len(peaks) > 0
        return {
            'is_cw': is_cw,
            'num_peaks': len(peaks),
            'peak_freqs': freqs[peaks] if len(peaks) > 0 else [],
            'peak_powers_db': power_db[peaks] if len(peaks) > 0 else [],
        }

    @staticmethod
    def detect_chirp(signal_iq: np.ndarray, fs: float = 1.0) -> Dict:
        """Detect chirp (frequency sweep) interference.
        
        Args:
            signal_iq: Complex IQ signal
            fs: Sampling frequency
            
        Returns:
            Dict with chirp detection results
        """
        # Compute instantaneous frequency
        analytic = signal.hilbert(signal_iq)
        phase = np.unwrap(np.angle(analytic))
        inst_freq = np.diff(phase) / (2 * np.pi) * fs
        
        freq_change = np.max(inst_freq) - np.min(inst_freq)
        is_chirp = freq_change > fs * 0.01  # More than 1% bandwidth change
        
        return {
            'is_chirp': is_chirp,
            'freq_change': freq_change,
            'inst_freq_min': np.min(inst_freq),
            'inst_freq_max': np.max(inst_freq),
        }

    @staticmethod
    def detect_pulse_train(signal_iq: np.ndarray, window_size: int = 100) -> Dict:
        """Detect pulse train interference.
        
        Args:
            signal_iq: Complex IQ signal
            window_size: Moving window size
            
        Returns:
            Dict with pulse train detection results
        """
        power = np.abs(signal_iq) ** 2
        moving_avg = signal.savgol_filter(power, min(window_size, len(power)-1), 1)
        
        # Detect rapid on/off transitions
        threshold = np.mean(moving_avg) * 2
        pulses = power > threshold
        transitions = np.diff(pulses.astype(int))
        num_transitions = np.sum(np.abs(transitions))
        
        is_pulse_train = num_transitions > 4  # Multiple pulses
        
        return {
            'is_pulse_train': is_pulse_train,
            'num_pulses': (num_transitions // 2),
            'pulse_count': num_transitions,
        }
