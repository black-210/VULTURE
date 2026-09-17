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
