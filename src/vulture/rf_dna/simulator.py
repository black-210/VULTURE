"""Deterministic IQ fixtures for tests and no-SDR development."""
from __future__ import annotations

from pathlib import Path
import numpy as np


def generate_iq(
    profile: str = "noise",
    duration: float = 1.0,
    sample_rate: float = 1_000_000.0,
    seed: int = 7,
) -> np.ndarray:
    """Generate complex baseband samples without opening hardware.

    Profiles are deliberately synthetic and suitable for unit tests. The
    function validates resource limits to prevent accidental huge allocations.
    """
    if duration <= 0 or sample_rate <= 0:
        raise ValueError("duration and sample_rate must be positive")
    count = int(duration * sample_rate)
    if count < 1 or count > 10_000_000:
        raise ValueError("sample count must be between 1 and 10,000,000")
    rng = np.random.default_rng(seed)
    t = np.arange(count, dtype=np.float64) / sample_rate
    noise = (rng.normal(size=count) + 1j * rng.normal(size=count)) / np.sqrt(2.0)
    name = profile.lower()
    if name == "noise":
        return noise.astype(np.complex64)
    if name == "multi-tone":
        tones = np.exp(2j * np.pi * 0.05 * sample_rate * t)
        tones += 0.5 * np.exp(2j * np.pi * 0.17 * sample_rate * t)
        return (tones + 0.05 * noise).astype(np.complex64)
    if name == "cw":
        return (np.exp(2j * np.pi * 0.1 * sample_rate * t) + 0.02 * noise).astype(np.complex64)
    if name == "chirp":
        phase = 2 * np.pi * (0.01 * sample_rate * t + 0.04 * sample_rate * t * t / max(duration, 1e-12))
        return (np.exp(1j * phase) + 0.03 * noise).astype(np.complex64)
    raise ValueError("unknown profile; choose noise, multi-tone, cw, or chirp")


def save_npz(path: str | Path, samples: np.ndarray, sample_rate: float) -> None:
    """Save a simulator capture with minimal provenance metadata."""
    array = np.asarray(samples, dtype=np.complex64)
    np.savez_compressed(path, iq=array, sample_rate=float(sample_rate), source="vulture-rf-dna-simulator")
