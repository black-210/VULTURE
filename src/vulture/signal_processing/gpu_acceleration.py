"""GPU acceleration for DSP operations."""

import numpy as np
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

HAS_CUPY = False
HAS_TORCH = False

try:
    import cupy as cp
    HAS_CUPY = True
except ImportError:
    pass

try:
    import torch
    HAS_TORCH = True
except ImportError:
    pass


class GPUAcceleration:
    """GPU-accelerated DSP operations (CuPy/PyTorch fallback to CPU)."""

    @staticmethod
    def get_device() -> str:
        """Check available GPU device.
        
        Returns:
            Device string
        """
        if HAS_CUPY:
            return "GPU (CuPy)"
        elif HAS_TORCH and torch.cuda.is_available():
            return f"GPU (PyTorch: {torch.cuda.get_device_name(0)})"
        return "CPU (no GPU available)"

    @staticmethod
    def compute_gpu_fft(data: np.ndarray) -> np.ndarray:
        """FFT with GPU acceleration.
        
        Args:
            data: Input array
            
        Returns:
            FFT result
        """
        if HAS_CUPY:
            try:
                gpu_data = cp.asarray(data)
                gpu_fft = cp.fft.fft(gpu_data)
                return np.array(cp.asnumpy(gpu_fft))
            except Exception as e:
                logger.warning(f"CuPy FFT failed: {e}, falling back to CPU")
                return np.fft.fft(data)
        else:
            logger.debug("CuPy not available, using NumPy FFT")
            return np.fft.fft(data)

    @staticmethod
    def compute_gpu_correlate(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Correlation with GPU acceleration.
        
        Args:
            x, y: Input arrays
            
        Returns:
            Correlation result
        """
        if HAS_CUPY:
            try:
                gpu_x = cp.asarray(x)
                gpu_y = cp.asarray(y)
                gpu_corr = cp.correlate(gpu_x, gpu_y)
                return np.array(cp.asnumpy(gpu_corr))
            except Exception as e:
                logger.warning(f"CuPy correlate failed: {e}, falling back to CPU")
        
        from scipy import signal
        return signal.correlate(x, y)

    @staticmethod
    def compute_gpu_filter(data: np.ndarray, b: np.ndarray, 
                          a: np.ndarray = None) -> np.ndarray:
        """Filter with GPU acceleration.
        
        Args:
            data: Input signal
            b: FIR coefficients or numerator
            a: Denominator (if None, FIR filter)
            
        Returns:
            Filtered signal
        """
        if HAS_CUPY:
            try:
                gpu_data = cp.asarray(data)
                gpu_b = cp.asarray(b)
                if a is not None:
                    gpu_a = cp.asarray(a)
                    gpu_result = cp.convolve(gpu_data, gpu_b / gpu_a[0])
                else:
                    gpu_result = cp.convolve(gpu_data, gpu_b)
                return np.array(cp.asnumpy(gpu_result))
            except Exception as e:
                logger.warning(f"CuPy filter failed: {e}, falling back to CPU")
        
        from scipy import signal
        if a is not None:
            return signal.filtfilt(b, a, data)
        else:
            return signal.filtfilt(b, [1], data)
