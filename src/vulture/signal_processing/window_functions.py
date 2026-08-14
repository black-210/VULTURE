"""Window Functions - Signal Windowing Library"""
import numpy as np
from scipy.signal import get_window, windows
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class WindowFunctions:
    """Comprehensive window function library"""
    
    WINDOW_TYPES = {
        'hamming': 'Hamming window',
        'hann': 'Hann window',
        'blackman': 'Blackman window',
        'bartlett': 'Bartlett window',
        'kaiser': 'Kaiser window',
        'tukey': 'Tukey window',
        'flattop': 'Flat-top window',
        'nuttall': 'Nuttall window',
        'boxcar': 'Rectangular window',
    }
    
    @staticmethod
    def apply_window(signal: np.ndarray, window_type: str = 'hann',
                    window_params: Dict = None) -> np.ndarray:
        """Apply window function to signal
        
        Args:
            signal: Input signal
            window_type: Type of window
            window_params: Window-specific parameters
        
        Returns:
            Windowed signal
        """
        window_params = window_params or {}
        window = get_window(window_type, len(signal), fftbins=False)
        return signal * window
    
    @staticmethod
    def get_window_properties(window_type: str, length: int) -> Dict:
        """Get window properties
        
        Args:
            window_type: Type of window
            length: Window length
        
        Returns:
            Dictionary of properties
        """
        window = get_window(window_type, length)
        
        # Compute main lobe width (approximate)
        fft_win = np.fft.fft(window, 4096)
        mag = np.abs(fft_win)
        main_lobe_width = np.sum(mag > np.max(mag) * 0.1) * 2 * np.pi / 4096
        
        return {
            'type': window_type,
            'length': length,
            'main_lobe_width': main_lobe_width,
            'peak_sidelobe': 20 * np.log10(np.max(np.abs(fft_win[1:])) / np.max(np.abs(fft_win)) + 1e-10),
        }
    
    @staticmethod
    def list_windows() -> Dict[str, str]:
        """List available windows
        
        Returns:
            Dictionary of window types and descriptions
        """
        return WindowFunctions.WINDOW_TYPES.copy()
