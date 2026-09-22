"""Human-readable report assembly."""
from __future__ import annotations
from .audit import audit_values
from .peaks import find_peaks
from .stats import describe


def signal_report(values: list[float], threshold: float | None = None) -> dict[str, object]:
    return {"engine": "vulture.offline_tools", "stats": describe(values),
            "peaks": find_peaks(values, threshold), "audit": audit_values(values),
            "status": "uncalibrated-local-analysis"}
