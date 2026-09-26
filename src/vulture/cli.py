"""VULTURE CLI with truthful, offline science and forensic capabilities.

The interactive prompt is intentionally a friendly ``>`` shell that exposes
real, local calculations and forensic audit checks. It does not scan live
systems, transmit RF, or attack targets.
"""
from __future__ import annotations

import json
import shlex
from pathlib import Path

import click
import numpy as np

from vulture.forensics import audit_chemistry, audit_mathematics, audit_physics, audit_protocol
from vulture.lab_cli import lab_cli
from vulture.offline_tools.cli import offline_cli
from vulture.iq_cli import iq


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
# These groups previously existed as independent Click modules but were not
# reachable through ``vulture``.
cli.add_command(lab_cli, name="lab")
cli.add_command(iq, name="iq")
cli.add_command(offline_cli, name="offline")


@cli.command()
def info() -> None:
    """Display platform capabilities."""
    click.echo("🦅 VULTURE")
    click.echo("Science: chemistry • physics • mathematics • RF")
    click.echo("Forensics: offline audit of supplied evidence only")
    click.echo("RF-DNA: vulture rf-dna --help")
    click.echo("Chemical-RF: vulture chemical-rf --help")
    click.echo("IQ: vulture iq --help")
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
    }
    click.echo(json.dumps(payload, indent=2, sort_keys=True))


@cli.group("chemical-rf")
def chemical_rf() -> None:
    """Chemistry and RF analysis commands operating on NPZ archives."""


@chemical_rf.command("nmr")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--nucleus", default="1H", show_default=True)
@click.option("--field-t", default=7.0, type=float, show_default=True)
def chemical_rf_nmr(input_path: str, nucleus: str, field_t: float) -> None:
    """Calculate Larmor frequency from NPZ archive metadata and store result."""
    from vulture.chemical_rf.spectroscopy import larmor_frequency_hz
    from vulture.sdr_iq_framework.partition import read_iq_file
    
    npz_file = Path(input_path)
    if not npz_file.exists():
        raise FileNotFoundError(f"NPZ file not found: {input_path}")
    
    # Load NPZ and extract sample rate if available
    data = np.load(npz_file)
    sample_rate = float(data.get("sample_rate", 1_000_000))
    
    # Calculate Larmor frequency
    freq_hz = larmor_frequency_hz(nucleus, field_t)
    
    result = {
        "input": str(input_path),
        "nucleus": nucleus,
        "field_t": field_t,
        "frequency_hz": freq_hz,
        "captured_sample_rate": sample_rate
    }
    click.echo(json.dumps(result, indent=2, sort_keys=True))


