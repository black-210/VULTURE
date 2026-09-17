# Chemical-RF Analysis: user guide and command reference

VULTURE's Chemical-RF tool is an **offline scientific analysis library**. It
connects chemical descriptors to RF engineering through explicit models,
calibration, spectroscopy, material screening, and auditable provenance. It
does not claim that a molecule is literally a 50-ohm circuit, and it never
controls transmitters or handles chemicals.

## Installation

```bash
python -m pip install -e .
```

For Python use:

```python
from vulture.chemical_rf import MolecularRFAnalyzer, simulate_fid

analyzer = MolecularRFAnalyzer()
analyzer.add_bond("H", "O", "single", 5.2, 0.957)
print(analyzer.calculate_molecular_rf_impedance(13.56e6))
fid = simulate_fid("1H", b0_field_t=7.0, duration_s=0.01, sample_rate_hz=1000)
```

## Commands

The commands are local and deterministic. Invoke the group through a small
wrapper or Python:

```bash
python -m vulture.chemical_rf.cli nmr --nucleus 1H --field-t 7
python -m vulture.chemical_rf.cli material --epsilon-r 4.2 --conductivity 0.01 --frequency-hz 13560000 --length-m 0.1
python -m vulture.chemical_rf.cli physics --frequency-hz 2400000000 --distance-m 10
python -m vulture.chemical_rf.cli report --sample-id resin-01 --real-ohm 48 --imag-ohm -3 --frequency-hz 13560000
```

- `nmr`: ideal Larmor frequency for supported nuclei.
- `material`: complex permittivity and half-wave resonator screening.
- `physics`: wavelength and Friis free-space path loss.
- `report`: JSON report with reflection coefficient, warning, and provenance hash.

## Chemistry, physics, and mathematics API

- Chemistry: `ChemicalEquationSolver.balance_equation`, reaction signature,
  bond transition scale, and NMR peak generation.
- Physics: `complex_permittivity`, Maxwell-Garnett mixing,
  `dielectric_resonance_frequency`, reflection coefficient, and FID/FFT.
- Mathematics: exact rational equation balancing, Gaussian elimination via
  `solve_linear_system`, uncertainty root-sum-square, and deterministic hashes.

## Truthfulness and validation

Energy-to-frequency (`E/h`) is an equivalent photon scale; it is not presented
as an RF resonance. Predictions without reference-load calibration are marked
`uncalibrated equivalent-circuit prediction`. Use independent measurements,
uncertainty budgets, temperature/humidity metadata, and repeatability tests
before engineering decisions.

Run tests with:

```bash
pytest tests/test_chemical_rf.py tests/test_chemical_rf_pipeline.py -q
```
