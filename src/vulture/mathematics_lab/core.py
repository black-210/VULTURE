"""Mathematics Laboratory: small helpers for linear algebra and numeric ops."""
import numpy as np


def normalize_vector(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v)
    return v / n if n != 0 else v
