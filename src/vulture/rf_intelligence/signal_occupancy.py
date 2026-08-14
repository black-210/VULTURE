"""Signal Occupancy - Spectrum Occupancy Analysis"""
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class SignalOccupancy:
    """Analyze spectrum occupancy"""
    
    def compute_occupancy(self, psd: np.ndarray, threshold: float = None) -> float:
        """Compute spectrum occupancy percentage
        
        Args:
            psd: Power spectral density
            threshold: Occupancy threshold
        
        Returns:
            Occupancy percentage (0-100)
        """
        if threshold is None:
            threshold = np.mean(psd) + np.std(psd)
        
        occupied = np.sum(psd > threshold)
        total = len(psd)
        return (occupied / total) * 100
    
    def find_occupied_bands(self, freqs: np.ndarray, psd: np.ndarray,
                           threshold: float = None, min_bandwidth: float = 1e3) -> List[Tuple[float, float]]:
        """Find occupied frequency bands
        
        Args:
            freqs: Frequency array
            psd: Power spectral density
            threshold: Detection threshold
            min_bandwidth: Minimum bandwidth
        
        Returns:
            List of (start_freq, stop_freq) tuples
        """
        if threshold is None:
            threshold = np.mean(psd) + np.std(psd)
        
        occupied = psd > threshold
        edges = np.diff(occupied.astype(int))
        starts = np.where(edges == 1)[0]
        ends = np.where(edges == -1)[0]
        
        bands = []
        for start, end in zip(starts, ends):
            if freqs[end] - freqs[start] >= min_bandwidth:
                bands.append((freqs[start], freqs[end]))
        
        return bands
