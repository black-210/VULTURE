import pytest
import numpy as np
from vulture.dsp.peak_detection import detect_peaks


def test_detect_peaks_prominence_or_fallback():
    x = np.zeros(100)
    x[20] = 1.0
    x[50] = 2.0
    x[80] = 0.8
    out = detect_peaks(x, prominence=0.5)
    assert 'peaks' in out
    assert 50 in out['peaks']
