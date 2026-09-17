# 🦅 VULTURE — Offline Scientific Intelligence Platform

VULTURE is a research-focused, offline scientific toolkit for chemistry, physics, mathematics, RF analysis, and forensic evidence review. It is built for controlled lab workflows, reproducible analysis, and auditable results driven by explicit user input and local datasets.

The platform is centered on:
- deterministic calculations
- provenance-aware reporting
- local-only execution
- transparent scientific workflows
- safe forensic review of supplied evidence
- CLI and Python API access

VULTURE does not silently open hardware, probe external systems, or initiate live network activity. SDR support is presented in a simulator-friendly and research-oriented way, with any real hardware use remaining explicit, user-controlled, and environment-dependent.

---

## Overview

VULTURE combines multiple scientific and engineering domains:

- chemistry and chemical reasoning
- RF and electromagnetic calculations
- signal-processing concepts
- spectroscopy workflows
- material dielectric screening
- mathematical validation
- forensic evidence review for supplied local data
- CLI and Python API access

This makes it useful for:
- scientific research
- engineering analysis
- RF simulation workflows
- chemical-RF exploration
- offline evidence audit
- local report generation

---

## Why VULTURE

VULTURE was designed to support trustworthy research and analysis with a clear emphasis on:
- reproducibility
- validation
- provenance
- local-only execution
- explainable outputs
- audit-friendly reporting

Rather than pretending to operate on external environments, VULTURE focuses on:
- computed results from explicit inputs
- controlled analysis decks
- documented assumptions
- safe forensic reporting of supplied data

---

## Core Capabilities

### 1) Chemical-RF Analysis
VULTURE includes scientific tools for chemistry and RF interplay, including:
- exact chemical equation balancing
- bond energy to equivalent frequency scaling
- ideal NMR Larmor calculation
- FID simulation
- FFT spectrum generation
- complex permittivity estimation
- dielectric screening and resonance estimation
- impedance modeling and reflection calculations

### 2) Physics and RF Modeling
- wavelength calculations
- path-loss estimation
- material resonance screening
- propagation analysis
- physical plausibility checks
- frequency-domain analysis support

### 3) Mathematics and Validation
- linear-system solving
- exact numerical validation
- finite-value checks
- deterministic calculations
- structured result generation

### 4) Forensic Audit Layer
VULTURE provides offline forensic-style checks for:
- chemistry input validation
- physics plausibility
- mathematical consistency
- protocol/frame metadata review

These commands work on supplied local evidence and return:
- case identifier
- subject
- timestamp
- SHA-256 digest
- findings with severity
- evidence
- recommendation

### 5) CLI and Interactive Prompt
A friendly interactive shell is included:
- `>` prompt
- status and help commands
- scientific command routing
- local-only execution
- structured JSON output

---

## SDR-Ready Design

VULTURE is designed with SDR-oriented workflows in mind, including:
- RF spectrum concepts
- frequency-domain calculations
- waveform and signal analysis
- simulation-driven experimentation
- offline RF analysis pipelines

Important boundary:
- SDR-ready design is supported
- live hardware operation is not activated by default
- external network scanning is not performed
- live RF transmission is not implied or executed automatically

This keeps the platform safe, transparent, and suitable for controlled research and laboratory environments.

---

## Installation

### Requirements
- Python 3.9+
- pip
- numpy
- scipy
- click
- pytest

### Install from source
```bash
git clone https://github.com/black-210/VULTURE.git
cd VULTURE
python -m pip install -e .
```

### Development install
```bash
python -m pip install -e ".[dev]"
```

---

## Command Line Usage

### Start the interactive shell
```bash
vulture --interactive
```

### Example session
```text
> help
> info
> status
> rf-wavelength --frequency-hz 1e9
> rf-path-loss --frequency-hz 2.4e9 --distance-m 10
> chemical-rf nmr --nucleus 1H --field-t 7
> chemical-rf material --epsilon-r 4.2 --conductivity 0.01 --frequency-hz 13560000 --length-m 0.1
> chemical-rf physics --frequency-hz 2400000000 --distance-m 10
> forensic physics --case-id C-001 --subject capture --frequency-hz 2.4e9 --distance-m 10
> forensic chemistry --case-id C-002 --subject sample --compounds-json '[{"elements":{"H":2,"O":1}}]'
> forensic math --case-id C-003 --subject system --matrix-json '[[2,1],[1,1]]' --vector-json '[3,2]'
> forensic protocol --case-id C-004 --subject frame --frames-json '[{"length":4,"declared_length":5}]'
> exit
```

---

## Commands Reference

### General commands
```bash
vulture --interactive
vulture info
vulture status
```

### RF commands
```bash
vulture rf-wavelength --frequency-hz 1e9
vulture rf-path-loss --frequency-hz 2.4e9 --distance-m 10
```

