"""Offline vulnerability-style checks and forensic evidence reports.

This module audits supplied data and configuration; it does not probe hosts,
transmit RF, exploit protocols, or execute chemistry. Findings are framed as
risk indicators requiring human/laboratory validation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class Finding:
    domain: str
    code: str
    severity: str
    title: str
    evidence: str
    recommendation: str


@dataclass
class ForensicReport:
    case_id: str
    subject: str
    created_at: str
    input_sha256: str
    mode: str = "offline-audit"
    findings: list[Finding] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["findings"] = [asdict(item) for item in self.findings]
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True, ensure_ascii=False)

    def to_text(self) -> str:
        lines = [
            "VULTURE FORENSIC OFFLINE AUDIT",
            f"Case: {self.case_id}", f"Subject: {self.subject}",
            f"Created: {self.created_at}", f"Input SHA-256: {self.input_sha256}",
            f"Mode: {self.mode}", "",
        ]
        for index, finding in enumerate(self.findings, 1):
            lines.extend([
                f"[{index}] {finding.severity} {finding.domain}/{finding.code}: {finding.title}",
                f"Evidence: {finding.evidence}",
                f"Recommendation: {finding.recommendation}", "",
            ])
        if not self.findings:
            lines.append("No indicators found by the selected offline checks.")
        return "\n".join(lines)


def _digest(value: Any) -> str:
    if isinstance(value, bytes):
        raw = value
    else:
        raw = json.dumps(value, sort_keys=True, default=str, ensure_ascii=False).encode()
    return sha256(raw).hexdigest()


def _report(case_id: str, subject: str, payload: Any, findings: list[Finding], metadata: dict[str, Any] | None = None) -> ForensicReport:
    if not case_id.strip() or not subject.strip():
        raise ValueError("case_id and subject are required")
    return ForensicReport(case_id, subject, datetime.now(timezone.utc).isoformat(), _digest(payload), findings=findings, metadata=metadata or {})


def audit_physics(case_id: str, subject: str, *, frequency_hz: float, distance_m: float, bandwidth_hz: float | None = None) -> ForensicReport:
    findings: list[Finding] = []
    if frequency_hz <= 0 or distance_m <= 0:
        findings.append(Finding("physics", "PHY-001", "high", "Invalid physical parameters", "frequency and distance must be positive", "Reject the measurement and preserve the original input."))
    if bandwidth_hz is not None and (bandwidth_hz <= 0 or bandwidth_hz > frequency_hz * 2):
        findings.append(Finding("physics", "PHY-002", "medium", "Implausible bandwidth", f"bandwidth_hz={bandwidth_hz}", "Check instrument span, sample rate, and unit conversion."))
    return _report(case_id, subject, {"frequency_hz": frequency_hz, "distance_m": distance_m, "bandwidth_hz": bandwidth_hz}, findings)


def audit_chemistry(case_id: str, subject: str, compounds: Sequence[Mapping[str, Any]]) -> ForensicReport:
    findings: list[Finding] = []
    for index, compound in enumerate(compounds):
        elements = compound.get("elements")
        if not isinstance(elements, Mapping) or not elements:
            findings.append(Finding("chemistry", "CHEM-001", "high", "Missing composition", f"compound index {index}", "Supply a validated elemental composition before balancing."))
            continue
        for element, count in elements.items():
            if not isinstance(element, str) or not element or not isinstance(count, (int, float)) or count <= 0 or not math.isfinite(float(count)):
                findings.append(Finding("chemistry", "CHEM-002", "high", "Invalid elemental count", f"{element}={count}", "Use positive finite atom counts and validate the formula."))
    return _report(case_id, subject, list(compounds), findings)


def audit_mathematics(case_id: str, subject: str, matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> ForensicReport:
    findings: list[Finding] = []
    rows = [list(row) for row in matrix]
    if not rows or any(len(row) != len(rows) for row in rows) or len(vector) != len(rows):
        findings.append(Finding("mathematics", "MATH-001", "high", "Malformed linear system", "matrix is not square or vector length differs", "Provide a square system with matching dimensions."))
    elif any(not math.isfinite(float(value)) for row in rows for value in row) or any(not math.isfinite(float(value)) for value in vector):
        findings.append(Finding("mathematics", "MATH-002", "high", "Non-finite numerical input", "NaN or infinity detected", "Reject the dataset and trace the producing calculation."))
    return _report(case_id, subject, {"matrix": rows, "vector": list(vector)}, findings)


def audit_protocol(case_id: str, subject: str, frames: Iterable[Mapping[str, Any]]) -> ForensicReport:
    findings: list[Finding] = []
    frame_list = list(frames)
    for index, frame in enumerate(frame_list):
        length = frame.get("length")
        declared = frame.get("declared_length")
        if isinstance(length, int) and isinstance(declared, int) and length != declared:
            findings.append(Finding("protocol", "PROTO-001", "high", "Length-field mismatch", f"frame {index}: declared={declared}, observed={length}", "Quarantine the capture and validate framing before decoding."))
        if frame.get("checksum_valid") is False:
            findings.append(Finding("protocol", "PROTO-002", "medium", "Checksum failure", f"frame {index}", "Preserve the raw frame and compare against a trusted decoder."))
        if frame.get("version") in (None, "", 0):
            findings.append(Finding("protocol", "PROTO-003", "low", "Missing protocol version", f"frame {index}", "Record the protocol version and capture metadata."))
    return _report(case_id, subject, frame_list, findings)


def write_report(report: ForensicReport, output: str | Path, fmt: str = "json") -> Path:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        path.write_text(report.to_json() + "\n", encoding="utf-8")
    elif fmt == "txt":
        path.write_text(report.to_text() + "\n", encoding="utf-8")
    else:
        raise ValueError("fmt must be json or txt")
    return path
