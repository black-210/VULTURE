"""Receive-only RF-DNA CLI with deterministic local analysis and reporting."""
from __future__ import annotations

import json
from pathlib import Path

import click
import numpy as np

from vulture.rf_dna.dashboard import build_capture_from_npz, build_dashboard_summary
from vulture.rf_dna.experiment_suite import run_quantum_experiment
from vulture.rf_dna.fingerprint import extract_fingerprint
from vulture.rf_dna.reporting import generate_report, rf_dna_status
from vulture.rf_dna.simulator import generate_iq, save_npz


@click.group(name="rf-dna")
def cli() -> None:
    """Receive-only RF-DNA simulation, fingerprinting, and reporting commands."""


@cli.command("status")
def status() -> None:
    """Return the safe status payload for the RF-DNA tool."""
    click.echo(json.dumps(rf_dna_status(), indent=2, sort_keys=True))


@cli.command("simulate")
@click.option("--profile", default="noise", show_default=True)
@click.option("--duration", type=float, default=1.0, show_default=True)
@click.option("--sample-rate", type=float, default=1_000_000, show_default=True)
@click.option("--seed", type=int, default=7, show_default=True)
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), required=True)
def simulate(profile: str, duration: float, sample_rate: float, seed: int, output: Path) -> None:
    """Generate a deterministic synthetic IQ capture without any SDR or network access."""
    iq = generate_iq(profile, duration, sample_rate, seed=seed)
    save_npz(output, iq, sample_rate)
    click.echo(
        json.dumps(
            {"output": str(output), "samples": int(iq.size), "profile": profile, "seed": seed},
            indent=2,
            sort_keys=True,
        )
    )


@cli.command("fingerprint")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True)
@click.option("--label", default="unlabelled", show_default=True)
def fingerprint(input_path: Path, label: str) -> None:
    """Extract a descriptive fingerprint from a local NPZ capture."""
    data = np.load(input_path)
    iq = np.asarray(data["iq"], dtype=np.complex64)
    sample_rate = float(data["sample_rate"])
    result = extract_fingerprint(iq, sample_rate).to_dict()
    result["label"] = label
    result["source"] = str(input_path)
    click.echo(json.dumps(result, indent=2, sort_keys=True))


@cli.command("dashboard")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True)
@click.option("--label", default="dashboard-capture", show_default=True)
def dashboard(input_path: Path, label: str) -> None:
    """Create a dashboard summary and provenance report from a local capture."""
    capture = build_capture_from_npz(input_path, label=label)
    click.echo(json.dumps(build_dashboard_summary([capture]), indent=2, sort_keys=True))


@cli.command("report")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True)
@click.option("--label", default="capture-report", show_default=True)
def report(input_path: Path, label: str) -> None:
    """Create a machine-readable RF-DNA report from a local capture."""
    click.echo(json.dumps(generate_report(input_path, label=label), indent=2, sort_keys=True))


@cli.command("quantum")
@click.option("--profile", default="multi-tone", show_default=True)
@click.option("--duration", type=float, default=2.0, show_default=True)
@click.option("--sample-rate", type=float, default=1_000_000, show_default=True)
@click.option("--seed", type=int, default=7, show_default=True)
def quantum(profile: str, duration: float, sample_rate: float, seed: int) -> None:
    """Run a deterministic quantum-inspired RF baseline against a classical reference."""
    iq = generate_iq(profile, duration, sample_rate, seed=seed)
    click.echo(json.dumps(run_quantum_experiment(iq, sample_rate, seed=seed), indent=2, sort_keys=True))


@cli.command("backends")
def backends() -> None:
    """Report optional receive backends without probing hardware or networks."""
    try:
        import SoapySDR  # type: ignore  # noqa: F401

        soapy = True
    except ImportError:
        soapy = False

    click.echo(
        json.dumps(
            {
                "local_npz": True,
                "simulator": True,
                "soapysdr_installed": soapy,
                "offline_mode": not soapy,
                "transmit": False,
                "network_probe": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    cli()
