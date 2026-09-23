"""Shared file boundary for the C and Python SDR partitions.

The partitions intentionally share one representation: little-endian complex64
samples in a ``.iq`` file, with an optional sidecar ``.json`` containing the
sample rate.  NPZ/NPY remain useful for Python fixtures, but are not required
by the C side.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np


class IQFileError(ValueError):
    """Raised when a shared IQ capture is missing or malformed."""


def _validate(samples: np.ndarray, sample_rate: float | None) -> tuple[np.ndarray, float | None]:
    samples = np.asarray(samples)
    if samples.ndim != 1:
        raise IQFileError("IQ data must be a one-dimensional complex array")
    if not np.iscomplexobj(samples):
        raise IQFileError("IQ data must contain complex samples")
    if samples.size == 0:
        raise IQFileError("IQ data must not be empty")
    if not np.isfinite(samples.real).all() or not np.isfinite(samples.imag).all():
        raise IQFileError("IQ data must contain only finite samples")
    if sample_rate is not None and (not np.isfinite(sample_rate) or sample_rate <= 0):
        raise IQFileError("sample_rate must be positive")
    return samples.astype(np.complex64, copy=False), sample_rate


def read_iq_file(path: str | Path, sample_rate: float | None = None) -> tuple[np.ndarray, float | None]:
    """Read the canonical ``.iq`` file or a compatible Python fixture.

    ``.iq`` is raw little-endian complex64 (I then Q for each sample).  A
    sibling ``<name>.json`` may provide ``{"sample_rate": ...}``; an explicit
    argument takes precedence.  ``.npz`` must contain ``iq`` and may contain
    ``sample_rate``.  No hardware discovery or reverse conversion is done.
    """
    path = Path(path)
    suffix = path.suffix.lower()
    rate = sample_rate
    if suffix == ".iq":
        samples = np.fromfile(path, dtype="<c8")
        if rate is None:
            metadata_path = path.with_suffix(".json")
            if metadata_path.exists():
                with metadata_path.open(encoding="utf-8") as handle:
                    rate = float(json.load(handle)["sample_rate"])
    elif suffix == ".npz":
        with np.load(path) as data:
            if "iq" not in data:
                raise IQFileError("NPZ must contain an 'iq' array")
            samples = data["iq"]
            if rate is None and "sample_rate" in data:
                rate = float(data["sample_rate"])
    elif suffix == ".npy":
        samples = np.load(path)
    else:
        raise IQFileError("expected a .iq, .npz, or .npy file")
    return _validate(samples, rate)


def write_iq_file(path: str | Path, samples: Any, sample_rate: float) -> None:
    """Write canonical complex64 IQ plus a sidecar sample-rate manifest."""
    array, rate = _validate(np.asarray(samples), float(sample_rate))
    path = Path(path)
    if path.suffix.lower() != ".iq":
        raise IQFileError("canonical SDR files must use the .iq extension")
    array.astype("<c8", copy=False).tofile(path)
    path.with_suffix(".json").write_text(
        json.dumps({"format": "complex64-le", "sample_rate": rate}, indent=2) + "\n",
        encoding="utf-8",
    )
