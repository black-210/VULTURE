"""pytest configuration and fixtures for VULTURE."""

import pytest
import numpy as np
from scipy import signal

@pytest.fixture
def sample_signal():
    """Generate sample signal."""
    t = np.arange(0, 1, 1/1e6)
    return np.sin(2*np.pi*1e3*t) + 0.1*np.random.randn(len(t))

@pytest.fixture
def iq_data():
    """Generate IQ signal."""
    t = np.arange(0, 1, 1/1e6)
    return np.exp(1j * 2*np.pi*1e3*t) + 0.05*np.random.randn(len(t))

@pytest.fixture
def random_data():
    """Generate random data."""
    return np.random.randn(10000)

@pytest.fixture
def bpsk_signal():
    """Generate BPSK signal."""
    bits = np.random.randint(0, 2, 1000)
    symbols = 2*bits - 1
    t = np.arange(0, len(symbols)*10, 1)
    carrier = np.sin(2*np.pi*0.01*t)
    return (np.repeat(symbols, 10) * carrier)

@pytest.fixture
def qpsk_signal():
    """Generate QPSK signal."""
    bits = np.random.randint(0, 4, 1000)
    symbols = np.exp(1j * np.pi/2 * bits)
    return np.repeat(symbols, 100)

@pytest.fixture
def chirp_signal():
    """Generate chirp signal."""
    t = np.linspace(0, 1, 1e6)
    return signal.chirp(t, 100, 1, 1000)

@pytest.fixture
def burst_signal():
    """Generate burst signal."""
    t = np.arange(0, 1, 1/1e6)
    burst1 = np.sin(2*np.pi*1e3*t[0:200000])
    silence = np.zeros(300000)
    burst2 = np.sin(2*np.pi*1e3*t[0:200000])
    burst3 = np.zeros(300000)
    return np.concatenate([burst1, silence, burst2, burst3])

@pytest.fixture
def multipath_signal():
    """Generate multipath signal."""
    t = np.arange(0, 1, 1/1e6)
    direct = np.sin(2*np.pi*1e3*t)
    path1 = 0.5*np.sin(2*np.pi*1e3*(t-0.0001))
    path2 = 0.3*np.sin(2*np.pi*1e3*(t-0.0002))
    return direct + path1 + path2