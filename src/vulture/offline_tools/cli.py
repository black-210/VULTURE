"""Click commands for the offline analysis toolkit."""
from __future__ import annotations
import json
import click
from .loaders import load_numbers
from .workflow import analyze


@click.group(name="offline")
def offline_cli() -> None:
    """Deterministic local analysis; no network, transmission, or device probing."""


@offline_cli.command("analyze")
@click.argument("path", type=click.Path(exists=True, dir_okay=False))
@click.option("--sample-rate", type=float, default=None)
def analyze_file(path: str, sample_rate: float | None) -> None:
    """Analyze numeric values from a local whitespace/CSV file."""
    click.echo(json.dumps(analyze(load_numbers(path), sample_rate), indent=2, sort_keys=True))
