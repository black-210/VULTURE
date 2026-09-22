# 🦅 VULTURE — Scientific, RF, SDR/IQ, Forensics, and Research Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![C](https://img.shields.io/badge/C11-native-00599C?logo=c&logoColor=white)](c/README.md)
[![RF](https://img.shields.io/badge/RF%20DNA-receive%20only-0A7B5E)](#rf-dna-and-sdriq)
[![License](https://img.shields.io/badge/License-AGPL--3.0-blue)](LICENSE)

VULTURE is a modular offline-first platform for scientific calculation, RF and SDR/IQ analysis, chemistry, physics, mathematics, forensic review, signal processing, machine learning, visualization, provenance, and reproducible research.

The project combines a Python application layer with an optional native C analysis layer. Python provides the primary user interface, orchestration, simulation, reporting, and extensibility. C provides small, deterministic native tools for bounded signal analysis, file integrity, RF mathematics, and local IQ processing.

> **Identity and scope:** VULTURE is an analysis and research platform. Existing scientific, forensic, RF, Chemical-RF, GUI, ML, quantum-research, Python, and native C features remain part of the project.
>
> **Authorized use only:** use VULTURE only with systems, frequencies, datasets, captures, and receivers that you own or are explicitly authorized to analyze. VULTURE is receive/analyze-only by design and does not provide RF transmission, network scanning, or unauthorized monitoring automation.

---

## Contents

- [What VULTURE provides](#what-vulture-provides)
- [Design principles](#design-principles)
- [Installation](#installation)
- [Fast start](#fast-start)
- [Main CLI](#main-cli)
- [RF and physics](#rf-and-physics)
- [Chemical-RF](#chemical-rf)
- [Forensic audit](#forensic-audit)
- [RF-DNA and SDR/IQ](#rf-dna-and-sdriq)
- [Offline analysis](#offline-analysis)
- [Interactive terminal](#interactive-terminal)
- [GUI](#gui)
- [Signal processing](#signal-processing)
- [AI/ML and analytics](#aiml-and-analytics)
- [Quantum and scientific research](#quantum-and-scientific-research)
- [Reports, provenance, and security](#reports-provenance-and-security)
- [Native C layer](#native-c-layer)
- [C++ and C# interoperability](#c-and-c-interoperability)
- [Public ecosystem references](#public-ecosystem-references)
- [Testing](#testing)
- [Project structure](#project-structure)
- [Limitations and responsible use](#limitations-and-responsible-use)
- [Roadmap](#roadmap)
- [License and identity](#license-and-identity)

---

## What VULTURE provides

### Scientific and engineering tools

- RF wavelength and free-space path-loss calculations.
- Chemistry and RF material screening.
- Complex-permittivity calculations.
- Dielectric half-wave resonance estimates.
- NMR and Larmor-frequency calculations.
- Spectroscopy and signal simulation helpers.
- Physics and mathematics calculations.
- Deterministic simulation profiles for offline experiments.
- Measurement and uncertainty helpers.
- Auditable, explicitly uncalibrated impedance reports.

### RF, SDR, and signal processing

- IQ loading from local files and deterministic simulator fixtures.
- Receive-only boundaries for approved SDR hardware where separately configured.
- FFT, DFT, PSD, spectrogram, waterfall, occupancy, peak, burst, and noise-floor workflows.
- Local anomaly and interference review for owned or authorized data.
- IQ metadata, provenance, hashes, calibration boundaries, and resampling boundaries.
- RF-DNA fingerprinting and capture comparison as descriptive statistical workflows.
- Deterministic seeds for reproducible simulations.
- Local dashboard and report generation.
- C-native IQ statistics, windowing, spectrum, quality, clipping, and correlation helpers.

### Evidence, forensics, and audit

- Offline physics, chemistry, mathematics, and protocol/frame audits.
- Structured JSON and human-readable reports.
- SHA-256 capture and file hashes.
- Case IDs, subject IDs, operator metadata, and review fields.
- Bounded inputs and fail-closed validation.
- Explicit distinction between a statistical result and a legal, identity, or attribution conclusion.

### AI, ML, and analytics

- Classical feature engineering and preprocessing.
- Model evaluation and offline benchmarking.
- Optional deep-learning and ONNX-related components where installed.
- Time-series, anomaly, clustering, and statistical analysis modules.
- Explainable feature reports.
- Human review before consequential decisions.

### GUI and research workflows

- Optional PyQt6 desktop interface.
- RF Intelligence, SDR/IQ, ML, RF-DNA dashboard, and provenance-review surfaces.
- Optional visualization and advanced plotting modules.
- Quantum-inspired experiments with classical baselines.
- Optional lab-only SoapySDR/UHD test markers.

---

## Design principles

VULTURE is built around explicit boundaries rather than hidden automation:

1. **Offline first.** Simulators and local-file workflows work without a network.
2. **Receive-only.** SDR integration is limited to explicitly configured receive workflows.
3. **Explicit inputs.** Commands operate on supplied values, files, or approved local devices.
4. **Fail closed.** Invalid parameters, missing files, malformed data, and unavailable optional dependencies produce errors instead of silently proceeding.
5. **Reproducible results.** Seeds, hashes, metadata, command lines, and software versions can be recorded.
6. **Human review.** Statistical similarity is not proof of identity or attribution.
7. **Layered architecture.** Python, C, optional GUI, and optional hardware adapters have separate responsibilities.
8. **No secret claims.** Reports describe calculations and assumptions instead of overstating certainty.
9. **Bounded resources.** Simulators and parsers impose limits to prevent accidental unbounded allocations.
10. **Reviewable code.** Native modules use small interfaces and explicit ownership.

---

## Installation

```bash
git clone https://github.com/black-210/VULTURE.git
cd VULTURE
python -m pip install -e .
```

Install development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Optional groups are available for additional science, ML, GUI, and security-related integrations:

```bash
python -m pip install -e ".[science]"
python -m pip install -e ".[ml]"
python -m pip install -e ".[gui]"
```

Optional SDR drivers are installed separately according to the operating system, vendor, and laboratory policy. VULTURE’s simulator and local-file workflows must remain usable without them.

---

## Fast start

```bash
vulture info
vulture status
vulture --help
vulture rf-wavelength --frequency-hz 1000000000
vulture rf-path-loss --frequency-hz 2400000000 --distance-m 10
vulture chemical-rf nmr --nucleus 1H --field-t 7
vulture rf-dna status
vulture --interactive
```

The expected status shape is:

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

Exact formatting and additional fields may vary by version. The important properties are that ordinary commands are local, no transmitter is opened, and no network probe is performed.

---

## Main CLI

Show all commands:

```bash
vulture --help
```

The main command exposes the project’s top-level surfaces:

```text
info
status
rf-wavelength
rf-path-loss
chemical-rf
rf-dna
forensic
offline
lab
```

Click parses the command, VULTURE validates its arguments, the local calculation or audit runs, and structured output is printed. Running a calculation does not automatically open a device or contact a service.

### `vulture info`

```bash
vulture info
```

Displays the platform areas, offline mode, RF-DNA entry point, and interactive terminal entry point.

### `vulture status`

```bash
vulture status
```

Reports safe runtime state. This is a status command, not a live scan.

---

## RF and physics

### Wavelength

```bash
vulture rf-wavelength --frequency-hz 1000000000
```

This calculates wavelength using the supplied frequency and the project’s scientific constant.

### Free-space path loss

```bash
vulture rf-path-loss --frequency-hz 2400000000 --distance-m 10
```

This is a supplied-parameter calculation. It does not measure a live link or contact a receiver.

The native equivalent is:

```bash
make -C c
./vulture_rf_analysis 2400000000 10
```

---

## Chemical-RF

Show the command group:

```bash
vulture chemical-rf --help
```

The standalone entry point is also available:

```bash
vulture-chemical-rf --help
```

### NMR/Larmor frequency

```bash
vulture chemical-rf nmr --nucleus 1H --field-t 7
```

The result is an ideal calculation based on project constants. It is not a statement about a measured instrument or sample.

### Material screening

```bash
vulture chemical-rf material \
  --epsilon-r 4.2 \
  --conductivity 0.01 \
  --frequency-hz 2400000000 \
  --length-m 0.1
```

This estimates complex permittivity and a dielectric half-wave resonance. It is an offline screening calculation, not a laboratory measurement.

### Physics calculation

```bash
vulture chemical-rf physics \
  --frequency-hz 2400000000 \
  --distance-m 10
```

### Impedance report

```bash
vulture chemical-rf report \
  --sample-id S-001 \
  --real-ohm 50 \
  --imag-ohm 2.5 \
  --frequency-hz 2400000000
```

Reports are explicitly uncalibrated and should retain their sample ID, frequency metadata, assumptions, and review state.

---

## Forensic audit

Forensic commands analyze supplied local values or metadata. They do not scan targets or networks.

### Physics audit

```bash
vulture forensic physics \
  --case-id C-001 \
  --subject capture \
  --frequency-hz 2400000000 \
  --distance-m 10 \
  --format json
```

Use `--format txt` for a human-readable report or `--output report.json` to save one.

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

A mismatch produces a finding or warning based on the supplied values. A report is an audit of provided data; it does not independently establish a legal conclusion.

---

## RF-DNA and SDR/IQ

RF-DNA is an integrated receive-oriented analysis workflow, not the entire VULTURE platform.

### Check capabilities

```bash
vulture rf-dna status
vulture rf-dna backends
```

The backend report distinguishes local simulation, local NPZ loading, optional installed SDR bindings, transmission capability, and network probing. Transmission and network probing remain disabled in the VULTURE workflow.

### Generate a deterministic local IQ fixture

```bash
vulture rf-dna simulate \
  --profile multi-tone \
  --duration 2 \
  --sample-rate 1000000 \
  --seed 7 \
  --output capture.npz
```

Available simulator profiles include:

- `noise`
- `multi-tone`
- `cw`
- `chirp`

The simulator validates duration, sample rate, sample count, and resource limits. It does not open an SDR.

### Fingerprint a local capture

```bash
vulture rf-dna fingerprint \
  --input capture.npz \
  --label lab-device-01
```

The result is a descriptive fingerprint derived from the supplied capture. It is not proof of identity.

### Dashboard and report

```bash
vulture rf-dna dashboard --input capture.npz --label lab-device-01
vulture rf-dna report --input capture.npz --label lab-device-01
```

### Quantum/classical baseline

```bash
vulture rf-dna quantum \
  --profile multi-tone \
  --duration 2 \
  --sample-rate 1000000 \
  --seed 7
```

This is a bounded local research comparison with a classical baseline. It does not require quantum hardware.

### Receive-only adapter

The receive adapter accepts local NPZ captures and can optionally use an explicitly configured approved receiver when the relevant bindings and laboratory configuration exist. It does not discover devices, scan frequencies, transmit, or contact networks.

---

## Offline analysis

The project also includes dependency-light local analysis helpers under `src/vulture/offline_tools/`.

Example:

```bash
vulture offline --help
vulture offline analyze measurements.txt
vulture offline analyze measurements.txt --sample-rate 1000
```

The offline toolkit provides:

- descriptive statistics
- RMS, variance, median, and peak-to-peak calculations
- thresholded peak detection
- Hann and related window helpers
- dependency-light DFT analysis
- dominant-frequency estimates
- finite-value validation
- SHA-256 provenance helpers
- uncertainty combination
- dielectric resonance helpers
- deterministic JSON reports
- local numeric-file loading
- audit metadata and calibration-status warnings

These functions operate on supplied local data and do not provide network, hardware, or transmission behavior.

---

## Interactive terminal

Start the prompt:

```bash
vulture --interactive
```

Typical commands include:

```text
> help
> info
> status
> rf-wavelength --frequency-hz 1e9
> rf-path-loss --frequency-hz 2.4e9 --distance-m 10
> chemical-rf nmr --nucleus 1H --field-t 7
> rf-dna status
> forensic physics --case-id C-001 --subject capture --frequency-hz 2.4e9 --distance-m 10
> history
> exit
```

The interactive shell maps to the same Click commands as the normal terminal entry point. Empty input does nothing. `help` prints commands. `history` prints prior commands. `exit` and `quit` close safely.

---

## GUI

The GUI is optional and separate from the terminal so VULTURE can run headlessly.

```bash
python -c "from vulture.gui import launch_gui; launch_gui()"
```

If PyQt6 is unavailable, command-line workflows remain usable.

The GUI may include:

- RF Intelligence review
- SDR/IQ workflow controls
- ML and feature workflow entry points
- RF-DNA dashboards
- provenance viewers
- visualization surfaces
- report review

The GUI is an analysis and review interface. It does not add transmission capability.

---

## Signal processing

VULTURE’s signal-processing areas include:

- FFT and DFT workflows
- PSD and spectrogram analysis
- waterfall and advanced visualization
- peak, burst, occupancy, noise-floor, and anomaly analysis
- IQ reading and writing
- metadata and provenance handling
- local resampling boundaries
- deterministic simulator fixtures
- receive-only adapter boundaries for optional approved hardware

Signal processing results depend on sample rate, sample format, windowing, calibration, clipping, noise, and capture quality. Reports should preserve those assumptions.

---

## AI/ML and analytics

The platform includes areas for:

- feature engineering and preprocessing
- classical model training and evaluation
- optional ONNX runtime workflows
- clustering and anomaly detection
- time-series analytics
- model and plugin boundaries
- explainable results
- operator review

Models operate on supplied or authorized data. A prediction is not automatically ground truth, identity, intent, or attribution.

---

## Quantum and scientific research

Optional research features include:

- QFT versus classical FFT comparisons
- quantum-inspired feature experiments
- simulated noise and robustness studies
- reproducible seeds and resource counts
- classical baselines
- chemistry, physics, spectroscopy, and material-screening workflows

These are research and simulation tools. Quantum features are optional and are not required for ordinary VULTURE operation.

---

## Reports, provenance, and security

VULTURE supports or provides boundaries for:

- JSON and text reports
- SHA-256 capture hashes
- local file hashes
- capture provenance records
- authorization metadata
- case IDs and audit labels
- bounded sample and request sizes
- explicit device allowlists for controlled integrations
- plugin permission boundaries
- fail-closed controls

Keep raw evidence, hashes, command lines, seeds, software versions, sample metadata, and authorization records together when reproducibility matters.

Remote deployments, where separately configured, must use real credentials, certificates, access controls, and secret-management practices. Never commit private keys, bearer tokens, passwords, or production secrets.

---

## Native C layer

The `c/` directory is VULTURE’s standalone native analysis layer.

Build it with:

```bash
make -C c
```

Clean generated binaries with:

```bash
make -C c clean
```

The C layer includes:

- `vulture_cli` for scalar signal analysis and hashing
- RF wavelength/path-loss calculations
- a local hash engine
- a text-to-C translation utility
- receive-only IQ analysis
- IQ text and binary readers
- Hann/Hamming window functions
- DFT-based dominant-frequency analysis
- IQ health metrics
- clipping and correlation checks
- deterministic JSON-like reports
- focused self-test modules
- C++ linkage declarations
- C#-friendly ABI declarations

Example commands:

```bash
./vulture_cli status
./vulture_cli demo
./vulture_cli analyze c/sample_signal.txt
./vulture_cli scan 0.1 1.4 0.2 4.8
./vulture_cli hash c/README.md
./vulture_rf_analysis 2400000000 10
./vulture_hash_engine c/README.md
```

For local IQ text files:

```text
1.0,0.0
0.7,0.7
0.0,1.0
-0.7,0.7
```

The native IQ workflow is designed to report descriptive metrics such as DC offsets, RMS, mean power, peak magnitude, crest factor, phase statistics, frequency estimates, IQ correlation, gain imbalance, and clipping fraction. It does not infer transmitter identity or provide attribution.

See [`c/README.md`](c/README.md) for the native-layer architecture, files, compiler workflow, safety model, and detailed C documentation.

---

## C++ and C# interoperability

The native interfaces include small compatibility headers:

- `c/vulture_cpp.h` provides C++ linkage guards.
- `c/vulture_csharp_abi.h` provides a C-ABI-oriented declaration surface for managed wrappers.

These headers are intentionally narrow. A wrapper should expose explicit local-file analysis functions, validate sizes and return codes, and preserve the same receive-only and offline boundaries as the native code.

They are compatibility declarations, not a full C++ or C# radio SDK and not a mechanism for hidden device access.

---

## Public ecosystem references

VULTURE can be used alongside public Linux, radio, SDR, and security ecosystems, but external package repositories are references rather than hidden dependencies of the project.

### BlackArch radio resources

- BlackArch radio page: <https://blackarch.org/radio.html>
- BlackArch official package repository: <https://github.com/BlackArch/blackarch-pkgbuilds>

### Pentoo resources

- Pentoo official overlay: <https://github.com/pentoo/pentoo-overlay>

These resources may help users discover publicly maintained packages and radio-related tooling. Always review package contents, licenses, permissions, device behavior, and legal requirements before installation or use. Their existence does not expand VULTURE’s capabilities or change its receive-only safety model.

---

## Testing

Run the Python test suite:

```bash
pytest -q
```

Run coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

Run selected core tests:

```bash
pytest -q tests/test_cli.py tests/test_forensics.py tests/test_rf_dna.py
```

Build and exercise the native layer:

```bash
make -C c clean
make -C c
./vulture_cli status
./vulture_cli demo
./vulture_cli analyze c/sample_signal.txt
./vulture_rf_analysis 1000000000 10
./vulture_hash_engine c/README.md
```

Use optional hardware tests only in an explicitly configured and authorized laboratory environment:

```bash
RF_DNA_LAB_HARDWARE=1 \
RF_DNA_SOAPY_ARGS='driver=approved-device' \
pytest -q -m hardware tests/test_approved_hardware.py
```

Hardware tests are intentionally skipped by the ordinary offline suite.

For native memory checking where available:

```bash
gcc -std=c11 -Wall -Wextra -Wpedantic -g \
  -fsanitize=address,undefined \
  -I c -o vulture_cli_sanitized \
  c/vulture_cli.c c/vulture_core.c -lm
```

---

## Project structure

```text
VULTURE/
├── README.md
├── LICENSE
├── pyproject.toml
├── setup.py
├── requirements.txt
├── c/
│   ├── README.md
│   ├── Makefile
│   ├── vulture_core.c
│   ├── vulture_core.h
│   ├── vulture_cli.c
│   ├── vulture_sdr.c
│   ├── vulture_sdr.h
│   ├── vulture_iq_*.c
│   ├── vulture_iq_*.h
│   ├── engines/
│   ├── translator/
│   └── docs/
├── docs/
│   ├── VULTURE_COMPLETE_COMMANDS.md
│   ├── VULTURE_TERMINAL_COMMANDS.md
│   ├── RF_DNA_COMMAND_GUIDE.md
│   ├── RF_DNA_SERVICE.md
│   └── DUAL_USE_LAB.md
├── examples/
├── src/vulture/
│   ├── cli.py
│   ├── gui.py
│   ├── chemical_rf/
│   ├── core/
│   ├── forensics/
│   ├── offline_tools/
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

## Limitations and responsible use

VULTURE is powerful because it combines many scientific and analytical modules, but every result requires appropriate human review.

- A fingerprint is a statistical similarity result, not proof of identity.
- A forensic report audits supplied data; it does not establish legal conclusions by itself.
- A simulation is not a measurement from physical hardware.
- A model prediction is not automatically ground truth.
- A mathematical estimate is not a calibration certificate.
- Optional SDR access must remain receive-only and explicitly authorized.
- No command should be used to interfere with communications.
- No command should be used to monitor systems without authorization.
- Public package repositories must be reviewed independently before installation.
- Captures may contain sensitive information and should be handled according to applicable policy and law.
- Results depend on sample quality, metadata, calibration, clipping, noise, windowing, and assumptions.

Use local simulators and prerecorded captures first. Keep raw evidence, hashes, command lines, seeds, software versions, and operator authorization together for reproducibility.

---

## Roadmap

Future work may include:

1. bounded streaming statistics
2. more structured report serialization
3. benchmark and profiling harnesses
4. reusable parser utilities
5. expanded hashing test vectors
6. improved IQ format validation
7. richer windowing and spectral metrics
8. local provenance metadata helpers
9. stable native wrapper functions for approved C++ and C# integrations
10. improved documentation and examples
11. additional deterministic simulator profiles
12. better cross-platform build coverage
13. clearer calibration and uncertainty metadata

New features should remain local, reviewable, dependency-light, and compatible with the existing VULTURE safety model. The project should not gain broad, implicit, or opaque operational behavior merely because a feature is technically possible.


## Linux Distribution Support

VULTURE is currently packaged and available in security-focused Linux ecosystems:

- **BlackArch Linux:** `vulture-black`
  https://blackarch.org/radio.html

- **Pentoo Linux:** `net-wireless/vulture`
  https://github.com/pentoo/pentoo-overlay

- **Source Repository:**
  https://github.com/black-210/VULTURE


---

## License and identity

VULTURE retains its project identity and existing direction. See [LICENSE](LICENSE) for the repository license and the project’s legal and ethical-use documentation for deployment requirements.

**VULTURE: scientific and defensive analysis, explicit controls, reproducible evidence, and no unsafe automation.**


