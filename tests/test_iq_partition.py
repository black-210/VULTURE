"""Tests for the shared C/Python complex IQ file contract."""
from pathlib import Path

import numpy as np
import pytest

from vulture.sdr_iq_framework.partition import IQFileError, read_iq_file, write_iq_file


def test_iq_round_trip_uses_complex64_and_metadata(tmp_path: Path) -> None:
    path = tmp_path / "capture.iq"
    original = np.asarray([1 + 2j, -0.5 + 0.25j], dtype=np.complex128)
    write_iq_file(path, original, 2_000_000)
    loaded, rate = read_iq_file(path)
    assert loaded.dtype == np.complex64
    assert np.allclose(loaded, original)
    assert rate == 2_000_000


def test_reader_accepts_iq_npz_contract(tmp_path: Path) -> None:
    path = tmp_path / "capture.npz"
    np.savez(path, iq=np.asarray([1 + 1j], dtype=np.complex64), sample_rate=10)
    samples, rate = read_iq_file(path)
    assert samples[0] == 1 + 1j
    assert rate == 10


def test_reader_rejects_real_or_empty_data(tmp_path: Path) -> None:
    real_path = tmp_path / "real.npy"
    np.save(real_path, np.ones(2))
    with pytest.raises(IQFileError):
        read_iq_file(real_path)
    empty_path = tmp_path / "empty.iq"
    empty_path.write_bytes(b"")
    with pytest.raises(IQFileError):
        read_iq_file(empty_path)
