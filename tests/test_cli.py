"""CLI for the VULTURE RF-DNA toolset.

This remains receive-only and never opens arbitrary networks or transmitters.
"""
from __future__ import annotations

import json
from pathlib import Path

import click

from .dashboard import build_capture_from_npz, build_dashboard_summary
from .experiment_suite import run_quantum_experiment
from .fingerprint import extract_fingerprint
from .reporting import generate_report, rf_dna_status, simulate_quantum_workflow
from .sdr_adapter import ReceiveOnlySource
from .simulator import generate_iq, save_npz


@click.group()
def cli() -> None:
    """VULTURE RF-DNA receive-only utilities, dashboard, provenance, and quantum baselines."""


@cli.command()
def status() -> None:
    """Return the status and safe capabilities for the local RF-DNA tool."""
    click.echo(json.dumps(rf_dna_status(), indent=2, sort_keys=True))


@cli.command()
@click.option("--profile", default="noise", show_default=True)
@click.option("--duration", type=float, default=1.0, show_default=True)
@click.option("--sample-rate", type=float, default=1_000_000, show_default=True)
@click.option("--seed", type=int, default=7, show_default=True)
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), required=True)
def simulate(profile: str, duration: float, sample_rate: float, seed: int, output: Path) -> None:
    """Generate a deterministic local IQ fixture; no SDR or network access is used."""
    iq = generate_iq(profile, duration, sample_rate, seed=seed)
    save_npz(output, iq, sample_rate)
    click.echo(json.dumps({"output": str(output), "samples": int(iq.size), "profile": profile, "seed": seed}, indent=2, sort_keys=True))


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
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True)
@click.option("--label", default="dashboard-capture", show_default=True)
def dashboard(input_path: Path, label: str) -> None:
    """Render a provenance-aware dashboard summary from a local capture."""
    capture = build_capture_from_npz(input_path, label=label)
    click.echo(json.dumps(build_dashboard_summary([capture]), indent=2, sort_keys=True))


@cli.command()
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True)
@click.option("--label", default="capture-report", show_default=True)
def report(input_path: Path, label: str) -> None:
    """Create a machine-readable local evidence report."""
    click.echo(json.dumps(generate_report(input_path, label=label), indent=2, sort_keys=True))


@cli.command()
@click.option("--profile", default="multi-tone", show_default=True)
@click.option("--duration", type=float, default=2.0, show_default=True)
@click.option("--sample-rate", type=float, default=1_000_000, show_default=True)
@click.option("--seed", type=int, default=7, show_default=True)
def quantum(profile: str, duration: float, sample_rate: float, seed: int) -> None:
    """Run a deterministic quantum-classical RF experiment prototype with a classical baseline."""
    iq = generate_iq(profile, duration, sample_rate, seed=seed)
    click.echo(json.dumps(run_quantum_experiment(iq, sample_rate, seed=seed), indent=2, sort_keys=True))


@cli.command()
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
