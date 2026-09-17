"""A defensible analysis pipeline with provenance and anti-placeholder checks."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Dict, Mapping

from .calibration import LinearCalibration
from .models import ExperimentRecord, Measurement
from .materials import reflection_coefficient


@dataclass
class ChemicalRFReport:
    sample_id: str
    impedance_ohm: complex
    reflection: complex
    calibration_rms_ohm: float | None
    provenance_hash: str
    warnings: list[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_id": self.sample_id,
            "impedance_ohm": {"real": self.impedance_ohm.real, "imag": self.impedance_ohm.imag},
            "reflection": {"real": self.reflection.real, "imag": self.reflection.imag},
            "calibration_rms_ohm": self.calibration_rms_ohm,
            "provenance_hash": self.provenance_hash,
            "warnings": self.warnings,
        }


class ChemicalRFAnalysisPipeline:
    """Turn a model result into an auditable report.

    The pipeline refuses NaN/inf values and marks uncalibrated predictions,
    preventing demo output from being mistaken for laboratory measurement.
    """

    def analyze_impedance(
        self, sample_id: str, impedance: complex, parameters: Mapping[str, Any],
        calibration: LinearCalibration | None = None,
    ) -> ChemicalRFReport:
        if not sample_id.strip():
            raise ValueError("sample_id is required")
        if not all(map(lambda x: abs(float(x)) < float("inf"), (impedance.real, impedance.imag))):
            raise ValueError("impedance must be finite")
        corrected = calibration.apply(impedance) if calibration else impedance
        payload = {"sample_id": sample_id, "impedance": [corrected.real, corrected.imag], "parameters": dict(parameters)}
        digest = sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
        warnings = [] if calibration else ["uncalibrated equivalent-circuit prediction"]
        return ChemicalRFReport(sample_id, corrected, reflection_coefficient(corrected), calibration.residual_rms_ohm if calibration else None, digest, warnings)

    @staticmethod
    def record(report: ChemicalRFReport) -> ExperimentRecord:
        record = ExperimentRecord(report.sample_id, "chemical-rf-impedance")
        record.results["impedance_real_ohm"] = Measurement(report.impedance_ohm.real, "ohm", source="pipeline")
        record.results["impedance_imag_ohm"] = Measurement(report.impedance_ohm.imag, "ohm", source="pipeline")
        record.parameters["provenance_hash"] = report.provenance_hash
        return record
