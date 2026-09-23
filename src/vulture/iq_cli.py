"""Top-level IQ file commands.

These commands operate on explicit local files and never open SDR hardware.
"""
from __future__ import annotations

import json
from pathlib import Path

import click

from vulture.sdr_iq_framework.convert import convert_iq_to_npz


@click.group("iq")
def iq() -> None:
    """Validate and convert canonical receive-only IQ captures."""


@iq.command("convert")
@click.argument("input_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("output_path", type=click.Path(dir_okay=False, path_type=Path))
@click.option("--source", default="recorded_iq", show_default=True)
@click.option("--overwrite", is_flag=True, help="Replace an existing NPZ archive.")
def convert(input_path: Path, output_path: Path, source: str, overwrite: bool) -> None:
    """Convert INPUT_PATH (.iq) to OUTPUT_PATH (.npz) with provenance metadata."""
    result = convert_iq_to_npz(input_path, output_path, source=source, overwrite=overwrite)
    click.echo(json.dumps(result, indent=2, sort_keys=True))
