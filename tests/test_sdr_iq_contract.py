"""Canonical SDR IQ integration tests."""
from pathlib import Path
import numpy as np
import pytest
from vulture.rf_dna.cli import ReceiveOnlySource
from vulture.sdr_iq_framework.partition import write_iq_file

def test_only_iq_files_are_accepted(tmp_path: Path):
    path = tmp_path / "capture.iq"
    write_iq_file(path, np.array([1+2j], dtype=np.complex64), 1_000_000)
    data, rate = ReceiveOnlySource.from_file_or_sdr(path=path)
    assert data.dtype == np.complex64 and rate == 1_000_000
    with pytest.raises(ValueError):
        ReceiveOnlySource.from_file_or_sdr(path=tmp_path / "capture.npz")

def test_npz_emulation_is_disabled():
    with pytest.raises(RuntimeError, match="disabled"):
        ReceiveOnlySource.from_npz("capture.npz")
