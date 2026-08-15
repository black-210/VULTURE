"""
RTL-SDR adapter using pyrtlsdr if available. Provides a minimal device wrapper compatible
with the HardwareInterface defined in vulture/sdr/hardware.py.
"""
from typing import Optional, Any, Dict

try:
    import numpy as np
except Exception:
    np = None

try:
    from rtlsdr import RtlSdr  # type: ignore
except Exception:
    RtlSdr = None

from .hardware import HardwareInterface

class RTLSDRDevice(HardwareInterface):
    def __init__(self, device: Optional[str] = None, cfg: Optional[Dict[str, Any]] = None):
        super().__init__(device=device, cfg=cfg)
        self.sdr = None
        self._is_running = False

    def start(self):
        if RtlSdr is None:
            raise RuntimeError("pyrtlsdr is required to use RTLSDRDevice")
        self.sdr = RtlSdr()
        # Apply basic configuration if provided
        if self.cfg:
            if "sample_rate" in self.cfg:
                self.sdr.sample_rate = float(self.cfg["sample_rate"])
            if "center_freq" in self.cfg:
                self.sdr.center_freq = float(self.cfg["center_freq"])
            if "gain" in self.cfg:
                self.sdr.gain = float(self.cfg["gain"])
        self._is_running = True

    def stop(self):
        if self.sdr is not None:
            try:
                self.sdr.close()
            except Exception:
                pass
        self.sdr = None
        self._is_running = False

    def read_samples(self, num_samples: int = 1024) -> Any:
        if not self._is_running or self.sdr is None:
            raise RuntimeError("Device not started")
        samples = self.sdr.read_samples(num_samples)
        # Ensure numpy array return type if numpy available
        if np is not None:
            return np.asarray(samples)
        return samples
