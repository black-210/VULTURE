"""Safe, local chemistry, physics, and mathematics utilities for the CLI."""
from __future__ import annotations

from math import gcd, pi, sqrt
from typing import Iterable, Sequence

C = 299_792_458.0


def free_space_path_loss_db(frequency_hz: float, distance_m: float) -> float:
    """Friis free-space path loss in dB; no transmitter control is performed."""
    if frequency_hz <= 0 or distance_m <= 0:
        raise ValueError("frequency_hz and distance_m must be positive")
    wavelength = C / frequency_hz
    return 20.0 * __import__("math").log10(4.0 * pi * distance_m / wavelength)


def wavelength_m(frequency_hz: float) -> float:
    if frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    return C / frequency_hz


def solve_linear_system(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> list[float]:
    """Small Gaussian-elimination solver using only the Python standard library."""
    a = [list(map(float, row)) + [float(value)] for row, value in zip(matrix, vector)]
    n = len(a)
    if n == 0 or any(len(row) != n + 1 for row in a):
        raise ValueError("matrix must be square and match vector length")
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        if abs(a[pivot][col]) < 1e-12:
            raise ValueError("singular matrix")
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [x / scale for x in a[col]]
        for row in range(n):
            if row != col:
                factor = a[row][col]
                a[row] = [x - factor * y for x, y in zip(a[row], a[col])]
    return [a[row][-1] for row in range(n)]


def gcd_many(values: Iterable[int]) -> int:
    result = 0
    for value in values:
        result = gcd(result, abs(int(value)))
    return result


__all__ = ["free_space_path_loss_db", "wavelength_m", "solve_linear_system", "gcd_many"]
