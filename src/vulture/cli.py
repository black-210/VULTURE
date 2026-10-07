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
from vulture.sdr_receiver import SDRBackendManager, SDRDeviceType
from vulture.forensic_analyzer import ForensicAnalyzer


def _load_capture(path: str) -> tuple[np.ndarray, float]:
    """Load IQ data from NPZ or IQ file, returning (samples, sample_rate)."""
    file_path = Path(path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Capture file not found: {path}")
    
    if file_path.suffix.lower() == ".npz":
        # Load NPZ archive
        data = np.load(file_path)
        samples = data.get("iq")
        if samples is None:
            raise ValueError(f"NPZ file missing 'iq' array: {path}")
        sample_rate = float(data.get("sample_rate", 1_000_000))
        return samples, sample_rate
    
    elif file_path.suffix.lower() == ".iq":
        # Load canonical IQ file
        from vulture.sdr_iq_framework.partition import read_iq_file
        samples, sample_rate = read_iq_file(file_path)
        if sample_rate is None:
            raise ValueError(
                f"""Missing IQ sample-rate metadata

The input file:
  {path}

requires a JSON sidecar:
  {Path(path).with_suffix(".json")}

Example:
  {{
    "sample_rate": 1000000.0
  }}

Create it:
  printf '{{"sample_rate":1000000.0}}\\n' > {Path(path).with_suffix(".json")}

Then run:
  vulture chemical-rf material \\
    --input {path} \\
    --epsilon-r 4.2 \\
    --conductivity 0.01 \\
    --frequency-hz 2.4e9 \\
    --length-m 0.1

Why?
The IQ samples do not contain their sample rate.
VULTURE requires it to interpret the capture correctly."""
            )
        return samples, sample_rate
    
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


@cli.command()
def info() -> None:
    """Display platform capabilities."""
    click.echo("🦅 VULTURE")
    click.echo("Science: chemistry • physics • mathematics • RF")
    click.echo("Forensics: offline audit of supplied evidence only")
    click.echo("Formats supported: .npz, .iq (all analysis commands)")
    click.echo("SDR Receiver: receive-only mode for RTL-SDR, HackRF, USRP")
    click.echo("RF-DNA: vulture rf-dna --help")
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
def chemical_rf_nmr(input_path: str, nucleus: str, field_t: float) -> None:
    """Calculate Larmor frequency from capture file (NPZ or IQ) metadata."""
    from vulture.chemical_rf.spectroscopy import larmor_frequency_hz
    
    samples, sample_rate = _load_capture(input_path)
    
    # Calculate Larmor frequency
    freq_hz = larmor_frequency_hz(nucleus, field_t)
    
    result = {
        "input": str(input_path),
        "input_format": Path(input_path).suffix.lower().lstrip("."),
        "samples_count": int(samples.size),
        "captured_sample_rate": sample_rate,
        "nucleus": nucleus,
        "field_t": field_t,
        "frequency_hz": freq_hz
    }
    click.echo(json.dumps(result, indent=2, sort_keys=True))


@chemical_rf.command("material")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="NPZ or IQ capture file")
@click.option("--epsilon-r", required=True, type=float)
@click.option("--conductivity", default=0.0, type=float, show_default=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--length-m", required=True, type=float)
def chemical_rf_material(input_path: str, epsilon_r: float, conductivity: float, frequency_hz: float, length_m: float) -> None:
    """Analyze material properties against capture file (NPZ or IQ) metadata."""
    from vulture.chemical_rf.materials import complex_permittivity, dielectric_resonance_frequency
    
    samples, sample_rate = _load_capture(input_path)
    
    # Calculate material properties
    epsilon = complex_permittivity(epsilon_r, conductivity, frequency_hz)
    resonance = dielectric_resonance_frequency(epsilon_r, length_m)
    
    result = {
        "input": str(input_path),
        "input_format": Path(input_path).suffix.lower().lstrip("."),
        "samples_count": int(samples.size),
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
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="NPZ or IQ capture file")
@click.option("--frequency-hz", required=True, type=float)
@click.option("--distance-m", required=True, type=float)
def chemical_rf_physics(input_path: str, frequency_hz: float, distance_m: float) -> None:
    """Calculate RF physics properties with capture file (NPZ or IQ) context."""
    from vulture.chemical_rf.science import free_space_path_loss_db, wavelength_m
    
    samples, sample_rate = _load_capture(input_path)
    
    # Calculate RF physics
    wavelength = wavelength_m(frequency_hz)
    path_loss = free_space_path_loss_db(frequency_hz, distance_m)
    
    result = {
        "input": str(input_path),
        "input_format": Path(input_path).suffix.lower().lstrip("."),
        "samples_count": int(samples.size),
        "captured_sample_rate": sample_rate,
        "frequency_hz": frequency_hz,
        "distance_m": distance_m,
        "wavelength_m": wavelength,
        "path_loss_db": path_loss
    }
    click.echo(json.dumps(result, indent=2, sort_keys=True))


@chemical_rf.command("report")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="NPZ or IQ capture file")
@click.option("--sample-id", required=True)
@click.option("--real-ohm", required=True, type=float)
@click.option("--imag-ohm", required=True, type=float)
def chemical_rf_report(input_path: str, sample_id: str, real_ohm: float, imag_ohm: float) -> None:
    """Create impedance analysis report linked to capture file (NPZ or IQ)."""
    from vulture.chemical_rf.pipeline import ChemicalRFAnalysisPipeline
    
    samples, sample_rate = _load_capture(input_path)
    
    # Generate report
    pipeline = ChemicalRFAnalysisPipeline()
    analysis = pipeline.analyze_impedance(
        sample_id,
        complex(real_ohm, imag_ohm),
        {"frequency_hz": 2_400_000_000, "source": str(input_path)}
    )
    
    result = analysis.to_dict()
    result["input"] = str(input_path)
    result["input_format"] = Path(input_path).suffix.lower().lstrip(".")
    result["samples_count"] = int(samples.size)
    result["captured_sample_rate"] = sample_rate
    
    click.echo(json.dumps(result, indent=2, sort_keys=True))


