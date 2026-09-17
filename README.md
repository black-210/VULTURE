# 🦅 VULTURE — Autonomous Intelligence & Research Platform

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![RF](https://img.shields.io/badge/RF%20DNA-receive%20only-0A7B5E)](#rf-dna)
[![License](https://img.shields.io/badge/License-AGPL--3.0-blue)](LICENSE)

VULTURE is a modular scientific, RF, SDR/IQ, machine-learning, forensic, chemistry, physics, mathematics, visualization, and research platform. It provides a terminal interface, an optional PyQt6 GUI, reusable Python APIs, deterministic offline fixtures, auditable reports, and controlled integrations for authorized laboratory work.

> **Identity and scope are preserved:** this is VULTURE. Existing scientific, forensic, RF, Chemical-RF, GUI, ML, quantum-research, and compatibility features remain part of the project. New material in this README documents and organizes those capabilities; it does not replace the project identity.

> **Authorized use only:** use the platform with systems, frequencies, datasets, and receivers you own or are explicitly authorized to analyze. VULTURE is receive/analyze-only by design and does not provide jamming, spoofing, unauthorized interception, credential theft, exploitation, evasion, or automatic transmission.

---

## Contents

- [What VULTURE provides](#what-vulture-provides)
- [Installation](#installation)
- [Fast start](#fast-start)
- [Main CLI](#main-cli)
- [RF and physics commands](#rf-and-physics-commands)
- [Chemical-RF commands](#chemical-rf-commands)
- [Forensic audit commands](#forensic-audit-commands)
- [RF-DNA commands](#rf-dna-commands)
- [Interactive terminal](#interactive-terminal)
- [GUI](#gui)
- [Signal processing and SDR/IQ](#signal-processing-and-sdriq)
- [AI/ML and analytics](#aiml-and-analytics)
- [Quantum and scientific research](#quantum-and-scientific-research)
- [Reports, provenance, and security](#reports-provenance-and-security)
- [Testing](#testing)
- [Project structure](#project-structure)
- [Safety and limitations](#safety-and-limitations)

---

## What VULTURE provides

### Scientific and engineering tools

- RF wavelength and free-space path-loss calculations.
- Chemistry/RF material screening and complex-permittivity calculations.
- NMR/Larmor-frequency calculations.
- Spectroscopy, physics, mathematics, and measurement helpers.
- Deterministic simulation profiles for offline experiments.

### RF intelligence and signal processing

- FFT, PSD, spectrogram, waterfall, occupancy, peak, burst, and noise-floor analysis.
- Interference and anomaly detection for owned or authorized bands.
- IQ loading, recording, playback, metadata, calibration, and resampling boundaries.
- Receive-only adapters for approved SDR hardware.
- Reproducible RF-DNA fingerprinting and capture comparison.

### Evidence, forensics, and audit

- Offline physics, chemistry, mathematics, and protocol/frame audits.
- Structured JSON and human-readable reports.
- SHA-256 capture hashes and provenance metadata.
- Explicit authorization and operator-review fields.
- Bounded inputs and fail-closed validation.

### AI, ML, and analytics

- Classical feature engineering and model evaluation.
- Optional deep-learning and ONNX-related components where installed.
- Explainable feature reports and offline benchmarking.
- Time-series, anomaly, clustering, and statistical analysis modules.
- Human review before any consequential action.

### GUI and research workflows

- Optional PyQt6 desktop interface.
- RF Intelligence, SDR/IQ, ML, RF-DNA dashboard, and provenance-review surfaces.
- Optional visualization and advanced plotting modules.
- Quantum-inspired experiments with classical baselines.
- Lab-only optional SoapySDR/UHD test markers.

---

## Installation

```bash
git clone https://github.com/black-210/VULTURE.git
cd VULTURE
python -m pip install -e .
```

Run the complete test suite:

```bash
pytest -q
```

Install optional development dependencies when supported by the environment:

```bash
python -m pip install -e ".[dev]"
```

Optional hardware drivers are installed separately according to the vendor and operating system. The simulator and offline analysis must remain usable without them.

---

## Fast start

```bash
vulture info
vulture status
vulture rf-wavelength --frequency-hz 1000000000
vulture rf-path-loss --frequency-hz 2400000000 --distance-m 10
vulture chemical-rf nmr --nucleus 1H --field-t 7
vulture forensic physics --case-id C-001 --subject capture --frequency-hz 2400000000 --distance-m 10
vulture --interactive
```

Expected `vulture status` result:

```json
{
  "analysis": "local-only",
  "cli": "online",
  "hardware": "not-opened",
  "mode": "offline-deterministic",
  "network": "disabled",
  "rf_dna_command": "vulture rf-dna",
  "rf_transmit": "disabled"
}
```

The exact output formatting depends on the installed version, but the safety fields above describe the intended mode.

---

## Main CLI

Show all commands:

```bash
vulture --help
```

The main command keeps the original VULTURE interface and includes:

```text
info
status
rf-wavelength
rf-path-loss
chemical-rf
forensic
rf-dna
```

Every command follows the same flow: Click parses the arguments, VULTURE validates them, the local calculation or audit runs, and JSON/text output is printed. Pressing Enter does not open a device unless a separate, explicit hardware operation is selected by an authorized deployment.

### `vulture info`

```bash
vulture info
```

Expected result:

```text
🦅 VULTURE
Science: chemistry • physics • mathematics • RF
Forensics: offline audit of supplied evidence only
RF-DNA: vulture rf-dna --help
Interactive: vulture --interactive
```

### `vulture status`

```bash
vulture status
```

Reports local deterministic mode, network state, hardware state, and RF transmission state. It is a status command, not a live scan.

---

## RF and physics commands

### Wavelength

```bash
vulture rf-wavelength --frequency-hz 1000000000
```

Expected result:

```json
{
  "frequency_hz": 1000000000.0,
  "wavelength_m": 0.299792458
}
```

This calculates `c / f` using the project’s scientific constant.

### Free-space path loss

```bash
vulture rf-path-loss --frequency-hz 2400000000 --distance-m 10
```

Expected result shape:

```json
{
  "frequency_hz": 2400000000.0,
  "distance_m": 10.0,
  "path_loss_db": 60.046
}
```

This is a supplied-parameter calculation. It does not measure a live link or contact a receiver.

---

## Chemical-RF commands

Show the group help:

```bash
vulture chemical-rf --help
```

### NMR/Larmor frequency

```bash
vulture chemical-rf nmr --nucleus 1H --field-t 7
```

Expected result shape:

```json
{
  "nucleus": "1H",
  "field_t": 7.0,
  "frequency_hz": 298000000.0
}
```

The precise value comes from the project’s nucleus constants.

### Material screening

```bash
vulture chemical-rf material \
  --epsilon-r 4.2 \
  --conductivity 0.01 \
  --frequency-hz 2400000000 \
  --length-m 0.1
```

Expected result shape:

```json
{
  "permittivity": {
    "real": 4.2,
    "imag": -0.0000000007
  },
  "resonance_hz": 730000000.0
}
```

This is an offline screening calculation, not a laboratory material measurement.

### Combined physics calculation

```bash
vulture chemical-rf physics --frequency-hz 2400000000 --distance-m 10
```

Expected result shape:

```json
{
  "wavelength_m": 0.124913524,
  "path_loss_db": 60.046
}
```

### Impedance report

```bash
vulture chemical-rf report \
  --sample-id S-001 \
  --real-ohm 50 \
  --imag-ohm 2.5 \
  --frequency-hz 2400000000
```

The report is explicitly uncalibrated and includes the sample ID, complex impedance, frequency metadata, and analysis fields.

---

## Forensic audit commands

All forensic commands analyze supplied local values or evidence metadata. They do not scan targets or networks.

### Physics audit

```bash
vulture forensic physics \
  --case-id C-001 \
  --subject capture \
  --frequency-hz 2400000000 \
  --distance-m 10 \
  --format json
```

Use `--format txt` for a human-readable report or `--output report.json` to save a report.

### Chemistry audit

```bash
vulture forensic chemistry \
  --case-id C-002 \
  --subject sample \
  --compounds-json '[{"elements":{"H":2,"O":1}}]'
```

### Mathematics audit

```bash
vulture forensic math \
  --case-id C-003 \
  --subject system \
  --matrix-json '[[2,1],[1,1]]' \
  --vector-json '[3,2]'
```

### Protocol/frame audit

```bash
vulture forensic protocol \
  --case-id C-004 \
  --subject frame \
  --frames-json '[{"length":4,"declared_length":5}]'
```

A mismatch may produce a warning finding rather than a silent success. Exact findings are generated from the supplied values.

---

## RF-DNA commands

RF-DNA is one part of VULTURE, not the whole platform. It is included here as an integrated command group:

```bash
vulture rf-dna --help
```

### Simulate and analyze

```bash
vulture rf-dna simulate --profile multi-tone --duration 2 --sample-rate 1000000 --seed 7 --output capture.npz
vulture rf-dna fingerprint --input capture.npz --label lab-device-01
vulture rf-dna dashboard --input capture.npz --label lab-device-01
vulture rf-dna report --input capture.npz --label lab-device-01
```

Expected simulation result:

```json
{
  "output": "capture.npz",
  "profile": "multi-tone",
  "samples": 2000000,
  "seed": 7
}
```

### Quantum/classical research baseline

```bash
vulture rf-dna quantum --profile multi-tone --duration 2 --sample-rate 1000000 --seed 7
```

This runs a bounded local QFT-like comparison and reports a classical FFT baseline. It does not require quantum hardware.

### Optional backend report

```bash
vulture rf-dna backends
```

Expected shape:

```json
{
  "local_npz": true,
  "network_probe": false,
  "simulator": true,
  "soapysdr_installed": false,
  "transmit": false
}
```

---

## Interactive terminal

Start the interactive prompt:

```bash
vulture --interactive
```

Typical session:

```text
🦅 VULTURE — Offline Scientific Intelligence Platform
chemistry • physics • mathematics • RF • forensic audit
Type: help | status | rf-dna status | forensic physics | exit
> help
Available commands:
  info
  status
  rf-wavelength --frequency-hz 1e9
  rf-path-loss --frequency-hz 2.4e9 --distance-m 10
  rf-dna status
  chemical-rf nmr --nucleus 1H --field-t 7
  forensic physics --case-id C-001 --subject capture --frequency-hz 2.4e9 --distance-m 10
  history
  exit
> status
{ ... local status JSON ... }
> history
1: help
2: status
> exit
✓ Session closed safely.
```

Behavior:

- Empty input: no action.
- `help` or `?`: prints the command list.
- `history`: prints previous commands.
- `exit` or `quit`: closes safely.
- Any supported command: executes the same local command logic as the terminal entry point.

---

## GUI

The GUI is optional and remains separate from the terminal so VULTURE can run headlessly.

Launch it from an installed checkout:

```bash
python -c "from vulture.gui import launch_gui; launch_gui()"
```

If PyQt6 is unavailable, the launcher logs that the GUI dependency is not available and returns without affecting CLI use.

The GUI includes the existing platform surfaces:

- **RF Intelligence:** analysis entry points and RF review.
- **SDR/IQ:** receive-oriented workflow controls.
- **Machine Learning:** model and feature workflow entry points.
- **RF-DNA dashboard:** capture summaries and fingerprint review where supported.
- **Provenance viewer:** capture source, authorization, hashes, sample metadata, and review state.

The GUI must be treated as a review and analysis interface. It does not add a transmission capability.

---

## Signal processing and SDR/IQ

VULTURE contains modules for:

- FFT and FFT-engine workflows.
- PSD and spectrogram analysis.
- Waterfall and advanced visualization.
- Peak, burst, occupancy, noise-floor, interference, and anomaly detection.
- IQ reading, writing, recording, playback, metadata extraction, resampling, and format handling.
- RTL-SDR, PlutoSDR, UHD/USRP, and SoapySDR-compatible boundaries when drivers are installed.

The receive adapter requires explicit configuration. Optional hardware tests are marked separately and are skipped by default.

---

## AI/ML and analytics

The platform includes existing AI/ML and analytics areas for:

- feature engineering and preprocessing;
- classical model training and evaluation;
- optional ONNX runtime workflows;
- clustering and anomaly detection;
- real-time and time-series analytics;
- model and plugin boundaries;
- explainable results and operator review.

These components operate on supplied or authorized data. They should not be interpreted as proof of identity, intent, or attribution without independent evidence.

---

## Quantum and scientific research

The optional research layer includes:

- QFT versus classical FFT comparisons;
- small variational or quantum-inspired feature experiments;
- simulated noise and robustness studies;
- reproducible seeds and resource counts;
- classical baselines for interpretable comparison;
- chemistry, physics, spectroscopy, and material-screening workflows.

Quantum features are optional and are not required for ordinary VULTURE operation.

---

## Reports, provenance, and security

VULTURE supports:

- JSON and text reports;
- SHA-256 capture hashes;
- capture provenance records;
- authorization metadata;
- audit-friendly labels and case IDs;
- bounded sample/request sizes;
- tenant isolation for the authenticated service;
- TLS for remote deployments;
- explicit device allowlists;
- plugin permissions and fail-closed controls.

Remote service deployments must use real deployment credentials and certificates. Never commit private keys, bearer tokens, or production secrets.

---

## Testing

Run all tests:

```bash
pytest -q
```

Run coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

Run core command and science tests:

```bash
pytest -q tests/test_cli.py tests/test_forensics.py tests/test_rf_dna.py
```

Optional controlled-lab tests:

```bash
RF_DNA_LAB_HARDWARE=1 RF_DNA_SOAPY_ARGS='driver=approved-device' \
pytest -q -m hardware tests/test_approved_hardware.py
```

Hardware tests are intentionally not part of the normal offline suite.

Expected successful output is generally:

```text
........................................................                 [100%]
XX passed, Y skipped in <time>s
```

The count varies as tests are added; the exit code and failure details are authoritative.

---

## Project structure

```text
VULTURE/
├── README.md
├── pyproject.toml
├── setup.py
├── requirements.txt
├── docs/
│   ├── VULTURE_COMPLETE_COMMANDS.md
│   ├── VULTURE_TERMINAL_COMMANDS.md
│   ├── RF_DNA_COMMAND_GUIDE.md
│   └── RF_DNA_SERVICE.md
├── examples/
├── src/vulture/
│   ├── cli.py
│   ├── gui.py
│   ├── core/
│   ├── chemical_rf/
│   ├── forensic_cli.py
│   ├── forensics/
│   ├── rf_dna/
│   ├── rf_intelligence/
│   ├── rf_fingerprinting_framework/
│   ├── sdr_iq_framework/
│   ├── signal_processing/
│   ├── ml_framework/
│   ├── timeseries_framework/
│   └── visualization_advanced/
├── tests/
└── rf_fingerprinting/
```

---

## Safety and limitations

VULTURE is powerful because it combines many scientific and analytical modules, but results still require human review.

- A fingerprint is a statistical similarity result, not proof of identity.
- A forensic report audits supplied data; it does not establish legal conclusions by itself.
- A simulation is not a measurement from physical hardware.
- A model prediction is not automatically ground truth.
- Optional SDR access must remain receive-only and explicitly authorized.
- No command should be used to interfere with communications or monitor systems without authorization.

Use local simulators and prerecorded captures first. Keep raw evidence, hashes, command lines, seeds, software versions, and operator authorization together for reproducibility.

---

## License and identity

This project retains the VULTURE identity and existing project direction. See [LICENSE](LICENSE) for the repository license and the legal/ethical-use documentation for deployment requirements.

**VULTURE: powerful scientific and defensive analysis, explicit controls, and no unsafe automation.**
