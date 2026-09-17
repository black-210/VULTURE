"""NMR and RF spectroscopy calculations."""
from __future__ import annotations

from typing import Dict, Iterable, Mapping
import numpy as np

from .constants import GYROMAGNETIC_RATIOS_MHZ_T


def larmor_frequency_hz(nucleus: str, b0_field_t: float, chemical_shift_ppm: float = 0.0) -> float:
    if b0_field_t <= 0:
        raise ValueError("b0_field_t must be positive")
    if nucleus not in GYROMAGNETIC_RATIOS_MHZ_T:
        raise ValueError(f"unsupported nucleus: {nucleus}")
    if not np.isfinite(chemical_shift_ppm):
        raise ValueError("chemical_shift_ppm must be finite")
    base = GYROMAGNETIC_RATIOS_MHZ_T[nucleus] * 1e6 * b0_field_t
    return float(base * (1.0 + chemical_shift_ppm * 1e-6))


def simulate_fid(
    nucleus: str = "1H", b0_field_t: float = 7.0, duration_s: float = 0.25,
    sample_rate_hz: float = 10_000.0, t2_s: float = 0.12,
    chemical_shift_ppm: float = 0.0, phase_rad: float = 0.0,
) -> Dict[str, object]:
    """Create a deterministic exponentially decaying complex FID."""
    if duration_s <= 0 or sample_rate_hz <= 0 or t2_s <= 0:
        raise ValueError("duration_s, sample_rate_hz and t2_s must be positive")
    count = int(round(duration_s * sample_rate_hz))
    time = np.arange(count, dtype=float) / sample_rate_hz
    frequency = larmor_frequency_hz(nucleus, b0_field_t, chemical_shift_ppm)
    fid = np.exp(-time / t2_s) * np.exp(1j * (2 * np.pi * frequency * time + phase_rad))
    return {"time_s": time, "fid": fid, "frequency_hz": frequency, "nucleus": nucleus}


def spectrum_from_fid(fid: np.ndarray, sample_rate_hz: float) -> Dict[str, np.ndarray]:
    """Return a centered FFT spectrum and frequency axis."""
    values = np.asarray(fid, dtype=complex)
    if values.ndim != 1 or values.size < 2 or sample_rate_hz <= 0:
        raise ValueError("fid must be a 1-D array with at least two samples")
    windowed = values * np.hanning(values.size)
    spectrum = np.fft.fftshift(np.fft.fft(windowed))
    frequencies = np.fft.fftshift(np.fft.fftfreq(values.size, 1.0 / sample_rate_hz))
    return {"frequency_hz": frequencies, "magnitude": np.abs(spectrum), "complex_spectrum": spectrum}
