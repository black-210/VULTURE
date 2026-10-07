"""VULTURE CLI with comprehensive offline science and forensic capabilities.

The CLI exposes real, deterministic, local calculations and forensic audit checks.
It does not scan live systems, transmit RF, or attack targets.

Main command groups:
- vulture info              Platform capabilities
- vulture status            Runtime status (offline-only)
- vulture chemical-rf       Chemistry and RF analysis
- vulture forensic          Forensic evidence audit
- vulture rf-dna            RF fingerprinting and DNA analysis
- vulture rf-vuln           RF physical vulnerability forensics
- vulture rf-security       RF security threat detection
- vulture chemical-vuln     Chemical vulnerability assessment
- vulture lab               Authorized simulations (synthetic data only)
- vulture iq                IQ file conversion and operations
- vulture offline           Standalone analysis tools
- vulture --interactive     Interactive command prompt
"""
from __future__ import annotations

import json
import shlex
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import click
import numpy as np

from vulture.forensics import audit_chemistry, audit_mathematics, audit_physics, audit_protocol
from vulture.lab_cli import lab_cli
from vulture.offline_tools.cli import offline_cli
from vulture.iq_cli import iq
from vulture.rf_vulnerability import (
    assess_rf_physical_vulnerability,
    CaptureMetadata,
    generate_rf_forensic_report,
)
from vulture.rf_security import analyze_rf_security_threats, generate_security_threat_report
from vulture.chemical_vulnerability import (
    assess_chemical_vulnerability,
    generate_chemical_forensic_report,
)


def _load_capture(path: str) -> tuple[np.ndarray, float]:
    """Load IQ data from NPZ or IQ file, returning (samples, sample_rate)."""
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Capture file not found: {path}")
    
    if path_obj.suffix.lower() == ".npz":
        with np.load(path) as data:
            if "iq" not in data:
                raise ValueError("NPZ file must contain 'iq' array")
            samples = np.asarray(data["iq"], dtype=np.complex128)
            sample_rate = float(data.get("sample_rate", 1_000_000.0))
    elif path_obj.suffix.lower() == ".iq":
        from vulture.sdr_iq_framework.partition import read_iq_file
        samples, sample_rate = read_iq_file(path)
        if sample_rate is None:
            raise ValueError(
                f"Could not determine sample rate from {path}.\n"
                f"Create a sidecar JSON file with sample rate:\n"
                f'  echo {{"sample_rate": 1000000}} > {path_obj.with_suffix(".json")}\n'
                f"Or use --sample-rate flag."
            )
    else:
        raise ValueError(f"Unsupported format: {path_obj.suffix}. Use .npz or .iq files.")
    
    return samples, float(sample_rate)


@click.group(invoke_without_command=True)
@click.option("--interactive", is_flag=True, help="Open the interactive > prompt.")
@click.pass_context
def cli(ctx: click.Context, interactive: bool) -> None:
    """🦅 VULTURE — Offline RF, chemistry, physics, mathematics & forensic audit CLI."""
    if interactive:
        InteractiveShell().run()
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# Register command groups
cli.add_command(lab_cli, name="lab")
cli.add_command(iq, name="iq")
cli.add_command(offline_cli, name="offline")


@cli.command()
def info() -> None:
    """Display platform capabilities and available modules."""
    click.echo("🦅 VULTURE — Offline Scientific Intelligence Platform")
    click.echo("")
    click.echo("Science modules:")
    click.echo("  • Chemistry (Chemical-RF, molecular analysis, spectroscopy)")
    click.echo("  • Physics (RF, path loss, wavelength, field strength)")
    click.echo("  • Mathematics (linear systems, numerical validation)")
    click.echo("  • RF-DNA (fingerprinting, simulation, reporting)")
    click.echo("")
    click.echo("Security & Vulnerability:")
    click.echo("  • RF Physical Vulnerability (path loss, field strength, forensics)")
    click.echo("  • RF Security Threats (jamming, spoofing, hijacking detection)")
    click.echo("  • Chemical Vulnerability (composition risk assessment)")
    click.echo("")
    click.echo("Forensic & Audit:")
    click.echo("  • Offline evidence audit (physics, chemistry, math, protocol)")
    click.echo("  • Evidence hashing and chain-of-custody")
    click.echo("  • JSON and text report generation")
    click.echo("")
    click.echo("Data handling:")
    click.echo("  • IQ file formats: .iq (complex64), .npz (NumPy arrays)")
    click.echo("  • SDR support: receive-only mode (no transmit)")
    click.echo("")
    click.echo("Quick help:")
    click.echo("  vulture status                          # Runtime status")
    click.echo("  vulture chemical-rf --help              # Chemistry & RF")
    click.echo("  vulture rf-vuln --help                  # RF vulnerability")
    click.echo("  vulture rf-security --help              # RF threat detection")
    click.echo("  vulture chemical-vuln --help            # Chemical risk")
    click.echo("  vulture forensic --help                 # Forensic audit")
    click.echo("  vulture rf-dna --help                   # RF fingerprinting")
    click.echo("  vulture lab --help                      # Lab simulations")
    click.echo("  vulture iq --help                       # IQ file tools")
    click.echo("  vulture --interactive                   # Interactive prompt")


