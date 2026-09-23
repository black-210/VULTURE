"""VULTURE RF-DNA receive-only adapter helpers.

This module deliberately avoids discovery or opening hardware unless the user has
explicitly configured a receive-only backend and is operating under the approved
lab or deployment constraints.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def discover_backend_status() -> dict[str, object]:
    """Return a safe backend capability report without opening hardware."""
    status: dict[str, object] = {
        "mode": "offline-deterministic",
        "local_npz": True,
        "simulator": True,
        "soapy_available": False,
        "device_count": 0,
        "device_args_required": True,
        "network_probe": False,
        "transmit": False,
        "receive_only": True,
        "discovery": "explicit-only",
        "message": "No hardware is opened automatically. SDR access remains explicit and user-configured.",
    }
    try:
        import SoapySDR  # type: ignore

        status["soapy_available"] = True
        status["message"] = "SoapySDR bindings are installed; explicit receive-only configuration is still required."
    except Exception:
        status["message"] = "No SDR runtime is available; VULTURE remains in offline mode."
    return status


def _read_iq_file(path: str | Path) -> np.ndarray:
    sample_path = Path(path)
    if not sample_path.exists():
        raise FileNotFoundError(f"{sample_path} does not exist")

    try:
        values = np.loadtxt(sample_path, delimiter=",", comments="#")
    except ValueError:
        values = np.loadtxt(sample_path, comments="#")

    values = np.asarray(values, dtype=np.float64)
    if values.size == 0:
        raise ValueError(f"no numeric data found in {sample_path}")
    if values.ndim == 1:
        if values.size % 2 != 0:
            raise ValueError(f"IQ file {sample_path} must contain even numbers of values")
        values = values.reshape(-1, 2)
    elif values.ndim != 2 or values.shape[1] < 2:
        raise ValueError(f"IQ file {sample_path} must contain interleaved I,Q pairs")
    return (values[:, 0] + 1j * values[:, 1]).astype(np.complex64)


def convert_iq_to_npz(
    input_path: str | Path,
    output_path: str | Path,
    sample_rate: float,
    center_frequency: float = 0.0,
    source: str = "converted",
) -> dict[str, object]:
    """Convert a local I/Q file into a canonical NPZ capture."""
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    iq = _read_iq_file(input_path)
    out_path = Path(output_path)
    if out_path.parent:
        out_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out_path,
        iq=np.asarray(iq, dtype=np.complex64),
        sample_rate=float(sample_rate),
        center_frequency=float(center_frequency),
        source=str(source),
    )
    return {
        "input": str(input_path),
        "output": str(out_path),
        "samples": int(iq.size),
        "sample_rate": float(sample_rate),
        "center_frequency": float(center_frequency),
        "source": str(source),
    }


__all__ = ["discover_backend_status", "convert_iq_to_npz"]
