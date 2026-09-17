# 🧪 Chemical-RF Analysis

VULTURE includes an offline, testable Chemical-RF scientific tool. It does not
pretend that a chemical bond is an RF circuit: it distinguishes equivalent
energy scales, ideal NMR frequencies, calibrated impedance estimates, material
models, and actual measurements.

## Capabilities

- Exact integer chemical-equation balancing.
- Bond energy → equivalent photon frequency (`E/h`) with correct units.
- Ideal NMR Larmor frequencies, deterministic FID generation, and FFT spectra.
- Complex permittivity, Maxwell-Garnett material mixing, resonator screening,
  reflection coefficient, and free-space path loss.
- Complex impedance calibration against reference loads.
- JSON reports with warnings, units, and deterministic provenance hashes.
- Mathematics utilities: exact rational algebra, Gaussian elimination, and
  uncertainty propagation.

## Quick commands

```bash
python -m vulture.chemical_rf.cli nmr --nucleus 1H --field-t 7
python -m vulture.chemical_rf.cli material --epsilon-r 4.2 --conductivity 0.01 --frequency-hz 13560000 --length-m 0.1
python -m vulture.chemical_rf.cli physics --frequency-hz 2400000000 --distance-m 10
python -m vulture.chemical_rf.cli report --sample-id resin-01 --real-ohm 48 --imag-ohm -3 --frequency-hz 13560000
```

Full reference: [Chemical-RF User Guide](docs/CHEMICAL_RF_USER_GUIDE.md)

Research concepts are documented in
[Chemical-RF Invention Disclosures](docs/CHEMICAL_RF_INVENTION_DISCLOSURES.md).
They are disclosures for prior-art review, not granted patents or legal claims
of novelty.
