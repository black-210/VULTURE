"""Hardware abstraction layer for SDR devices.

This module provides a small, testable abstraction over real SDR device APIs
(like pyrtlsdr, SoapySDR, UHD). The implementation here is a safe stub that
can be extended to integrate with real hardware in a single place.
"""
from typing import Optional
import numpy as np


class HardwareAbstraction:
    """A minimal hardware abstraction for SDRs.

    Methods are intentionally limited and synchronous. Replace internals with
    actual device calls (pyrtlsdr, SoapySDR) when wiring to hardware.
    """

    def __init__(self, device: str = "rtlsdr"):
        self.device = device
        self.opened = False
        self.center_freq = None
        self.sample_rate = None

    def open_device(self):
        # In a real implementation, open device handles here.
        self.opened = True

    def set_center_freq(self, freq: float):
        self.center_freq = float(freq)

    def set_sample_rate(self, rate: float):
        self.sample_rate = float(rate)

    def set_gain(self, gain: Optional[str] = None):
        # Accept 'auto' or numeric values
        self.gain = gain

    def read_samples(self, num_samples: int = 1024):
        # Replace with real device read. Here we simulate complex zeros.
        return np.zeros(num_samples, dtype=np.complex64)

    def close_device(self):
        self.opened = False
