"""Authorized red-team/blue-team laboratory simulations.

These scenarios generate deterministic local evidence and defensive telemetry.
They never send packets, access networks, transmit RF, or exploit a target.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import random
from typing import Any


@dataclass(frozen=True)
class LabResult:
    scenario: str
    mode: str
    status: str
    observations: list[dict[str, Any]]
    controls: list[str]
    evidence_sha256: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _result(scenario: str, observations: list[dict[str, Any]], controls: list[str]) -> LabResult:
    payload = {"scenario": scenario, "observations": observations, "controls": controls}
    digest = sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return LabResult(scenario, "AUTHORIZED_OFFLINE_LAB", "SIMULATED", observations, controls, digest, datetime.now(timezone.utc).isoformat())


def attack_simulation(scenario: str, seed: int = 7) -> LabResult:
    """Model an adversarial RF/cyber scenario without executing it."""
    rng = random.Random(seed)
    observations = [
        {"stage": "threat_model", "scenario": scenario, "target": "synthetic-lab-target"},
        {"stage": "signal_model", "samples": 4096, "snr_db": round(rng.uniform(8.0, 24.0), 2), "transmission": False},
        {"stage": "impact_estimate", "risk": "research-only", "external_access": False},
    ]
    controls = ["no_network", "no_rf_transmit", "synthetic_data_only", "human_approval_required"]
    return _result(scenario, observations, controls)


def defense_simulation(scenario: str, seed: int = 11) -> LabResult:
    """Evaluate defensive detection against deterministic synthetic telemetry."""
    rng = random.Random(seed)
    observations = [
        {"stage": "baseline", "window_samples": 4096, "noise_floor_db": round(-92 + rng.random() * 3, 2)},
        {"stage": "detector", "scenario": scenario, "anomaly_score": round(rng.random(), 4)},
        {"stage": "response_plan", "action": "alert_and_quarantine_capture", "automatic_transmit": False},
    ]
    controls = ["local_capture_only", "no_active_countermeasure", "audit_log", "operator_review"]
    return _result(scenario, observations, controls)
