"""CLI commands for offline forensic audits."""
from __future__ import annotations

import json
import click

from .forensics import audit_chemistry, audit_mathematics, audit_physics, audit_protocol, write_report


def _save(report, output: str | None, fmt: str) -> None:
    if output:
        write_report(report, output, fmt)
    click.echo(report.to_json() if fmt == "json" else report.to_text())


@click.group("forensic")
def forensic_cli() -> None:
    """Audit local evidence for physics, chemistry, math, or protocol anomalies."""


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
    _save(audit_physics(case_id, subject, frequency_hz=frequency_hz, distance_m=distance_m, bandwidth_hz=bandwidth_hz), output, fmt)


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
    _save(audit_mathematics(case_id, subject, json.loads(matrix_json), json.loads(vector_json)), output, fmt)


@forensic_cli.command("protocol")
@click.option("--case-id", required=True)
@click.option("--subject", required=True)
@click.option("--frames-json", required=True)
@click.option("--output", type=click.Path(dir_okay=False))
@click.option("--format", "fmt", type=click.Choice(["json", "txt"]), default="json", show_default=True)
def protocol(case_id, subject, frames_json, output, fmt):
    """Check supplied protocol metadata and frames; no network probing occurs."""
    _save(audit_protocol(case_id, subject, json.loads(frames_json)), output, fmt)
