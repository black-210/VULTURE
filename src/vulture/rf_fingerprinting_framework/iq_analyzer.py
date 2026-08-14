"""IQ Analyzer - I/Q Constellation and Imbalance Analysis"""
import numpy as np
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class IQAnalyzer:
    """Analyze I/Q constellation and properties"""
    
    @staticmethod
    def compute_iq_imbalance(signal: np.ndarray) -> Dict[str, float]:
        """Compute I/Q imbalance metrics
        
        Args:
            signal: IQ signal
        
        Returns:
            Imbalance metrics
        """
        i = np.real(signal)
        q = np.imag(signal)
        
        # Amplitude imbalance
        amp_ratio = np.std(i) / (np.std(q) + 1e-10)
        amp_imbalance_db = 20 * np.log10(amp_ratio + 1e-10)
        
        # Phase imbalance (orthogonality)
        correlation = np.corrcoef(i, q)[0, 1]
        phase_imbalance = np.arcsin(np.clip(correlation, -1, 1)) * 180 / np.pi
        
        return {
            'amplitude_imbalance_db': amp_imbalance_db,
            'phase_imbalance_degrees': phase_imbalance,
            'iq_correlation': correlation,
            'iq_power_ratio': (np.mean(i**2)) / (np.mean(q**2) + 1e-10),
        }
    
    @staticmethod
    def compute_constellation_metrics(signal: np.ndarray) -> Dict[str, float]:
        """Compute constellation diagram metrics
        
        Args:
            signal: IQ signal
        
        Returns:
            Constellation metrics
        """
        # Compute constellation center
        center_i = np.mean(np.real(signal))
        center_q = np.mean(np.imag(signal))
        center = center_i + 1j * center_q
        
        # Distance from center
        distances = np.abs(signal - center)
        
        return {
            'constellation_center_i': center_i,
            'constellation_center_q': center_q,
            'constellation_radius_mean': np.mean(distances),
            'constellation_radius_std': np.std(distances),
            'constellation_radius_max': np.max(distances),
            'constellation_evm': np.sqrt(np.mean(distances ** 2)) / (np.abs(center) + 1e-10),
        }