@cli.command()
def status() -> None:
    """Show safe runtime status and capabilities."""
    payload = {
        "platform": "VULTURE",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "runtime_status": {
            "cli": "online",
            "mode": "offline-deterministic",
            "hardware_access": "disabled",
            "network_access": "disabled",
            "rf_transmission": "disabled",
            "chemical_synthesis": "disabled",
            "analysis_mode": "local-only",
        },
        "supported_formats": {
            "capture": [".iq", ".npz", ".npy"],
            "metadata": [".json"],
        },
        "sdr_mode": "receive-only",
        "main_commands": {
            "scientific": ["chemical-rf", "forensic", "rf-dna"],
            "security": ["rf-vuln", "rf-security", "chemical-vuln"],
            "utilities": ["iq", "offline", "lab"],
            "interactive": "vulture --interactive",
        },
    }
    click.echo(json.dumps(payload, indent=2, sort_keys=True))


# ============================================================================
# RF VULNERABILITY & FORENSICS GROUP
# ============================================================================

@cli.group("rf-vuln")
def rf_vuln() -> None:
    """RF physical vulnerability and forensic analysis from local captures."""


@rf_vuln.command("physical-check")
@click.option("--case-id", required=True, help="Forensic case identifier")
@click.option("--subject", required=True, help="Device or subject under assessment")
@click.option("--frequency-hz", required=True, type=float, help="Operating frequency in Hz")
@click.option("--distance-m", required=True, type=float, help="Distance in meters")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), default=None, help="IQ capture file (.iq or .npz)")
@click.option("--sample-rate", type=float, default=None, help="Sample rate in Hz (for .iq files)")
@click.option("--tx-power-dbm", default=20.0, type=float, show_default=True, help="Transmit power assumption (dBm)")
@click.option("--bandwidth-hz", type=float, default=None, help="Signal bandwidth in Hz")
@click.option("--exposure-risk", default=1.0, type=float, show_default=True, help="Exposure multiplier")
@click.option("--environment-factor", default=1.0, type=float, show_default=True, help="Environment multiplier")
@click.option("--sdr-receive", is_flag=True, default=False, help="Use receive-only SDR mode")
@click.option("--sdr-center-frequency-hz", type=float, default=None, help="SDR center frequency")
@click.option("--sdr-device-args", default=None, help="SoapySDR device string")
@click.option("--sdr-gain", type=float, default=None, help="SDR receiver gain")
@click.option("--output", type=click.Path(dir_okay=False), default=None, help="Output report file")
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True, help="Report format")
def rf_vuln_check(
    case_id: str,
    subject: str,
    frequency_hz: float,
    distance_m: float,
    input_path: Optional[str],
    sample_rate: Optional[float],
    tx_power_dbm: float,
    bandwidth_hz: Optional[float],
    exposure_risk: float,
    environment_factor: float,
    sdr_receive: bool,
    sdr_center_frequency_hz: Optional[float],
    sdr_device_args: Optional[str],
    sdr_gain: Optional[float],
    output: Optional[str],
    fmt: str,
) -> None:
    """Assess RF physical vulnerability from local capture or SDR receive-only mode."""
    if input_path is not None and sdr_receive:
        raise click.BadParameter("Choose either --input or --sdr-receive, not both")
    
    capture_metadata = None
    if input_path is not None:
        capture_metadata = CaptureMetadata.from_path(input_path, sample_rate=sample_rate)
    
    assessment = assess_rf_physical_vulnerability(
        case_id=case_id,
        subject=subject,
        frequency_hz=frequency_hz,
        distance_m=distance_m,
        input_path=input_path,
        sample_rate=sample_rate,
        tx_power_dbm=tx_power_dbm,
        bandwidth_hz=bandwidth_hz,
        exposure_risk=exposure_risk,
        environment_factor=environment_factor,
        sdr_receive=sdr_receive,
        sdr_center_frequency_hz=sdr_center_frequency_hz,
        sdr_device_args=sdr_device_args,
        sdr_gain=sdr_gain,
    )
    
    if fmt == "json":
        report = assessment.to_json()
    else:
        report = generate_rf_forensic_report(assessment)
    
    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(report + ("\n" if not report.endswith("\n") else ""), encoding="utf-8")
        click.echo(f"Report written to {output}")
    else:
        click.echo(report)


