"""Pytest configuration and fixtures."""

import pytest
import numpy as np
from scipy import signal


@pytest.fixture
def sample_signal():
    """Generate clean test signal."""
    fs = 1000
    t = np.arange(0, 1, 1/fs)
    return np.sin(2 * np.pi * 50 * t)


@pytest.fixture
def iq_data():
    """Generate complex IQ test data."""
    return np.exp(1j * 2 * np.pi * 0.1 * np.arange(10000))


@pytest.fixture
def random_data():
    """Generate random test data."""
    np.random.seed(42)
    return np.random.randn(1000)


@pytest.fixture
def feature_matrix():
    """Generate feature matrix."""
    np.random.seed(42)
    return np.random.randn(100, 10)
