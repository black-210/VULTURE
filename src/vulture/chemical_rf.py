"""Chemistry-aware RF analysis primitives.

This module deliberately separates measured NMR frequencies from molecular
energy scales.  A chemical bond energy is not itself an RF resonance; it is
converted to an equivalent photon frequency for comparison, while NMR peaks
are calculated from gyromagnetic ratios and the applied magnetic field.

The implementation is dependency-light and deterministic so it can be used
with measured data, simulators, and tests without a quantum-chemistry package.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd, pi
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

PLANCK_EV_S = 4.135667696e-15
ELECTRON_CHARGE = 1.602176634e-19
H_PLANCK = 6.62607015e-34

# Gyromagnetic ratios in MHz/T (cycles, not radians).
GYROMAGNETIC_RATIOS_MHZ_T = {
    "H": 42.57747892,
    "1H": 42.57747892,
    "C": 10.7084,
    "13C": 10.7084,
    "N": 3.077,
    "15N": -4.316,
    "P": 17.235,
    "31P": 17.235,
    "F": 40.053,
    "19F": 40.053,
}

BOND_ORDER = {"single": 1.0, "double": 2.0, "triple": 3.0, "aromatic": 1.5}


@dataclass(frozen=True)
class ChemicalBond:
    """A bond descriptor with an equivalent energy-transition frequency."""

    atom1: str
    atom2: str
    bond_type: str
    bond_energy: float  # eV per bond
    bond_length: float  # Angstrom

    def __post_init__(self) -> None:
        if self.bond_energy <= 0 or self.bond_length <= 0:
            raise ValueError("bond_energy and bond_length must be positive")
        if self.bond_type not in BOND_ORDER:
            raise ValueError(f"unsupported bond_type: {self.bond_type}")

    @property
    def transition_frequency_hz(self) -> float:
        """Equivalent photon frequency E/h (usually IR/optical, not RF)."""
        return self.bond_energy / PLANCK_EV_S

    @property
    def bond_order(self) -> float:
        return BOND_ORDER[self.bond_type]


@dataclass(frozen=True)
class NMRPeak:
    nucleus: str
    frequency_hz: float
    chemical_shift_ppm: float = 0.0


class MolecularRFAnalyzer:
    """Calculate reproducible, physically labelled molecular/RF observables.

    The impedance is a low-order equivalent-circuit estimate, not a claim
    that an isolated molecule is a 50-ohm circuit.  It is useful for comparing
    candidate materials when a calibration reference is supplied.
    """

    def __init__(self, reference_impedance_ohm: float = 50.0) -> None:
        if reference_impedance_ohm <= 0:
            raise ValueError("reference_impedance_ohm must be positive")
        self.reference_impedance_ohm = float(reference_impedance_ohm)
        self.bonds: List[ChemicalBond] = []

    def add_bond(
        self, atom1: str, atom2: str, bond_type: str, bond_energy: float, bond_length: float
    ) -> ChemicalBond:
        bond = ChemicalBond(atom1, atom2, bond_type, float(bond_energy), float(bond_length))
        self.bonds.append(bond)
        return bond

    def calculate_molecular_rf_impedance(self, frequency_hz: float = 1e6) -> complex:
        """Return a calibrated series-RC proxy at ``frequency_hz``.

        Bond order and length determine the normalized capacitance proxy; the
        result is explicitly an *equivalent* impedance for material ranking.
        """
        if frequency_hz <= 0:
            raise ValueError("frequency_hz must be positive")
        if not self.bonds:
            return complex(self.reference_impedance_ohm, 0.0)
        length_factor = sum(b.bond_length / b.bond_order for b in self.bonds) / len(self.bonds)
        energy_factor = sum(b.bond_energy for b in self.bonds) / len(self.bonds)
        resistance = self.reference_impedance_ohm * (length_factor / 1.0)
        # Dimensionless calibration keeps the proxy stable and interpretable.
        capacitance_f = 1e-12 * (1.0 + energy_factor / 10.0) / max(length_factor, 1e-12)
        reactance = -1.0 / (2.0 * pi * frequency_hz * capacitance_f)
        return complex(resistance, reactance)

    def calculate_molecular_resonance(self) -> float:
        """Return the mean equivalent bond transition frequency in Hz."""
        if not self.bonds:
            return 0.0
        return sum(b.transition_frequency_hz for b in self.bonds) / len(self.bonds)

    def simulate_nmr_spectrum(
        self, b0_field: float = 7.0, nuclei: Iterable[str] = ("1H",),
        chemical_shifts_ppm: Mapping[str, float] | None = None,
    ) -> Dict[str, object]:
        """Generate ideal Larmor peaks; shifts are additive in ppm."""
        if b0_field <= 0:
            raise ValueError("b0_field must be positive")
        shifts = chemical_shifts_ppm or {}
        peaks: List[Dict[str, float | str]] = []
        for nucleus in nuclei:
            if nucleus not in GYROMAGNETIC_RATIOS_MHZ_T:
                raise ValueError(f"unsupported nucleus: {nucleus}")
            shift = float(shifts.get(nucleus, 0.0))
            base_hz = GYROMAGNETIC_RATIOS_MHZ_T[nucleus] * 1e6 * b0_field
            peaks.append({"nucleus": nucleus, "frequency_hz": base_hz * (1 + shift * 1e-6), "chemical_shift_ppm": shift})
        return {"b0_field_t": b0_field, "peaks": peaks, "reference": "ideal Larmor frequency"}


class ChemicalEquationSolver:
    """Exact integer balancing and reaction energy-frequency bookkeeping."""

    @staticmethod
    def balance_equation(reactants: Sequence[Mapping], products: Sequence[Mapping]) -> Dict[str, object]:
        compounds = list(reactants) + list(products)
        if not compounds or not reactants or not products:
            raise ValueError("reactants and products must both be non-empty")
        elements = sorted({e for c in compounds for e in c.get("elements", {})})
        matrix = [[Fraction(c.get("elements", {}).get(e, 0)) * (1 if j < len(reactants) else -1)
                   for j, c in enumerate(compounds)] for e in elements]
        vector = ChemicalEquationSolver._null_vector(matrix)
        lcm = 1
        for value in vector:
            lcm = lcm * value.denominator // gcd(lcm, value.denominator)
        integers = [abs(int(v * lcm)) for v in vector]
        divisor = 0
        for value in integers:
            divisor = gcd(divisor, value)
        integers = [v // divisor for v in integers]
        return {"reactant_coefficients": integers[:len(reactants)], "product_coefficients": integers[len(reactants):], "elements": elements}

    @staticmethod
    def _null_vector(matrix: List[List[Fraction]]) -> List[Fraction]:
        rows = [row[:] for row in matrix]
        m, n = len(rows), len(rows[0])
        pivot_cols: List[int] = []
        r = 0
        for c in range(n):
            pivot = next((i for i in range(r, m) if rows[i][c]), None)
            if pivot is None:
                continue
            rows[r], rows[pivot] = rows[pivot], rows[r]
            scale = rows[r][c]
            rows[r] = [x / scale for x in rows[r]]
            for i in range(m):
                if i != r and rows[i][c]:
                    factor = rows[i][c]
                    rows[i] = [a - factor * b for a, b in zip(rows[i], rows[r])]
            pivot_cols.append(c)
            r += 1
            if r == m:
                break
        free = next((c for c in range(n) if c not in pivot_cols), None)
        if free is None:
            raise ValueError("equation has no non-zero balancing solution")
        result = [Fraction(0) for _ in range(n)]
        result[free] = Fraction(1)
        for row, pivot_col in reversed(list(enumerate(pivot_cols))):
            result[pivot_col] = -sum(rows[row][j] * result[j] for j in range(n) if j != pivot_col)
        return result

    @staticmethod
    def calculate_reaction_rf_signature(reactants: Sequence[Mapping], products: Sequence[Mapping]) -> complex:
        delta_ev = sum(float(p.get("bond_energy", 0.0)) for p in products) - sum(float(r.get("bond_energy", 0.0)) for r in reactants)
        return complex(delta_ev / PLANCK_EV_S, 0.0)


__all__ = ["ChemicalBond", "ChemicalEquationSolver", "MolecularRFAnalyzer", "NMRPeak"]