@rf_vuln.command("report")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--distance-m", required=True, type=float)
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), default=None)
@click.option("--sample-rate", type=float, default=None)
@click.option("--output", type=click.Path(dir_okay=False), required=True)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="txt", show_default=True)
def rf_vuln_report(
    case_id: str,
    subject: str,
    frequency_hz: float,
    distance_m: float,
    input_path: Optional[str],
    sample_rate: Optional[float],
    output: str,
    fmt: str,
) -> None:
    """Generate a forensic RF vulnerability report and save to file."""
    capture_metadata = None
    if input_path is not None:
        capture_metadata = CaptureMetadata.from_path(input_path, sample_rate=sample_rate)
    
    assessment = assess_rf_physical_vulnerability(
        case_id=case_id,
        subject=subject,
        frequency_hz=frequency_hz,
        distance_m=distance_m,
        input_path=input_path,
        sample_rate=sample_rate,
    )
    
    if fmt == "json":
        report = assessment.to_json()
    else:
        report = generate_rf_forensic_report(assessment)
    
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(report + "\n", encoding="utf-8")
    click.echo(f"✓ Report saved to {output}")


# ============================================================================
# RF SECURITY THREAT DETECTION GROUP
# ============================================================================

@cli.group("rf-security")
def rf_security() -> None:
    """RF security threat detection and analysis from captured IQ data."""


@rf_security.command("analyze")
@click.option("--case-id", required=True, help="Case identifier")
@click.option("--subject", required=True, help="Subject device name")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="IQ capture file")
@click.option("--sample-rate", type=float, default=None, help="Sample rate (for .iq files)")
@click.option("--output", type=click.Path(dir_okay=False), default=None, help="Output report file")
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def rf_security_analyze(
    case_id: str,
    subject: str,
    input_path: str,
    sample_rate: Optional[float],
    output: Optional[str],
    fmt: str,
) -> None:
    """Analyze IQ capture for RF security threats (jamming, spoofing, hijacking, etc.)."""
    samples, rate = _load_capture(input_path)
    if sample_rate is not None:
        rate = sample_rate
    
    duration_s = len(samples) / rate if rate > 0 else 0.0
    
    analysis = analyze_rf_security_threats(
        case_id=case_id,
        subject=subject,
        samples=samples,
        sample_rate=rate,
        duration_s=duration_s,
    )
    
    if fmt == "json":
        report = analysis.to_json()
    else:
        report = generate_security_threat_report(analysis)
    
    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(report + ("\n" if not report.endswith("\n") else ""), encoding="utf-8")
        click.echo(f"✓ Threat analysis saved to {output}")
    else:
        click.echo(report)


@rf_security.command("report")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--sample-rate", type=float, default=None)
@click.option("--output", type=click.Path(dir_okay=False), required=True)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="txt", show_default=True)
def rf_security_report(
    case_id: str,
    subject: str,
    input_path: str,
    sample_rate: Optional[float],
    output: str,
    fmt: str,
) -> None:
    """Generate a plain-text RF security threat report."""
    samples, rate = _load_capture(input_path)
    if sample_rate is not None:
        rate = sample_rate
    
    analysis = analyze_rf_security_threats(
        case_id=case_id,
        subject=subject,
        samples=samples,
        sample_rate=rate,
        duration_s=len(samples) / rate if rate > 0 else 0.0,
    )
    
    if fmt == "json":
        report = analysis.to_json()
    else:
        report = generate_security_threat_report(analysis)
    
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(report + "\n", encoding="utf-8")
    click.echo(f"✓ Report saved to {output}")


