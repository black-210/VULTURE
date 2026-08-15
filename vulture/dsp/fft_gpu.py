"""
GPU-accelerated FFT helpers using CuPy when available, falling back to NumPy.
Provides fft/ifft with transparent array conversion.
"""
from typing import Any

try:
    import cupy as cp
    _CUPY_AVAILABLE = True
except Exception:
    cp = None
    _CUPY_AVAILABLE = False

try:
    import numpy as np
except Exception:
    np = None


def _to_numpy(x):
    if _CUPY_AVAILABLE and hasattr(x, 'get'):
        return cp.asnumpy(x)
    return x


def _to_cupy(x):
    if _CUPY_AVAILABLE:
        return cp.asarray(x)
    return x


def fft(samples: Any):
    """Compute FFT using CuPy if available, otherwise NumPy."""
    if _CUPY_AVAILABLE:
        arr = _to_cupy(samples)
        return cp.fft.fft(arr)
    if np is None:
        raise RuntimeError("numpy is required for FFT")
    return np.fft.fft(samples)


def ifft(spectrum: Any):
    """Compute inverse FFT."""
    if _CUPY_AVAILABLE:
        arr = _to_cupy(spectrum)
        return cp.fft.ifft(arr)
    if np is None:
        raise RuntimeError("numpy is required for IFFT")
    return np.fft.ifft(spectrum)


def compute_psd_gpu(samples: Any, fs: float = 1.0):
    """Simple PSD using FFT path; prefers GPU when available. Returns (freqs, psd)."""
    if np is None:
        raise RuntimeError("numpy is required for PSD computation")
    if _CUPY_AVAILABLE:
        x = cp.asarray(samples)
        N = x.size
        spec = cp.fft.rfft(x * cp.hanning(N))
        psd = (cp.abs(spec) ** 2) / (fs * N)
        freqs = cp.fft.rfftfreq(N, d=1.0 / fs)
        return _to_numpy(freqs), _to_numpy(psd)
    else:
        x = np.asarray(samples)
        N = x.size
        spec = np.fft.rfft(x * np.hanning(N))
        psd = (np.abs(spec) ** 2) / (fs * N)
        freqs = np.fft.rfftfreq(N, d=1.0 / fs)
        return freqs, psd
