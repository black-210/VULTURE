"""Tests for truthful IQ capture manifests."""
from pathlib import Path

import numpy as np
import pytest

from vulture.sdr_iq_framework.capture_manifest import (
    canonicalize_iq_capture,
    summarize_iq_capture,
)
from vulture.sdr_iq_framework.partition import write_iq_file


def test_summary_contains_integrity_and_signal_fields(tmp_path: Path) -> None:
    path = tmp_path / "capture.iq"
    write_iq_file(path, np.asarray([1 + 0j, 0 + 1j], dtype=np.complex64), 10)
    result = summarize_iq_capture(path, source="sdr", require_hardware=True)
    assert result["hardware_verified"] is True
    assert len(result["sha256"]) == 64
    assert result["samples"] == 2


def test_canonicalization_preserves_synthetic_provenance(tmp_path: Path) -> None:
    source = tmp_path / "source.iq"
    output = tmp_path / "canonical.iq"
    write_iq_file(source, np.asarray([1 + 2j], dtype=np.complex64), 100)
    result = canonicalize_iq_capture(source, output, source="simulation")
    assert result["hardware_verified"] is False
    assert output.with_suffix(".manifest.json").exists()
    with pytest.raises(ValueError, match="synthetic provenance"):
        canonicalize_iq_capture(source, tmp_path / "rejected.iq", source="simulation", require_hardware=True)
