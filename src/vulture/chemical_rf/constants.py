"""Physical constants and nuclei used by the Chemical-RF package."""

PLANCK_EV_S = 4.135667696e-15
PLANCK_J_S = 6.62607015e-34
BOLTZMANN_J_K = 1.380649e-23

# Cyclic gyromagnetic ratio in MHz/T. Values are suitable for ideal Larmor
# estimates; instrument-specific references should be supplied for calibration.
GYROMAGNETIC_RATIOS_MHZ_T = {
    "1H": 42.57747892,
    "H": 42.57747892,
    "13C": 10.7084,
    "C": 10.7084,
    "15N": -4.316,
    "N": 3.077,
    "19F": 40.053,
    "F": 40.053,
    "31P": 17.235,
    "P": 17.235,
    "29Si": -8.465,
}

BOND_ORDER = {"single": 1.0, "double": 2.0, "triple": 3.0, "aromatic": 1.5}
