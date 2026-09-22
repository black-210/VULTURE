🦅 VULTURE — Scientific, RF,# 🦅 VULTURE — Autonomous Intelligence & Research Platform

VULTURE is a receive-only RF analysis, scientific tooling, signal-processing, forensics, and chemistry/physics platform built for offline investigation of local data and authorized signals. The project combines a Python CLI, optional scientific modules, RF-DNA workflows, forensic audits, and an isolated C extension layer.

The platform is designed to run locally and deterministically. It does not transmit, actively scan, or control hardware unless the user explicitly configures an approved receive-only adapter for local analysis of authorized signals.

> Safety model: VULTURE is for analysis of supplied, local, or authorized data. It is not a transmission tool, a live target scanner, or an autonomous system for remote exploitation.

---

## Contents

- Overview
- Installation
- Main CLI
- RF and physics commands
- Chemical-RF commands
- Forensic audit commands
- RF-DNA commands
- Interactive terminal
- Signal processing and SDR/IQ
- C extension layer
- Testing
- Project structure
- Safety and limitations

---

## Overview

VULTURE provides a modular set of capabilities across several domains:

- Scientific calculations: RF wavelength, path loss, chemistry screening, NMR frequency, and material analysis.
- Signal processing: FFT, PSD, spectrogram, peak detection, and deterministic local-signal analysis.
- RF-DNA: offline simulation, local fingerprinting, and comparison workflows.
- Forensics: case-based evidence review with local analysis and structured text/JSON reporting.
- Optional Python modules for ML, quantum-inspired research, and visualization.
- Native C tooling for fast analytical helpers and deterministic local processing.

The project keeps a clear separation between:

- local simulations and offline calculations
- file-based evidence analysis
- authorized RF receive-only hardware workflows
- human review and provenance tracking

---

## Installation

Clone the repository:

```bash
git clone https://github.com/black-210/VULTURE.git
cd VULTURE
python -m pip install -e .
```

Install dev tooling if needed:

```bash
python -m pip install -e ".[dev]"
```

Optional scientific dependencies are available through extras:

```bash
python -m pip install -e ".[science]"
python -m pip install -e ".[ml]"
python -m pip install -e ".[security]"
python -m pip install -e ".[gui]"
```

The project is intended to work headlessly in offline environments and should remain usable without hardware drivers or remote services.

---

## Main CLI

List available commands:

```bash
vulture --help
```

The main CLI is organized around a small set of command groups:

```text
vulture info
vulture status
vulture rf-wavelength
vulture rf-path-loss
vulture chemical-rf
vulture forensic
vulture rf-dna
vulture --interactive
```

### `vulture info`

```bash
vulture info
```

Typical output:

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

This reports local deterministic mode, network status, hardware state, and receive/transmit boundaries. It is a status command, not a live measurement.

Expected structure:

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

---

## RF and physics commands

### Wavelength

```bash
vulture rf-wavelength --frequency-hz 1000000000
```

Expected shape:

```json
{
  "frequency_hz": 1000000000.0,
  "wavelength_m": 0.299792458
}
```

This calculates the wavelength based on the local physical constant for the speed of light.

### Path loss

```bash
vulture rf-path-loss --frequency-hz 2400000000 --distance-m 10
```

Expected shape:

```json
{
  "frequency_hz": 2400000000.0,
  "distance_m": 10.0,
  "path_loss_db": 60.046
}
```

This is a local bounded calculation using supplied values. It does not measure a live link or contact a receiver.

---

## Chemical-RF commands

Chemical-RF is grouped under:

```bash
vulture chemical-rf --help
```

### NMR/Larmor frequency

```bash
vulture chemical-rf nmr --nucleus 1H --field-t 7
```

Expected shape:

```json
{
  "nucleus": "1H",
  "field_t": 7.0,
  "frequency_hz": 298000000.0
}
```

### Material screening

```bash
vulture chemical-rf material \
  --epsilon-r 4.2 \
  --conductivity 0.01 \
  --frequency-hz 2400000000 \
  --length-m 0.1
```

Expected shape:

```json
{
  "permittivity": {
    "real": 4.2,
    "imag": -0.0000000007
  },
  "resonance_hz": 730000000.0
}
```

### Combined physics calculation

```bash
vulture chemical-rf physics --frequency-hz 2400000000 --distance-m 10
```

### Impedance report

```bash
vulture chemical-rf report \
  --sample-id S-001 \
  --real-ohm 50 \
  --imag-ohm 2.5 \
  --frequency-hz 2400000000
```

The report is explicitly uncalibrated and includes sample metadata and local analysis values.

---

## Forensic audit commands

All forensic operations analyze supplied evidence or local numerical values. They do not scan targets or live networks.