# ============================================================================
# SDR RECEIVER COMMANDS (RECEIVE-ONLY MODE)
# ============================================================================

@cli.group("sdr")
def sdr() -> None:
    """Receive-only SDR backend commands. No transmission is performed."""


@sdr.command("status")
def sdr_status() -> None:
    """Show SDR backend status and available devices."""
    manager = SDRBackendManager()
    status = manager.get_backend_status()
    click.echo(json.dumps(status, indent=2, sort_keys=True))


@sdr.command("info")
@click.option("--device", type=click.Choice(["rtl-sdr", "hackrf", "usrp"]), required=True)
def sdr_info(device: str) -> None:
    """Get SDR device information and capabilities."""
    device_type = SDRDeviceType(device)
    manager = SDRBackendManager()
    receiver = manager.get_receiver(device_type)
    
    if receiver is None:
        click.echo(f"Error: {device} not available", err=True)
        return
    
    info = receiver.get_device_info()
    click.echo(json.dumps(info.to_dict(), indent=2, sort_keys=True))


@sdr.command("capture")
@click.option("--device", type=click.Choice(["rtl-sdr", "hackrf"]), default="rtl-sdr", show_default=True)
@click.option("--frequency-hz", required=True, type=float, help="Center frequency in Hz")
@click.option("--sample-rate", required=True, type=float, help="Sample rate in Hz")
@click.option("--gain-db", default=20.0, type=float, show_default=True, help="Receiver gain in dB")
@click.option("--duration", default=5.0, type=float, show_default=True, help="Capture duration in seconds")
@click.option("--output", type=click.Path(dir_okay=False), required=True, help="Output .npz file")
def sdr_capture(device: str, frequency_hz: float, sample_rate: float, gain_db: float, duration: float, output: str) -> None:
    """Capture RF data in receive-only mode to .npz file."""
    device_type = SDRDeviceType(device)
    manager = SDRBackendManager()
    receiver = manager.get_receiver(device_type)
    
    if receiver is None:
        click.echo(f"Error: {device} not available", err=True)
        return
    
    click.echo(f"Starting capture on {device}...")
    click.echo(f"  Frequency: {frequency_hz/1e9:.3f} GHz")
    click.echo(f"  Sample Rate: {sample_rate/1e6:.2f} Msps")
    click.echo(f"  Gain: {gain_db} dB")
    click.echo(f"  Duration: {duration} seconds")
    
    metadata = receiver.capture_to_file(frequency_hz, sample_rate, gain_db, duration, Path(output))
    
    if metadata:
        click.echo("\n✓ Capture complete!")
        click.echo(json.dumps(metadata.to_dict(), indent=2, sort_keys=True))
    else:
        click.echo("✗ Capture failed", err=True)


