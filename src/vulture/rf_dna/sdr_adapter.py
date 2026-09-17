"""Receive-only SDR boundary.

The adapter accepts local files and an optional explicitly configured SoapySDR
backend. It intentionally exposes no transmit, tuning-scan, or network-probe
operations. Hardware integration remains optional and environment-dependent.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import numpy as np


@dataclass(frozen=True)
class ReceiveConfig:
    sample_rate: float
    center_frequency: float
    gain: float | None = None
    device_args: str | None = None


class ReceiveOnlySource:
    """Read IQ from a local NPZ file or an approved attached receiver."""

    def __init__(self, config: ReceiveConfig):
        if config.sample_rate <= 0 or config.center_frequency < 0:
            raise ValueError("invalid receive configuration")
        self.config = config

    @staticmethod
    def from_npz(path: str | Path) -> tuple[np.ndarray, float]:
        """Load a local simulator/recording capture without network access."""
        with np.load(path) as data:
            if "iq" not in data:
                raise ValueError("NPZ must contain an 'iq' array")
            iq = np.asarray(data["iq"], dtype=np.complex64)
            rate = float(data["sample_rate"]) if "sample_rate" in data else 0.0
        if iq.size == 0 or rate <= 0:
            raise ValueError("capture must contain samples and a positive sample_rate")
        return iq, rate

    def open_soapysdr(self):  # pragma: no cover - requires optional hardware
        """Open an explicitly configured SoapySDR RX stream, if installed.

        This method is opt-in and receive-only. It does not discover devices or
        transmit. Deployments must enforce their own allowlist and permissions.
        """
        if not self.config.device_args:
            raise ValueError("device_args must be explicitly configured")
        try:
            import SoapySDR  # type: ignore
        except ImportError as exc:
            raise RuntimeError("install the approved SoapySDR Python bindings first") from exc
        device = SoapySDR.Device(self.config.device_args)
        device.setSampleRate(SoapySDR.SOAPY_SDR_RX, 0, self.config.sample_rate)
        device.setFrequency(SoapySDR.SOAPY_SDR_RX, 0, self.config.center_frequency)
        if self.config.gain is not None:
            device.setGain(SoapySDR.SOAPY_SDR_RX, 0, self.config.gain)
        stream = device.setupStream(SoapySDR.SOAPY_SDR_RX, SoapySDR.SOAPY_SDR_CF32)
        device.activateStream(stream)
        return device, stream
