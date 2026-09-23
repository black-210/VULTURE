"""FFT and spectral measurements from recorded IQ only."""
from __future__ import annotations

import numpy as np


def spectrum(samples: np.ndarray, sample_rate: float, window: str = "hann") -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(samples, dtype=np.complex64)
    if values.ndim != 1 or values.size < 2 or sample_rate <= 0:
        raise ValueError("need at least two samples and a positive sample rate")
    if window == "hann":
        values = values * np.hanning(values.size)
    elif window != "rectangular":
        raise ValueError("window must be hann or rectangular")
    frequencies = np.fft.fftshift(np.fft.fftfreq(values.size, 1.0 / sample_rate))
    power = np.abs(np.fft.fftshift(np.fft.fft(values))) ** 2
    return frequencies, power


def occupied_bandwidth(samples: np.ndarray, sample_rate: float, fraction: float = 0.99) -> float:
    frequencies, power = spectrum(samples, sample_rate)
    if not 0 < fraction <= 1 or not np.any(power):
        raise ValueError("fraction must be in (0, 1] and signal power must be non-zero")
    order = np.argsort(power)[::-1]
    selected = np.zeros(power.size, dtype=bool)
    selected[order[: max(1, int(np.ceil(order.size * fraction)))]] = True
    occupied = frequencies[selected]
    return float(occupied.max() - occupied.min())
