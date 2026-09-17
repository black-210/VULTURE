"""CLI for safe, local RF-DNA simulator and fingerprint operations."""
from __future__ import annotations

import json
from pathlib import Path
import click
import numpy as np

from .fingerprint import extract_fingerprint
from .sdr_adapter import ReceiveOnlySource
from .simulator import generate_iq, save_npz


@click.group()
def cli() -> None:
    """VULTURE RF-DNA receive-only research utilities."""


@cli.command()
@click.option("--profile", default="noise", show_default=True)
@click.option("--duration", type=float, default=1.0, show_default=True)
@click.option("--sample-rate", type=float, default=1_000_000, show_default=True)
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), required=True)
def simulate(profile: str, duration: float, sample_rate: float, output: Path) -> None:
    """Generate a deterministic local IQ fixture; no SDR or network is used."""
    iq = generate_iq(profile, duration, sample_rate)
    save_npz(output, iq, sample_rate)
    click.echo(json.dumps({"output": str(output), "samples": int(iq.size), "profile": profile}, indent=2))


@cli.command()
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True)
@click.option("--label", default="unlabelled", show_default=True)
def fingerprint(input_path: Path, label: str) -> None:
    """Extract a descriptive fingerprint from a local NPZ capture."""
    iq, rate = ReceiveOnlySource.from_npz(input_path)
    result = extract_fingerprint(iq, rate).to_dict()
    result["label"] = label
    result["source"] = str(input_path)
    click.echo(json.dumps(result, indent=2, sort_keys=True))


@cli.command()
def backends() -> None:
    """Report optional receive backends without probing hardware or networks."""
    try:
        import SoapySDR  # type: ignore  # noqa: F401
        soapy = True
    except ImportError:
        soapy = False
    click.echo(json.dumps({"local_npz": True, "simulator": True, "soapysdr_installed": soapy, "transmit": False, "network_probe": False}, indent=2))


if __name__ == "__main__":
    cli()
