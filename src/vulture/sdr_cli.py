"""CLI commands for receive-only SDR operations.

This module exposes the SDR receiver interface through Click commands.
All operations are receive-only; transmission is disabled.
"""
from __future__ import annotations

import json
from pathlib import Path

import click
import numpy as np

from .sdr_receiver import (
    RTLSDRReceiver,
    HackRFReceiver,
    USRPReceiver,
    get_available_devices,
)


@click.group("sdr")
def sdr_cli() -> None:
    """Receive-only SDR operations for RTL-SDR, HackRF, and USRP devices."""


@sdr_cli.command("status")
def sdr_status() -> None:
    """Check backend availability and connected SDR devices.
    
    This command is receive-only and performs no transmission or hardware access.
    """
    available = get_available_devices()
    payload = {
        "available_devices": available,
        "receive_only": True,
        "transmission_disabled": True,
        "timestamp": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat(),
    }
    click.echo(json.dumps(payload, indent=2, sort_keys=True))


@sdr_cli.command("info")
@click.option(
    "--device",
    type=click.Choice(["rtl-sdr", "hackrf", "usrp"]),
    required=True,
    help="Device type",
)
def sdr_info(device: str) -> None:
    """Get hardware capabilities and specifications for a specific SDR device."""
    receiver = None
    if device == "rtl-sdr":
        receiver = RTLSDRReceiver()
    elif device == "hackrf":
        receiver = HackRFReceiver()
    elif device == "usrp":
        receiver = USRPReceiver()

    if receiver is None:
        raise ValueError(f"Unknown device type: {device}")

    if not receiver.connect():
        raise RuntimeError(f"Failed to connect to {device}")

    try:
        info = receiver.get_device_info()
        payload = {
            "available": info.available,
            "backend": info.backend,
            "device_type": info.device_type.value,
            "driver_loaded": info.driver_loaded,
            "frequency_range_hz": info.frequency_range_hz,
            "gain_range_db": info.gain_range_db,
            "model": info.model,
            "sample_rate_range_hz": info.sample_rate_range_hz,
            "serial_number": info.serial_number,
        }
        click.echo(json.dumps(payload, indent=2, sort_keys=True))
    finally:
        receiver.disconnect()


@sdr_cli.command("capture")
@click.option(
    "--device",
    type=click.Choice(["rtl-sdr", "hackrf"]),
    default="rtl-sdr",
    show_default=True,
    help="SDR device type",
)
@click.option(
    "--frequency-hz",
    type=float,
    required=True,
    help="Center frequency in Hz (e.g., 433920000 for 433.92 MHz)",
)
@click.option(
    "--sample-rate",
    type=float,
    required=True,
    help="Sample rate in Hz (must be within device capability)",
)
@click.option(
    "--gain-db",
    type=float,
    default=20.0,
    show_default=True,
    help="Receiver gain in dB",
)
@click.option(
    "--duration",
    type=float,
    default=5.0,
    show_default=True,
    help="Capture duration in seconds",
)
@click.option(
    "--output",
    type=click.Path(dir_okay=False),
    required=True,
    help="Output .npz file path",
)
def sdr_capture(
    device: str,
    frequency_hz: float,
    sample_rate: float,
    gain_db: float,
    duration: float,
    output: str,
) -> None:
    """Capture RF samples in receive-only mode and save to NPZ format with metadata.
    
    The output NPZ file contains:
    - iq: Complex64 IQ samples
    - sample_rate: Recorded sample rate
    - center_frequency: Center frequency in Hz
    - duration: Capture duration in seconds
    - gain_db: Receiver gain used
    """
    receiver = None
    if device == "rtl-sdr":
        receiver = RTLSDRReceiver()
    elif device == "hackrf":
        receiver = HackRFReceiver()
    else:
        raise ValueError(f"Unknown device type: {device}")

    if not receiver.connect():
        raise RuntimeError(f"Failed to connect to {device}")

    try:
        click.echo(f"Starting capture on {device}...")
        click.echo(f"  Frequency: {frequency_hz / 1e9:.3f} GHz")
        click.echo(f"  Sample Rate: {sample_rate / 1e6:.2f} Msps")
        click.echo(f"  Gain: {gain_db} dB")
        click.echo(f"  Duration: {duration} seconds")
        click.echo()

        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        metadata = receiver.capture_to_file(
            center_frequency_hz=frequency_hz,
            sample_rate_hz=sample_rate,
            gain_db=gain_db,
            duration_seconds=duration,
            output_path=output_path,
        )

        if metadata:
            click.echo("✓ Capture complete!")
            payload = {
                "capture_path": str(output_path),
                "center_frequency_hz": metadata.center_frequency_hz,
                "device_info": {
                    "available": metadata.device_info.available,
                    "backend": metadata.device_info.backend,
                    "device_type": metadata.device_info.device_type.value,
                    "driver_loaded": metadata.device_info.driver_loaded,
                    "frequency_range_hz": metadata.device_info.frequency_range_hz,
                    "gain_range_db": metadata.device_info.gain_range_db,
                    "model": metadata.device_info.model,
                    "sample_rate_range_hz": metadata.device_info.sample_rate_range_hz,
                    "serial_number": metadata.device_info.serial_number,
                },
                "duration_seconds": metadata.duration_seconds,
                "end_time": metadata.end_time,
                "gain_db": metadata.gain_db,
                "sample_rate_actual": metadata.sample_rate_actual,
                "sample_rate_hz": metadata.sample_rate_hz,
                "samples_collected": metadata.samples_collected,
                "start_time": metadata.start_time,
            }
            click.echo(json.dumps(payload, indent=2, sort_keys=True))
        else:
            raise RuntimeError("Capture failed")
    finally:
        receiver.disconnect()


