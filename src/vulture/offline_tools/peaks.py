"""Conservative local peak detection."""
from __future__ import annotations

from .stats import describe
from .validation import finite_values


def find_peaks(values: list[float], threshold: float | None = None) -> list[dict[str, float | int]]:
    data = finite_values(values)
    summary = describe(data)
    limit = summary["mean"] + summary["stddev"] if threshold is None else float(threshold)
    return [{"index": index, "value": data[index]} for index in range(1, len(data) - 1)
            if data[index] >= data[index - 1] and data[index] >= data[index + 1] and data[index] >= limit]
