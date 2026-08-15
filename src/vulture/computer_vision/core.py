"""Computer Vision basic loader and adapter placeholders."""
from typing import Tuple
import numpy as np


def load_image(path: str) -> np.ndarray:
    """Minimal stub for image loading; replace with PIL/OpenCV in full build."""
    # Return a tiny dummy image so code can run without optional deps
    return np.zeros((10, 10, 3), dtype=np.uint8)
