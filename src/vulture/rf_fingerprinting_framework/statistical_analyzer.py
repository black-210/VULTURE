"""Statistical Analyzer - Advanced Statistical Analysis"""
import numpy as np
from scipy import stats
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class StatisticalAnalyzer:
    """Perform statistical analysis on RF signals"""
    
    @staticmethod
    def compute_moments(signal: np.ndarray, max_order: int = 4) -> Dict[str, float]:
        """Compute statistical moments
        
        Args:
            signal: Input signal
            max_order: Maximum moment order
        
        Returns:
            Dictionary of moments
        """
        moments = {}
        amplitude = np.abs(signal)
        
        for order in range(1, max_order + 1):
            moments[f'moment_{order}'] = np.mean(amplitude ** order)
        
        return moments
    
    @staticmethod
    def higher_order_statistics(signal: np.ndarray) -> Dict[str, float]:
        """Compute higher-order statistics
        
        Args:
            signal: Input signal
        
        Returns:
            Dictionary of HOS features
        """
        i = np.real(signal)
        q = np.imag(signal)
        
        return {
            'i_skewness': stats.skew(i),
            'i_kurtosis': stats.kurtosis(i),
            'q_skewness': stats.skew(q),
            'q_kurtosis': stats.kurtosis(q),
            'iq_joint_skewness': stats.skew(np.abs(signal)),
            'iq_joint_kurtosis': stats.kurtosis(np.abs(signal)),
        }
    
    @staticmethod
    def compute_pdf_parameters(signal: np.ndarray, num_bins: int = 50) -> Dict[str, float]:
        """Estimate PDF parameters
        
        Args:
            signal: Input signal
            num_bins: Number of histogram bins
        
        Returns:
            Dictionary of PDF parameters
        """
        amplitude = np.abs(signal)
        hist, bin_edges = np.histogram(amplitude, bins=num_bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        return {
            'pdf_max': np.max(hist),
            'pdf_min': np.min(hist),
            'pdf_entropy': -np.sum((hist / np.sum(hist)) * np.log(hist / np.sum(hist) + 1e-10)),
        }