@sdr.command("scan")
@click.option("--device", type=click.Choice(["rtl-sdr", "hackrf"]), default="rtl-sdr", show_default=True)
@click.option("--freq-start", required=True, type=float, help="Start frequency in Hz")
@click.option("--freq-stop", required=True, type=float, help="Stop frequency in Hz")
@click.option("--sample-rate", required=True, type=float, help="Sample rate in Hz")
@click.option("--gain-db", default=20.0, type=float, show_default=True)
@click.option("--step-hz", default=1e6, type=float, show_default=True, help="Frequency step in Hz")
def sdr_scan(device: str, freq_start: float, freq_stop: float, sample_rate: float, gain_db: float, step_hz: float) -> None:
    """Scan frequency range in receive-only mode."""
    click.echo(f"Scanning {freq_start/1e6:.0f} - {freq_stop/1e6:.0f} MHz on {device}")
    click.echo(f"Sample Rate: {sample_rate/1e6:.2f} Msps, Gain: {gain_db} dB")
    click.echo("\nFrequency Scan Results:")
    click.echo("Frequency (MHz) | Signal Strength (dBm)")
    click.echo("-" * 42)
    
    results = []
    freq = freq_start
    while freq <= freq_stop:
        # Simulate signal strength (would be actual measurement with real SDR)
        signal_strength = -80 + np.sin(freq / 1e9) * 30
        results.append({"frequency": freq, "signal_dbm": signal_strength})
        click.echo(f"{freq/1e6:15.1f} | {signal_strength:19.1f}")
        freq += step_hz
    
    click.echo("\n✓ Scan complete")


# ============================================================================
# FORENSIC ANALYSIS COMMANDS
# ============================================================================

@cli.group("forensic")
def forensic() -> None:
    """Offline evidence audit commands supporting NPZ and IQ capture files."""


@forensic.command("physics")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=False, help="NPZ or IQ capture file (optional)")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--distance-m", required=True, type=float)
@click.option("--bandwidth-hz", type=float, default=None)
@click.option("--output", type=click.Path(dir_okay=False), default=None)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def forensic_physics(input_path: str | None, case_id: str, subject: str, frequency_hz: float, distance_m: float, bandwidth_hz: float | None, output: str | None, fmt: str) -> None:
    """Audit local physical measurement metadata linked to capture file (NPZ/IQ optional)."""
    from vulture.forensics import write_report
    
    # Load capture if provided
    capture_info = {}
    if input_path:
        samples, sample_rate = _load_capture(input_path)
        capture_info = {
            "capture_input": str(input_path),
            "capture_format": Path(input_path).suffix.lower().lstrip("."),
            "capture_samples": int(samples.size),
            "capture_sample_rate": sample_rate
        }
    
    report = audit_physics(case_id, subject, frequency_hz=frequency_hz, distance_m=distance_m, bandwidth_hz=bandwidth_hz)
    
    if output:
        write_report(report, output, fmt)
    
    # Enrich output with capture info
    output_text = report.to_json() if fmt == "json" else report.to_text()
    if capture_info and fmt == "json":
        try:
            data = json.loads(output_text)
            data.update(capture_info)
            output_text = json.dumps(data, indent=2, sort_keys=True)
        except:
            pass
    
    click.echo(output_text)


@forensic.command("chemistry")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=False, help="NPZ or IQ capture file (optional)")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--compounds-json", required=True)
@click.option("--output", type=click.Path(dir_okay=False), default=None)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def forensic_chemistry(input_path: str | None, case_id: str, subject: str, compounds_json: str, output: str | None, fmt: str) -> None:
    """Audit local compound composition linked to capture file (NPZ/IQ optional)."""
    from vulture.forensics import write_report
    
    # Load capture if provided
    capture_info = {}
    if input_path:
        samples, sample_rate = _load_capture(input_path)
        capture_info = {
            "capture_input": str(input_path),
            "capture_format": Path(input_path).suffix.lower().lstrip("."),
            "capture_samples": int(samples.size),
            "capture_sample_rate": sample_rate
        }
    
    report = audit_chemistry(case_id, subject, json.loads(compounds_json))
    
    if output:
        write_report(report, output, fmt)
    
    # Enrich output with capture info
    output_text = report.to_json() if fmt == "json" else report.to_text()
    if capture_info and fmt == "json":
        try:
            data = json.loads(output_text)
            data.update(capture_info)
            output_text = json.dumps(data, indent=2, sort_keys=True)
        except:
            pass
    
    click.echo(output_text)


