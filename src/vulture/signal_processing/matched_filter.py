"""Matched filtering with PFA threshold calculation."""

import numpy as np
from scipy import signal, stats
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class MatchedFilter:
    """Optimal matched filtering."""

    @staticmethod
    def filter(data: np.ndarray, template: np.ndarray, 
               normalize: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """Apply matched filter.
        
        Args:
            data: Input signal
            template: Template/signal to match
            normalize: Normalize by signal energy
            
        Returns:
            (filter_output, normalized_output)
        """
        output = signal.correlate(data, template, mode='same')
        
        if normalize:
            template_energy = np.sum(template ** 2)
            normalized = output / np.sqrt(template_energy)
        else:
            normalized = output
        
        return output, normalized

    @staticmethod
    def compute_threshold(noise_psd: float, target_pfa: float, 
                         signal_length: int) -> float:
        """Compute Neyman-Pearson threshold.
        
        Args:
            noise_psd: Noise power spectral density
            target_pfa: Probability of false alarm
            signal_length: Signal length
            
        Returns:
            Detection threshold
        """
        # For Gaussian noise: threshold = noise_std * sqrt(2 * ln(1/pfa))
        noise_std = np.sqrt(noise_psd)
        threshold = noise_std * np.sqrt(2 * np.log(1 / target_pfa))
        return threshold

    @staticmethod
    def detect(output: np.ndarray, threshold: float) -> np.ndarray:
        """Apply threshold to matched filter output.
        
        Args:
            output: Matched filter output
            threshold: Detection threshold
            
        Returns:
            Binary detection array
        """
        return (np.abs(output) > threshold).astype(int)