### Chemical-RF commands
```bash
vulture chemical-rf nmr --nucleus 1H --field-t 7
vulture chemical-rf material --epsilon-r 4.2 --conductivity 0.01 --frequency-hz 13560000 --length-m 0.1
vulture chemical-rf physics --frequency-hz 2400000000 --distance-m 10
vulture chemical-rf report --sample-id sample-01 --real-ohm 48 --imag-ohm -3 --frequency-hz 13560000
```

### Forensic commands
```bash
vulture forensic physics --case-id C-001 --subject capture --frequency-hz 2.4e9 --distance-m 10
vulture forensic chemistry --case-id C-002 --subject sample --compounds-json '[{"elements":{"H":2,"O":1}}]'
vulture forensic math --case-id C-003 --subject system --matrix-json '[[2,1],[1,1]]' --vector-json '[3,2]'
vulture forensic protocol --case-id C-004 --subject frame --frames-json '[{"length":4,"declared_length":5}]'
```

---

## Python API Examples

### RF wavelength
```python
from vulture.chemical_rf.science import wavelength_m

lam = wavelength_m(1e9)
print(lam)
```

### Path loss
```python
from vulture.chemical_rf.science import free_space_path_loss_db

loss_db = free_space_path_loss_db(2.4e9, 10.0)
print(loss_db)
```

### NMR frequency
```python
from vulture.chemical_rf.spectroscopy import larmor_frequency_hz

freq = larmor_frequency_hz("1H", 7.0)
print(freq)
```

### Forensic audit
```python
from vulture.forensics import audit_physics, audit_protocol

report = audit_physics(
    "C-001",
    "sample-capture",
    frequency_hz=2.4e9,
    distance_m=10.0,
    bandwidth_hz=5e6,
)

print(report.to_json())
```

### Chemical-RF material screening
```python
from vulture.chemical_rf.materials import complex_permittivity, dielectric_resonance_frequency

eps = complex_permittivity(4.2, 0.01, 13.56e6)
res = dielectric_resonance_frequency(4.2, 0.1)

print(eps)
print(res)
```

---

## Example Output

### RF wavelength output
```json
{
  "frequency_hz": 1000000000.0,
  "wavelength_m": 0.299792458
}
```

### Forensic chemistry output
```json
{
  "case_id": "C-002",
  "subject": "sample",
  "mode": "offline-audit",
  "input_sha256": "a1c9b7d4...",
  "findings": [
    {
      "domain": "chemistry",
      "code": "CHEM-001",
      "severity": "high",
      "title": "Missing composition",
      "evidence": "compound index 0",
      "recommendation": "Supply a validated elemental composition before balancing."
    }
  ]
}
```

---

## Project Structure

```text
VULTURE/
├── README.md
├── pyproject.toml
├── requirements.txt
├── src/
│   └── vulture/
│       ├── __init__.py
│       ├── cli.py
│       ├── forensic_cli.py
│       ├── forensics.py
│       ├── chemical_rf/
│       │   ├── __init__.py
│       │   ├── cli.py
│       │   ├── science.py
│       │   ├── spectroscopy.py
│       │   ├── materials.py
│       │   ├── pipeline.py
│       │   └── ...
│       └── ...
├── docs/
│   ├── CHEMICAL_RF_INTEGRATION.md
│   ├── CHEMICAL_RF_USER_GUIDE.md
│   ├── CHEMICAL_RF_INVENTION_DISCLOSURES.md
│   ├── FORENSIC_AUDIT.md
│   └── ...
├── tests/
│   ├── test_cli.py
│   ├── test_forensics.py
│   ├── test_chemical_rf.py
│   └── ...
└── ...
```

---

## Safety and Scientific Boundaries

VULTURE is designed for:
- local analysis
- lab-safe workflows
- scientific research
- forensic review of supplied evidence
- reproducible computations

The platform explicitly avoids:
- silent live probing
- unauthorized external access
- live network scanning
- unapproved hardware activation
- harmful or exploitative automation

All outputs should be reviewed as scientific or forensic evidence, not as legal proof or direct operational results.

---

## Licensing

This project is distributed under the Apache 2.0 license unless otherwise noted.

---

## Contributing

Contributions are welcome in:
- chemistry modeling
- RF simulation and analysis
- physics validation
- spectroscopy tools
- forensic reporting
- CLI improvement
- documentation and test coverage

Please keep changes:
- deterministic
- documented
- test-backed
- scientifically explainable

---

## Roadmap

Planned improvements include:
- deeper RF material models
- richer spectroscopy support
- improved physical validation
- stronger forensic reporting
- richer JSON and TXT exports
- dashboard-style local summaries
- expanded CLI usability

---

## Status

VULTURE is an active scientific engineering platform focused on:
- local-only analysis
- chemistry + RF workflows
- forensic evidence review
- reproducible scientific output
- safe research-oriented operations

---

## Final Note

VULTURE is best understood as a scientifically grounded, locally executed toolkit for chemistry, RF analysis, mathematics, and evidence review. It prioritizes clarity, reproducibility, and safe operation in controlled research contexts.


