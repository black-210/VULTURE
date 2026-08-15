"""Medical research utilities: ECG/EEG minimal analyzers.

Research-only helpers; does not provide clinical-grade functionality.
"""
import numpy as np


def simple_ecg_qrs_detect(signal: np.ndarray) -> int:
    # naive energy thresholding for QRS-like peaks
    signal = np.abs(signal)
    return int((signal > (np.mean(signal) + 2 * np.std(signal))).sum())
