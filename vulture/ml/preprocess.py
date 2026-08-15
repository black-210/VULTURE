from typing import Any, Tuple

try:
    import numpy as np
except Exception:  # pragma: no cover - optional
    np = None


def scale_minmax(X: Any, feature_range: Tuple[float, float] = (0.0, 1.0)) -> Any:
    """Min-max scale array-like X to given feature_range.

    Falls back to returning X if numpy not available.
    """
    if np is None:
        return X
    X = np.asarray(X, dtype=float)
    minv = X.min(axis=0)
    maxv = X.max(axis=0)
    scale = (feature_range[1] - feature_range[0]) / (maxv - minv + 1e-12)
    return feature_range[0] + (X - minv) * scale


def standardize(X: Any) -> Any:
    """Zero-mean unit-variance standardization."""
    if np is None:
        return X
    X = np.asarray(X, dtype=float)
    mean = X.mean(axis=0)
    std = X.std(axis=0) + 1e-12
    return (X - mean) / std


def to_tensor(X: Any):
    """Convert array-like to torch tensor if torch is available, otherwise return numpy array."""
    try:
        import torch
        return torch.from_numpy(X) if hasattr(X, "__array__") else torch.tensor(X)
    except Exception:
        return X
