# Chemical-RF Analysis

VULTURE's Chemical-RF module provides executable, calibrated analysis rather
than treating a chemical bond as a literal 50-ohm RF component.

## What is calculated

- **Equivalent impedance:** a documented series-RC proxy that can be compared
  between candidate materials at a specified frequency. It is not a direct
  measurement of an isolated molecule.
- **Bond energy scale:** `E / h` is reported as an equivalent photon frequency.
  For ordinary bonds this is generally infrared/optical, not an RF resonance.
- **NMR spectrum:** ideal Larmor frequencies are calculated from the field and
  nucleus gyromagnetic ratio. Optional chemical shifts are applied in ppm.
- **Equation balancing:** exact rational linear algebra produces the smallest
  integer stoichiometric coefficients.
- **Reaction signature:** reaction bond-energy deltas are converted to an
  equivalent frequency scale and returned with an explicit real-valued phase.

## Example

```python
from vulture.chemical_rf import MolecularRFAnalyzer

analyzer = MolecularRFAnalyzer()
analyzer.add_bond("H", "O", "single", bond_energy=5.2, bond_length=0.957)

z = analyzer.calculate_molecular_rf_impedance(frequency_hz=13.56e6)
nmr = analyzer.simulate_nmr_spectrum(b0_field=7.0, nuclei=("1H", "13C"))
print(z, nmr["peaks"])
```

The module is deterministic, has no network or hardware requirement, and is
covered by `tests/test_chemical_rf.py`. Experimental claims require calibration
against measured dielectric/NMR data before being used for instrumentation.
