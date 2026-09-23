"""Canonical IQ-to-NPZ conversion for the Python analysis pipeline."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import numpy as np

from .partition import IQFileError, read_iq_file


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def convert_iq_to_npz(
    input_path: str | Path,
    output_path: str | Path,
    *,
    source: str = "recorded_iq",
    overwrite: bool = False,
) -> dict[str, Any]:
    """Convert a canonical ``.iq`` capture to an analysis-ready NPZ archive.

    The conversion preserves the complex64 samples and sample-rate metadata. It
    does not synthesize samples or claim that a file came from hardware. The
    NPZ contains ``iq``, ``sample_rate``, ``source``, ``format``, ``sha256``,
    ``sample_count``, and ``dtype`` fields for downstream RF-DNA commands.
    """
    input_file = Path(input_path)
    output_file = Path(output_path)
    if input_file.suffix.lower() != ".iq":
        raise IQFileError("IQ-to-NPZ conversion requires a canonical .iq input")
    if output_file.suffix.lower() != ".npz":
        raise IQFileError("IQ-to-NPZ conversion requires a .npz output")
    if output_file.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output_file}")

    samples, sample_rate = read_iq_file(input_file)
    if sample_rate is None:
        raise IQFileError(".iq input requires a positive sample rate in its .json sidecar")

    digest = _sha256(input_file)
    metadata = {
        "source": str(source),
        "format": "complex64-le",
        "sha256": digest,
        "sample_count": int(samples.size),
        "dtype": "complex64",
        "sample_rate": float(sample_rate),
    }
    np.savez_compressed(
        output_file,
        iq=np.asarray(samples, dtype=np.complex64),
        sample_rate=metadata["sample_rate"],
        source=metadata["source"],
        format=metadata["format"],
        sha256=metadata["sha256"],
        sample_count=metadata["sample_count"],
        dtype=metadata["dtype"],
    )
    return {"input": str(input_file), "output": str(output_file), **metadata}
