"""Simple window functions for local signal processing."""
from __future__ import annotations
import math


def hann(size: int) -> list[float]:
    if size < 1:
        raise ValueError("size must be positive")
    if size == 1:
        return [1.0]
    return [0.5 - 0.5 * math.cos(2 * math.pi * index / (size - 1)) for index in range(size)]


def apply_window(values: list[float], window: str = "hann") -> list[float]:
    if window != "hann":
        raise ValueError("supported windows: hann")
    weights = hann(len(values))
    return [float(value) * weight for value, weight in zip(values, weights)]
