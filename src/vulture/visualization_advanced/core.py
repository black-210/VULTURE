"""Advanced visualization placeholders: spectrum and waterfall render helpers."""
import numpy as np


def spectrum_to_image(spectrum: np.ndarray, height: int = 256) -> np.ndarray:
    spec = np.asarray(spectrum)
    img = np.tile(spec.reshape(-1, 1), (1, height))
    return img
