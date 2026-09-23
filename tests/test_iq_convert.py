"""Tests for canonical IQ-to-NPZ conversion."""
from pathlib import Path

import numpy as np
import pytest
from click.testing import CliRunner

from vulture.iq_cli import iq
from vulture.sdr_iq_framework.convert import convert_iq_to_npz
from vulture.sdr_iq_framework.partition import write_iq_file


def test_convert_preserves_samples_and_writes_metadata(tmp_path: Path) -> None:
    iq_path = tmp_path / "capture.iq"
    npz_path = tmp_path / "capture.npz"
    samples = np.asarray([1 + 2j, -0.5 + 0.25j], dtype=np.complex64)
    write_iq_file(iq_path, samples, 2_000_000)

    result = convert_iq_to_npz(iq_path, npz_path, source="sdr")
    with np.load(npz_path) as archive:
        assert np.array_equal(archive["iq"], samples)
        assert float(archive["sample_rate"]) == 2_000_000
        assert str(archive["source"]) == "sdr"
        assert str(archive["format"]) == "complex64-le"
        assert str(archive["dtype"]) == "complex64"
        assert int(archive["sample_count"]) == 2
        assert str(archive["sha256"]) == result["sha256"]


def test_conversion_requires_iq_and_does_not_overwrite(tmp_path: Path) -> None:
    source = tmp_path / "capture.npy"
    np.save(source, np.asarray([1 + 0j], dtype=np.complex64))
    with pytest.raises(ValueError, match="canonical .iq"):
        convert_iq_to_npz(source, tmp_path / "capture.npz")

    iq_path = tmp_path / "capture.iq"
    output = tmp_path / "capture.npz"
    write_iq_file(iq_path, np.asarray([1 + 0j], dtype=np.complex64), 10)
    convert_iq_to_npz(iq_path, output)
    with pytest.raises(FileExistsError):
        convert_iq_to_npz(iq_path, output)


def test_iq_convert_command_outputs_json(tmp_path: Path) -> None:
    iq_path = tmp_path / "capture.iq"
    npz_path = tmp_path / "capture.npz"
    write_iq_file(iq_path, np.asarray([1 + 0j], dtype=np.complex64), 10)
    result = CliRunner().invoke(iq, ["convert", str(iq_path), str(npz_path)])
    assert result.exit_code == 0, result.output
    assert json.loads(result.output)["output"] == str(npz_path)
