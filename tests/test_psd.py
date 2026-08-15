import pytest
import numpy as np
from vulture.dsp.psd_scipy import compute_psd


def test_compute_psd_welch_or_fallback():
    # generate a test tone + noise
    fs = 1024
    t = np.arange(0, 1.0, 1.0 / fs)
    signal = np.sin(2 * np.pi * 50 * t) + 0.1 * np.random.randn(len(t))
    out = compute_psd(signal, fs=fs, method='welch', nperseg=256)
    assert 'freqs' in out and 'psd' in out
    assert len(out['freqs']) == len(out['psd'])
