"""
Signal Processing framework stubs: FFT/PSD, filters, windowing, spectrogram.
"""
from .fft import fft, ifft
from .psd import compute_psd
from .filters import apply_filter
from .window import get_window
from .spectrogram import generate_spectrogram

__all__ = ["fft", "ifft", "compute_psd", "apply_filter", "get_window", "generate_spectrogram"]
