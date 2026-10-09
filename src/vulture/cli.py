"""VULTURE CLI: offline RF, chemistry, physics, mathematics & forensic audit.

This CLI delivers local science and forensic capabilities without
network access, hardware probing, or RF transmission.
"""
from __future__ import annotations

import json
from pathlib import Path

import click
import numpy as np

from .forensic_cli import forensic_cli
from .lab_cli import lab_cli
from .offline_tools.cli import offline_cli
from .iq_cli import iq
from .interactive_shell import InteractiveShell


def _load_capture(path: str) -> tuple[np.ndarray, float]:
    """Load a capture file from NPZ or IQ format."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Capture file not found: {path}")

    suffix = file_path.suffix.lower()

    if suffix == ".npz":
        data = np.load(file_path)
        samples = data.get("iq")
        if samples is None:
            raise ValueError(f"NPZ file missing 'iq' array: {path}")
        sample_rate = float(data.get("sample_rate", 1_000_000))
        return np.asarray(samples), sample_rate

    if suffix == ".iq":
        from vulture.sdr_iq_framework.partition import read_iq_file

        samples, sample_rate = read_iq_file(file_path)
        if sample_rate is None:
            raise ValueError(
                f"""
Why?
The IQ samples do not contain their sample rate.
VULTURE requires it to interpret the capture correctly."""
            )
        return np.asarray(samples), float(sample_rate)

    else:
        raise ValueError(f"Unsupported format: {file_path.suffix}. Use .npz or .iq files.")


@click.group(invoke_without_command=True)
@click.option("--interactive", is_flag=True, help="Open the interactive > prompt.")
@click.pass_context
def cli(ctx: click.Context, interactive: bool) -> None:
    """🦅 VULTURE — offline RF, chemistry, physics, mathematics and evidence audit CLI."""
    if interactive:
        InteractiveShell().run()
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# Register every maintained command group in the canonical console entry point.
cli.add_command(lab_cli, name="lab")
cli.add_command(iq, name="iq")
cli.add_command(offline_cli, name="offline")
cli.add_command(forensic_cli, name="forensic")


@cli.command()
def info() -> None:
    """Display platform capabilities."""
    click.echo("🦅 VULTURE")
    click.echo("Science: chemistry • physics • mathematics • RF")
    click.echo("Forensics: offline audit of supplied evidence only")
    click.echo("Formats supported: .npz, .iq (all analysis commands)")
    click.echo("SDR Receiver: receive-only mode for RTL-SDR, HackRF, USRP")
    click.echo("RF-DNA: vulture rf-dna --help")
    click.echo("RF-Vulnerability: vulture rf-vuln --help")
    click.echo("Chemical-RF: vulture chemical-rf --help")
    click.echo("Forensic: vulture forensic --help")
    click.echo("SDR: vulture sdr --help")
    click.echo("IQ: vulture iq --help (convert .iq ↔ .npz)")
    click.echo("Offline analysis: vulture offline --help")
    click.echo("Lab: vulture lab --help")
    click.echo("Interactive: vulture --interactive")


@cli.command()
def status() -> None:
    """Show safe runtime status."""
    payload = {
        "cli": "online",
        "mode": "offline-deterministic",
        "hardware": "not-opened",
        "network": "disabled",
        "rf_transmit": "disabled",
        "analysis": "local-only",
        "rf_dna_command": "vulture rf-dna",
        "rf_vuln_command": "vulture rf-vuln",
        "capture_formats": ["npz", "iq"],
        "forensic_formats": ["npz", "iq"],
        "sdr_mode": "receive-only"
    }
    click.echo(json.dumps(payload, indent=2, sort_keys=True))


@cli.group("chemical-rf")
def chemical_rf() -> None:
    """Chemistry and RF analysis commands operating on NPZ or IQ captures."""


@chemical_rf.command("nmr")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="NPZ or IQ capture file")
@click.option("--nucleus", default="1H", show_default=True)
@click.option("--field-t", default=7.0, type=float, show_default=True)
def nmr(input_path: str, nucleus: str, field_t: float) -> None:
    """Offline NMR spectroscopy analysis from a local capture file."""
    from vulture.chemical_rf.spectroscopy import compute_nmr_spectrum

    samples, sample_rate = _load_capture(input_path)
    spectrum = compute_nmr_spectrum(
        samples,
        sample_rate=sample_rate,
        nucleus=nucleus,
        field_strength_tesla=field_t,
    )
    click.echo(json.dumps(spectrum.to_dict(), indent=2, sort_keys=True))


@chemical_rf.command("path-loss")
@click.option("--frequency-hz", required=True, type=float)
@click.option("--distance-m", required=True, type=float)
@click.option("--antenna-gain-dbi", default=0.0, type=float, show_default=True)
def path_loss(frequency_hz: float, distance_m: float, antenna_gain_dbi: float) -> None:
    """Calculate free-space path loss in dB."""
    from vulture.chemical_rf.science import free_space_path_loss_db

    loss_db = free_space_path_loss_db(
        frequency_hz=frequency_hz,
        distance_m=distance_m,
        antenna_gain_dbi=antenna_gain_dbi,
    )
    click.echo(json.dumps({"frequency_hz": frequency_hz, "distance_m": distance_m, "path_loss_db": loss_db}, indent=2))


@chemical_rf.command("wavelength")
@click.option("--frequency-hz", required=True, type=float)
def wavelength(frequency_hz: float) -> None:
    """Calculate wavelength from frequency."""
    from vulture.chemical_rf.science import wavelength_m

    wave_m = wavelength_m(frequency_hz)
    click.echo(json.dumps({"frequency_hz": frequency_hz, "wavelength_m": wave_m}, indent=2))


@cli.group("rf-vuln")
def rf_vuln() -> None:
    """Offline RF vulnerability and device compromise assessment."""


@rf_vuln.command("device")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="NPZ or IQ capture file")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--output", type=click.Path(dir_okay=False))
@click.option("--format", "fmt", type=click.Choice(["json", "txt", "html"]), default="json", show_default=True)
def rf_vuln_device(input_path: str, case_id: str, subject: str, frequency_hz: float, output: str | None, fmt: str) -> None:
    """Run forensic device compromise analysis against an offline capture."""
    from vulture.forensic_analyzer import ForensicAnalyzer

    samples, sample_rate = _load_capture(input_path)
    analyzer = ForensicAnalyzer(case_id, subject)
    analysis = analyzer.analyze_iq_capture(samples, sample_rate, frequency_hz)

    if fmt == "json":
        payload = analysis.to_json()
    elif fmt == "html":
        payload = """<!DOCTYPE html><html><head><title>VULTURE RF Vulnerability Report</title></head><body><h1>RF Vulnerability Assessment</h1><pre>""" + analysis.to_text().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</pre></body></html>"
    else:
        payload = analysis.to_text()

    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload)
        click.echo(f"Report saved to {output}")
    click.echo(payload)


@rf_vuln.command("report")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="NPZ or IQ capture file")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--output", type=click.Path(dir_okay=False), required=True)
@click.option("--format", "fmt", type=click.Choice(["json", "txt", "html"]), default="json", show_default=True)
def rf_vuln_report(input_path: str, case_id: str, subject: str, frequency_hz: float, output: str, fmt: str) -> None:
    """Write RF vulnerability assessment report to disk."""
    from vulture.forensic_analyzer import ForensicAnalyzer

    samples, sample_rate = _load_capture(input_path)
    analyzer = ForensicAnalyzer(case_id, subject)
    analysis = analyzer.analyze_iq_capture(samples, sample_rate, frequency_hz)

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if fmt == "json":
        content = analysis.to_json()
    elif fmt == "txt":
        content = analysis.to_text()
    else:
        content = """<!DOCTYPE html><html><head><title>VULTURE RF Vulnerability Report</title></head><body><h1>RF Vulnerability Assessment</h1><pre>""" + analysis.to_text().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</pre></body></html>"

    output_path.write_text(content)
    click.echo(f"✓ Report saved to {output}")
    click.echo(f"  Format: {fmt}")
    click.echo(f"  Evidence Hash: {analysis.evidence_hash}")


@cli.group("rf-dna")
def rf_dna() -> None:
    """Integrated receive-only RF-DNA simulation, analysis, and reporting commands."""


def _run_rf_dna(args: tuple[str, ...]) -> None:
    """Forward integrated commands to the existing RF-DNA Click group."""
    from vulture.rf_dna.cli import cli as rf_dna_cli

    rf_dna_cli.main(list(args), standalone_mode=False)


@rf_dna.command("status")
def rf_dna_status() -> None:
    """Show RF-DNA capabilities through the main VULTURE command."""
    _run_rf_dna(("status",))


@rf_dna.command("simulate")
@click.option("--profile", default="noise", show_default=True)
@click.option("--duration", type=float, default=1.0, show_default=True)
@click.option("--sample-rate", type=float, default=1_000_000, show_default=True)
@click.option("--seed", type=int, default=7, show_default=True)
@click.option("--output", type=click.Path(dir_okay=False), required=True)
def rf_dna_simulate(profile: str, duration: float, sample_rate: float, seed: int, output: str) -> None:
    """Simulate an RF-DNA profile and save to .npz."""
    _run_rf_dna(("simulate", "--profile", profile, "--duration", str(duration), "--sample-rate", str(sample_rate), "--seed", str(seed), "--output", output))


@rf_dna.command("analyze")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="NPZ or IQ capture file")
@click.option("--frequency-hz", required=True, type=float)
def rf_dna_analyze(input_path: str, frequency_hz: float) -> None:
    """Analyze RF-DNA fingerprint from a capture file."""
    _run_rf_dna(("analyze", "--input", input_path, "--frequency-hz", str(frequency_hz)))


if __name__ == "__main__":
    cli()
