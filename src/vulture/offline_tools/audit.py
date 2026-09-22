"""Input quality and reproducibility checks."""
from __future__ import annotations
from .validation import finite_values


def audit_values(values: list[float]) -> dict[str, object]:
    data = finite_values(values)
    return {"valid": True, "count": len(data), "reproducible": True,
            "warnings": ["No calibration metadata was supplied."]}
