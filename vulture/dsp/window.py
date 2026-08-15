from typing import Any


def get_window(name: str, n: int):
    """Return window samples by name (hann, hamming, blackman)."""
    try:
        import numpy as np
    except Exception:
        raise RuntimeError("numpy is required for window functions")
    name = name.lower()
    if name == "hann":
        return np.hanning(n)
    if name == "hamming":
        return np.hamming(n)
    if name == "blackman":
        return np.blackman(n)
    # default rectangular
    return np.ones(n)