# ============================================================================
# CHEMICAL VULNERABILITY GROUP
# ============================================================================

@cli.group("chemical-vuln")
def chemical_vuln() -> None:
    """Chemical composition vulnerability and risk assessment."""


@chemical_vuln.command("assess")
@click.option("--case-id", required=True, help="Case identifier")
@click.option("--subject", required=True, help="Sample or mixture name")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="JSON file with compound metadata")
@click.option("--exposure-window-h", default=8.0, type=float, show_default=True, help="Exposure window in hours")
@click.option("--environment-factor", default=1.0, type=float, show_default=True, help="Environment risk multiplier")
@click.option("--output", type=click.Path(dir_okay=False), default=None, help="Output report file")
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def chemical_vuln_assess(
    case_id: str,
    subject: str,
    input_path: str,
    exposure_window_h: float,
    environment_factor: float,
    output: Optional[str],
    fmt: str,
) -> None:
    """Assess chemical composition for vulnerability from low to critical."""
    compounds_data = json.loads(Path(input_path).read_text(encoding="utf-8"))
    
    assessment = assess_chemical_vulnerability(
        case_id=case_id,
        subject=subject,
        compounds=compounds_data,
        exposure_window_h=exposure_window_h,
        environment_factor=environment_factor,
    )
    
    if fmt == "json":
        report = assessment.to_json()
    else:
        report = generate_chemical_forensic_report(assessment)
    
    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(report + ("\n" if not report.endswith("\n") else ""), encoding="utf-8")
        click.echo(f"✓ Assessment saved to {output}")
    else:
        click.echo(report)


@chemical_vuln.command("report")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("--exposure-window-h", default=8.0, type=float, show_default=True)
@click.option("--environment-factor", default=1.0, type=float, show_default=True)
@click.option("--output", type=click.Path(dir_okay=False), required=True)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="txt", show_default=True)
def chemical_vuln_report(
    case_id: str,
    subject: str,
    input_path: str,
    exposure_window_h: float,
    environment_factor: float,
    output: str,
    fmt: str,
) -> None:
    """Generate a chemical vulnerability forensic report."""
    compounds_data = json.loads(Path(input_path).read_text(encoding="utf-8"))
    
    assessment = assess_chemical_vulnerability(
        case_id=case_id,
        subject=subject,
        compounds=compounds_data,
        exposure_window_h=exposure_window_h,
        environment_factor=environment_factor,
    )
    
    if fmt == "json":
        report = assessment.to_json()
    else:
        report = generate_chemical_forensic_report(assessment)
    
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(report + "\n", encoding="utf-8")
    click.echo(f"✓ Report saved to {output}")


# ============================================================================
# FORENSIC AUDIT GROUP (existing)
# ============================================================================

@cli.group("forensic")
def forensic() -> None:
    """Offline forensic evidence audit commands."""


@forensic.command("physics")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frequency-hz", type=float, required=True)
@click.option("--distance-m", type=float, required=True)
@click.option("--bandwidth-hz", type=float, default=None)
def forensic_physics(case_id: str, subject: str, frequency_hz: float, distance_m: float, bandwidth_hz: Optional[float]) -> None:
    """Audit RF physics parameters."""
    report = audit_physics(
        case_id=case_id,
        subject=subject,
        frequency_hz=frequency_hz,
        distance_m=distance_m,
        bandwidth_hz=bandwidth_hz,
    )
    click.echo(report.to_json() if hasattr(report, "to_json") else report.to_text())


@forensic.command("chemistry")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True)
def forensic_chemistry(case_id: str, subject: str, input_path: str) -> None:
    """Audit chemical composition."""
    compounds_data = json.loads(Path(input_path).read_text(encoding="utf-8"))
    report = audit_chemistry(case_id=case_id, subject=subject, compounds=compounds_data)
    click.echo(report.to_json() if hasattr(report, "to_json") else report.to_text())


