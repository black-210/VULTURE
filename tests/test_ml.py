import pytest
from vulture.ml import extract_basic_features, detect_gpu


def test_extract_basic_features():
    data = [0, 1, 2, 3, 4]
    feats = extract_basic_features(data)
    assert "mean" in feats and "rms" in feats


def test_detect_gpu():
    # detect_gpu should return a string or None, but must not raise
    dev = detect_gpu()
    assert dev is None or isinstance(dev, str)
