"""Receive-only SDR boundary.

The adapter accepts local files and an optional explicitly configured SoapySDR
backend. It intentionally exposes no transmit, tuning-scan, or network-probe
operations. Hardware integration remains optional and environment-dependent.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import click
import numpy as np


@dataclass(frozen=True)
class ReceiveConfig:
    sample_rate: float
    center_frequency: float
    gain: float | None = None
    device_args: str | None = None


def discover_backend_status() -> dict[str, object]:
    """Report optional receive backends without opening hardware or probing networks."""
    status: dict[str, object] = {
        "mode": "offline-deterministic",
        "local_npz": True,
        "simulator": True,
        "soapy_available": False,
        "device_count": 0,
        "device_args_required": True,
        "network_probe": False,
        "transmit": False,
        "receive_only": True,
        "discovery": "explicit-only",
        "message": "No hardware is opened automatically. SDR access remains explicit and user-configured.",
    }
    try:
        import SoapySDR  # type: ignore

        status["soapy_available"] = True
        status["message"] = "SoapySDR bindings are installed; explicit receive-only configuration is still required."
    except Exception:
        status["message"] = "No SDR runtime is available; VULTURE remains in offline mode."
    return status


def _read_float_pairs(path: str | Path) -> np.ndarray:
    """Read interleaved real/imag pairs from a local IQ or complex file."""
    sample_path = Path(path)
    if not sample_path.exists():
        raise FileNotFoundError(f"{sample_path} does not exist")

    suffix = sample_path.suffix.lower()
    if suffix == ".npz":
        with np.load(sample_path) as data:
            if "iq" not in data:
                raise ValueError("NPZ must contain an 'iq' array")
            values = np.asarray(data["iq"], dtype=np.complex64)
        return values

    try:
        raw = np.loadtxt(sample_path, delimiter=",", comments="#")
    except ValueError:
        try:
            raw = np.loadtxt(sample_path, comments="#")
        except ValueError as exc:
            raise ValueError(f"could not parse IQ payload in {sample_path}") from exc

    values = np.asarray(raw, dtype=np.float64)
    if values.size == 0:
        raise ValueError(f"no numeric samples found in {sample_path}")

    if values.ndim == 1:
        if values.size % 2 != 0:
            raise ValueError(f"IQ samples in {sample_path} must be provided as interleaved I,Q pairs")
        values = values.reshape(-1, 2)
    elif values.ndim != 2 or values.shape[1] < 2:
        raise ValueError(f"IQ samples in {sample_path} must have at least two columns")

    if values.shape[1] == 2:
        return (values[:, 0] + 1j * values[:, 1]).astype(np.complex64)

    if values.shape[1] >= 2:
        return (values[:, 0] + 1j * values[:, 1]).astype(np.complex64)

    raise ValueError(f"unsupported sample layout in {sample_path}")


def convert_iq_to_npz(
    input_path: str | Path,
    output_path: str | Path,
    sample_rate: float,
    center_frequency: float = 0.0,
    source: str = "converted",
) -> dict[str, object]:
    """Convert local complex/IQ files to a canonical NPZ capture without hardware access."""
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")

    iq = _read_float_pairs(input_path)
    if iq.size == 0:
        raise ValueError("converted capture is empty")

    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out_path,
        iq=np.asarray(iq, dtype=np.complex64),
        sample_rate=float(sample_rate),
        center_frequency=float(center_frequency),
        source=str(source),
    )
    return {
        "input": str(input_path),
        "output": str(out_path),
        "samples": int(iq.size),
        "sample_rate": float(sample_rate),
        "center_frequency": float(center_frequency),
        "source": str(source),
        "mode": "offline-deterministic",
    }


class ReceiveOnlySource:
    """Read IQ from a local NPZ file or an approved attached receiver."""

    def __init__(self, config: ReceiveConfig):
        if config.sample_rate <= 0 or config.center_frequency < 0:
            raise ValueError("invalid receive configuration")
        self.config = config

    @staticmethod
    def is_soapysdr_available() -> bool:
        """Check if an explicit receive backend is installed."""
        try:
            import SoapySDR  # type: ignore
            return True
        except Exception:
            return False

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

    @staticmethod
    def from_iq_file(path: str | Path) -> tuple[np.ndarray, float]:
        """Load an interleaved I,Q text or binary payload into complex samples."""
        iq = _read_float_pairs(path)
        if iq.size == 0:
            raise ValueError("no complex samples were found")
        return iq.astype(np.complex64), 1.0

    @staticmethod
    def from_complex_file(path: str | Path, sample_rate: float = 1.0) -> tuple[np.ndarray, float]:
        """Load a complex-valued or I,Q file and attach an explicit sample rate."""
        iq = _read_float_pairs(path)
        if iq.size == 0:
            raise ValueError("no complex samples were found")
        if sample_rate <= 0:
            raise ValueError("sample_rate must be positive")
        return iq.astype(np.complex64), float(sample_rate)

    @staticmethod
    def from_file_or_sdr(path: str | Path | None = None, config: ReceiveConfig | None = None):
        """Prefer local IQ fixtures and fail cleanly without an SDR backend."""
        if path is not None:
            return ReceiveOnlySource.from_npz(path)

        if config is None:
            raise ValueError("provide --input or a configured SDR receive config")

        if not ReceiveOnlySource.is_soapysdr_available():
            raise RuntimeError(
                "No SDR backend is installed. VULTURE remains in offline mode; "
                "use a local .npz capture or an approved offline IQ file."
            )

        return ReceiveOnlySource(config)

    def open_soapysdr(self):  # pragma: no cover - requires optional hardware
        """Open an explicitly configured SoapySDR RX stream, if installed.

        This method is opt-in and receive-only. It does not discover devices or
        transmit. Deployments must enforce their own allowlist and permissions.
        """
        if not self.config.device_args:
            raise ValueError("device_args must be explicitly configured")
        if not self.is_soapysdr_available():
            raise RuntimeError("SoapySDR runtime is unavailable; offline mode is required")
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


@click.group()
def cli() -> None:
    """Receive-only SDR workflow and conversion tools."""


@cli.command("status")
def status_command() -> None:
    """Return a safe backend status payload without opening hardware."""
    click.echo(json.dumps(discover_backend_status(), indent=2, sort_keys=True))


@cli.command("discover")
def discover_command() -> None:
    """Report whether an explicit SDR backend is available for approved use."""
    click.echo(json.dumps(discover_backend_status(), indent=2, sort_keys=True))


@cli.command("convert")
@click.option("--input", "input_path", required=True, type=click.Path(exists=True, dir_okay=False))
@click.option("--output", "output_path", required=True, type=click.Path(dir_okay=False))
@click.option("--sample-rate", required=True, type=float)
@click.option("--center-frequency", default=0.0, type=float)
@click.option("--source", default="converted")
def convert_command(input_path: str, output_path: str, sample_rate: float, center_frequency: float, source: str) -> None:
    """Convert local I/Q or complex samples into a canonical NPZ capture."""
    result = convert_iq_to_npz(
        input_path=input_path,
        output_path=output_path,
        sample_rate=sample_rate,
        center_frequency=center_frequency,
        source=source,
    )
    click.echo(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    cli()


__all__ = [
    "ReceiveConfig",
    "ReceiveOnlySource",
    "convert_iq_to_npz",
    "discover_backend_status",
    "cli",
]