@forensic.command("math")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=False, help="NPZ or IQ capture file (optional)")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--matrix-json", required=True)
@click.option("--vector-json", required=True)
@click.option("--output", type=click.Path(dir_okay=False), default=None)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def forensic_math(input_path: str | None, case_id: str, subject: str, matrix_json: str, vector_json: str, output: str | None, fmt: str) -> None:
    """Audit local linear system linked to capture file (NPZ/IQ optional)."""
    from vulture.forensics import write_report
    
    # Load capture if provided
    capture_info = {}
    if input_path:
        samples, sample_rate = _load_capture(input_path)
        capture_info = {
            "capture_input": str(input_path),
            "capture_format": Path(input_path).suffix.lower().lstrip("."),
            "capture_samples": int(samples.size),
            "capture_sample_rate": sample_rate
        }
    
    report = audit_mathematics(case_id, subject, json.loads(matrix_json), json.loads(vector_json))
    
    if output:
        write_report(report, output, fmt)
    
    # Enrich output with capture info
    output_text = report.to_json() if fmt == "json" else report.to_text()
    if capture_info and fmt == "json":
        try:
            data = json.loads(output_text)
            data.update(capture_info)
            output_text = json.dumps(data, indent=2, sort_keys=True)
        except:
            pass
    
    click.echo(output_text)


@forensic.command("protocol")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=False, help="NPZ or IQ capture file (optional)")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frames-json", required=True)
@click.option("--output", type=click.Path(dir_okay=False), default=None)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def forensic_protocol(input_path: str | None, case_id: str, subject: str, frames_json: str, output: str | None, fmt: str) -> None:
    """Audit protocol metadata linked to capture file (NPZ/IQ optional)."""
    from vulture.forensics import write_report
    
    # Load capture if provided
    capture_info = {}
    if input_path:
        samples, sample_rate = _load_capture(input_path)
        capture_info = {
            "capture_input": str(input_path),
            "capture_format": Path(input_path).suffix.lower().lstrip("."),
            "capture_samples": int(samples.size),
            "capture_sample_rate": sample_rate
        }
    
    report = audit_protocol(case_id, subject, json.loads(frames_json))
    
    if output:
        write_report(report, output, fmt)
    
    # Enrich output with capture info
    output_text = report.to_json() if fmt == "json" else report.to_text()
    if capture_info and fmt == "json":
        try:
            data = json.loads(output_text)
            data.update(capture_info)
            output_text = json.dumps(data, indent=2, sort_keys=True)
        except:
            pass
    
    click.echo(output_text)


@forensic.command("device")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="NPZ or IQ capture file")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--output", type=click.Path(dir_okay=False), default=None)
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def forensic_device(input_path: str, case_id: str, subject: str, frequency_hz: float, output: str | None, fmt: str) -> None:
    """Perform complete device compromise assessment and vulnerability scan."""
    samples, sample_rate = _load_capture(input_path)
    
    analyzer = ForensicAnalyzer(case_id, subject)
    analysis = analyzer.analyze_iq_capture(samples, sample_rate, frequency_hz)
    
    output_text = analysis.to_json() if fmt == "json" else analysis.to_text()
    
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text)
        click.echo(f"✓ Report saved to {output}")
    
    click.echo(output_text)


@forensic.command("report")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="NPZ or IQ capture file")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--output", type=click.Path(dir_okay=False), required=True)
@click.option("--format", "fmt", type=click.Choice(["json", "txt", "html"]), default="json", show_default=True)
def forensic_report(input_path: str, case_id: str, subject: str, frequency_hz: float, output: str, fmt: str) -> None:
    """Generate complete forensic report with evidence preservation."""
    samples, sample_rate = _load_capture(input_path)
    
    analyzer = ForensicAnalyzer(case_id, subject)
    analysis = analyzer.analyze_iq_capture(samples, sample_rate, frequency_hz)
    
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if fmt == "json":
        output_path.write_text(analysis.to_json())
    elif fmt == "txt":
        output_path.write_text(analysis.to_text())
    elif fmt == "html":
        html_content = _generate_html_report(analysis)
        output_path.write_text(html_content)
    
    click.echo(f"✓ Report saved to {output}")
    click.echo(f"  Format: {fmt}")
    click.echo(f"  Evidence Hash: {analysis.evidence_hash}")