@chemical_rf.command("material")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--epsilon-r", required=True, type=float)
@click.option("--conductivity", default=0.0, type=float, show_default=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--length-m", required=True, type=float)
def chemical_rf_material(input_path: str, epsilon_r: float, conductivity: float, frequency_hz: float, length_m: float) -> None:
    """Analyze material properties against NPZ capture metadata."""
    from vulture.chemical_rf.materials import complex_permittivity, dielectric_resonance_frequency
    
    npz_file = Path(input_path)
    if not npz_file.exists():
        raise FileNotFoundError(f"NPZ file not found: {input_path}")
    
    # Load NPZ
    data = np.load(npz_file)
    sample_rate = float(data.get("sample_rate", 1_000_000))
    
    # Calculate material properties
    epsilon = complex_permittivity(epsilon_r, conductivity, frequency_hz)
    resonance = dielectric_resonance_frequency(epsilon_r, length_m)
    
    result = {
        "input": str(input_path),
        "captured_sample_rate": sample_rate,
        "permittivity": {
            "real": epsilon.real,
            "imag": epsilon.imag
        },
        "resonance_hz": resonance,
        "material": {
            "epsilon_r": epsilon_r,
            "conductivity": conductivity,
            "length_m": length_m
        }
    }
    click.echo(json.dumps(result, indent=2, sort_keys=True))


@chemical_rf.command("physics")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--distance-m", required=True, type=float)
def chemical_rf_physics(input_path: str, frequency_hz: float, distance_m: float) -> None:
    """Calculate RF physics properties with NPZ capture context."""
    from vulture.chemical_rf.science import free_space_path_loss_db, wavelength_m
    
    npz_file = Path(input_path)
    if not npz_file.exists():
        raise FileNotFoundError(f"NPZ file not found: {input_path}")
    
    # Load NPZ
    data = np.load(npz_file)
    sample_rate = float(data.get("sample_rate", 1_000_000))
    
    # Calculate RF physics
    wavelength = wavelength_m(frequency_hz)
    path_loss = free_space_path_loss_db(frequency_hz, distance_m)
    
    result = {
        "input": str(input_path),
        "captured_sample_rate": sample_rate,
        "frequency_hz": frequency_hz,
        "distance_m": distance_m,
        "wavelength_m": wavelength,
        "path_loss_db": path_loss
    }
    click.echo(json.dumps(result, indent=2, sort_keys=True))


@chemical_rf.command("report")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--sample-id", required=True)
@click.option("--real-ohm", required=True, type=float)
@click.option("--imag-ohm", required=True, type=float)
def chemical_rf_report(input_path: str, sample_id: str, real_ohm: float, imag_ohm: float) -> None:
    """Create impedance analysis report linked to NPZ capture."""
    from vulture.chemical_rf.pipeline import ChemicalRFAnalysisPipeline
    
    npz_file = Path(input_path)
    if not npz_file.exists():
        raise FileNotFoundError(f"NPZ file not found: {input_path}")
    
    # Load NPZ
    data = np.load(npz_file)
    sample_rate = float(data.get("sample_rate", 1_000_000))
    frequency_hz = float(data.get("frequency_hz", 2_400_000_000))
    
    # Generate report
    pipeline = ChemicalRFAnalysisPipeline()
    analysis = pipeline.analyze_impedance(
        sample_id,
        complex(real_ohm, imag_ohm),
        {"frequency_hz": frequency_hz, "source": str(input_path)}
    )
    
    result = analysis.to_dict()
    result["input"] = str(input_path)
    result["captured_sample_rate"] = sample_rate
    
    click.echo(json.dumps(result, indent=2, sort_keys=True))


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
    """Generate a deterministic local IQ fixture without hardware or network access."""
    _run_rf_dna(("simulate", "--profile", profile, "--duration", str(duration), "--sample-rate", str(sample_rate), "--seed", str(seed), "--output", output))


@rf_dna.command("fingerprint")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--label", default="unlabelled", show_default=True)
def rf_dna_fingerprint(input_path: str, label: str) -> None:
    """Extract a descriptive fingerprint from a local NPZ capture."""
    _run_rf_dna(("fingerprint", "--input", input_path, "--label", label))


@rf_dna.command("dashboard")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--label", default="dashboard-capture", show_default=True)
def rf_dna_dashboard(input_path: str, label: str) -> None:
    """Create a dashboard and provenance summary from a local capture."""
    _run_rf_dna(("dashboard", "--input", input_path, "--label", label))


@rf_dna.command("report")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--label", default="capture-report", show_default=True)
def rf_dna_report(input_path: str, label: str) -> None:
    """Create a machine-readable local RF-DNA report."""
    _run_rf_dna(("report", "--input", input_path, "--label", label))


@rf_dna.command("quantum")
@click.option("--profile", default="multi-tone", show_default=True)
@click.option("--duration", type=float, default=2.0, show_default=True)
@click.option("--sample-rate", type=float, default=1_000_000, show_default=True)
@click.option("--seed", type=int, default=7, show_default=True)
def rf_dna_quantum(profile: str, duration: float, sample_rate: float, seed: int) -> None:
    """Run a local quantum-inspired experiment with a classical baseline."""
    _run_rf_dna(("quantum", "--profile", profile, "--duration", str(duration), "--sample-rate", str(sample_rate), "--seed", str(seed)))


@rf_dna.command("backends")
def rf_dna_backends() -> None:
    """Report optional receive backends without probing hardware or networks."""
    _run_rf_dna(("backends",))


@cli.group("forensic")
def forensic() -> None:
    """Offline evidence audit commands for supplied local data."""


@forensic.command("physics")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--distance-m", required=True, type=float)
@click.option("--bandwidth-hz", type=float, default=None)
@click.option("--output", type=click.Path(dir_okay=False), default=None)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def forensic_physics(case_id: str, subject: str, frequency_hz: float, distance_m: float, bandwidth_hz: float | None, output: str | None, fmt: str) -> None:
    """Audit local physical measurement metadata."""
    from vulture.forensics import write_report
    report = audit_physics(case_id, subject, frequency_hz=frequency_hz, distance_m=distance_m, bandwidth_hz=bandwidth_hz)
    if output:
        write_report(report, output, fmt)
    click.echo(report.to_json() if fmt == "json" else report.to_text())


@forensic.command("chemistry")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--compounds-json", required=True)
@click.option("--output", type=click.Path(dir_okay=False), default=None)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def forensic_chemistry(case_id: str, subject: str, compounds_json: str, output: str | None, fmt: str) -> None:
    """Audit local compound composition structures."""
    from vulture.forensics import write_report
    report = audit_chemistry(case_id, subject, json.loads(compounds_json))
    if output:
        write_report(report, output, fmt)
    click.echo(report.to_json() if fmt == "json" else report.to_text())


@forensic.command("math")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--matrix-json", required=True)
@click.option("--vector-json", required=True)
@click.option("--output", type=click.Path(dir_okay=False), default=None)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def forensic_math(case_id: str, subject: str, matrix_json: str, vector_json: str, output: str | None, fmt: str) -> None:
    """Audit a local linear system."""
    from vulture.forensics import write_report
    report = audit_mathematics(case_id, subject, json.loads(matrix_json), json.loads(vector_json))
    if output:
        write_report(report, output, fmt)
    click.echo(report.to_json() if fmt == "json" else report.to_text())


@forensic.command("protocol")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frames-json", required=True)
@click.option("--output", type=click.Path(dir_okay=False), default=None)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def forensic_protocol(case_id: str, subject: str, frames_json: str, output: str | None, fmt: str) -> None:
    """Audit supplied protocol/frame metadata without network access."""
    from vulture.forensics import write_report
    report = audit_protocol(case_id, subject, json.loads(frames_json))
    if output:
        write_report(report, output, fmt)
    click.echo(report.to_json() if fmt == "json" else report.to_text())


class InteractiveShell:
    """Friendly interactive prompt for the scientific and forensic toolset."""

    def __init__(self) -> None:
        self.running = True
        self.history: list[str] = []

    @staticmethod
    def banner() -> None:
        click.echo("══════════════════════════════════════════════════════════")
        click.echo("🦅 VULTURE — Offline Scientific Intelligence Platform")
        click.echo("chemistry • physics • mathematics • RF • forensic audit")
        click.echo("Type: help | status | rf-dna status | chemical-rf nmr | exit")
        click.echo("══════════════════════════════════════════════════════════")

    def run(self) -> None:
        self.banner()
        while self.running:
            try:
                cmd = click.prompt(">", prompt_suffix=" ", show_default=False)
            except (EOFError, KeyboardInterrupt):
                click.echo()
                break
            self.process(cmd)

    def process(self, line: str) -> None:
        line = line.strip()
        if not line:
            return
        self.history.append(line)
        command = line.lower()
        if command in {"exit", "quit"}:
            self.running = False
            click.echo("✓ Session closed safely.")
            return
        if command in {"help", "?"}:
            click.echo("Available commands:")
            click.echo("  info")
            click.echo("  status")
            click.echo("  iq convert capture.iq capture.npz")
            click.echo("  offline analyze values.csv --sample-rate 1000000")
            click.echo("  rf-dna status")
            click.echo("  rf-dna simulate --profile multi-tone --duration 2 --sample-rate 1000000 --output capture.npz")
            click.echo("  rf-dna fingerprint --input capture.npz --label lab-device-01")
            click.echo("  rf-dna dashboard --input capture.npz")
            click.echo("  rf-dna report --input capture.npz")
            click.echo("  rf-dna quantum --profile multi-tone")
            click.echo("  rf-dna backends")
            click.echo("  chemical-rf nmr --input capture.npz --nucleus 1H --field-t 7")
            click.echo("  chemical-rf material --input capture.npz --epsilon-r 4.2 --frequency-hz 2.4e9 --length-m 0.1")
            click.echo("  chemical-rf physics --input capture.npz --frequency-hz 2.4e9 --distance-m 10")
            click.echo("  chemical-rf report --input capture.npz --sample-id S-001 --real-ohm 50 --imag-ohm 2.5")
            click.echo("  forensic physics --case-id C-001 --subject capture --frequency-hz 2.4e9 --distance-m 10")
            click.echo("  forensic chemistry --case-id C-002 --subject sample --compounds-json '[{\"elements\":{\"H\":2,\"O\":1}}]'")
            click.echo("  forensic math --case-id C-003 --subject system --matrix-json '[[2,1],[1,1]]' --vector-json '[3,2]'")
            click.echo("  forensic protocol --case-id C-004 --subject frame --frames-json '[{\"length\":4,\"declared_length\":5}]'")
            click.echo("  lab attack-sim --scenario spoofing")
            click.echo("  lab defense-sim --scenario jamming-detection")
            click.echo("  history")
            click.echo("  exit")
            return
        if command == "history":
            for index, item in enumerate(self.history[:-1], 1):
                click.echo(f"{index}: {item}")
            return
        try:
            cli.main(shlex.split(line), standalone_mode=False)
        except SystemExit:
            pass
        except Exception as exc:  # pragma: no cover
            click.echo(f"error: {exc}")


if __name__ == "__main__":
    cli()
