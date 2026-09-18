"""Validated data models for chemistry/RF experiments.

These models are intentionally measurement-oriented: every predicted quantity
can carry uncertainty, calibration provenance, and a clear unit.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Mapping, Optional, Tuple


@dataclass(frozen=True)
class Measurement:
    value: float
    unit: str
    uncertainty: Optional[float] = None
    source: str = "model"

    def __post_init__(self) -> None:
        if not self.unit:
            raise ValueError("measurement unit is required")
        if self.uncertainty is not None and self.uncertainty < 0:
            raise ValueError("uncertainty cannot be negative")


@dataclass(frozen=True)
class CalibrationPoint:
    frequency_hz: float
    measured_impedance_ohm: complex
    temperature_c: float = 25.0
    humidity_percent: Optional[float] = None

    def __post_init__(self) -> None:
        if self.frequency_hz <= 0:
            raise ValueError("frequency_hz must be positive")
        if self.temperature_c < -273.15:
            raise ValueError("temperature cannot be below absolute zero")
        if self.humidity_percent is not None and not 0 <= self.humidity_percent <= 100:
            raise ValueError("humidity_percent must be between 0 and 100")


@dataclass
class ExperimentRecord:
    sample_id: str
    method: str
    parameters: Dict[str, float | str] = field(default_factory=dict)
    results: Dict[str, Measurement] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, object]:
        return {
            "sample_id": self.sample_id,
            "method": self.method,
            "parameters": dict(self.parameters),
            "results": {k: vars(v) for k, v in self.results.items()},
            "created_at": self.created_at,
        }
    def from_dict(cls, data: Dict[str, object]) -> ExperimentRecord:
        return cls(
            sample_id=data["sample_id"],
            method=data["method"],
            parameters=data.get("parameters", {}),
            results={k: Measurement(**v) for k, v in data.get("results", {}).items()},
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat())
        )
      
    
    def validate(self) -> None:
        if not self.sample_id:
           raise ValueError("sample_id is required")
        if not self.method:
            raise ValueError("method is required")
        for key, measurement in self.results.items():
            if not isinstance(measurement, Measurement):
                raise ValueError(f"Result '{key}' must be a Measurement instance")
    def add_result(self, key: str, measurement: Measurement) -> None:
        if key in self.results:
            raise ValueError(f"Result '{key}' already exists")
        self.results[key] = measurement
        self.validate()
    def remove_result(self, key: str) -> None:
        if key not in self.results:
            raise ValueError(f"Result '{key}' does not exist")
        del self.results[key]
        self.validate()
    def update_result(self, key: str, measurement: Measurement) -> None:
        if key not in self.results:
            raise ValueError(f"Result '{key}' does not exist")
        self.results[key] = measurement
        self.validate()
    def get_result(self, key: str) -> Measurement:
        if key not in self.results:
            raise ValueError(f"Result '{key}' does not exist")
        return self.results[key]