@sdr_cli.command("scan")
@click.option(
    "--device",
    type=click.Choice(["rtl-sdr", "hackrf"]),
    default="rtl-sdr",
    show_default=True,
    help="SDR device type",
)
@click.option(
    "--freq-start",
    type=float,
    required=True,
    help="Start frequency in Hz (e.g., 88000000 for 88 MHz)",
)
@click.option(
    "--freq-stop",
    type=float,
    required=True,
    help="Stop frequency in Hz (e.g., 108000000 for 108 MHz)",
)
@click.option(
    "--sample-rate",
    type=float,
    required=True,
    help="Sample rate in Hz",
)
@click.option(
    "--gain-db",
    type=float,
    default=20.0,
    show_default=True,
    help="Receiver gain in dB",
)
@click.option(
    "--step-hz",
    type=float,
    default=1000000,
    show_default=True,
    help="Frequency step size in Hz (e.g., 1000000 for 1 MHz)",
)
def sdr_scan(
    device: str,
    freq_start: float,
    freq_stop: float,
    sample_rate: float,
    gain_db: float,
    step_hz: float,
) -> None:
    """Scan a frequency range in receive-only mode and report signal strength.
    
    Reports signal strength (dBm) at each frequency step across the specified range.
    """
    receiver = None
    if device == "rtl-sdr":
        receiver = RTLSDRReceiver()
    elif device == "hackrf":
        receiver = HackRFReceiver()
    else:
        raise ValueError(f"Unknown device type: {device}")

    if not receiver.connect():
        raise RuntimeError(f"Failed to connect to {device}")

    try:
        click.echo(f"Scanning {freq_start / 1e6:.0f} - {freq_stop / 1e6:.0f} MHz on {device}")
        click.echo(f"Sample Rate: {sample_rate / 1e6:.2f} Msps, Gain: {gain_db} dB")
        click.echo()
        click.echo("Frequency Scan Results:")
        click.echo("Frequency (MHz) | Signal Strength (dBm)")
        click.echo("------------------------------------------")

        results = []
        freq = freq_start
        while freq <= freq_stop:
            if not receiver.set_frequency(freq):
                raise RuntimeError(f"Failed to set frequency to {freq} Hz")
            if not receiver.set_sample_rate(sample_rate):
                raise RuntimeError(f"Failed to set sample rate to {sample_rate} Hz")
            if not receiver.set_gain(gain_db):
                raise RuntimeError(f"Failed to set gain to {gain_db} dB")

            if not receiver.start_rx():
                raise RuntimeError("Failed to start RX")

            try:
                # Read samples to measure power
                num_samples = int(sample_rate * 0.1)  # 100ms of samples
                samples = receiver.read_samples(num_samples)
                if samples is not None:
                    power_linear = np.mean(np.abs(samples) ** 2)
                    power_dbm = 10 * np.log10(power_linear + 1e-10)
                    results.append((freq / 1e6, power_dbm))
                    click.echo(f"{freq / 1e6:10.1f}   |{power_dbm:15.1f}")
            finally:
                receiver.stop_rx()

            freq += step_hz

        click.echo()
        click.echo("✓ Scan complete")
    finally:
        receiver.disconnect()
