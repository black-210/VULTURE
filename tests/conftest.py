"""Conftest for pytest configuration."""
import pytest
import numpy as np

@pytest.fixture
def sample_signal():
    return np.sin(2 * np.pi * 0.1 * np.arange(1000))

@pytest.fixture
def iq_data():
    return np.exp(1j * 2 * np.pi * 0.1 * np.arange(1000))

@pytest.fixture
def random_data():
    return np.random.randn(1000)
