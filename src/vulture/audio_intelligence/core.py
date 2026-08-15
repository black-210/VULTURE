"""Audio Intelligence: simple feature extraction placeholders."""
import numpy as np


def rms(audio: np.ndarray) -> float:
    audio = np.asarray(audio)
    return float(np.sqrt(np.mean(audio.astype(float) ** 2)))
