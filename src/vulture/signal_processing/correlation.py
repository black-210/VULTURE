"""Correlation and convolution operations."""
import numpy as np
from scipy import signal
import logging
logger = logging.getLogger(__name__)
class Correlation:
    @staticmethod
    def cross_correlation(x, y):
        return np.correlate(x, y, mode='full')
    @staticmethod
    def auto_correlation(x):
        return np.correlate(x, x, mode='full')
    @staticmethod
    def correlation_coefficient(x, y):
        return np.corrcoef(x, y)[0, 1]
    @staticmethod
    def convolution(x, h):
        return np.convolve(x, h, mode='full')
    @staticmethod
    def cross_correlation_fast(x, y):
        return signal.correlate(x, y, mode='same')