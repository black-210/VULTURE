"""Sample rate management."""
import numpy as np
import logging
from scipy import signal
logger = logging.getLogger(__name__)
class SampleRateManager:
    @staticmethod
    def resample(data, original_rate, target_rate):
        if original_rate == target_rate:
            return data
        num_samples = int(len(data) * target_rate / original_rate)
        return signal.resample(data, num_samples)
    @staticmethod
    def decimate(data, factor):
        return signal.decimate(data, factor)
    @staticmethod
    def interpolate(data, factor):
        return signal.resample_poly(data, factor, 1)
    @staticmethod
    def get_supported_rates():
        return [8000, 11025, 16000, 22050, 44100, 48000, 96000, 192000, 2e6, 4e6, 8e6]