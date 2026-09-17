"""Command-line interface for safe, reproducible Chemical-RF analysis."""
from __future__ import annotations

import json
import click

from .materials import complex_permittivity, dielectric_resonance_frequency
from .pipeline import ChemicalRFAnalysisPipeline
from .science import free_space_path_loss_db, wavelength_m
from .spectroscopy import larmor_frequency_hz


@click.group(name="chemical-rf")
def chemical_rf_cli() -> None:
    """Chemistry, RF, physics, and mathematics calculations (offline only)."""


@chemical_rf_cli.command("nmr")
@click.option("--nucleus", default="1H", show_default=True)
@click.option("--field-t", default=7.0, type=float, show_default=True)
def nmr(nucleus: str, field_t: float) -> None:
    """Calculate an ideal Larmor frequency."""
    click.echo(json.dumps({"nucleus": nucleus, "field_t": field_t, "frequency_hz": larmor_frequency_hz(nucleus, field_t)}, indent=2))


@chemical_rf_cli.command("material")
@click.option("--epsilon-r", required=True, type=float)
@click.option("--conductivity", default=0.0, type=float, show_default=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--length-m", required=True, type=float)
def material(epsilon_r: float, conductivity: float, frequency_hz: float, length_m: float) -> None:
    """Screen a dielectric candidate and estimate a half-wave resonance."""
    epsilon = complex_permittivity(epsilon_r, conductivity, frequency_hz)
    result = {"permittivity": {"real": epsilon.real, "imag": epsilon.imag}, "resonance_hz": dielectric_resonance_frequency(epsilon_r, length_m)}
    click.echo(json.dumps(result, indent=2))


@chemical_rf_cli.command("physics")
@click.option("--frequency-hz", required=True, type=float)
@click.option("--distance-m", required=True, type=float)
def physics(frequency_hz: float, distance_m: float) -> None:
    """Calculate wavelength and free-space path loss."""
    click.echo(json.dumps({"wavelength_m": wavelength_m(frequency_hz), "path_loss_db": free_space_path_loss_db(frequency_hz, distance_m)}, indent=2))


@chemical_rf_cli.command("report")
@click.option("--sample-id", required=True)
@click.option("--real-ohm", required=True, type=float)
@click.option("--imag-ohm", required=True, type=float)
@click.option("--frequency-hz", required=True, type=float)
def report(sample_id: str, real_ohm: float, imag_ohm: float, frequency_hz: float) -> None:
    """Create an auditable, explicitly uncalibrated impedance report."""
    result = ChemicalRFAnalysisPipeline().analyze_impedance(sample_id, complex(real_ohm, imag_ohm), {"frequency_hz": frequency_hz})
    click.echo(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    chemical_rf_cli()
