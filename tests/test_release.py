"""Release metadata regression tests."""

from vulture import __version__
from vulture.release import RELEASE_VERSION, release_status


def test_release_metadata_is_consistent():
    status = release_status()
    assert __version__ == RELEASE_VERSION == "3.0.0"
    assert status["expected_release"] == "3.0.0"
    assert status["network"] == "disabled"
