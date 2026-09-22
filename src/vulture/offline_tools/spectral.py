"""Frequency-domain summaries for deterministic local signals."""
from __future__ import annotations
from .transform import dft
from .validation import finite_values
from .windows import apply_window


def dominant_frequency(values: list[float], sample_rate: float) -> dict[str, float | int]:
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    data = apply_window(finite_values(values))
    spectrum = dft(data)
    half = len(spectrum) // 2 + 1
    index = max(range(half), key=lambda item: abs(spectrum[item]))
    return {"bin": index, "frequency_hz": index * sample_rate / len(data), "magnitude": abs(spectrum[index])}
