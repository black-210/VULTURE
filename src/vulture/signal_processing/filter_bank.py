"""Filter Bank - Multi-channel Filter Architecture"""
import numpy as np
from .fir_filter import FIRFilter
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class FilterBank:
    """Multi-channel filter bank implementation"""
    
    def __init__(self, num_channels: int, filter_order: int, sample_rate: float = 1e6):
        """Initialize filter bank
        
        Args:
            num_channels: Number of channels
            filter_order: Filter order
            sample_rate: Sample rate
        """
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self.filters: List[FIRFilter] = []
        self._create_filters(filter_order)
    
    def _create_filters(self, filter_order: int) -> None:
        """Create filter bank filters
        
        Args:
            filter_order: Filter order
        """
        nyquist = self.sample_rate / 2
        bandwidth = nyquist / self.num_channels
        
        for i in range(self.num_channels):
            fir = FIRFilter(filter_order, self.sample_rate)
            low_freq = i * bandwidth
            high_freq = (i + 1) * bandwidth
            fir.design_bandpass(low_freq, high_freq)
            self.filters.append(fir)
    
    def apply(self, signal: np.ndarray) -> np.ndarray:
        """Apply filter bank to signal
        
        Args:
            signal: Input signal
        
        Returns:
            Channel outputs (num_channels x signal_length)
        """
        outputs = np.zeros((self.num_channels, len(signal)))
        for i, fir in enumerate(self.filters):
            outputs[i] = fir.apply(signal)
        return outputs
    
    def get_channel_powers(self, signal: np.ndarray) -> np.ndarray:
        """Get power in each channel
        
        Args:
            signal: Input signal
        
        Returns:
            Power in each channel
        """
        outputs = self.apply(signal)
        powers = np.mean(np.abs(outputs) ** 2, axis=1)
        return powers
