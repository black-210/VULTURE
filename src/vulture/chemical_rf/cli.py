"""Command-line interface for safe, reproducible Chemical-RF analysis."""
from __future__ import annotations

import json
from pathlib import Path

import click

from . import ChemicalEquationSolver, MolecularRFAnalyzer
from .materials import (
    absorption_coefficient,
    complex_permittivity,
    dielectric_resonance_frequency,
    maxwell_garnett_permittivity,
    reflection_coefficient,
)
from .pipeline import ChemicalRFAnalysisPipeline
from .science import free_space_path_loss_db, wavelength_m
from .spectroscopy import larmor_frequency_hz, simulate_fid, spectrum_from_fid


def _complex_json(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imag": float(value.imag)}


def _load_json(value: str, name: str):
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise click.BadParameter(f"{name} must be valid JSON") from exc


def _bonds(analyzer: MolecularRFAnalyzer, bonds: list[dict]) -> None:
    for bond in bonds:
        required = {"atom1", "atom2", "bond_type", "bond_energy", "bond_length"}
        missing = required - bond.keys()
        if missing:
            raise click.BadParameter(f"bond is missing fields: {', '.join(sorted(missing))}")
        analyzer.add_bond(
            str(bond["atom1"]), str(bond["atom2"]), str(bond["bond_type"]),
            float(bond["bond_energy"]), float(bond["bond_length"]),
        )


@click.group(name="chemical-rf")
def chemical_rf_cli() -> None:
    """Chemistry, RF, physics, and mathematics calculations (offline only)."""


@chemical_rf_cli.command("nmr")
@click.option("--nucleus", default="1H", show_default=True)
@click.option("--field-t", default=7.0, type=float, show_default=True)
@click.option("--shift-ppm", default=0.0, type=float, show_default=True)
def nmr(nucleus: str, field_t: float, shift_ppm: float) -> None:
    """Calculate an ideal Larmor frequency, optionally shifted in ppm."""
    click.echo(json.dumps({"nucleus": nucleus, "field_t": field_t, "chemical_shift_ppm": shift_ppm, "frequency_hz": larmor_frequency_hz(nucleus, field_t, shift_ppm)}, indent=2))


@chemical_rf_cli.command("material")
@click.option("--epsilon-r", required=True, type=float)
@click.option("--conductivity", default=0.0, type=float, show_default=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--length-m", required=True, type=float)
@click.option("--mode", default=1, type=int, show_default=True)
def material(epsilon_r: float, conductivity: float, frequency_hz: float, length_m: float, mode: int) -> None:
    """Screen a dielectric candidate and estimate a resonator frequency."""
    epsilon = complex_permittivity(epsilon_r, conductivity, frequency_hz)
    result = {"permittivity": _complex_json(epsilon), "resonance_hz": dielectric_resonance_frequency(epsilon_r, length_m, mode)}
    click.echo(json.dumps(result, indent=2))


@chemical_rf_cli.command("material-mix")
@click.option("--matrix-epsilon", required=True, type=float)
@click.option("--matrix-conductivity", default=0.0, type=float, show_default=True)
@click.option("--inclusion-epsilon", required=True, type=float)
@click.option("--inclusion-conductivity", default=0.0, type=float, show_default=True)
@click.option("--frequency-hz", required=True, type=float)
@click.option("--volume-fraction", required=True, type=float)
def material_mix(matrix_epsilon: float, matrix_conductivity: float, inclusion_epsilon: float, inclusion_conductivity: float, frequency_hz: float, volume_fraction: float) -> None:
    """Estimate effective complex permittivity with Maxwell-Garnett mixing."""
    matrix = complex_permittivity(matrix_epsilon, matrix_conductivity, frequency_hz)
    inclusion = complex_permittivity(inclusion_epsilon, inclusion_conductivity, frequency_hz)
    click.echo(json.dumps({"effective_permittivity": _complex_json(maxwell_garnett_permittivity(matrix, inclusion, volume_fraction)), "volume_fraction": volume_fraction}, indent=2))


@chemical_rf_cli.command("physics")
@click.option("--frequency-hz", required=True, type=float)
@click.option("--distance-m", required=True, type=float)
def physics(frequency_hz: float, distance_m: float) -> None:
    """Calculate wavelength and free-space path loss."""
    click.echo(json.dumps({"wavelength_m": wavelength_m(frequency_hz), "path_loss_db": free_space_path_loss_db(frequency_hz, distance_m)}, indent=2))


@chemical_rf_cli.command("impedance")
@click.option("--impedance-ohm", required=True, type=float)
@click.option("--reactance-ohm", default=0.0, type=float, show_default=True)
@click.option("--reference-ohm", default=50.0, type=float, show_default=True)
def impedance(impedance_ohm: float, reactance_ohm: float, reference_ohm: float) -> None:
    """Calculate reflection and absorption from a supplied complex load."""
    load = complex(impedance_ohm, reactance_ohm)
    reference = complex(reference_ohm, 0.0)
    click.echo(json.dumps({"load_ohm": _complex_json(load), "reflection": _complex_json(reflection_coefficient(load, reference)), "absorption": absorption_coefficient(load, reference)}, indent=2))


@chemical_rf_cli.command("molecular")
@click.option("--bonds-json", required=True, help="JSON list of molecular bond descriptors.")
@click.option("--frequency-hz", default=1e6, type=float, show_default=True)
def molecular(bonds_json: str, frequency_hz: float) -> None:
    """Calculate equivalent molecular impedance and bond transition scale."""
    analyzer = MolecularRFAnalyzer()
    bonds = _load_json(bonds_json, "bonds-json")
    if not isinstance(bonds, list):
        raise click.BadParameter("bonds-json must be a JSON list")
    _bonds(analyzer, bonds)
    click.echo(json.dumps({"impedance_ohm": _complex_json(analyzer.calculate_molecular_rf_impedance(frequency_hz)), "resonance_hz": analyzer.calculate_molecular_resonance(), "bond_count": len(bonds), "interpretation": "equivalent model; not a direct molecular measurement"}, indent=2))


@chemical_rf_cli.command("balance")
@click.option("--reactants-json", required=True)
@click.option("--products-json", required=True)
def balance(reactants_json: str, products_json: str) -> None:
    """Balance compounds represented by element-count JSON objects."""
    reactants = _load_json(reactants_json, "reactants-json")
    products = _load_json(products_json, "products-json")
    if not isinstance(reactants, list) or not isinstance(products, list):
        raise click.BadParameter("reactants-json and products-json must be JSON lists")
    click.echo(json.dumps(ChemicalEquationSolver.balance_equation(reactants, products), indent=2))


@chemical_rf_cli.command("fid")
@click.option("--nucleus", default="1H", show_default=True)
@click.option("--field-t", default=7.0, type=float, show_default=True)
@click.option("--duration-s", default=0.01, type=float, show_default=True)
@click.option("--sample-rate-hz", default=1000.0, type=float, show_default=True)
@click.option("--t2-s", default=0.12, type=float, show_default=True)
def fid(nucleus: str, field_t: float, duration_s: float, sample_rate_hz: float, t2_s: float) -> None:
    """Simulate a deterministic local complex NMR free-induction decay."""
    result = simulate_fid(nucleus, field_t, duration_s, sample_rate_hz, t2_s)
    click.echo(json.dumps({"nucleus": nucleus, "field_t": field_t, "frequency_hz": result["frequency_hz"], "sample_count": len(result["fid"]), "duration_s": duration_s}, indent=2))


@chemical_rf_cli.command("spectrum")
@click.option("--nucleus", default="1H", show_default=True)
@click.option("--field-t", default=7.0, type=float, show_default=True)
@click.option("--duration-s", default=0.01, type=float, show_default=True)
@click.option("--sample-rate-hz", default=1000.0, type=float, show_default=True)
def spectrum(nucleus: str, field_t: float, duration_s: float, sample_rate_hz: float) -> None:
    """Simulate an FID and report its deterministic FFT summary."""
    result = simulate_fid(nucleus, field_t, duration_s, sample_rate_hz)
    fft = spectrum_from_fid(result["fid"], sample_rate_hz)
    peak = int(fft["magnitude"].argmax())
    click.echo(json.dumps({"nucleus": nucleus, "sample_count": len(result["fid"]), "peak_frequency_hz": float(fft["frequency_hz"][peak]), "peak_magnitude": float(fft["magnitude"][peak])}, indent=2))


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
