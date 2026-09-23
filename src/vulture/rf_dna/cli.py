"""Receive-only SDR and canonical .iq boundary.

Synthetic generation is intentionally not part of this module. Offline input
must be a canonical little-endian complex64 .iq capture with a JSON sidecar.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from vulture.sdr_iq_framework.partition import read_iq_file, write_iq_file


@dataclass(frozen=True)
class ReceiveConfig:
    sample_rate: float
    center_frequency: float
    gain: float | None = None
    device_args: str | None = None
    channel: int = 0


class ReceiveOnlySource:
    """Read canonical .iq captures or an explicitly configured RX device."""

    def __init__(self, config: ReceiveConfig):
        if config.sample_rate <= 0 or config.center_frequency < 0:
            raise ValueError("invalid receive configuration")
        if config.channel < 0:
            raise ValueError("channel must be non-negative")
        self.config = config

    @staticmethod
    def is_soapysdr_available() -> bool:
        try:
            import SoapySDR  # type: ignore
            return True
        except Exception:
            return False

    @staticmethod
    def from_iq(path: str | Path, sample_rate: float | None = None) -> tuple[np.ndarray, float]:
        iq, rate = read_iq_file(path, sample_rate)
        if rate is None:
            raise ValueError(".iq capture requires a positive sample rate or .json sidecar")
        return iq, rate

    @staticmethod
    def from_npz(path: str | Path) -> tuple[np.ndarray, float]:
        raise RuntimeError("NPZ fixtures are disabled; use a canonical .iq capture")

    @staticmethod
    def from_file_or_sdr(path: str | Path | None = None, config: ReceiveConfig | None = None):
        if path is not None:
            if Path(path).suffix.lower() != ".iq":
                raise ValueError("input must be a canonical .iq capture")
            return ReceiveOnlySource.from_iq(path)
        if config is None:
            raise ValueError("provide --input capture.iq or a configured SDR receive config")
        return ReceiveOnlySource(config)

    def open_soapysdr(self):  # pragma: no cover - requires optional hardware
        if not self.config.device_args:
            raise ValueError("device_args must be explicitly configured")
        if not self.is_soapysdr_available():
            raise RuntimeError("SoapySDR runtime is unavailable")
        import SoapySDR  # type: ignore
        device = SoapySDR.Device(self.config.device_args)
        direction = SoapySDR.SOAPY_SDR_RX
        channel = self.config.channel
        device.setSampleRate(direction, channel, self.config.sample_rate)
        device.setFrequency(direction, channel, self.config.center_frequency)
        if self.config.gain is not None:
            device.setGain(direction, channel, self.config.gain)
        stream = device.setupStream(direction, SoapySDR.SOAPY_SDR_CF32, [channel])
        device.activateStream(stream)
        return device, stream

    def capture_to_iq(self, path: str | Path, sample_count: int, chunk_size: int = 16_384) -> int:
        """Capture receive-only samples from the configured SDR into .iq."""
        if sample_count <= 0 or chunk_size <= 0:
            raise ValueError("sample_count and chunk_size must be positive")
        import SoapySDR  # type: ignore
        device, stream = self.open_soapysdr()
        samples: list[np.ndarray] = []
        remaining = sample_count
        try:
            while remaining:
                count = min(chunk_size, remaining)
                buffer = np.empty(count, dtype=np.complex64)
                result = device.readStream(stream, [buffer], count)
                if result.ret <= 0:
                    raise RuntimeError(f"SDR read failed with code {result.ret}")
                samples.append(buffer[:result.ret].copy())
                remaining -= result.ret
        finally:
            device.deactivateStream(stream)
            device.closeStream(stream)
        write_iq_file(path, np.concatenate(samples), self.config.sample_rate)
        return sample_count
