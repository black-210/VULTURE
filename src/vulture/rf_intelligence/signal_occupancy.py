"""Signal occupancy analysis: band detection, duty cycle, frequency allocation."""

import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class OccupancyAnalyzer:
    """RF band occupancy analysis."""

    @staticmethod
    def compute_occupancy(power_db: np.ndarray, freqs: np.ndarray, threshold_db: float = -80) -> Dict:
        """Compute band occupancy metrics.
        
        Args:
            power_db: Power spectrum in dB
            freqs: Frequency array
            threshold_db: Detection threshold
            
        Returns:
            Dict with occupancy metrics
        """
        occupied = power_db > threshold_db
        occupancy_percent = 100 * np.sum(occupied) / len(occupied)
        
        return {
            'occupancy_percent': occupancy_percent,
            'num_occupied_bins': np.sum(occupied),
            'threshold_db': threshold_db,
            'max_power_db': np.max(power_db),
            'mean_power_db': np.mean(power_db),
        }

    @staticmethod
    def detect_bands(power_db: np.ndarray, freqs: np.ndarray, threshold_db: float = -80,
                    min_bandwidth: float = 1e6) -> List[Dict]:
        """Detect occupied frequency bands.
        
        Args:
            power_db: Power spectrum in dB
            freqs: Frequency array
            threshold_db: Detection threshold
            min_bandwidth: Minimum band width to report
            
        Returns:
            List of band dicts
        """
        occupied = power_db > threshold_db
        freq_resolution = freqs[1] - freqs[0] if len(freqs) > 1 else 1
        
        # Find transitions
        transitions = np.diff(occupied.astype(int))
        starts = np.where(transitions == 1)[0] + 1
        ends = np.where(transitions == -1)[0] + 1
        
        bands = []
        for start, end in zip(starts, ends):
            center_idx = (start + end) // 2
            bandwidth = (end - start) * freq_resolution
            if bandwidth >= min_bandwidth:
                bands.append({
                    'center_freq': freqs[center_idx],
                    'start_freq': freqs[start],
                    'end_freq': freqs[min(end, len(freqs)-1)],
                    'bandwidth': bandwidth,
                    'power_db': np.mean(power_db[start:end]),
                })
        return bands

    @staticmethod
    def compute_duty_cycle(signal_iq: np.ndarray, window_size: int = 1024,
                          threshold: float = 0.1) -> float:
        """Compute transmitter duty cycle.
        
        Args:
            signal_iq: Complex IQ signal
            window_size: Sliding window size
            threshold: Detection threshold (normalized)
            
        Returns:
            Duty cycle (0-1)
        """
        power = np.abs(signal_iq) ** 2
        power_normalized = power / np.max(power) if np.max(power) > 0 else power
        
        detected = power_normalized > threshold
        duty_cycle = np.sum(detected) / len(detected)
        return duty_cycle
