"""One-call deterministic analysis workflow."""
from __future__ import annotations
from .report import signal_report
from .spectral import dominant_frequency


def analyze(values: list[float], sample_rate: float | None = None) -> dict[str, object]:
    report = signal_report(values)
    if sample_rate is not None:
        report["spectrum"] = dominant_frequency(values, sample_rate)
    return report
