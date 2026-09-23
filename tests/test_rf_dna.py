import numpy as np

from vulture.rf_dna.fingerprint import extract_fingerprint, similarity
from vulture.rf_dna.simulator import generate_iq


def test_simulator_is_deterministic():
    assert np.array_equal(generate_iq("cw", 0.01, 10_000), generate_iq("cw", 0.01, 10_000))


def test_fingerprint_is_stable_and_comparable():
    left = extract_fingerprint(generate_iq("cw", 0.01, 10_000), 10_000)
    right = extract_fingerprint(generate_iq("cw", 0.01, 10_000), 10_000)
    assert left.digest == right.digest
    assert similarity(left, right) == 1.0


def test_receive_safe_profiles_are_available():
    assert generate_iq("noise", 0.001, 10_000).dtype == np.complex64


def test_discovery_status_is_safe():
    from vulture.rf_dna.cli import discover_backend_status

    status = discover_backend_status()
    assert status["mode"] == "offline-deterministic"
    assert status["transmit"] is False
    assert status["network_probe"] is False


def test_complex_to_npz_conversion(tmp_path):
    from vulture.rf_dna.cli import convert_iq_to_npz

    capture = tmp_path / "capture.iq"
    samples = np.array([1.0, 0.0, 0.5, 0.5, -0.25, 0.25], dtype=np.float32)
    capture.write_bytes(samples.tobytes())

    output = tmp_path / "capture.npz"
    result = convert_iq_to_npz(capture, output, sample_rate=1_000_000.0)

    data = np.load(output)
    assert "iq" in data
    assert "sample_rate" in data
    assert result["samples"] == 3
    assert data["sample_rate"] == 1_000_000.0
