"""Descriptive statistics without optional scientific dependencies."""
from __future__ import annotations

from .validation import finite_values


def describe(values: list[float]) -> dict[str, float | int]:
    data = sorted(finite_values(values))
    count = len(data)
    mean = sum(data) / count
    variance = sum((value - mean) ** 2 for value in data) / count
    median = data[count // 2] if count % 2 else (data[count // 2 - 1] + data[count // 2]) / 2
    return {"count": count, "min": data[0], "max": data[-1], "mean": mean,
            "median": median, "variance": variance, "stddev": variance ** 0.5,
            "rms": (sum(value * value for value in data) / count) ** 0.5,
            "peak_to_peak": data[-1] - data[0]}