### Physics audit

```bash
vulture forensic physics \
  --case-id C-001 \
  --subject capture \
  --frequency-hz 2400000000 \
  --distance-m 10 \
  --format json
```

Use `--format txt` for human-readable output or `--output report.json` to persist the audit.

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

These routines generate findings based only on the supplied evidence and local assumptions. They are audit and review tools, not proof of identity or legal conclusion.

---

## RF-DNA commands

RF-DNA is a major subsystem of the project, but it is not the whole platform.

```bash
vulture rf-dna --help
```

### Simulate

```bash
vulture rf-dna simulate --profile multi-tone --duration 2 --sample-rate 1000000 --seed 7 --output capture.npz
```

### Fingerprint

```bash
vulture rf-dna fingerprint --input capture.npz --label lab-device-01
```

### Dashboard

```bash
vulture rf-dna dashboard --input capture.npz --label lab-device-01
```

### Report

```bash
vulture rf-dna report --input capture.npz --label lab-device-01
```

### Quantum/classical baseline

```bash
vulture rf-dna quantum --profile multi-tone --duration 2 --sample-rate 1000000 --seed 7
```

This runs a bounded local comparison using a QFT-like path and a classical FFT baseline. It does not require quantum hardware.

### Hardware/backends status

```bash
vulture rf-dna backends
```

Expected result shape:

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

Start the interactive mode:

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

- blank input does nothing
- `help` or `?` prints available command guidance
- `history` prints commands executed in the session
- `exit` or `quit` exits cleanly
- supported commands run the same local logic as the normal entrance points

---

## Signal processing and SDR/IQ

The project includes modules and patterns for:

- FFT and PSD analysis
- spectrogram and waterfall workflows
- peak, burst, occupancy, and noise-floor detection
- IQ loading, recording, playback, metadata extraction, and resampling
- optional SDR adapter flow for approved hardware
- receive-only boundaries for local analysis

These features are intended to work with local files and authorized devices. They are not meant for remote surveillance or unauthorized emissions.

If SDR drivers are not installed, the platform should degrade safely and keep simulator-based analysis available.

---

## C extension layer

A separate native C layer lives under the `c/` directory. It is deliberately isolated from the Python application and is intended for lightweight analytical tasks, not to replace the Python CLI.

Build the native layer:

```bash
make -C c
```

Representative commands:

```bash
./vulture_cli status
./vulture_cli analyze c/sample_signal.txt
./vulture_cli scan 0.1 1.4 0.2 4.8 0.1 3.2 0.2 5.9
./vulture_cli hash README.md
./vulture_rf_analysis 2400000000 10
./vulture_hash_engine c/sample_signal.txt
```

The C layer focuses on deterministic and local calculations, with standard C11 interfaces and minimal dependencies.

---

## Testing

Run the test suite:

```bash
pytest -q
```

Run coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

Run a smaller but representative subset:

```bash
pytest -q tests/test_cli.py tests/test_forensics.py tests/test_rf_dna.py
```

The repository is designed so that hardware-dependent tests remain optional and disabled by default unless explicitly enabled in a suitable environment.

---

## Project structure

```text
VULTURE/
├── README.md
├── pyproject.toml
├── LICENSE
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
│   ├── chemical_rf/
│   ├── core/
│   ├── forensic_cli.py
│   ├── forensics/
│   ├── rf_dna/
│   ├── rf_intelligence/
│   ├── signal_processing/
│   ├── lab/
│   ├── ml_framework/
│   └── visualization_advanced/
├── tests/
├── c/
└── rf_fingerprinting/
```

---

## Safety and limitations

VULTURE is powerful because it spans multiple scientific and analytical domains, but it remains a local analysis and review platform.

- A fingerprint is a similarity result, not proof of identity.
- A forensic report audits supplied data; it does not establish legal conclusions by itself.
- A simulation is not a live measurement from hardware.
- A model prediction is not ground truth.
- Optional SDR access must remain receive-only and explicitly authorized.
- No command should be used to interfere with communications or monitor systems without permission.
- Local evidence, hashes, command lines, seeds, and operator authorization should remain preserved for auditability and reproducibility.

Use local simulators and offline capture files first. Keep raw evidence and metadata together, and review results with human oversight.

---

## License and identity

This project keeps the VULTURE identity and safety-first direction. See `LICENSE` for the project’s legal framework.

VULTURE is a defensive, scientific, and analytical platform with explicit control boundaries and no unsafe automation.

---

## Final note

The repository already contains a legitimate set of commands and features. The correct approach is to document them accurately, clearly, and consistently rather than expanding the README with invented or misleading content. This rewrite keeps the project honest and useful while making the documentation easier to navigate and maintain.
