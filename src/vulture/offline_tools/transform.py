"""Portable DFT utilities for small offline fixtures."""
from __future__ import annotations
import cmath
import math


def dft(values: list[float]) -> list[complex]:
    size = len(values)
    if size == 0:
        raise ValueError("values must not be empty")
    return [sum(value * cmath.exp(-2j * math.pi * frequency * index / size)
                for index, value in enumerate(values)) for frequency in range(size)]
