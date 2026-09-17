"""RF-DNA feature summary and simulated report utilities for README and CLI use."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from .dashboard import build_capture_from_npz
from .experiment_suite import run_quantum_experiment
from .fingerprint import extract_fingerprint
from .simulator import generate_iq


def rf_dna_status() -> dict[str, Any]:
    """Return a compact status packet for the locally installed RF-DNA tool."""
    return {
        "tool": "vulture-rf-dna",
        "receive_only": True,
        "tenant_isolation": True,
        "tls_required_for_remote": True,
        "hardware_optional": True,
        "status": "ready",
        "safe_operations": ["simulate", "fingerprint", "dashboard", "provenance", "quantum-baseline"],
    }


def generate_report(input_path: str | Path, label: str = "capture") -> dict[str, Any]:
    """Create an informative summary report from a local capture."""
    capture = build_capture_from_npz(input_path, label=label)
    iq = np.asarray(np.load(input_path)["iq"], dtype=np.complex64)
    fp = extract_fingerprint(iq, float(np.load(input_path)["sample_rate"]))
    return {
        "label": label,
        "summary": {
            "sample_count": int(iq.size),
            "digest": fp.digest,
            "rms_amplitude": fp.rms_amplitude,
            "peak_amplitude": fp.peak_amplitude,
            "spectral_centroid_hz": fp.spectral_centroid_hz,
        },
        "dashboard": capture.to_dict(),
    }


def simulate_quantum_workflow(profile: str = "multi-tone", duration: float = 2.0, sample_rate: float = 1_000_000.0, seed: int = 7) -> dict[str, Any]:
    """Run a deterministic local workflow and include a classical baseline."""
    iq = generate_iq(profile, duration, sample_rate, seed=seed)
    qresult = run_quantum_experiment(iq, sample_rate, seed=seed)
    return {
        "profile": profile,
        "sample_count": int(iq.size),
        "sample_rate": float(sample_rate),
        "quantum_experiment": qresult,
        "status": "simulated",
    }
