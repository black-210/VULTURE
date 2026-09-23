"""Auditable SDR/IQ capture summary and canonicalization helpers.

This module never upgrades synthetic samples into real measurements. It can
canonicalize an existing IQ recording and emit a compact JSON manifest, or
summarize a capture produced by an explicitly configured receive-only SDR.
Synthetic provenance is preserved and rejected when ``require_hardware`` is
requested.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
from typing import Any

import numpy as np

from .partition import IQFileError, read_iq_file, write_iq_file


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def summarize_iq_capture(
    path: str | Path,
    *,
    source: str = "recorded_iq",
    require_hardware: bool = False,
) -> dict[str, Any]:
    """Return a truthful, JSON-serializable summary for a canonical ``.iq`` file."""
    capture = Path(path)
    if capture.suffix.lower() != ".iq":
        raise IQFileError("capture summaries require a canonical .iq file")
    if source.lower() in {"simulation", "simulated", "emulator", "fixture"} and require_hardware:
        raise ValueError("synthetic provenance cannot be presented as hardware capture")
    samples, sample_rate = read_iq_file(capture)
    magnitude = np.abs(samples)
    power = magnitude * magnitude
    return {
        "format": "complex64-le",
        "source": source,
        "hardware_verified": source.lower() in {"sdr", "hardware", "recorded_iq"},
        "path": str(capture),
        "sha256": _sha256(capture),
        "samples": int(samples.size),
        "sample_rate_hz": float(sample_rate) if sample_rate is not None else None,
        "duration_s": float(samples.size / sample_rate) if sample_rate else None,
        "dtype": str(samples.dtype),
        "mean_i": float(samples.real.mean()),
        "mean_q": float(samples.imag.mean()),
        "rms": float(np.sqrt(power.mean())),
        "peak": float(magnitude.max()),
        "mean_power": float(power.mean()),
        "software": "vulture",
        "python": platform.python_version(),
    }


def canonicalize_iq_capture(
    source_path: str | Path,
    output_path: str | Path,
    *,
    source: str = "recorded_iq",
    require_hardware: bool = False,
) -> dict[str, Any]:
    """Copy a real IQ recording to canonical form and write its manifest.

    This is a format conversion, not a simulation-to-hardware conversion. The
    manifest retains the supplied provenance and ``hardware_verified`` status.
    """
    source_file = Path(source_path)
    output_file = Path(output_path)
    samples, rate = read_iq_file(source_file)
    if rate is None:
        raise IQFileError("source capture must provide sample rate metadata")
    if source.lower() in {"simulation", "simulated", "emulator", "fixture"} and require_hardware:
        raise ValueError("cannot certify simulated input as hardware capture")
    write_iq_file(output_file, samples, rate)
    summary = summarize_iq_capture(output_file, source=source, require_hardware=require_hardware)
    manifest = output_file.with_suffix(".manifest.json")
    manifest.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary
