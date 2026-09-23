"""Small JSON-ready command operations for IQ capture review."""
from __future__ import annotations

from pathlib import Path

from .capture_manifest import summarize_iq_capture
from .integrity import sha256_file
from .partition import read_iq_file
from .quality import quality_report
from .spectral import occupied_bandwidth
from .statistics import summarize


def inspect_capture(path: str | Path) -> dict[str, object]:
    samples, rate = read_iq_file(path)
    if rate is None:
        raise ValueError("capture metadata must include sample_rate")
    result: dict[str, object] = summarize_iq_capture(path, source="recorded_iq")
    result["statistics"] = summarize(samples)
    result["quality"] = quality_report(samples, rate)
    result["sha256"] = sha256_file(path)
    result["occupied_bandwidth_hz"] = occupied_bandwidth(samples, rate)
    return result
