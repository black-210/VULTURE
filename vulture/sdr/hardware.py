from typing import Optional, Dict, Any

class HardwareInterface:
    """Abstract hardware interface for SDR devices (RTLSDR, UHD, Pluto, etc.)."""

    def __init__(self, device: Optional[str] = None, cfg: Optional[Dict[str, Any]] = None) -> None:
        self.device = device
        self.cfg = cfg or {}

    def start(self):
        """Open device and start streaming. Override in concrete implementations."""
        raise NotImplementedError

    def stop(self):
        """Stop streaming and close device."""
        raise NotImplementedError

    def read_samples(self, num_samples: int):
        """Read num_samples IQ samples from device."""
        raise NotImplementedError
