"""Input validation utilities."""
import numpy as np
from typing import Union, Tuple

def validate_iq_data(data: np.ndarray) -> Tuple[bool, str]:
    """Validate IQ data array.
    
    Args:
        data: Input IQ data.
    
    Returns:
        Tuple of (is_valid, error_message).
    """
    if not isinstance(data, np.ndarray):
        return False, "IQ data must be numpy array"
    
    if data.ndim not in [1, 2]:
        return False, "IQ data must be 1D or 2D array"
    
    if data.dtype not in [np.complex64, np.complex128, np.float32, np.float64]:
        return False, f"Unsupported data type: {data.dtype}"
    
    if data.size == 0:
        return False, "IQ data cannot be empty"
    
    return True, ""

def validate_signal_power(data: np.ndarray) -> bool:
    """Check if signal has reasonable power (not all zeros).
    
    Args:
        data: Input signal.
    
    Returns:
        True if signal has power, False otherwise.
    """
    power = np.mean(np.abs(data) ** 2)
    return power > 1e-10
