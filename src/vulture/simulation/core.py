"""Simulation framework: basic signal and communication simulators."""
import numpy as np


def sin_wave(freq: float, fs: float, length: int):
    t = np.arange(length) / fs
    return np.sin(2 * np.pi * freq * t)
