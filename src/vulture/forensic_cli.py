"""CLI commands for offline forensic audits.

This module exposes the local, evidence-driven checks used by VULTURE for
science and forensic analysis. It deliberately does not access hardware or
perform live probing.
"""
from __future__ import annotations

import json
from pathlib import Path

import click
import numpy as np

from .forensic_analyzer import ForensicAnalyzer
from .forensics import audit_chemistry, audit_mathematics, audit_physics, audit_protocol, write_report


def _load_capture(path: str) -> tuple[np.ndarray, float]:
    """Load a capture file from NPZ or IQ format."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Capture file not found: {path}")

    suffix = file_path.suffix.lower()
    if suffix == ".npz":
        data = np.load(file_path, allow_pickle=True)
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
                f"Missing sample-rate metadata for IQ file: {path}. "
                "Add a JSON sidecar with a 'sample_rate' field."
            )
        return np.asarray(samples), float(sample_rate)

    raise ValueError(f"Unsupported capture format: {file_path.suffix}. Use .npz or .iq files.")


def _save(report, output: str | None, fmt: str) -> None:
    if output:
        write_report(report, output, fmt)
    click.echo(report.to_json() if fmt == "json" else report.to_text())


@click.group("forensic")
def forensic_cli() -> None:
    """Audit local evidence for physics, chemistry, math, protocol, and device anomalies."""


@forensic_cli.command("physics")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--distance-m", required=True, type=float)
@click.option("--bandwidth-hz", type=float)
@click.option("--output", type=click.Path(dir_okay=False))
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def physics(case_id, subject, frequency_hz, distance_m, bandwidth_hz, output, fmt):
    """Check physical measurement plausibility without accessing hardware."""
    _save(
        audit_physics(
            case_id,
            subject,
            frequency_hz=frequency_hz,
            distance_m=distance_m,
            bandwidth_hz=bandwidth_hz,
        ),
        output,
        fmt,
    )


@forensic_cli.command("chemistry")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--compounds-json", required=True, help="JSON list of compounds with elements maps.")
@click.option("--output", type=click.Path(dir_okay=False))
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def chemistry(case_id, subject, compounds_json, output, fmt):
    """Check local compound composition data for invalid values."""
    compounds = json.loads(compounds_json)
    _save(audit_chemistry(case_id, subject, compounds), output, fmt)


@forensic_cli.command("math")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--matrix-json", required=True)
@click.option("--vector-json", required=True)
@click.option("--output", type=click.Path(dir_okay=False))
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def mathematics(case_id, subject, matrix_json, vector_json, output, fmt):
    """Check a local linear system for dimensions and non-finite values."""
    _save(
        audit_mathematics(
            case_id,
            subject,
            json.loads(matrix_json),
            json.loads(vector_json),
        ),
        output,
        fmt,
    )


@forensic_cli.command("protocol")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frames-json", required=True)
@click.option("--output", type=click.Path(dir_okay=False))
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def protocol(case_id, subject, frames_json, output, fmt):
    """Check supplied protocol metadata and frames; no network probing occurs."""
    _save(audit_protocol(case_id, subject, json.loads(frames_json)), output, fmt)


@forensic_cli.command("device")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="NPZ or IQ capture file")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--output", type=click.Path(dir_okay=False))
@click.option("--format", "fmt", type=click.Choice(["json", "txt", "html"]), default="json", show_default=True)
def device(input_path: str, case_id: str, subject: str, frequency_hz: float, output: str | None, fmt: str) -> None:
    """Run strong forensic device analysis against an offline capture."""
    samples, sample_rate = _load_capture(input_path)
    analyzer = ForensicAnalyzer(case_id, subject)
    analysis = analyzer.analyze_iq_capture(samples, sample_rate, frequency_hz)

    if fmt == "json":
        payload = analysis.to_json()
    elif fmt == "html":
        payload = """<!DOCTYPE html><html><head><title>VULTURE Forensic Report</title></head><body><h1>VULTURE Forensic Analysis Report</h1><pre>""" + analysis.to_text().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</pre></body></html>"
    else:
        payload = analysis.to_text()

    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload)
        click.echo(f"Report saved to {output}")
    click.echo(payload)


@forensic_cli.command("report")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="NPZ or IQ capture file")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--output", type=click.Path(dir_okay=False), required=True)
@click.option("--format", "fmt", type=click.Choice(["json", "txt", "html"]), default="json", show_default=True)
def report(input_path: str, case_id: str, subject: str, frequency_hz: float, output: str, fmt: str) -> None:
    """Write a forensic evidence report to disk in json/txt/html format."""
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
        content = """<!DOCTYPE html><html><head><title>VULTURE Forensic Report</title></head><body><h1>VULTURE Forensic Analysis Report</h1><pre>""" + analysis.to_text().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</pre></body></html>"

    output_path.write_text(content)
    click.echo(f"✓ Report saved to {output}")
    click.echo(f"  Format: {fmt}")
    click.echo(f"  Evidence Hash: {analysis.evidence_hash}")


@forensic_cli.command("vulnerability")
@click.option("--input", "input_path", type=click.Path(exists=True, dir_okay=False), required=True, help="NPZ or IQ capture file")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--output", type=click.Path(dir_okay=False))
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def vulnerability(input_path: str, case_id: str, subject: str, frequency_hz: float, output: str | None, fmt: str) -> None:
    """Alias for device compromise analysis and vulnerability assessment."""
    device(input_path, case_id, subject, frequency_hz, output, fmt)
