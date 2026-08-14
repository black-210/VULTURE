"""Matched Filter - Optimal Signal Detection"""
import numpy as np
from scipy.signal import correlate
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class MatchedFilter:
    """Matched filter for signal detection"""
    
    def __init__(self, template: np.ndarray):
        """Initialize matched filter
        
        Args:
            template: Template signal for matching
        """
        self.template = template
        self.energy = np.sum(np.abs(template) ** 2)
    
    def detect(self, signal: np.ndarray, threshold: float = None) -> Tuple[np.ndarray, np.ndarray]:
        """Detect template in signal
        
        Args:
            signal: Input signal
            threshold: Detection threshold
        
        Returns:
            (Detection indices, Detection statistics)
        """
        correlation = correlate(signal, self.template, mode='valid')
        correlation_normalized = correlation / np.sqrt(self.energy)
        
        if threshold is None:
            threshold = np.mean(correlation_normalized) + 3 * np.std(correlation_normalized)
        
        detections = np.where(correlation_normalized > threshold)[0]
        
        return detections, correlation_normalized
    
    def get_snr(self, signal: np.ndarray, noise_only: np.ndarray = None) -> float:
        """Estimate SNR for detection
        
        Args:
            signal: Input signal
            noise_only: Noise-only sample
        
        Returns:
            SNR estimate
        """
        correlation = correlate(signal, self.template, mode='valid')
        signal_power = np.max(np.abs(correlation)) ** 2
        
        if noise_only is not None:
            noise_corr = correlate(noise_only, self.template, mode='valid')
            noise_power = np.mean(np.abs(noise_corr) ** 2)
        else:
            noise_power = np.mean(np.abs(correlation) ** 2) - signal_power
        
        snr = signal_power / (noise_power + 1e-10)
        return 10 * np.log10(snr + 1e-10)