@forensic.command("math")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True)
def forensic_math(case_id: str, subject: str, input_path: str) -> None:
    """Audit mathematical systems."""
    data = json.loads(Path(input_path).read_text(encoding="utf-8"))
    report = audit_mathematics(case_id=case_id, subject=subject, matrix=data["matrix"], vector=data["vector"])
    click.echo(report.to_json() if hasattr(report, "to_json") else report.to_text())


@forensic.command("protocol")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True)
def forensic_protocol(case_id: str, subject: str, input_path: str) -> None:
    """Audit protocol frames."""
    frames_data = json.loads(Path(input_path).read_text(encoding="utf-8"))
    report = audit_protocol(case_id=case_id, subject=subject, frames=frames_data)
    click.echo(report.to_json() if hasattr(report, "to_json") else report.to_text())


# ============================================================================
# INTERACTIVE SHELL
# ============================================================================

class InteractiveShell:
    """Interactive CLI shell with convenient command access."""
    
    def __init__(self):
        self.running = True
        self.history = []
    
    def run(self) -> None:
        self.banner()
        while self.running:
            try:
                cmd = click.prompt(">", prompt_suffix=" ")
            except (EOFError, KeyboardInterrupt):
                click.echo("")
                break
            self.process(cmd)
    
    def banner(self) -> None:
        click.echo("")
        click.echo("╔════════════════════════════════════════════════════════════╗")
        click.echo("║  🦅 VULTURE — Interactive Scientific & Forensic Shell     ║")
        click.echo("║  Offline, deterministic, evidence-based analysis          ║")
        click.echo("║  Type 'help' for command list, 'exit' to quit             ║")
        click.echo("╚════════════════════════════════════════════════════════════╝")
        click.echo("")
    
    def process(self, line: str) -> None:
        line = line.strip()
        if not line:
            return
        
        self.history.append(line)
        
        if line in ("quit", "exit"):
            self.running = False
            click.echo("✓ Session closed safely.")
            return
        
        if line == "help":
            self.show_help()
            return
        
        if line == "history":
            for idx, item in enumerate(self.history[:-1], 1):
                click.echo(f"{idx}: {item}")
            return
        
        try:
            ctx = click.Context(cli)
            cli.main(shlex.split(line), standalone_mode=False, obj=ctx)
        except SystemExit:
            pass
        except Exception as exc:
            click.echo(f"✗ Error: {exc}")
    
    def show_help(self) -> None:
        lines = [
            "",
            "Available command groups:",
            "  info                                   Platform capabilities",
            "  status                                 Runtime status",
            "",
            "RF & Physics:",
            "    rf-vuln physical-check               RF vulnerability assessment",
            "    rf-vuln report                       Generate RF forensic report",
            "    rf-security analyze                  Detect RF security threats",
            "    rf-security report                   Generate threat report",
            "",
            "Chemistry:",
            "    chemical-vuln assess                 Assess chemical risk",
            "    chemical-vuln report                 Generate chemical report",
            "    chemical-rf nmr                      Calculate Larmor frequency",
            "    chemical-rf material                 Analyze material properties",
            "",
            "Forensics:",
            "    forensic physics                     Audit RF physics",
            "    forensic chemistry                   Audit chemical data",
            "    forensic math                        Audit mathematical systems",
            "    forensic protocol                    Audit protocol frames",
            "",
            "RF-DNA & Analysis:",
            "    rf-dna status                        Check RF-DNA status",
            "    rf-dna simulate                      Generate test capture",
            "    rf-dna fingerprint                   Extract RF fingerprint",
            "    rf-dna dashboard                     Build capture dashboard",
            "    rf-dna report                        Generate RF report",
            "    rf-dna quantum                       Run quantum baseline",
            "",
            "Lab (Simulations):",
            "    lab attack-sim                       Simulate attack scenario",
            "    lab defense-sim                      Simulate defense scenario",
            "",
            "File Tools:",
            "    iq convert                           Convert .iq ↔ .npz",
            "    offline analyze                      Standalone analysis",
            "",
            "Shell:",
            "    help                                 Show this help",
            "    history                              Show command history",
            "    exit | quit                          Close session",
            "",
        ]
        click.echo("\n".join(lines))


if __name__ == "__main__":
    cli()
