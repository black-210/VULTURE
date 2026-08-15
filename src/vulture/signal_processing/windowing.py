"""Window functions with scallop loss database."""

import numpy as np
from scipy import signal
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class WindowManager:
    """Window function management and scallop loss data."""

    # Scallop loss (dB) for common windows
    SCALLOP_LOSS = {
        'boxcar': 3.92,
        'hann': 1.42,
        'hamming': 1.30,
        'blackman': 1.10,
        'bartlett': 4.49,
        'kaiser': 1.42,  # varies with beta
        'tukey': 1.42,  # varies with alpha
    }

    MAIN_LOBE_WIDTH = {
        'boxcar': 4.0,
        'hann': 8.0,
        'hamming': 8.0,
        'blackman': 12.0,
        'bartlett': 8.0,
        'kaiser': 5.0,
    }

    @staticmethod
    def get_window(name: str, size: int, **kwargs) -> np.ndarray:
        """Get window function.
        
        Args:
            name: Window name
            size: Window size
            **kwargs: Window-specific parameters
            
        Returns:
            Window array
        """
        return signal.get_window(name, size, fftbins=False)

    @staticmethod
    def get_scallop_loss(window_name: str) -> float:
        """Get scallop loss for window.
        
        Args:
            window_name: Window name
            
        Returns:
            Scallop loss in dB
        """
        return WindowManager.SCALLOP_LOSS.get(window_name, 3.92)

    @staticmethod
    def get_main_lobe_width(window_name: str) -> float:
        """Get main lobe width.
        
        Args:
            window_name: Window name
            
        Returns:
            Main lobe width (bins)
        """
        return WindowManager.MAIN_LOBE_WIDTH.get(window_name, 4.0)

    @staticmethod
    def compare_windows() -> Dict:
        """Compare window characteristics.
        
        Returns:
            Dict with window properties
        """
        return {
            'scallop_loss': dict(WindowManager.SCALLOP_LOSS),
            'main_lobe_width': dict(WindowManager.MAIN_LOBE_WIDTH),
        }
