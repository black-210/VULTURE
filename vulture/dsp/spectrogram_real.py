"""
Spectrogram generation using scipy.signal.spectrogram with numpy fallback.
Returns times, freqs, and Sxx (magnitude or power).
"""
from typing import Any, Dict

try:
    import numpy as np
except Exception:
    np = None


def generate_spectrogram_real(samples: Any, fs: float = 1.0, nperseg: int = 256, noverlap: int = None) -> Dict[str, Any]:
    """Generate spectrogram data.

    Args:
        samples: 1D array-like signal.
        fs: sampling rate
        nperseg: samples per segment
        noverlap: overlap between segments

    Returns:
        dict with 'times', 'freqs', 'Sxx'
    """
    if np is None:
        raise RuntimeError("numpy is required for spectrogram generation")

    samples = np.asarray(samples)
    try:
        from scipy import signal
        if noverlap is None:
            noverlap = nperseg // 2
        freqs, times, Sxx = signal.spectrogram(samples, fs=fs, nperseg=nperseg, noverlap=noverlap, window='hann')
        return {"times": times, "freqs": freqs, "Sxx": Sxx}
    except Exception:
        # Fallback naive STFT
        step = nperseg - (noverlap or (nperseg // 2))
        shape = ((len(samples) - nperseg) // step + 1, nperseg)
        segments = [samples[i * step:i * step + nperseg] * np.hanning(nperseg) for i in range(shape[0])]
        S = [np.fft.rfft(s) for s in segments]
        Sxx = np.abs(np.vstack(S).T)
        freqs = np.fft.rfftfreq(nperseg, d=1.0 / fs)
        times = np.arange(Sxx.shape[1]) * (step / fs)
        return {"times": times, "freqs": freqs, "Sxx": Sxx}
