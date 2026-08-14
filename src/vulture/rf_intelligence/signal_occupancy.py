"""Signal occupancy analysis."""
import numpy as np
import logging

logger = logging.getLogger(__name__)

class SignalOccupancy:
    """Signal occupancy methods."""
    
    @staticmethod
    def compute_occupancy(psd, threshold=None):
        if threshold is None:
            noise_floor = np.percentile(psd, 10)
            threshold = noise_floor + 3
        occupied = np.sum(psd > threshold)
        return occupied / len(psd)
    
    @staticmethod
    def find_occupied_bands(frequencies, psd, threshold, min_bandwidth=1e5):
        occupied = psd > threshold
        bands = []
        in_band = False
        start_idx = 0
        
        for i, is_occupied in enumerate(occupied):
            if is_occupied and not in_band:
                in_band = True
                start_idx = i
            elif not is_occupied and in_band:
                in_band = False
                bandwidth = frequencies[i-1] - frequencies[start_idx]
                if bandwidth >= min_bandwidth:
                    power = np.mean(psd[start_idx:i])
                    bands.append((frequencies[start_idx], frequencies[i-1], power))
        return bands
    
    @staticmethod
    def duty_cycle_analysis(data, fs, threshold):
        envelope = np.abs(data)
        occupied_samples = np.sum(envelope > threshold)
        return occupied_samples / len(data)