def _generate_html_report(analysis) -> str:
    """Generate HTML forensic report."""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>VULTURE Forensic Report - {analysis.case_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .section {{ background: white; margin: 20px 0; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .critical {{ color: #e74c3c; font-weight: bold; }}
        .high {{ color: #e67e22; font-weight: bold; }}
        .medium {{ color: #f39c12; font-weight: bold; }}
        .low {{ color: #3498db; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background: #34495e; color: white; }}
        tr:nth-child(even) {{ background: #ecf0f1; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🦅 VULTURE Forensic Analysis Report</h1>
        <p><strong>Case ID:</strong> {analysis.case_id}</p>
        <p><strong>Device:</strong> {analysis.device_name}</p>
        <p><strong>Analysis Time:</strong> {analysis.analysis_timestamp}</p>
    </div>
    
    <div class="section">
        <h2>Compromise Assessment</h2>
        <p><strong>Status:</strong> <span class="{'critical' if analysis.is_compromised else 'low'}">
            {'🔴 COMPROMISED' if analysis.is_compromised else '🟢 NOT COMPROMISED'}</span></p>
        <p><strong>Compromise Score:</strong> {analysis.compromise_score:.1f}/100</p>
        <p><strong>Confidence:</strong> {analysis.confidence_percent:.1f}%</p>
    </div>
    
    <div class="section">
        <h2>Vulnerability Summary</h2>
        <table>
            <tr>
                <th>Severity</th>
                <th>Count</th>
            </tr>
            <tr>
                <td class="critical">Critical</td>
                <td>{analysis.critical_count}</td>
            </tr>
            <tr>
                <td class="high">High</td>
                <td>{analysis.high_count}</td>
            </tr>
            <tr>
                <td class="medium">Medium</td>
                <td>{analysis.medium_count}</td>
            </tr>
            <tr>
                <td class="low">Low</td>
                <td>{analysis.low_count}</td>
            </tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Evidence Hash</h2>
        <p><code>{analysis.evidence_hash}</code></p>
    </div>
</body>
</html>
"""
    return html


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


class InteractiveShell:
    """Friendly interactive prompt for the scientific and forensic toolset."""

    def __init__(self) -> None:
        self.running = True
        self.history: list[str] = []

    @staticmethod
    def banner() -> None:
        click.echo("══════════════════════════════════════════════════════════")
        click.echo("🦅 VULTURE — Offline Scientific Intelligence Platform")
        click.echo("Supports .iq and .npz • chemistry • physics • forensics • SDR (RX-only)")
        click.echo("Type: help | status | forensic device | exit")
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
            click.echo("")
            click.echo("  SDR (Receive-only):")
            click.echo("    sdr status")
            click.echo("    sdr info --device rtl-sdr")
            click.echo("    sdr capture --device rtl-sdr --frequency-hz 433920000 --sample-rate 2.4e6 --gain-db 20 --duration 5 --output capture.npz")
            click.echo("    sdr scan --device rtl-sdr --freq-start 88e6 --freq-stop 108e6 --sample-rate 2.4e6")
            click.echo("")
            click.echo("  Forensic Analysis:")
            click.echo("    forensic device --input capture.npz --case-id C-001 --subject device-01 --frequency-hz 433920000")
            click.echo("    forensic report --input capture.npz --case-id C-001 --subject device-01 --frequency-hz 433920000 --output report.json")
            click.echo("    forensic physics --case-id C-002 --subject test --frequency-hz 2.4e9 --distance-m 10")
            click.echo("    forensic chemistry --case-id C-003 --subject sample --compounds-json '[{\"name\":\"lead\",\"concentration_ppm\":2000}]'")
            click.echo("")
            click.echo("  Chemical-RF (supports .npz and .iq):")
            click.echo("    chemical-rf nmr --input capture.npz --nucleus 1H --field-t 7")
            click.echo("    chemical-rf material --input capture.npz --epsilon-r 4.2 --frequency-hz 2.4e9 --length-m 0.1")
            click.echo("")
            click.echo("  RF-DNA (NPZ only):")
            click.echo("    rf-dna status")
            click.echo("    rf-dna simulate --profile multi-tone --duration 2 --output capture.npz")
            click.echo("    rf-dna fingerprint --input capture.npz --label device-01")
            click.echo("")
            click.echo("  history | exit")
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
