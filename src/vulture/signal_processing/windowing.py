"""Windowing functions for signal processing."""
import numpy as np
from scipy import signal
import logging
logger = logging.getLogger(__name__)
class WindowingFunctions:
    WINDOWS = ['hann', 'hamming', 'blackman', 'bartlett', 'kaiser', 'tukey', 'rectangular']
    @staticmethod
    def get_window(window_type, size, param=None):
        if window_type == 'kaiser' and param:
            return signal.get_window((window_type, param), size)
        elif window_type == 'tukey' and param:
            return signal.get_window((window_type, param), size)
        else:
            return signal.get_window(window_type, size)
    @staticmethod
    def apply_window(data, window_type='hann'):
        window = signal.get_window(window_type, len(data))
        return data * window
    @staticmethod
    def get_scallop_loss(window_type):
        windows_loss = {'hann': 1.45, 'hamming': 1.30, 'blackman': 1.1, 'bartlett': 1.27, 'rectangular': 3.92}
        return windows_loss.get(window_type, 0)